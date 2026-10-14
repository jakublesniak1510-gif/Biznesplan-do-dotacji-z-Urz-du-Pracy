# -*- coding: utf-8 -*-
"""
Generator arkusza model-finansowy-pup.xlsx (openpyxl).

Uruchomienie:
    python3 model-finansowy/build_model.py
Następnie przelicz formuły (LibreOffice), np. skryptem recalc.py ze skilla xlsx:
    python3 <skill>/scripts/recalc.py model-finansowy/model-finansowy-pup.xlsx

Wszystkie wyniki są FORMUŁAMI. Wartości liczbowe wpisane na sztywno to wyłącznie:
  - dane wejściowe (żółte komórki, niebieska czcionka) – przykład "fryzjerka mobilna",
  - stałe 2026 w arkuszu Stale-2026 (z linkiem do źródła).
"""
import datetime as dt
import os
import re

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model-finansowy-pup.xlsx")

# ---------------------------------------------------------------- style
FONT_NAME = "Arial"
F_BASE = Font(name=FONT_NAME, size=10)
F_BOLD = Font(name=FONT_NAME, size=10, bold=True)
F_TITLE = Font(name=FONT_NAME, size=14, bold=True)
F_SECTION = Font(name=FONT_NAME, size=11, bold=True)
F_NOTE = Font(name=FONT_NAME, size=9, italic=True, color="595959")
F_INPUT = Font(name=FONT_NAME, size=10, color="0000FF")
F_LINK = Font(name=FONT_NAME, size=10, color="008000")
F_CALC = Font(name=FONT_NAME, size=10, color="000000")
FILL_INPUT = PatternFill("solid", fgColor="FFFF00")
FILL_HEAD = PatternFill("solid", fgColor="D9E1F2")
FILL_TOTAL = PatternFill("solid", fgColor="F2F2F2")
FILL_CHECK = PatternFill("solid", fgColor="E2EFDA")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

PLN = '#,##0.00;(#,##0.00);"-"'
PLN0 = '#,##0;(#,##0);"-"'
PCT = '0.0%;(0.0%);"-"'
PCT_IN = '0.0%'
NUM = '#,##0;(#,##0);"-"'
NUM1 = '#,##0.0;(#,##0.0);"-"'
MULT = '0.00'
DATE = 'yyyy-mm-dd'
MONTH = 'mm.yyyy'

MONTH_COLS = [get_column_letter(c) for c in range(3, 15)]  # C..N
FIRST, LAST = MONTH_COLS[0], MONTH_COLS[-1]
TOTAL_COL = "O"

wb = Workbook()
NAMES = {}          # nazwa -> arkusz
INPUT_CELLS = set()  # (arkusz, adres)


def define(name, ws, addr):
    col, row = re.match(r"([A-Z]+)(\d+)", addr).groups()
    ref = f"'{ws.title}'!${col}${row}"
    wb.defined_names[name] = DefinedName(name, attr_text=ref)
    NAMES[name] = ws.title


def put(ws, addr, value, fmt=None, bold=False, inp=False, comment=None, wrap=False, align=None):
    c = ws[addr]
    c.value = value
    if fmt:
        c.number_format = fmt
    if inp:
        c.fill = FILL_INPUT
        c.font = F_INPUT
        INPUT_CELLS.add((ws.title, addr))
    elif bold:
        c.font = F_BOLD
    if comment:
        c.comment = Comment(comment, "Model PUP")
        c.comment.width = 320
        c.comment.height = 140
    if wrap or align:
        c.alignment = Alignment(wrap_text=wrap, vertical="top", horizontal=align)
    return c


def header_row(ws, row, labels, start_col=1, height=None):
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=start_col + i, value=lab)
        c.font = F_BOLD
        c.fill = FILL_HEAD
        c.border = BORDER
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    if height:
        ws.row_dimensions[row].height = height


def title(ws, text, note=None):
    ws["A1"] = text
    ws["A1"].font = F_TITLE
    if note:
        ws["A2"] = note
        ws["A2"].font = F_NOTE


def section(ws, addr, text):
    ws[addr] = text
    ws[addr].font = F_SECTION


def total_style(ws, row, c1, c2):
    for col in range(c1, c2 + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = F_BOLD
        cell.fill = FILL_TOTAL
        cell.border = BORDER


def month_header(ws, row_nr, row_date, label_nr="Miesiąc działalności", with_total=True):
    put(ws, f"A{row_nr}", label_nr, bold=True)
    put(ws, f"A{row_date}", "Miesiąc kalendarzowy", bold=True)
    for i, col in enumerate(MONTH_COLS):
        if i == 0:
            put(ws, f"{col}{row_nr}", 1, fmt="0")
        else:
            put(ws, f"{col}{row_nr}", f"={MONTH_COLS[i-1]}{row_nr}+1", fmt="0")
        put(ws, f"{col}{row_date}", f"=EDATE(DataStartu,{col}{row_nr}-1)", fmt=MONTH)
        for r in (row_nr, row_date):
            ws[f"{col}{r}"].fill = FILL_HEAD
            ws[f"{col}{r}"].font = F_BOLD
            ws[f"{col}{r}"].alignment = Alignment(horizontal="center")
    if with_total:
        put(ws, f"{TOTAL_COL}{row_nr}", "Razem 12 mies.", bold=True)
        ws[f"{TOTAL_COL}{row_nr}"].fill = FILL_HEAD
        ws[f"{TOTAL_COL}{row_date}"].fill = FILL_HEAD
    ws[f"A{row_nr}"].fill = FILL_HEAD
    ws[f"A{row_date}"].fill = FILL_HEAD
    ws[f"B{row_nr}"].fill = FILL_HEAD
    ws[f"B{row_date}"].fill = FILL_HEAD


def month_row(ws, row, label, formula_fn, fmt=PLN, total=True, bold=False, param=None,
              param_fmt=None, param_input=False, param_comment=None, label_comment=None):
    """formula_fn(col, prev_col_or_None) -> formula string for month column."""
    put(ws, f"A{row}", label, bold=bold, comment=label_comment)
    if param is not None:
        put(ws, f"B{row}", param, fmt=param_fmt, inp=param_input, comment=param_comment)
    for i, col in enumerate(MONTH_COLS):
        prev = MONTH_COLS[i - 1] if i > 0 else None
        put(ws, f"{col}{row}", formula_fn(col, prev), fmt=fmt)
    if total:
        put(ws, f"{TOTAL_COL}{row}", f"=SUM({FIRST}{row}:{LAST}{row})", fmt=fmt)
    if bold:
        total_style(ws, row, 1, 15)


def yes_no(ws, rng):
    dv = DataValidation(type="list", formula1='"TAK,NIE"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(rng)


def list_validation(ws, rng, items):
    dv = DataValidation(type="list", formula1='"' + ",".join(items) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(rng)


# =====================================================================
# 1. ZALOZENIA
# =====================================================================
ws = wb.active
ws.title = "Zalozenia"
title(ws, "Założenia modelu finansowego – wniosek o dofinansowanie z PUP",
      "Żółte komórki z niebieską czcionką = dane do wpisania. Pozostałe komórki liczą się same (formuły). "
      "Przykład: fryzjerka mobilna – DANE FIKCYJNE, do podmiany.")
header_row(ws, 3, ["Parametr", "Wartość", "Opis / skąd wziąć"])

Z = [
    # row, label, value, name, fmt, comment/description, validation
    (4, "Nazwa / branża", "Fryzjerka mobilna – przykład (dane fikcyjne)", None, None,
     "Tylko opis – nie wpływa na obliczenia.", None),
    (5, "Kwota dotacji z PUP (zł)", 26000, "Dotacja", PLN,
     "Kwota, o którą wnioskujesz. Powinna odpowiadać sumie pozycji kosztorysu finansowanych z dotacji.", None),
    (6, "Maksymalna kwota dotacji wg ogłoszenia naboru (zł)", 30000, "MaxDotacja", PLN,
     "Z ogłoszenia/regulaminu Twojego PUP (każdy urząd ustala własny limit, ustawowo do 6-krotności przeciętnego wynagrodzenia).", None),
    (7, "Wkład własny – gotówka wniesiona na start (zł)", 3000, "WkladWlasny", PLN,
     "Pieniądze własne przeznaczone na zakupy z kosztorysu (finansowanie: wkład własny) i rezerwę na start.", None),
    (8, "Data rozpoczęcia działalności", dt.date(2026, 12, 1), "DataStartu", DATE,
     "Planowana data wpisu do CEIDG (zwykle po podpisaniu umowy z PUP). Miesiąc 1 modelu = miesiąc tej daty.", None),
    (9, "Forma opodatkowania", "ryczałt", "FormaOpodatkowania", None,
     "skala / liniowy / ryczałt (wybierz z listy).", ("list", ["skala", "liniowy", "ryczałt"])),
    (10, "Stawka ryczałtu (gdy forma = ryczałt)", 0.085, "StawkaRyczaltu", PCT_IN,
     "Np. 8,5% usługi (w tym fryzjerskie), 3% handel, 5,5% roboty budowlane. Sprawdź stawkę dla swojego PKD/PKWiU.", None),
    (11, "Ulga na start (6 mies. bez składek społecznych)", "TAK", "UlgaStart", None,
     "TAK / NIE. Tylko gdy w ostatnich 60 mies. nie prowadziłeś działalności i nie zakładasz firmy u byłego pracodawcy.", ("yn",)),
    (12, "Liczba miesięcy ulgi na start", 6, "MiesUlgi", "0",
     "Ustawowo do 6 pełnych miesięcy kalendarzowych (model liczy od miesiąca 1).", None),
    (13, "Preferencyjne składki ZUS (\"mały ZUS\")", "TAK", "Preferencyjny", None,
     "TAK / NIE. Podstawa 30% płacy minimalnej przez 24 mies. po uldze na start.", ("yn",)),
    (14, "Liczba miesięcy składek preferencyjnych", 24, "MiesPref", "0",
     "Ustawowo 24 miesiące kalendarzowe.", None),
    (15, "Mały ZUS plus (opcjonalnie, po okresie preferencyjnym)", "NIE", "MalyZUS", None,
     "TAK / NIE. W pierwszych 12 mies. zwykle niedostępny (wymaga działalności w poprzednim roku i przychodu ≤ 120 000 zł). "
     "Działa w modelu tylko w miesiącach po uldze i preferencyjnym ZUS.", ("yn",)),
    (16, "Podstawa wymiaru – Mały ZUS plus (zł/mies.)", 3000, "PodstawaMZP", PLN,
     "Wpisz podstawę wyliczoną z dochodu za poprzedni rok (50% średniego miesięcznego dochodu). Model ogranicza ją do przedziału 30% płacy min. – 60% prognozowanego wynagrodzenia.", None),
    (17, "Dobrowolne ubezpieczenie chorobowe", "TAK", "Chorobowe", None,
     "TAK / NIE. Bez chorobowego nie ma zasiłku chorobowego ani macierzyńskiego z ZUS.", ("yn",)),
    (18, "Czynny podatnik VAT", "NIE", "VATczynny", None,
     "TAK / NIE. Przy zwolnieniu podmiotowym (limit 240 000 zł w 2026 r., proporcjonalnie w roku startu) wpisz NIE.", ("yn",)),
    (19, "Stawka VAT na sprzedaż (gdy czynny VAT)", 0.08, "StawkaVAT", PCT_IN,
     "Np. 8% usługi fryzjerskie, 23% większość usług. Gdy VAT = NIE, ceny w arkuszu Przychody są kwotą przychodu.", None),
    (20, "Dni robocze w miesiącu", 21, "DniRobocze", "0",
     "Ile dni w miesiącu realnie pracujesz.", None),
    (21, "Godziny pracy z klientem dziennie", 6, "GodzinyDzien", "0.0",
     "Bez czasu dojazdów i przerw – służy do kontroli obłożenia w arkuszu Przychody.", None),
    (22, "Spadek przychodów – scenariusz pesymistyczny", 0.30, "SpadekPesym", PCT_IN,
     "Standardowo 30% (wymóg wielu komisji: co jeśli przychody będą niższe).", None),
]
for row, label, val, name, fmt, desc, valid in Z:
    put(ws, f"A{row}", label)
    put(ws, f"B{row}", val, fmt=fmt, inp=True)
    put(ws, f"C{row}", desc, wrap=True)
    ws[f"C{row}"].font = F_NOTE
    if name:
        define(name, ws, f"B{row}")
    if valid:
        if valid[0] == "yn":
            yes_no(ws, f"B{row}")
        else:
            list_validation(ws, f"B{row}", valid[1])

section(ws, "A25", "Kontrole spójności (liczone automatycznie)")
header_row(ws, 26, ["Kontrola", "Wynik", "Co zrobić, gdy wynik nie jest OK"])
CHECKS = [
    (27, "Kwota dotacji ≤ maksymalna kwota z naboru",
     '=IF(Dotacja<=MaxDotacja,"OK","PRZEKROCZONO")', "Zmniejsz kwotę dotacji / kosztorys."),
    (28, "Wydatki z dotacji ≤ kwota dotacji",
     '=IF(KosztorysDotacja<=Dotacja+0.005,"OK","PRZEKROCZONO")',
     "Przenieś część pozycji na wkład własny albo usuń pozycje."),
    (29, "Kwota dotacji nierozplanowana w kosztorysie (zł)",
     '=Dotacja-KosztorysDotacja', "Komisja oczekuje, że cała dotacja jest rozpisana na pozycje."),
    (30, "Limity kategorii wg regulaminu",
     '=IF(COUNTIF(Kosztorys!$E$33:$E$37,"PRZEKROCZONY")=0,"OK","PRZEKROCZONY LIMIT")',
     "Zobacz tabelę limitów w arkuszu Kosztorys."),
    (31, "Najniższe saldo gotówki w 12 mies. – scenariusz bazowy (zł)",
     "=MIN(Prognoza!$K$5:$K$17)", "Wartość ujemna = brak płynności: zwiększ wkład własny lub obniż koszty."),
    (32, "Najniższe saldo gotówki – scenariusz pesymistyczny (zł)",
     "=MIN(Prognoza!$R$5:$R$17)", "Ujemne saldo w pesymistycznym scenariuszu opisz w sekcji 09 (plan B)."),
    (33, "Najwyższe obłożenie godzin pracy",
     "=MAX(Przychody!$C$38:$N$38)", "Powyżej 100% – plan sprzedaży jest fizycznie niewykonalny, popraw liczby."),
    (34, "Przychód vs limit zwolnienia z VAT (rok startu proporcjonalnie, rok następny)",
     "=0", "Limit w roku startu liczony proporcjonalnie do dni działalności; w roku następnym – pełny limit (dla miesięcy objętych modelem)."),
]
for row, label, f, todo in CHECKS:
    put(ws, f"A{row}", label)
    fmt = PLN if ("zł" in label) else (PCT if "obłożenie" in label else None)
    put(ws, f"B{row}", f, fmt=fmt)
    ws[f"B{row}"].fill = FILL_CHECK
    put(ws, f"C{row}", todo, wrap=True)
    ws[f"C{row}"].font = F_NOTE

ws.column_dimensions["A"].width = 52
ws.column_dimensions["B"].width = 30
ws.column_dimensions["C"].width = 95

# =====================================================================
# 2. STALE-2026
# =====================================================================
st = wb.create_sheet("Stale-2026")
title(st, "Stałe prawne i parametry na 2026 r.",
      "Weryfikacja: 14.10.2026. Kolumna F: 'zweryfikowano' = potwierdzone w podanym źródle; '[do weryfikacji]' = nie potwierdzono "
      "w tej sesji – sprawdź przed użyciem. Od 01.01.2027 kwoty się zmienią (płaca minimalna, podstawy ZUS, od 02.2027 składka zdrowotna).")
header_row(st, 4, ["Parametr", "Wartość", "Jednostka", "Źródło (link)", "Akt / data źródła", "Status", "Uwagi"], height=30)

L_DZU = "https://dziennikustaw.gov.pl/D2025000124201.pdf"
L_MP = "https://monitorpolski.gov.pl/M2025000120601.pdf"
L_GUS4 = ("https://stat.gov.pl/sygnalne/komunikaty-i-obwieszczenia/lista-komunikatow-i-obwieszczen/"
          "obwieszczenie-w-sprawie-przecietnego-miesiecznego-wynagrodzenia-w-sektorze-przedsiebiorstw-"
          "wlacznie-z-wyplatami-z-zysku-w-czwartym-kwartale-2025-r-,58,49.html")
L_ZL = "https://zielonalinia.gov.pl/stawki-zus-dla-przedsiebiorcow-46392/"
L_INEWI = "https://inewi.pl/blog/skladki-zus-dla-przedsiebiorcow-ile-wyniosa"
L_INFAKT = "https://www.infakt.pl/blog/?p=81462"
L_WYP = "https://poradnikprzedsiebiorcy.pl/-skladka-wypadkowa-jak-ustalic-wlasciwa-stope-procentowa"
L_PIT = "https://poradnikprzedsiebiorcy.pl/-skala-podatkowa-nowy-prog-podatkowy-i-kwota-wolna"
L_VAT = ("https://www.podatki.biz/artykuly/nowy-limit-zwolnienia-podmiotowego-z-vat-w-2026-r-mf-o-"
         "przepisach-przejsciowych_4_60302.htm")
L_VAT8 = "https://www.podatki.biz/artykuly/obnizona-stawka-vat-w-2024-r-8-takze-dla-uslug-kosmetycznych_4_54561.htm"
L_RYCZ = "https://firmove.pl/aktualnosci/finanse/podatki/ryczalt-a-uslugi-fryzjerskie-wszystko-co-warto-wiedziec"
L_ULGA = "https://sum.money/pl/zus-jdg-ulga-na-start/"
L_MP720 = "https://eli.gov.pl/eli/MP/2026/720/ogl/pol/pdf"

OK = "zweryfikowano"
DW = "[do weryfikacji]"

S = [
    ("sec", "A. Wynagrodzenia (podstawy do składek)"),
    ("PlacaMin", "Minimalne wynagrodzenie 2026", 4806, "zł/mies.", L_DZU,
     "Rozp. RM z 11.09.2025, Dz.U. 2025 poz. 1242", OK, "Tekst rozporządzenia sprawdzony w PDF Dz.U.", PLN),
    ("PrognozaWyn", "Prognozowane przeciętne wynagrodzenie 2026", 9420, "zł/mies.", L_MP,
     "Obwieszczenie MRPiPS z 19.11.2025, M.P. 2025 poz. 1206", OK, "Tekst obwieszczenia sprawdzony w PDF M.P.", PLN),
    ("WynIVkw", "Przeciętne wynagrodzenie w sektorze przedsiębiorstw z wypłatami z zysku, IV kw. 2025", 9228.64,
     "zł/mies.", L_GUS4, "Obwieszczenie Prezesa GUS z 22.01.2026", OK,
     "Podstawa składki zdrowotnej na ryczałcie od 02.2026 do 01.2027. Potwierdzone też: infakt.pl (22.01.2026).", PLN),
    ("sec", "B. Składki na ubezpieczenia społeczne"),
    ("PodstPelna", "Podstawa wymiaru – pełny ZUS (60% prognozowanego wynagrodzenia)", "=ROUND(0.6*PrognozaWyn,2)",
     "zł/mies.", L_ZL, "art. 18 ust. 8 ustawy o s.u.s.", OK, "Wynik: 5 652,00 zł; zielonalinia.gov.pl (stan na 29.05.2026)", PLN),
    ("PodstPref", "Podstawa wymiaru – preferencyjny ZUS (30% płacy minimalnej)", "=ROUND(0.3*PlacaMin,2)",
     "zł/mies.", L_ZL, "art. 18a ustawy o s.u.s.", OK, "Wynik: 1 441,80 zł", PLN),
    ("StEmer", "Stopa składki emerytalnej", 0.1952, "%", L_ZL, "ustawa o s.u.s.", OK, "", '0.00%'),
    ("StRent", "Stopa składki rentowej", 0.08, "%", L_ZL, "ustawa o s.u.s.", OK, "", '0.00%'),
    ("StChor", "Stopa składki chorobowej (dobrowolna)", 0.0245, "%", L_ZL, "ustawa o s.u.s.", OK, "", '0.00%'),
    ("StWyp", "Stopa składki wypadkowej (płatnik do 9 ubezpieczonych)", 0.0167, "%", L_WYP,
     "rok składkowy 04.2026–03.2027", OK, "Stopa 50% najwyższej (3,33%). ZUS ustala ją sam dla małych płatników.", '0.00%'),
    ("StFP", "Fundusz Pracy + Fundusz Solidarnościowy", 0.0245, "%", L_ZL, "ustawa o promocji zatrudnienia",
     OK, "Nie opłaca się, gdy podstawa < minimalne wynagrodzenie (np. preferencyjny ZUS).", '0.00%'),
    ("ZUSPelnyEmer", "Pełny ZUS – składka emerytalna", "=ROUND(PodstPelna*StEmer,2)", "zł/mies.", L_INEWI,
     "wyliczenie", OK, "1 103,27 zł", PLN),
    ("ZUSPelnyRent", "Pełny ZUS – składka rentowa", "=ROUND(PodstPelna*StRent,2)", "zł/mies.", L_INEWI,
     "wyliczenie", OK, "452,16 zł", PLN),
    ("ZUSPelnyChor", "Pełny ZUS – składka chorobowa", "=ROUND(PodstPelna*StChor,2)", "zł/mies.", L_INEWI,
     "wyliczenie", OK, "138,47 zł", PLN),
    ("ZUSPelnyWyp", "Pełny ZUS – składka wypadkowa", "=ROUND(PodstPelna*StWyp,2)", "zł/mies.", L_INEWI,
     "wyliczenie", OK, "94,39 zł", PLN),
    ("ZUSPelnyFP", "Pełny ZUS – FP + FS", "=ROUND(PodstPelna*StFP,2)", "zł/mies.", L_INEWI,
     "wyliczenie", OK, "138,47 zł", PLN),
    ("ZUSPelnySuma", "Pełny ZUS – razem społeczne z chorobowym i FP", "=ZUSPelnyEmer+ZUSPelnyRent+ZUSPelnyChor+ZUSPelnyWyp+ZUSPelnyFP",
     "zł/mies.", L_INEWI, "wyliczenie", OK, "1 926,76 zł (bez chorobowego 1 788,29 zł)", PLN),
    ("ZUSPrefSuma", "Preferencyjny ZUS – razem społeczne z chorobowym",
     "=ROUND(PodstPref*StEmer,2)+ROUND(PodstPref*StRent,2)+ROUND(PodstPref*StChor,2)+ROUND(PodstPref*StWyp,2)",
     "zł/mies.", L_INEWI, "wyliczenie", OK, "456,18 zł (bez chorobowego 420,86 zł); bez FP", PLN),
    ("sec", "C. Składka zdrowotna (rok składkowy 02.2026–01.2027)"),
    ("ZdrSkala", "Składka zdrowotna – skala podatkowa (% dochodu)", 0.09, "%", L_INFAKT,
     "ustawa o świadczeniach opieki zdrowotnej", OK, "Brak odliczenia od podatku na skali.", '0.0%'),
    ("ZdrLin", "Składka zdrowotna – podatek liniowy (% dochodu)", 0.049, "%", L_INEWI,
     "ustawa o świadczeniach opieki zdrowotnej", OK, "", '0.0%'),
    ("ZdrMinPodst", "Minimalna podstawa składki zdrowotnej (skala, liniowy) = 100% płacy minimalnej", "=PlacaMin",
     "zł/mies.", L_INFAKT, "od 01.02.2026 (w 2025: 75%)", OK,
     "Ustawa przedłużająca obniżoną podstawę 75% nie weszła w życie (weto).", PLN),
    ("ZdrMin", "Minimalna składka zdrowotna (skala, liniowy)", "=ROUND(0.09*ZdrMinPodst,2)", "zł/mies.", L_INFAKT,
     "wyliczenie", OK, "432,54 zł. Za styczeń 2026 obowiązywały jeszcze kwoty z 2025 r.", PLN),
    ("LimitZdrLin", "Roczny limit odliczenia składki zdrowotnej – liniowy", 14100, "zł/rok", L_INFAKT,
     "2026", OK, "Potwierdzone w 2 źródłach wtórnych (infakt, zestawienia 2026); brak tekstu obwieszczenia MF w tej sesji.", PLN),
    ("RyczProg1", "Ryczałt – próg przychodu rocznego 1", 60000, "zł/rok", L_INFAKT, "ustawa o świad. opieki zdr.",
     OK, "", PLN),
    ("RyczProg2", "Ryczałt – próg przychodu rocznego 2", 300000, "zł/rok", L_INFAKT, "ustawa o świad. opieki zdr.",
     OK, "", PLN),
    ("ZdrRycz1", "Ryczałt – składka zdrowotna przy przychodzie ≤ 60 000 zł (9% × 60% WynIVkw)",
     "=ROUND(0.09*0.6*WynIVkw,2)", "zł/mies.", L_INEWI, "wyliczenie", OK, "498,35 zł", PLN),
    ("ZdrRycz2", "Ryczałt – składka zdrowotna przy przychodzie 60 000–300 000 zł (9% × 100%)",
     "=ROUND(0.09*WynIVkw,2)", "zł/mies.", L_INEWI, "wyliczenie", OK, "830,58 zł", PLN),
    ("ZdrRycz3", "Ryczałt – składka zdrowotna przy przychodzie > 300 000 zł (9% × 180%)",
     "=ROUND(0.09*1.8*WynIVkw,2)", "zł/mies.", L_INEWI, "wyliczenie", OK, "1 495,04 zł", PLN),
    ("RyczOdlicz", "Ryczałt – część zapłaconej składki zdrowotnej odliczana od przychodu", 0.5, "%", L_ULGA,
     "ustawa o ryczałcie", OK, "Źródło wtórne (zasady Polskiego Ładu, bez zmian w 2026).", '0%'),
    ("sec", "D. Podatek dochodowy"),
    ("KwotaWolna", "Kwota wolna od podatku (skala)", 30000, "zł/rok", L_PIT, "ustawa o PIT, art. 27", OK, "", PLN),
    ("ProgPod", "Próg podatkowy (skala)", 120000, "zł/rok", L_PIT, "ustawa o PIT, art. 27", OK, "", PLN),
    ("Stawka1", "Stawka podatku – I próg skali", 0.12, "%", L_PIT, "ustawa o PIT, art. 27", OK, "", '0%'),
    ("Stawka2", "Stawka podatku – II próg skali", 0.32, "%", L_PIT, "ustawa o PIT, art. 27", OK, "", '0%'),
    ("KwotaZmn", "Kwota zmniejszająca podatek (12% × kwota wolna)", "=KwotaWolna*Stawka1", "zł/rok", L_PIT,
     "wyliczenie", OK, "3 600 zł", PLN),
    ("StLiniowy", "Podatek liniowy", 0.19, "%", L_PIT, "ustawa o PIT, art. 30c", OK, "Bez kwoty wolnej.", '0%'),
    ("RyczFryz", "Ryczałt – usługi fryzjerskie (stawka referencyjna dla przykładu)", 0.085, "%", L_RYCZ,
     "ustawa o ryczałcie, art. 12", OK,
     "Stawkę używaną w obliczeniach wpisujesz w Zalozenia!B10. " + DW +
     ": przy przychodach z usług > 100 000 zł/rok nadwyżka może podlegać stawce 12,5% – model tego nie liczy.", '0.0%'),
    ("sec", "E. VAT i inne"),
    ("LimitVAT", "Limit zwolnienia podmiotowego z VAT", 240000, "zł/rok", L_VAT,
     "art. 113 ustawy o VAT, nowelizacja z 24.06.2025, od 01.01.2026", OK, "W roku rozpoczęcia – proporcjonalnie do okresu działalności.", PLN),
    ("VATFryz", "Stawka VAT – usługi fryzjerskie", 0.08, "%", L_VAT8, "rozporządzenie MF – stawki obniżone", OK,
     "Istotne tylko dla czynnego podatnika VAT.", '0%'),
    ("WynIIkw26", "Przeciętne wynagrodzenie w sekt. przedsiębiorstw z wypł. z zysku, II kw. 2026 (informacyjnie)",
     9396.33, "zł/mies.", L_MP720, "Obwieszczenie Prezesa GUS z 20.07.2026, M.P. 2026 poz. 720", OK,
     "Nie używane w obliczeniach – orientacyjnie do porównań.", PLN),
    ("UlgaMax", "Ulga na start – maksymalna liczba miesięcy", 6, "mies.", L_ULGA, "art. 18 ust. 1 Prawa przedsiębiorców",
     OK, "Zwalnia ze składek społecznych i FP; zdrowotną płaci się.", "0"),
    ("PrefMax", "Preferencyjne składki – liczba miesięcy", 24, "mies.", L_ULGA, "art. 18a ustawy o s.u.s.", OK, "", "0"),
    ("MZPLimit", "Mały ZUS plus – limit przychodu z poprzedniego roku", 120000, "zł/rok", L_INEWI,
     "art. 18c ustawy o s.u.s.", DW,
     "Warunki (m.in. 60 dni działalności w poprzednim roku, 36 mies. w okresie 60 mies., podstawa = 50% średniego dochodu) – nie potwierdzono w źródle pierwotnym w tej sesji.", PLN),
    ("DotacjaPIT", "Dotacja z PUP zwolniona z podatku dochodowego", "TAK", "", "",
     "art. 21 ust. 1 pkt 121 ustawy o PIT", DW,
     "Wiedza ogólna – nie potwierdzono w tej sesji. Skutek: wydatki sfinansowane dotacją (w tym amortyzacja) nie są kosztem podatkowym – model nie ujmuje zakupów w kosztach.", None),
    ("DotacjaMax", "Maksymalna kwota dofinansowania – reguła ustawowa", "do 6 × przeciętne wynagrodzenie", "", "",
     "ustawa z 20.03.2025 o rynku pracy i służbach zatrudnienia", DW,
     "Faktyczny limit ustala każdy PUP w naborze (przykłady 2026: 25–40 tys. zł) – wpisz w Zalozenia!B6.", None),
]
r = 5
for item in S:
    if item[0] == "sec":
        section(st, f"A{r}", item[1])
        r += 1
        continue
    name, label, val, unit, link, act, status, note, fmt = item
    put(st, f"A{r}", label, wrap=True)
    is_formula = isinstance(val, str) and val.startswith("=")
    put(st, f"B{r}", val, fmt=fmt)
    if not is_formula and isinstance(val, (int, float)):
        st[f"B{r}"].font = F_INPUT
        INPUT_CELLS.add((st.title, f"B{r}"))
    put(st, f"C{r}", unit)
    if link:
        put(st, f"D{r}", link)
        st[f"D{r}"].hyperlink = link
        st[f"D{r}"].font = Font(name=FONT_NAME, size=9, color="0563C1", underline="single")
    put(st, f"E{r}", act, wrap=True)
    put(st, f"F{r}", status)
    st[f"F{r}"].font = Font(name=FONT_NAME, size=10, bold=True,
                            color=("008000" if status == OK else "C00000"))
    put(st, f"G{r}", note, wrap=True)
    if status == DW:
        st[f"B{r}"].comment = Comment(f"{DW}: {note}", "Model PUP")
        st[f"B{r}"].comment.width = 320
        st[f"B{r}"].comment.height = 120
    else:
        st[f"B{r}"].comment = Comment(f"Źródło: {act}. {link}. Sprawdzono 14.10.2026.", "Model PUP")
        st[f"B{r}"].comment.width = 320
        st[f"B{r}"].comment.height = 100
    if name:
        define(name, st, f"B{r}")
    r += 1
for col, w in zip("ABCDEFG", [62, 18, 10, 48, 36, 17, 70]):
    st.column_dimensions[col].width = w

# =====================================================================
# 3. KOSZTORYS
# =====================================================================
ks = wb.create_sheet("Kosztorys")
title(ks, "Kosztorys zakupów (specyfikacja wydatków)",
      "Wpisuj pozycje w wierszach 5–24 (żółte). Kwota do rozliczenia: netto u czynnego podatnika VAT, brutto u zwolnionego z VAT. "
      "Linki do ofert – wklej prawdziwe oferty (urząd często ich żąda).")
KH = ["Lp.", "Nazwa pozycji", "Kategoria", "Nowy / używany", "Ilość", "Cena jedn. netto (zł)", "Wartość netto (zł)",
      "Stawka VAT", "Kwota VAT (zł)", "Wartość brutto (zł)", "Kwota do rozliczenia (zł)", "Źródło oferty (link)",
      "Finansowanie", "Limit kategorii wg regulaminu %", "Przekroczenie limitu?"]
header_row(ks, 4, KH, height=45)
OFERTA = "[przykład – wklej link do konkretnej oferty]"
ITEMS = [
    ("Fotel fryzjerski mobilny, składany", "sprzęt", "nowy", 1, 650, 0.23, "dotacja"),
    ("Przenośna myjka do włosów z podgrzewaniem wody", "sprzęt", "nowy", 1, 1200, 0.23, "dotacja"),
    ("Suszarka profesjonalna 2000 W", "sprzęt", "nowy", 2, 450, 0.23, "dotacja"),
    ("Prostownica i lokówka profesjonalna (zestaw)", "sprzęt", "nowy", 1, 700, 0.23, "dotacja"),
    ("Maszynka bezprzewodowa + trymer", "sprzęt", "nowy", 1, 1100, 0.23, "dotacja"),
    ("Nożyczki fryzjerskie: proste + degażówki", "sprzęt", "nowy", 1, 1800, 0.23, "dotacja"),
    ("Sterylizator UV i kuweta do dezynfekcji narzędzi", "sprzęt", "nowy", 1, 900, 0.23, "dotacja"),
    ("Climazon przenośny (używany, od osoby prywatnej)", "sprzęt", "używany", 1, 1500, 0, "dotacja"),
    ("Walizka na kółkach i organizery na narzędzia", "sprzęt", "nowy", 1, 600, 0.23, "dotacja"),
    ("Kasa fiskalna online", "sprzęt", "nowy", 1, 1800, 0.23, "dotacja"),
    ("Lampa LED akumulatorowa do pracy u klienta", "sprzęt", "nowy", 1, 265, 0.23, "dotacja"),
    ("Peleryny, ręczniki, szczotki, grzebienie, klipsy", "inne", "nowy", 1, 1200, 0.23, "dotacja"),
    ("Pierwszy zapas farb, oksydantów i kosmetyków", "towar", "nowy", 1, 5000, 0.23, "dotacja"),
    ("Oklejenie samochodu folią z logo i telefonem", "reklama", "nowy", 1, 1800, 0.23, "dotacja"),
    ("Logo i strona www z rezerwacją online", "reklama", "nowy", 1, 2000, 0.23, "dotacja"),
    ("Tablet do kalendarza wizyt i portfolio", "sprzęt", "nowy", 1, 1400, 0.23, "wkład własny"),
    ("Ulotki, wizytówki, karty stałego klienta", "reklama", "nowy", 1, 500, 0.23, "wkład własny"),
]
K_FIRST, K_LAST = 5, 24
CAT_FIRST, CAT_LAST = 33, 37
for i in range(K_FIRST, K_LAST + 1):
    idx = i - K_FIRST
    put(ks, f"A{i}", idx + 1, fmt="0")
    data = ITEMS[idx] if idx < len(ITEMS) else (None, None, None, None, None, None, None)
    name, cat, cond, qty, price, vat, fin = data
    put(ks, f"B{i}", name, inp=True)
    put(ks, f"C{i}", cat, inp=True)
    put(ks, f"D{i}", cond, inp=True)
    put(ks, f"E{i}", qty, fmt="0", inp=True)
    put(ks, f"F{i}", price, fmt=PLN, inp=True)
    put(ks, f"G{i}", f"=E{i}*F{i}", fmt=PLN)
    put(ks, f"H{i}", vat, fmt='0%', inp=True)
    put(ks, f"I{i}", f"=ROUND(G{i}*H{i},2)", fmt=PLN)
    put(ks, f"J{i}", f"=G{i}+I{i}", fmt=PLN)
    put(ks, f"K{i}", f'=IF(VATczynny="TAK",G{i},J{i})', fmt=PLN)
    put(ks, f"L{i}", OFERTA if name else None, inp=True)
    put(ks, f"M{i}", fin, inp=True)
    put(ks, f"N{i}", f'=IF(C{i}="","",IFERROR(VLOOKUP(C{i},$A${CAT_FIRST}:$B${CAT_LAST},2,FALSE),"brak kategorii"))', fmt='0%')
    put(ks, f"O{i}", f'=IF(C{i}="","",IFERROR(VLOOKUP(C{i},$A${CAT_FIRST}:$E${CAT_LAST},5,FALSE),"brak kategorii"))')
    for col in "ABCDEFGHIJKLMNO":
        ks[f"{col}{i}"].border = BORDER
ks[f"H{K_FIRST+7}"].comment = Comment("Zakup od osoby prywatnej – bez VAT. Kupujący płaci 2% PCC od wartości > 1000 zł "
                                      "(tu 30 zł – poza dotacją). Wymagana umowa kupna-sprzedaży i zwykle oświadczenie, "
                                      "że sprzęt nie był kupiony ze środków publicznych w ostatnich 7 latach.", "Model PUP")
list_validation(ks, f"C{K_FIRST}:C{K_LAST}", ["sprzęt", "towar", "reklama", "remont", "inne"])
list_validation(ks, f"D{K_FIRST}:D{K_LAST}", ["nowy", "używany"])
list_validation(ks, f"M{K_FIRST}:M{K_LAST}", ["dotacja", "wkład własny"])

R_SUM = 25
put(ks, f"B{R_SUM}", "RAZEM", bold=True)
for col in "GIJK":
    put(ks, f"{col}{R_SUM}", f"=SUM({col}{K_FIRST}:{col}{K_LAST})", fmt=PLN)
total_style(ks, R_SUM, 1, 15)
put(ks, f"B{R_SUM+1}", "w tym finansowane z dotacji")
for col in "GIJK":
    put(ks, f"{col}{R_SUM+1}", f'=SUMIFS({col}{K_FIRST}:{col}{K_LAST},$M${K_FIRST}:$M${K_LAST},"dotacja")', fmt=PLN)
put(ks, f"B{R_SUM+2}", "w tym finansowane z wkładu własnego")
for col in "GIJK":
    put(ks, f"{col}{R_SUM+2}", f'=SUMIFS({col}{K_FIRST}:{col}{K_LAST},$M${K_FIRST}:$M${K_LAST},"wkład własny")', fmt=PLN)
put(ks, f"B{R_SUM+3}", "Kwota dotacji (z arkusza Zalozenia)")
put(ks, f"K{R_SUM+3}", "=Dotacja", fmt=PLN)
put(ks, f"B{R_SUM+4}", "Pozostało do rozplanowania z dotacji (ujemne = przekroczenie)")
put(ks, f"K{R_SUM+4}", f"=K{R_SUM+3}-K{R_SUM+1}", fmt=PLN)
put(ks, f"L{R_SUM+4}", f'=IF(K{R_SUM+4}<-0.005,"PRZEKROCZONO KWOTĘ DOTACJI",IF(K{R_SUM+4}>0.005,"Dotacja nie w pełni rozplanowana","OK – dotacja rozplanowana"))')
ks[f"L{R_SUM+4}"].font = F_BOLD
define("KosztorysDotacja", ks, f"K{R_SUM+1}")
define("KosztorysWklad", ks, f"K{R_SUM+2}")
define("KosztorysRazem", ks, f"K{R_SUM}")

section(ks, "A31", "Limity kategorii wg regulaminu PUP (udział w kwocie dotacji)")
header_row(ks, 32, ["Kategoria", "Limit wg regulaminu %", "Suma z dotacji (zł)", "Udział w kwocie dotacji", "Status"], height=30)
CATS = [("sprzęt", 1.0), ("towar", 0.30), ("reklama", 0.20), ("remont", 0.20), ("inne", 0.10)]
for j, (cat, lim) in enumerate(CATS):
    rr = CAT_FIRST + j
    put(ks, f"A{rr}", cat)
    put(ks, f"B{rr}", lim, fmt='0%', inp=True,
        comment="Przykładowy limit – sprawdź regulamin swojego PUP i wpisz właściwy." if j == 0 else None)
    put(ks, f"C{rr}", f'=SUMIFS($K${K_FIRST}:$K${K_LAST},$C${K_FIRST}:$C${K_LAST},A{rr},$M${K_FIRST}:$M${K_LAST},"dotacja")', fmt=PLN)
    put(ks, f"D{rr}", f"=IF(Dotacja>0,C{rr}/Dotacja,0)", fmt=PCT)
    put(ks, f"E{rr}", f'=IF(D{rr}>B{rr}+0.00001,"PRZEKROCZONY","OK")')
    for col in "ABCDE":
        ks[f"{col}{rr}"].border = BORDER
put(ks, f"A{CAT_LAST+1}", "Razem", bold=True)
put(ks, f"C{CAT_LAST+1}", f"=SUM(C{CAT_FIRST}:C{CAT_LAST})", fmt=PLN)
put(ks, f"D{CAT_LAST+1}", f"=SUM(D{CAT_FIRST}:D{CAT_LAST})", fmt=PCT)
total_style(ks, CAT_LAST + 1, 1, 5)
put(ks, f"A{CAT_LAST+2}", "Kontrola: suma kategorii = suma z dotacji")
put(ks, f"C{CAT_LAST+2}", f'=IF(ABS(C{CAT_LAST+1}-K{R_SUM+1})<0.01,"OK","SPRAWDŹ KATEGORIE (puste/nieznane)")')
for col, w in zip("ABCDEFGHIJKLMNO", [6, 46, 12, 12, 7, 14, 14, 9, 12, 14, 15, 40, 14, 14, 15]):
    ks.column_dimensions[col].width = w
ks.column_dimensions["A"].width = 16
ks.freeze_panes = "C5"

# =====================================================================
# 4. PRZYCHODY
# =====================================================================
pr = wb.create_sheet("Przychody")
title(pr, "Prognoza przychodów – 12 miesięcy",
      "Sprzedaż = liczba sprzedaży przy pełnym obłożeniu × współczynnik rozruchu × mnożnik sezonowy (zaokrąglone do całych sztuk). "
      "Ceny: kwota płacona przez klienta (u czynnego VAT-owca model odejmuje VAT).")
section(pr, "A4", "A. Linie usług / produktów (maks. 5)")
header_row(pr, 5, ["Nazwa usługi / produktu", "Cena dla klienta (zł)", "Liczba sprzedaży / mies. (pełne obłożenie)",
                   "Czas 1 usługi (h)", "Przychód z 1 sprzedaży (zł, netto)"], height=45)
LINES = [
    ("Strzyżenie damskie z modelowaniem", 80, 30, 1.0),
    ("Strzyżenie męskie i dziecięce", 45, 30, 0.5),
    ("Koloryzacja (z materiałem)", 200, 12, 2.5),
    ("Upięcie okolicznościowe / ślubne", 220, 5, 1.5),
    ("Strzyżenie seniorów w DPS (umowa)", 40, 20, 0.5),
]
L_FIRST = 6
for j, (nm, price, qty, hrs) in enumerate(LINES):
    rr = L_FIRST + j
    put(pr, f"A{rr}", nm, inp=True)
    put(pr, f"B{rr}", price, fmt=PLN, inp=True)
    put(pr, f"C{rr}", qty, fmt="0", inp=True)
    put(pr, f"D{rr}", hrs, fmt="0.0", inp=True)
    put(pr, f"E{rr}", f'=IF(VATczynny="TAK",ROUND(B{rr}/(1+StawkaVAT),2),B{rr})', fmt=PLN)
L_LAST = L_FIRST + 4

section(pr, "A12", "B. Sezonowość wg miesiąca kalendarzowego (1,00 = przeciętny miesiąc)")
put(pr, "A13", "Miesiąc kalendarzowy", bold=True)
put(pr, "A14", "Mnożnik sezonowy", bold=True)
CAL = ["sty", "lut", "mar", "kwi", "maj", "cze", "lip", "sie", "wrz", "paź", "lis", "gru"]
SEAS = [0.85, 0.85, 0.95, 1.05, 1.10, 1.15, 1.00, 0.95, 1.05, 0.95, 0.95, 1.15]
for i, col in enumerate(MONTH_COLS):
    put(pr, f"{col}13", CAL[i], bold=True)
    pr[f"{col}13"].fill = FILL_HEAD
    pr[f"{col}13"].alignment = Alignment(horizontal="center")
    put(pr, f"{col}14", SEAS[i], fmt=MULT, inp=True)
pr["A13"].fill = FILL_HEAD
put(pr, "O14", "=AVERAGE(C14:N14)", fmt=MULT)
put(pr, "O13", "średnia", bold=True)
pr["C14"].comment = Comment("Przykład fryzjerki: szczyt w grudniu (święta, sylwester), maj–czerwiec (śluby, komunie), "
                            "dołek w styczniu–lutym. Średnia powinna być bliska 1,00.", "Model PUP")

section(pr, "A16", "C. Prognoza miesięczna")
month_header(pr, 17, 18)
RZ = [0.40, 0.60, 0.80] + [1.0] * 9
put(pr, "A19", "Współczynnik rozruchu", bold=True,
    comment="Edytowalny: jaki % docelowej sprzedaży osiągniesz w danym miesiącu działalności (m1 40%, m2 60%, m3 80%, od m4 100%).")
for i, col in enumerate(MONTH_COLS):
    put(pr, f"{col}19", RZ[i], fmt=PCT_IN, inp=True)
month_row(pr, 20, "Mnożnik sezonowy (z tabeli B)",
          lambda c, p: f"=INDEX($C$14:$N$14,MONTH({c}$18))", fmt=MULT, total=False)
put(pr, "A21", "Liczba sprzedaży (szt. / usług)", bold=True)
Q_FIRST = 22
for j in range(5):
    rr = Q_FIRST + j
    lr = L_FIRST + j
    month_row(pr, rr, f"=A{lr}", lambda c, p, lr=lr: f"=ROUND($C{lr}*{c}$19*{c}$20,0)", fmt=NUM)
put(pr, "A27", "Przychód netto (zł)", bold=True)
P_FIRST = 28
for j in range(5):
    rr = P_FIRST + j
    month_row(pr, rr, f"=A{L_FIRST+j}", lambda c, p, j=j: f"={c}{Q_FIRST+j}*$E${L_FIRST+j}", fmt=PLN)
R_PRZ = 33
month_row(pr, R_PRZ, "PRZYCHÓD RAZEM (zł)", lambda c, p: f"=SUM({c}{P_FIRST}:{c}{P_FIRST+4})", bold=True)
month_row(pr, 34, "Liczba sprzedaży razem", lambda c, p: f"=SUM({c}{Q_FIRST}:{c}{Q_FIRST+4})", fmt=NUM)
section(pr, "A35", "D. Kontrola wykonalności (obłożenie czasu pracy)")
month_row(pr, 36, "Godziny pracy z klientami", lambda c, p: f"=SUMPRODUCT($D${L_FIRST}:$D${L_LAST},{c}{Q_FIRST}:{c}{Q_FIRST+4})", fmt=NUM1)
month_row(pr, 37, "Dostępne godziny (dni robocze × godziny)", lambda c, p: "=DniRobocze*GodzinyDzien", fmt=NUM1)
month_row(pr, 38, "Obłożenie", lambda c, p: f"=IF({c}37>0,{c}36/{c}37,0)", fmt=PCT, total=False)
put(pr, "O38", "=IF(O37>0,O36/O37,0)", fmt=PCT)
pr.column_dimensions["A"].width = 44
pr.column_dimensions["B"].width = 14
for col in MONTH_COLS + ["O"]:
    pr.column_dimensions[col].width = 12
pr.column_dimensions["C"].width = 16
pr.column_dimensions["D"].width = 12
pr.column_dimensions["E"].width = 16
pr.freeze_panes = "C19"

# =====================================================================
# 5. KOSZTY
# =====================================================================
ko = wb.create_sheet("Koszty")
title(ko, "Koszty, składki ZUS, składka zdrowotna i podatek – 12 miesięcy",
      "Kolumna B: kwota miesięczna (żółte) lub % przychodu. ZUS wg wariantu z arkusza Zalozenia. Podatek liczony narastająco "
      "w roku kalendarzowym (zaliczki), kwota wolna i próg skali resetują się 1 stycznia.")
month_header(ko, 4, 5)
month_row(ko, 6, "Rok kalendarzowy (podatkowy)", lambda c, p: f"=YEAR({c}5)", fmt="0", total=False)

section(ko, "A8", "A. Koszty stałe (zł/mies.)")
put(ko, "B8", "Kwota / mies.", bold=True)
FIXED = [
    ("Czynsz / najem lokalu", 0, "Fryzjerka mobilna nie wynajmuje lokalu."),
    ("Media (prąd, woda, gaz)", 0, "Usługi w domu klienta – media po stronie klienta."),
    ("Telefon i internet", 80, None),
    ("Księgowość (biuro rachunkowe)", 200, None),
    ("Ubezpieczenie (OC działalności, inne)", 60, None),
    ("Paliwo i eksploatacja auta", 700, "Ok. 1 300 km/mies. dojazdów do klientów."),
    ("Reklama (bieżąca)", 250, "Reklamy FB/Instagram, druk."),
    ("Inne (system rezerwacji, konto, serwis kasy)", 200, None),
]
F_FIRST = 9
for j, (nm, val, cm) in enumerate(FIXED):
    rr = F_FIRST + j
    month_row(ko, rr, nm, lambda c, p, rr=rr: f"=$B{rr}", param=val, param_fmt=PLN, param_input=True,
              param_comment=cm)
F_LAST = F_FIRST + len(FIXED) - 1
R_FIXED = F_LAST + 1  # 17
month_row(ko, R_FIXED, "Koszty stałe razem", lambda c, p: f"=SUM({c}{F_FIRST}:{c}{F_LAST})", bold=True)

section(ko, "A19", "B. Koszty zmienne")
R_MATPCT = 20
put(ko, f"A{R_MATPCT}", "Materiały i kosmetyki zużyte w usługach (% przychodu)")
put(ko, f"B{R_MATPCT}", 0.12, fmt=PCT_IN, inp=True,
    comment="Udział materiałów w przychodzie. Fryzjer: zwykle 10–15% (farby, oksydanty, szampony).")
define("MaterialyPct", ko, f"B{R_MATPCT}")
put(ko, f"C{R_MATPCT}", "→ kwoty w blokach scenariuszy poniżej", )
ko[f"C{R_MATPCT}"].font = F_NOTE

section(ko, "A22", "C. Składki ZUS na ubezpieczenia społeczne (wg wariantu z Zalozen)")
R_ETAP = 23
ulga_m = 'IF(UlgaStart="TAK",MiesUlgi,0)'
month_row(ko, R_ETAP, "Etap ZUS",
          lambda c, p: (f'=IF(AND(UlgaStart="TAK",{c}$4<=MiesUlgi),"Ulga na start",'
                        f'IF(AND(Preferencyjny="TAK",{c}$4<={ulga_m}+MiesPref),"Preferencyjny",'
                        f'IF(MalyZUS="TAK","Mały ZUS plus","Pełny")))'), fmt=None, total=False)
R_PODST = 24
month_row(ko, R_PODST, "Podstawa wymiaru (zł)",
          lambda c, p: (f'=IF({c}{R_ETAP}="Ulga na start",0,IF({c}{R_ETAP}="Preferencyjny",PodstPref,'
                        f'IF({c}{R_ETAP}="Mały ZUS plus",MIN(MAX(PodstawaMZP,PodstPref),PodstPelna),PodstPelna)))'),
          total=False)
month_row(ko, 25, "Emerytalna", lambda c, p: f"=ROUND({c}{R_PODST}*StEmer,2)")
month_row(ko, 26, "Rentowa", lambda c, p: f"=ROUND({c}{R_PODST}*StRent,2)")
month_row(ko, 27, "Chorobowa (dobrowolna)", lambda c, p: f'=IF(Chorobowe="TAK",ROUND({c}{R_PODST}*StChor,2),0)')
month_row(ko, 28, "Wypadkowa", lambda c, p: f"=ROUND({c}{R_PODST}*StWyp,2)")
month_row(ko, 29, "Fundusz Pracy + FS (gdy podstawa ≥ płaca minimalna)",
          lambda c, p: f"=IF({c}{R_PODST}>=PlacaMin,ROUND({c}{R_PODST}*StFP,2),0)")
R_ZUS = 30
month_row(ko, R_ZUS, "Składki społeczne razem", lambda c, p: f"=SUM({c}25:{c}29)", bold=True)

# ----- bloki scenariuszy
BLOCK_ROWS = {}


def scenario_block(start, label, factor_expr, key):
    rows = {}
    section(ko, f"A{start}", label)
    r = start + 1
    names = ["prz", "stale", "mat", "oper", "zus", "doch", "przcum", "zdr", "zdrcum", "odl", "podst",
             "podstcum", "podcum", "zalcum", "pod", "kosztyrazem", "wynik", "netto"]
    for i, n in enumerate(names):
        rows[n] = r + i
    R = rows
    month_row(ko, R["prz"], "Przychód netto (zł)", lambda c, p: f"=Przychody!{c}{R_PRZ}*(1-{factor_expr})")
    month_row(ko, R["stale"], "Koszty stałe", lambda c, p: f"={c}${R_FIXED}")
    month_row(ko, R["mat"], "Materiały (koszty zmienne)", lambda c, p: f"=ROUND({c}{R['prz']}*MaterialyPct,2)")
    month_row(ko, R["oper"], "Koszty operacyjne razem (bez ZUS i podatku)", lambda c, p: f"={c}{R['stale']}+{c}{R['mat']}", bold=True)
    month_row(ko, R["zus"], "Składki społeczne ZUS", lambda c, p: f"={c}${R_ZUS}")
    month_row(ko, R["doch"], "Dochód po składkach społecznych (podstawa zdrowotnej skala/liniowy)",
              lambda c, p: f"={c}{R['prz']}-{c}{R['oper']}-{c}{R['zus']}")
    month_row(ko, R["przcum"], "Przychód narastająco w roku kalendarzowym (próg ryczałtu)",
              lambda c, p: f'=SUMIFS(${FIRST}{R["prz"]}:${LAST}{R["prz"]},${FIRST}$6:${LAST}$6,{c}$6,${FIRST}$4:${LAST}$4,"<="&{c}$4)',
              total=False)
    month_row(ko, R["zdr"], "Składka zdrowotna",
              lambda c, p: (f'=IF(FormaOpodatkowania="ryczałt",IF({c}{R["przcum"]}<=RyczProg1,ZdrRycz1,'
                            f'IF({c}{R["przcum"]}<=RyczProg2,ZdrRycz2,ZdrRycz3)),'
                            f'MAX(ZdrMin,ROUND(MAX(0,{c}{R["doch"]})*IF(FormaOpodatkowania="liniowy",ZdrLin,ZdrSkala),2)))'))
    month_row(ko, R["zdrcum"], "Składka zdrowotna narastająco w roku (pomocniczo)",
              lambda c, p: f'=SUMIFS(${FIRST}{R["zdr"]}:${LAST}{R["zdr"]},${FIRST}$6:${LAST}$6,{c}$6,${FIRST}$4:${LAST}$4,"<="&{c}$4)',
              total=False)
    month_row(ko, R["odl"], "Odliczenie składki zdrowotnej (liniowy: do limitu; ryczałt: 50%)",
              lambda c, p: (f'=IF(FormaOpodatkowania="liniowy",MIN({c}{R["zdrcum"]},LimitZdrLin)-MIN({c}{R["zdrcum"]}-{c}{R["zdr"]},LimitZdrLin),'
                            f'IF(FormaOpodatkowania="ryczałt",ROUND({c}{R["zdr"]}*RyczOdlicz,2),0))'))
    month_row(ko, R["podst"], "Podstawa opodatkowania w miesiącu",
              lambda c, p: (f'=IF(FormaOpodatkowania="ryczałt",{c}{R["prz"]}-{c}{R["zus"]}-{c}{R["odl"]},'
                            f'{c}{R["prz"]}-{c}{R["oper"]}-{c}{R["zus"]}-{c}{R["odl"]})'))
    month_row(ko, R["podstcum"], "Podstawa narastająco w roku",
              lambda c, p: f'=SUMIFS(${FIRST}{R["podst"]}:${LAST}{R["podst"]},${FIRST}$6:${LAST}$6,{c}$6,${FIRST}$4:${LAST}$4,"<="&{c}$4)',
              total=False)
    month_row(ko, R["podcum"], "Podatek należny narastająco w roku",
              lambda c, p: (f'=ROUND(IF(FormaOpodatkowania="ryczałt",MAX(0,{c}{R["podstcum"]})*StawkaRyczaltu,'
                            f'IF(FormaOpodatkowania="liniowy",MAX(0,{c}{R["podstcum"]})*StLiniowy,'
                            f'IF({c}{R["podstcum"]}<=ProgPod,MAX(0,{c}{R["podstcum"]}*Stawka1-KwotaZmn),'
                            f'ProgPod*Stawka1-KwotaZmn+({c}{R["podstcum"]}-ProgPod)*Stawka2))),0)'), total=False)
    month_row(ko, R["zalcum"], "Zaliczki wpłacone narastająco w roku",
              lambda c, p: (f'={c}{R["podcum"]}' if p is None else
                            f'=IF({c}$6={p}$6,MAX({c}{R["podcum"]},{p}{R["zalcum"]}),{c}{R["podcum"]})'), total=False)
    month_row(ko, R["pod"], "Podatek dochodowy (zaliczka za miesiąc)",
              lambda c, p: (f'={c}{R["zalcum"]}' if p is None else
                            f'=IF({c}$6={p}$6,{c}{R["zalcum"]}-{p}{R["zalcum"]},{c}{R["zalcum"]})'))
    month_row(ko, R["kosztyrazem"], "KOSZTY RAZEM (operacyjne + ZUS + zdrowotna)",
              lambda c, p: f"={c}{R['oper']}+{c}{R['zus']}+{c}{R['zdr']}", bold=True)
    month_row(ko, R["wynik"], "Wynik przed opodatkowaniem", lambda c, p: f"={c}{R['prz']}-{c}{R['kosztyrazem']}", bold=True)
    month_row(ko, R["netto"], "Wynik netto (po podatku)", lambda c, p: f"={c}{R['wynik']}-{c}{R['pod']}", bold=True)
    BLOCK_ROWS[key] = rows
    return r + len(names)


nxt = scenario_block(32, "D. Scenariusz bazowy", "0", "base")
scenario_block(nxt + 1, "E. Scenariusz pesymistyczny (przychody niższe o % z Zalozenia!B22)", "SpadekPesym", "pes")
ko.column_dimensions["A"].width = 58
ko.column_dimensions["B"].width = 13
for col in MONTH_COLS + ["O"]:
    ko.column_dimensions[col].width = 12
ko.freeze_panes = "C6"
B = BLOCK_ROWS["base"]
P = BLOCK_ROWS["pes"]

# =====================================================================
# 6. PROGNOZA
# =====================================================================
pg = wb.create_sheet("Prognoza")
title(pg, "Rachunek wyników i przepływy pieniężne – 12 miesięcy",
      "Miesiąc 0 = start: wpływ dotacji i wkładu własnego, zapłata za zakupy z kosztorysu. Scenariusz pesymistyczny w kolumnach M–R.")
pg.merge_cells("C3:K3")
pg["C3"] = "SCENARIUSZ BAZOWY"
pg.merge_cells("M3:S3")
pg["M3"] = "=\"SCENARIUSZ PESYMISTYCZNY (przychody −\"&TEXT(SpadekPesym,\"0%\")&\")\""
for a in ("C3", "M3"):
    pg[a].font = F_SECTION
    pg[a].alignment = Alignment(horizontal="center")
    pg[a].fill = FILL_HEAD
PH = ["Miesiąc", "Data", "Przychody (zł)", "Koszty operacyjne (zł)", "Składki społeczne ZUS (zł)", "Składka zdrowotna (zł)",
      "Koszty razem (zł)", "Wynik przed opodatkowaniem (zł)", "Podatek dochodowy (zł)", "Wynik netto (zł)",
      "Gotówka skumulowana (zł)", "", "Przychody (zł)", "Koszty razem (zł)", "Wynik przed opodatkowaniem (zł)",
      "Podatek dochodowy (zł)", "Wynik netto (zł)", "Gotówka skumulowana (zł)", "Miesiąc z zyskiem (1/0)"]
header_row(pg, 4, PH, height=48)
pg["L4"].fill = PatternFill(fill_type=None)
pg["L4"].border = Border()
# m0
put(pg, "A5", 0, fmt="0")
put(pg, "B5", "=DataStartu", fmt=MONTH)
put(pg, "C5", "Start: dotacja + wkład własny − zakupy z kosztorysu")
pg["C5"].font = F_NOTE
put(pg, "K5", "=Dotacja+WkladWlasny-KosztorysRazem", fmt=PLN)
put(pg, "R5", "=Dotacja+WkladWlasny-KosztorysRazem", fmt=PLN)
pg["K5"].comment = Comment("Dotacja (wpływ) + wkład własny (wpływ) − wszystkie zakupy z kosztorysu (kwota do rozliczenia). "
                           "U czynnego VAT-owca liczone netto: VAT odliczony od zakupów z dotacji zwraca się do PUP.", "Model PUP")


def idx(sheet_row, sheet="Koszty"):
    return f"=INDEX({sheet}!${FIRST}${sheet_row}:${LAST}${sheet_row},$A{{r}})"


PROG = {
    "B": f"=EDATE(DataStartu,$A{{r}}-1)",
    "C": idx(B["prz"]), "D": idx(B["oper"]), "E": idx(B["zus"]), "F": idx(B["zdr"]),
    "G": "=D{r}+E{r}+F{r}", "H": "=C{r}-G{r}", "I": idx(B["pod"]), "J": "=H{r}-I{r}",
    "K": "=K{p}+J{r}",
    "M": idx(P["prz"]), "N": idx(P["kosztyrazem"]), "O": "=M{r}-N{r}", "P": idx(P["pod"]),
    "Q": "=O{r}-P{r}", "R": "=R{p}+Q{r}", "S": "=IF(J{r}>0,1,0)",
}
for m in range(1, 13):
    rr = 5 + m
    put(pg, f"A{rr}", m, fmt="0")
    for col, f in PROG.items():
        put(pg, f"{col}{rr}", f.format(r=rr, p=rr - 1), fmt=(MONTH if col == "B" else ("0" if col == "S" else PLN)))
# m0 row in K/R references: rows 6.. use K5/R5 – OK. Wiersz 18 = m12
R_TOT = 19
put(pg, f"A{R_TOT}", "Razem 12 mies.", bold=True)
for col in "CDEFGHIJMNOPQ":
    put(pg, f"{col}{R_TOT}", f"=SUM({col}6:{col}17)", fmt=PLN)
put(pg, f"K{R_TOT}", "=K17", fmt=PLN)
put(pg, f"R{R_TOT}", "=R17", fmt=PLN)
put(pg, f"S{R_TOT}", "=SUM(S6:S17)", fmt="0")
total_style(pg, R_TOT, 1, 19)
pg[f"L{R_TOT}"].fill = PatternFill(fill_type=None)
pg[f"L{R_TOT}"].border = Border()

section(pg, "A22", "Próg rentowności")
header_row(pg, 23, ["Wskaźnik", "", "Wartość", "Jak liczone"], height=20)
pg.merge_cells("A23:B23")
BEP = [
    (24, "Średnie miesięczne koszty stałe z ZUS i zdrowotną (zł)",
     f"=(Koszty!O{R_FIXED}+Koszty!O{R_ZUS}+Koszty!O{B['zdr']})/12", PLN,
     "Koszty stałe + składki społeczne + zdrowotna, średnio z 12 mies."),
    (25, "Udział kosztów zmiennych w przychodzie", "=MaterialyPct", PCT, "Materiały jako % przychodu (arkusz Koszty)."),
    (26, "PRÓG RENTOWNOŚCI – przychód miesięczny (zł)", "=IF(C25<1,C24/(1-C25),0)", PLN,
     "Koszty stałe ÷ (1 − % kosztów zmiennych). Poniżej tej sprzedaży firma traci."),
    (27, "Średnia cena netto jednej sprzedaży (zł)", "=IF(Przychody!O34>0,Przychody!O33/Przychody!O34,0)", PLN,
     "Przychód roczny ÷ liczba sprzedaży w roku."),
    (28, "PRÓG RENTOWNOŚCI – liczba sprzedaży / mies.", "=IF(C27>0,ROUNDUP(C26/C27,0),0)", NUM,
     "Ile usług/sztuk miesięcznie trzeba sprzedać."),
    (29, "Próg rentowności po okresie ulg (pełny ZUS) – przychód miesięczny (zł)",
     f'=IF(C25<1,(Koszty!O{R_FIXED}/12+ZUSPelnySuma-IF(Chorobowe="TAK",0,ZUSPelnyChor)+Koszty!O{B["zdr"]}/12)/(1-C25),0)', PLN,
     "Jak wyżej, ale ze składkami społecznymi pełnymi (po 30 mies. ulg)."),
    (30, "Średni przychód miesięczny od 4. miesiąca – scenariusz bazowy (zł)", "=AVERAGE(C9:C17)", PLN,
     "Po okresie rozruchu."),
    (31, "Margines bezpieczeństwa – scenariusz bazowy", "=IF(C30>0,(C30-C26)/C30,0)", PCT,
     "O ile % mogą spaść przychody, zanim firma przestanie zarabiać."),
    (32, "Średni przychód miesięczny od 4. miesiąca – scenariusz pesymistyczny (zł)", "=AVERAGE(M9:M17)", PLN, ""),
    (33, "Margines bezpieczeństwa – scenariusz pesymistyczny", "=IF(C32>0,(C32-C26)/C32,0)", PCT,
     "Ujemny = w pesymistycznym scenariuszu firma jest poniżej progu."),
    (34, "Pierwszy miesiąc z dodatnim wynikiem netto (bazowy)", '=IFERROR(MATCH(1,S6:S17,0),"brak w 12 mies.")', "0", ""),
]
for rr, lab, f, fmt, how in BEP:
    put(pg, f"A{rr}", lab, bold=("PRÓG" in lab))
    pg.merge_cells(f"A{rr}:B{rr}")
    put(pg, f"C{rr}", f, fmt=fmt)
    put(pg, f"D{rr}", how)
    pg[f"D{rr}"].font = F_NOTE
define("ProgRentPrzychod", pg, "C26")
define("ProgRentSzt", pg, "C28")
define("ark_prog_rent_pelny_zus", pg, "C29")
define("ark_margines", pg, "C31")
define("ark_margines_pes", pg, "C33")
define("ark_pierwszy_mies_zysku", pg, "C34")
define("ark_reklama_mies", ko, "B15")
define("ark_reklama_kosztorys_dotacja", ks, "C35")
for _j, (_cat, _l) in enumerate(CATS):
    define("ark_kat_" + _cat.replace("ę", "e"), ks, f"C{CAT_FIRST + _j}")
define("ark_kosztorys_razem", ks, f"K{R_SUM}")
define("ark_kosztorys_dotacja", ks, f"K{R_SUM+1}")
define("ark_kosztorys_wklad", ks, f"K{R_SUM+2}")
define("ark_dotacja", wb["Zalozenia"], "B5")
define("ark_wklad_wlasny", wb["Zalozenia"], "B7")
define("ark_oblozenie_max", wb["Zalozenia"], "B33")
define("ark_koszty_stale_mies", ko, f"C{R_FIXED}")
define("ark_zus_m12", ko, f"N{R_ZUS}")
define("ark_zdrowotna_12m", ko, f"O{B['zdr']}")
define("ark_przychod_sredni_od_m4", pg, "C30")
define("ark_materialy_pct", ko, f"B{R_MATPCT}")
pg.column_dimensions["A"].width = 10
pg.column_dimensions["B"].width = 10
for col in "CDEFGHIJKMNOPQRS":
    pg.column_dimensions[col].width = 14
pg.column_dimensions["L"].width = 2
pg.freeze_panes = "C5"

# =====================================================================
# 7. DO-WNIOSKU
# =====================================================================
dw = wb.create_sheet("Do-wniosku")
title(dw, "Tabele do przepisania do wniosku PUP",
      "Wartości liczone automatycznie z pozostałych arkuszy (scenariusz bazowy). Kwoty w zł, zaokrąglone do pełnych złotych w wyświetlaniu.")
section(dw, "A4", "1. Kalkulacja przewidywanych przychodów i kosztów na 12 miesięcy – układ miesięczny")
month_header(dw, 5, 6, label_nr="Pozycja / miesiąc działalności")
TAB = [("Przychody ze sprzedaży", B["prz"], True),
       ("Koszty razem, w tym:", B["kosztyrazem"], True),
       ("– zakup materiałów i towarów", B["mat"], False)]
TAB += [("– " + FIXED[j][0][0].lower() + FIXED[j][0][1:], F_FIRST + j, False) for j in range(len(FIXED))]
TAB += [("– składki ZUS (społeczne)", R_ZUS, False),
        ("– składka zdrowotna", B["zdr"], False),
        ("Dochód (przychody − koszty)", B["wynik"], True),
        ("Podatek dochodowy", B["pod"], False),
        ("Dochód netto (po podatku)", B["netto"], True)]
T1_FIRST = 7
for j, (lab, src, bold) in enumerate(TAB):
    rr = T1_FIRST + j
    month_row(dw, rr, lab, lambda c, p, src=src: f"=Koszty!{c}{src}", fmt=PLN0, bold=bold)
T1_LAST = T1_FIRST + len(TAB) - 1

q_start = T1_LAST + 3
section(dw, f"A{q_start}", "1a. Ta sama kalkulacja – układ kwartalny")
QH = ["Pozycja", "", "Kwartał I (mies. 1–3)", "Kwartał II (mies. 4–6)", "Kwartał III (mies. 7–9)",
      "Kwartał IV (mies. 10–12)", "Razem 12 mies."]
header_row(dw, q_start + 1, QH, height=32)
QCOLS = [("C", "E"), ("F", "H"), ("I", "K"), ("L", "N")]
for j, (lab, src, bold) in enumerate(TAB):
    rr = q_start + 2 + j
    src_r = T1_FIRST + j
    put(dw, f"A{rr}", f"=A{src_r}", bold=bold)
    for k, (a, b2) in enumerate(QCOLS):
        put(dw, f"{get_column_letter(3+k)}{rr}", f"=SUM({a}{src_r}:{b2}{src_r})", fmt=PLN0)
    put(dw, f"G{rr}", f"=SUM(C{rr}:F{rr})", fmt=PLN0)
    if bold:
        total_style(dw, rr, 1, 7)
q_last = q_start + 1 + len(TAB)
put(dw, f"A{q_last+1}", "Kontrola: suma kwartałów = suma miesięcy")
put(dw, f"G{q_last+1}", f'=IF(ABS(G{q_start+2}-O{T1_FIRST})<0.01,"OK","BŁĄD")')

s_start = q_last + 4
section(dw, f"A{s_start}", "2. Specyfikacja wydatków w ramach dotacji (i wkładu własnego)")
SH = ["Lp.", "Rodzaj wydatku (nazwa)", "Kategoria", "Nowy / używany", "Ilość", "Kwota netto (zł)", "VAT (zł)",
      "Kwota brutto (zł)", "Źródło finansowania", "Kwota z dotacji (zł)"]
header_row(dw, s_start + 1, SH, height=32)
for i in range(K_FIRST, K_LAST + 1):
    rr = s_start + 2 + (i - K_FIRST)
    put(dw, f"A{rr}", f'=IF(Kosztorys!B{i}="","",Kosztorys!A{i})')
    put(dw, f"B{rr}", f'=IF(Kosztorys!B{i}="","",Kosztorys!B{i})')
    put(dw, f"C{rr}", f'=IF(Kosztorys!B{i}="","",Kosztorys!C{i})')
    put(dw, f"D{rr}", f'=IF(Kosztorys!B{i}="","",Kosztorys!D{i})')
    put(dw, f"E{rr}", f"=Kosztorys!E{i}", fmt=NUM)
    put(dw, f"F{rr}", f"=Kosztorys!G{i}", fmt=PLN)
    put(dw, f"G{rr}", f"=Kosztorys!I{i}", fmt=PLN)
    put(dw, f"H{rr}", f"=Kosztorys!J{i}", fmt=PLN)
    put(dw, f"I{rr}", f'=IF(Kosztorys!B{i}="","",Kosztorys!M{i})')
    put(dw, f"J{rr}", f'=IF(Kosztorys!M{i}="dotacja",Kosztorys!K{i},0)', fmt=PLN)
s_last = s_start + 1 + (K_LAST - K_FIRST + 1)
put(dw, f"B{s_last+1}", "RAZEM", bold=True)
for col in "FGHJ":
    put(dw, f"{col}{s_last+1}", f"=SUM({col}{s_start+2}:{col}{s_last})", fmt=PLN)
total_style(dw, s_last + 1, 1, 10)
put(dw, f"B{s_last+2}", "Wnioskowana kwota dotacji")
put(dw, f"J{s_last+2}", "=Dotacja", fmt=PLN)
put(dw, f"B{s_last+3}", "Wkład własny (gotówka)")
put(dw, f"J{s_last+3}", "=WkladWlasny", fmt=PLN)

w_start = s_last + 6
section(dw, f"A{w_start}", "3. Wskaźniki ekonomiczne")
header_row(dw, w_start + 1, ["Wskaźnik", "", "Scenariusz bazowy", "Scenariusz pesymistyczny", "Uwagi"], height=30)
W = [
    ("Przychody w 12 mies. (zł)", "=Prognoza!C19", "=Prognoza!M19", PLN, ""),
    ("Koszty w 12 mies. (zł)", "=Prognoza!G19", "=Prognoza!N19", PLN, "z ZUS i zdrowotną, bez podatku"),
    ("Zysk roczny przed opodatkowaniem (zł)", "=Prognoza!H19", "=Prognoza!O19", PLN, ""),
    ("Podatek dochodowy w 12 mies. (zł)", "=Prognoza!I19", "=Prognoza!P19", PLN, ""),
    ("ZYSK ROCZNY NETTO (zł)", "=Prognoza!J19", "=Prognoza!Q19", PLN, ""),
    ("Średni zysk netto miesięcznie (zł)", f"=C{w_start+6}/12", f"=D{w_start+6}/12", PLN, ""),
    ("Rentowność sprzedaży netto", f"=IF(C{w_start+2}>0,C{w_start+6}/C{w_start+2},0)",
     f"=IF(D{w_start+2}>0,D{w_start+6}/D{w_start+2},0)", PCT, "zysk netto ÷ przychody"),
    ("Próg rentowności – przychód miesięczny (zł)", "=ProgRentPrzychod", "=ProgRentPrzychod", PLN,
     "nie zależy od scenariusza"),
    ("Próg rentowności – liczba sprzedaży / mies.", "=ProgRentSzt", "=ProgRentSzt", NUM, ""),
    ("Zwrot z dotacji (zysk netto roczny ÷ dotacja)", f"=IF(Dotacja>0,C{w_start+6}/Dotacja,0)",
     f"=IF(Dotacja>0,D{w_start+6}/Dotacja,0)", PCT, "ile % dotacji firma 'zarabia' w roku"),
    ("Okres zwrotu dotacji (mies.)", f"=IF(C{w_start+7}>0,Dotacja/C{w_start+7},\"nie zwraca się\")",
     f"=IF(D{w_start+7}>0,Dotacja/D{w_start+7},\"nie zwraca się\")", NUM1, "dotacja ÷ średni zysk netto mies."),
    ("Gotówka na koniec 12. miesiąca (zł)", "=Prognoza!K19", "=Prognoza!R19", PLN, ""),
    ("Najniższe saldo gotówki w 12 mies. (zł)", "=MIN(Prognoza!K5:K17)", "=MIN(Prognoza!R5:R17)", PLN,
     "ujemne = brak płynności"),
]
W_NAMES = ["przychod_12m", "koszty_12m", "zysk_brutto_12m", "podatek_12m", "zysk_netto_12m",
           "zysk_netto_mies", "rentownosc", "prog_rent_zl", "prog_rent_szt", "zwrot_z_dotacji",
           "okres_zwrotu_mies", "gotowka_m12", "min_saldo"]
for j, (lab, fb, fp, fmt, note) in enumerate(W):
    rr = w_start + 2 + j
    put(dw, f"A{rr}", lab, bold=lab.isupper() or "ZYSK" in lab)
    dw.merge_cells(f"A{rr}:B{rr}")
    put(dw, f"C{rr}", fb, fmt=fmt)
    put(dw, f"D{rr}", fp, fmt=fmt)
    put(dw, f"E{rr}", note)
    dw[f"E{rr}"].font = F_NOTE
    define(f"ark_{W_NAMES[j]}", dw, f"C{rr}")
    define(f"ark_{W_NAMES[j]}_pes", dw, f"D{rr}")
dw.column_dimensions["A"].width = 46
dw.column_dimensions["B"].width = 34
for col in MONTH_COLS + ["O"]:
    dw.column_dimensions[col].width = 13
dw.column_dimensions["C"].width = 16
dw.column_dimensions["D"].width = 16
dw.column_dimensions["I"].width = 14

# formuła kontroli VAT (potrzebuje numeru wiersza przychodu z arkusza Koszty)
_y = "YEAR(DataStartu)"
_rng = f"Koszty!${FIRST}${B['prz']}:${LAST}${B['prz']}"
_yr = f"Koszty!${FIRST}$6:${LAST}$6"
wb["Zalozenia"]["B34"] = (
    f'=IF(VATczynny="TAK","czynny VAT",IF(AND(SUMIFS({_rng},{_yr},{_y})<=LimitVAT*(DATE({_y},12,31)-DataStartu+1)/'
    f'(DATE({_y},12,31)-DATE({_y},1,1)+1),SUMIFS({_rng},{_yr},{_y}+1)<=LimitVAT),"OK (poniżej limitu)",'
    f'"UWAGA: możliwe przekroczenie limitu"))')

# =====================================================================
# Kolorowanie: formuły czarne, odwołania do innych arkuszy zielone
# =====================================================================
TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
for sh in wb.worksheets:
    for row in sh.iter_rows():
        for c in row:
            if c.value is None:
                continue
            if (sh.title, c.coordinate) in INPUT_CELLS:
                continue
            if c.font is None or c.font.name != FONT_NAME:
                c.font = F_BASE
            if isinstance(c.value, str) and c.value.startswith("="):
                cross = "!" in c.value or any(NAMES.get(t) not in (None, sh.title) for t in TOKEN.findall(c.value))
                f = c.font
                c.font = Font(name=FONT_NAME, size=f.size or 10, bold=f.bold, italic=f.italic,
                              color=("008000" if cross else "000000"))

# legenda na arkuszu Zalozenia
zl = wb["Zalozenia"]
put(zl, "E3", "Legenda kolorów", bold=True)
put(zl, "E4", "Dane do wpisania", inp=True)
zl["E5"] = "Formuła w tym arkuszu"
zl["E5"].font = F_CALC
zl["E6"] = "Odwołanie do innego arkusza"
zl["E6"].font = F_LINK
zl.column_dimensions["E"].width = 30
INPUT_CELLS.discard(("Zalozenia", "E4"))

wb.save(OUT)
print("Zapisano:", OUT)
