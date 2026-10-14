"""Ustawienia monitora. Wszystko, co zależy od środowiska, czytamy ze zmiennych env.

Sekretów (klucze API, hasła SMTP) nigdy nie zapisujemy w repozytorium.
"""

from __future__ import annotations

import os
from pathlib import Path

KATALOG_ALERTY = Path(__file__).resolve().parent.parent
KATALOG_DANE = Path(os.environ.get("ALERTY_KATALOG_DANE", KATALOG_ALERTY / "dane"))
PLIK_LISTA_PUP = Path(os.environ.get("ALERTY_LISTA_PUP", KATALOG_ALERTY / "pup-lista.csv"))
PLIK_STAN = KATALOG_DANE / "stan.json"
PLIK_NABORY = KATALOG_DANE / "nabory-2026.json"
PLIK_RAPORT = KATALOG_DANE / "raport-skanu.md"
PLIK_NOWE_ALERT = KATALOG_DANE / "nowe-alert.md"
PLIK_NOWE_JSON = KATALOG_DANE / "nowe.json"
KATALOG_CACHE = KATALOG_DANE / "cache"

# Kontakt w User-Agent: serwery urzędów widzą, kto pobiera i jak się z nim skontaktować.
# Ustaw ALERTY_KONTAKT na adres e-mail firmy (np. alerty@twojadomena.pl).
KONTAKT = os.environ.get(
    "ALERTY_KONTAKT",
    "https://github.com/jakublesniak1510-gif/Biznesplan-do-dotacji-z-Urz-du-Pracy",
)
USER_AGENT = os.environ.get(
    "ALERTY_USER_AGENT",
    f"AlertyNaborowPUP/1.0 (monitor naborow PUP; 1-2 zapytania na urzad dziennie; kontakt: {KONTAKT})",
)

# Uprzejme pobieranie
MAKS_ROWNOLEGLYCH = int(os.environ.get("ALERTY_MAKS_ROWNOLEGLYCH", "4"))
# minimalny odstęp między KOLEJNYMI zapytaniami do tej samej grupy hostów (np. *.praca.gov.pl
# stoją na jednej platformie, więc traktujemy je jak jeden serwer)
ODSTEP_GRUPA_S = float(os.environ.get("ALERTY_ODSTEP_S", "1.0"))
TIMEOUT_S = float(os.environ.get("ALERTY_TIMEOUT_S", "30"))
MAKS_CRAWL_DELAY_S = 60.0  # górna granica dla Crawl-delay z robots.txt

# Zielona Linia (WordPress REST API)
ZL_API = "https://zielonalinia.gov.pl/wp-json/wp/v2/posts"
ZL_KATEGORIA_REGIONY = 235  # „Informacje z regionów”
ZL_DNI_WSTECZ = int(os.environ.get("ALERTY_ZL_DNI_WSTECZ", "45"))

# Strony PUP (wspólny szablon praca.gov.pl / Liferay „nnk-theme”)
PUP_SCIEZKA_AKTUALNOSCI = "/rynek-pracy/aktualnosci"
PUP_MAKS_SZCZEGOLOW = int(os.environ.get("ALERTY_MAKS_SZCZEGOLOW", "40"))

# Alert
URL_ZAMOWIENIA = os.environ.get("ALERTY_URL_ZAMOWIENIA", "https://twojadomena.pl/zamow")
URL_QUIZ = os.environ.get("ALERTY_URL_QUIZ", "https://twojadomena.pl/quiz")
URL_WYPISZ = os.environ.get("ALERTY_URL_WYPISZ", "{{ unsubscribe }}")  # znacznik Brevo
NAZWA_USLUGI = os.environ.get("ALERTY_NAZWA_USLUGI", "[nazwa usługi]")
CENA_OD = os.environ.get("ALERTY_CENA_OD", "299 zł")
DANE_ADMINISTRATORA = os.environ.get(
    "ALERTY_ADMINISTRATOR", "[Administrator danych: firma, adres, NIP]"
)
