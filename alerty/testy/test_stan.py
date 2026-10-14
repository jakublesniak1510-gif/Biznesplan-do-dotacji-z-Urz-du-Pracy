"""Deduplikacja, znane wpisy i „nowe od ostatniego uruchomienia”."""

from datetime import date

from monitor.klasyfikator import klasyfikuj
from monitor.model import Wpis
from monitor.stan import Stan, klucz_wpisu

URL_PUP = ("https://tuchola.praca.gov.pl/rynek-pracy/aktualnosci/-/asset_publisher/8VCc6CLiHUaO/content/"
           "nabor-wnioskow-o-dofinansowanie-podjecia-dzialalnosci-gospodarczej-1?p_r_p_assetEntryId=69834237")
URL_PUP_INNY = URL_PUP.replace("rynek-pracy/aktualnosci", "strona-glowna").replace("8VCc6CLiHUaO", "Qat7ebECUfDp")


def wpis_pup(**kw) -> Wpis:
    d = dict(zrodlo="pup", tytul="Nabór wniosków o dofinansowanie podjęcia działalności gospodarczej", url=URL_PUP,
             data_publikacji="2026-10-08", pup_id="tuchola", pup_nazwa="Powiatowy Urząd Pracy w Tucholi",
             wojewodztwo="kujawsko-pomorskie", tresc="Dyrektor PUP w Tucholi zaprasza…")
    d.update(kw)
    return klasyfikuj(Wpis(**d))


def wpis_zl(**kw) -> Wpis:
    d = dict(zrodlo="zielonalinia",
             tytul="PUP Tuchola – Nabór wniosków o dofinansowanie podjęcia działalności gospodarczej",
             url="https://zielonalinia.gov.pl/pup-tuchola-nabor-wnioskow-o-dofinansowanie-podjecia-dzialalnosci-gospodarczej/",
             data_publikacji="2026-10-14", pup_id="tuchola", wojewodztwo="kujawsko-pomorskie",
             tresc="Wnioski przyjmowane będą w terminie od 19.10.2026 r. do 20.10.2026 r.", url_urzedu=URL_PUP_INNY)
    d.update(kw)
    return klasyfikuj(Wpis(**d))


def test_nowe_tylko_raz():
    stan = Stan()
    assert len(stan.aktualizuj([wpis_pup()], "2026-10-14T07:10:00+02:00")) == 1
    assert stan.aktualizuj([wpis_pup()], "2026-10-14T15:10:00+02:00") == []
    w = next(iter(stan.wpisy.values()))
    assert w.pierwszy_raz.startswith("2026-10-14T07:10") and w.ostatni_raz.startswith("2026-10-14T15:10")


def test_ten_sam_artykul_pod_dwoma_adresami():
    stan = Stan()
    stan.aktualizuj([wpis_pup()])
    assert stan.aktualizuj([wpis_pup(url=URL_PUP_INNY)]) == []
    assert len(stan.wpisy) == 1


def test_zielona_linia_scalana_z_ogloszeniem_urzedu():
    stan = Stan()
    stan.aktualizuj([wpis_pup()])
    nowe = stan.aktualizuj([wpis_zl()])
    assert nowe == []
    (w,) = stan.wpisy.values()
    assert w.zrodla == ["pup", "zielonalinia"]
    # daty z Zielonej Linii uzupełniają wpis z listy PUP
    assert (w.nabor_od, w.nabor_do) == ("2026-10-19", "2026-10-20")
    assert klucz_wpisu(wpis_zl()) == "tuchola.praca.gov.pl#69834237"


def test_deduplikacja_przyblizona_po_tytule():
    # wpis ZL bez linku do urzędu: ten sam PUP, ten sam tytuł, publikacja 3 dni później
    stan = Stan()
    stan.aktualizuj([wpis_pup(data_publikacji="2026-10-11")])
    assert stan.aktualizuj([wpis_zl(url_urzedu="")]) == []
    # ten sam tytuł po 2 miesiącach to nowy nabór
    assert len(stan.aktualizuj([wpis_zl(url_urzedu="", data_publikacji="2026-12-14",
                                         url="https://zielonalinia.gov.pl/pup-tuchola-nabor-2/",
                                         tresc="Wnioski przyjmowane będą od 4.01.2027 r. do 8.01.2027 r.")])) == 1


def test_zapis_i_odczyt(tmp_path):
    sciezka = tmp_path / "stan.json"
    stan = Stan(sciezka=sciezka)
    stan.aktualizuj([wpis_pup(), wpis_zl(url_urzedu="", tytul="PUP Tuchola – Targi pracy", url="https://zielonalinia.gov.pl/targi/")])
    stan.dane["ostatni_skan"] = "2026-10-14T07:10:00+02:00"
    stan.zapisz()
    ponownie = Stan.wczytaj(sciezka)
    assert set(ponownie.wpisy) == set(stan.wpisy)
    assert ponownie.dane["ostatni_skan"] == "2026-10-14T07:10:00+02:00"
    assert ponownie.aktualizuj([wpis_pup()]) == []
    assert len(ponownie.nabory()) == 1


def test_przycinanie_starych_wpisow():
    stan = Stan()
    stan.aktualizuj([wpis_zl(url_urzedu="", tytul="PUP Tuchola – Targi pracy", url="https://zielonalinia.gov.pl/t/")],
                    "2024-01-01T07:00:00+01:00")
    stan.aktualizuj([wpis_pup()], "2026-10-14T07:00:00+02:00")
    assert stan.przytnij(date(2026, 10, 14)) == 1
    assert len(stan.wpisy) == 1


def test_wstrzymanie_zamyka_nabor_do_wyczerpania():
    stan = Stan()
    otwarty = wpis_pup(pup_id="wroclaw", url="https://wroclaw.praca.gov.pl/x/-/a/content/n?p_r_p_assetEntryId=1",
                       data_publikacji="2026-09-01", tresc="Nabór prowadzony od 2.09.2026 r. do wyczerpania środków.")
    stan.aktualizuj([otwarty])
    w = stan.wpisy[klucz_wpisu(otwarty)]
    from monitor.klasyfikator import status
    assert status(w, date(2026, 9, 20)) == "trwa (do wyczerpania środków)"
    wstrzymanie = wpis_pup(pup_id="wroclaw", url="https://wroclaw.praca.gov.pl/x/-/a/content/w?p_r_p_assetEntryId=2",
                           data_publikacji="2026-09-25",
                           tytul="Wstrzymanie naboru wniosków o dofinansowanie podjęcia działalności gospodarczej",
                           tresc="Powiatowy Urząd Pracy we Wrocławiu informuje, że z dniem 26.09.2026r. wstrzymuje nabór wniosków.")
    stan.aktualizuj([wstrzymanie])
    assert w.wstrzymany == "2026-09-26"
    assert status(w, date(2026, 9, 25)) == "trwa (do wyczerpania środków)"
    assert status(w, date(2026, 9, 27)) == "zakończony"


def test_deduplikacja_po_datach_naboru():
    # PUP Turek: inny tytuł na stronie urzędu i w Zielonej Linii, link ZL tylko do strony głównej
    stan = Stan()
    z_pup = wpis_pup(pup_id="turek", url="https://turek.praca.gov.pl/x/-/a/content/d?p_r_p_assetEntryId=69660107",
                     tytul="DOFINANSOWANIE NA PODJĘCIE DZIAŁALNOŚCI GOSPODARCZEJ DLA OSÓB DO 30 roku życia",
                     data_publikacji="2026-10-02", tresc="Nabór w dniach 15-19 października 2026 r.")
    z_zl = wpis_zl(pup_id="turek", url_urzedu="http://turek.praca.gov.pl", data_publikacji="2026-10-12",
                   tytul="PUP Turek – Nabór wniosków w ramach dofinansowania na podjęcie działalności gospodarczej dla osób do 30 r.ż.",
                   url="https://zielonalinia.gov.pl/pup-turek-nabor/", tresc="Kiedy? W dniach 15-19 października 2026 r.")
    stan.aktualizuj([z_pup])
    assert stan.aktualizuj([z_zl]) == []
    assert len(stan.wpisy) == 1
