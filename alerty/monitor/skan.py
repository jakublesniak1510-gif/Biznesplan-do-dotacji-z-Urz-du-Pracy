"""Jeden przebieg monitora: pobranie → klasyfikacja → dociągnięcie szczegółów → stan → pliki wynikowe."""

from __future__ import annotations

import json
import logging
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import date, timedelta

from monitor import konfiguracja as k
from monitor.alert import do_alertu, markdown_issue
from monitor.klasyfikator import (
    KATEGORIE_ALERTU,
    SYGNAL_NABORU,
    ZAKONCZENIE,
    klasyfikuj,
    normalizuj,
    rozbij_tytul_zl,
    status,
    dni_do_konca,
)
from monitor.model import Pup, Wpis
from monitor.pobieranie import Klient
from monitor.stan import Stan, klucz_wpisu
from monitor.zrodla import (
    IndeksPup,
    pobierz_wiele_pup,
    pobierz_zielona_linia,
    teraz_iso,
    uzupelnij_szczegoly,
)

log = logging.getLogger(__name__)


@dataclass
class WynikSkanu:
    dzis: date
    wpisy: list[Wpis] = field(default_factory=list)
    nowe: list[Wpis] = field(default_factory=list)
    nowe_do_alertu: list[Wpis] = field(default_factory=list)
    bledy: dict[str, str] = field(default_factory=dict)
    statystyki: dict = field(default_factory=dict)


def _kandydat_na_szczegoly(w: Wpis) -> bool:
    if w.kategoria in KATEGORIE_ALERTU or w.kategoria == ZAKONCZENIE:
        return not (w.nabor_do or w.tryb == "do wyczerpania środków") or w.zrodlo == "pup"
    # ogólny tytuł („Ogłoszenie o naborze wniosków”, „Środki z Funduszu Pracy”) – sprawdzamy treść
    _, t = rozbij_tytul_zl(w.tytul)
    return w.pewnosc == "niska" and bool(SYGNAL_NABORU.search(normalizuj(t)))


def skanuj(
    stan: Stan,
    pupy: list[Pup],
    indeks: IndeksPup,
    dzis: date,
    zrodla: tuple[str, ...] = ("zl", "pup"),
    zl_od: date | None = None,
    strony: int = 1,
    szczegoly: bool = True,
    klient: Klient | None = None,
) -> WynikSkanu:
    klient = klient or Klient()
    wynik = WynikSkanu(dzis=dzis)
    teraz = teraz_iso()

    # 1. Zielona Linia
    if "zl" in zrodla:
        if zl_od is None:
            ostatni = stan.dane.get("ostatni_skan_zl", "")[:10]
            zl_od = (date.fromisoformat(ostatni) - timedelta(days=3)) if ostatni else dzis - timedelta(days=k.ZL_DNI_WSTECZ)
        zl, bledy_zl = pobierz_zielona_linia(klient, zl_od, indeks)
        for i, b in enumerate(bledy_zl):
            wynik.bledy[f"zielonalinia{'' if i == 0 else i}"] = b
        if not bledy_zl:
            stan.dane["ostatni_skan_zl"] = teraz
        wynik.statystyki["zielonalinia_wpisy"] = len(zl)
        wynik.statystyki["zielonalinia_od"] = zl_od.isoformat()
        wynik.wpisy.extend(zl)

    # 2. Strony PUP
    if "pup" in zrodla and pupy:
        wpisy_pup, bledy_pup = pobierz_wiele_pup(klient, pupy, strony)
        wynik.bledy.update(bledy_pup)
        wynik.statystyki["pup_sprawdzone"] = len(pupy)
        wynik.statystyki["pup_ok"] = len(pupy) - len(bledy_pup)
        wynik.statystyki["pup_wpisy"] = len(wpisy_pup)
        zr = stan.dane.setdefault("zrodla", {})
        for p in pupy:
            zr[p.pup_id] = {
                **zr.get(p.pup_id, {}),
                "ostatnia_proba": teraz,
                **({"ostatni_blad": bledy_pup[p.pup_id]} if p.pup_id in bledy_pup else {"ostatni_ok": teraz, "ostatni_blad": ""}),
            }
        wynik.wpisy.extend(wpisy_pup)

    # 3. Klasyfikacja wstępna (tytuł + zajawka / treść z API)
    for w in wynik.wpisy:
        klasyfikuj(w, dzis)
        w.klucz = klucz_wpisu(w)

    # 4. Pełna treść ogłoszenia dla kandydatów, których jeszcze nie znamy ze szczegółami
    if szczegoly:
        def znany_ze_szczegolami(w: Wpis) -> bool:
            kl = stan.znajdz(w)
            return kl is not None and len(stan.wpisy[kl].tresc) > 400

        granica = (dzis - timedelta(days=30)).isoformat()
        kandydaci = [w for w in wynik.wpisy if _kandydat_na_szczegoly(w) and not znany_ze_szczegolami(w)
                     and (w.zrodlo == "pup" or w.url_urzedu) and (w.data_publikacji or dzis.isoformat()) >= granica]
        # najpierw ogłoszenia ze stron urzędów i najnowsze (limit zapytań na skan)
        kandydaci.sort(key=lambda w: w.data_publikacji or "9999", reverse=True)
        kandydaci.sort(key=lambda w: w.zrodlo != "pup")
        kandydaci = kandydaci[: k.PUP_MAKS_SZCZEGOLOW]
        with ThreadPoolExecutor(max_workers=k.MAKS_ROWNOLEGLYCH) as pula:
            udane = sum(pula.map(lambda w: uzupelnij_szczegoly(klient, w), kandydaci))
        for w in kandydaci:
            klasyfikuj(w, dzis)
        wynik.statystyki["szczegoly_pobrane"] = udane
        wynik.statystyki["szczegoly_kandydaci"] = len(kandydaci)

    # 5. Stan
    wynik.nowe = stan.aktualizuj(wynik.wpisy, teraz)
    wynik.nowe_do_alertu = do_alertu(wynik.nowe, dzis)
    stan.dane["ostatni_skan"] = teraz
    stan.przytnij(dzis)
    wynik.statystyki["kategorie"] = dict(Counter(w.kategoria for w in wynik.wpisy))
    wynik.statystyki["nowe"] = len(wynik.nowe)
    wynik.statystyki["nowe_do_alertu"] = len(wynik.nowe_do_alertu)
    wynik.statystyki["http"] = dict(klient.statystyki)
    stan.dane["ostatni_skan_info"] = {"dzis": dzis.isoformat(), "statystyki": wynik.statystyki, "bledy": wynik.bledy}
    klient.zapisz_cache()
    return wynik


def rekord_naboru(w: Wpis, dzis: date) -> dict:
    d = w.do_slownika()
    d["status"] = status(w, dzis) or ("zakończony" if w.kategoria == ZAKONCZENIE else "")
    d["dni_do_konca"] = dni_do_konca(w, dzis)
    return d


def zapisz_wyniki(stan: Stan, wynik: WynikSkanu, rok: int = 2026) -> None:
    dzis = wynik.dzis
    nabory = [w for w in stan.nabory() if (w.data_publikacji or w.nabor_od or "")[:4] == str(rok)]
    nabory.sort(key=lambda w: (w.data_publikacji, w.pup_id), reverse=True)
    aktywne = do_alertu(nabory, dzis)
    dane = {
        "wygenerowano": teraz_iso(),
        "dzis": dzis.isoformat(),
        "opis": "Nabory wniosków o środki na podjęcie działalności gospodarczej (PUP) wykryte przez monitor alerty/",
        "liczba_wszystkich": len(nabory),
        "liczba_aktywnych_dzis": len(aktywne),
        "nabory": [rekord_naboru(w, dzis) for w in nabory],
    }
    k.PLIK_NABORY.parent.mkdir(parents=True, exist_ok=True)
    k.PLIK_NABORY.write_text(json.dumps(dane, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    k.PLIK_NOWE_JSON.write_text(
        json.dumps([rekord_naboru(w, dzis) for w in wynik.nowe_do_alertu], ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    k.PLIK_NOWE_ALERT.write_text(markdown_issue(wynik.nowe_do_alertu, dzis), encoding="utf-8")
    stan.zapisz()
