"""Stan monitora w pliku JSON (bez bazy danych): znane wpisy, deduplikacja, nowe od ostatniego skanu.

Klucz wpisu:
- ogłoszenie na *.praca.gov.pl → `host#assetEntryId` (ten sam artykuł bywa pod kilkoma adresami:
  /strona-glowna/... i /rynek-pracy/aktualnosci/...),
- wpis Zielonej Linii z linkiem do strony urzędu → ten sam klucz co ogłoszenie urzędu
  (dzięki temu nabór z dwóch źródeł jest jednym wpisem),
- pozostałe wpisy Zielonej Linii → `zl#slug`.
Dodatkowo deduplikacja przybliżona:
- ten sam PUP + ten sam znormalizowany tytuł + daty publikacji w odstępie do 5 dni (Zielona Linia publikuje
  z opóźnieniem 0–3 dni),
- ten sam PUP + ta sama kategoria + identyczne daty naboru od–do (tytuły na stronie urzędu i w Zielonej Linii
  często się różnią, a link w Zielonej Linii bywa tylko do strony głównej urzędu).
"""

from __future__ import annotations

import json
import re
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlsplit

from monitor import konfiguracja as k
from monitor.klasyfikator import KATEGORIE_ALERTU, ZAKONCZENIE, normalizuj, rozbij_tytul_zl
from monitor.model import Wpis
from monitor.zrodla import id_ogloszenia_praca_gov, teraz_iso

WERSJA = 1
RETENCJA_DNI = 120  # wpisy spoza kategorii alertu usuwamy po tym czasie od ostatniego widzenia
MAKS_TRESC_INNE = 0  # treści wpisów nieistotnych nie trzymamy (mniejszy plik stanu w repo)


def klucz_wpisu(wpis: Wpis) -> str:
    for url in (wpis.url if wpis.zrodlo == "pup" else "", wpis.url_urzedu):
        if url:
            kl = id_ogloszenia_praca_gov(url)
            if kl:
                return kl
    if wpis.zrodlo == "zielonalinia":
        sciezka = urlsplit(wpis.url).path.strip("/")
        return "zl#" + (sciezka.split("/")[-1] if sciezka else wpis.url)
    return wpis.url


def tytul_znormalizowany(tytul: str) -> str:
    _, t = rozbij_tytul_zl(tytul)
    t = normalizuj(t)
    t = re.sub(r"[^\w ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


class Stan:
    def __init__(self, dane: dict | None = None, sciezka: Path | None = None) -> None:
        self.sciezka = sciezka
        self.dane = dane or {"wersja": WERSJA, "ostatni_skan": "", "ostatni_skan_zl": "", "wpisy": {},
                             "zrodla": {}}
        self.wpisy: dict[str, Wpis] = {kl: Wpis.ze_slownika(w) for kl, w in self.dane.get("wpisy", {}).items()}
        self._indeks_tytulow: dict[tuple[str, str], list[str]] = {}
        self._indeks_dat: dict[tuple[str, str, str, str], str] = {}
        for kl, w in self.wpisy.items():
            self._dodaj_do_indeksu(kl, w)

    # ---------- plik ----------
    @classmethod
    def wczytaj(cls, sciezka: Path = k.PLIK_STAN) -> "Stan":
        if sciezka.exists():
            return cls(json.loads(sciezka.read_text(encoding="utf-8")), sciezka)
        return cls(None, sciezka)

    def zapisz(self, sciezka: Path | None = None) -> None:
        sciezka = sciezka or self.sciezka or k.PLIK_STAN
        self.dane["wersja"] = WERSJA
        self.dane["wpisy"] = {kl: w.do_slownika() for kl, w in sorted(self.wpisy.items())}
        sciezka.parent.mkdir(parents=True, exist_ok=True)
        sciezka.write_text(json.dumps(self.dane, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    # ---------- deduplikacja ----------
    @staticmethod
    def _klucz_dat(w: Wpis) -> tuple[str, str, str, str] | None:
        if w.pup_id and w.nabor_od and w.nabor_do and w.kategoria in KATEGORIE_ALERTU:
            return (w.pup_id, w.kategoria, w.nabor_od, w.nabor_do)
        return None

    def _dodaj_do_indeksu(self, kl: str, w: Wpis) -> None:
        if w.pup_id:
            self._indeks_tytulow.setdefault((w.pup_id, tytul_znormalizowany(w.tytul)), []).append(kl)
        kd = self._klucz_dat(w)
        if kd:
            self._indeks_dat.setdefault(kd, kl)

    def znajdz(self, wpis: Wpis) -> str | None:
        kl = wpis.klucz or klucz_wpisu(wpis)
        if kl in self.wpisy:
            return kl
        if not wpis.pup_id:
            return None
        for kand in self._indeks_tytulow.get((wpis.pup_id, tytul_znormalizowany(wpis.tytul)), []):
            inny = self.wpisy[kand]
            try:
                roznica = abs((date.fromisoformat(inny.data_publikacji) - date.fromisoformat(wpis.data_publikacji)).days)
            except ValueError:
                roznica = 0
            if roznica <= 5:
                return kand
        kd = self._klucz_dat(wpis)
        if kd and kd in self._indeks_dat and self._indeks_dat[kd] in self.wpisy:
            return self._indeks_dat[kd]
        return None

    def czy_znany(self, wpis: Wpis) -> bool:
        return self.znajdz(wpis) is not None

    def aktualizuj(self, wpisy: list[Wpis], teraz: str | None = None) -> list[Wpis]:
        """Dopisuje wpisy do stanu. Zwraca listę wpisów NOWYCH (niewidzianych wcześniej)."""
        teraz = teraz or teraz_iso()
        nowe: list[Wpis] = []
        for w in wpisy:
            w.klucz = w.klucz or klucz_wpisu(w)
            kl = self.znajdz(w)
            if kl is None:
                w.pierwszy_raz = w.pierwszy_raz or teraz
                if not w.data_publikacji:  # lista bez dat (karuzela): przyjmujemy datę pierwszego wykrycia
                    w.data_publikacji = w.pierwszy_raz[:10]
                w.ostatni_raz = teraz
                w.zrodla = sorted(set(w.zrodla) | {w.zrodlo})
                self.wpisy[w.klucz] = w
                self._dodaj_do_indeksu(w.klucz, w)
                nowe.append(w)
            else:
                self._scal(self.wpisy[kl], w, teraz)
                self._dodaj_do_indeksu(kl, self.wpisy[kl])
        self.oznacz_wstrzymane()
        return nowe

    def oznacz_wstrzymane(self) -> int:
        """Ogłoszenie „zakończenie / wstrzymanie naboru / lista rankingowa” zamyka wcześniejszy nabór tego PUP,
        jeśli ten nie miał daty końca (tryb „do wyczerpania środków”, ciągły albo brak dat)."""
        zakonczenia = [w for w in self.wpisy.values() if w.kategoria == ZAKONCZENIE and w.pup_id and w.data_publikacji]
        licznik = 0
        for z in zakonczenia:
            data_z = z.nabor_od if (z.nabor_od and z.nabor_od >= z.data_publikacji) else z.data_publikacji
            for w in self.wpisy.values():
                if (w.pup_id == z.pup_id and w.kategoria in KATEGORIE_ALERTU and not w.nabor_do and not w.wstrzymany
                        and w.data_publikacji and w.data_publikacji <= z.data_publikacji
                        and (date.fromisoformat(z.data_publikacji) - date.fromisoformat(w.data_publikacji)).days <= 120
                        and ("pfron" in normalizuj(z.tytul)) == ("PFRON" in w.zrodla_finansowania)):
                    w.wstrzymany = data_z
                    licznik += 1
        return licznik

    @staticmethod
    def _scal(stary: Wpis, nowy: Wpis, teraz: str) -> None:
        stary.ostatni_raz = teraz
        stary.zrodla = sorted(set(stary.zrodla) | {nowy.zrodlo})
        # ogłoszenie urzędu jest źródłem pierwotnym: jego adres i tytuł mają pierwszeństwo
        if nowy.zrodlo == "pup" and stary.zrodlo != "pup":
            stary.url_urzedu = nowy.url  # adres z listy aktualności urzędu jest kanoniczny
        if not stary.url_urzedu and nowy.url_urzedu:
            stary.url_urzedu = nowy.url_urzedu
        for pole in ("pup_id", "pup_nazwa", "wojewodztwo", "nabor_od", "nabor_do", "tryb", "kwota_opis"):
            if not getattr(stary, pole) and getattr(nowy, pole):
                setattr(stary, pole, getattr(nowy, pole))
        if stary.kwota_max_zl is None and nowy.kwota_max_zl is not None:
            stary.kwota_max_zl = nowy.kwota_max_zl
        if stary.liczba_miejsc is None and nowy.liczba_miejsc is not None:
            stary.liczba_miejsc = nowy.liczba_miejsc
        stary.zrodla_finansowania = sorted(set(stary.zrodla_finansowania) | set(nowy.zrodla_finansowania))
        stary.grupy_docelowe = sorted(set(stary.grupy_docelowe) | set(nowy.grupy_docelowe))
        if len(nowy.tresc) > len(stary.tresc):
            stary.tresc = nowy.tresc
        # pewniejsza klasyfikacja (np. po dociągnięciu pełnej treści) wygrywa
        ranga = {"wysoka": 3, "średnia": 2, "niska": 1, "": 0}
        if nowy.kategoria and ranga.get(nowy.pewnosc, 0) > ranga.get(stary.pewnosc, 0):
            stary.kategoria, stary.pewnosc = nowy.kategoria, nowy.pewnosc

    def przebuduj(self) -> int:
        """Ponowna deduplikacja całego stanu (np. po zmianie reguł). Zwraca liczbę scalonych wpisów."""
        stare = sorted(self.wpisy.values(), key=lambda w: (w.zrodlo != "pup", w.pierwszy_raz))
        przed = len(stare)
        self.wpisy, self._indeks_tytulow, self._indeks_dat = {}, {}, {}
        for w in stare:
            self.aktualizuj([w], w.ostatni_raz or None)
        return przed - len(self.wpisy)

    # ---------- porządki ----------
    def przytnij(self, dzis: date) -> int:
        """Skraca treść wpisów nieistotnych i usuwa bardzo stare. Zwraca liczbę usuniętych."""
        granica = (dzis - timedelta(days=RETENCJA_DNI)).isoformat()
        do_usuniecia = []
        for kl, w in self.wpisy.items():
            if w.kategoria not in KATEGORIE_ALERTU and w.kategoria != ZAKONCZENIE:
                w.tresc = w.tresc[:MAKS_TRESC_INNE]
                if (w.ostatni_raz or "")[:10] < granica:
                    do_usuniecia.append(kl)
        for kl in do_usuniecia:
            del self.wpisy[kl]
        return len(do_usuniecia)

    def nabory(self) -> list[Wpis]:
        return [w for w in self.wpisy.values() if w.kategoria in KATEGORIE_ALERTU or w.kategoria == ZAKONCZENIE]
