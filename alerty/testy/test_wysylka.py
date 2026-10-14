"""Eksport pod mailing i wysyłka Brevo (na sztucznej sesji, bez sieci i bez sekretów)."""

import csv
import json
from datetime import date

from monitor.klasyfikator import klasyfikuj
from monitor.model import Wpis
from monitor.wysylka import eksport_csv, eksport_json, eksport_kampanii, utworz_kampanie_brevo, wyslij_alerty

DZIS = date(2026, 10, 14)


def nabor():
    return klasyfikuj(Wpis(zrodlo="pup", tytul="Nabór wniosków o dofinansowanie podjęcia działalności gospodarczej",
                           url="https://legnica.praca.gov.pl/rynek-pracy/aktualnosci/-/a/content/n?p_r_p_assetEntryId=5",
                           data_publikacji="2026-10-09", pup_id="legnica", pup_nazwa="Powiatowy Urząd Pracy w Legnicy",
                           wojewodztwo="dolnośląskie", tresc="Nabór od 19.10.2026 do 28.10.2026. Kwota dotacji: do 40 000 zł."))


def test_eksport_csv_json_html(tmp_path):
    w = [nabor()]
    plik = eksport_csv(w, tmp_path / "n.csv", DZIS)
    with open(plik, encoding="utf-8-sig") as f:
        wiersze = list(csv.DictReader(f, delimiter=";"))
    assert wiersze[0]["pup_id"] == "legnica" and wiersze[0]["nabor_do"] == "2026-10-28"
    assert wiersze[0]["dni_do_konca"] == "14" and "utm_source=alert" in wiersze[0]["link_cta"]
    dane = json.loads(eksport_json(w, tmp_path / "n.json", DZIS).read_text(encoding="utf-8"))
    assert dane["liczba"] == 1 and dane["nabory"][0]["kwota_max_zl"] == 40000
    pliki = eksport_kampanii(w, tmp_path / "kampanie", DZIS)
    assert {p.suffix for p in pliki} == {".html", ".txt", ".json"}
    assert any(p.name == "alert-2026-10-14-dolnoslaskie.html" for p in pliki)


class FakeSesja:
    def __init__(self):
        self.posty = []

    def post(self, url, headers=None, json=None, timeout=None):
        self.posty.append((url, headers, json))

        class R:
            def raise_for_status(self_inner):
                pass

            def json(self_inner):
                return {"id": 77}

        return R()


def test_brevo_szkic(monkeypatch):
    monkeypatch.setenv("BREVO_API_KEY", "test-klucz")
    monkeypatch.setenv("BREVO_NADAWCA_EMAIL", "alerty@example.pl")
    s = FakeSesja()
    wynik = utworz_kampanie_brevo("Temat", "<p>x</p>", 12, "Alert test", wyslij=False, sesja=s)
    assert wynik["id"] == 77 and len(s.posty) == 1
    url, naglowki, tresc = s.posty[0]
    assert url == "https://api.brevo.com/v3/emailCampaigns"
    assert naglowki["api-key"] == "test-klucz"
    assert tresc["recipients"] == {"listIds": [12]} and tresc["sender"]["email"] == "alerty@example.pl"
    utworz_kampanie_brevo("Temat", "<p>x</p>", 12, "Alert test", wyslij=True, sesja=s)
    assert s.posty[-1][0].endswith("/emailCampaigns/77/sendNow")


def test_bez_konfiguracji_tylko_eksport(monkeypatch):
    for z in ("BREVO_API_KEY", "SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "ALERTY_EMAIL_WLASCICIELA"):
        monkeypatch.delenv(z, raising=False)
    assert wyslij_alerty([nabor()], DZIS) == ["brak konfiguracji SMTP_* ani BREVO_API_KEY: tylko eksport plików"]
