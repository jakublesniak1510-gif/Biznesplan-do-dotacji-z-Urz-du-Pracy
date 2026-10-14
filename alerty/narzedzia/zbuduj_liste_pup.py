"""Buduje `alerty/pup-lista.csv` z wykazu urzędów i sprawdza subdomeny *.praca.gov.pl.

Źródła wykazu (`narzedzia/wykaz-pup.csv`):
- nazwy i województwa: MRPiPS, „Wskaźniki efektywności podstawowych form aktywizacji zawodowej uzyskane
  w powiatowych urzędach pracy w roku 2025” (załącznik do informacji DF-VIII.6022.8.2026,
  https://www.gov.pl/attachment/97f4922b-ed14-467c-8fe0-ec52678a2c57), 340 urzędów,
  + Miejski Urząd Pracy w Radomiu (nie ma go w tym zestawieniu, a działa) = 341,
- kandydaci subdomen: linki do stron urzędów w treści wpisów Zielonej Linii (2026), ręczne uzupełnienia
  dla urzędów miejskich/grodzkich, a dla reszty nazwa miasta bez polskich znaków.

Potwierdzenie subdomeny = strona `https://[subdomena].praca.gov.pl/rynek-pracy/aktualnosci` odpowiada 200,
ma listę aktualności w szablonie praca.gov.pl, a nagłówek strony zawiera nazwę urzędu.

Użycie (z katalogu alerty/):  python narzedzia/zbuduj_liste_pup.py [--bez-weryfikacji]
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bs4 import BeautifulSoup  # noqa: E402

from monitor import konfiguracja as k  # noqa: E402
from monitor.pobieranie import Klient  # noqa: E402
from monitor.model import Pup  # noqa: E402
from monitor.zrodla import klucz_nazwy, parsuj_liste_aktualnosci  # noqa: E402

KATALOG = Path(__file__).resolve().parent
KOLUMNY = ["pup_id", "nazwa", "wojewodztwo", "miasto", "url", "sciezka_aktualnosci", "subdomena_potwierdzona",
           "zrodlo_subdomeny", "nazwa_na_stronie", "uwagi"]
# kolejność prób: wspólny szablon, wariant „aktualności urzędu”, strona główna (lista aktualności na stronie głównej)
SCIEZKI = ["/rynek-pracy/aktualnosci", "/rynek-pracy/aktualnosci-urzedu", "/"]


def nazwa_ze_strony(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    h1 = soup.select_one("h1.sr-only") or soup.find("title")
    tekst = h1.get_text(" ", strip=True) if h1 else ""
    return re.sub(r"^Aktualności urzędu\s*-\s*", "", tekst).strip()


def zgodna(nazwa_wykaz: str, nazwa_strona: str, miasto: str) -> bool:
    a, b = klucz_nazwy(nazwa_wykaz), klucz_nazwy(nazwa_strona)
    if not b:
        return False
    rdzen = klucz_nazwy(miasto)[:5]
    return a == b or rdzen in b or b in a or a in b


def sprawdz(klient: Klient, wiersz: dict) -> dict:
    wynik = {"pup_id": "", "url": "", "sciezka": SCIEZKI[0], "nazwa_na_stronie": "", "potwierdzona": False, "blad": ""}
    for kandydat in wiersz["kandydaci_subdomen"].split("|"):
        url = f"https://{kandydat}.praca.gov.pl"
        for sciezka in SCIEZKI:
            odp = klient.pobierz(url + sciezka, uzyj_cache=False)
            if not odp.ok or not odp.tekst:
                wynik["blad"] = f"{kandydat}{sciezka}: {odp.blad}"
                if odp.status == 0:  # brak hosta: nie próbujemy innych ścieżek
                    break
                continue
            nazwa = nazwa_ze_strony(odp.tekst)
            ma_liste = bool(parsuj_liste_aktualnosci(odp.tekst, Pup(kandydat, "", "", url), url + sciezka))
            wynik.update(pup_id=kandydat, url=url, nazwa_na_stronie=nazwa)
            if ma_liste and zgodna(wiersz["nazwa"], nazwa, wiersz["miasto"]):
                wynik.update(potwierdzona=True, blad="", sciezka=sciezka)
                return wynik
            wynik["blad"] = f"{kandydat}{sciezka}: {'brak listy aktualności' if not ma_liste else 'inna nazwa: ' + nazwa}"
    return wynik


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bez-weryfikacji", action="store_true")
    ap.add_argument("--wyjscie", default=str(k.PLIK_LISTA_PUP))
    ap.add_argument("--tylko-niepotwierdzone", action="store_true",
                    help="sprawdź ponownie tylko urzędy bez potwierdzenia w istniejącym pup-lista.csv")
    args = ap.parse_args()
    with open(KATALOG / "wykaz-pup.csv", encoding="utf-8", newline="") as f:
        wykaz = list(csv.DictReader(f))
    dzis = date.today().isoformat()
    poprzednie: dict[str, dict] = {}
    if args.tylko_niepotwierdzone and Path(args.wyjscie).exists():
        with open(args.wyjscie, encoding="utf-8", newline="") as f:
            poprzednie = {w["nazwa"]: w for w in csv.DictReader(f)}
    if args.bez_weryfikacji:
        wyniki = [{"pup_id": w["kandydaci_subdomen"].split("|")[0], "url": "", "sciezka": SCIEZKI[0], "nazwa_na_stronie": "",
                   "potwierdzona": False, "blad": ""} for w in wykaz]
    else:
        klient = Klient()
        def sprawdz_lub_zostaw(w: dict) -> dict:
            p = poprzednie.get(w["nazwa"])
            if p and p.get("subdomena_potwierdzona"):
                return {"pup_id": p["pup_id"], "url": p["url"], "sciezka": p.get("sciezka_aktualnosci") or SCIEZKI[0],
                        "nazwa_na_stronie": p["nazwa_na_stronie"], "potwierdzona": True, "blad": "",
                        "data": p["subdomena_potwierdzona"]}
            return sprawdz(klient, w)

        with ThreadPoolExecutor(max_workers=k.MAKS_ROWNOLEGLYCH) as pula:
            wyniki = list(pula.map(sprawdz_lub_zostaw, wykaz))
        klient.zapisz_cache()  # robots.txt zapamiętane na tydzień
        print(f"Zapytania HTTP: {klient.statystyki}")
    wiersze = []
    for w, r in zip(wykaz, wyniki):
        pup_id = r["pup_id"] or w["kandydaci_subdomen"].split("|")[0]
        uwagi = "; ".join(filter(None, [w.get("uwagi", ""), "" if r["potwierdzona"] else f"NIEPOTWIERDZONA {r['blad']}".strip()]))
        wiersze.append({
            "pup_id": pup_id, "nazwa": w["nazwa"], "wojewodztwo": w["wojewodztwo"], "miasto": w["miasto"],
            "url": r["url"] or f"https://{pup_id}.praca.gov.pl",
            "sciezka_aktualnosci": r.get("sciezka", SCIEZKI[0]),
            "subdomena_potwierdzona": (r.get("data") or dzis) if r["potwierdzona"] else "",
            "zrodlo_subdomeny": w["zrodlo_subdomeny"], "nazwa_na_stronie": r["nazwa_na_stronie"], "uwagi": uwagi,
        })
    with open(args.wyjscie, "w", encoding="utf-8", newline="") as f:
        pisz = csv.DictWriter(f, fieldnames=KOLUMNY)
        pisz.writeheader()
        pisz.writerows(wiersze)
    potw = sum(1 for w in wiersze if w["subdomena_potwierdzona"])
    print(f"Zapisano {len(wiersze)} urzędów, potwierdzone subdomeny: {potw}")
    for w in wiersze:
        if not w["subdomena_potwierdzona"]:
            print(f"  NIE: {w['nazwa']} ({w['wojewodztwo']}): {w['uwagi']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
