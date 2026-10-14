# 03 – Analiza rynku i klientów

> Typowe nazwy pola: „Analiza rynku”, „Charakterystyka rynku i potencjalnych klientów”, „Rynek docelowy i popyt”, „Do kogo skierowana jest oferta”.
> Sekcja odpowiada na pytanie: **czy na tym terenie są ludzie lub firmy, które zapłacą za Twoją usługę, i skąd to wiesz.**

## 1. Cel sekcji

Pokazać komisji, że:
1. znasz swoich klientów z nazwy segmentu i z miejsca (osiedle, gmina, typ firmy);
2. wiesz, **jak daleko** sięga Twoja działalność;
3. masz **dowody popytu** z własnego rozpoznania (rozmowy, zapytania, listy intencyjne, ankieta, dawni klienci), a nie tylko ogólne stwierdzenia;
4. wiesz, jak popyt **zmienia się w ciągu roku**, i masz to uwzględnione w prognozie (arkusz: `Przychody`, sezonowość).

## 2. Dane wejściowe z kwestionariusza

| Kod | Dane | Uwagi |
|---|---|---|
| K6 | zasięg (km), lista obsługiwanych miejscowości lub osiedli | nazwy, nie „okolice” |
| K7 | segmenty klientów (kto, ile, gdzie), z jakich powodów kupują | 2–4 segmenty |
| K7 | dane liczbowe o terenie **podane przez klienta lub właściciela** (liczba mieszkańców, mieszkań, firm, z podaniem źródła, np. GUS BDL, gmina) | model sam ich nie wyszukuje |
| K7 | dowody popytu: listy intencyjne (od kogo, na co), zapytania, ankieta (liczba odpowiedzi), dawni klienci | z liczbami |
| K7 | sezonowość: które miesiące są mocne, a które słabe i dlaczego | zgodnie z arkuszem `Przychody!C14:N14` |
| K8 | (1 zdanie) czy rynek jest zajęty | szczegóły w sekcji 04 |
| arkusz | mnożniki sezonowe, przychód miesięczny | do zdania o sezonowości; bez liczenia |

Liczby o rynku (mieszkańcy, firmy, ceny) pochodzą **wyłącznie** z kwestionariusza albo z notatki właściciela dołączonej do kwestionariusza. Model nie podaje statystyk „z pamięci”. Gdy ich brak, wstawia `[BRAK DANYCH: liczba mieszkańców gminy X – źródło GUS BDL]`.

## 3. Struktura

1. **Obszar działania:** miejscowości, zasięg, liczby (jeśli podane) i sposób dotarcia (dojazd, lokal).
2. **Segmenty klientów:** dla każdego 2–3 zdania: kto, ilu (jeśli wiadomo), czego potrzebuje, jak często kupuje, ile może zapłacić.
3. **Dowody popytu:** konkretnie: „2 listy intencyjne: …”, „ankieta w grupie … – 46 odpowiedzi, 19 osób zainteresowanych”, „lista 40 stałych klientek”.
4. **Sezonowość:** mocne i słabe miesiące, powód, co robisz w słabych miesiącach. Odwołanie do założeń arkusza bez podawania mnożników.
5. **Wniosek:** jedno zdanie łączące popyt z planem sprzedaży, bez obietnic.

## 4. Długość – trzy warianty

| Wariant | Znaki | Co zawiera |
|---|---|---|
| krótki | ~800 | obszar (1 zdanie), 2 główne segmenty po 1 zdaniu, 1–2 najmocniejsze dowody popytu, sezonowość w 1 zdaniu |
| standard | ~2000 | pełna struktura 1–5; 3–4 segmenty; wszystkie dowody popytu |
| długi | ~4000 | jak standard + szersza charakterystyka terenu (dane z K7 ze źródłem), opis potrzeb każdego segmentu na przykładach sytuacji, plan na słabe miesiące, tabela segmentów (segment / liczba / częstotliwość / dowód) |

## 5. Co punktuje komisja

- **Dowody, nie deklaracje.** Listy intencyjne, zapytania ofertowe i przedwstępne umowy są przez wiele PUP punktowane osobno albo sprawdzane na rozmowie.
- **Realny zasięg** dopasowany do sprzętu i transportu z kosztorysu (bez auta nie obsłuży się 6 gmin).
- **Segmenty, które da się policzyć** („38 wspólnot u jednego zarządcy”), a nie „osoby w każdym wieku”.
- **Świadomość sezonowości** i jej odbicie w prognozie. Prognoza z płaską sprzedażą przez 12 miesięcy w branży sezonowej budzi wątpliwości.

## 6. Typowe błędy

- Statystyki krajowe zamiast lokalnych („Polacy wydają rocznie X mld zł na…”).
- „Klientami będą wszyscy mieszkańcy”.
- Dowody popytu bez liczb („wiele osób było zainteresowanych”).
- Wpisanie listów intencyjnych, których klient nie ma. To najszybszy sposób na utratę wiarygodności na rozmowie.

## 7. Prompt sekcji

```text
SEKCJA 03 – ANALIZA RYNKU I KLIENTÓW
Napisz treść pola "{{pole_formularza}}" (limit: {{limit_znakow}}, ton: {{ton}}).
Kolejność: (1) obszar działania – nazwy miejscowości/osiedli i zasięg z K6, liczby o terenie
tylko z K7 (ze źródłem, jeśli podane); (2) segmenty klientów z K7 – kto, ilu, czego
potrzebuje, jak często kupuje; (3) dowody popytu z K7 – dokładnie tak, jak je opisano (kto,
ile, kiedy); (4) sezonowość z K7 – mocne i słabe miesiące, powód, co robię w słabych
miesiącach; (5) jedno zdanie wniosku – bez obietnic.
Nie podawaj żadnych statystyk spoza kwestionariusza. Nie twórz listów intencyjnych, ankiet,
liczby zainteresowanych. Brak danych o terenie = [BRAK DANYCH: …].
W wariancie długim możesz dodać tabelę: segment | liczba/zakres | jak często | dowód.
```

## 8. Przykład wypełnienia – firma sprzątająca

> **DANE FIKCYJNE – PRZYKŁAD.** Zielonów, Osiedle Słoneczne, „Admin-Dom”, „Fizjo-Ruch”, „Bilans” i wszystkie liczby są wymyślone.

**Skrót kwestionariusza:** Katarzyna, Zielonów. Usługi: sprzątanie mieszkań i domów, małych biur i gabinetów, klatek schodowych, sprzątanie po remontach. Zasięg: Zielonów oraz Borków i Lipy (do 15 km, dojazd do 20 minut, własne auto). Dane z notatki właściciela: Zielonów ok. 28 tys. mieszkańców (GUS BDL 2025). Na Osiedlu Słonecznym oddano w latach 2023–2026 ok. 420 mieszkań (informacja dewelopera). Zarządca „Admin-Dom” obsługuje 38 wspólnot. Obecnie klatki sprząta firma z miasta wojewódzkiego, a zarząd jednej wspólnoty skarżył się na nieregularność. Dowody: 2 listy intencyjne: gabinet fizjoterapii „Fizjo-Ruch” (sprzątanie 3 razy w tygodniu) i biuro rachunkowe „Bilans” (2 razy w tygodniu). Ankieta w grupie FB mieszkańców Osiedla Słonecznego (09.2026): 46 odpowiedzi, 19 osób zainteresowanych sprzątaniem co 2 tygodnie; odpowiadali głównie pracujący rodzice i pary 30–45 lat („nie mamy czasu w tygodniu, a soboty szkoda”). 3 biura nieruchomości zlecają sprzątanie mieszkań przed sprzedażą lub najmem. Sezonowość: szczyt w marcu–kwietniu i listopadzie–grudniu (okna, porządki przedświąteczne), słabiej w lipcu i sierpniu w mieszkaniach (urlopy), biura stabilne przez cały rok.

### Wariant standard (~2000 znaków), ton: rzeczowy

```text
Będę działać w Zielonowie, który ma ok. 28 tys. mieszkańców (GUS BDL, 2025 r.), oraz w sąsiednich gminach Borków i Lipy, w promieniu do 15 km. Wszędzie dojadę w ciągu 20 minut.

Moja oferta jest skierowana do czterech grup klientów.

1. Mieszkańcy nowych osiedli. Na samym Osiedlu Słonecznym w latach 2023–2026 oddano ok. 420 mieszkań. Z mojej ankiety wynika, że to głównie pracujący rodzice i pary w wieku 30–45 lat. Jak napisała jedna z osób: „nie mamy czasu w tygodniu, a soboty szkoda”.
2. Wspólnoty mieszkaniowe. Zarządca „Admin-Dom” obsługuje 38 wspólnot w Zielonowie. Klatki sprząta dziś firma z miasta wojewódzkiego, a zarząd jednej ze wspólnot skarżył się na nieregularne terminy. Lokalna firma, która jest na miejscu w razie potrzeby, ma tu szansę na zlecenie.
3. Małe biura i gabinety. Potrzebują sprzątania po godzinach, 2–3 razy w tygodniu, przez cały rok. To będzie stała podstawa moich przychodów.
4. Sprzątanie po remontach i przed sprzedażą lub najmem mieszkań. Takie zlecenia przekazują trzy biura nieruchomości z Zielonowa.

Popyt sprawdziłam przed złożeniem wniosku. Mam dwa listy intencyjne: od gabinetu fizjoterapii „Fizjo-Ruch” (sprzątanie 3 razy w tygodniu) i od biura rachunkowego „Bilans” (2 razy w tygodniu). We wrześniu 2026 r. przeprowadziłam ankietę w grupie mieszkańców Osiedla Słonecznego na Facebooku. Odpowiedziało 46 osób, a 19 z nich chce regularnego sprzątania co dwa tygodnie.

Popyt zmienia się w ciągu roku. Najwięcej pracy jest w marcu i kwietniu oraz w listopadzie i grudniu, kiedy klienci zamawiają mycie okien i porządki przed świętami. W lipcu i sierpniu część klientów indywidualnych wyjeżdża na urlopy. Wtedy więcej czasu poświęcę na sprzątanie klatek i zlecenia od biur nieruchomości. Biura i gabinety zamawiają usługi równo przez cały rok. Tę zmienność uwzględniłam w prognozie sprzedaży.

Stałe zlecenia z biur, zainteresowanie z ankiety i zlecenia sezonowe pozwalają mi zaplanować pracę od pierwszego miesiąca działalności.
```

### Na co zwrócić uwagę w przykładzie

- Każda liczba ma źródło w skrócie kwestionariusza (GUS BDL, deweloper, zarządca, ankieta).
- Sezonowość ma powód i plan na słabe miesiące, a zdanie o prognozie nie podaje mnożników.
- Ostatnie zdanie jest wnioskiem, a nie obietnicą („pozwalają zaplanować”, a nie „gwarantują sukces”).
- Nie ma ogólników typu „rosnące zapotrzebowanie na usługi sprzątania”.
