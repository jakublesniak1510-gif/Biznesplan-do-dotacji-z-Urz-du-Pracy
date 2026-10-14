from pup_gen import kontrola
from pup_gen.schemat import Kwestionariusz

from conftest import surowy_kwestionariusz
from pomocnicze import wynik

POPRAWNY = ("Od grudnia 2026 r. strzygę klientki w ich domach w Borkowie. Strzyżenie damskie kosztuje 80 zł, "
            "koloryzacja 200 zł. W 12 miesiącach zakładam 87 415 zł przychodu, a zysk netto wyniesie 42 429 zł. "
            "Margines bezpieczeństwa to 68,3%, materiały to 12% przychodu. Przy przychodach niższych o 30% "
            "zysk netto wyniesie 22 536 zł.")


def _poziomy(raport, kategoria):
    return [u for u in raport.ustalenia if u.kategoria == kategoria]


def test_wzorce_parsowane_z_pliku():
    frazy = {w.fraza: w for w in kontrola.wzorce()}
    assert len(frazy) > 40
    assert frazy["kompleksowa obsługa"].poziom == "BLOKUJE"
    assert frazy["dynamicznie rozwijający się branża"].kategoria == "zakazany zwrot"
    assert frazy["gwarantuję"].kategoria == "obietnica"
    assert frazy["konkurencyjne ceny"].poziom == "OSTRZEŻENIE"  # warunkowy: „(bez podania cen…)”


def test_poprawny_tekst_bez_blokad(kw, regulamin, fin_szablonu):
    r = kontrola.sprawdz(wynik(fin_szablonu, {"1": (POPRAWNY, len(POPRAWNY) + 20)}), kw, regulamin)
    assert not [u for u in r.ustalenia if u.poziom == "BLOKUJE"], r.markdown()


def test_zakazane_zwroty(kw, regulamin, fin_szablonu):
    tekst = ("Działam na dynamicznie rozwijającym się rynku i zapewniam kompleksową obsługę. "
             "W dzisiejszych czasach to kluczowe.")
    r = kontrola.sprawdz(wynik(fin_szablonu, {"1": (tekst, None)}), kw, regulamin)
    znalezione = _poziomy(r, "zakazany zwrot")
    assert len(znalezione) >= 4
    assert all(u.poziom == "BLOKUJE" for u in znalezione)
    assert "BLOKUJE" in r.markdown() and r.blokuje


def test_obietnice(kw, regulamin, fin_szablonu):
    r = kontrola.sprawdz(wynik(fin_szablonu, {"1": ("Gwarantuję, że klienci na pewno przyjdą.", None)}), kw, regulamin)
    assert len([u for u in _poziomy(r, "obietnica") if u.poziom == "BLOKUJE"]) == 2


def test_niespojna_liczba(kw, regulamin, fin_szablonu):
    tekst = POPRAWNY + " Zysk netto wyniesie 55 555 zł, a marża 47%."
    r = kontrola.sprawdz(wynik(fin_szablonu, {"1": (tekst, None)}), kw, regulamin)
    liczby = _poziomy(r, "spójność liczb")
    assert {u.poziom for u in liczby} == {"BLOKUJE"}
    assert len(liczby) == 2
    assert "55 555 zł" in liczby[0].komunikat


def test_przekroczony_limit_reklamy(kw, regulamin, fin_szablonu):
    ostry = regulamin.model_copy(update={"limit_reklama_pct": 10.0})  # reklama w przykładzie = 18% dotacji
    r = kontrola.sprawdz(wynik(fin_szablonu, {"1": (POPRAWNY, None)}), kw, ostry)
    blok = [u for u in _poziomy(r, "regulamin") if u.poziom == "BLOKUJE"]
    assert any("reklama" in u.komunikat and "limit regulaminu 10%" in u.komunikat for u in blok)


def test_dlugosc_i_braki(kw, regulamin, fin_szablonu):
    za_dlugi = POPRAWNY
    za_krotki = "Od grudnia 2026 r. strzygę w Borkowie. [BRAK DANYCH: kod PKD 2025]"
    r = kontrola.sprawdz(wynik(fin_szablonu, {"1": (za_dlugi, 100), "2": (za_krotki, 1000)}), kw, regulamin)
    dl = {u.pole: u.poziom for u in _poziomy(r, "długość")}
    assert dl == {"1": "BLOKUJE", "2": "OSTRZEŻENIE"}
    assert r.braki == [("2", "[BRAK DANYCH: kod PKD 2025]")]
    assert "Pytania do klienta" in r.markdown()


def test_niepodstawiona_zmienna_i_wzmianka_o_ai(kw, regulamin, fin_szablonu):
    tekst = "Zysk wyniesie {{ark_nieistniejaca}}. Tekst przygotował model językowy."
    r = kontrola.sprawdz(wynik(fin_szablonu, {"1": (tekst, None)}), kw, regulamin)
    kategorie = {u.kategoria for u in r.ustalenia if u.poziom == "BLOKUJE"}
    assert {"zmienne", "wzmianka o AI"} <= kategorie


def test_wykluczenia_regulaminu(regulamin, fin_szablonu):
    d = surowy_kwestionariusz()
    d["pomysl"]["pkd"] = [{"kod": "47.79.Z", "nazwa": "Sprzedaż detaliczna artykułów używanych", "glowny": True}]
    d["pomysl"]["sezonowosc"] = "tak"
    d["pomysl"]["opis"] += " Dodatkowo prowadzę komis odzieży."
    d["zakup_od_rodziny"] = True
    kw = Kwestionariusz.model_validate(d)
    r = kontrola.sprawdz(wynik(fin_szablonu, {"1": (POPRAWNY, None)}), kw, regulamin)
    blok = " | ".join(u.komunikat for u in _poziomy(r, "regulamin") if u.poziom == "BLOKUJE")
    assert "47.79.Z" in blok and "sezonow" in blok and "komis" in blok and "rodziny" in blok


def test_komisja_to_nie_komis(kw, regulamin, fin_szablonu):
    d = surowy_kwestionariusz()
    d["pomysl"]["opis"] += " Komisja oceniająca zna moje kwalifikacje."
    r = kontrola.sprawdz(wynik(fin_szablonu, {"1": (POPRAWNY, None)}), Kwestionariusz.model_validate(d), regulamin)
    assert not any("komis" in u.komunikat for u in r.ustalenia if u.poziom == "BLOKUJE")


def test_sprzet_uzywany_zakazany(kw, fin_szablonu):
    from pup_gen import przebieg
    lipno = przebieg.wczytaj_regulamin("lipno-przyklad")
    r = kontrola.sprawdz(wynik(fin_szablonu, {"1": (POPRAWNY, None)}), kw, lipno)
    assert any("używanego" in u.komunikat for u in r.ustalenia if u.poziom == "BLOKUJE")
