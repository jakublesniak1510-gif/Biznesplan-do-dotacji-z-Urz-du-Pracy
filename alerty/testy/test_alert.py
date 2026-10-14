"""Treść alertu e-mail (HTML i tekst), grupowanie po województwie, treść Issue."""

from datetime import date
from urllib.parse import parse_qs, urlsplit

from monitor.alert import (
    do_alertu,
    grupuj_po_wojewodztwie,
    html_alertu,
    markdown_issue,
    tekst_alertu,
    temat_emaila,
    url_cta,
)
from monitor.klasyfikator import klasyfikuj
from monitor.model import Wpis

DZIS = date(2026, 10, 14)


def nabor(pup_id, nazwa, woj, od, do, kwota_txt="", tytul="Nabór wniosków o dofinansowanie podjęcia działalności gospodarczej"):
    w = Wpis(zrodlo="pup", tytul=tytul, url=f"https://{pup_id}.praca.gov.pl/rynek-pracy/aktualnosci/-/x/content/n?p_r_p_assetEntryId=1",
             data_publikacji="2026-10-13", pup_id=pup_id, pup_nazwa=nazwa, wojewodztwo=woj,
             tresc=f"Nabór prowadzony będzie od {od} do {do}. {kwota_txt}")
    return klasyfikuj(w)


def przyklady():
    return [
        nabor("legnica", "Powiatowy Urząd Pracy w Legnicy", "dolnośląskie", "19.10.2026", "28.10.2026",
              "Maksymalna kwota dofinansowania wynosi 40 000,00 zł ze środków Funduszu Pracy."),
        nabor("tuchola", "Powiatowy Urząd Pracy w Tucholi", "kujawsko-pomorskie", "12.10.2026", "16.10.2026"),
        nabor("jawor", "Powiatowy Urząd Pracy w Jaworze", "dolnośląskie", "01.10.2026", "02.10.2026"),  # zakończony
    ]


def test_wybor_i_grupowanie():
    aktywne = do_alertu(przyklady(), DZIS)
    assert [w.pup_id for w in aktywne] == ["legnica", "tuchola"]
    grupy = grupuj_po_wojewodztwie(aktywne)
    assert list(grupy) == ["dolnośląskie", "kujawsko-pomorskie"]


def test_url_cta_utm():
    w = przyklady()[0]
    q = parse_qs(urlsplit(url_cta(w, DZIS, "https://example.pl/zamow")).query)
    assert q["utm_source"] == ["alert"] and q["utm_medium"] == ["email"]
    assert q["utm_campaign"] == ["legnica"] and q["utm_content"] == ["2026-10-14"]


def test_tresc_html_i_tekst():
    legnica, tuchola, _ = przyklady()
    html = html_alertu([legnica], "dolnośląskie", DZIS)
    tekst = tekst_alertu([legnica], "dolnośląskie", DZIS)
    for tresc in (html, tekst):
        assert "Powiatowy Urząd Pracy w Legnicy" in tresc
        assert "19.10.2026 – 28.10.2026" in tresc
        assert "start za 5 dni" in tresc
        assert "do 40 000 zł" in tresc
        assert "https://legnica.praca.gov.pl/" in tresc
        assert "utm_source=alert" in tresc
        assert "Wypisz się" in tresc or "Wypisz" in tresc
        assert "Nie gwarantujemy przyznania dotacji" in tresc
    assert html.startswith("<!doctype html>") and 'lang="pl"' in html
    tekst_t = tekst_alertu([tuchola], "kujawsko-pomorskie", DZIS)
    assert "zostały 2 dni" in tekst_t


def test_temat():
    legnica, tuchola, _ = przyklady()
    assert temat_emaila([legnica], "dolnośląskie") == (
        "Nabór na dotację na firmę – PUP w Legnicy, do 40 000 zł, wnioski 19.10.2026 – 28.10.2026")
    assert temat_emaila([legnica, tuchola], "x") == "2 nabory na dotacje na firmę – woj. x"
    assert temat_emaila([legnica] * 5, "x") == "5 naborów na dotacje na firmę – woj. x"


def test_issue_markdown():
    md = markdown_issue(do_alertu(przyklady(), DZIS), DZIS)
    assert "### dolnośląskie" in md and "### kujawsko-pomorskie" in md
    assert "| Powiatowy Urząd Pracy w Tucholi |" in md
    assert markdown_issue([], DZIS) == ""
