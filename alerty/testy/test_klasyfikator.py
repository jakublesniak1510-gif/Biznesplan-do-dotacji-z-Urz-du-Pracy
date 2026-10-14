"""Klasyfikator na prawdziwych tytułach i fragmentach ogłoszeń (Zielona Linia i strony PUP, 2026)."""

from datetime import date

import pytest

from monitor.klasyfikator import (
    DOTACJA,
    DOTACJA_PFRON,
    INNE,
    INNE_FORMY,
    SPOTKANIE,
    ZAKONCZENIE,
    ZAPOWIEDZ,
    klasyfikuj,
    klasyfikuj_tekst,
    opis_terminu,
    rozbij_tytul_zl,
    status,
    wyciagnij_daty,
    wyciagnij_grupy,
    wyciagnij_kwote,
    wyciagnij_liczbe_miejsc,
    wyciagnij_zrodla,
)
from monitor.model import Wpis

# 20 prawdziwych tytułów (pobrane 14.10.2026 z zielonalinia.gov.pl i *.praca.gov.pl)
PRAWDZIWE_TYTULY = [
    ("PUP Tuchola – Nabór wniosków o dofinansowanie podjęcia działalności gospodarczej", DOTACJA),
    ("PUP Gorzów Wielkopolski – Nabór wniosków o przyznanie środków na podjęcie działalności gospodarczej dla osób do 30 r.ż.", DOTACJA),
    ("PUP Żory – Nabór wniosków na dotacje na rozpoczęcie działalności gospodarczej", DOTACJA),
    ("PUP Strzelin – Nabór wniosków na jednorazowe środki na podjęcie działalności gospodarczej", DOTACJA),
    ("PUP Zawiercie – Własny biznes z EFS+ nabór wniosków", DOTACJA),
    ("PUP Inowrocław – 30 tysięcy złotych na otwarcie firmy – nabór wniosków", DOTACJA),
    ("PUP Oświęcim – II Nabór wniosków na działalność gospodarczą", DOTACJA),
    ("NABÓR WNIOSKÓW O DOFINANSOWANIE PODJĘCIA DZIAŁALNOŚCI GOSPODARCZEJ", DOTACJA),
    ("PUP Sanok – Nabór wniosków o dofinansowanie podjęcia działalności gospodarczej i prac interwencyjnych", DOTACJA),
    ("PUP Myszków – II nabór wniosków – dotacja na podjęcie działalności gospodarczej – PFRON", DOTACJA_PFRON),
    ("NABÓR WNIOSKÓW O PRZYZNANIE ŚRODKÓW PFRON NA ROZPOCZĘCIE DZIAŁALNOŚCI GOSPODARCZEJ (POWIAT GRODZKI)", DOTACJA_PFRON),
    ("PUP Golub-Dobrzyń – Spotkanie informacyjne dla osób planujących rozpocząć działalność gospodarczą", SPOTKANIE),
    ("PUP Wągrowiec – Webinarium „Wsparcie finansowe na rozpoczęcie i rozwój działalności gospodarczej”", SPOTKANIE),
    ("PUP Parczew – Nabór wniosków na organizację staży", INNE_FORMY),
    ("PUP Opole Lubelskie – Nabór wniosków o przyznanie bonu na zasiedlenie", INNE_FORMY),
    ("Nabór wniosków o refundację kosztów wyposażenia lub doposażenia stanowiska pracy", INNE_FORMY),
    ("PUP Zamość – Nabór wniosków o dofinansowanie kształcenia ustawicznego ze środków KFS", INNE_FORMY),
    ("PUP Działdowo – Nabór wniosków o skierowanie na wybrane szkolenie przez osobę bezrobotną niezbędne do "
     "podjęcia pracy lub rozpoczęcia działalności gospodarczej", INNE_FORMY),
    ("PUP Krapkowice – Rozpoczęcie naboru do programu „Pierwszy biznes – Wsparcie w starcie”", INNE_FORMY),
    ("PUP Bydgoszcz – IV Kujawsko-Pomorskie Targi Pracy", INNE),
]


@pytest.mark.parametrize("tytul,oczekiwana", PRAWDZIWE_TYTULY)
def test_kategoria_prawdziwych_tytulow(tytul, oczekiwana):
    assert klasyfikuj_tekst(tytul)[0] == oczekiwana


def test_dwadziescia_tytulow():
    assert len(PRAWDZIWE_TYTULY) == 20


def test_tytul_ogolny_rozstrzyga_tresc():
    # PUP Olecko: ogólny tytuł, a w treści nabór na staż → nie alarmujemy
    tytul = "PUP Olecko – Środki z Funduszu Pracy – zaproszenie do składania wniosków"
    tresc = ("Powiatowy Urząd Pracy w Olecku informuje o możliwości złożenia wniosków na staż. Nabór wniosków będzie "
             "odbywać się w sposób ciągły, wnioski rozpatrywane będą według kolejności wpływu do wyczerpania środków.")
    assert klasyfikuj_tekst(tytul, tresc)[0] == INNE
    # ten sam ogólny tytuł z treścią o środkach na działalność → nabór (pewność średnia)
    tresc2 = "Urząd ogłasza nabór wniosków o przyznanie jednorazowo środków na podjęcie działalności gospodarczej."
    assert klasyfikuj_tekst(tytul, tresc2) == (DOTACJA, "średnia")


@pytest.mark.parametrize("tytul", [
    # prawdziwe tytuły ze stron PUP (skan 14.10.2026)
    "Wstrzymanie naboru wniosków o dofinansowanie podjęcia działalności gospodarczej",  # PUP Wrocław
    "Lista rankingowa - dotacje 31.08-02.09.2026 r.",  # PUP Myszków
    "ZAKOŃCZENIE NABORU WNIOSKÓW O DOFINANSOWANIE BEZZWROTNEJ DOTACJI NA ZAŁOŻENIE DZIAŁALNOŚCI GOSPODARCZEJ",  # PUP Turek
    "Konkurs dotyczący wniosków o dotację na rozpoczęcie działalności gospodarczej został rozstrzygnięty",  # GUP Gdańsk
])
def test_prawdziwe_zakonczenia(tytul):
    assert klasyfikuj_tekst(tytul)[0] == ZAKONCZENIE


def test_zakonczenie_i_zapowiedz():
    assert klasyfikuj_tekst("Zakończenie naboru wniosków o dofinansowanie podjęcia działalności gospodarczej")[0] == ZAKONCZENIE
    assert klasyfikuj_tekst("Informacja o planowanym naborze wniosków o dofinansowanie podjęcia działalności gospodarczej")[0] == ZAPOWIEDZ


def test_rozbij_tytul_zl():
    assert rozbij_tytul_zl("PUP Gorzów Wielkopolski – Nabór wniosków") == ("Gorzów Wielkopolski", "Nabór wniosków")
    assert rozbij_tytul_zl("UP m.st. Warszawa – Nabór wniosków")[0] == "m.st. Warszawa"
    assert rozbij_tytul_zl("PUP Jastrzębie-Zdrój – Nabór wniosków")[0] == "Jastrzębie-Zdrój"
    assert rozbij_tytul_zl("Nabór wniosków o dofinansowanie") == ("", "Nabór wniosków o dofinansowanie")


# ---------------------------------------------------------------- daty
ODN = date(2026, 10, 14)


@pytest.mark.parametrize(
    "tekst,od,do,tryb",
    [
        ("Wnioski przyjmowane będą od 20.10.2026 do 24.10.2026", date(2026, 10, 20), date(2026, 10, 24), "terminowy"),
        ("nabór w dniach 3–7 listopada", date(2026, 11, 3), date(2026, 11, 7), "terminowy"),
        ("Nabór trwa do wyczerpania środków.", None, None, "do wyczerpania środków"),
        # prawdziwe fragmenty z ogłoszeń
        ("Wnioski przyjmowane będą w terminie od 19.10.2026 r. do 20.10.2026 r.", date(2026, 10, 19), date(2026, 10, 20), "terminowy"),
        ("Kiedy? W dniach 15-19 października 2026 r., w godzinach 7:30 – 15:30", date(2026, 10, 15), date(2026, 10, 19), "terminowy"),
        ("Nabór odbędzie się w dniach od 12 do 14 października 2026 r. Liczba miejsc: 3.", date(2026, 10, 12), date(2026, 10, 14), "terminowy"),
        ("Termin naboru: 28–29 września 2026 r.", date(2026, 9, 28), date(2026, 9, 29), "terminowy"),
        ("Nabór prowadzony będzie od dnia 12.10.2026 r. w sposób ciągły – do wyczerpania środków.", date(2026, 10, 12), None, "do wyczerpania środków"),
        ("Nabór wniosków trwa od 14.09.2026r. do 18.09.2026 r.", date(2026, 9, 14), date(2026, 9, 18), "terminowy"),
        ("W dniu 01.10.2026 r. od godz. 8:00 do godz. 14:00 Powiatowy Urząd Pracy w Ostrołęce prowadzić będzie nabór",
         date(2026, 10, 1), date(2026, 10, 1), "terminowy"),
        ("Wnioski będą przyjmowane: 25 września 2026 r. Kwota dofinansowania: do 25 000,00 złotych", date(2026, 9, 25), date(2026, 9, 25), "terminowy"),
        ("Nabór prowadzony będzie od 9 października 2026 r. Nabór ma charakter otwarty, tj. potrwa do momentu jego odwołania.",
         date(2026, 10, 9), None, "ciągły"),
        ("nabór od dnia 20 października 2026 r. (od godz. 8:00) do dnia 24 października 2026 r.", date(2026, 10, 20), date(2026, 10, 24), "terminowy"),
        ("przyjmowanie wniosków 20-24.10.2026", date(2026, 10, 20), date(2026, 10, 24), "terminowy"),
        ("wnioski można składać do 30.10.2026 r.", None, date(2026, 10, 30), "terminowy"),
    ],
)
def test_daty(tekst, od, do, tryb):
    wynik = wyciagnij_daty(tekst, ODN)
    assert (wynik["od"], wynik["do"], wynik["tryb"]) == (od, do, tryb)


def test_daty_przelom_roku():
    # ogłoszenie z grudnia o naborze w styczniu, bez roku w tekście
    wynik = wyciagnij_daty("nabór wniosków w dniach 12-16 stycznia", date(2026, 12, 18))
    assert wynik["od"] == date(2027, 1, 12) and wynik["do"] == date(2027, 1, 16)


def test_godziny_nie_sa_datami():
    assert wyciagnij_daty("wnioski przyjmujemy w godz. 7.30 – 15.30", ODN)["do"] is None


# ---------------------------------------------------------------- kwota, źródło, miejsca, grupy
def test_kwota_na_osobe_a_pula():
    # PUP Żory: limit na osobę 30 000, pula 60 000
    t = ("W ramach naboru można ubiegać się o dotację w wysokości do: 30 000,00 PLN. "
         "Urząd dysponuje kwotą 60 000,00 zł.")
    assert wyciagnij_kwote(t) == (30000, "do 30 000 zł")
    # PUP Turek: podana tylko pula
    kwota, opis = wyciagnij_kwote("Kwota w dyspozycji: 60.733,44 zł Planowane jest dofinansowanie dla 2 osób.")
    assert kwota is None and opis.startswith("pula naboru: 60 733 zł")
    # PUP Tuchola: krotność przeciętnego wynagrodzenia
    assert wyciagnij_kwote("Wysokość dofinansowania nie może przekroczyć kwoty 6-krotności przeciętnego wynagrodzenia.") == (
        None, "do 6-krotności przeciętnego wynagrodzenia")
    assert wyciagnij_kwote("PUP Inowrocław – 30 tysięcy złotych na otwarcie firmy")[0] == 30000


def test_zrodla_finansowania():
    assert wyciagnij_zrodla("ze środków Funduszu Pracy") == ["FP"]
    assert wyciagnij_zrodla("Dotacje na podjęcie działalności gospodarczej w ramach Projektu EFS+") == ["EFS+"]
    assert wyciagnij_zrodla("FEdKP: 30 tysięcy złotych na otwarcie firmy") == ["EFS+"]
    assert wyciagnij_zrodla("w ramach środków Państwowego Funduszu Rehabilitacji Osób Niepełnosprawnych (PFRON)") == ["PFRON"]
    assert wyciagnij_zrodla("Program „Rezerwa Funduszu Pracy na finansowanie kosztów realizacji form pomocy bez EFS+”") == ["FP"]


@pytest.mark.parametrize(
    "tekst,liczba",
    [
        ("Nabór odbędzie się w dniach od 12 do 14 października 2026 r. Liczba miejsc: 3.", 3),
        ("Planowane jest dofinansowanie dla 2 osób.", 2),
        ("Planowana liczba dotacji: ok. 8 Planowana kwota dotacji na osobę: ok. 20.000,00 zł", 8),
        ("Planowana liczba osób bezrobotnych objęta wsparciem – 24 osoby.", 24),
        ("Prognozowana liczba dotacji – 2.", 2),
        ("Więcej informacji znajduje się na stronie urzędu.", None),
    ],
)
def test_liczba_miejsc(tekst, liczba):
    assert wyciagnij_liczbe_miejsc(tekst) == liczba


def test_grupy():
    assert wyciagnij_grupy("dla osób do 30 r.ż.") == ["do 30 lat"]
    assert "osoby z niepełnosprawnością" in wyciagnij_grupy("osoby niepełnosprawne zarejestrowane w PUP")


# ---------------------------------------------------------------- pełna klasyfikacja i status
def _wpis_turek() -> Wpis:
    return Wpis(
        zrodlo="zielonalinia",
        tytul="PUP Turek – Nabór wniosków w ramach dofinansowania na podjęcie działalności gospodarczej dla osób do 30 r.ż.",
        url="https://zielonalinia.gov.pl/pup-turek-nabor/",
        data_publikacji="2026-10-12",
        tresc=("Powiatowy Urząd Pracy w Turku ogłasza nabór wniosków w ramach dofinansowania na podjęcie działalności "
               "gospodarczej dla osób do 30. r.ż. Kwota w dyspozycji: 60.733,44 zł Planowane jest dofinansowanie dla 2 osób. "
               "Kiedy? W dniach 15-19 października 2026 r., w godzinach 7:30 – 15:30"),
    )


def test_klasyfikuj_pelny_wpis():
    w = klasyfikuj(_wpis_turek())
    assert w.kategoria == DOTACJA and w.pewnosc == "wysoka"
    assert (w.nabor_od, w.nabor_do, w.tryb) == ("2026-10-15", "2026-10-19", "terminowy")
    assert w.liczba_miejsc == 2 and w.grupy_docelowe == ["do 30 lat"]


def test_status_i_opis_terminu():
    w = klasyfikuj(_wpis_turek())
    assert status(w, date(2026, 10, 14)) == "zapowiedziany"
    assert opis_terminu(w, date(2026, 10, 14)) == "start jutro"
    assert status(w, date(2026, 10, 16)) == "trwa"
    assert opis_terminu(w, date(2026, 10, 16)) == "zostały 3 dni"
    assert opis_terminu(w, date(2026, 10, 19)) == "dziś ostatni dzień"
    assert status(w, date(2026, 10, 20)) == "zakończony"
    w.nabor_od, w.nabor_do = "2026-10-01", "2026-10-30"
    assert opis_terminu(w, date(2026, 10, 14)) == "zostało 16 dni"
    assert opis_terminu(w, date(2026, 10, 8)) == "zostały 22 dni"
