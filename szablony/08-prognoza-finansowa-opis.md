# 08 – Prognoza finansowa: komentarz słowny do liczb z arkusza

> Typowe nazwy pola: „Uzasadnienie przyjętych założeń finansowych”, „Opis prognozy przychodów i kosztów”, „Efektywność ekonomiczna przedsięwzięcia”, „Komentarz do kalkulacji”.
> Tabele liczbowe przepisuje się z arkusza `Do-wniosku`. Ta sekcja **wyjaśnia słowami, skąd te liczby się wzięły**. Model **nie liczy żadnej wartości**: każda liczba finansowa to zmienna `{{ark_…}}`.

## 1. Cel sekcji

Przekonać komisję, że prognoza jest **realna i ostrożna**:
1. przychody wynikają z cen × liczby usług, z rozruchem i sezonowością;
2. koszty są kompletne (w tym ZUS po okresie ulg, składka zdrowotna, podatek);
3. firma osiąga **próg rentowności**, a zysk wystarcza na utrzymanie;
4. przy przychodach **o 30% niższych** firma nadal się utrzyma (albo wiadomo, co wtedy zrobisz);
5. gotówki nie zabraknie na starcie.

## 2. Dane wejściowe – zmienne z arkusza

| Zmienna | Znaczenie | Gdzie w arkuszu |
|---|---|---|
| `{{ark_przychod_12m}}` / `_pes` | przychody w 12 mies. (bazowy / −30%) | `Do-wniosku` |
| `{{ark_koszty_12m}}` / `_pes` | koszty z ZUS i zdrowotną (bez podatku) | `Do-wniosku` |
| `{{ark_zysk_netto_12m}}` / `_pes` | zysk netto | `Do-wniosku` |
| `{{ark_zysk_netto_mies}}` / `_pes` | średni zysk netto miesięcznie | `Do-wniosku` |
| `{{ark_podatek_12m}}` | podatek dochodowy w 12 mies. | `Do-wniosku` |
| `{{ark_przychod_sredni_od_m4}}` | średni przychód miesięczny po rozruchu | `Prognoza!C30` |
| `{{ark_koszty_stale_mies}}` | koszty stałe miesięcznie (bez ZUS) | `Koszty!C17` |
| `{{ark_materialy_pct}}` | materiały jako % przychodu | `Koszty!B20` |
| `{{ark_zus_m12}}` | składki społeczne w 12. miesiącu | `Koszty!N30` |
| `{{ark_zdrowotna_12m}}` | składka zdrowotna w 12 mies. | `Koszty` |
| `{{ark_prog_rent_zl}}`, `{{ark_prog_rent_szt}}` | próg rentowności (zł/mies., usług/mies.) | `Prognoza!C26`, `C28` |
| `{{ark_prog_rent_pelny_zus}}` | próg rentowności po okresie ulg ZUS | `Prognoza!C29` |
| `{{ark_margines}}` / `_pes` | margines bezpieczeństwa | `Prognoza!C31`, `C33` |
| `{{ark_pierwszy_mies_zysku}}` | pierwszy miesiąc z zyskiem netto | `Prognoza!C34` |
| `{{ark_min_saldo}}` / `_pes`, `{{ark_gotowka_m12}}` | najniższe saldo gotówki, gotówka na koniec m12 | `Do-wniosku` |
| `{{ark_oblozenie_max}}` | najwyższe obłożenie czasu pracy | `Zalozenia!B33` |
| `{{ark_dotacja}}`, `{{ark_wklad_wlasny}}`, `{{ark_okres_zwrotu_mies}}` | dotacja, wkład, okres zwrotu dotacji | `Zalozenia`, `Do-wniosku` |

Z kwestionariusza i arkusza (dane wejściowe, wolno przepisać dosłownie):
- ceny usług i liczba usług przy pełnym obłożeniu (`Przychody!A6:D10`),
- współczynnik rozruchu (`Przychody!C19:N19`, np. 40% / 60% / 80% / 100%),
- opis sezonowości (K7) i jej uzasadnienie,
- forma opodatkowania, wariant ZUS (`Zalozenia`),
- K11: inne dochody gospodarstwa i miesięczne potrzeby życiowe (jeśli podane).

## 3. Struktura

1. **Założenia przychodów:** usługi i ceny, liczba usług przy pełnym obłożeniu, skąd te liczby (K7: dawni klienci, listy intencyjne), rozruch, sezonowość, obłożenie czasu pracy (`{{ark_oblozenie_max}}`).
2. **Założenia kosztów:** koszty stałe `{{ark_koszty_stale_mies}}`, materiały `{{ark_materialy_pct}}` przychodu, ZUS (ulga na start → preferencyjny, `{{ark_zus_m12}}` w 12. miesiącu), składka zdrowotna, forma opodatkowania.
3. **Wynik:** przychody, koszty, zysk netto w 12 mies. i średnio na miesiąc, pierwszy miesiąc z zyskiem.
4. **Próg rentowności:** kwota i liczba usług miesięcznie, porównanie ze średnim przychodem po rozruchu (margines bezpieczeństwa), próg po okresie ulg ZUS.
5. **Scenariusz pesymistyczny (−30%):** przychody, zysk netto, najniższe saldo gotówki. **Co wtedy zrobisz** (z K12, np. dodatkowa usługa, cięcie kosztów, praca w soboty).
6. **Płynność i utrzymanie:** saldo na starcie (dotacja + wkład − zakupy), gotówka po 12 miesiącach, czy zysk pokrywa potrzeby życiowe (K11).

## 4. Długość – warianty

| Wariant | Znaki | Co zawiera |
|---|---|---|
| krótki | ~800 | 1 zdanie o założeniach przychodów, zysk netto roczny i miesięczny, próg rentowności, 1 zdanie o scenariuszu −30% |
| standard | ~2000 | pełna struktura 1–6, zwięźle |
| długi | ~4000 | jak standard + omówienie każdej linii przychodu, kosztów stałych pozycja po pozycji (z kwotami wejściowymi), mechanizm ZUS i podatku słowami, próg rentowności po ulgach i plan na 2. rok, szczegółowy plan działań w scenariuszu pesymistycznym |

## 5. Co punktuje komisja

- **Realizm przychodów:** liczba usług możliwa do wykonania w czasie pracy (obłożenie < 100%), ceny zgodne z sekcją 04, rozruch zamiast pełnej sprzedaży od 1. miesiąca.
- **Kompletność kosztów:** ZUS i zdrowotna, paliwo, księgowość, ubezpieczenie. Pominięcie ZUS jest najczęstszym powodem obniżenia oceny.
- **Spójność:** liczby w opisie = tabele z `Do-wniosku` = kosztorys.
- **Analiza wrażliwości:** pytanie „co, jeśli przychody będą o 30% niższe?” pada na wielu komisjach.
- **Perspektywa po ulgach ZUS:** czy firma utrzyma się, gdy składki wzrosną do pełnych (dla PUP ważne jest utrzymanie działalności co najmniej 12 mies., a dla wnioskodawcy znacznie dłużej).

## 6. Typowe błędy

- Liczby w opisie, których nie ma w tabelach (np. inny zysk).
- Przychody „z sufitu”: brak związku z cenami i liczbą klientów.
- Brak kosztów życia właściciela w ocenie, czy firma się opłaca.
- Optymistyczne sformułowania: „zysk na pewno wyniesie…”.

## 7. Prompt sekcji

```text
SEKCJA 08 – PROGNOZA FINANSOWA (KOMENTARZ)
Napisz treść pola "{{pole_formularza}}" (limit: {{limit_znakow}}, ton: {{ton}}).
WSZYSTKIE kwoty, sumy, procenty, progi i salda wstawiaj WYŁĄCZNIE jako zmienne {{ark_…}} z
<arkusz>. Nie licz niczego (nie dodawaj, nie odejmuj, nie licz procentów ani różnic między
scenariuszami). Wolno przepisać dosłownie: ceny usług, liczby usług przy pełnym obłożeniu,
współczynniki rozruchu, nazwy miesięcy sezonu.
Kolejność: (1) założenia przychodów – ceny × liczba usług, skąd te liczby (K7), rozruch,
sezonowość, {{ark_oblozenie_max}}; (2) założenia kosztów – {{ark_koszty_stale_mies}},
{{ark_materialy_pct}}, wariant ZUS z <parametry>, {{ark_zus_m12}}, składka zdrowotna, forma
opodatkowania; (3) wynik – {{ark_przychod_12m}}, {{ark_koszty_12m}}, {{ark_zysk_netto_12m}},
{{ark_zysk_netto_mies}}, {{ark_pierwszy_mies_zysku}}; (4) próg rentowności – {{ark_prog_rent_zl}},
{{ark_prog_rent_szt}}, {{ark_przychod_sredni_od_m4}}, {{ark_margines}}, {{ark_prog_rent_pelny_zus}};
(5) scenariusz −30% – {{ark_przychod_12m_pes}}, {{ark_zysk_netto_12m_pes}},
{{ark_zysk_netto_mies_pes}}, {{ark_min_saldo_pes}} + działania z K12; (6) płynność i utrzymanie –
{{ark_min_saldo}}, {{ark_gotowka_m12}}, potrzeby życiowe z K11.
Jeśli w K12 brak działań na wypadek niższych przychodów – [BRAK DANYCH: co zrobię, gdy
przychody będą o 30% niższe]. Jeśli w K11 brak kosztów życia – [BRAK DANYCH: miesięczne
wydatki domowe].
Bez słów: "na pewno", "gwarantuje", "pewny zysk".
```

## 8. Przykład wypełnienia – fryzjerka mobilna (liczby z arkusza przykładowego)

> **DANE FIKCYJNE – PRZYKŁAD.** Liczby pochodzą z `model-finansowy-pup.xlsx` w wersji przykładowej (start 01.12.2026, ryczałt 8,5%, ulga na start + preferencyjny ZUS, zwolnienie z VAT). Tekst zawiera zmienne, a tabela pod nim pokazuje wartości podstawione przez system.

**Skrót kwestionariusza:** usługi i ceny jak w arkuszu `Przychody` (strzyżenie damskie 80 zł – 30/mies.; męskie i dziecięce 45 zł – 30; koloryzacja 200 zł – 12; upięcia 220 zł – 5; strzyżenie w DPS 40 zł – 20). Podstawa liczby usług: ok. 40 stałych klientek z salonu zadeklarowało przejście do niej, a umowa z DPS „Pod Lipami” trwa od 2022 r. Rozruch 40% / 60% / 80%, od 4. miesiąca 100%. Sezon: grudzień, maj–czerwiec (śluby, komunie) mocniejsze, styczeń–luty słabsze. K12 – gdy przychody spadną: zaproponuje strzyżenie w drugim DPS w gminie Lipy i w zakładzie opiekuńczym w Zielonowie, wprowadzi pakiety dla rodzin (strzyżenie 3–4 osób podczas jednej wizyty), ograniczy płatną reklamę. K11: mąż pracuje na etacie; wydatki domowe pokrywa jego pensja, a od firmy potrzebuje min. 2 000 zł miesięcznie.

### Wariant standard (~2000 znaków), ton: rzeczowy

```text
Przychody policzyłam jako cenę usługi pomnożoną przez liczbę usług w miesiącu. Przy pełnym obłożeniu zakładam 30 strzyżeń damskich po 80 zł, 30 strzyżeń męskich i dziecięcych po 45 zł, 12 koloryzacji po 200 zł, 5 upięć po 220 zł i 20 strzyżeń w DPS po 40 zł. Opieram się na deklaracjach ok. 40 stałych klientek z salonu i na umowie z DPS „Pod Lipami”, którą mam od 2022 r. W pierwszym miesiącu przyjęłam 40% tej sprzedaży, w drugim 60%, w trzecim 80%, a pełną sprzedaż od czwartego miesiąca. Uwzględniłam sezon: więcej pracy w grudniu oraz w maju i czerwcu, mniej w styczniu i lutym. W najbardziej pracowitym miesiącu wykorzystam {{ark_oblozenie_max}} czasu przeznaczonego na pracę u klientów.

Koszty stałe wyniosą {{ark_koszty_stale_mies}} miesięcznie, głównie paliwo, księgowość i reklama. Materiały to {{ark_materialy_pct}} przychodu. Przez pierwsze 6 miesięcy skorzystam z ulgi na start, a potem zapłacę preferencyjne składki ZUS ({{ark_zus_m12}} w 12. miesiącu). Składka zdrowotna w pierwszym roku to {{ark_zdrowotna_12m}}. Rozliczam się ryczałtem 8,5%.

W ciągu 12 miesięcy zakładam {{ark_przychod_12m}} przychodu i {{ark_koszty_12m}} kosztów. Zysk netto po podatku wyniesie {{ark_zysk_netto_12m}}, czyli średnio {{ark_zysk_netto_mies}} miesięcznie. Zysk powinien pojawić się już w miesiącu nr {{ark_pierwszy_mies_zysku}}.

Próg rentowności to {{ark_prog_rent_zl}} przychodu miesięcznie, czyli ok. {{ark_prog_rent_szt}} usług. Po okresie rozruchu planuję średnio {{ark_przychod_sredni_od_m4}} miesięcznie, więc margines bezpieczeństwa wynosi {{ark_margines}}. Po zakończeniu ulg w ZUS próg wzrośnie do {{ark_prog_rent_pelny_zus}} miesięcznie.

Sprawdziłam też wariant z przychodami niższymi o 30%. Przychody wyniosłyby wtedy {{ark_przychod_12m_pes}}, a zysk netto {{ark_zysk_netto_12m_pes}}, czyli średnio {{ark_zysk_netto_mies_pes}} miesięcznie. W takiej sytuacji zaproponuję usługi drugiemu DPS w gminie Lipy i zakładowi opiekuńczemu w Zielonowie, wprowadzę pakiety dla rodzin i ograniczę płatną reklamę.

Po zakupach z dotacji i wkładu własnego zostanie mi {{ark_min_saldo}} gotówki. Od pierwszego miesiąca saldo będzie rosło. Wydatki domowe pokrywa pensja męża, a od firmy potrzebuję co najmniej 2 000 zł miesięcznie.
```

**Wartości podstawione z arkusza przykładowego:**

| Zmienna | Wartość | Zmienna | Wartość |
|---|---|---|---|
| `ark_oblozenie_max` | 86% | `ark_prog_rent_zl` | 2 613 zł |
| `ark_koszty_stale_mies` | 1 490 zł | `ark_prog_rent_szt` | 32 |
| `ark_materialy_pct` | 12% | `ark_przychod_sredni_od_m4` | 8 246 zł |
| `ark_zus_m12` | 456,18 zł | `ark_margines` | 68% |
| `ark_zdrowotna_12m` | 6 977 zł | `ark_prog_rent_pelny_zus` | 4 543 zł |
| `ark_przychod_12m` | 87 415 zł | `ark_przychod_12m_pes` | 61 191 zł |
| `ark_koszty_12m` | 38 084 zł | `ark_zysk_netto_12m_pes` | 22 536 zł |
| `ark_zysk_netto_12m` | 42 429 zł | `ark_zysk_netto_mies_pes` | 1 878 zł |
| `ark_zysk_netto_mies` | 3 536 zł | `ark_min_saldo` | 668 zł |
| `ark_pierwszy_mies_zysku` | 1 | | |

### Na co zwrócić uwagę w przykładzie

- Żadna kwota finansowa nie jest wpisana ręcznie. Wyjątkiem są ceny i liczby usług (dane wejściowe) oraz 2 000 zł z K11.
- Zdanie o minimalnym dochodzie z K11 (2 000 zł) pozwala komisji samodzielnie porównać go ze zmiennymi `ark_zysk_netto_mies` i `_pes`. Model nie pisze „to wystarczy”, bo byłoby to porównanie liczb, czyli obliczenie.
- **Uwaga dla weryfikującego:** niskie saldo na starcie (`ark_min_saldo` = 668 zł) to słaby punkt przykładu. Przed oddaniem wniosku warto zwiększyć wkład własny albo przesunąć część zakupów. Komisja może dopytać, z czego pokryte zostaną koszty pierwszego miesiąca.
- Margines 68% wynika z niskich składek ZUS w okresie ulg. Dlatego tekst podaje też próg po ulgach. To uczciwe wobec komisji i przygotowuje klientkę do pytania o 3. rok działalności.
