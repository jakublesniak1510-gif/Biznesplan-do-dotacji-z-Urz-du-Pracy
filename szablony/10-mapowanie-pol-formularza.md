# 10 – Mapowanie pól formularza PUP na sekcje 01–09

> Każdy powiatowy urząd pracy ma własny wzór wniosku o dofinansowanie podjęcia działalności gospodarczej (różne nazwy pól, kolejność, limity). Ten krok zamienia formularz wgrany przez klienta (PDF lub DOCX) na **listę pól z limitami**, przypisaną do naszych sekcji 01–09 i tabel z arkusza. Wynik akceptuje właściciel **przed** generowaniem treści.

## 1. Wynik tego kroku

Plik `mapowanie.json` (i tabela do podglądu dla właściciela):

```json
{
  "pup": "PUP w Zielonowie",
  "formularz": "Wniosek o przyznanie dofinansowania – wzór 2026",
  "plik_zrodlowy": "wniosek_PUP_Zielonow_2026.pdf",
  "typ_pliku": "pdf_formularz",
  "pola": [
    {
      "id": "IV.1",
      "nazwa_w_formularzu": "Opis planowanego przedsięwzięcia",
      "strona": 4,
      "limit": {"wartosc": 2000, "jednostka": "znaki_ze_spacjami", "zrodlo": "/MaxLen"},
      "limit_znakow": 2000,
      "sekcje": ["01"],
      "podzial_limitu": null,
      "format": "tekst",
      "uwagi": ""
    }
  ],
  "tabele_z_arkusza": [
    {"id": "V.2", "nazwa_w_formularzu": "Kalkulacja przychodów i kosztów", "arkusz": "Do-wniosku", "uklad": "kwartalny"}
  ],
  "poza_zakresem": ["I. Dane wnioskodawcy", "VII. Formy zabezpieczenia zwrotu", "VIII. Oświadczenia"],
  "do_wyjasnienia": ["Pole III.3 bez limitu – przyjęto 1 strona = 1 800 znaków"]
}
```

## 2. Procedura krok po kroku

### Krok 1 – rozpoznaj typ pliku

| Typ | Jak rozpoznać | Narzędzie |
|---|---|---|
| PDF z polami formularza (AcroForm) | `pypdf` zwraca pola z `get_fields()` | `pypdf` – nazwy pól, `/MaxLen` (twardy limit znaków), `/TU` (opis pola) |
| PDF „płaski” (tekst, bez pól) | brak pól, ale `pdftotext` zwraca tekst | `pdftotext -layout`, `pdfplumber` (tabele) |
| Skan (obraz) | `pdftotext` zwraca pusty lub prawie pusty tekst | OCR: `ocrmypdf -l pol` lub `tesseract … -l pol`, potem jak PDF płaski |
| DOCX | rozszerzenie / nagłówek ZIP | `python-docx` – akapity, tabele; pola formularza (content controls `w:sdt`) |
| DOC / ODT / XLSX | rzadkie | konwersja `soffice --headless --convert-to docx` / odczyt `openpyxl` |

### Krok 2 – wyciągnij pola i teksty wokół nich

```python
# PDF z polami formularza
from pypdf import PdfReader
reader = PdfReader("wniosek.pdf")
for name, f in (reader.get_fields() or {}).items():
    print(name, f.get("/FT"), f.get("/MaxLen"), f.get("/TU"))   # /Tx = pole tekstowe

# PDF płaski – tekst z układem (nagłówki pól + instrukcje typu "max. 2000 znaków")
#   pdftotext -layout wniosek.pdf wniosek.txt
import pdfplumber
with pdfplumber.open("wniosek.pdf") as pdf:
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ""
        tables = page.extract_tables()

# DOCX
from docx import Document
doc = Document("wniosek.docx")
paragrafy = [p.text for p in doc.paragraphs if p.text.strip()]
tabele = [[[c.text for c in r.cells] for r in t.rows] for t in doc.tables]
```

Pliki od klienta traktujemy jako niezaufane: rozpakowujemy je do osobnego katalogu, a skrypty uruchamiamy spoza tego katalogu.

### Krok 3 – znajdź limity i sprowadź je do znaków ze spacjami

Szukaj w tekście przy polu (regex, bez rozróżniania wielkości liter):
`(max\.?|maks\.?|maksymalnie|do|nie więcej niż|limit)\s*(\d[\d\s]*)\s*(znak|słów|wyraz|stron|lini|wiersz)`

| Zapis w formularzu | Przyjmowana wartość | Uwagi |
|---|---|---|
| `/MaxLen` w polu PDF | dokładnie tyle znaków | limit twardy: pole nie przyjmie więcej |
| „max. N znaków (ze spacjami)” | N | |
| „max. N znaków bez spacji” | ≈ N × 1,15 ze spacjami | w tekście polskim ok. 13–15% znaków to spacje. Licz ostrożnie, a po wygenerowaniu sprawdź skryptem bez spacji |
| „max. N słów” | ≈ N × 7 znaków | średnio 6–7 znaków na słowo ze spacją |
| „1 strona A4” | 1 800 znaków | strona znormalizowana. Przy czcionce 10 pt może zmieścić się więcej, ale liczymy ostrożnie |
| „pół strony” | 900 | |
| pole o N liniach (puste linie do ręcznego wypełnienia) | N × 85 | przy wydruku formularza i Arial 11 pt |
| brak limitu | 2 000 (standard) | zapisz w `do_wyjasnienia`. Długie teksty bez limitu nie dają punktów, a męczą komisję |

Do generowania przyjmij **95% limitu twardego** (margines na poprawki właściciela). Przy limitach przeliczanych przyjmij 90%.

### Krok 4 – przypisz pola do sekcji

Słownik słów kluczowych (sprawdzaj nazwę pola i instrukcję pod nią):

| Słowa w nazwie lub instrukcji pola | Sekcja |
|---|---|
| opis przedsięwzięcia, charakterystyka działalności, przedmiot, rodzaj działalności, PKD, lokalizacja, miejsce prowadzenia | 01 |
| kwalifikacje, wykształcenie, doświadczenie, przygotowanie zawodowe, kursy, uprawnienia | 02 |
| rynek, klienci, odbiorcy, popyt, zapotrzebowanie, zasięg, sezonowość | 03 |
| konkurencja, konkurenci, przewaga | 04 |
| marketing, promocja, reklama, pozyskanie klientów, sprzedaż, dystrybucja | 05 |
| specyfikacja wydatków, kosztorys, zakupy, uzasadnienie wydatków, sprzęt, wyposażenie | 06 (+ tabela z arkusza `Do-wniosku` część 2) |
| SWOT, mocne i słabe strony, szanse, zagrożenia | 07 |
| przychody, koszty, kalkulacja, efektywność, zysk, opłacalność, próg rentowności, prognoza | 08 (+ tabela z arkusza `Do-wniosku` część 1/1a/3) |
| ryzyko, zagrożenia dla realizacji, plan awaryjny, co w przypadku | 09 |
| dane osobowe, adres, PESEL, rachunek bankowy, zabezpieczenie (poręczenie, weksel, blokada, gwarancja), oświadczenia, pomoc de minimis, załączniki | poza zakresem: wypełnia klient, ale dodaj do jego listy kontrolnej |

Reguły szczególne:
- **Pole łączone** (np. „Analiza rynku i konkurencji”): `sekcje: ["03","04"]`, `podzial_limitu: {"03": 0.55, "04": 0.45}`. Model pisze jeden ciągły tekst według obu szablonów, a operator przekazuje oba szablony.
- **Pole rozbite** (np. SWOT w 4 polach, konkurencja w tabeli z wierszami): jedna sekcja, kilka pól. Zapisz `format: "4_pola"` lub `"tabela"` i liczbę wierszy.
- **Tabela liczbowa w formularzu** (przychody i koszty, harmonogram wydatków): `tabele_z_arkusza`, układ `miesięczny` / `kwartalny` / `roczny`. Liczby przepisujemy z arkusza `Do-wniosku`, a model ich nie generuje.
- **Pytania otwarte nietypowe** (np. „Dlaczego wybrał Pan samozatrudnienie zamiast pracy etatowej?”): przypisz do najbliższej sekcji (zwykle 01 – motywacja albo 09) i dodaj `uwagi` z treścią pytania. Model dostaje pytanie dosłownie w `<parametry>`.
- **Kolejność:** zachowaj kolejność pól z formularza. Generujemy sekcjami, ale składamy dokument w kolejności urzędu.

### Krok 5 – akceptacja właściciela

Właściciel sprawdza tabelę mapowania (pkt 3) i:
- potwierdza limity (szczególnie przeliczone ze stron i słów);
- uzupełnia `do_wyjasnienia` (np. dzwoni do PUP albo sprawdza regulamin);
- dopisuje notatkę o regulaminie (kategorie wydatków, limity %, zasady dla sprzętu używanego). Notatka trafia do sekcji 06 i do arkusza `Kosztorys` (B33–B37).

Dopiero po akceptacji uruchamiamy generowanie sekcji 01–09 z `limit_znakow` z mapowania.

## 3. Przykładowa tabela mapowania

> **DANE FIKCYJNE.** Wzór wniosku „PUP w Zielonowie 2026” jest wymyślony, ale jego układ odpowiada typowym formularzom PUP.

| Id | Pole w formularzu | Str. | Limit w formularzu | Limit do generowania | Sekcja / źródło | Format | Uwagi |
|---|---|---|---|---|---|---|---|
| I | Dane wnioskodawcy | 1 | – | – | poza zakresem | – | klient |
| II.1 | Rodzaj i miejsce planowanej działalności, kod PKD | 2 | `/MaxLen` 800 | 760 | 01 (wariant krótki) | tekst | PKD 2025 |
| II.2 | Planowana forma opodatkowania | 2 | pole wyboru | – | z arkusza `Zalozenia!B9` | zaznaczenie | ręcznie |
| III.1 | Wykształcenie i doświadczenie zawodowe związane z działalnością | 3 | „max. 1 strona” | 1 620 | 02 | tekst | 1 800 × 0,9 |
| III.2 | Dlaczego zdecydował/a się Pan/i na własną działalność? | 3 | 10 linii | 765 | 01 – motywacja | tekst | pytanie przekazać dosłownie |
| IV.1 | Opis planowanego przedsięwzięcia | 4 | `/MaxLen` 2000 | 1 900 | 01 (standard) | tekst | |
| IV.2 | Analiza rynku i konkurencji | 4–5 | „max. 3000 znaków” | 2 850 | 03 + 04 (55/45) | tekst | tabela niedozwolona, konkurenci w akapitach |
| IV.3 | Sposób pozyskania klientów | 5 | „max. 300 słów” | 1 890 | 05 | tekst | 300 × 7 × 0,9 |
| IV.4 | Analiza SWOT | 5 | tabela 2×2, każda ćwiartka 6 linii | 4 × 450 | 07 (4 pola) | 4 pola | 6 × 85 × 0,9 |
| V.1 | Specyfikacja wydatków z uzasadnieniem | 6 | tabela, kolumna „uzasadnienie” bez limitu | 300 / poz. | 06 (pozycyjny) + `Do-wniosku` cz. 2 | tabela | kwoty brutto (zwolnienie z VAT) |
| V.2 | Kalkulacja przewidywanych przychodów i kosztów w pierwszym roku | 7 | tabela kwartalna | – | `Do-wniosku` cz. 1a | tabela | przepisać, model nie pisze |
| V.3 | Uzasadnienie przyjętych założeń finansowych | 7 | brak limitu | 2 000 | 08 (standard) | tekst | `do_wyjasnienia` |
| V.4 | Co Pan/i zrobi, jeśli przychody będą niższe od planowanych? | 8 | 8 linii | 610 | 09 (krótki) + scenariusz −30% | tekst | |
| VI | Wysokość wnioskowanej kwoty i wkład własny | 8 | pola liczbowe | – | `Zalozenia!B5`, `B7` | liczby | |
| VII | Proponowana forma zabezpieczenia zwrotu | 9 | – | – | poza zakresem | – | lista kontrolna klienta |
| VIII | Oświadczenia, de minimis, załączniki | 10–12 | – | – | poza zakresem | – | lista kontrolna klienta |

## 4. Prompt do kroku mapowania

Wywołanie: `system` = poniższy prompt; `user` = tekst wyciągnięty z formularza (z numerami stron) + lista pól AcroForm (nazwa, `/MaxLen`, `/TU`), jeśli są.

```text
Jesteś asystentem, który analizuje formularz wniosku o dofinansowanie podjęcia działalności
gospodarczej z powiatowego urzędu pracy. Dostajesz tekst formularza (z numerami stron) oraz –
jeśli istnieją – listę pól formularza PDF z atrybutem /MaxLen.

Zadanie: zwróć WYŁĄCZNIE poprawny JSON zgodny ze schematem:
{ "pup": str, "formularz": str, "pola": [ { "id": str, "nazwa_w_formularzu": str,
  "strona": int, "limit": {"wartosc": number|null, "jednostka": "znaki_ze_spacjami"|
  "znaki_bez_spacji"|"slowa"|"strony"|"linie"|"brak", "zrodlo": str},
  "limit_znakow": int|null, "sekcje": [str], "podzial_limitu": object|null,
  "format": "tekst"|"tabela"|"4_pola"|"zaznaczenie"|"liczba", "uwagi": str } ],
  "tabele_z_arkusza": [...], "poza_zakresem": [str], "do_wyjasnienia": [str] }

Zasady:
1. Wypisz KAŻDE pole do wypełnienia, w kolejności z formularza. Nie pomijaj pól
   "poza zakresem" – trafiają do listy poza_zakresem.
2. Limit: jeśli pole PDF ma /MaxLen – to jest limit (jednostka znaki_ze_spacjami, zrodlo
   "/MaxLen"). W przeciwnym razie szukaj w tekście przy polu zapisów typu "max. 2000 znaków",
   "do 300 słów", "1 strona". Przelicz na limit_znakow: znaki bez spacji ×1,15; słowa ×7;
   strona 1800; linia 85. Do limit_znakow zastosuj współczynnik 0,95 dla /MaxLen i znaków ze
   spacjami, 0,90 dla pozostałych jednostek; zaokrąglij w dół do dziesiątek.
   Brak limitu → limit_znakow 2000 i wpis w do_wyjasnienia.
3. Sekcje przypisuj według słownika: 01 opis/PKD/lokalizacja/motywacja; 02 kwalifikacje i
   doświadczenie; 03 rynek i klienci; 04 konkurencja; 05 marketing i pozyskanie klientów;
   06 wydatki i ich uzasadnienie; 07 SWOT; 08 przychody/koszty/opłacalność (opis);
   09 ryzyka/plan B/co jeśli. Pole łączące dwa tematy → dwie sekcje i podzial_limitu
   proporcjonalnie do wagi tematów (np. 0.55/0.45).
4. Tabele liczbowe (przychody, koszty, harmonogram, specyfikacja kwot) → tabele_z_arkusza
   z układem (miesięczny/kwartalny/roczny). Nie przypisuj ich do sekcji tekstowych, chyba że
   tabela ma kolumnę "uzasadnienie" – wtedy dodatkowo pole z sekcją 06, format "tabela".
5. Pytania nietypowe przepisz dosłownie do "uwagi".
6. Niczego nie zgaduj: jeśli nie wiesz, do której sekcji należy pole albo jaki ma limit –
   wpisz to do do_wyjasnienia.
```

## 5. Kontrola po mapowaniu (skrypt + właściciel)

- [ ] Liczba pól tekstowych w JSON = liczba pól tekstowych w formularzu (porównaj z `get_fields()` albo policz ręcznie).
- [ ] Każda sekcja 01–09 jest przypisana do co najmniej jednego pola albo świadomie pominięta (np. formularz nie ma SWOT, więc treść sekcji 07 wykorzystujemy tylko przy przygotowaniu do rozmowy).
- [ ] Suma `podzial_limitu` dla każdego pola wynosi 1,0.
- [ ] Tabele liczbowe mają wskazany układ, a arkusz `Do-wniosku` ma taki układ (miesięczny lub kwartalny). Jeśli PUP chce układu rocznego albo półrocznego, właściciel sumuje kolumny ręcznie lub dodaje wiersz w arkuszu.
- [ ] `poza_zakresem` trafia do listy kontrolnej klienta (zabezpieczenie zwrotu, oświadczenia, załączniki).
