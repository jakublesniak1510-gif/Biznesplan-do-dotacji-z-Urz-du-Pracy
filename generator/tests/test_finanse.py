import pytest

from pup_gen import finanse
from pup_gen.schemat import Kwestionariusz

from conftest import kwestionariusz, surowy_kwestionariusz


def test_formatowanie_pl():
    assert finanse.liczba_pl(61190.5) == "61 191"          # ROUND_HALF_UP, nie bankierskie
    assert finanse.liczba_pl(1234567.891, 2) == "1 234 567,89"
    assert finanse.formatuj_ark("ark_zus_m12", 456.18) == "456,18 zł"
    assert finanse.formatuj_ark("ark_margines", 0.68309) == "68,3%"
    assert finanse.formatuj_ark("ark_materialy_pct", 0.12) == "12%"
    assert finanse.formatuj_ark("ark_prog_rent_szt", 32) == "32"
    assert finanse.formatuj_ark("ark_okres_zwrotu_mies", 7.353) == "7,4 mies."
    assert finanse.formatuj_ark("ark_min_saldo", -1500.4) == "-1 500 zł"


@pytest.mark.soffice
def test_arkusz_fryzjerki_zgodny_z_szablonem_08(tmp_path, regulamin):
    """Kwestionariusz fryzjerki ma te same dane co przykład w arkuszu – wyniki muszą się zgadzać."""
    w = finanse.policz(kwestionariusz(), regulamin, tmp_path)
    assert w.plik.exists()
    assert len(w.wartosci) >= 48
    assert all(v is not None for v in w.wartosci.values())
    for nazwa in ("ark_przychod_12m", "ark_koszty_12m", "ark_zysk_netto_12m", "ark_dotacja",
                  "ark_kosztorys_dotacja", "ark_prog_rent_zl", "ark_gotowka_m12", "ark_zdrowotna_12m"):
        assert w.wartosci[nazwa] > 0, nazwa
    assert w.ark["ark_przychod_12m"] == "87 415 zł"
    assert w.ark["ark_zysk_netto_12m"] == "42 429 zł"
    assert w.ark["ark_przychod_12m_pes"] == "61 191 zł"
    assert w.ark["ark_zus_m12"] == "456,18 zł"
    _, _, bledy = finanse.odczytaj(w.plik)
    assert bledy == 0
    k = list(w.kontrole.values())
    assert k[0] == "OK" and k[1] == "OK" and k[3] == "OK"
    assert not [o for o in w.ostrzezenia if o.poziom == "BLOKUJE"]
    assert len(w.tabele["kalkulacja_miesieczna"][0]) == 14
    assert w.tabele["kosztorys"][1][1] == "Fotel fryzjerski mobilny, składany"


@pytest.mark.soffice
def test_arkusz_vat_czynny_mechanik(tmp_path, regulamin):
    w = finanse.policz(kwestionariusz("mechanik-samochodowy"), regulamin, tmp_path)
    assert w.wartosci["ark_kosztorys_dotacja"] == pytest.approx(30000, abs=0.01)  # kwoty netto
    assert w.wartosci["ark_przychod_12m"] > 100000
    assert w.kontrole[list(w.kontrole)[7]] == "czynny VAT"


@pytest.mark.soffice
def test_ostrzezenia_ujemna_gotowka_i_limit_kategorii(tmp_path, regulamin):
    d = surowy_kwestionariusz()
    d["zakupy"] = [z for z in d["zakupy"] if not z["nazwa"].startswith(("Kasa", "Lampa", "Walizka"))]
    for z in d["zakupy"]:
        if z["kategoria"] == "towar":
            z["cena_brutto"] = 9000  # 34,6% dotacji przy limicie 30%
    d["prognoza"]["koszty_stale"]["czynsz"] = 6000
    d["wklad_wlasny"]["kwota"] = 0
    w = finanse.policz(Kwestionariusz.model_validate(d), regulamin, tmp_path)
    blokujace = " ".join(o.komunikat for o in w.ostrzezenia if o.poziom == "BLOKUJE")
    assert "Ujemna gotówka" in blokujace
    assert "limit kategorii" in blokujace


def test_wypelnienie_nie_niszczy_formul(tmp_path, regulamin):
    import openpyxl
    plik = tmp_path / "a.xlsx"
    finanse.wypelnij(kwestionariusz("firma-sprzatajaca"), regulamin, plik)
    wb = openpyxl.load_workbook(plik)
    assert str(wb["Kosztorys"]["G5"].value).startswith("=")
    assert str(wb["Prognoza"]["C26"].value).startswith("=")
    assert wb["Kosztorys"]["B5"].value == "Odkurzacz piorący profesjonalny"
    assert wb["Kosztorys"]["B34"].value == pytest.approx(0.30)
    assert wb["Zalozenia"]["B9"].value == "ryczałt"
    assert wb["Kosztorys"]["B18"].value is None  # pozycja 14 – pusto
