from pup_gen import prompty
from pup_gen.cli import main
from pup_gen.koszt import CENNIK_USD_ZA_MTOK, szacuj

from conftest import mapa


def test_szacunek_kosztu(kw, regulamin, fin_szablonu):
    dane = prompty.blok_danych_klienta(kw, fin_szablonu, regulamin)
    zap = [prompty.zbuduj_zapytanie(kw, p, fin_szablonu, regulamin, dane_klienta=dane)
           for p in mapa().pola if p.sekcje_tekstowe]
    sz = szacuj(zap, "claude-opus-5-5")
    assert len(sz.pola) == 11
    assert 0.1 < sz.usd < sz.usd_bez_cache < 5
    assert szacuj(zap, "claude-sonnet-5-5").usd < sz.usd
    assert set(CENNIK_USD_ZA_MTOK) == {"claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5"}


def test_komenda_koszt(capsys):
    assert main(["koszt", "--model", "claude-opus-5-5"]) == 0
    out = capsys.readouterr().out
    assert "Koszt na plan z prompt caching" in out and "USD" in out
