"""Automatyczna kontrola jakości wygenerowanych treści (uzupełnia docs/checklista-weryfikacji.md).

1. zakazane zwroty (lista parsowana z szablony/00-system-prompt.md),
2. znaczniki [BRAK DANYCH: …] – pytania do klienta,
3. długość vs limit pola (85–100%),
4. spójność liczb: kwoty i procenty w tekście muszą wynikać z arkusza (`ark_*`) lub kwestionariusza,
5. regulamin PUP: wykluczenia działalności, limity kategorii kosztorysu, pojazdy, sprzęt używany,
6. podobieństwo do wcześniejszych planów do tego samego PUP (n-gramy + TF-IDF, bez zależności),
7. obietnice i gwarancje.
Wynik: raport Markdown z podziałem BLOKUJE / OSTRZEŻENIE / INFO.
"""

from __future__ import annotations

import datetime as dt
import json
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

from . import KATALOG_SZABLONOW
from .finanse import liczba_pl, procent_pl
from .prompty import prompt_systemowy
from .schemat import Kwestionariusz, Ostrzezenie, RegulaminPUP, WynikGeneracji

PROG_8GRAM = 1            # tyle wspólnych 8-wyrazowych fragmentów wystarczy do ostrzeżenia
PROG_COSINUS = 0.60       # podobieństwo TF-IDF całych planów
PROG_JACCARD_3 = 0.20     # wspólne trójki wyrazów
ROTACJA_TONU_DNI = 92     # rotacja tonu w obrębie PUP (ok. 3 miesiące)

_RE_BRAK = re.compile(r"\[BRAK DANYCH:[^\]]*\]")
_RE_ZMIENNA = re.compile(r"\{\{[^{}]*\}\}")
_RE_KWOTA = re.compile(r"(?<![\d,.])(-?\d{1,3}(?:[  ]\d{3})+|-?\d+)(?:,(\d+))?\s?(zł|złotych|PLN|%)")
_RE_LICZBA_W_TEKSCIE = re.compile(r"(?<![\d,])(\d{1,3}(?:[  ]\d{3})+|\d+)(?:[,.](\d+))?")
_NAZWY_PROC = ("ark_margines", "ark_rentownosc", "ark_zwrot_z_dotacji", "ark_materialy_pct", "ark_oblozenie_max")
_KOSZTORYS_ZAKAZY = {
    "kasa fiskaln": "kasa fiskalna",
    "leasing": "leasing / raty",
    "kaucj": "kaucja",
    "czynsz": "czynsz",
    "ubezpieczen": "ubezpieczenie",
    "szkoleni": "szkolenie",
    "transport": "transport / przesyłka",
    "przesyłk": "transport / przesyłka",
    "zus": "składki ZUS",
    "nieruchomoś": "nieruchomość",
}


# --------------------------------------------------------------------------- wzorce zwrotów
@dataclass(frozen=True)
class Wzorzec:
    fraza: str
    regex: re.Pattern[str]
    poziom: str
    kategoria: str  # "zakazany zwrot" | "obietnica"


def _rdzen(slowo: str) -> str:
    s = slowo.lower().strip(".,;:!?\"„”'")
    if s.endswith("%"):
        return re.escape(s)
    if len(s) <= 4:
        return re.escape(s) + r"\b"
    if s.endswith("ek"):
        return re.escape(s[:-2]) + r"\w*"
    return re.escape(s[: len(s) - (1 if len(s) <= 6 else 2)]) + r"\w*"


def _regex_frazy(fraza: str) -> re.Pattern[str]:
    slowa = [w for w in fraza.split() if w.strip(".,;:")]
    return re.compile(r"(?<!\w)" + r"\W+".join(_rdzen(w) for w in slowa), re.I)


def _regex_wykluczenia(fraza: str) -> re.Pattern[str]:
    """Dokładniejsze dopasowanie niż _regex_frazy: krótkie słowa tylko z typowymi końcówkami („komis” ≠ „komisja”)."""
    czesci = []
    for w in fraza.lower().split():
        if len(w) <= 6:
            czesci.append(re.escape(w) + r"(?:u|ie|em|y|ów|ami|ach|om|a|e|i)?\b")
        else:
            czesci.append(_rdzen(w))
    return re.compile(r"(?<!\w)" + r"\W+".join(czesci), re.I)


@lru_cache(maxsize=None)
def wzorce(katalog: Path = KATALOG_SZABLONOW) -> tuple[Wzorzec, ...]:
    """Parsuje LISTĘ ZAKAZANĄ i zasadę 8 z promptu systemowego."""
    system = prompt_systemowy(katalog)
    m = re.search(r"LISTA ZAKAZANA[^\n]*\n(.*?)\n\s*FORMAT ODPOWIEDZI", system, re.S)
    if not m:
        raise RuntimeError("Nie znaleziono LISTY ZAKAZANEJ w 00-system-prompt.md")
    wynik: dict[str, Wzorzec] = {}
    for linia in m.group(1).splitlines():
        linia = linia.strip()
        if not linia.startswith("- "):
            continue
        linia = linia[2:]
        obietnica = "zasada 8" in linia
        warunkowy = bool(re.search(r"\((bez|jako hasło)", linia))
        czysta = re.sub(r"\([^)]*\)", "", linia).replace("…", "").replace("...", "")
        alternatywy = [a.strip(" ,") for a in czysta.split("/") if a.strip(" ,")]
        pierwsza = alternatywy[0].split()
        zamiana = len(pierwsza) > 1 and all(len(a.split()) == 1 for a in alternatywy[1:])
        for alt in alternatywy:
            slowa = alt.split()
            if zamiana and alt != alternatywy[0]:
                slowa = pierwsza[:-1] + slowa  # „rynek / branża / sektor” – zamiana ostatniego wyrazu
            fraza = " ".join(slowa)
            wynik[fraza] = Wzorzec(fraza, _regex_frazy(fraza),
                                   "OSTRZEŻENIE" if warunkowy else "BLOKUJE",
                                   "obietnica" if obietnica else "zakazany zwrot")
    m8 = re.search(r"8\. Żadnych obietnic.*?Zakazane:(.*?)Piszesz", system, re.S)
    if m8:
        for fraza in (" ".join(f.split()) for f in re.findall(r'"([^"]+)"', m8.group(1))):
            pojedyncze = len(fraza.split()) == 1 and not fraza.startswith("gwarant")
            wynik[fraza] = Wzorzec(fraza, _regex_frazy(fraza), "OSTRZEŻENIE" if pojedyncze else "BLOKUJE",
                                   "obietnica")
    return tuple(wynik.values())


# --------------------------------------------------------------------------- liczby
def _na_liczbe(calk: str, ulamek: str | None) -> float:
    return float(calk.replace(" ", "").replace(" ", "") + ("." + ulamek if ulamek else ""))


def _liczby_z_danych(dane: Any) -> set[float]:
    wynik: set[float] = set()
    if isinstance(dane, dict):
        for v in dane.values():
            wynik |= _liczby_z_danych(v)
    elif isinstance(dane, list):
        for v in dane:
            wynik |= _liczby_z_danych(v)
    elif isinstance(dane, bool):
        pass
    elif isinstance(dane, (int, float)):
        wynik.add(float(dane))
        if 0 < abs(dane) <= 1:
            wynik.add(round(float(dane) * 100, 4))
    elif isinstance(dane, str) and not dane.startswith("http"):
        for calk, ulamek in _RE_LICZBA_W_TEKSCIE.findall(dane):
            wynik.add(_na_liczbe(calk, ulamek))
    return wynik


def dozwolone_liczby(wynik: WynikGeneracji, kw: Kwestionariusz) -> tuple[set[float], set[float]]:
    """(kwoty w zł, procenty) dopuszczalne w tekście."""
    kwoty: set[float] = set()
    procenty: set[float] = {30.0}  # scenariusz pesymistyczny (Zalozenia!B22)
    for nazwa, v in wynik.ark_wartosci.items():
        if not isinstance(v, (int, float)):
            continue
        if nazwa.startswith(_NAZWY_PROC):
            procenty.add(v * 100)
        else:
            kwoty.add(float(v))
    z_kw = _liczby_z_danych(kw.model_dump(mode="json"))
    kwoty |= z_kw
    procenty |= z_kw
    for z in kw.zakupy:
        kwoty |= {z.cena_netto, round(z.cena_netto * z.ilosc, 2), round(z.cena_brutto * z.ilosc, 2),
                  z.kwota_do_rozliczenia(True), z.kwota_do_rozliczenia(False)}
    return kwoty, procenty


def _pasuje(x: float, zbior: set[float], procent: bool) -> bool:
    if procent:
        return any(abs(x - v) <= 0.51 for v in zbior)
    return any(abs(x - v) <= max(1.01, abs(v) * 0.001) for v in zbior)


# --------------------------------------------------------------------------- podobieństwo
def _slowa(tekst: str) -> list[str]:
    tekst = _RE_BRAK.sub(" ", tekst.lower())
    return [w for w in re.findall(r"[^\W\d_]+", tekst)]


def _ngramy(slowa: list[str], n: int) -> set[tuple[str, ...]]:
    return {tuple(slowa[i:i + n]) for i in range(len(slowa) - n + 1)}


def _tfidf_cosinus(dokumenty: list[list[str]]) -> list[float]:
    """Cosinus TF-IDF (unigramy + bigramy) pierwszego dokumentu względem pozostałych."""
    torby = [Counter(d + [f"{a} {b}" for a, b in zip(d, d[1:])]) for d in dokumenty]
    n = len(torby)
    df = Counter(t for torba in torby for t in torba)
    idf = {t: math.log((1 + n) / (1 + c)) + 1 for t, c in df.items()}
    wektory = [{t: c * idf[t] for t, c in torba.items()} for torba in torby]
    normy = [math.sqrt(sum(v * v for v in w.values())) or 1.0 for w in wektory]
    w0 = wektory[0]
    return [sum(w0.get(t, 0) * v for t, v in w.items()) / (normy[0] * normy[i])
            for i, w in enumerate(wektory) if i > 0]


def wczytaj_archiwum(archiwum: Path | None, wynik: WynikGeneracji, pomin: Path | None = None) -> list[tuple[Path, WynikGeneracji]]:
    if not archiwum or not archiwum.exists():
        return []
    plany = []
    for plik in sorted(archiwum.rglob("wynik.json")):
        if pomin and plik.resolve().parent == pomin.resolve():
            continue
        try:
            inny = WynikGeneracji.model_validate_json(plik.read_text(encoding="utf-8"))
        except ValueError:
            continue
        ten_sam_pup = (inny.pup_id and inny.pup_id == wynik.pup_id) or inny.pup == wynik.pup
        if ten_sam_pup and inny.id_zlecenia != wynik.id_zlecenia:
            plany.append((plik, inny))
    return plany


def porownaj_z_archiwum(wynik: WynikGeneracji, archiwum: list[tuple[Path, WynikGeneracji]]) -> list[Ostrzezenie]:
    ust: list[Ostrzezenie] = []
    if not archiwum:
        ust.append(Ostrzezenie(poziom="INFO", kategoria="podobieństwo",
                               komunikat="Brak wcześniejszych planów do tego PUP w archiwum – test bliźniaka pominięty."))
        return ust
    ten = _slowa(wynik.tekst_calkowity())
    inne = [_slowa(p.tekst_calkowity()) for _, p in archiwum]
    cosinusy = _tfidf_cosinus([ten] + inne)
    for (plik, plan), slowa, cos in zip(archiwum, inne, cosinusy):
        wspolne8 = _ngramy(ten, 8) & _ngramy(slowa, 8)
        t3, i3 = _ngramy(ten, 3), _ngramy(slowa, 3)
        jaccard = len(t3 & i3) / (len(t3 | i3) or 1)
        opis = (f"plan {plan.id_zlecenia} ({plan.data:%Y-%m-%d}, ton {plan.ton}): TF-IDF {cos:.2f}, "
                f"Jaccard 3-gramów {jaccard:.2f}, wspólne fragmenty 8-wyrazowe: {len(wspolne8)}")
        if len(wspolne8) >= PROG_8GRAM or cos >= PROG_COSINUS or jaccard >= PROG_JACCARD_3:
            przyklady = "; ".join("„" + " ".join(g) + "”" for g in sorted(wspolne8)[:3])
            ust.append(Ostrzezenie(poziom="OSTRZEŻENIE", kategoria="podobieństwo",
                                   komunikat=opis + (f". Np. {przyklady}" if przyklady else "")
                                   + ". Przeredaguj powtarzające się zdania i zmień układ akapitów."))
        else:
            ust.append(Ostrzezenie(poziom="INFO", kategoria="podobieństwo", komunikat=opis))
        if plan.ton == wynik.ton and abs((wynik.data - plan.data).days) <= ROTACJA_TONU_DNI:
            ust.append(Ostrzezenie(poziom="OSTRZEŻENIE", kategoria="rotacja tonu",
                                   komunikat=f"Ten sam ton „{wynik.ton}” co plan {plan.id_zlecenia} do tego PUP "
                                             f"w ciągu 3 miesięcy – zmień ton (00-system-prompt.md, „Rotacja”)."))
    return ust


# --------------------------------------------------------------------------- raport
@dataclass
class RaportKontroli:
    wynik: WynikGeneracji
    ustalenia: list[Ostrzezenie] = field(default_factory=list)
    braki: list[tuple[str, str]] = field(default_factory=list)  # (id pola, znacznik)

    def dodaj(self, poziom: str, kategoria: str, komunikat: str, pole: str | None = None) -> None:
        self.ustalenia.append(Ostrzezenie(poziom=poziom, kategoria=kategoria, komunikat=komunikat, pole=pole))

    def liczba(self, poziom: str) -> int:
        return sum(1 for u in self.ustalenia if u.poziom == poziom)

    @property
    def blokuje(self) -> bool:
        return self.liczba("BLOKUJE") > 0

    def markdown(self) -> str:
        w = self.wynik
        lin = [
            f"# Raport kontroli – {w.id_zlecenia}",
            "",
            "> **Dokument wewnętrzny dla właściciela. Nie wysyłać klientowi.**",
            "",
            f"- Klient: {w.imie}, {w.miejscowosc}",
            f"- Urząd: {w.pup} · formularz: {w.formularz}",
            f"- Wygenerowano: {w.data:%Y-%m-%d %H:%M} · model: {w.model} · tryb: {w.tryb} · ton: {w.ton}",
            f"- Wynik: **{self.liczba('BLOKUJE')} BLOKUJE**, {self.liczba('OSTRZEŻENIE')} OSTRZEŻENIE, "
            f"{self.liczba('INFO')} INFO, znaczniki BRAK DANYCH: {len(self.braki)}",
            "",
        ]
        if w.tryb == "dry-run":
            lin += ["> Tryb --dry-run: teksty pochodzą z atrapy modelu i służą tylko do sprawdzenia przebiegu.", ""]
        for poziom, tytul in (("BLOKUJE", "⛔ BLOKUJE – popraw przed wysłaniem"),
                              ("OSTRZEŻENIE", "OSTRZEŻENIE – sprawdź i zdecyduj"), ("INFO", "INFO")):
            lin += [f"## {tytul}", ""]
            pozycje = [u for u in self.ustalenia if u.poziom == poziom]
            lin += [f"- **[{u.kategoria}]**{f' (pole {u.pole})' if u.pole else ''} {u.komunikat}" for u in pozycje] \
                or ["- brak"]
            lin.append("")
        lin += ["## Pytania do klienta (znaczniki BRAK DANYCH)", ""]
        lin += [f"- pole {pole}: {znacznik}" for pole, znacznik in self.braki] or ["- brak"]
        lin += ["", "## Długość pól", "", "| Pole | Limit | Znaki | % limitu |", "|---|---:|---:|---:|"]
        for p in w.pola:
            if p.limit_znakow and p.tekst:
                lin.append(f"| {p.id} {p.nazwa_w_formularzu[:50]} | {p.limit_znakow} | {p.liczba_znakow} | "
                           f"{round(100 * p.liczba_znakow / p.limit_znakow)}% |")
        lin += ["", "## Do sprawdzenia ręcznie (checklista, części A, D, E, G)", "",
                "- Prawdziwość faktów: każdy fakt da się wskazać w kwestionariuszu; konkurenci i ceny sprawdzone "
                "w Google Maps / na stronach (min. 2).",
                "- Zabezpieczenie zwrotu i warunki z art. 148 – zgodnie z kwestionariuszem i regulaminem.",
                "- Tekst brzmi jak klient: przeczytaj na głos sekcje 01 i 03.",
                "- Wersja formularza = formularz z bieżącego naboru; pola osobowe zostają dla klienta.", ""]
        return "\n".join(lin)


def sprawdz(wynik: WynikGeneracji, kw: Kwestionariusz, regulamin: RegulaminPUP | None,
            archiwum: Path | None = None, katalog_wyniku: Path | None = None,
            katalog_szablonow: Path = KATALOG_SZABLONOW) -> RaportKontroli:
    raport = RaportKontroli(wynik=wynik)
    raport.ustalenia += wynik.ostrzezenia_finansowe
    wz = wzorce(katalog_szablonow)

    for p in wynik.pola:
        tekstowe = [s for s in p.sekcje if s.isdigit()]
        if tekstowe and not p.tekst.strip():
            raport.dodaj("BLOKUJE", "brak treści", "Pole tekstowe bez treści.", p.id)
            continue
        if not p.tekst:
            continue
        bez_brakow = _RE_BRAK.sub(" ", p.tekst)
        # (1) zakazane zwroty, (7) obietnice
        for w in wz:
            for m in w.regex.finditer(bez_brakow):
                raport.dodaj(w.poziom, w.kategoria, f"„{m.group(0)}” (wzorzec z listy: „{w.fraza}”).", p.id)
        if re.search(r"\b(AI|ChatGPT|Claude)\b|sztuczn\w* inteligencj|model\w* językow", bez_brakow):
            raport.dodaj("BLOKUJE", "wzmianka o AI", "Tekst wspomina o AI / modelu językowym.", p.id)
        if re.search(r"\b(wnioskodawc|klient planuje|firma oferuje)", bez_brakow, re.I):
            raport.dodaj("OSTRZEŻENIE", "głos wnioskodawcy", "Tekst w 3. osobie – pisz w 1. osobie.", p.id)
        if bez_brakow.lstrip().startswith("Planuję otworzyć"):
            raport.dodaj("INFO", "styl", "Tekst zaczyna się od „Planuję otworzyć…” – zmień początek.", p.id)
        niepodstawione = _RE_ZMIENNA.findall(p.tekst)
        if niepodstawione:
            raport.dodaj("BLOKUJE", "zmienne", f"Niepodstawione zmienne: {', '.join(sorted(set(niepodstawione)))}.",
                         p.id)
        # (2) braki
        for znacznik in _RE_BRAK.findall(p.tekst):
            raport.braki.append((p.id, znacznik))
        # (3) długość
        if p.limit_znakow:
            udzial = p.liczba_znakow / p.limit_znakow
            if udzial > 1:
                raport.dodaj("BLOKUJE", "długość", f"{p.liczba_znakow} znaków przy limicie {p.limit_znakow} "
                                                   f"({procent_pl(udzial)}).", p.id)
            elif udzial < 0.85:
                raport.dodaj("OSTRZEŻENIE", "długość", f"Tylko {procent_pl(udzial)} limitu ({p.liczba_znakow}/"
                                                       f"{p.limit_znakow}) – dopisz fakty albo zostaw świadomie.", p.id)

    if raport.braki:
        raport.dodaj("OSTRZEŻENIE", "BRAK DANYCH",
                     f"Znaczniki do uzupełnienia z klientem albo usunięcia zdania: {len(raport.braki)} "
                     "(lista na końcu raportu).")

    # (4) spójność liczb
    kwoty, procenty = dozwolone_liczby(wynik, kw)
    for p in wynik.pola:
        for calk, ulamek, jednostka in _RE_KWOTA.findall(_RE_BRAK.sub(" ", p.tekst)):
            x = _na_liczbe(calk, ulamek)
            jest_procent = jednostka == "%"
            if not _pasuje(x, procenty if jest_procent else kwoty, jest_procent):
                zapis = f"{calk}{',' + ulamek if ulamek else ''} {jednostka}".replace(" %", "%")
                raport.dodaj("BLOKUJE", "spójność liczb",
                             f"Liczba „{zapis}” nie występuje w arkuszu (ark_*) ani w kwestionariuszu.", p.id)

    # (5) regulamin
    _kontrola_regulaminu(raport, wynik, kw, regulamin)

    # (6) podobieństwo
    raport.ustalenia += porownaj_z_archiwum(wynik, wczytaj_archiwum(archiwum, wynik, katalog_wyniku))
    return raport


def _kontrola_regulaminu(raport: RaportKontroli, wynik: WynikGeneracji, kw: Kwestionariusz,
                         reg: RegulaminPUP | None) -> None:
    kat = "regulamin"
    if kw.zakup_od_rodziny:
        raport.dodaj("BLOKUJE", kat, "Klient planuje zakup od rodziny / poręczyciela (pyt. 9.5) – zmień sprzedawcę.")
    if not kw.pomysl.pkd:
        raport.dodaj("OSTRZEŻENIE", kat, "Brak kodu PKD 2025 – dobierz podklasę przed wysłaniem.")
    for z in kw.zakupy:
        nazwa = z.nazwa.lower()
        for klucz, opis in _KOSZTORYS_ZAKAZY.items():
            if klucz in nazwa:
                raport.dodaj("OSTRZEŻENIE", kat, f"Pozycja „{z.nazwa}”: {opis} bywa wykluczona z katalogu wydatków – "
                                                 "sprawdź regulamin.")
                break
    bez_linku = [z.nazwa for z in kw.zakupy if not z.link and z.finansowanie == "dotacja"]
    if bez_linku:
        raport.dodaj("INFO", kat, f"{len(bez_linku)} pozycji z dotacji bez linku do oferty (urząd często ich żąda): "
                                  + "; ".join(bez_linku[:5]) + ("…" if len(bez_linku) > 5 else "") + ".")
    if reg is None:
        raport.dodaj("OSTRZEŻENIE", kat, "Brak regulaminu PUP w bazie – wykluczenia i limity niesprawdzone.")
        return
    tekst_dzial = " ".join([kw.pomysl.opis] + [u.nazwa for u in kw.uslugi] + [p.nazwa for p in kw.pomysl.pkd]).lower()
    kody = {p.kod for p in kw.pomysl.pkd}
    for wyk in reg.wykluczenia_dzialalnosci:
        w = wyk.lower()
        if re.fullmatch(r"\d{2}\.\d{2}(\.[a-z])?", w):
            if any(k.lower().startswith(w) for k in kody):
                raport.dodaj("BLOKUJE", kat, f"PKD {wyk} jest na liście wykluczeń urzędu.")
            continue
        if "sezonow" in w:
            if kw.pomysl.sezonowosc == "tak":
                raport.dodaj("BLOKUJE", kat, f"Urząd wyklucza: „{wyk}”, a klient zaznaczył działalność sezonową.")
            elif kw.pomysl.sezonowosc == "częściowo":
                raport.dodaj("OSTRZEŻENIE", kat, f"Urząd wyklucza: „{wyk}”; działalność częściowo sezonowa – "
                                                 "opisz całoroczny charakter.")
            continue
        if "rodzin" in w:
            if kw.pomysl.przejecie_od_rodziny.strip().lower() not in ("nie", "", "brak"):
                raport.dodaj("BLOKUJE", kat, f"Urząd wyklucza: „{wyk}”; klient: {kw.pomysl.przejecie_od_rodziny}.")
            continue
        if _regex_wykluczenia(w).search(tekst_dzial):
            raport.dodaj("BLOKUJE", kat, f"Opis działalności pasuje do wykluczenia urzędu: „{wyk}”.")

    dotacja = wynik.ark_wartosci.get("ark_dotacja") or kw.kwota_wnioskowana
    for nazwa, limit in (("towar", reg.limit_towar_pct), ("reklama", reg.limit_reklama_pct),
                         ("remont", reg.limit_remont_pct)):
        suma = wynik.ark_wartosci.get(f"ark_kat_{nazwa}")
        if limit is None or not isinstance(suma, (int, float)) or not dotacja:
            continue
        udzial = 100 * suma / dotacja
        if udzial > limit + 1e-6:
            raport.dodaj("BLOKUJE", kat, f"Kategoria „{nazwa}”: {liczba_pl(suma)} zł = {liczba_pl(udzial, 1)}% dotacji, "
                                         f"limit regulaminu {liczba_pl(limit)}%.")
        else:
            raport.dodaj("INFO", kat, f"Kategoria „{nazwa}”: {liczba_pl(udzial, 1)}% dotacji (limit {liczba_pl(limit)}%).")
    pojazdy = sum(z.kwota_do_rozliczenia(kw.vat_czynny) for z in kw.zakupy if z.pojazd and z.finansowanie == "dotacja")
    if pojazdy and reg.limit_samochod_pct is not None:
        if reg.limit_samochod_pct == 0:
            raport.dodaj("BLOKUJE", kat, "Regulamin zakazuje zakupu pojazdu z dotacji.")
        elif 100 * pojazdy / dotacja > reg.limit_samochod_pct:
            raport.dodaj("BLOKUJE", kat, f"Pojazd: {liczba_pl(100 * pojazdy / dotacja, 1)}% dotacji, "
                                         f"limit {liczba_pl(reg.limit_samochod_pct)}%.")
    if any(z.stan == "używany" for z in kw.zakupy):
        zasada = (reg.sprzet_uzywany or "").lower()
        if zasada.startswith("nie"):
            raport.dodaj("BLOKUJE", kat, "Regulamin nie dopuszcza sprzętu używanego, a kosztorys go zawiera.")
        elif zasada:
            raport.dodaj("INFO", kat, f"Sprzęt używany – warunki urzędu: {reg.sprzet_uzywany}.")
    if reg.kwota_max_zl and kw.kwota_wnioskowana > reg.kwota_max_zl:
        raport.dodaj("BLOKUJE", kat, f"Kwota {liczba_pl(kw.kwota_wnioskowana)} zł > maksimum urzędu "
                                     f"{liczba_pl(reg.kwota_max_zl)} zł.")
    if reg.liczba_poreczycieli and kw.zabezpieczenie.liczba_poreczycieli < reg.liczba_poreczycieli \
            and "poręczenie" in " ".join(kw.zabezpieczenie.formy):
        raport.dodaj("OSTRZEŻENIE", kat, f"Urząd wymaga {reg.liczba_poreczycieli} poręczycieli, klient ma "
                                         f"{kw.zabezpieczenie.liczba_poreczycieli}.")


def zapisz_raport(raport: RaportKontroli, katalog: Path) -> Path:
    plik = katalog / "raport-kontroli-WLASCICIEL.md"
    plik.write_text(raport.markdown(), encoding="utf-8")
    (katalog / "raport-kontroli.json").write_text(json.dumps(
        {"blokuje": raport.liczba("BLOKUJE"), "ostrzezenia": raport.liczba("OSTRZEŻENIE"),
         "info": raport.liczba("INFO"), "braki": len(raport.braki),
         "ustalenia": [u.model_dump() for u in raport.ustalenia],
         "data": dt.datetime.now().isoformat(timespec="seconds")}, ensure_ascii=False, indent=1), encoding="utf-8")
    return plik
