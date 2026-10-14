"""Parsery źródeł na zapisanych prawdziwych stronach (fixtures/, pobrane 14.10.2026)."""

import json

from monitor.model import Pup
from monitor.zrodla import (
    IndeksPup,
    id_ogloszenia_praca_gov,
    klucz_nazwy,
    link_do_strony,
    parsuj_liste_aktualnosci,
    parsuj_szczegoly,
    parsuj_zielona_linia,
)

TUCHOLA = Pup("tuchola", "Powiatowy Urząd Pracy w Tucholi", "kujawsko-pomorskie", "https://tuchola.praca.gov.pl", "Tuchola", "2026-10-14")
LEGNICA = Pup("legnica", "Powiatowy Urząd Pracy w Legnicy", "dolnośląskie", "https://legnica.praca.gov.pl", "Legnica", "2026-10-14")
GORZOW = Pup("gorzow", "Powiatowy Urząd Pracy w Gorzowie Wielkopolskim", "lubuskie", "https://gorzow.praca.gov.pl", "Gorzów Wielkopolski", "2026-10-14")


def test_lista_aktualnosci_tuchola(fixture_tekst):
    wpisy = parsuj_liste_aktualnosci(fixture_tekst("pup-tuchola-aktualnosci.html"), TUCHOLA)
    assert len(wpisy) == 10
    nabor = wpisy[1]
    assert nabor.tytul == "Nabór wniosków o dofinansowanie podjęcia działalności gospodarczej"
    assert nabor.data_publikacji == "2026-10-08"
    assert nabor.url.startswith("https://tuchola.praca.gov.pl/rynek-pracy/aktualnosci/-/asset_publisher/")
    assert "p_r_p_assetEntryId=69834237" in nabor.url
    assert nabor.tresc.startswith("Dyrektor Powiatowego Urzędu Pracy w Tucholi")
    assert nabor.pup_id == "tuchola" and nabor.wojewodztwo == "kujawsko-pomorskie"


def test_wspolny_szablon_kilku_urzedow(fixture_tekst):
    # ten sam parser działa dla różnych urzędów (wspólny szablon praca.gov.pl)
    for plik, pup, oczekiwany in [
        ("pup-legnica-aktualnosci.html", LEGNICA, "NABÓR WNIOSKÓW O DOFINANSOWANIE PODJĘCIA DZIAŁALNOŚCI GOSPODARCZEJ"),
        ("pup-gorzow-aktualnosci.html", GORZOW, "Nabór wniosków o przyznanie środków na podjęcie działalności gospodarczej"),
        ("pup-zory-aktualnosci.html", Pup("zory", "PUP w Żorach", "śląskie", "https://zory.praca.gov.pl"), "Nabór wniosków na dotacje"),
        ("pup-katowice-aktualnosci.html", Pup("katowice", "PUP w Katowicach", "śląskie", "https://katowice.praca.gov.pl"), "Nabór wniosków o refundację"),
    ]:
        wpisy = parsuj_liste_aktualnosci(fixture_tekst(plik), pup)
        assert len(wpisy) >= 10, plik
        assert all(w.data_publikacji.startswith("2026-") for w in wpisy), plik
        assert all(w.url.startswith(pup.url) for w in wpisy), plik
        assert any(w.tytul.startswith(oczekiwany) for w in wpisy), plik


def test_stronicowanie(fixture_tekst):
    url = link_do_strony(fixture_tekst("pup-tuchola-aktualnosci.html"), 2)
    assert url and url.endswith("_cur=2")


def test_szczegoly_ogloszenia(fixture_tekst):
    tytul, tresc = parsuj_szczegoly(fixture_tekst("pup-tuchola-ogloszenie.html"))
    assert tytul == "Nabór wniosków o dofinansowanie podjęcia działalności gospodarczej"
    assert "jednorazowo środków na podjęcie działalności gospodarczej" in tresc
    assert "19.10.2026" in tresc


def test_zielona_linia_api(fixture_tekst):
    dane = json.loads(fixture_tekst("zielonalinia-posts-2026-10.json"))
    indeks = IndeksPup([TUCHOLA, LEGNICA, GORZOW])
    wpisy = parsuj_zielona_linia(dane, indeks)
    assert len(wpisy) == 40
    tuchola = next(w for w in wpisy if "Tuchola" in w.tytul)
    assert tuchola.tytul == "PUP Tuchola – Nabór wniosków o dofinansowanie podjęcia działalności gospodarczej"
    assert tuchola.data_publikacji == "2026-10-14"
    assert tuchola.pup_id == "tuchola"  # po linku do strony urzędu
    assert tuchola.url_urzedu.startswith("https://tuchola.praca.gov.pl/")
    assert "od 19.10.2026 r. do 20.10.2026 r." in tuchola.tresc
    gorzow = next(w for w in wpisy if "Gorzów" in w.tytul)
    assert gorzow.pup_id == "gorzow" and gorzow.wojewodztwo == "lubuskie"


def test_identyfikator_ogloszenia_ten_sam_dla_roznych_adresow():
    z_listy = ("https://tuchola.praca.gov.pl/rynek-pracy/aktualnosci/-/asset_publisher/8VCc6CLiHUaO/content/"
               "nabor-wnioskow-o-dofinansowanie-podjecia-dzialalnosci-gospodarczej-1?p_r_p_assetEntryId=69834237")
    z_zielonej_linii = ("https://tuchola.praca.gov.pl/strona-glowna/-/asset_publisher/Qat7ebECUfDp/content/"
                        "nabor-wnioskow-o-dofinansowanie-podjecia-dzialalnosci-gospodarczej-1?p_r_p_assetEntryId=69834237")
    assert id_ogloszenia_praca_gov(z_listy) == id_ogloszenia_praca_gov(z_zielonej_linii) == "tuchola.praca.gov.pl#69834237"
    assert id_ogloszenia_praca_gov("https://zielonalinia.gov.pl/x/") is None


def test_indeks_po_nazwie():
    indeks = IndeksPup([TUCHOLA, GORZOW])
    assert indeks.po_nazwie("Gorzów Wielkopolski") is GORZOW
    assert indeks.po_nazwie("Tuchola") is TUCHOLA
    assert indeks.po_nazwie("Kraków") is None
    assert klucz_nazwy("Łódź-Wschód") == "lodzwschod"


def test_zielona_linia_stronicowanie_naglowek_malymi_literami(fixture_tekst):
    # HTTP/2 zwraca nagłówki małymi literami (x-wp-totalpages): stronicowanie musi działać
    from datetime import date

    from requests.structures import CaseInsensitiveDict

    from monitor.pobieranie import Odpowiedz
    from monitor.zrodla import pobierz_zielona_linia

    class K:
        strony = []

        def pobierz(self, url, params=None, uzyj_cache=True):
            self.strony.append(params["page"])
            return Odpowiedz(url, 200, fixture_tekst("zielonalinia-posts-2026-10.json"),
                             naglowki=CaseInsensitiveDict({"x-wp-totalpages": "2"}))

    k = K()
    wpisy, bledy = pobierz_zielona_linia(k, date(2026, 1, 1))
    assert k.strony == [1, 2] and len(wpisy) == 80 and bledy == []
