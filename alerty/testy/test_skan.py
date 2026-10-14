"""Pełny przebieg skanu na fixture'ach (bez sieci): Zielona Linia + 2 urzędy, dedup między źródłami."""

import json
from datetime import date

from monitor.klasyfikator import DOTACJA
from monitor.model import Pup
from monitor.pobieranie import Odpowiedz
from monitor.skan import skanuj
from monitor.stan import Stan
from monitor.zrodla import IndeksPup

DZIS = date(2026, 10, 14)
TUCHOLA = Pup("tuchola", "Powiatowy Urząd Pracy w Tucholi", "kujawsko-pomorskie", "https://tuchola.praca.gov.pl", "Tuchola", "2026-10-14")
LEGNICA = Pup("legnica", "Powiatowy Urząd Pracy w Legnicy", "dolnośląskie", "https://legnica.praca.gov.pl", "Legnica", "2026-10-14")


class FakeKlient:
    def __init__(self, fixture_tekst):
        self.f = fixture_tekst
        self.statystyki = {"zapytania": 0, "niezmienione": 0, "bledy": 0, "zablokowane_robots": 0}
        self.urle = []

    def pobierz(self, url, params=None, uzyj_cache=True):
        self.urle.append(url)
        self.statystyki["zapytania"] += 1
        if "zielonalinia.gov.pl/wp-json" in url:
            return Odpowiedz(url, 200, self.f("zielonalinia-posts-2026-10.json"), naglowki={"X-WP-TotalPages": "1"})
        if url == "https://tuchola.praca.gov.pl/rynek-pracy/aktualnosci":
            return Odpowiedz(url, 200, self.f("pup-tuchola-aktualnosci.html"))
        if url == "https://legnica.praca.gov.pl/rynek-pracy/aktualnosci":
            return Odpowiedz(url, 200, self.f("pup-legnica-aktualnosci.html"))
        if "tuchola.praca.gov.pl" in url and "assetEntryId=69834237" in url:
            return Odpowiedz(url, 200, self.f("pup-tuchola-ogloszenie.html"))
        return Odpowiedz(url, 404, None, blad="HTTP 404")

    def zapisz_cache(self):
        pass


def test_skan_end_to_end(fixture_tekst):
    stan = Stan()
    klient = FakeKlient(fixture_tekst)
    wynik = skanuj(stan, [TUCHOLA, LEGNICA], IndeksPup([TUCHOLA, LEGNICA]), DZIS, klient=klient,
                   zl_od=date(2026, 9, 1))
    assert wynik.statystyki["zielonalinia_wpisy"] == 40
    assert wynik.statystyki["pup_ok"] == 2
    tuchola = [w for w in stan.wpisy.values() if w.pup_id == "tuchola" and w.kategoria == DOTACJA]
    # ogłoszenie urzędu i wpis Zielonej Linii to jeden nabór
    assert len(tuchola) == 1
    t = tuchola[0]
    assert t.zrodla == ["pup", "zielonalinia"]
    assert (t.nabor_od, t.nabor_do) == ("2026-10-19", "2026-10-20")
    assert any(w.pup_id == "tuchola" for w in wynik.nowe_do_alertu)
    # drugi skan: nic nowego
    wynik2 = skanuj(stan, [TUCHOLA, LEGNICA], IndeksPup([TUCHOLA, LEGNICA]), DZIS, klient=FakeKlient(fixture_tekst),
                    zl_od=date(2026, 9, 1))
    assert wynik2.nowe == []
    json.dumps(stan.dane, ensure_ascii=False)  # stan da się zapisać
