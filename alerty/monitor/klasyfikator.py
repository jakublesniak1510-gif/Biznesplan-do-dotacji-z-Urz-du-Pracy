"""Reguły: czy wpis dotyczy naboru wniosków o środki na podjęcie działalności gospodarczej,
oraz wyciąganie z treści: dat naboru, trybu, kwoty, źródła finansowania, liczby miejsc, grup.

Bez modeli językowych: same wyrażenia regularne, żeby wynik był przewidywalny i testowalny.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import date, timedelta

from monitor.model import Wpis

# --------------------------------------------------------------------------------------
# Kategorie
# --------------------------------------------------------------------------------------
DOTACJA = "dotacja_dzialalnosc"  # FP / EFS+ / rezerwa: jednorazowe środki na podjęcie działalności
DOTACJA_PFRON = "dotacja_dzialalnosc_pfron"  # PFRON: środki na rozpoczęcie działalności (os. z niepełnospr.)
ZAPOWIEDZ = "zapowiedz_naboru"  # „planowany nabór”, „informacja o planowanym naborze”
ZAKONCZENIE = "zakonczenie_naboru"  # zakończenie / wstrzymanie / wyniki naboru na działalność
SPOTKANIE = "spotkanie_informacyjne"  # webinar, spotkanie, szkolenie „jak założyć firmę”
INNE_FORMY = "inne_formy_wsparcia"  # staże, bony, doposażenie, KFS, szkolenia, prace interwencyjne…
INNE = "inne"

KATEGORIE = (DOTACJA, DOTACJA_PFRON, ZAPOWIEDZ, ZAKONCZENIE, SPOTKANIE, INNE_FORMY, INNE)
KATEGORIE_ALERTU = (DOTACJA, DOTACJA_PFRON, ZAPOWIEDZ)

MIESIACE = {
    "stycznia": 1, "lutego": 2, "marca": 3, "kwietnia": 4, "maja": 5, "czerwca": 6,
    "lipca": 7, "sierpnia": 8, "września": 9, "października": 10, "listopada": 11, "grudnia": 12,
    # mianownik (zdarza się: „nabór: 3–7 listopad 2026”)
    "styczeń": 1, "luty": 2, "marzec": 3, "kwiecień": 4, "maj": 5, "czerwiec": 6,
    "lipiec": 7, "sierpień": 8, "wrzesień": 9, "październik": 10, "listopad": 11, "grudzień": 12,
}
RZYMSKIE = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7, "viii": 8,
            "ix": 9, "x": 10, "xi": 11, "xii": 12}

# --------------------------------------------------------------------------------------
# Normalizacja tekstu
# --------------------------------------------------------------------------------------
_MYSLNIKI = dict.fromkeys(map(ord, "‐‑‒–—―−"), "-")


def normalizuj(tekst: str) -> str:
    """Małe litery, jednolite myślniki i spacje, bez „r.”/„roku” po latach."""
    t = unicodedata.normalize("NFC", tekst or "")
    t = t.replace(" ", " ").replace(" ", " ").translate(_MYSLNIKI)
    t = t.lower()
    t = re.sub(r"(\d{4})\s*(?:r\.|roku\b|r\b)", r"\1", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


# --------------------------------------------------------------------------------------
# Daty
# --------------------------------------------------------------------------------------
_MIES = "|".join(sorted(MIESIACE, key=len, reverse=True))
_RZYM = r"(?:xii|xi|x|ix|viii|vii|vi|v|iv|iii|ii|i)"
# jedna data: 20.10.2026 | 20.10 | 20 października 2026 | 20 października | 20.x.2026 | 2026-10-20
DATA = (
    rf"(?:\d{{4}}-\d{{2}}-\d{{2}}"
    rf"|\d{{1,2}}\s?[./]\s?(?:\d{{1,2}}|{_RZYM})(?:\s?[./]\s?\d{{4}})?(?![\d])"
    rf"|\d{{1,2}}\s(?:{_MIES})(?:\s\d{{4}})?)"
)
_DNIA = r"(?:dnia\s|dn\.\s?)?"
_SEP = r"\s?-\s?"

WZORY_ZAKRESU = [
    # od 20.10.2026 do 24.10.2026 | od dnia 20 października do dnia 24 października 2026
    re.compile(rf"\bod\s{_DNIA}(?P<a>{DATA}).{{0,40}}?\bdo\s{_DNIA}(?P<b>{DATA})"),
    # od 3 do 7 listopada [2026]
    re.compile(rf"\bod\s{_DNIA}(?P<d1>\d{{1,2}})\sdo\s{_DNIA}(?P<d2>\d{{1,2}})\s(?P<m>{_MIES})(?:\s(?P<y>\d{{4}}))?"),
    # 3-7 listopada [2026] (np. „w dniach 3–7 listopada”)
    re.compile(rf"(?<![\d.])(?P<d1>\d{{1,2}}){_SEP}(?P<d2>\d{{1,2}})\s(?P<m>{_MIES})(?:\s(?P<y>\d{{4}}))?"),
    # 20-24.10.2026 | 20-24.10
    re.compile(rf"(?<![\d.])(?P<d1>\d{{1,2}}){_SEP}(?P<d2>\d{{1,2}})\.(?P<m>\d{{1,2}})(?:\.(?P<y>\d{{4}}))?(?![\d])"),
    # 20.10.2026 - 24.10.2026 | 20.10 - 24.10.2026
    re.compile(rf"(?P<a>{DATA}){_SEP}(?P<b>{DATA})"),
]
WZOR_OD = re.compile(rf"\b(?:od|z\sdniem|począwszy\sod)\s{_DNIA}(?P<a>{DATA})")
WZOR_DO = re.compile(rf"\bdo\s{_DNIA}(?P<b>{DATA})")
WZOR_DNIA = re.compile(rf"\b(?:w\sdniu|dnia|w\sdn\.)\s(?P<a>{DATA})")
# „Wnioski będą przyjmowane: 25 września 2026 r.”, „Termin naboru: 20.10.2026”
WZOR_PO_KLUCZU = re.compile(
    rf"(?:przyjmowane|przyjmowanie\swniosków|składanie\swniosków|termin\snaboru|termin\sskładania\swniosków|"
    rf"nab[óo]r\s(?:wniosków\s)?(?:prowadzony\sbędzie|będzie\sprowadzony|odbędzie\ssię))[:\s-]{{1,3}}"
    rf"(?:w\sdniu\s|dnia\s)?(?P<a>{DATA})(?!\s?-)"
)
KONTEKST_NABORU = re.compile(r"nab[óo]r|wnios|przyjmow|składa|termin")
WZOR_WYCZERPANIA = re.compile(
    r"do\s(?:czasu\s|momentu\s)?(?:wyczerpania|wykorzystania)\s(?:\w+\s)?(?:środków|limitu|puli|alokacji)|do\swyczerpania\b"
)
WZOR_CIAGLY = re.compile(
    r"nab[óo]r\sciągły|w\strybie\sciągłym|ciągł\w+\snab[óo]r|charakter\sotwarty|otwarty\snab[óo]r|nab[óo]r\sotwarty|"
    r"do\s(?:momentu\s)?(?:jego\s)?odwołania"
)


def _parsuj_date(s: str) -> tuple[int, int, int | None] | None:
    s = s.strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return int(m.group(3)), int(m.group(2)), int(m.group(1))
    m = re.fullmatch(rf"(\d{{1,2}})\s?[./]\s?(\d{{1,2}}|{_RZYM})(?:\s?[./]\s?(\d{{4}}))?", s)
    if m:
        mies = m.group(2)
        mies_n = int(mies) if mies.isdigit() else RZYMSKIE[mies]
        return int(m.group(1)), mies_n, int(m.group(3)) if m.group(3) else None
    m = re.fullmatch(rf"(\d{{1,2}})\s({_MIES})(?:\s(\d{{4}}))?", s)
    if m:
        return int(m.group(1)), MIESIACE[m.group(2)], int(m.group(3)) if m.group(3) else None
    return None


def _zloz(d: int, m: int, y: int | None, odniesienie: date) -> date | None:
    rok = y if y is not None else odniesienie.year
    try:
        wynik = date(rok, m, d)
    except ValueError:
        return None
    if y is None and wynik < odniesienie - timedelta(days=120):
        # ogłoszenie z grudnia o naborze w styczniu
        try:
            wynik = date(rok + 1, m, d)
        except ValueError:
            return None
    return wynik


def _zakres_z_dopasowania(m: re.Match, odn: date) -> tuple[date | None, date | None]:
    g = m.groupdict()
    if g.get("a") is not None and g.get("b") is not None:
        pa, pb = _parsuj_date(g["a"]), _parsuj_date(g["b"])
        if not pa or not pb:
            return None, None
        rok_b = pb[2] if pb[2] is not None else None
        db = _zloz(pb[0], pb[1], rok_b, odn)
        if db is None:
            return None, None
        rok_a = pa[2] if pa[2] is not None else db.year
        da = _zloz(pa[0], pa[1], rok_a, odn)
        if da and da > db and pa[2] is None:
            da = _zloz(pa[0], pa[1], db.year - 1, odn)
        return da, db
    d1, d2, mies = int(g["d1"]), int(g["d2"]), g["m"]
    mies_n = int(mies) if mies.isdigit() else MIESIACE[mies]
    rok = int(g["y"]) if g.get("y") else None
    db = _zloz(d2, mies_n, rok, odn)
    da = _zloz(d1, mies_n, db.year if db else rok, odn)
    return da, db


def wyciagnij_daty(tekst: str, odniesienie: date | None = None) -> dict:
    """Zwraca {"od": date|None, "do": date|None, "tryb": str}.

    Obsługuje m.in.: „od 20.10.2026 do 24.10.2026”, „w dniach 3–7 listopada”,
    „20-24.10.2026”, „od dnia 20 października do 24 października 2026 r.”,
    „do 24.10.2026”, „w dniu 20.10.2026”, „do wyczerpania środków”, „nabór ciągły”.
    """
    odn = odniesienie or date.today()
    t = normalizuj(tekst)
    wynik: dict = {"od": None, "do": None, "tryb": ""}

    kandydaci: list[tuple[int, int, date | None, date | None]] = []
    for prio, wzor in enumerate(WZORY_ZAKRESU):
        for m in wzor.finditer(t):
            da, db = _zakres_z_dopasowania(m, odn)
            if da and db and da <= db and (db - da).days <= 120:
                kandydaci.append((m.start(), prio, da, db))
    if kandydaci:
        # pierwszy zakres w tekście, który ma w pobliżu słowa o naborze/wnioskach; inaczej pierwszy w ogóle
        kandydaci.sort()
        wybrany = None
        for poz, _prio, da, db in kandydaci:
            if KONTEKST_NABORU.search(t[max(0, poz - 160): poz + 20]):
                wybrany = (da, db)
                break
        if wybrany is None:
            wybrany = (kandydaci[0][2], kandydaci[0][3])
        wynik["od"], wynik["do"] = wybrany
    else:
        m_dnia = next((m for m in WZOR_DNIA.finditer(t)
                       if KONTEKST_NABORU.search(t[max(0, m.start() - 160): m.end() + 160])), None)
        m_dnia = m_dnia or next(iter(WZOR_PO_KLUCZU.finditer(t)), None)
        m_od = next((m for m in WZOR_OD.finditer(t)
                     if KONTEKST_NABORU.search(t[max(0, m.start() - 160): m.start() + 10])), None)
        m_do = next((m for m in WZOR_DO.finditer(t)
                     if KONTEKST_NABORU.search(t[max(0, m.start() - 160): m.start() + 10])), None)
        if m_od:
            p = _parsuj_date(m_od.group("a"))
            wynik["od"] = _zloz(*p, odn) if p else None
        if m_do:
            p = _parsuj_date(m_do.group("b"))
            wynik["do"] = _zloz(*p, odn) if p else None
        if not m_od and not m_do and m_dnia:
            p = _parsuj_date(m_dnia.group("a"))
            d = _zloz(*p, odn) if p else None
            wynik["od"] = wynik["do"] = d
        if wynik["od"] and wynik["do"] and wynik["od"] > wynik["do"]:
            wynik["od"] = None

    if WZOR_WYCZERPANIA.search(t):
        wynik["tryb"] = "do wyczerpania środków"
    elif WZOR_CIAGLY.search(t):
        wynik["tryb"] = "ciągły"
    elif wynik["do"]:
        wynik["tryb"] = "terminowy"
    return wynik


# --------------------------------------------------------------------------------------
# Kwota, źródło, liczba miejsc, grupy
# --------------------------------------------------------------------------------------
_KWOTA = re.compile(
    r"(?P<n>\d{1,3}(?:[ .]\d{3})+|\d{4,6})(?:,\d{1,2}|,-)?\s?(?:zł\b|złotych|pln\b)"
)
_KWOTA_TYS = re.compile(r"(?P<n>\d{1,3}(?:,\d)?)\s?(?:tys\.|tysięcy|tyś\.)\s?(?:zł|złotych|pln)")
_KROTNOSC = re.compile(
    r"(?P<n>\d+(?:,\d+)?|jedno|dwu|trzy|cztero|pięcio|sześcio|siedmio|ośmio)\s?-?\s?krotn\w*\s(?:kwoty\s)?"
    r"(?:przeciętnego|przeciętnej)\s(?:miesięcznego\s)?wynagrodzeni\w*"
)
_SLOWNIE = {"jedno": "1", "dwu": "2", "trzy": "3", "cztero": "4", "pięcio": "5", "sześcio": "6",
            "siedmio": "7", "ośmio": "8"}


_KONTEKST_PULI = re.compile(
    r"(?:dysponuje|dyspozycji|rozdysponowani\w*|łączn\w*|przeznaczon\w*|pula|puli|budżet\w*|limit\w*|"
    r"na\sten\scel|na\sbieżący\snab[óo]r|alokacj\w*|kwot\w*\sśrodków|środki\sw\swysokości|wynosi\słącznie)"
    r"[^.;]{0,45}$"
)
_KONTEKST_OSOBY = re.compile(
    r"(?:maksymaln\w*|maks\.|max\.?|do\skwoty|w\swysokości\sdo|wysokości\sdo|do:|nie\s(?:więcej|wyższ\w*)\sniż|"
    r"kwot\w*\s(?:dotacji|dofinansowania|wsparcia|jednorazowego)|na\sosobę|na\sjedną\sosobę|dotacj\w*\sdo|"
    r"dofinansowani\w*\s(?:do|w\swysokości)|średni\w*\swysokość|o\sktórą\smożna)[^.;]{0,40}$"
)


def wyciagnij_kwote(tekst: str) -> tuple[int | None, str]:
    """Zwraca (kwota_max_zl na osobę, opis).

    Kwoty puli naboru („urząd dysponuje kwotą 60 000 zł”) nie są limitem na osobę: trafiają tylko do opisu.
    Kwoty spoza 5–150 tys. zł ignorujemy.
    """
    t = normalizuj(tekst)
    osoba, pula, neutralne = [], [], []
    trafienia = [(m.start(), int(re.sub(r"[ .]", "", m.group("n")))) for m in _KWOTA.finditer(t)]
    trafienia += [(m.start(), int(float(m.group("n").replace(",", ".")) * 1000)) for m in _KWOTA_TYS.finditer(t)]
    for poz, n in trafienia:
        if not 5_000 <= n <= 150_000:
            continue
        przed = t[max(0, poz - 80): poz]
        if _KONTEKST_OSOBY.search(przed):
            osoba.append(n)
        elif _KONTEKST_PULI.search(przed):
            pula.append(n)
        else:
            neutralne.append(n)
    opis = ""
    mk = _KROTNOSC.search(t)
    if mk:
        n = _SLOWNIE.get(mk.group("n"), mk.group("n"))
        opis = f"do {n}-krotności przeciętnego wynagrodzenia"
    kwota = max(osoba) if osoba else (neutralne[0] if len(set(neutralne)) == 1 else None)
    if kwota and not opis:
        opis = f"do {kwota:,} zł".replace(",", " ")
    if not opis and pula:
        opis = f"pula naboru: {max(pula):,} zł (limit na osobę w ogłoszeniu)".replace(",", " ")
    return kwota, opis


_ZRODLA = [
    ("FP", re.compile(r"funduszu?\spracy|\bfp\b|rezerw\w*\s(?:ministra|funduszu|fp)|rezerwy\sministra")),
    ("EFS+", re.compile(
        r"(?<!bez\s)efs\s?\+|(?<!bez\s)efs\splus|europejsk\w+\sfundusz\w*\sspołeczn|fundusz\w*\seuropejsk\w*\sdla|"
        r"\bfe(?:m|dkp|kp|ds|dś|dl|lu|lub|ł|łd|l|ma|mp|op|pk|pd|pm|sl|śl|sw|św|wm|wl|wp|zp)\b|program\w*\sregionaln|"
        r"projekt\w*\sunijn|fundusz\w*\seuropejsk|w\sramach\s(?:ww\.\s)?projektu|projekt\w*\s(?:pn\.|pt\.|„)"
    )),
    ("PFRON", re.compile(r"pfron|państwowego\sfunduszu\srehabilitacji")),
]


def wyciagnij_zrodla(tekst: str) -> list[str]:
    t = normalizuj(tekst)
    return [nazwa for nazwa, wzor in _ZRODLA if wzor.search(t)]


_MIEJSCA = [
    re.compile(r"liczb\w*\smiejsc\w*[:\s-]{1,3}(?:wynosi\s)?(\d{1,3})\b"),
    re.compile(r"(?:planowan|prognozowan|przewidywan)\w*\sliczb\w*\s(?:[a-ząćęłńóśźż.]+\s){0,4}?[:\s-]{1,4}(?:wynosi\s)?(?:ok\.\s?|około\s)?(\d{1,3})\b"),
    re.compile(r"liczb\w*\s(?:dotacji|dofinansowań|osób|uczestników|wniosków\sdo\srealizacji)[:\s-]{1,4}(?:wynosi\s)?(?:ok\.\s?|około\s)?(\d{1,3})\b"),
    re.compile(r"(?:dla|maksymalnie|łącznie|planuje\ssię|przewiduje\ssię|zaplanowano)\s(?:dla\s)?(\d{1,3})\s(?:osób|osoby|bezrobotnych|uczestnik\w*|wnioskodawc\w*)"),
    re.compile(r"planowan\w*\sliczb\w*\s(?:osób|uczestników|dotacji)[:\s-]{1,3}(\d{1,3})\b"),
    re.compile(r"(?:pierwszych|maksymalnie)\s(\d{1,3})\swnios\w*"),
    re.compile(r"(\d{1,3})\s(?:dotacj\w*|miejsc\w*)\b"),
]


def wyciagnij_liczbe_miejsc(tekst: str) -> int | None:
    t = normalizuj(tekst)
    for wzor in _MIEJSCA:
        m = wzor.search(t)
        if m and 1 <= int(m.group(1)) <= 500:
            return int(m.group(1))
    return None


_GRUPY = [
    ("do 30 lat", re.compile(r"do\s30\s?(?:r\.?\s?ż|roku\sżycia|lat)|poniżej\s30|18\s?-\s?29|przed\sukończeniem\s30|młodzi\w*\sdo\s30|30\sroku\sżycia")),
    ("30+", re.compile(r"powyżej\s30\s(?:r\.?\s?ż|roku|lat)|30\s?\+|30\slat\si\swięcej|30\sroku\sżycia\si\spowyżej")),
    ("50+", re.compile(r"powyżej\s50|50\s?\+|po\s50\s|50\sroku\sżycia\si\spowyżej")),
    ("kobiety", re.compile(r"\bkobiet")),
    ("długotrwale bezrobotni", re.compile(r"długotrwale\sbezrobotn")),
    ("osoby z niepełnosprawnością", re.compile(r"niepełnosprawn")),
    ("absolwenci", re.compile(r"absolwent")),
]


def wyciagnij_grupy(tekst: str) -> list[str]:
    t = normalizuj(tekst)
    return [g for g, w in _GRUPY if w.search(t)]


# --------------------------------------------------------------------------------------
# Klasyfikacja
# --------------------------------------------------------------------------------------
TEMAT = re.compile(
    r"(?:podjęci\w*|rozpoczęci\w*|założeni\w*|zakładani\w*|uruchomieni\w*|podejmowani\w*|otwarci\w*)\s"
    r"(?:i\s(?:rozw[óo]j\w*|prowadzeni\w*)\s)?(?:prowadzenia\s)?"
    r"(?:własnej\s|własnego\s|samodzielnej\s|swojej\s)?(?:działalności|działalność|firmy|biznesu)"
    r"|jednorazow\w*\s(?:\w+\s){0,2}środk\w*"
    r"|\bdotacj\w*"
    r"|(?:środk\w*|wniosk\w*|dofinansowani\w*|nab[óo]r\w*)\s(?:\w+\s){0,2}(?:na|do)\s(?:otwarci\w*\s)?(?:własn\w+\s)?działalnoś"
    r"|środk\w*\s(?:\w+\s)?na\s(?:podjęcie|rozpoczęcie|założenie|uruchomienie)"
    r"|(?:rozpocząć|założyć|załóż|otworzyć|podjąć|rozpoczynając\w*|zakładając\w*)\s(?:własn\w+\s)?(?:działalność|firmę|biznes)"
    r"|samozatrudni"
    r"|własn\w*\s(?:firm\w*|biznes\w*)\b"
)
# „szkolenie niezbędne do podjęcia pracy lub działalności gospodarczej” to nie nabór na działalność
_NIE_TEMAT = re.compile(
    r"(?:niezbędn\w*\s)?do\spodjęcia\s(?:pracy|zatrudnienia)(?:,?\s(?:lub|albo|i)\s(?:podjęcia\s|rozpoczęcia\s)?"
    r"(?:innej\spracy\szarobkowej|działalności(?:\sgospodarczej)?))*"
)
SYGNAL_NABORU = re.compile(
    r"nab[óo]r|wnios\w*|przyjmow\w*|składani\w*|zaprasz\w*|ogłasza|przyznani\w*|dofinansowani\w*|dotacj\w*|środki"
)
INFO = re.compile(
    r"spotkani|webinar|webinari|szkoleni|zajęci\w*\sz\szakresu|ośrod\w*\sdoradcz|warsztat|lunch|konsultacj|dyżur|targi|porad\w*\sgrupow|"
    r"seminari|konferencj|\bkurs\b|akademi|punkt\sinformac|jak\szałożyć|krok\spo\skroku|zaproszenie\sna|"
    r"inkubator|wydarzeni|wykład|poradnik|e-learning|szkolenie\s(?:„|\")"
)
KONIEC = re.compile(
    r"zakończ|wstrzym|zawiesz|unieważ|odwoł|wyniki|rozstrzyg|lista\srankingow|lista\srezerwow|wyczerpaniem|"
    r"rozpatrzeni\w*\swniosków|zamknięci\w*\snaboru"
)
ZAPOWIEDZ_W = re.compile(r"planowan\w*\snab|planowanym\snaborze|zapowied|przewidywan\w*\stermin|nabór\sruszy|wkrótce\snabór")
INNE_FORMY_W = re.compile(
    r"staż|\bbon\w*\b|bonu|doposażeni|wyposażeni\w*\s(?:lub\sdoposażeni\w*\s)?stanowisk|refundacj|\bkfs\b|"
    r"krajow\w*\sfundusz\w*\sszkoleniow|kształceni\w*\sustawiczn|szkoleni|prac\w*\sinterwencyjn|"
    r"robot\w*\spubliczn|prac\w*\sspołecznie|zasiedleni|voucher|pożyczk|składek|aktywizacj|\bbur\b|"
    r"usług\w*\srozwojow|studi\w*\spodyplomow|egzamin|przygotowani\w*\szawodow|oferta\spracy|giełd|"
    r"badani\w*\sankietow|barometr|cudzoziem|dofinansowani\w*\swynagrodzeni|grant\w*\sna\stelepracę|"
    r"świadczeni\w*\saktywizacyjn|zatrudnieni\w*\swspieran|zwrot\w*\skosztów|"
    r"lokaln\w*\sgrup\w*\sdziałania|\blgd\b|wsparci\w*\sw\sstarcie|pierwszy\sbiznes|działalnoś\w*\snierejestrow|"
    r"bez\srejestrowania"
)
PREFIKS_ZL = re.compile(
    r"^\s*(?P<urzad>(?:p|m|g|s|w)?up|urząd\spracy|powiatowy\surząd\spracy)\s+(?P<miasto>.+?)\s+[–\-]\s+",
    re.IGNORECASE,
)


def rozbij_tytul_zl(tytul: str) -> tuple[str, str]:
    """„PUP Tuchola – Nabór …” → („Tuchola”, „Nabór …”)."""
    tytul = tytul.replace(" ", " ")
    m = PREFIKS_ZL.match(tytul)
    if not m:
        return "", tytul.strip()
    return m.group("miasto").strip(), tytul[m.end():].strip()


def _pfron(tytul_n: str, tresc_n: str) -> bool:
    if re.search(r"pfron|niepełnospraw", tytul_n):
        return True
    return bool(re.search(r"pfron|państwowego\sfunduszu\srehabilitacji", tresc_n)) and not re.search(
        r"funduszu?\spracy|efs", tresc_n
    )


def _tylko_inne_programy(tn: str) -> bool:
    """LGD, „Pierwszy biznes – Wsparcie w starcie” (pożyczka BGK), działalność nierejestrowana: to nie dotacja PUP."""
    return bool(re.search(r"lokaln\w*\sgrup\w*\sdziałania|\blgd\b|wsparci\w*\sw\sstarcie|pierwszy\sbiznes|"
                          r"nierejestrow|bez\srejestrowania", tn))


def klasyfikuj_tekst(tytul: str, tresc: str = "") -> tuple[str, str]:
    """Zwraca (kategoria, pewność)."""
    _, tytul = rozbij_tytul_zl(tytul)
    tn, cn = _NIE_TEMAT.sub(" ", normalizuj(tytul)), _NIE_TEMAT.sub(" ", normalizuj(tresc))
    temat_t = bool(TEMAT.search(tn)) and not _tylko_inne_programy(tn)
    if temat_t:
        if KONIEC.search(tn):
            return ZAKONCZENIE, "wysoka"
        if INFO.search(tn) and not re.search(r"nab[óo]r\s(?:wniosk|na\s)", tn):
            return SPOTKANIE, "wysoka"
        if ZAPOWIEDZ_W.search(tn):
            return ZAPOWIEDZ, "wysoka"
        if re.search(r"pożyczk", tn) and not re.search(r"dotacj|jednorazow|dofinansowa|środk", tn):
            return INNE_FORMY, "wysoka"
        if SYGNAL_NABORU.search(tn) or SYGNAL_NABORU.search(cn[:400]):
            return (DOTACJA_PFRON if _pfron(tn, cn) else DOTACJA), "wysoka"
        return INNE, "niska"
    if INNE_FORMY_W.search(tn) or INFO.search(tn):
        return (INNE_FORMY if INNE_FORMY_W.search(tn) else INNE), "wysoka"
    # Tytuł ogólny („Środki z Funduszu Pracy – zaproszenie do składania wniosków”, „Ogłoszenie o naborze”)
    if SYGNAL_NABORU.search(tn) and TEMAT.search(cn):
        if KONIEC.search(tn):
            return ZAKONCZENIE, "średnia"
        if ZAPOWIEDZ_W.search(tn) or ZAPOWIEDZ_W.search(cn[:300]):
            return ZAPOWIEDZ, "średnia"
        return (DOTACJA_PFRON if _pfron(tn, cn) else DOTACJA), "średnia"
    return INNE, "wysoka" if not SYGNAL_NABORU.search(tn) else "niska"


def klasyfikuj(wpis: Wpis, odniesienie: date | None = None) -> Wpis:
    """Uzupełnia pola klasyfikacji w miejscu i zwraca wpis."""
    kat, pewnosc = klasyfikuj_tekst(wpis.tytul, wpis.tresc)
    wpis.kategoria, wpis.pewnosc = kat, pewnosc
    if kat in KATEGORIE_ALERTU or kat == ZAKONCZENIE:
        try:
            odn = date.fromisoformat(wpis.data_publikacji) if wpis.data_publikacji else odniesienie
        except ValueError:
            odn = odniesienie
        pelny = f"{rozbij_tytul_zl(wpis.tytul)[1]}. {wpis.tresc}"
        d = wyciagnij_daty(pelny, odn)
        wpis.nabor_od = d["od"].isoformat() if d["od"] else ""
        wpis.nabor_do = d["do"].isoformat() if d["do"] else ""
        wpis.tryb = d["tryb"]
        wpis.kwota_max_zl, wpis.kwota_opis = wyciagnij_kwote(pelny)
        wpis.zrodla_finansowania = wyciagnij_zrodla(pelny)
        if kat == DOTACJA_PFRON and "PFRON" not in wpis.zrodla_finansowania:
            wpis.zrodla_finansowania.append("PFRON")
        wpis.liczba_miejsc = wyciagnij_liczbe_miejsc(pelny)
        wpis.grupy_docelowe = wyciagnij_grupy(pelny)
    return wpis


# --------------------------------------------------------------------------------------
# Status względem „dziś”
# --------------------------------------------------------------------------------------
TRWA = "trwa"
ZAPOWIEDZIANY = "zapowiedziany"
TRWA_DO_WYCZERPANIA = "trwa (do wyczerpania środków)"
DO_WERYFIKACJI = "do weryfikacji (brak dat)"
ZAKONCZONY = "zakończony"
NIEAKTUALNY = "prawdopodobnie nieaktualny"
STATUSY_AKTYWNE = (TRWA, ZAPOWIEDZIANY, TRWA_DO_WYCZERPANIA, DO_WERYFIKACJI)


def status(wpis: Wpis, dzis: date) -> str:
    if wpis.kategoria not in KATEGORIE_ALERTU:
        return ""
    pub = date.fromisoformat(wpis.data_publikacji) if wpis.data_publikacji else dzis
    if wpis.wstrzymany and wpis.wstrzymany <= dzis.isoformat():
        return ZAKONCZONY
    do = date.fromisoformat(wpis.nabor_do) if wpis.nabor_do else None
    od = date.fromisoformat(wpis.nabor_od) if wpis.nabor_od else None
    if do:
        if do < dzis:
            return ZAKONCZONY
        if od and od > dzis:
            return ZAPOWIEDZIANY
        return TRWA
    if od and od > dzis:
        return ZAPOWIEDZIANY
    if wpis.tryb in ("do wyczerpania środków", "ciągły"):
        return TRWA_DO_WYCZERPANIA if (dzis - pub).days <= 30 else NIEAKTUALNY
    if wpis.kategoria == ZAPOWIEDZ:
        return ZAPOWIEDZIANY if (dzis - pub).days <= 45 else NIEAKTUALNY
    return DO_WERYFIKACJI if (dzis - pub).days <= 10 else NIEAKTUALNY


def dni_do_konca(wpis: Wpis, dzis: date) -> int | None:
    if not wpis.nabor_do:
        return None
    return (date.fromisoformat(wpis.nabor_do) - dzis).days


def opis_terminu(wpis: Wpis, dzis: date) -> str:
    """Czytelny opis do e-maila: „zostały 3 dni”, „ostatni dzień”, „start za 5 dni”."""
    od = date.fromisoformat(wpis.nabor_od) if wpis.nabor_od else None
    dni = dni_do_konca(wpis, dzis)
    if od and od > dzis:
        za = (od - dzis).days
        return f"start za {za} {_dni(za)}" if za > 1 else "start jutro"
    if dni is None:
        return "do wyczerpania środków: liczy się kolejność" if wpis.tryb == "do wyczerpania środków" else "termin do sprawdzenia w ogłoszeniu"
    if dni < 0:
        return "nabór zakończony"
    if dni == 0:
        return "dziś ostatni dzień"
    if dni == 1:
        return "został 1 dzień (jutro ostatni dzień)"
    if dni % 10 in (2, 3, 4) and dni % 100 not in (12, 13, 14):
        return f"zostały {dni} dni"
    return f"zostało {dni} dni"


def _dni(n: int) -> str:
    return "dzień" if n == 1 else "dni"
