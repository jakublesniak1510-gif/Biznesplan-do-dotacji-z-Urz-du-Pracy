# Model finansowy do wniosku PUP – instrukcja

Plik: `model-finansowy-pup.xlsx`. Generator: `build_model.py` (Python + openpyxl).
Stan stałych prawnych: **2026 r.**, sprawdzone 14.10.2026 (szczegóły i linki w arkuszu `Stale-2026`).

Arkusz liczy wszystkie liczby do wniosku: kosztorys, przychody, koszty, ZUS, składkę zdrowotną, podatek, przepływy gotówki i próg rentowności. **Model językowy tych liczb nie liczy.** Bierze gotowe wartości z arkusza (nazwane komórki `ark_*`, opis niżej) i wstawia je do tekstu jako zmienne.

---

## 1. Szybki start (nowy klient)

1. Skopiuj plik i nadaj mu nazwę `model-<nazwisko>-<data>.xlsx`.
2. Wypełniaj **tylko żółte komórki z niebieską czcionką**, w tej kolejności:
   1. `Zalozenia`: kwota dotacji, limit z naboru, wkład własny, data startu, forma opodatkowania, warianty ZUS, VAT, czas pracy.
   2. `Kosztorys`: pozycje zakupów (wiersze 5–24) i limity kategorii z regulaminu PUP (tabela w wierszach 33–37).
   3. `Przychody`: do 5 usług lub produktów (cena, liczba sprzedaży przy pełnym obłożeniu, czas jednej usługi), współczynnik rozruchu i sezonowość.
   4. `Koszty`: koszty stałe miesięczne (kolumna B) i % materiałów (B20).
3. Otwórz plik w Excelu albo LibreOffice. Formuły przeliczą się same. Jeśli generujesz plik skryptem, przelicz go przez `recalc.py` (patrz pkt 7).
4. Sprawdź blok **Kontrole spójności** w `Zalozenia` (wiersze 27–34). Każda kontrola musi pokazywać „OK” albo mieć świadomie opisany powód, dlaczego nie pokazuje.
5. Przepisz tabele z arkusza `Do-wniosku` do formularza PUP. Wartości `ark_*` przekaż do szablonu `szablony/08-prognoza-finansowa-opis.md`.

Przykład w pliku to **fryzjerka mobilna** i są to **dane fikcyjne**. Przed pracą nad klientem nadpisz wszystkie żółte komórki.

## 2. Arkusze

| Arkusz | Co zawiera | Co edytujesz |
|---|---|---|
| `Zalozenia` | parametry klienta, legenda kolorów, kontrole spójności | B4–B22 |
| `Stale-2026` | płaca minimalna, podstawy i stopy ZUS, składka zdrowotna, progi podatkowe, limit VAT; źródło, akt prawny i status każdej wartości | tylko przy zmianie przepisów (niebieskie wartości) |
| `Kosztorys` | pozycje zakupów: netto, VAT, brutto, finansowanie, limity kategorii i flaga przekroczenia | B–F, H, L, M w wierszach 5–24 oraz limity B33–B37 |
| `Przychody` | 5 linii usług × 12 mies.: rozruch, sezonowość, obłożenie godzin | A6–D10, C14–N14 (sezonowość), C19–N19 (rozruch) |
| `Koszty` | koszty stałe, materiały, ZUS według etapu, składka zdrowotna, podatek; dwa bloki: bazowy i pesymistyczny | B9–B16, B20 |
| `Prognoza` | rachunek 12-miesięczny w pionie; miesiąc 0 (dotacja, wkład, zakupy); gotówka skumulowana; scenariusz pesymistyczny w kolumnach M–R; próg rentowności | nic |
| `Do-wniosku` | tabele do przepisania: kalkulacja miesięczna i kwartalna, specyfikacja wydatków, wskaźniki | nic |

Kolory: **żółte tło i niebieska czcionka** oznaczają dane wejściowe, **czarna czcionka** formułę w tym samym arkuszu, a **zielona** odwołanie do innego arkusza.

## 3. Jak liczony jest ZUS

Etap ZUS w danym miesiącu ustala `Koszty!C23:N23` według ustawień z `Zalozenia`:

1. **Ulga na start** (`UlgaStart = TAK`): przez pierwsze `MiesUlgi` miesięcy (domyślnie 6) składki społeczne wynoszą 0 zł. Składkę zdrowotną płaci się normalnie.
2. **Preferencyjny ZUS** (`Preferencyjny = TAK`): przez kolejne `MiesPref` miesięcy (domyślnie 24) podstawa wynosi 30% płacy minimalnej, czyli 1 441,80 zł. Bez Funduszu Pracy.
3. **Mały ZUS plus** (`MalyZUS = TAK`): działa dopiero po ulgach. Podstawa to wartość z `Zalozenia!B16`, ograniczona do przedziału 1 441,80–5 652 zł. Fundusz Pracy liczy się tylko wtedy, gdy podstawa jest ≥ płacy minimalnej. Uwaga: w pierwszym roku działalności Mały ZUS plus zwykle nie przysługuje.
4. **Pełny ZUS**: podstawa wynosi 60% prognozowanego przeciętnego wynagrodzenia, czyli 5 652 zł. Składki z chorobową i FP dają 1 926,76 zł miesięcznie.

Każda składka jest liczona osobno jako `ROUND(podstawa × stopa; 2)`. Stopy: emerytalna 19,52%, rentowa 8%, chorobowa 2,45% (tylko gdy `Chorobowe = TAK`), wypadkowa 1,67%, FP+FS 2,45%.

Przy domyślnych ustawieniach (ulga i preferencyjny ZUS) przez całe 12 miesięcy modelu klient płaci najwyżej preferencyjne składki. Pełny ZUS zaczyna się dopiero w 31. miesiącu. Dlatego `Prognoza!C29` pokazuje dodatkowo **próg rentowności po okresie ulg**. Komisje coraz częściej o niego pytają.

## 4. Jak liczona jest składka zdrowotna

| Forma | Mechanizm w modelu |
|---|---|
| skala | 9% × (przychód − koszty − składki społeczne) w danym miesiącu, nie mniej niż 432,54 zł |
| liniowy | 4,9% × ten sam dochód, nie mniej niż 432,54 zł. Zapłaconą składkę odlicza się od dochodu do limitu 14 100 zł rocznie (limit liczony narastająco w roku kalendarzowym) |
| ryczałt | kwota stała zależna od przychodu narastająco w roku kalendarzowym: ≤ 60 000 zł → 498,35 zł; 60 000–300 000 zł → 830,58 zł; > 300 000 zł → 1 495,04 zł. 50% zapłaconej składki odlicza się od przychodu |

## 5. Jak liczony jest podatek dochodowy

Model liczy zaliczki **narastająco w roku kalendarzowym**, tak jak robi to księgowa. Każdy rok podatkowy liczy się osobno: jeśli start przypada w trakcie roku, 1 stycznia narastanie zaczyna się od zera, a kwota wolna i próg skali działają od nowa.

1. Podstawa miesięczna:
   - skala i liniowy: przychód − koszty operacyjne − składki społeczne − (liniowy: odliczona składka zdrowotna);
   - ryczałt: przychód − składki społeczne − 50% składki zdrowotnej.
2. Podatek należny od podstawy narastającej (`Koszty!…podcum`):
   - **skala**: do 120 000 zł: `max(0; 12% × podstawa − 3 600)`; powyżej: `10 800 + 32% × nadwyżka`;
   - **liniowy**: `19% × max(0; podstawa)`;
   - **ryczałt**: `stawka × max(0; podstawa)` (stawka z `Zalozenia!B10`).
3. Zaliczka za miesiąc = podatek należny narastająco − zaliczki już wpłacone w tym roku, nie mniej niż 0. Strata w jednym miesiącu zmniejsza kolejne zaliczki, ale nie powoduje zwrotu w trakcie roku.

## 6. Kosztorys i przepływy gotówki

- **Kwota do rozliczenia** (kolumna K) to kwota brutto u osoby zwolnionej z VAT i kwota netto u czynnego podatnika VAT. Czynny podatnik odlicza VAT, a równowartość VAT od zakupów z dotacji zwraca do PUP, więc w modelu VAT jest neutralny.
- Pozycje z finansowaniem „dotacja” sumują się w `KosztorysDotacja` i są porównywane z kwotą dotacji. Każda kategoria (sprzęt, towar, reklama, remont, inne) jest porównywana z limitem % z regulaminu PUP. Limity w pliku są **przykładowe**: wpisz te z regulaminu urzędu klienta.
- **Miesiąc 0** w `Prognoza`: + dotacja + wkład własny − wszystkie zakupy z kosztorysu. Od miesiąca 1 do gotówki dochodzi wynik netto.
- Zakupy z kosztorysu **nie są kosztem w rachunku wyników** (brak amortyzacji). Wydatki sfinansowane zwolnioną z podatku dotacją nie są kosztem podatkowym, a zakupy z wkładu własnego są w przykładzie drobne. To podejście ostrożne: podatek wychodzi raczej trochę wyższy niż niższy.

## 7. Przeliczenie i kontrola po zmianach w generatorze

```bash
python3 model-finansowy/build_model.py
python3 <katalog-skilla-xlsx>/scripts/recalc.py model-finansowy/model-finansowy-pup.xlsx 60
```

`recalc.py` musi zwrócić `"status": "success"` i `"total_errors": 0`. Wynik dla wersji z 14.10.2026: **1 929 formuł, 0 błędów**. Przetestowano też warianty: skala, liniowy, pełny ZUS od startu, Mały ZUS plus, czynny VAT ze startem w lipcu (przejście roku podatkowego). W żadnym nie pojawił się błąd formuły.

## 8. Nazwane komórki dla szablonów tekstowych (`ark_*`)

Szablony w `szablony/` odwołują się do tych nazw. Wartość czytasz z przeliczonego pliku, np. przez `openpyxl` z `data_only=True`. Sufiks `_pes` oznacza scenariusz pesymistyczny.

| Nazwa | Znaczenie | Przykład (fryzjerka) |
|---|---|---|
| `ark_przychod_12m` | przychody w 12 mies. | 87 415 zł |
| `ark_koszty_12m` | koszty z ZUS i zdrowotną (bez podatku) | 38 084 zł |
| `ark_zysk_brutto_12m` | wynik przed opodatkowaniem | 49 331 zł |
| `ark_podatek_12m` | podatek dochodowy | 6 902 zł |
| `ark_zysk_netto_12m` | zysk netto w 12 mies. | 42 429 zł |
| `ark_zysk_netto_mies` | średni zysk netto miesięcznie | 3 536 zł |
| `ark_rentownosc` | zysk netto ÷ przychody | 48,5% |
| `ark_prog_rent_zl` / `ark_prog_rent_szt` | próg rentowności (zł/mies. i liczba sprzedaży/mies.) | 2 613 zł / 32 usługi |
| `ark_prog_rent_pelny_zus` | próg rentowności po okresie ulg | 4 543 zł |
| `ark_margines` / `ark_margines_pes` | margines bezpieczeństwa | 68% / 55% |
| `ark_zwrot_z_dotacji` | zysk netto roczny ÷ dotacja | 163% |
| `ark_okres_zwrotu_mies` | dotacja ÷ średni zysk netto | 7,4 mies. |
| `ark_gotowka_m12`, `ark_min_saldo` | gotówka na koniec m12, najniższe saldo | 43 097 zł / 668 zł |
| `ark_pierwszy_mies_zysku` | pierwszy miesiąc z zyskiem netto | 1 |
| `ark_przychod_12m_pes`, `ark_zysk_netto_12m_pes`, … | to samo dla przychodów −30% | 61 191 zł / 22 536 zł |
| `ark_przychod_sredni_od_m4` | średni przychód miesięczny po rozruchu | 8 246 zł |
| `ark_koszty_stale_mies` | koszty stałe miesięcznie (bez ZUS) | 1 490 zł |
| `ark_materialy_pct` | materiały jako % przychodu | 12% |
| `ark_zus_m12` | składki społeczne w 12. miesiącu | 456,18 zł |
| `ark_zdrowotna_12m` | składka zdrowotna w 12 mies. | 6 977 zł |
| `ark_oblozenie_max` | najwyższe obłożenie czasu pracy | 86% |
| `ark_reklama_mies` | miesięczny budżet reklamy | 250 zł |
| `ark_dotacja`, `ark_wklad_wlasny` | kwota dotacji, wkład własny | 26 000 zł / 3 000 zł |
| `ark_kosztorys_razem`, `ark_kosztorys_dotacja`, `ark_kosztorys_wklad` | zakupy: razem / z dotacji / z wkładu | 28 332 zł / 25 995 zł / 2 337 zł |
| `ark_kat_sprzet`, `ark_kat_towar`, `ark_kat_reklama`, `ark_kat_remont`, `ark_kat_inne` | zakupy z dotacji według kategorii | 13 695 / 6 150 / 4 674 / 0 / 1 476 zł |

Pozostałe nazwy (`Dotacja`, `WkladWlasny`, `DataStartu`, `FormaOpodatkowania`, `PlacaMin`, `ZdrMin` itd.) widać w menedżerze nazw (Excel: Formuły → Menedżer nazw).

## 9. Znane uproszczenia (powiedz o nich klientowi, jeśli mają znaczenie)

1. **Stałe 2026 przez całe 12 miesięcy.** Przy starcie w grudniu 2026 r. 11 miesięcy przypada na 2027 r. Od 01.01.2027 zmienią się płaca minimalna i podstawy ZUS, a od 02.2027 składka zdrowotna. Gdy kwoty na 2027 r. zostaną ogłoszone, zrób kopię arkusza `Stale-2026` z nowymi wartościami.
2. **Składka zdrowotna na skali i liniowym** liczona jest od dochodu z tego samego miesiąca. W rzeczywistości liczy się ją od dochodu z miesiąca poprzedniego, a rok rozlicza się w zeznaniu rocznym. Na sumę roczną wpływa to w niewielkim stopniu.
3. **Ryczałt: jedna stawka.** Model nie dzieli przychodu na części opodatkowane różnymi stawkami. Nie uwzględnia też 12,5% od nadwyżki przychodów z niektórych usług ponad 100 000 zł rocznie (status: [do weryfikacji]). Próg składki zdrowotnej liczony jest od przychodu brutto, bez pomniejszeń.
4. **Brak amortyzacji i brak kosztów podatkowych z zakupów kosztorysowych** (patrz pkt 6).
5. **VAT neutralny:** przepływy liczone są netto u czynnego podatnika VAT. Model nie pokazuje przesunięć czasowych rozliczeń VAT.
6. **Limit zwolnienia z VAT** w roku startu liczony jest proporcjonalnie do dni. Przychód w modelu jest przypisany do miesięcy, a nie do dni.
7. **Brak wynagrodzeń pracowników** i kosztów zatrudnienia. Model jest przeznaczony dla jednoosobowej działalności. Pracownika dopisz jako koszt stały w „Inne”, z ZUS pracodawcy.
8. **Wypadkowa 1,67%** dotyczy płatników zgłaszających do 9 osób. Model nie obsługuje innych stóp.
9. **Liczba sprzedaży jest zaokrąglana do całych sztuk** w każdym miesiącu, więc przy małych ilościach sezonowość może dawać skoki o ±1.
10. **Brak kosztów życia właściciela.** Zysk netto to dochód właściciela przed jego prywatnymi wydatkami. Komisje pytają, czy wystarczy na utrzymanie: odpowiedź opisz w sekcji 08 lub 09.

## 10. Czego nie robić

- Nie wpisuj liczb w komórki z formułami (czarne i zielone), bo zepsujesz spójność wniosku.
- Nie zaokrąglaj „na oko” liczb przepisywanych do formularza. Arkusz `Do-wniosku` wyświetla kwoty w pełnych złotych.
- Nie zmieniaj stałych w `Stale-2026` bez wpisania nowego źródła i daty w kolumnach D–F.
