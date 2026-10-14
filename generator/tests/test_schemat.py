import copy
import json

import pytest
from pydantic import ValidationError

from pup_gen.schemat import (Kwestionariusz, MapaFormularza, dowod_poprawny, pesel_poprawny,
                             wczytaj_regulaminy)
from pup_gen import KATALOG_PRZYKLADOW

from conftest import PRZYKLADY, surowy_kwestionariusz

PESEL_TESTOWY = "44051401359"  # poprawna suma kontrolna (numer z dokumentacji, nie osoby)


@pytest.mark.parametrize("nazwa", PRZYKLADY)
def test_przyklady_sa_poprawne(nazwa):
    kw = Kwestionariusz.model_validate(surowy_kwestionariusz(nazwa))
    assert kw.suma_zakupow_z_dotacji() <= kw.kwota_wnioskowana
    assert 3 <= len(kw.konkurencja.konkurenci) <= 5


def test_sumy_kontrolne():
    assert pesel_poprawny(PESEL_TESTOWY)
    assert not pesel_poprawny("44051401358")
    assert dowod_poprawny("ABA", "300000")
    assert not dowod_poprawny("ABA", "400000")


def test_odrzuca_pesel_w_tekscie():
    d = surowy_kwestionariusz()
    d["pomysl"]["motywacja"] = f"Mój PESEL to {PESEL_TESTOWY}, proszę wpisać."
    with pytest.raises(ValidationError) as e:
        Kwestionariusz.model_validate(d)
    assert "PESEL" in str(e.value)
    assert "pomysl.motywacja" in str(e.value)


def test_odrzuca_pesel_bez_slowa_i_pole_pesel():
    d = surowy_kwestionariusz()
    d["notatka_wlasciciela"] = f"numer {PESEL_TESTOWY}"
    with pytest.raises(ValidationError, match="PESEL"):
        Kwestionariusz.model_validate(d)
    d = surowy_kwestionariusz()
    d["kontakt"]["pesel"] = "123"
    with pytest.raises(ValidationError, match="niedozwolonej nazwie"):
        Kwestionariusz.model_validate(d)


def test_odrzuca_numer_dowodu():
    d = surowy_kwestionariusz()
    d["notatka_wlasciciela"] = "dowód ABA 300000"
    with pytest.raises(ValidationError, match="dowodu"):
        Kwestionariusz.model_validate(d)


def test_nie_myli_identyfikatora_oferty_z_peselem():
    d = surowy_kwestionariusz()
    d["zakupy"][0]["link"] = f"https://allegro.pl/oferta/fotel-{PESEL_TESTOWY}"
    Kwestionariusz.model_validate(d)


def test_cena_musi_byc_dodatnia():
    d = surowy_kwestionariusz()
    d["zakupy"][0]["cena_brutto"] = 0
    with pytest.raises(ValidationError, match="cena_brutto"):
        Kwestionariusz.model_validate(d)
    d = surowy_kwestionariusz()
    d["uslugi"][0]["cena"] = -5
    with pytest.raises(ValidationError):
        Kwestionariusz.model_validate(d)


def test_suma_zakupow_nie_moze_przekroczyc_dotacji():
    d = surowy_kwestionariusz()
    d["kwota_wnioskowana"] = 20000
    with pytest.raises(ValidationError, match="przekraczają kwotę wnioskowaną"):
        Kwestionariusz.model_validate(d)


def test_kwota_nie_wieksza_niz_maksimum_naboru():
    d = surowy_kwestionariusz()
    d["nabor"]["kwota_max_zl"] = 25000
    with pytest.raises(ValidationError, match="maksimum naboru"):
        Kwestionariusz.model_validate(d)


def test_dane_do_promptu_bez_kontaktu_i_zabezpieczenia(kw):
    tekst = json.dumps(kw.dane_do_promptu(), ensure_ascii=False)
    assert kw.kontakt.email not in tekst and "600 100 200" not in tekst
    assert "szwagierka" not in tekst  # zabezpieczenie
    assert "https://" not in tekst     # linki do ofert i naboru
    assert '"imie": "Anna"' in tekst and "K10_zakupy_i_zasoby" in tekst


def test_kwota_do_rozliczenia_netto_i_brutto(kw):
    myjka = kw.zakupy[1]
    assert myjka.cena_netto == 1200.0
    assert myjka.kwota_do_rozliczenia(vat_czynny=False) == 1476.0
    assert myjka.kwota_do_rozliczenia(vat_czynny=True) == 1200.0


def test_regulaminy_z_csv():
    regs = wczytaj_regulaminy(KATALOG_PRZYKLADOW / "regulaminy-przyklad.csv")
    z = regs["zielonow"]
    assert z.limit_reklama_pct == 20 and z.limit_samochod_pct == 0
    assert "lombard" in z.wykluczenia_dzialalnosci
    assert regs["lipno-przyklad"].limit_remont_pct is None


def test_mapa_waliduje_sekcje_i_podzial():
    baza = {"pup": "X", "formularz": "Y", "pola": [{"id": "1", "nazwa_w_formularzu": "A", "sekcje": ["03", "04"],
                                                     "podzial_limitu": {"03": 0.5, "04": 0.4}}]}
    with pytest.raises(ValidationError, match="podzial_limitu"):
        MapaFormularza.model_validate(baza)
    zla = copy.deepcopy(baza)
    zla["pola"][0] = {"id": "1", "nazwa_w_formularzu": "A", "sekcje": ["12"]}
    with pytest.raises(ValidationError, match="nieznane sekcje"):
        MapaFormularza.model_validate(zla)
    ok = {"pup": "X", "formularz": "Y", "pola": [{"id": "1", "nazwa_w_formularzu": "A", "sekcja": "tabela:kosztorys"}]}
    assert MapaFormularza.model_validate(ok).pola[0].tabele == ["kosztorys"]


@pytest.mark.parametrize("plik,liczba", [("mapa-krotka-6-pol", 6), ("mapa-dluga-14-pol", 14)])
def test_przykladowe_mapy(plik, liczba):
    m = MapaFormularza.model_validate_json((KATALOG_PRZYKLADOW / f"{plik}.json").read_text(encoding="utf-8"))
    assert len(m.pola) == liczba
    if liczba == 6:
        assert all(p.limit_znakow for p in m.pola)


def test_baza_regulaminow_repozytorium_wczytuje_sie():
    from pup_gen import PLIK_BAZY_PUP
    if not PLIK_BAZY_PUP.exists():
        pytest.skip("brak baza-pup/regulaminy-pup-2026.csv")
    regs = wczytaj_regulaminy(PLIK_BAZY_PUP)
    assert regs and all(r.pup_id and r.nazwa_pup for r in regs.values())


def test_bledny_wiersz_regulaminu_pominiety(tmp_path):
    plik = tmp_path / "r.csv"
    plik.write_text("pup_id;nazwa_pup;kwota_max_zl\nok;PUP OK;30000\nzly;PUP zły;trzydzieści\n", encoding="utf-8")
    assert list(wczytaj_regulaminy(plik)) == ["ok"]
