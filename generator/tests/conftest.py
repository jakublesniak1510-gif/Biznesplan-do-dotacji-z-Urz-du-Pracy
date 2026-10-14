"""Wspólne dane testowe. Testy z prawdziwym LibreOffice oznaczone są markerem `soffice`."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from pup_gen import KATALOG_PRZYKLADOW, PLIK_MODELU, finanse, przebieg
from pup_gen.schemat import Kwestionariusz, MapaFormularza

PRZYKLADY = ["fryzjerka-mobilna", "mechanik-samochodowy", "firma-sprzatajaca"]
SOFFICE = shutil.which("soffice") or (Path("/usr/bin/soffice") if Path("/usr/bin/soffice").exists() else None)


def pytest_configure(config):
    config.addinivalue_line("markers", "soffice: test używa prawdziwego LibreOffice")


def pytest_collection_modifyitems(config, items):
    if SOFFICE:
        return
    pomin = pytest.mark.skip(reason="brak LibreOffice (soffice)")
    for item in items:
        if "soffice" in item.keywords:
            item.add_marker(pomin)


def surowy_kwestionariusz(nazwa: str = "fryzjerka-mobilna") -> dict:
    return json.loads((KATALOG_PRZYKLADOW / f"kwestionariusz-{nazwa}.json").read_text(encoding="utf-8"))


def kwestionariusz(nazwa: str = "fryzjerka-mobilna") -> Kwestionariusz:
    return Kwestionariusz.model_validate(surowy_kwestionariusz(nazwa))


def mapa(nazwa: str = "mapa-dluga-14-pol") -> MapaFormularza:
    return MapaFormularza.model_validate_json((KATALOG_PRZYKLADOW / f"{nazwa}.json").read_text(encoding="utf-8"))


@pytest.fixture
def kw() -> Kwestionariusz:
    return kwestionariusz()


@pytest.fixture
def regulamin():
    return przebieg.wczytaj_regulamin("zielonow")


@pytest.fixture(scope="session")
def fin_szablonu() -> finanse.WynikFinansowy:
    """Wartości ark_* zapisane w szablonie arkusza (przykład fryzjerki) – bez uruchamiania LibreOffice."""
    wartosci, kontrole, _ = finanse.odczytaj(PLIK_MODELU)
    return finanse.WynikFinansowy(plik=PLIK_MODELU, wartosci=wartosci, kontrole=kontrole,
                                  ark={n: finanse.formatuj_ark(n, v) for n, v in wartosci.items()},
                                  tabele=finanse.odczytaj_tabele(PLIK_MODELU))
