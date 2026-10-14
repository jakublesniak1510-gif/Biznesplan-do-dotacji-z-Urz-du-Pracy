from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixture_tekst():
    def wczytaj(nazwa: str) -> str:
        return (FIXTURES / nazwa).read_text(encoding="utf-8")

    return wczytaj
