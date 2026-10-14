"""Uprzejmy klient HTTP.

- własny User-Agent z kontaktem,
- respektowanie robots.txt (Allow/Disallow + Crawl-delay),
- odstępy między zapytaniami do tej samej grupy hostów (wszystkie *.praca.gov.pl = jedna grupa),
- limit równoległości (semafor),
- warunkowe GET z ETag / Last-Modified oraz skrót treści (pomijamy parsowanie, gdy nic się nie zmieniło),
- 1 ponowienie przy błędzie sieci/5xx, obsługa 429 (Retry-After).
"""

from __future__ import annotations

import hashlib
import json
import logging
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

import requests
from requests.structures import CaseInsensitiveDict

from monitor import konfiguracja as k

log = logging.getLogger(__name__)

ROBOTS_WAZNOSC_S = 7 * 24 * 3600  # robots.txt odświeżamy raz w tygodniu


@dataclass
class Odpowiedz:
    url: str
    status: int
    tekst: str | None
    niezmieniona: bool = False  # 304 albo ten sam skrót treści co ostatnio
    blad: str | None = None
    naglowki: CaseInsensitiveDict | dict | None = None

    @property
    def ok(self) -> bool:
        return self.blad is None and self.status in (200, 304)


def grupa_hosta(host: str) -> str:
    """Hosty na wspólnej infrastrukturze traktujemy jako jeden serwer (wspólny limit tempa)."""
    host = host.lower()
    if host.endswith(".praca.gov.pl") or host == "praca.gov.pl":
        return "praca.gov.pl"
    return host


class Klient:
    def __init__(
        self,
        user_agent: str = k.USER_AGENT,
        odstep_s: float = k.ODSTEP_GRUPA_S,
        maks_rownoleglych: int = k.MAKS_ROWNOLEGLYCH,
        katalog_cache: Path | None = k.KATALOG_CACHE,
        sesja: requests.Session | None = None,
        respektuj_robots: bool = True,
    ) -> None:
        self.user_agent = user_agent
        self.odstep_s = odstep_s
        self.semafor = threading.BoundedSemaphore(maks_rownoleglych)
        self.sesja = sesja or requests.Session()
        self.sesja.headers.update(
            {
                "User-Agent": user_agent,
                "Accept-Language": "pl,en;q=0.5",
                "From": k.KONTAKT if "@" in k.KONTAKT else "",
            }
        )
        if not self.sesja.headers.get("From"):
            del self.sesja.headers["From"]
        self.respektuj_robots = respektuj_robots
        self._robots: dict[str, RobotFileParser | None] = {}
        self._ostatnie: dict[str, float] = {}
        self._blokada = threading.Lock()
        self._blokady_grup: dict[str, threading.Lock] = {}
        self.katalog_cache = katalog_cache
        self._cache: dict[str, dict] = {}
        self._plik_cache = katalog_cache / "http-cache.json" if katalog_cache else None
        if self._plik_cache and self._plik_cache.exists():
            try:
                self._cache = json.loads(self._plik_cache.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                self._cache = {}
        self.statystyki = {"zapytania": 0, "niezmienione": 0, "bledy": 0, "zablokowane_robots": 0}

    # ---------- robots.txt ----------
    def _robots_dla(self, url: str) -> RobotFileParser | None:
        cz = urlsplit(url)
        baza = f"{cz.scheme}://{cz.netloc}"
        with self._blokada:
            if baza in self._robots:
                return self._robots[baza]
        rp: RobotFileParser | None = RobotFileParser()
        klucz = "robots:" + baza
        zapamietany = self._cache.get(klucz)
        if zapamietany and time.time() - zapamietany.get("ts", 0) < ROBOTS_WAZNOSC_S:
            if zapamietany.get("zakaz"):
                rp.disallow_all = True
            else:
                rp.parse(zapamietany["linie"])
        else:
            try:
                self._czekaj(grupa_hosta(cz.netloc), 0)
                r = self.sesja.get(baza + "/robots.txt", timeout=k.TIMEOUT_S)
                self.statystyki["zapytania"] += 1
                linie: list[str] = []
                zakaz = False
                if r.status_code == 200 and "text/plain" in r.headers.get("Content-Type", "text/plain"):
                    linie = r.text.splitlines()
                elif r.status_code in (401, 403):
                    zakaz = True
                # 404 / przekierowanie na stronę HTML = brak ograniczeń
                if zakaz:
                    rp.disallow_all = True
                else:
                    rp.parse(linie)
                self._cache[klucz] = {"linie": linie, "zakaz": zakaz, "ts": time.time()}
            except requests.RequestException as e:
                log.warning("robots.txt niedostępny dla %s: %s", baza, e)
                rp = None  # nie wiemy: pozwalamy, ale z domyślnym odstępem
        with self._blokada:
            self._robots[baza] = rp
        return rp

    def dozwolone(self, url: str) -> bool:
        if not self.respektuj_robots:
            return True
        rp = self._robots_dla(url)
        return True if rp is None else rp.can_fetch(self.user_agent, url)

    def opoznienie_dla(self, url: str) -> float:
        rp = self._robots_dla(url) if self.respektuj_robots else None
        cd = None
        if rp is not None:
            try:
                cd = rp.crawl_delay(self.user_agent)
            except AttributeError:
                cd = None
        return min(max(self.odstep_s, float(cd or 0)), k.MAKS_CRAWL_DELAY_S)

    # ---------- tempo ----------
    def _czekaj(self, grupa: str, odstep: float) -> None:
        with self._blokada:
            blok = self._blokady_grup.setdefault(grupa, threading.Lock())
        with blok:
            teraz = time.monotonic()
            nastepny = self._ostatnie.get(grupa, 0.0) + odstep
            if nastepny > teraz:
                time.sleep(nastepny - teraz)
            self._ostatnie[grupa] = time.monotonic()

    # ---------- GET ----------
    def pobierz(self, url: str, params: dict | None = None, uzyj_cache: bool = True) -> Odpowiedz:
        pelny = requests.Request("GET", url, params=params).prepare().url or url
        if not self.dozwolone(pelny):
            self.statystyki["zablokowane_robots"] += 1
            return Odpowiedz(pelny, 0, None, blad="zablokowane przez robots.txt")
        grupa = grupa_hosta(urlsplit(pelny).netloc)
        odstep = self.opoznienie_dla(pelny)
        naglowki = {}
        wpis_cache = self._cache.get(pelny, {}) if uzyj_cache else {}
        if wpis_cache.get("etag"):
            naglowki["If-None-Match"] = wpis_cache["etag"]
        if wpis_cache.get("last_modified"):
            naglowki["If-Modified-Since"] = wpis_cache["last_modified"]

        with self.semafor:
            for proba in range(2):
                self._czekaj(grupa, odstep)
                try:
                    r = self.sesja.get(pelny, headers=naglowki, timeout=k.TIMEOUT_S)
                    self.statystyki["zapytania"] += 1
                except requests.RequestException as e:
                    if proba == 0:
                        time.sleep(5)
                        continue
                    self.statystyki["bledy"] += 1
                    return Odpowiedz(pelny, 0, None, blad=f"{type(e).__name__}: {e}")
                if r.status_code == 429 or r.status_code >= 500:
                    if proba == 0:
                        czekaj = r.headers.get("Retry-After", "10")
                        time.sleep(min(float(czekaj) if czekaj.isdigit() else 10, 60))
                        continue
                    self.statystyki["bledy"] += 1
                    return Odpowiedz(pelny, r.status_code, None, blad=f"HTTP {r.status_code}")
                break

        if r.status_code == 304:
            self.statystyki["niezmienione"] += 1
            return Odpowiedz(pelny, 304, None, niezmieniona=True)
        if r.status_code != 200:
            self.statystyki["bledy"] += 1
            return Odpowiedz(pelny, r.status_code, None, blad=f"HTTP {r.status_code}")
        r.encoding = r.encoding or "utf-8"
        if "charset" not in r.headers.get("Content-Type", ""):
            r.encoding = "utf-8"
        tekst = r.text
        skrot = hashlib.sha256(tekst.encode("utf-8", "ignore")).hexdigest()[:16]
        niezmieniona = uzyj_cache and wpis_cache.get("skrot") == skrot
        if niezmieniona:
            self.statystyki["niezmienione"] += 1
        self._cache[pelny] = {
            "etag": r.headers.get("ETag"),
            "last_modified": r.headers.get("Last-Modified"),
            "skrot": skrot,
            "pobrano": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        return Odpowiedz(pelny, 200, tekst, niezmieniona=niezmieniona, naglowki=CaseInsensitiveDict(r.headers))

    def zapisz_cache(self) -> None:
        if not self._plik_cache:
            return
        self._plik_cache.parent.mkdir(parents=True, exist_ok=True)
        self._plik_cache.write_text(
            json.dumps(self._cache, ensure_ascii=False, indent=0, sort_keys=True), encoding="utf-8"
        )
