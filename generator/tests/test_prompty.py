from pup_gen import KATALOG_SZABLONOW, prompty
from pup_gen.schemat import PoleFormularza

from conftest import mapa


def test_prompt_systemowy_z_pliku():
    s = prompty.prompt_systemowy()
    assert s.startswith("Jesteś asystentem")
    assert "LISTA ZAKAZANA" in s and "=====" not in s
    assert s in (KATALOG_SZABLONOW / "00-system-prompt.md").read_text(encoding="utf-8")


def test_szablon_bez_przykladu():
    for nr in [f"{i:02d}" for i in range(1, 10)]:
        sz = prompty.wczytaj_szablon(nr)
        assert "## 8." not in sz.tresc and "DANE FIKCYJNE" not in sz.tresc
        assert sz.prompt_sekcji.startswith(f"SEKCJA {nr}")


def test_wypelnienie_promptu_sekcji():
    pole = PoleFormularza(id="IV.2", nazwa_w_formularzu="Analiza konkurencji", sekcje=["04"], format="tabela",
                          limit_znakow=2000)
    tekst = prompty.wypelnij_prompt_sekcji(prompty.wczytaj_szablon("04"), pole, 2000, "rzeczowy")
    assert '"Analiza konkurencji"' in tekst and "limit: 2000" in tekst and "ton: rzeczowy" in tekst
    assert "format: tabela)" in tekst and "{{" not in tekst
    pole06 = pole.model_copy(update={"sekcje": ["06"]})
    assert "format: pozycyjny" in prompty.wypelnij_prompt_sekcji(prompty.wczytaj_szablon("06"), pole06, 2000, "ciepły")
    t08 = prompty.wypelnij_prompt_sekcji(prompty.wczytaj_szablon("08"), pole.model_copy(update={"sekcje": ["08"]}), 2000, "ciepły")
    assert "{{ark_przychod_12m}}" in t08  # zmienne arkusza zostają dla modelu


def test_warianty_dlugosci():
    assert prompty.wariant_dla_limitu(760) == "krótki"
    assert prompty.wariant_dla_limitu(1900) == "standard"
    assert prompty.wariant_dla_limitu(3800) == "długi"
    assert prompty.wariant_dla_limitu(None) == "standard"


def test_zapytanie_sklada_bloki(kw, regulamin, fin_szablonu):
    pole = next(p for p in mapa().pola if p.id == "IV.2")
    z = prompty.zbuduj_zapytanie(kw, pole, fin_szablonu, regulamin)
    assert z.sekcje == ["03", "04"] and z.limit_znakow == 2850
    assert "<kwestionariusz>" in z.dane_klienta and '"ark_przychod_12m": "87 415 zł"' in z.dane_klienta
    assert "<regulamin_pup>" in z.dane_klienta
    assert kw.kontakt.email not in z.dane_klienta
    assert 'nr="03"' in z.szablony and 'nr="04"' in z.szablony
    assert "podzial_limitu" in z.polecenie and "ton: ciepły" in z.polecenie and "wariant: standard" in z.polecenie
    bloki = z.tresc_uzytkownika()
    assert [("cache_control" in b) for b in bloki] == [True, True, False]


def test_uwagi_pola_przekazane_doslownie(kw, regulamin, fin_szablonu):
    pole = next(p for p in mapa().pola if p.id == "III.2")
    z = prompty.zbuduj_zapytanie(kw, pole, fin_szablonu, regulamin)
    assert "Dlaczego zdecydował/a się Pan/i na własną działalność?" in z.polecenie
    assert "wariant: krótki" in z.polecenie
