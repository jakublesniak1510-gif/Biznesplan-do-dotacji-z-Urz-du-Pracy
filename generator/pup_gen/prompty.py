"""Składanie promptów z plików `szablony/*.md` (treści szablonów nie kopiujemy do kodu).

Kolejność bloków jest ustawiona pod prompt caching:
  system (stały dla wszystkich klientów)  ->  dane klienta + arkusz (stałe dla jednego zlecenia)
  ->  szablon sekcji (stały dla sekcji)  ->  parametry pola i prompt sekcji (zmienne).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from . import KATALOG_SZABLONOW
from .finanse import WynikFinansowy, procent_pl
from .llm import ZapytanieLLM
from .schemat import Kwestionariusz, PoleFormularza, RegulaminPUP

WARIANTY = {"krótki": 800, "standard": 2000, "długi": 4000}
_RE_ZMIENNA_OPCJI = re.compile(r"\{\{([^{}]*\|[^{}]*)\}\}")


class BladSzablonu(RuntimeError):
    pass


@dataclass(frozen=True)
class SzablonSekcji:
    sekcja: str
    plik: Path
    tytul: str
    tresc: str           # sekcje 1–7 pliku, bez przykładu wypełnienia (przykładów nie wysyłamy do modelu)
    prompt_sekcji: str   # blok ```text z części „Prompt sekcji”


def _plik_sekcji(sekcja: str, katalog: Path) -> Path:
    pliki = sorted(katalog.glob(f"{sekcja}-*.md"))
    if not pliki:
        raise BladSzablonu(f"Brak szablonu sekcji {sekcja} w {katalog}")
    return pliki[0]


@lru_cache(maxsize=None)
def prompt_systemowy(katalog: Path = KATALOG_SZABLONOW) -> str:
    """Część PROMPT pliku 00 (między liniami =====)."""
    tekst = _plik_sekcji("00", katalog).read_text(encoding="utf-8")
    m = re.search(r"^=====\s*$(.*?)^=====\s*$", tekst, re.S | re.M)
    if not m:
        raise BladSzablonu("W 00-system-prompt.md nie znaleziono bloku między liniami =====")
    return m.group(1).strip()


@lru_cache(maxsize=None)
def wczytaj_szablon(sekcja: str, katalog: Path = KATALOG_SZABLONOW) -> SzablonSekcji:
    plik = _plik_sekcji(sekcja, katalog)
    tekst = plik.read_text(encoding="utf-8")
    tytul = tekst.splitlines()[0].lstrip("# ").strip()
    tresc = re.split(r"^## 8\.", tekst, maxsplit=1, flags=re.M)[0].strip()
    m = re.search(r"^## 7\..*?```text\n(.*?)```", tekst, re.S | re.M)
    if not m:
        raise BladSzablonu(f"{plik.name}: brak bloku ```text w części „Prompt sekcji”")
    return SzablonSekcji(sekcja=sekcja, plik=plik, tytul=tytul, tresc=tresc, prompt_sekcji=m.group(1).strip())


def wariant_dla_limitu(limit: int | None) -> str:
    if limit is None:
        return "standard"
    if limit <= 1200:
        return "krótki"
    if limit <= 3000:
        return "standard"
    return "długi"


def _wybierz_opcje(opcje: list[str], format_pola: str) -> str:
    preferencje = {
        "tabela": ["tabela", "pozycyjny"],
        "4_pola": ["4 osobne pola", "4 listy"],
    }.get(format_pola, ["tekst", "opisowy", "4 listy"])
    for p in preferencje:
        if p in opcje:
            return p
    return opcje[0]


def wypelnij_prompt_sekcji(szablon: SzablonSekcji, pole: PoleFormularza, limit: int, ton: str) -> str:
    """Podstawia {{pole_formularza}}, {{limit_znakow}}, {{ton}} i warianty {{a | b}}; {{ark_*}} zostają."""
    tekst = (szablon.prompt_sekcji
             .replace("{{pole_formularza}}", pole.nazwa_w_formularzu)
             .replace("{{limit_znakow}}", str(limit))
             .replace("{{ton}}", ton))
    return _RE_ZMIENNA_OPCJI.sub(
        lambda m: _wybierz_opcje([o.strip() for o in m.group(1).split("|")], pole.format), tekst)


def _regulamin_dla_modelu(reg: RegulaminPUP | None) -> dict[str, Any] | None:
    if reg is None:
        return None
    pola = ("nazwa_pup", "limit_reklama_pct", "limit_towar_pct", "limit_remont_pct", "limit_samochod_pct",
            "sprzet_uzywany", "wykluczenia_dzialalnosci", "okres_prowadzenia_mies", "kryteria_punktowane")
    return {p: getattr(reg, p) for p in pola if getattr(reg, p) not in (None, [], "")}


def blok_danych_klienta(kw: Kwestionariusz, fin: WynikFinansowy, reg: RegulaminPUP | None) -> str:
    """Wspólny dla wszystkich pól jednego klienta – drugi punkt cache."""
    p = kw.prognoza
    arkusz = {
        "zmienne": fin.ark,
        "dane_wejsciowe_wolno_przepisac": {
            "rozruch_m1_m12": [procent_pl(x) for x in p.rozruch],
            "sezonowosc_sty_gru": p.sezonowosc,
            "materialy_procent_przychodu": procent_pl(p.materialy_pct),
            "scenariusz_pesymistyczny": "przychody niższe o 30%",
            "dni_robocze": p.dni_robocze,
            "godziny_pracy_z_klientem_dziennie": p.godziny_dzien,
            "koszty_stale_mies_zl": p.koszty_stale.model_dump(),
        },
    }
    czesci = [
        "<kwestionariusz>\n" + json.dumps(kw.dane_do_promptu(), ensure_ascii=False, indent=1) + "\n</kwestionariusz>",
        "<arkusz>\n" + json.dumps(arkusz, ensure_ascii=False, indent=1) + "\n</arkusz>",
    ]
    reg_m = _regulamin_dla_modelu(reg)
    if reg_m:
        czesci.append("<regulamin_pup>\n" + json.dumps(reg_m, ensure_ascii=False, indent=1) + "\n</regulamin_pup>")
    return "\n\n".join(czesci)


def zbuduj_zapytanie(kw: Kwestionariusz, pole: PoleFormularza, fin: WynikFinansowy,
                     reg: RegulaminPUP | None, katalog: Path = KATALOG_SZABLONOW,
                     dane_klienta: str | None = None) -> ZapytanieLLM:
    sekcje = pole.sekcje_tekstowe
    if not sekcje:
        raise ValueError(f"Pole {pole.id} nie ma sekcji tekstowej")
    wariant = wariant_dla_limitu(pole.limit_znakow)
    limit = pole.limit_znakow or WARIANTY[wariant]
    szablony = [wczytaj_szablon(s, katalog) for s in sekcje]

    blok_szablonow = "\n\n".join(
        f"<szablon_sekcji nr=\"{s.sekcja}\">\n{s.tresc}\n</szablon_sekcji>" for s in szablony)

    parametry = [
        f"sekcja: {' + '.join(s.plik.stem for s in szablony)}",
        f"pole_formularza: \"{pole.id} {pole.nazwa_w_formularzu}\"",
        f"limit_znakow: {limit} (ze spacjami, liczony PO podstawieniu wartości zmiennych z <arkusz>)",
        f"wariant: {wariant}",
        f"ton: {kw.ton}",
        f"format: {pole.format}",
        f"kwoty: {'netto (czynny VAT)' if kw.vat_czynny else 'brutto (zwolnienie z VAT)'}",
        f"wariant_zus: {kw.forma.zus}",
        f"forma_opodatkowania: {kw.forma.opodatkowanie}",
    ]
    if pole.podzial_limitu:
        parametry.append("podzial_limitu: " + ", ".join(
            f"sekcja {s} ≈ {round(udzial * limit)} znaków" for s, udzial in pole.podzial_limitu.items()))
    if pole.uwagi:
        parametry.append(f"uwagi_do_pola (pytanie z formularza dosłownie): \"{pole.uwagi}\"")

    prompty_sekcji = "\n\n".join(wypelnij_prompt_sekcji(s, pole, limit, kw.ton) for s in szablony)
    polecenie = (
        "<parametry>\n" + "\n".join(parametry) + "\n</parametry>\n\n"
        "<prompt_sekcji>\n" + prompty_sekcji + "\n</prompt_sekcji>\n\n"
        + ("To jedno pole formularza łączy kilka sekcji: napisz jeden ciągły tekst według wszystkich "
           "dołączonych szablonów, w proporcjach z podzial_limitu.\n" if len(szablony) > 1 else "")
        + "Napisz treść tego pola. Zwróć dokładnie bloki <tekst> i <kontrola>."
    )
    return ZapytanieLLM(
        system=prompt_systemowy(katalog),
        dane_klienta=dane_klienta if dane_klienta is not None else blok_danych_klienta(kw, fin, reg),
        szablony=blok_szablonow,
        polecenie=polecenie,
        pole_id=pole.id,
        sekcje=sekcje,
        limit_znakow=limit,
        kontekst={
            "kwestionariusz": kw,
            "ark": fin.ark,
            "wariant": wariant,
            "format": pole.format,
            "podzial_limitu": pole.podzial_limitu,
            "uwagi": pole.uwagi,
        },
    )


def prosba_o_skrocenie(dlugosc: int, limit: int) -> str:
    return (f"Tekst po podstawieniu zmiennych ma {dlugosc} znaków ze spacjami, a limit pola to {limit}. "
            f"Skróć go o co najmniej {dlugosc - limit + max(20, limit // 50)} znaków, zachowując fakty, "
            "zmienne {{ark_…}} i znaczniki [BRAK DANYCH: …]. Zwróć ponownie bloki <tekst> i <kontrola>.")
