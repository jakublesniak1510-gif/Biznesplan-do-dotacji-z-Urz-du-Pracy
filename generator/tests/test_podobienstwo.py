import datetime as dt

from pup_gen import kontrola

from pomocnicze import wynik

TEKST_A = ("Od grudnia 2026 r. strzygę klientki w ich domach w Borkowie i Zielonowie. Przez dziewięć lat "
           "pracowałam w salonie przy ulicy Kościuszki, a od 2022 r. raz w miesiącu strzygę mieszkańców domu "
           "pomocy społecznej Pod Lipami. Klientki z salonu pytały, czy mogę przyjeżdżać do nich do domu, "
           "bo część z nich przestała wychodzić. Sprzęt wożę w walizce, a wizyty umawiam przez telefon i stronę.")
TEKST_B = TEKST_A.replace("Borkowie i Zielonowie", "Lipach i Borkowie").replace("dziewięć", "osiem")
TEKST_C = ("Warsztat w Lipach przy drodze powiatowej obsłuży auta osobowe i dostawcze. Mam certyfikat "
           "F-gazowy i piętnaście lat praktyki jako mechanik, ostatnio kierownik zmiany. Firma przewozowa "
           "podpisała list intencyjny na serwis sześciu busów. Diagnostykę komputerową wykonam na miejscu.")


def _zapisz(katalog, w):
    katalog.mkdir(parents=True)
    (katalog / "wynik.json").write_text(w.model_dump_json(), encoding="utf-8")


def test_dwa_podobne_plany_do_tego_samego_pup(tmp_path, kw, regulamin, fin_szablonu):
    _zapisz(tmp_path / "zielonow" / "stary", wynik(fin_szablonu, {"1": (TEKST_B, None)}, id_zlecenia="stary",
                                                    data=dt.datetime(2026, 9, 1)))
    _zapisz(tmp_path / "inny-pup" / "x", wynik(fin_szablonu, {"1": (TEKST_A, None)}, id_zlecenia="x", pup_id="inny"))
    nowy = wynik(fin_szablonu, {"1": (TEKST_A, None)}, id_zlecenia="nowy")
    nowy.pup = "Inna nazwa"  # porównanie po pup_id
    r = kontrola.sprawdz(nowy, kw, regulamin, archiwum=tmp_path)
    podob = [u for u in r.ustalenia if u.kategoria == "podobieństwo"]
    assert len(podob) == 1 and podob[0].poziom == "OSTRZEŻENIE"
    assert "plan stary" in podob[0].komunikat and "fragmenty 8-wyrazowe" in podob[0].komunikat
    assert any(u.kategoria == "rotacja tonu" for u in r.ustalenia)  # ten sam ton w ciągu 3 miesięcy


def test_rozne_plany_tylko_info(tmp_path, kw, regulamin, fin_szablonu):
    _zapisz(tmp_path / "a", wynik(fin_szablonu, {"1": (TEKST_C, None)}, id_zlecenia="mechanik", ton="techniczny"))
    r = kontrola.sprawdz(wynik(fin_szablonu, {"1": (TEKST_A, None)}, id_zlecenia="nowy"), kw, regulamin,
                         archiwum=tmp_path)
    podob = [u for u in r.ustalenia if u.kategoria == "podobieństwo"]
    assert [u.poziom for u in podob] == ["INFO"]
    assert not any(u.kategoria == "rotacja tonu" for u in r.ustalenia)


def test_tfidf_identyczne_i_rozne():
    a = kontrola._slowa(TEKST_A)
    cos = kontrola._tfidf_cosinus([a, a, kontrola._slowa(TEKST_C)])
    assert cos[0] > 0.99 and cos[1] < 0.2
