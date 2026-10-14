"""Eksport alertów pod narzędzie mailingowe (Brevo i inne) oraz opcjonalna wysyłka.

Domyślnie NIC nie jest wysyłane do subskrybentów automatycznie:
- eksport CSV/JSON/HTML (zawsze, bez sekretów),
- SMTP: wiadomość „do weryfikacji” dla właściciela (gdy ustawiono SMTP_*),
- Brevo: kampania tworzona jako SZKIC (gdy ustawiono BREVO_API_KEY); wysyłka natychmiastowa tylko przy
  BREVO_WYSYLAJ=1.

Zmienne środowiskowe (sekrety trzymamy w GitHub Secrets / menedżerze haseł, nigdy w repo):
  SMTP_HOST, SMTP_PORT (587), SMTP_USER, SMTP_PASSWORD, SMTP_FROM, ALERTY_EMAIL_WLASCICIELA
  BREVO_API_KEY, BREVO_NADAWCA_EMAIL, BREVO_NADAWCA_NAZWA, BREVO_LISTY (JSON: {"śląskie": 12, ...}),
  BREVO_WYSYLAJ ("1" = wyślij od razu, domyślnie szkic)
"""

from __future__ import annotations

import csv
import json
import os
import smtplib
import ssl
from datetime import date
from email.message import EmailMessage
from pathlib import Path

import requests

from monitor.alert import (
    grupuj_po_wojewodztwie,
    html_alertu,
    link_ogloszenia,
    nazwa_urzedu,
    opis_dat,
    tekst_alertu,
    temat_emaila,
    url_cta,
)
from monitor.klasyfikator import dni_do_konca, opis_terminu, rozbij_tytul_zl, status
from monitor.model import Wpis

BREVO_API = "https://api.brevo.com/v3"

KOLUMNY_CSV = [
    "wojewodztwo", "pup_id", "urzad", "tytul", "nabor_od", "nabor_do", "termin_opis", "dni_do_konca",
    "status", "tryb", "kwota_max_zl", "kwota_opis", "zrodla_finansowania", "grupy_docelowe", "liczba_miejsc",
    "link_ogloszenia", "link_cta", "data_publikacji", "zrodla", "temat_emaila",
]


def wiersz_eksportu(w: Wpis, dzis: date) -> dict:
    return {
        "wojewodztwo": w.wojewodztwo,
        "pup_id": w.pup_id,
        "urzad": nazwa_urzedu(w),
        "tytul": rozbij_tytul_zl(w.tytul)[1],
        "nabor_od": w.nabor_od,
        "nabor_do": w.nabor_do,
        "termin_opis": f"{opis_dat(w)} ({opis_terminu(w, dzis)})",
        "dni_do_konca": dni_do_konca(w, dzis),
        "status": status(w, dzis),
        "tryb": w.tryb,
        "kwota_max_zl": w.kwota_max_zl,
        "kwota_opis": w.kwota_opis,
        "zrodla_finansowania": " | ".join(w.zrodla_finansowania),
        "grupy_docelowe": " | ".join(w.grupy_docelowe),
        "liczba_miejsc": w.liczba_miejsc,
        "link_ogloszenia": link_ogloszenia(w),
        "link_cta": url_cta(w, dzis),
        "data_publikacji": w.data_publikacji,
        "zrodla": " | ".join(w.zrodla),
        "temat_emaila": temat_emaila([w], w.wojewodztwo),
    }


def eksport_csv(wpisy: list[Wpis], sciezka: Path, dzis: date) -> Path:
    """CSV (UTF-8 z BOM, separator „;”) do importu w arkuszu albo jako źródło danych kampanii."""
    sciezka.parent.mkdir(parents=True, exist_ok=True)
    with open(sciezka, "w", encoding="utf-8-sig", newline="") as f:
        pisz = csv.DictWriter(f, fieldnames=KOLUMNY_CSV, delimiter=";")
        pisz.writeheader()
        for w in wpisy:
            pisz.writerow(wiersz_eksportu(w, dzis))
    return sciezka


def eksport_json(wpisy: list[Wpis], sciezka: Path, dzis: date) -> Path:
    sciezka.parent.mkdir(parents=True, exist_ok=True)
    dane = {"wygenerowano": dzis.isoformat(), "liczba": len(wpisy), "nabory": [wiersz_eksportu(w, dzis) for w in wpisy]}
    sciezka.write_text(json.dumps(dane, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return sciezka


def eksport_kampanii(wpisy: list[Wpis], katalog: Path, dzis: date) -> list[Path]:
    """Dla każdego województwa: gotowy HTML i tekst e-maila + meta.json (temat, preheader)."""
    pliki = []
    katalog.mkdir(parents=True, exist_ok=True)
    for woj, lista in grupuj_po_wojewodztwie(wpisy).items():
        baza = katalog / f"alert-{dzis.isoformat()}-{_slug(woj)}"
        baza.with_suffix(".html").write_text(html_alertu(lista, woj, dzis), encoding="utf-8")
        baza.with_suffix(".txt").write_text(tekst_alertu(lista, woj, dzis), encoding="utf-8")
        meta = {"wojewodztwo": woj, "temat": temat_emaila(lista, woj),
                "preheader": "Termin, kwota i link do ogłoszenia. Co przygotować i jak zdążyć.",
                "liczba_naborow": len(lista)}
        baza.with_suffix(".json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
        pliki += [baza.with_suffix(".html"), baza.with_suffix(".txt"), baza.with_suffix(".json")]
    return pliki


def _slug(tekst: str) -> str:
    zamiany = str.maketrans("ąćęłńóśźż", "acelnoszz")
    return tekst.lower().translate(zamiany).replace(" ", "-")


# --------------------------------------------------------------------------------------
# SMTP (wiadomość do właściciela)
# --------------------------------------------------------------------------------------
def smtp_skonfigurowany() -> bool:
    return all(os.environ.get(z) for z in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "ALERTY_EMAIL_WLASCICIELA"))


def wyslij_smtp(temat: str, html_tresc: str, tekst: str, do: str | None = None) -> None:
    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT", "587"))
    uzytkownik = os.environ["SMTP_USER"]
    nadawca = os.environ.get("SMTP_FROM", uzytkownik)
    odbiorca = do or os.environ["ALERTY_EMAIL_WLASCICIELA"]
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = temat, nadawca, odbiorca
    msg.set_content(tekst)
    msg.add_alternative(html_tresc, subtype="html")
    kontekst = ssl.create_default_context()
    if port == 465:
        with smtplib.SMTP_SSL(host, port, context=kontekst, timeout=30) as s:
            s.login(uzytkownik, os.environ["SMTP_PASSWORD"])
            s.send_message(msg)
    else:
        with smtplib.SMTP(host, port, timeout=30) as s:
            s.starttls(context=kontekst)
            s.login(uzytkownik, os.environ["SMTP_PASSWORD"])
            s.send_message(msg)


# --------------------------------------------------------------------------------------
# Brevo (kampania e-mail do listy danego województwa)
# --------------------------------------------------------------------------------------
def brevo_skonfigurowany() -> bool:
    return bool(os.environ.get("BREVO_API_KEY"))


def listy_brevo() -> dict[str, int]:
    try:
        return {kk: int(v) for kk, v in json.loads(os.environ.get("BREVO_LISTY", "{}")).items()}
    except (ValueError, AttributeError):
        return {}


def utworz_kampanie_brevo(temat: str, html_tresc: str, lista_id: int, nazwa: str,
                          wyslij: bool = False, sesja: requests.Session | None = None) -> dict:
    """POST /v3/emailCampaigns (+ /sendNow przy wyslij=True). Zwraca odpowiedź API."""
    s = sesja or requests.Session()
    naglowki = {"api-key": os.environ["BREVO_API_KEY"], "accept": "application/json",
                "content-type": "application/json"}
    tresc = {
        "name": nazwa,
        "subject": temat,
        "sender": {"name": os.environ.get("BREVO_NADAWCA_NAZWA", "Alerty naborów"),
                   "email": os.environ["BREVO_NADAWCA_EMAIL"]},
        "type": "classic",
        "htmlContent": html_tresc,
        "recipients": {"listIds": [lista_id]},
        "previewText": "Termin, kwota i link do ogłoszenia. Co przygotować i jak zdążyć.",
    }
    r = s.post(f"{BREVO_API}/emailCampaigns", headers=naglowki, json=tresc, timeout=30)
    r.raise_for_status()
    wynik = r.json()
    if wyslij and "id" in wynik:
        r2 = s.post(f"{BREVO_API}/emailCampaigns/{wynik['id']}/sendNow", headers=naglowki, timeout=30)
        r2.raise_for_status()
        wynik["wyslano"] = True
    return wynik


def wyslij_alerty(wpisy: list[Wpis], dzis: date) -> list[str]:
    """Wysyłka według dostępnej konfiguracji. Zwraca log czynności (bez sekretów)."""
    log: list[str] = []
    grupy = grupuj_po_wojewodztwie(wpisy)
    if not grupy:
        return ["brak naborów do wysłania"]
    if smtp_skonfigurowany():
        for woj, lista in grupy.items():
            wyslij_smtp(f"[do weryfikacji] {temat_emaila(lista, woj)}", html_alertu(lista, woj, dzis),
                        tekst_alertu(lista, woj, dzis))
            log.append(f"SMTP: wysłano do właściciela ({woj}, {len(lista)} nab.)")
    if brevo_skonfigurowany():
        listy = listy_brevo()
        wyslij = os.environ.get("BREVO_WYSYLAJ") == "1"
        for woj, lista in grupy.items():
            if woj not in listy:
                log.append(f"Brevo: brak listy dla województwa {woj} w BREVO_LISTY, pominięto")
                continue
            wynik = utworz_kampanie_brevo(temat_emaila(lista, woj), html_alertu(lista, woj, dzis), listy[woj],
                                          nazwa=f"Alert {dzis.isoformat()} {woj}", wyslij=wyslij)
            log.append(f"Brevo: kampania {wynik.get('id')} ({woj}) {'wysłana' if wyslij else 'utworzona jako szkic'}")
    if not log:
        log.append("brak konfiguracji SMTP_* ani BREVO_API_KEY: tylko eksport plików")
    return log
