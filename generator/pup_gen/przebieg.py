"""Pełny przebieg zlecenia: arkusz -> treści pól -> kontrola -> DOCX + raport.

Pliki w katalogu wyniku:
  wynik.json                         – teksty pól, zmienne ark_*, ostrzeżenia (wejście dla `pup-gen sprawdz`)
  kwestionariusz.json, mapa.json, regulamin.json – kopie danych wejściowych (do ponownej kontroli)
  arkusz-<id>.xlsx                   – przeliczony arkusz klienta
  PUP-<miasto>_<id>_wniosek_v1.docx  – dokument dla klienta (opcjonalnie .pdf)
  raport-kontroli-WLASCICIEL.md/.docx, raport-kontroli.json – tylko dla właściciela
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path

from . import KATALOG_PRZYKLADOW, PLIK_BAZY_PUP
from . import dokument, finanse, kontrola, prompty
from .llm import BladLLM, KlientLLM, OdpowiedzLLM, teraz
from .schemat import Kwestionariusz, MapaFormularza, RegulaminPUP, WynikGeneracji, WynikPola, wczytaj_regulaminy

log = logging.getLogger(__name__)
_RE_TEKST = re.compile(r"<tekst>\s*(.*?)\s*</tekst>", re.S)
_RE_KONTROLA = re.compile(r"<kontrola>\s*(.*?)\s*</kontrola>", re.S)
_RE_ARK = re.compile(r"\{\{\s*(ark_[a-z0-9_]+)\s*\}\}")


@dataclass
class Pliki:
    katalog: Path
    wynik: Path
    arkusz: Path
    docx: Path
    raport: Path
    pdf: Path | None = None


def parsuj_odpowiedz(surowy: str) -> tuple[str | None, str]:
    t, k = _RE_TEKST.search(surowy), _RE_KONTROLA.search(surowy)
    return (t.group(1).strip() if t else None), (k.group(1).strip() if k else "")


def podstaw(tekst: str, ark: dict[str, str]) -> str:
    """Podstawia {{ark_*}} wartościami z arkusza; nieznane zmienne zostają (kontrola je zablokuje)."""
    return _RE_ARK.sub(lambda m: ark.get(m.group(1), m.group(0)), tekst)


def wczytaj_regulamin(pup_id: str | None, plik_csv: Path | None = None) -> RegulaminPUP | None:
    if not pup_id:
        return None
    for plik in (plik_csv, PLIK_BAZY_PUP, KATALOG_PRZYKLADOW / "regulaminy-przyklad.csv"):
        if plik and plik.exists():
            reg = wczytaj_regulaminy(plik).get(pup_id)
            if reg:
                return reg
    return None


def _generuj_pole(klient: KlientLLM, zapytanie, ark: dict[str, str], wp: WynikPola) -> None:
    odp: OdpowiedzLLM | None = None
    tekst_zm: str | None = None
    tokeny: dict[str, int] = {}

    def zlicz(o: OdpowiedzLLM) -> None:
        for k, v in o.tokeny.items():
            tokeny[k] = tokeny.get(k, 0) + v

    for _ in range(2):  # druga próba, gdy model nie zwrócił bloku <tekst>
        odp = klient.generuj(zapytanie)
        wp.proby += 1
        zlicz(odp)
        tekst_zm, wp.kontrola_modelu = parsuj_odpowiedz(odp.tekst_surowy)
        if tekst_zm is not None:
            break
    if tekst_zm is None:
        raise BladLLM(f"Pole {wp.id}: odpowiedź bez bloku <tekst>.")
    tekst = podstaw(tekst_zm, ark)
    limit = wp.limit_znakow
    if limit and len(tekst) > limit:  # jedna prośba o skrócenie z dokładną nadwyżką
        odp2 = klient.generuj(zapytanie, prompty.prosba_o_skrocenie(len(tekst), limit), odp)
        wp.proby += 1
        zlicz(odp2)
        krotszy, kontrola_m = parsuj_odpowiedz(odp2.tekst_surowy)
        if krotszy:
            tekst_zm, wp.kontrola_modelu = krotszy, kontrola_m
            tekst = podstaw(tekst_zm, ark)
    wp.tekst_ze_zmiennymi = tekst_zm
    wp.tekst = tekst
    wp.liczba_znakow = len(tekst)
    wp.braki = re.findall(r"\[BRAK DANYCH:[^\]]*\]", tekst)
    wp.tokeny = tokeny
    log.info("pole=%s znaki=%d limit=%s próby=%d", wp.id, wp.liczba_znakow, limit, wp.proby)


def generuj(kw: Kwestionariusz, mapa: MapaFormularza, regulamin: RegulaminPUP | None, klient: KlientLLM,
            katalog: Path, archiwum: Path | None = None, pdf: bool = False,
            tryb: str = "api") -> tuple[WynikGeneracji, kontrola.RaportKontroli, Pliki]:
    katalog.mkdir(parents=True, exist_ok=True)
    fin = finanse.policz(kw, regulamin, katalog)
    dane_klienta = prompty.blok_danych_klienta(kw, fin, regulamin)

    pola: list[WynikPola] = []
    for pole in mapa.pola:
        wp = WynikPola(id=pole.id, nazwa_w_formularzu=pole.nazwa_w_formularzu, sekcje=pole.sekcje,
                       format=pole.format, uwagi=pole.uwagi,
                       limit_znakow=(pole.limit_znakow or prompty.WARIANTY["standard"]) if pole.sekcje_tekstowe else pole.limit_znakow)
        if pole.sekcje_tekstowe:
            zapytanie = prompty.zbuduj_zapytanie(kw, pole, fin, regulamin, dane_klienta=dane_klienta)
            _generuj_pole(klient, zapytanie, fin.ark, wp)
        pola.append(wp)

    wynik = WynikGeneracji(
        id_zlecenia=kw.id, imie=kw.osoba.imie, miejscowosc=kw.osoba.miejscowosc,
        pup=mapa.pup or kw.nabor.nazwa_pup, pup_id=kw.nabor.pup_id or mapa.pup_id, formularz=mapa.formularz,
        ton=kw.ton, data=teraz(), model=klient.model, tryb=tryb, pola=pola, ark=fin.ark,
        ark_wartosci={k: (v if isinstance(v, (int, float, str)) or v is None else str(v)) for k, v in fin.wartosci.items()},
        kontrole_arkusza={k: (v if isinstance(v, (int, float, str)) or v is None else str(v)) for k, v in fin.kontrole.items()},
        ostrzezenia_finansowe=fin.ostrzezenia, plik_arkusza=fin.plik.name,
    )
    plik_wyniku = katalog / "wynik.json"
    plik_wyniku.write_text(wynik.model_dump_json(indent=1), encoding="utf-8")
    (katalog / "kwestionariusz.json").write_text(kw.model_dump_json(indent=1), encoding="utf-8")
    (katalog / "mapa.json").write_text(mapa.model_dump_json(indent=1), encoding="utf-8")
    if regulamin:
        (katalog / "regulamin.json").write_text(regulamin.model_dump_json(indent=1), encoding="utf-8")

    raport = kontrola.sprawdz(wynik, kw, regulamin, archiwum, katalog_wyniku=katalog)
    plik_raportu = kontrola.zapisz_raport(raport, katalog)
    dokument.zapisz_raport_docx(raport.markdown(), katalog / "raport-kontroli-WLASCICIEL.docx")
    miasto = (regulamin.miasto if regulamin and regulamin.miasto else None) or kw.nabor.powiat or kw.nabor.nazwa_pup
    plik_docx = dokument.zapisz_dokument(wynik, mapa, fin.tabele, kw, katalog / dokument.nazwa_pliku(wynik, miasto))
    plik_pdf = finanse.konwertuj_pdf(plik_docx, katalog) if pdf else None
    return wynik, raport, Pliki(katalog, plik_wyniku, fin.plik, plik_docx, plik_raportu, plik_pdf)


def sprawdz_katalog(katalog: Path, archiwum: Path | None = None) -> kontrola.RaportKontroli:
    """Ponowna kontrola gotowego wyniku (np. po ręcznej edycji tekstów w wynik.json)."""
    wynik = WynikGeneracji.model_validate_json((katalog / "wynik.json").read_text(encoding="utf-8"))
    kw = Kwestionariusz.model_validate_json((katalog / "kwestionariusz.json").read_text(encoding="utf-8"))
    plik_reg = katalog / "regulamin.json"
    regulamin = RegulaminPUP.model_validate(json.loads(plik_reg.read_text(encoding="utf-8"))) if plik_reg.exists() \
        else wczytaj_regulamin(wynik.pup_id)
    for p in wynik.pola:  # długość liczona od nowa – teksty mogły być poprawione ręcznie
        p.liczba_znakow = len(p.tekst)
    raport = kontrola.sprawdz(wynik, kw, regulamin, archiwum, katalog_wyniku=katalog)
    kontrola.zapisz_raport(raport, katalog)
    dokument.zapisz_raport_docx(raport.markdown(), katalog / "raport-kontroli-WLASCICIEL.docx")
    return raport
