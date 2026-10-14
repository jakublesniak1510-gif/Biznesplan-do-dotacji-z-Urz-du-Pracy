"""Struktury danych monitora."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields


@dataclass
class Pup:
    pup_id: str
    nazwa: str
    wojewodztwo: str
    url: str
    miasto: str = ""
    subdomena_potwierdzona: str = ""  # data RRRR-MM-DD albo pusto
    sciezka_aktualnosci: str = "/rynek-pracy/aktualnosci"  # kilka urzędów ma inną (np. /rynek-pracy/aktualnosci-urzedu)

    @property
    def host(self) -> str:
        return self.url.split("//", 1)[-1].split("/", 1)[0]


@dataclass
class Wpis:
    """Pojedyncza aktualność (z Zielonej Linii albo ze strony PUP) wraz z wynikiem klasyfikacji."""

    zrodlo: str  # "zielonalinia" | "pup"
    tytul: str
    url: str
    data_publikacji: str = ""  # RRRR-MM-DD
    pup_id: str = ""
    pup_nazwa: str = ""
    wojewodztwo: str = ""
    tresc: str = ""  # zajawka / treść bez HTML (skrócona)
    url_urzedu: str = ""  # link do ogłoszenia na stronie PUP (dla wpisów z Zielonej Linii)
    # --- klasyfikacja ---
    kategoria: str = ""  # zob. klasyfikator.KATEGORIE
    pewnosc: str = ""  # "wysoka" | "średnia" | "niska"
    nabor_od: str = ""
    nabor_do: str = ""
    tryb: str = ""  # "terminowy" | "do wyczerpania środków" | "ciągły" | ""
    kwota_max_zl: int | None = None
    kwota_opis: str = ""
    zrodla_finansowania: list[str] = field(default_factory=list)
    liczba_miejsc: int | None = None
    grupy_docelowe: list[str] = field(default_factory=list)
    wstrzymany: str = ""  # RRRR-MM-DD: urząd ogłosił zakończenie/wstrzymanie albo listę rankingową
    # --- stan ---
    klucz: str = ""
    zrodla: list[str] = field(default_factory=list)  # wszystkie źródła, w których widziano wpis
    pierwszy_raz: str = ""
    ostatni_raz: str = ""

    def do_slownika(self) -> dict:
        return asdict(self)

    @classmethod
    def ze_slownika(cls, d: dict) -> "Wpis":
        znane = {f.name for f in fields(cls)}
        return cls(**{kk: v for kk, v in d.items() if kk in znane})
