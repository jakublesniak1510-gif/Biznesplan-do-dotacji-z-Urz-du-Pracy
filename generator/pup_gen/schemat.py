"""Modele danych: kwestionariusz klienta, regulamin PUP, mapa formularza, wynik generacji.

Pola kwestionariusza odpowiadają `docs/kwestionariusz-klienta.md` (numery pytań w komentarzach),
a `Kwestionariusz.dane_do_promptu()` układa je według słownika K1–K15 z `szablony/00-system-prompt.md`.
"""

from __future__ import annotations

import csv
import datetime as dt
import logging
import re
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Ton = Literal["rzeczowy", "ciepły", "techniczny"]
Poziom = Literal["BLOKUJE", "OSTRZEŻENIE", "INFO"]
KategoriaZakupu = Literal["sprzęt", "towar", "reklama", "remont", "inne"]

TABELE_ARKUSZA = ("kosztorys", "kalkulacja_miesieczna", "kalkulacja_kwartalna", "wskazniki")
DANE_ARKUSZA = ("kwota_dotacji", "wklad_wlasny", "forma_opodatkowania", "pkd", "data_startu")
SEKCJE_TEKSTOWE = tuple(f"{i:02d}" for i in range(1, 10))


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


# --------------------------------------------------------------------------- dane osobowe
_KLUCZE_ZAKAZANE = re.compile(
    r"pesel|^(dow[oó]d(_osobisty)?|(nr|numer|seria)_(dowodu|dokumentu|rachunku)|rachunek_bankowy|iban)$", re.I)
_PESEL_SLOWO = re.compile(r"pesel\W{0,5}\d", re.I)
_RE_11_CYFR = re.compile(r"(?<!\d)\d{11}(?!\d)")
_RE_DOWOD = re.compile(r"(?<![A-Za-z0-9])([A-Z]{3})\s?(\d{6})(?![0-9])")


def pesel_poprawny(numer: str) -> bool:
    """Suma kontrolna PESEL (wagi 1-3-7-9)."""
    if not re.fullmatch(r"\d{11}", numer):
        return False
    wagi = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)
    suma = sum(int(c) * w for c, w in zip(numer, wagi))
    return (10 - suma % 10) % 10 == int(numer[10])


def dowod_poprawny(seria: str, numer: str) -> bool:
    """Suma kontrolna numeru dowodu osobistego (AAA + 6 cyfr, cyfra kontrolna na 4. pozycji)."""
    znaki = [ord(c) - 55 for c in seria] + [int(c) for c in numer]
    wagi = (7, 3, 1, 0, 7, 3, 1, 7, 3)
    return sum(z * w for z, w in zip(znaki, wagi)) % 10 == znaki[3]


def znajdz_dane_osobowe(dane: Any, sciezka: str = "") -> list[str]:
    """Zwraca listę miejsc (ścieżek), w których wygląda na to, że jest PESEL lub numer dowodu."""
    znalezione: list[str] = []
    if isinstance(dane, dict):
        for klucz, wartosc in dane.items():
            sc = f"{sciezka}.{klucz}" if sciezka else str(klucz)
            if _KLUCZE_ZAKAZANE.search(str(klucz)) and wartosc not in (None, "", [], {}):
                znalezione.append(f"{sc} (pole o niedozwolonej nazwie)")
            znalezione += znajdz_dane_osobowe(wartosc, sc)
    elif isinstance(dane, list):
        for i, wartosc in enumerate(dane):
            znalezione += znajdz_dane_osobowe(wartosc, f"{sciezka}[{i}]")
    elif isinstance(dane, (str, int)) and not isinstance(dane, bool):
        tekst = str(dane)
        if tekst.startswith(("http://", "https://", "www.")):
            return znalezione  # identyfikatory ofert w linkach to nie PESEL
        if _PESEL_SLOWO.search(tekst) or any(pesel_poprawny(m) for m in _RE_11_CYFR.findall(tekst)):
            znalezione.append(f"{sciezka} (PESEL)")
        if any(dowod_poprawny(s, n) for s, n in _RE_DOWOD.findall(tekst)):
            znalezione.append(f"{sciezka} (numer dowodu osobistego)")
    return znalezione


# --------------------------------------------------------------------------- kwestionariusz
class Kontakt(_Model):
    """Sekcja 0. Nie trafia do promptów ani do logów."""

    email: str | None = None
    telefon: str | None = None


class Osoba(_Model):
    """K1 / pyt. 0.1. Tylko imię i miejscowość – nazwiska i adresu nie zbieramy."""

    imie: str = Field(min_length=2)
    miejscowosc: str
    gmina: str | None = None


class Nabor(_Model):
    """Sekcja 1 – urząd i nabór."""

    nazwa_pup: str
    pup_id: str | None = Field(None, description="slug z bazy regulaminów, np. 'zielonow'")
    powiat: str | None = None
    url_ogloszenia: str | None = None
    url_regulaminu: str | None = None
    kwota_max_zl: float | None = Field(None, gt=0)
    termin_zlozenia: dt.date | None = None
    zrodlo_finansowania: str | None = None


class Zabezpieczenie(_Model):
    """Sekcja 2 – bez danych poręczycieli. Nie trafia do promptów."""

    formy: list[str] = Field(default_factory=list)
    liczba_poreczycieli: int = Field(0, ge=0)
    uwagi: str | None = None


class Pkd(_Model):
    kod: str = Field(pattern=r"^\d{2}\.\d{2}\.[A-Z]$")
    nazwa: str
    glowny: bool = False


class Pomysl(_Model):
    """Sekcja 3."""

    opis: str = Field(min_length=300, description="pyt. 3.1, min. 300 znaków")
    pkd: list[Pkd] = Field(default_factory=list, description="pyt. 3.3; puste = dobiera właściciel")
    uprawnienia: str = Field(description="pyt. 3.4")
    sezonowosc: Literal["nie", "częściowo", "tak"] = "nie"
    sezonowosc_opis: str | None = None
    data_startu: dt.date
    przejecie_od_rodziny: str = Field("nie", description="pyt. 3.7")
    motywacja: str | None = Field(None, description="pyt. 3.8 / K13")


class Usluga(_Model):
    """Pyt. 3.2 – jedna linia arkusza `Przychody` (maks. 5)."""

    nazwa: str
    cena: float = Field(gt=0, description="cena dla klienta w zł")
    jednostka: str = "usługa"
    liczba_mies: int = Field(gt=0, description="liczba sprzedaży miesięcznie przy pełnym obłożeniu")
    czas_h: float = Field(gt=0, description="czas jednej usługi w godzinach")
    glowna: bool = False


class Forma(_Model):
    """Sekcja 4."""

    forma_prawna: str = "jednoosobowa działalność gospodarcza"
    opodatkowanie: Literal["skala", "liniowy", "ryczałt", "nie wiem"] = "nie wiem"
    stawka_ryczaltu: float | None = Field(None, gt=0, lt=0.2)
    vat: Literal["zwolniony", "czynny", "nie wiem"] = "nie wiem"
    stawka_vat_sprzedaz: float = Field(0.23, ge=0, le=0.23)
    zus: Literal["ulga na start + preferencyjny", "preferencyjny", "pełny", "nie wiem"] = "nie wiem"
    chorobowe: bool = True
    ksiegowosc: str | None = None

    @model_validator(mode="after")
    def _ryczalt(self) -> Forma:
        if self.opodatkowanie == "ryczałt" and self.stawka_ryczaltu is None:
            raise ValueError("forma.stawka_ryczaltu: przy ryczałcie podaj stawkę (np. 0.085)")
        return self


class Lokalizacja(_Model):
    """Sekcja 5 / K6."""

    tryb: Literal["własny lokal", "wynajem", "użyczenie", "w mieszkaniu", "mobilnie", "online"]
    miejscowosc: str
    ulica: str | None = None
    opis_lokalu: str | None = None
    dokument_lokalu: Literal["tak", "w trakcie", "nie", "nie dotyczy"] = "nie dotyczy"
    obszar: list[str] = Field(default_factory=list, description="obsługiwane miejscowości / gminy")
    promien_km: float | None = Field(None, gt=0)
    dojazd: str | None = None
    prawo_jazdy: str | None = None
    przechowywanie_sprzetu: str | None = None
    godziny_pracy: str | None = None
    przyjmowanie_zlecen: str | None = None


class Wyksztalcenie(_Model):
    poziom: str
    szkola: str | None = None
    kierunek: str | None = None
    rok: int | None = Field(None, ge=1950, le=2030)


class Kurs(_Model):
    nazwa: str
    organizator: str | None = None
    rok: int | None = Field(None, ge=1950, le=2030)
    godziny: int | None = Field(None, gt=0)


class Praca(_Model):
    pracodawca: str
    miejscowosc: str | None = None
    stanowisko: str
    od: str = Field(description="RRRR albo RRRR-MM")
    do: str = Field(description="RRRR, RRRR-MM albo 'obecnie'")
    obowiazki: str


class Kwalifikacje(_Model):
    """Sekcja 6 / K2–K3."""

    wyksztalcenie: list[Wyksztalcenie] = Field(min_length=1)
    kursy: list[Kurs] = Field(default_factory=list)
    doswiadczenie: list[Praca] = Field(default_factory=list)
    nieformalne: str | None = None
    dokumenty: list[str] = Field(default_factory=list, description="dokumenty, które klient dołączy")
    szkolenie_pup: str | None = None
    inne_umiejetnosci: str | None = None


class Segment(_Model):
    nazwa: str
    opis: str
    liczba: str | None = None


class DaneTerenu(_Model):
    opis: str
    zrodlo: str


class Klienci(_Model):
    """Sekcja 7 / K7."""

    segmenty: list[Segment] = Field(min_length=1)
    dane_o_terenie: list[DaneTerenu] = Field(default_factory=list)
    dowody_popytu: list[str] = Field(default_factory=list)
    zainteresowani: str | None = None


class Konkurent(_Model):
    nazwa: str
    miejscowosc: str
    link: str | None = None
    oferta: str
    ceny: str
    zrodlo_cen: str | None = None
    slabe_strony: str
    mocne_strony: str | None = None


class Konkurencja(_Model):
    """Sekcja 8 / K8 – 3 do 5 konkurentów."""

    konkurenci: list[Konkurent] = Field(min_length=3, max_length=5)
    data_rozpoznania: str | None = None
    substytuty: list[str] = Field(default_factory=list)
    przewaga: str


class Marketing(_Model):
    """K9."""

    kanaly: list[str] = Field(min_length=1)
    pierwsze_dzialania: list[str] = Field(default_factory=list)
    cele: str | None = None
    utrzymanie: list[str] = Field(default_factory=list)


class Zakup(_Model):
    """Pyt. 9.1 – jedna pozycja kosztorysu (wiersze 5–24 arkusza `Kosztorys`)."""

    nazwa: str
    kategoria: KategoriaZakupu
    stan: Literal["nowy", "używany"] = "nowy"
    ilosc: int = Field(1, gt=0)
    cena_brutto: float = Field(gt=0, description="cena brutto za sztukę z oferty")
    stawka_vat: float = Field(0.23, ge=0, le=0.23, description="0 przy zakupie od osoby prywatnej")
    sprzedawca: str | None = None
    link: str | None = None
    uzasadnienie: str
    finansowanie: Literal["dotacja", "wkład własny"] = "dotacja"
    pojazd: bool = False

    @property
    def cena_netto(self) -> float:
        return round(self.cena_brutto / (1 + self.stawka_vat), 2)

    def kwota_do_rozliczenia(self, vat_czynny: bool) -> float:
        """Jak kolumna K arkusza: netto u czynnego podatnika VAT, brutto u zwolnionego."""
        netto = round(self.cena_netto * self.ilosc, 2)
        return netto if vat_czynny else round(netto + round(netto * self.stawka_vat, 2), 2)


class Zasob(_Model):
    nazwa: str
    wartosc: float | None = Field(None, ge=0)


class WkladWlasny(_Model):
    """Sekcja 10 / K11."""

    kwota: float = Field(0, ge=0)
    zrodlo: str | None = None
    na_co: str | None = None


class ListIntencyjny(_Model):
    """Sekcja 11."""

    od_kogo: str
    czego_dotyczy: str
    czestotliwosc: str | None = None
    status: Literal["podpisany", "obiecany", "w trakcie"] = "podpisany"


class KosztyStale(_Model):
    """Pyt. 13.3 – arkusz `Koszty!B9:B16` (zł/mies.)."""

    czynsz: float = Field(0, ge=0)
    media: float = Field(0, ge=0)
    telefon_internet: float = Field(0, ge=0)
    ksiegowosc: float = Field(0, ge=0)
    ubezpieczenie: float = Field(0, ge=0)
    paliwo: float = Field(0, ge=0)
    reklama: float = Field(0, ge=0)
    inne: float = Field(0, ge=0)


class Prognoza(_Model):
    """Sekcja 13 – dane wejściowe arkusza."""

    klienci_m1: int | None = Field(None, ge=0)
    klienci_m6: int | None = Field(None, ge=0)
    klienci_m12: int | None = Field(None, ge=0)
    sezonowosc: list[float] = Field(default_factory=lambda: [1.0] * 12, description="mnożniki sty..gru")
    rozruch: list[float] = Field(default_factory=lambda: [0.4, 0.6, 0.8] + [1.0] * 9)
    dni_robocze: int = Field(21, gt=0, le=31)
    godziny_dzien: float = Field(6, gt=0, le=16)
    materialy_pct: float = Field(0.1, ge=0, lt=1)
    materialy_opis: str | None = None
    koszty_stale: KosztyStale = Field(default_factory=KosztyStale)

    @field_validator("sezonowosc", "rozruch")
    @classmethod
    def _dwanascie(cls, v: list[float]) -> list[float]:
        if len(v) != 12 or any(x < 0 for x in v):
            raise ValueError("lista musi mieć 12 nieujemnych wartości (miesiące)")
        return v


class Ryzyko(_Model):
    ryzyko: str
    zapobieganie: str | None = None
    plan_b: str | None = None


class FinanseDomowe(_Model):
    """K11 – inne dochody gospodarstwa i potrzeby życiowe."""

    inne_dochody: str | None = None
    potrzeby_mies: float | None = Field(None, ge=0)
    wytrzymalosc: Literal["< 3 mies.", "3–6 mies.", "> 6 mies."] | None = None


class Kwestionariusz(_Model):
    """Odpowiedzi klienta (docs/kwestionariusz-klienta.md, wersja 2)."""

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{2,80}$", description="identyfikator zlecenia (slug)")
    kontakt: Kontakt = Field(default_factory=Kontakt)
    osoba: Osoba
    nabor: Nabor
    status: Literal["bezrobotny", "absolwent CIS", "absolwent KIS", "opiekun osoby niepełnosprawnej"]
    bezrobotny_od: str | None = None
    powod_utraty_pracy: str | None = None
    grupy: list[str] = Field(default_factory=list)
    kwota_wnioskowana: float = Field(gt=0)
    zabezpieczenie: Zabezpieczenie = Field(default_factory=Zabezpieczenie)
    pomysl: Pomysl
    uslugi: list[Usluga] = Field(min_length=1, max_length=5)
    forma: Forma = Field(default_factory=Forma)
    lokalizacja: Lokalizacja
    kwalifikacje: Kwalifikacje
    klienci: Klienci
    konkurencja: Konkurencja
    marketing: Marketing
    zakupy: list[Zakup] = Field(min_length=1, max_length=20)
    zakup_od_rodziny: bool = False
    zasoby_posiadane: list[Zasob] = Field(default_factory=list)
    wklad_wlasny: WkladWlasny = Field(default_factory=WkladWlasny)
    listy_intencyjne: list[ListIntencyjny] = Field(default_factory=list)
    zatrudnienie: str = "nie"
    prognoza: Prognoza = Field(default_factory=Prognoza)
    ryzyka: list[Ryzyko] = Field(default_factory=list)
    finanse_domowe: FinanseDomowe = Field(default_factory=FinanseDomowe)
    ton: Ton
    notatka_wlasciciela: str | None = Field(None, description="np. dane o terenie, ustalenia z regulaminu")

    @model_validator(mode="before")
    @classmethod
    def _bez_danych_osobowych(cls, dane: Any) -> Any:
        miejsca = znajdz_dane_osobowe(dane)
        if miejsca:
            raise ValueError(
                "Kwestionariusz zawiera dane, których nie zbieramy (PESEL / numer dowodu): "
                + ", ".join(miejsca)
                + ". Usuń je – klient wpisuje je sam w formularzu urzędu."
            )
        return dane

    @model_validator(mode="after")
    def _kwoty(self) -> Kwestionariusz:
        suma = self.suma_zakupow_z_dotacji()
        if suma > self.kwota_wnioskowana + 0.01:
            raise ValueError(
                f"Zakupy finansowane z dotacji ({suma:.2f} zł) przekraczają kwotę wnioskowaną "
                f"({self.kwota_wnioskowana:.2f} zł). Przenieś część pozycji na wkład własny."
            )
        if self.nabor.kwota_max_zl and self.kwota_wnioskowana > self.nabor.kwota_max_zl + 0.01:
            raise ValueError(
                f"Kwota wnioskowana {self.kwota_wnioskowana:.2f} zł przekracza maksimum naboru "
                f"{self.nabor.kwota_max_zl:.2f} zł."
            )
        return self

    @property
    def vat_czynny(self) -> bool:
        return self.forma.vat == "czynny"

    def suma_zakupow_z_dotacji(self) -> float:
        return round(sum(z.kwota_do_rozliczenia(self.vat_czynny) for z in self.zakupy
                         if z.finansowanie == "dotacja"), 2)

    def dane_do_promptu(self) -> dict[str, Any]:
        """Dane dla modelu, ułożone według słownika K1–K15.

        Bez kontaktu, zabezpieczenia, grup (np. niepełnosprawność) i bez linków do ofert.
        Z danych osobowych zostaje tylko imię i miejscowość.
        """
        d = self.model_dump(mode="json", exclude_none=True)
        return {
            "K1_osoba_i_urzad": {
                "imie": self.osoba.imie,
                "miejscowosc": self.osoba.miejscowosc,
                **({"gmina": self.osoba.gmina} if self.osoba.gmina else {}),
                "urzad_pracy": self.nabor.nazwa_pup,
            },
            "K2_wyksztalcenie_kursy_uprawnienia": {
                "wyksztalcenie": d["kwalifikacje"]["wyksztalcenie"],
                "kursy": d["kwalifikacje"].get("kursy", []),
                "uprawnienia_do_dzialalnosci": self.pomysl.uprawnienia,
                "prawo_jazdy": self.lokalizacja.prawo_jazdy,
                "szkolenie_pup": self.kwalifikacje.szkolenie_pup,
                "inne_umiejetnosci": self.kwalifikacje.inne_umiejetnosci,
                "dokumenty_do_dolaczenia": self.kwalifikacje.dokumenty,
            },
            "K3_doswiadczenie": {
                "praca": d["kwalifikacje"].get("doswiadczenie", []),
                "nieformalne": self.kwalifikacje.nieformalne,
            },
            "K4_status": {"bezrobotny_od": self.bezrobotny_od, "powod_utraty_pracy": self.powod_utraty_pracy},
            "K5_dzialalnosc": {
                "opis_klienta": self.pomysl.opis,
                "uslugi_i_ceny": [
                    {k: v for k, v in u.items() if k != "czas_h"} | {"czas_jednej_uslugi_h": u["czas_h"]}
                    for u in d["uslugi"]
                ],
                "pkd": d["pomysl"].get("pkd", []),
                "forma_prawna": self.forma.forma_prawna,
                "opodatkowanie": self.forma.opodatkowanie,
                "stawka_ryczaltu": self.forma.stawka_ryczaltu,
                "vat": self.forma.vat,
                "zus": self.forma.zus,
                "ksiegowosc": self.forma.ksiegowosc,
                "data_startu": self.pomysl.data_startu.isoformat(),
                "zatrudnienie": self.zatrudnienie,
            },
            "K6_lokalizacja": d["lokalizacja"],
            "K7_klienci_i_popyt": {
                **d["klienci"],
                "listy_intencyjne": d.get("listy_intencyjne", []),
                "sezonowosc": self.pomysl.sezonowosc,
                "sezonowosc_opis": self.pomysl.sezonowosc_opis,
                "klienci_miesiecznie_m1_m6_m12": [
                    self.prognoza.klienci_m1, self.prognoza.klienci_m6, self.prognoza.klienci_m12],
            },
            "K8_konkurencja": {
                **d["konkurencja"],
                "konkurenci": [{k: v for k, v in c.items() if k != "link"}
                               for c in d["konkurencja"]["konkurenci"]],
            },
            "K9_marketing": d["marketing"],
            "K10_zakupy_i_zasoby": {
                "kosztorys": [
                    {
                        "nazwa": z.nazwa, "kategoria": z.kategoria, "stan": z.stan, "ilosc": z.ilosc,
                        "kwota_do_rozliczenia_zl": z.kwota_do_rozliczenia(self.vat_czynny),
                        "finansowanie": z.finansowanie, "sprzedawca": z.sprzedawca,
                        "uzasadnienie_klienta": z.uzasadnienie,
                    }
                    for z in self.zakupy
                ],
                "kwoty": "netto (czynny VAT)" if self.vat_czynny else "brutto (zwolnienie z VAT)",
                "zasoby_posiadane": d.get("zasoby_posiadane", []),
            },
            "K11_finanse": {
                "wklad_wlasny": d["wklad_wlasny"],
                **d["finanse_domowe"],
            },
            "K12_ryzyka": d.get("ryzyka", []),
            "K13_motywacja": self.pomysl.motywacja,
            "notatka_wlasciciela": self.notatka_wlasciciela,
        }


# --------------------------------------------------------------------------- regulamin PUP
class RegulaminPUP(BaseModel):
    """Jeden wiersz `baza-pup/regulaminy-pup-2026.csv` (kolumny wg baza-pup/SCHEMAT.md)."""

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    pup_id: str
    nazwa_pup: str
    powiat: str | None = None
    wojewodztwo: str | None = None
    miasto: str | None = None
    url_pup: str | None = None
    url_regulamin: str | None = None
    url_formularz: str | None = None
    data_regulaminu: dt.date | None = None
    kwota_max_zl: float | None = None
    zrodlo_finansowania: str | None = None
    grupy_docelowe: list[str] = Field(default_factory=list)
    nabor_ostatni_od: dt.date | None = None
    nabor_ostatni_do: dt.date | None = None
    nabor_tryb: str | None = None
    liczba_miejsc: int | None = None
    okres_prowadzenia_mies: int | None = None
    wklad_wlasny: str | None = None
    limit_reklama_pct: float | None = None
    limit_towar_pct: float | None = None
    limit_remont_pct: float | None = None
    limit_samochod_pct: float | None = None
    sprzet_uzywany: str | None = None
    zabezpieczenia: list[str] = Field(default_factory=list)
    liczba_poreczycieli: int | None = None
    dochod_poreczyciela_min_zl: float | None = None
    wykluczenia_dzialalnosci: list[str] = Field(default_factory=list)
    karta_oceny_max_pkt: float | None = None
    karta_oceny_prog_pkt: float | None = None
    kryteria_punktowane: list[str] = Field(default_factory=list)
    komisja_rozmowa: str | None = None
    wizja_lokalna: str | None = None
    termin_uzupelnien_dni: int | None = None
    uwagi: str | None = None
    zrodla: list[str] = Field(default_factory=list)
    zweryfikowano: dt.date | None = None

    @model_validator(mode="before")
    @classmethod
    def _z_csv(cls, dane: Any) -> Any:
        if not isinstance(dane, dict):
            return dane
        wynik: dict[str, Any] = {}
        listowe = {n for n, f in cls.model_fields.items() if "list" in str(f.annotation)}
        liczbowe = {n for n, f in cls.model_fields.items()
                    if str(f.annotation).startswith(("float", "int"))}
        for klucz, wartosc in dane.items():
            if klucz is None:
                continue
            if isinstance(wartosc, str):
                wartosc = wartosc.strip()
                if wartosc == "":
                    continue
                if klucz in listowe:
                    wartosc = [x.strip() for x in wartosc.split("|") if x.strip()]
                elif klucz in liczbowe:
                    wartosc = wartosc.replace(" ", "").replace(",", ".")
            wynik[klucz] = wartosc
        return wynik


def wczytaj_regulaminy(plik: Path) -> dict[str, RegulaminPUP]:
    """Wczytuje bazę regulaminów; błędny wiersz jest pomijany (z ostrzeżeniem), żeby nie blokował innych urzędów."""
    wynik: dict[str, RegulaminPUP] = {}
    with open(plik, encoding="utf-8-sig", newline="") as f:
        for nr, wiersz in enumerate(csv.DictReader(f, delimiter=";"), start=2):
            try:
                reg = RegulaminPUP.model_validate(wiersz)
            except ValueError as e:
                logging.getLogger(__name__).warning("%s, wiersz %d pominięty: %s", plik.name, nr,
                                                    "; ".join(str(b["loc"]) for b in getattr(e, "errors", lambda: [])()))
                continue
            wynik[reg.pup_id] = reg
    return wynik


# --------------------------------------------------------------------------- mapa formularza
_RE_SEKCJA = re.compile(
    r"^(0[1-9])$|^tabela:(" + "|".join(TABELE_ARKUSZA) + r")$|^dane:(" + "|".join(DANE_ARKUSZA) + r")$"
)


class PoleFormularza(BaseModel):
    """Pole wniosku PUP (szablony/10-mapowanie-pol-formularza.md)."""

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    nazwa_w_formularzu: str
    strona: int | None = None
    limit_znakow: int | None = Field(None, gt=0)
    sekcje: list[str] = Field(min_length=1)
    podzial_limitu: dict[str, float] | None = None
    format: Literal["tekst", "tabela", "4_pola", "zaznaczenie", "liczba"] = "tekst"
    uwagi: str = ""

    @model_validator(mode="before")
    @classmethod
    def _sekcja_jako_tekst(cls, dane: Any) -> Any:
        if isinstance(dane, dict) and "sekcja" in dane and "sekcje" not in dane:
            dane = {**dane, "sekcje": [dane["sekcja"]]}
        return dane

    @field_validator("sekcje")
    @classmethod
    def _sekcje(cls, v: list[str]) -> list[str]:
        zle = [s for s in v if not _RE_SEKCJA.match(s)]
        if zle:
            raise ValueError(f"nieznane sekcje {zle}; dozwolone: 01–09, tabela:<{'|'.join(TABELE_ARKUSZA)}>, "
                             f"dane:<{'|'.join(DANE_ARKUSZA)}>")
        return v

    @model_validator(mode="after")
    def _podzial(self) -> PoleFormularza:
        if self.podzial_limitu:
            if set(self.podzial_limitu) - set(self.sekcje_tekstowe):
                raise ValueError(f"pole {self.id}: podzial_limitu dotyczy sekcji spoza listy sekcje")
            if abs(sum(self.podzial_limitu.values()) - 1.0) > 0.01:
                raise ValueError(f"pole {self.id}: suma podzial_limitu musi wynosić 1,0")
        return self

    @property
    def sekcje_tekstowe(self) -> list[str]:
        return [s for s in self.sekcje if s in SEKCJE_TEKSTOWE]

    @property
    def tabele(self) -> list[str]:
        return [s.split(":", 1)[1] for s in self.sekcje if s.startswith("tabela:")]

    @property
    def dane(self) -> list[str]:
        return [s.split(":", 1)[1] for s in self.sekcje if s.startswith("dane:")]


class MapaFormularza(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    pup: str
    pup_id: str | None = None
    formularz: str
    plik_zrodlowy: str | None = None
    typ_pliku: str | None = None
    pola: list[PoleFormularza] = Field(min_length=1)
    tabele_z_arkusza: list[dict[str, Any]] = Field(default_factory=list)
    poza_zakresem: list[str] = Field(default_factory=list)
    do_wyjasnienia: list[str] = Field(default_factory=list)

    @field_validator("pola")
    @classmethod
    def _unikalne(cls, v: list[PoleFormularza]) -> list[PoleFormularza]:
        ids = [p.id for p in v]
        if len(ids) != len(set(ids)):
            raise ValueError("powtórzone id pól w mapie formularza")
        return v


# --------------------------------------------------------------------------- wynik
class Ostrzezenie(BaseModel):
    poziom: Poziom
    kategoria: str
    komunikat: str
    pole: str | None = None


class WynikPola(BaseModel):
    id: str
    nazwa_w_formularzu: str
    sekcje: list[str]
    format: str = "tekst"
    limit_znakow: int | None = None
    uwagi: str = ""
    tekst: str = ""
    tekst_ze_zmiennymi: str = ""
    liczba_znakow: int = 0
    braki: list[str] = Field(default_factory=list)
    kontrola_modelu: str = ""
    proby: int = 0
    tokeny: dict[str, int] = Field(default_factory=dict)


class WynikGeneracji(BaseModel):
    id_zlecenia: str
    imie: str
    miejscowosc: str
    pup: str
    pup_id: str | None = None
    formularz: str
    ton: Ton
    data: dt.datetime
    model: str
    tryb: Literal["dry-run", "api"]
    pola: list[WynikPola]
    ark: dict[str, str] = Field(default_factory=dict)
    ark_wartosci: dict[str, float | str | None] = Field(default_factory=dict)
    kontrole_arkusza: dict[str, float | str | None] = Field(default_factory=dict)
    ostrzezenia_finansowe: list[Ostrzezenie] = Field(default_factory=list)
    plik_arkusza: str | None = None

    def tekst_calkowity(self) -> str:
        return "\n\n".join(p.tekst for p in self.pola if p.tekst)
