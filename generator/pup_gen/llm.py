"""Klienci modelu językowego: `KlientClaude` (API Anthropic) i `KlientAtrapa` (offline, deterministyczny).

Prawdziwe wywołanie włącza się zmienną środowiskową ANTHROPIC_API_KEY (albo `ant auth login`);
bez niej CLI używa atrapy. Logi zawierają tylko id pola, długości i liczbę tokenów – bez treści.
"""

from __future__ import annotations

import datetime as dt
import logging
import os
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from .schemat import Kwestionariusz

log = logging.getLogger(__name__)

DOMYSLNY_MODEL = "claude-opus-5-5"
DOMYSLNY_EFFORT = "high"
BETA_FALLBACK = "server-side-fallback-2026-07-01"


class BladLLM(RuntimeError):
    pass


@dataclass
class ZapytanieLLM:
    system: str          # prompt systemowy z szablony/00 – cache 1
    dane_klienta: str    # <kwestionariusz> + <arkusz> + <regulamin_pup> – cache 2 (wspólne dla pól klienta)
    szablony: str        # <szablon_sekcji> – cache 3
    polecenie: str       # <parametry> + prompt sekcji – zmienne
    pole_id: str
    sekcje: list[str]
    limit_znakow: int
    kontekst: dict[str, Any] = field(default_factory=dict)  # tylko dla atrapy, nie trafia do API

    def tresc_uzytkownika(self) -> list[dict[str, Any]]:
        return [
            {"type": "text", "text": self.dane_klienta, "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": self.szablony, "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": self.polecenie},
        ]


@dataclass
class OdpowiedzLLM:
    tekst_surowy: str
    model: str
    tokeny: dict[str, int] = field(default_factory=dict)
    tresc_asystenta: Any = None   # bloki odpowiedzi do dopisania w kolejnej turze (bez zmian)
    stop_reason: str | None = None


class KlientLLM(Protocol):
    model: str

    def generuj(self, zapytanie: ZapytanieLLM, poprawka: str | None = None,
                poprzednia: OdpowiedzLLM | None = None) -> OdpowiedzLLM: ...


# =========================================================================== Claude
class KlientClaude:
    """SDK `anthropic`: adaptive thinking, effort, prompt caching (3 punkty), fallback po odmowie, retry SDK."""

    def __init__(self, model: str | None = None, effort: str | None = None, max_tokens: int = 16000,
                 max_retries: int = 4, timeout: float = 600.0, fallback: bool = True, klient: Any = None):
        import anthropic

        self.model = model or os.environ.get("PUP_GEN_MODEL", DOMYSLNY_MODEL)
        self.effort = effort or os.environ.get("PUP_GEN_EFFORT", DOMYSLNY_EFFORT)
        self.max_tokens = max_tokens
        self.fallback = fallback
        self._anthropic = anthropic
        self.klient = klient or anthropic.Anthropic(max_retries=max_retries, timeout=timeout)

    def _parametry(self, zapytanie: ZapytanieLLM, poprawka: str | None,
                   poprzednia: OdpowiedzLLM | None) -> dict[str, Any]:
        messages: list[dict[str, Any]] = [{"role": "user", "content": zapytanie.tresc_uzytkownika()}]
        if poprzednia is not None and poprawka:
            # historia tylko dopisywana (append-only) – bloki asystenta wracają bez zmian
            messages += [{"role": "assistant", "content": poprzednia.tresc_asystenta},
                         {"role": "user", "content": poprawka}]
        params: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system": [{"type": "text", "text": zapytanie.system, "cache_control": {"type": "ephemeral"}}],
            "messages": messages,
            "thinking": {"type": "adaptive"},
            "output_config": {"effort": self.effort},
        }
        if self.fallback:
            params["betas"] = [BETA_FALLBACK]
            params["fallbacks"] = "default"
        return params

    def generuj(self, zapytanie: ZapytanieLLM, poprawka: str | None = None,
                poprzednia: OdpowiedzLLM | None = None) -> OdpowiedzLLM:
        a = self._anthropic
        params = self._parametry(zapytanie, poprawka, poprzednia)
        try:
            with self.klient.beta.messages.stream(**params) as stream:
                msg = stream.get_final_message()
        except a.BadRequestError as e:
            raise BladLLM(f"Błędne zapytanie (400) dla pola {zapytanie.pole_id}: {e.message}") from e
        except a.AuthenticationError as e:
            raise BladLLM("Nieprawidłowy klucz API (ANTHROPIC_API_KEY).") from e
        except a.PermissionDeniedError as e:
            raise BladLLM("Klucz API nie ma uprawnień do tego modelu lub funkcji.") from e
        except a.NotFoundError as e:
            raise BladLLM(f"Nieznany model: {self.model}") from e
        except a.RateLimitError as e:
            raise BladLLM("Limit zapytań (429) – SDK ponawiał bez skutku; spróbuj później.") from e
        except a.APIStatusError as e:
            raise BladLLM(f"Błąd API {e.status_code} po ponowieniach.") from e
        except a.APIConnectionError as e:
            raise BladLLM("Brak połączenia z API Anthropic.") from e

        if msg.stop_reason == "refusal":
            kategoria = getattr(getattr(msg, "stop_details", None), "category", None)
            raise BladLLM(f"Model odmówił odpowiedzi dla pola {zapytanie.pole_id} (kategoria: {kategoria}).")
        if msg.stop_reason == "max_tokens":
            raise BladLLM(f"Odpowiedź dla pola {zapytanie.pole_id} ucięta (max_tokens={self.max_tokens}).")
        tekst = "".join(b.text for b in msg.content if b.type == "text")
        u = msg.usage
        tokeny = {
            "wejscie": u.input_tokens or 0,
            "wyjscie": u.output_tokens or 0,
            "cache_odczyt": u.cache_read_input_tokens or 0,
            "cache_zapis": u.cache_creation_input_tokens or 0,
        }
        log.info("pole=%s model=%s tokeny=%s request_id=%s", zapytanie.pole_id, msg.model, tokeny,
                 getattr(msg, "_request_id", None))
        return OdpowiedzLLM(tekst_surowy=tekst, model=msg.model, tokeny=tokeny,
                            tresc_asystenta=msg.content, stop_reason=msg.stop_reason)

    def policz_tokeny(self, zapytanie: ZapytanieLLM) -> int:
        """Dokładna liczba tokenów wejścia (endpoint count_tokens)."""
        wynik = self.klient.messages.count_tokens(
            model=self.model,
            system=[{"type": "text", "text": zapytanie.system}],
            messages=[{"role": "user", "content": zapytanie.tresc_uzytkownika()}],
        )
        return wynik.input_tokens


# =========================================================================== atrapa
_MIESIACE_DOP = ["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca", "lipca", "sierpnia",
                 "września", "października", "listopada", "grudnia"]
_MESKIE_NA_A = {"kuba", "barnaba", "bonawentura", "kosma"}
_RE_ARK = re.compile(r"\{\{(ark_[a-z0-9_]+)\}\}")


def _zl(x: float) -> str:
    from .finanse import liczba_pl
    return f"{liczba_pl(x, 0 if float(x).is_integer() else 2)} zł"


def _male(nazwa: str) -> str:
    return nazwa[:1].lower() + nazwa[1:]


def _zdania(tekst: str | None) -> list[str]:
    if not tekst:
        return []
    czesci = re.split(r"(?<=[.!?])\s+(?=[A-ZĄĆĘŁŃÓŚŹŻ„\"])", tekst.strip())
    return [c if c.endswith((".", "!", "?")) else c + "." for c in czesci if c]


class KlientAtrapa:
    """Deterministyczny tekst z faktów kwestionariusza i zmiennych {{ark_*}}, o długości 85–98% limitu.

    Służy do testów i trybu --dry-run: sprawdza cały przebieg (prompty, podstawianie zmiennych,
    kontrola, DOCX) bez klucza API. To nie jest tekst do wysłania klientowi.
    """

    model = "atrapa-offline"

    def generuj(self, zapytanie: ZapytanieLLM, poprawka: str | None = None,
                poprzednia: OdpowiedzLLM | None = None) -> OdpowiedzLLM:
        kw: Kwestionariusz = zapytanie.kontekst["kwestionariusz"]
        ark: dict[str, str] = zapytanie.kontekst.get("ark", {})
        limit = zapytanie.limit_znakow
        if poprawka:
            m = re.search(r"o co najmniej (\d+)", poprawka)
            limit = max(200, limit - (int(m.group(1)) if m else limit // 10))
        akapity: list[list[str]] = []
        for s in zapytanie.sekcje:
            akapity += self._akapity(s, kw, zapytanie.kontekst.get("format", "tekst"),
                                     zapytanie.kontekst.get("wariant", "standard"))
        tekst = self._dopasuj(akapity, kw, zapytanie.sekcje, limit, ark)
        zmienne = sorted(set(_RE_ARK.findall(tekst)))
        braki = re.findall(r"\[BRAK DANYCH:[^\]]*\]", tekst)
        surowy = (
            f"<tekst>\n{tekst}\n</tekst>\n<kontrola>\n"
            f"- liczba_znakow_ze_spacjami: {len(self._podstaw(tekst, ark))}\n- limit: {zapytanie.limit_znakow}\n"
            f"- uzyte_fakty: {', '.join('K' + s for s in zapytanie.sekcje)} (atrapa)\n"
            f"- braki: {'; '.join(braki) or 'brak'}\n- zmienne_arkusza: {', '.join(zmienne) or 'brak'}\n"
            "- ryzyka_dla_weryfikujacego: tekst z atrapy (tryb offline) – nie wysyłać klientowi\n</kontrola>"
        )
        dl_wej = sum(len(x) for x in (zapytanie.system, zapytanie.dane_klienta, zapytanie.szablony,
                                      zapytanie.polecenie))
        return OdpowiedzLLM(tekst_surowy=surowy, model=self.model, stop_reason="end_turn",
                            tokeny={"wejscie": dl_wej // 3, "wyjscie": len(surowy) // 3,
                                    "cache_odczyt": 0, "cache_zapis": 0})

    # ------------------------------------------------------------------ dopasowanie długości
    @staticmethod
    def _podstaw(tekst: str, ark: dict[str, str]) -> str:
        return _RE_ARK.sub(lambda m: ark.get(m.group(1), m.group(0)), tekst)

    def _dopasuj(self, akapity: list[list[str]], kw: Kwestionariusz, sekcje: list[str], limit: int,
                 ark: dict[str, str]) -> str:
        cel_min, cel_max = int(limit * 0.88), int(limit * 0.98)
        wynik: list[list[str]] = []
        dlugosc = 0

        def dodaj(zrodlo: list[list[str]]) -> None:
            nonlocal dlugosc
            for akapit in zrodlo:
                biezacy: list[str] = []
                for zdanie in akapit:
                    dl = len(self._podstaw(zdanie, ark)) + 1
                    if dlugosc + dl > cel_max:
                        continue
                    biezacy.append(zdanie)
                    dlugosc += dl
                if biezacy:
                    wynik.append(biezacy)
                    dlugosc += 1
                if dlugosc >= cel_min:
                    return

        dodaj(akapity)
        for s in ("01", "02", "03", "04", "07"):  # uzupełnienie faktami z innych sekcji
            if dlugosc >= cel_min:
                break
            if s not in sekcje:
                dodaj(self._akapity(s, kw, "tekst")[1:])
        return "\n\n".join("\n".join(a) if any(z.startswith("– ") for z in a) else " ".join(a) for a in wynik)

    # ------------------------------------------------------------------ treść sekcji
    def _akapity(self, sekcja: str, kw: Kwestionariusz, format_pola: str,
                 wariant: str = "standard") -> list[list[str]]:
        kobieta = kw.osoba.imie.lower().endswith("a") and kw.osoba.imie.lower() not in _MESKIE_NA_A

        def r(k: str, m: str) -> str:
            return k if kobieta else m

        lok, pom, kwal = kw.lokalizacja, kw.pomysl, kw.kwalifikacje
        start = pom.data_startu
        miesiac = f"{_MIESIACE_DOP[start.month - 1]} {start.year} r."
        uslugi = [f"{_male(u.nazwa)} – {_zl(u.cena)}" for u in kw.uslugi]
        glowna = next((u for u in kw.uslugi if u.glowna), kw.uslugi[0])
        obszar = ", ".join(lok.obszar) or lok.miejscowosc

        if sekcja == "01":
            otwarcie = {
                "rzeczowy": f"Od {miesiac} prowadzę jednoosobową działalność w miejscowości {lok.miejscowosc}.",
                "ciepły": f"Od {miesiac} chcę pracować na własny rachunek, u siebie w okolicy: {obszar}.",
                "techniczny": f"Termin rozpoczęcia działalności: {miesiac[:-3]} r., miejsce: {lok.miejscowosc}.",
            }[kw.ton]
            p1 = [otwarcie] + _zdania(pom.opis)[:3]
            p2 = [f"Usługa główna: {_male(glowna.nazwa)} – {_zl(glowna.cena)}.",
                  "Cennik pozostałych usług: " + "; ".join(x for x in uslugi if not x.startswith(_male(glowna.nazwa))) + "."]
            p3 = []
            if lok.tryb == "mobilnie":
                p3.append(f"Pracuję u klientów, w miejscowościach: {obszar}.")
            else:
                p3.append(f"Miejsce pracy: {lok.ulica + ', ' if lok.ulica else ''}{lok.miejscowosc} ({lok.tryb}).")
                p3 += _zdania(lok.opis_lokalu)
            if lok.promien_km:
                p3.append(f"Zasięg dojazdu: do {lok.promien_km:g} km.")
            if lok.dojazd:
                p3.append(f"Dojazd: {lok.dojazd}.")
            if lok.godziny_pracy:
                p3.append(f"Godziny pracy: {lok.godziny_pracy}.")
            if lok.przyjmowanie_zlecen:
                p3.append(f"Zlecenia przyjmuję {lok.przyjmowanie_zlecen}.")
            p4 = [f"PKD 2025: {p.kod} {p.nazwa}." for p in pom.pkd] or \
                 ["[BRAK DANYCH: kod PKD 2025 – dobiera właściciel, nie model]"]
            p4.append(f"Forma prawna: {kw.forma.forma_prawna}.")
            p4.append({
                "ryczałt": f"Opodatkowanie: ryczałt od przychodów ewidencjonowanych, stawka "
                           f"{str(round((kw.forma.stawka_ryczaltu or 0) * 100, 1)).replace('.', ',').removesuffix(',0')}%.",
                "skala": "Opodatkowanie: zasady ogólne (skala podatkowa).",
                "liniowy": "Opodatkowanie: podatek liniowy.",
                "nie wiem": "[BRAK DANYCH: forma opodatkowania – decyzja klienta lub księgowej]",
            }[kw.forma.opodatkowanie])
            p4.append({"zwolniony": "Korzystam ze zwolnienia podmiotowego z VAT.",
                       "czynny": "Od początku będę czynnym podatnikiem VAT.",
                       "nie wiem": "[BRAK DANYCH: status VAT]"}[kw.forma.vat])
            p5 = _zdania(pom.motywacja) + ["Swoje przygotowanie zawodowe opisuję w części o kwalifikacjach."]
            if wariant == "krótki":  # przy krótkim polu dane formalne mają pierwszeństwo przed opisem dojazdu
                return [p1[:2], p2, p4, p3, p5]
            return [p1, p2, p3, p4, p5]

        if sekcja == "02":
            wyk = []
            for w in kwal.wyksztalcenie:
                opis = ", ".join(x for x in (w.poziom, w.kierunek, w.szkola) if x)
                wyk.append(f"{opis}{f' ({w.rok} r.)' if w.rok else ''}")
            p1 = ["Wykształcenie i dyplomy: " + "; ".join(wyk) + "."]
            p2 = []
            for k in kwal.kursy:
                rok = f"W {k.rok} r." if k.rok else f"[BRAK DANYCH: rok kursu „{k.nazwa}”]"
                dodatki = ", ".join(x for x in (k.organizator, f"{k.godziny} h" if k.godziny else None) if x)
                p2.append(f"{rok} {r('ukończyłam', 'ukończyłem')} kurs „{k.nazwa}”{f' ({dodatki})' if dodatki else ''}.")
            p3 = [f"{p.od}–{p.do}: {p.stanowisko}, {p.pracodawca}{f' ({p.miejscowosc})' if p.miejscowosc else ''}. "
                  f"Zakres: {p.obowiazki}." for p in kwal.doswiadczenie]
            p4 = [f"Doświadczenie nieformalne: {kwal.nieformalne}"] if kwal.nieformalne else []
            p5 = []
            if kwal.inne_umiejetnosci:
                p5.append(f"Umiejętności przydatne w firmie: {kwal.inne_umiejetnosci}.")
            if kw.forma.ksiegowosc:
                p5.append(f"Księgowość: {kw.forma.ksiegowosc}.")
            p5.append(f"Szkolenie z zakładania firmy: {kwal.szkolenie_pup}." if kwal.szkolenie_pup else
                      "[BRAK DANYCH: czy było szkolenie z zakładania firmy, np. w PUP – nazwa i rok]")
            p6 = [f"Do wniosku dołączam: {', '.join(kwal.dokumenty)}."] if kwal.dokumenty else []
            return [p1, p3, p2, p4, p5, p6]

        if sekcja == "03":
            p1 = [f"Obszar działania: {obszar}" + (f", do {lok.promien_km:g} km." if lok.promien_km else ".")]
            p1 += [f"{d.opis} (źródło: {d.zrodlo})." for d in kw.klienci.dane_o_terenie] or \
                  ["[BRAK DANYCH: liczba mieszkańców obszaru działania – źródło GUS BDL]"]
            p2 = [f"{i}. {s.nazwa.capitalize()}: {s.opis}{f' ({s.liczba})' if s.liczba else ''}."
                  for i, s in enumerate(kw.klienci.segmenty, 1)]
            p3 = []
            if kw.klienci.dowody_popytu:
                p3.append(f"Popyt {r('sprawdziłam', 'sprawdziłem')} przed złożeniem wniosku: "
                          + "; ".join(kw.klienci.dowody_popytu) + ".")
            p3 += [f"List intencyjny ({li.status}): {li.od_kogo} – {li.czego_dotyczy}"
                   f"{f', {li.czestotliwosc}' if li.czestotliwosc else ''}." for li in kw.listy_intencyjne]
            p4 = ([f"Sezonowość: {pom.sezonowosc_opis}"] if pom.sezonowosc_opis else []) + \
                 [f"{r('Uwzględniłam', 'Uwzględniłem')} to w prognozie sprzedaży."
                  if pom.sezonowosc != "nie" else "Popyt jest podobny przez cały rok."]
            p5 = ["Te dowody popytu są podstawą liczby usług przyjętej w prognozie."]
            return [p1, p2, p3, p4, p5]

        if sekcja == "04":
            ko = kw.konkurencja
            p1 = [f"Konkurencję {r('sprawdziłam', 'sprawdziłem')}"
                  f"{f' ({ko.data_rozpoznania})' if ko.data_rozpoznania else ''} na obszarze: {obszar}."]
            akapity = [p1]
            for c in ko.konkurenci:
                zd = [f"{c.nazwa} ({c.miejscowosc}): {c.oferta}.",
                      f"Ceny: {c.ceny}{f' (źródło: {c.zrodlo_cen})' if c.zrodlo_cen else ''}.",
                      f"Słabe strony: {c.slabe_strony}."]
                if c.mocne_strony:
                    zd.append(f"Mocna strona: {c.mocne_strony}.")
                akapity.append(zd)
            if ko.substytuty:
                akapity.append([f"Klienci mogą też wybrać: {', '.join(ko.substytuty)}."])
            akapity.append([f"Czym się wyróżniam: {ko.przewaga}", "Moje ceny: " + "; ".join(uslugi) + "."])
            return akapity

        if sekcja == "05":
            m = kw.marketing
            p1 = [f"Promocję kieruję do grup: {', '.join(s.nazwa for s in kw.klienci.segmenty)}.",
                  f"Główny kanał: {m.kanaly[0]}."]
            p2 = ["Kanały promocji: " + "; ".join(m.kanaly) + "."]
            reklama = [z for z in kw.zakupy if z.kategoria == "reklama"]
            p3 = [f"{z.nazwa} – {_zl(z.kwota_do_rozliczenia(kw.vat_czynny))}." for z in reklama]
            p3.append("Bieżący budżet reklamy: {{ark_reklama_mies}} miesięcznie.")
            p4 = [f"– {d}" for d in m.pierwsze_dzialania]
            p4.append(f"– cel: {m.cele}" if m.cele else "– [BRAK DANYCH: ilu klientów chcę mieć po 3 miesiącach]")
            p5 = ["Utrzymanie klientów: " + "; ".join(m.utrzymanie) + "."] if m.utrzymanie else []
            return [p1, p2, p3, ["Plan pierwszych 90 dni:"] + p4 if p4 else [], p5]

        if sekcja == "06":
            rodzaj = "netto, bo jestem czynnym podatnikiem VAT" if kw.vat_czynny else "brutto, bo nie płacę VAT"
            p1 = ["Z dotacji przeznaczę {{ark_kosztorys_dotacja}}, a z wkładu własnego {{ark_kosztorys_wklad}}.",
                  f"Kwoty podaję {rodzaj}."]
            akapity = [p1]
            zmienne = {"sprzęt": "ark_kat_sprzet", "towar": "ark_kat_towar", "reklama": "ark_kat_reklama",
                       "remont": "ark_kat_remont", "inne": "ark_kat_inne"}
            for kat, zm in zmienne.items():
                pozycje = [z for z in kw.zakupy if z.kategoria == kat and z.finansowanie == "dotacja"]
                if not pozycje:
                    continue
                opisy = [f"{z.nazwa} ({_zl(z.kwota_do_rozliczenia(kw.vat_czynny))}, {z.stan}"
                         f"{f', {z.ilosc} szt.' if z.ilosc > 1 else ''}): {z.uzasadnienie}." for z in pozycje]
                if format_pola == "tabela":
                    akapity += [[o] for o in opisy]
                else:
                    akapity.append([f"{kat.capitalize()} – {{{{{zm}}}}}."] + opisy)
            wklad = [z for z in kw.zakupy if z.finansowanie == "wkład własny"]
            if wklad:
                akapity.append(["Z wkładu własnego: " + "; ".join(
                    f"{z.nazwa} ({_zl(z.kwota_do_rozliczenia(kw.vat_czynny))}) – {z.uzasadnienie}" for z in wklad) + "."])
            if kw.zasoby_posiadane:
                akapity.append([f"Mam już: {', '.join(z.nazwa for z in kw.zasoby_posiadane)}, "
                                "więc nie ujmuję tego w kosztorysie."])
            return akapity

        if sekcja == "07":
            s = [f"– {p.stanowisko}, {p.pracodawca} ({p.od}–{p.do})" for p in kwal.doswiadczenie[:3]]
            s += [f"– kurs „{k.nazwa}”" for k in kwal.kursy[:2]]
            s += [f"– {z.nazwa}" for z in kw.zasoby_posiadane[:2]]
            w = [f"– {x.ryzyko}{f' ({x.zapobieganie})' if x.zapobieganie else ''}" for x in kw.ryzyka[:3]] or \
                ["– [BRAK DANYCH: słabe strony według klienta]"]
            o = [f"– {d}" for d in kw.klienci.dowody_popytu[:3]]
            o += [f"– {c.nazwa}: {c.slabe_strony}" for c in kw.konkurencja.konkurenci[:2]]
            t = ([f"– sezonowość: {pom.sezonowosc_opis}"] if pom.sezonowosc_opis else [])
            t += [f"– {c.nazwa}: {c.mocne_strony}" for c in kw.konkurencja.konkurenci if c.mocne_strony][:2]
            t += [f"– {x.ryzyko}" for x in kw.ryzyka[3:5]]
            return [["Mocne strony:"] + s, ["Słabe strony:"] + w, ["Szanse:"] + o,
                    ["Zagrożenia:"] + (t or ["– [BRAK DANYCH: zagrożenia zewnętrzne według klienta]"]),
                    [f"Mocne strony wykorzystam przy obsłudze grup: "
                     f"{', '.join(x.nazwa for x in kw.klienci.segmenty[:3])}.",
                     "Sposoby ograniczania zagrożeń opisuję w części o ryzykach."]]

        if sekcja == "08":
            from .finanse import procent_pl
            p = kw.prognoza
            p1 = [f"Przychody {r('policzyłam', 'policzyłem')} jako cenę usługi pomnożoną przez liczbę usług w miesiącu.",
                  "Przy pełnym obłożeniu zakładam: " + "; ".join(
                      f"{_male(u.nazwa)} – {u.liczba_mies} po {_zl(u.cena)}" for u in kw.uslugi) + ".",
                  f"Rozruch: w 1. miesiącu {procent_pl(p.rozruch[0])}, w 2. {procent_pl(p.rozruch[1])}, "
                  f"w 3. {procent_pl(p.rozruch[2])} docelowej sprzedaży.",
                  "W najbardziej pracowitym miesiącu wykorzystam {{ark_oblozenie_max}} czasu pracy z klientami."]
            if pom.sezonowosc_opis:
                p1.append(f"Sezonowość: {pom.sezonowosc_opis}")
            zus = {"ulga na start + preferencyjny": "Najpierw korzystam z ulgi na start, potem z preferencyjnych "
                                                     "składek ZUS ({{ark_zus_m12}} w 12. miesiącu).",
                   "preferencyjny": "Płacę preferencyjne składki ZUS ({{ark_zus_m12}} w 12. miesiącu).",
                   "pełny": "Płacę pełne składki ZUS ({{ark_zus_m12}} w 12. miesiącu).",
                   "nie wiem": "[BRAK DANYCH: wariant ZUS] Składki w 12. miesiącu: {{ark_zus_m12}}."}[kw.forma.zus]
            p2 = ["Koszty stałe wyniosą {{ark_koszty_stale_mies}} miesięcznie.",
                  "Materiały to {{ark_materialy_pct}} przychodu.", zus,
                  "Składka zdrowotna w pierwszych 12 miesiącach: {{ark_zdrowotna_12m}}."]
            p3 = ["W 12 miesiącach zakładam {{ark_przychod_12m}} przychodu i {{ark_koszty_12m}} kosztów.",
                  "Zysk netto po podatku wyniesie {{ark_zysk_netto_12m}}, średnio {{ark_zysk_netto_mies}} miesięcznie.",
                  "Pierwszy miesiąc z zyskiem netto: nr {{ark_pierwszy_mies_zysku}}."]
            p4 = ["Próg rentowności to {{ark_prog_rent_zl}} przychodu miesięcznie, czyli ok. {{ark_prog_rent_szt}} usług.",
                  "Po rozruchu planuję średnio {{ark_przychod_sredni_od_m4}} miesięcznie, "
                  "więc margines bezpieczeństwa wynosi {{ark_margines}}.",
                  "Po zakończeniu ulg w ZUS próg wzrośnie do {{ark_prog_rent_pelny_zus}} miesięcznie."]
            plan_b = next((x.plan_b for x in kw.ryzyka if x.plan_b and re.search(r"mniej|przychod|klient", x.ryzyko)),
                          next((x.plan_b for x in kw.ryzyka if x.plan_b), None))
            p5 = ["Przy przychodach niższych o 30% wyniosłyby one {{ark_przychod_12m_pes}}, a zysk netto "
                  "{{ark_zysk_netto_12m_pes}}, średnio {{ark_zysk_netto_mies_pes}} miesięcznie.",
                  "Najniższe saldo gotówki w tym wariancie: {{ark_min_saldo_pes}}.",
                  f"Wtedy: {plan_b}." if plan_b else "[BRAK DANYCH: co zrobię, gdy przychody będą o 30% niższe]"]
            fd = kw.finanse_domowe
            p6 = ["Najniższe saldo gotówki w wariancie bazowym: {{ark_min_saldo}}, na koniec 12. miesiąca: "
                  "{{ark_gotowka_m12}}."]
            if fd.inne_dochody:
                p6.append(f"Sytuacja domowa: {fd.inne_dochody}.")
            p6.append(f"Od firmy potrzebuję co najmniej {_zl(fd.potrzeby_mies)} miesięcznie." if fd.potrzeby_mies
                      else "[BRAK DANYCH: miesięczne wydatki domowe]")
            return [p1, p2, p3, p4, p5, p6]

        if sekcja == "09":
            akapity = [[f"Przy planowaniu firmy {r('przeanalizowałam', 'przeanalizowałem')} ryzyka, "
                        "które mogą utrudnić prowadzenie działalności przez okres umowy z urzędem."]]
            for x in kw.ryzyka:
                akapity.append([
                    f"Ryzyko: {x.ryzyko}.",
                    f"Zapobieganie: {x.zapobieganie}." if x.zapobieganie else
                    f"[BRAK DANYCH: jak zapobiegam ryzyku „{x.ryzyko}”]",
                    f"Plan B: {x.plan_b}." if x.plan_b else f"[BRAK DANYCH: co zrobię, gdy {x.ryzyko}]",
                ])
            if not kw.ryzyka:
                akapity.append(["[BRAK DANYCH: ryzyka według klienta i plan B]"])
            akapity.append(["Przy przychodach niższych o 30% średni zysk netto wyniesie {{ark_zysk_netto_mies_pes}} "
                            "miesięcznie, a najniższe saldo gotówki {{ark_min_saldo_pes}}.",
                            "Szczegóły opisuję w części finansowej."])
            utrz = [f"Źródła na najsłabszy miesiąc: {kw.wklad_wlasny.zrodlo or 'oszczędności'}"
                    f"{f'; {kw.finanse_domowe.inne_dochody}' if kw.finanse_domowe.inne_dochody else ''}."]
            akapity.append(utrz)
            return akapity
        raise ValueError(f"Nieznana sekcja {sekcja}")


def klient_domyslny(dry_run: bool = False, model: str | None = None, effort: str | None = None) -> KlientLLM:
    """Atrapa przy --dry-run albo bez ANTHROPIC_API_KEY; w przeciwnym razie Claude."""
    if dry_run or not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")):
        if not dry_run:
            log.warning("Brak ANTHROPIC_API_KEY – używam atrapy modelu (tryb offline).")
        return KlientAtrapa()
    return KlientClaude(model=model, effort=effort)


def teraz() -> dt.datetime:
    return dt.datetime.now().replace(microsecond=0)
