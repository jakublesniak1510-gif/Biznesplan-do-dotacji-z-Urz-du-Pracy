"""Pobieranie aktualności: Zielona Linia (WordPress REST API) i strony PUP (szablon praca.gov.pl).

Zasada: z każdego źródła wyciągamy surowe wpisy (`Wpis`), klasyfikacja dzieje się osobno.
"""

from __future__ import annotations

import csv
import html as html_lib
import json
import logging
import re
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlsplit

from bs4 import BeautifulSoup

from monitor import konfiguracja as k
from monitor.klasyfikator import rozbij_tytul_zl
from monitor.model import Pup, Wpis
from monitor.pobieranie import Klient

log = logging.getLogger(__name__)

MAKS_TRESC = 4000  # znaków treści zapisywanych przy wpisie


# --------------------------------------------------------------------------------------
# Lista PUP
# --------------------------------------------------------------------------------------
def wczytaj_liste_pup(sciezka: Path = k.PLIK_LISTA_PUP) -> list[Pup]:
    with open(sciezka, encoding="utf-8", newline="") as f:
        return [
            Pup(
                pup_id=w["pup_id"],
                nazwa=w["nazwa"],
                wojewodztwo=w["wojewodztwo"],
                url=w["url"],
                miasto=w.get("miasto", ""),
                subdomena_potwierdzona=w.get("subdomena_potwierdzona", ""),
                sciezka_aktualnosci=w.get("sciezka_aktualnosci") or k.PUP_SCIEZKA_AKTUALNOSCI,
            )
            for w in csv.DictReader(f)
        ]


def klucz_nazwy(tekst: str) -> str:
    """„Gorzów Wielkopolski” → „gorzowwielkopolski” (bez znaków diakrytycznych, spacji, myślników)."""
    t = unicodedata.normalize("NFKD", tekst.lower().replace("ł", "l"))
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", t)


class IndeksPup:
    """Szybkie wyszukiwanie PUP po hoście (subdomenie) i po nazwie miasta z tytułu Zielonej Linii."""

    def __init__(self, pupy: list[Pup]) -> None:
        self.pupy = pupy
        self.po_hoscie = {p.host.lower(): p for p in pupy}
        self.po_id = {p.pup_id: p for p in pupy}
        self.po_miescie: dict[str, Pup] = {}
        for p in pupy:
            for nazwa in filter(None, [p.miasto, *p.miasto.split("|")]):
                self.po_miescie.setdefault(klucz_nazwy(nazwa), p)
            self.po_miescie.setdefault(klucz_nazwy(p.pup_id), p)

    def po_url(self, url: str) -> Pup | None:
        return self.po_hoscie.get(urlsplit(url).netloc.lower())

    def po_nazwie(self, miasto: str) -> Pup | None:
        if not miasto:
            return None
        kl = klucz_nazwy(miasto)
        if kl in self.po_miescie:
            return self.po_miescie[kl]
        # „Mińska Mazowiecki”, „Nakle nad Notecią”: dopasowanie po prefiksie (min. 5 znaków)
        kandydaci = [p for kk, p in self.po_miescie.items() if len(kl) >= 5 and (kk.startswith(kl[:6]))]
        return kandydaci[0] if len(kandydaci) == 1 else None


# --------------------------------------------------------------------------------------
# Pomocnicze
# --------------------------------------------------------------------------------------
def html_na_tekst(fragment: str) -> str:
    if not fragment:
        return ""
    soup = BeautifulSoup(fragment, "lxml")
    for s in soup(["script", "style", "noscript"]):
        s.decompose()
    tekst = soup.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", tekst).strip()


def _data_pl(tekst: str) -> str:
    m = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", tekst or "")
    if not m:
        return ""
    try:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1))).isoformat()
    except ValueError:
        return ""


# --------------------------------------------------------------------------------------
# Zielona Linia
# --------------------------------------------------------------------------------------
def parsuj_zielona_linia(dane: list[dict], indeks: IndeksPup | None = None) -> list[Wpis]:
    """Zamienia odpowiedź `GET /wp-json/wp/v2/posts` na wpisy."""
    wyniki = []
    for post in dane:
        tytul = html_lib.unescape(post.get("title", {}).get("rendered", "")).strip()
        tresc_html = post.get("content", {}).get("rendered", "") or post.get("excerpt", {}).get("rendered", "")
        soup = BeautifulSoup(tresc_html or "", "lxml")
        url_urzedu = ""
        for a in soup.find_all("a", href=True):
            host = urlsplit(a["href"]).netloc.lower()
            if host.endswith(".praca.gov.pl") and not host.startswith(("www.", "psz.", "oferty.", "eures.")):
                url_urzedu = a["href"]
                break
        miasto, _ = rozbij_tytul_zl(tytul)
        pup = (indeks.po_url(url_urzedu) if indeks and url_urzedu else None) or (
            indeks.po_nazwie(miasto) if indeks else None
        )
        wyniki.append(
            Wpis(
                zrodlo="zielonalinia",
                tytul=tytul,
                url=post.get("link", ""),
                data_publikacji=(post.get("date") or "")[:10],
                pup_id=pup.pup_id if pup else "",
                pup_nazwa=pup.nazwa if pup else (f"PUP {miasto}" if miasto else ""),
                wojewodztwo=pup.wojewodztwo if pup else "",
                tresc=html_na_tekst(tresc_html)[:MAKS_TRESC],
                url_urzedu=url_urzedu,
            )
        )
    return wyniki


def pobierz_zielona_linia(klient: Klient, po: date, indeks: IndeksPup | None = None,
                          maks_stron: int = 30) -> tuple[list[Wpis], list[str]]:
    """Wpisy z kategorii „Informacje z regionów” opublikowane po dacie `po`."""
    wpisy: list[Wpis] = []
    bledy: list[str] = []
    strona = 1
    while strona <= maks_stron:
        params = {
            "categories": k.ZL_KATEGORIA_REGIONY,
            "after": f"{po.isoformat()}T00:00:00",
            "per_page": 100,
            "page": strona,
            "orderby": "date",
            "order": "desc",
            "_fields": "id,date,modified,link,title,content",
        }
        odp = klient.pobierz(k.ZL_API, params=params, uzyj_cache=False)
        if not odp.ok or odp.tekst is None:
            if odp.status == 400 and strona > 1:  # za daleko: rest_post_invalid_page_number
                break
            bledy.append(f"Zielona Linia, strona {strona}: {odp.blad}")
            break
        dane = json.loads(odp.tekst)
        wpisy.extend(parsuj_zielona_linia(dane, indeks))
        stron = int((odp.naglowki or {}).get("X-WP-TotalPages", "1") or 1)
        if strona >= stron or not dane:
            break
        strona += 1
    return wpisy, bledy


# --------------------------------------------------------------------------------------
# Strony PUP (szablon praca.gov.pl)
# --------------------------------------------------------------------------------------
# Selektory wspólnego szablonu (Liferay, motyw „nnk-theme”), sprawdzone 14.10.2026
SEL_ELEMENT = ".nnk-article-list .nnk-article-list-article-content"
SEL_DATA = ".nnk-article-list-article-publish-date"
SEL_LINK = ".nnk-article-link-underline a[href]"
SEL_TYTUL = "h3"
SEL_ZAJAWKA = ".nnk-article-list-article-summary"
SEL_STRONICOWANIE = ".pagination a[href], .lfr-pagination a[href]"
# wariant zapasowy: karuzela na stronie głównej (np. PUP Krasnystaw, Środa Wlkp.): brak dat na liście
SEL_KARUZELA = "a[href*='/-/asset_publisher/'][href*='/content/']"
# stałe strony szablonu (nie aktualności), które też są linkami „/content/”
POMIN_TRESCI = ("przygotowanie-ogloszenia-o-poszukiwaniu-pracy",)
# strona pojedynczej aktualności
SEL_SZCZ_TYTUL = ".asset-full-content .asset-title"
SEL_SZCZ_TRESC = ".asset-full-content .asset-content .journal-content-article"


def parsuj_liste_aktualnosci(html: str, pup: Pup, url_bazowy: str | None = None) -> list[Wpis]:
    soup = BeautifulSoup(html, "lxml")
    baza = url_bazowy or pup.url
    wyniki = []
    for el in soup.select(SEL_ELEMENT):
        a = el.select_one(SEL_LINK)
        if not a:
            continue
        h = a.select_one(SEL_TYTUL) or a
        d = el.select_one(SEL_DATA)
        z = el.select_one(SEL_ZAJAWKA)
        wyniki.append(
            Wpis(
                zrodlo="pup",
                tytul=re.sub(r"\s+", " ", h.get_text(" ", strip=True)),
                url=urljoin(baza, a["href"]),
                data_publikacji=_data_pl(d.get_text(strip=True) if d else ""),
                pup_id=pup.pup_id,
                pup_nazwa=pup.nazwa,
                wojewodztwo=pup.wojewodztwo,
                tresc=re.sub(r"\s+", " ", z.get_text(" ", strip=True)).rstrip(".").strip() if z else "",
            )
        )
    if not wyniki:
        wyniki = _parsuj_karuzele(soup, pup, baza)
    return wyniki


def _parsuj_karuzele(soup: BeautifulSoup, pup: Pup, baza: str) -> list[Wpis]:
    widziane, wyniki = set(), []
    for a in soup.select(SEL_KARUZELA):
        url = urljoin(baza, a["href"])
        if url in widziane or any(p in url for p in POMIN_TRESCI) or pup.host not in url:
            continue
        tytul_el = a.select_one(".nnk_slider-asset-title, h2, h3, h4")
        tytul = re.sub(r"\s+", " ", (tytul_el or a).get_text(" ", strip=True))
        if len(tytul) < 8 or tytul.lower() in ("czytaj więcej", "więcej"):
            continue
        widziane.add(url)
        wyniki.append(Wpis(zrodlo="pup", tytul=tytul, url=url, pup_id=pup.pup_id, pup_nazwa=pup.nazwa,
                           wojewodztwo=pup.wojewodztwo))
    return wyniki


def link_do_strony(html: str, numer: int) -> str | None:
    soup = BeautifulSoup(html, "lxml")
    for a in soup.select(SEL_STRONICOWANIE):
        if a.get_text(strip=True) == str(numer) and "_cur=" in a["href"]:
            return a["href"]
    return None


def parsuj_szczegoly(html: str) -> tuple[str, str]:
    """(tytuł, treść) ze strony pojedynczej aktualności."""
    soup = BeautifulSoup(html, "lxml")
    t = soup.select_one(SEL_SZCZ_TYTUL)
    c = soup.select_one(SEL_SZCZ_TRESC)
    tytul = re.sub(r"\s+", " ", t.get_text(" ", strip=True)) if t else ""
    tresc = html_na_tekst(str(c)) if c else ""
    return tytul, tresc[:MAKS_TRESC]


def pobierz_pup(klient: Klient, pup: Pup, strony: int = 1) -> tuple[list[Wpis], str | None]:
    """Lista aktualności jednego PUP (pierwsza strona = 10-15 najnowszych wpisów)."""
    url = pup.url.rstrip("/") + (pup.sciezka_aktualnosci or k.PUP_SCIEZKA_AKTUALNOSCI)
    wpisy: list[Wpis] = []
    for nr in range(1, strony + 1):
        odp = klient.pobierz(url)
        if not odp.ok or odp.tekst is None:
            if odp.niezmieniona:
                return wpisy, None
            return wpisy, odp.blad or f"HTTP {odp.status}"
        nowe = parsuj_liste_aktualnosci(odp.tekst, pup, url)
        if nr == 1 and not nowe:
            return wpisy, "brak listy aktualności (inny szablon albo pusta strona)"
        wpisy.extend(nowe)
        if nr < strony:
            nastepny = link_do_strony(odp.tekst, nr + 1)
            if not nastepny:
                break
            url = nastepny
    return wpisy, None


def pobierz_wiele_pup(klient: Klient, pupy: list[Pup], strony: int = 1) -> tuple[list[Wpis], dict[str, str]]:
    wpisy: list[Wpis] = []
    bledy: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=k.MAKS_ROWNOLEGLYCH) as pula:
        for pup, (w, blad) in zip(pupy, pula.map(lambda p: pobierz_pup(klient, p, strony), pupy)):
            wpisy.extend(w)
            if blad:
                bledy[pup.pup_id] = blad
    return wpisy, bledy


def uzupelnij_szczegoly(klient: Klient, wpis: Wpis) -> bool:
    """Dociąga pełną treść ogłoszenia ze strony PUP (tylko dla kandydatów na nabór)."""
    url = wpis.url if wpis.zrodlo == "pup" else wpis.url_urzedu
    if not url:
        return False
    odp = klient.pobierz(url, uzyj_cache=False)
    if not odp.ok or not odp.tekst:
        return False
    tytul, tresc = parsuj_szczegoly(odp.tekst)
    if tresc:
        wpis.tresc = tresc
    if tytul and wpis.zrodlo == "pup":
        wpis.tytul = tytul
    return bool(tresc)


def id_ogloszenia_praca_gov(url: str) -> str | None:
    """Stały identyfikator ogłoszenia z adresu praca.gov.pl: host#assetEntryId albo host#slug."""
    cz = urlsplit(url)
    if not cz.netloc.lower().endswith("praca.gov.pl"):
        return None
    q = parse_qs(cz.query)
    for klucz, wartosci in q.items():
        if klucz.endswith("assetEntryId") and wartosci and wartosci[0].isdigit():
            return f"{cz.netloc.lower()}#{wartosci[0]}"
    m = re.search(r"/content/([^/?#]+)", cz.path)
    if m:
        return f"{cz.netloc.lower()}#{m.group(1)}"
    return None


def teraz_iso() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
