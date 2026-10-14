# 05 – Plan marketingowy (promocja i pozyskanie klientów)

> Typowe nazwy pola: „Plan marketingowy”, „Sposób pozyskania klientów”, „Promocja i reklama”, „Strategia sprzedaży”.
> Komisja sprawdza tu, **czy wiesz, skąd wezmą się pierwsi klienci** i czy budżet na reklamę zgadza się z kosztorysem i prognozą kosztów.

## 1. Cel sekcji

Opisać konkretnie:
1. **kanały,** czyli gdzie i jak dotrzesz do każdego segmentu z sekcji 03;
2. **budżet:** jednorazowy (pozycje reklamowe z kosztorysu) i miesięczny (koszt reklamy w arkuszu);
3. **pierwsze 90 dni:** co zrobisz przed startem, w 1., 2. i 3. miesiącu, z mierzalnym celem;
4. **jak utrzymasz klientów** (polecenia, abonamenty, przypomnienia).

## 2. Dane wejściowe

| Źródło | Dane |
|---|---|
| K9 | kanały promocji wskazane przez klienta (konkretne grupy FB, tablice ogłoszeń, parafia, lokalna gazeta, Google, Booksy, OLX, współprace) |
| K9 | pierwsze działania, terminy, cele (np. liczba klientów) |
| K7 | segmenty klientów, żeby dopasować kanał do segmentu |
| K10 / arkusz `Kosztorys` | pozycje kategorii „reklama”: nazwy i ceny (np. logo, strona, oklejenie auta, ulotki) |
| arkusz | `{{ark_reklama_mies}}`: miesięczny budżet reklamy (`Koszty!B15`); `{{ark_reklama_kosztorys_dotacja}}`: suma reklamy z dotacji |
| K5 | ceny i ewentualne promocje startowe (tylko jeśli podane) |

## 3. Struktura

1. **Zdanie wprowadzające:** do kogo kierujesz promocję (segmenty z 03) i jaki jest główny kanał.
2. **Kanały:** dla każdego jedno zdanie *co dokładnie* + *dla którego segmentu*. Nazwy: „grupa FB »Borków i okolice« (8 tys. członków)”, a nie „media społecznościowe”.
3. **Budżet:** pozycje jednorazowe z kosztorysu (nazwa + cena z K10) i budżet miesięczny `{{ark_reklama_mies}}`. Bez sumowania przez model.
4. **Plan 90 dni:** lista albo tabela: *Przed startem / Miesiąc 1 / Miesiąc 2 / Miesiąc 3*, z działaniem i celem (np. „10 stałych klientów”). Cele tylko z K9; jeśli ich brak, wstaw znacznik.
5. **Utrzymanie klientów:** polecenia, karta stałego klienta, abonament, przypomnienia SMS (tylko te z K9).

## 4. Długość – trzy warianty

| Wariant | Znaki | Co zawiera |
|---|---|---|
| krótki | ~800 | 3–4 kanały w zdaniach, budżet miesięczny, 1 zdanie o pierwszym kwartale |
| standard | ~2000 | pełna struktura 1–5; plan 90 dni jako lista |
| długi | ~4000 | jak standard + tabela 90 dni (działanie / kanał / koszt / cel), opis przekazu reklamowego (co komunikujesz), mierzenie efektów (skąd klient się dowiedział), plan na miesiące 4–12 |

## 5. Co punktuje komisja

- **Kanały dopasowane do segmentów i terenu.** Dla seniorów sprawdzą się parafia, ulotki w przychodni i DPS. Dla młodych rodzin grupy osiedlowe na FB. Dla firm wizyta osobista i oferta e-mailem.
- **Spójność liczb:** pozycje reklamowe w opisie = pozycje w kosztorysie, a budżet miesięczny = koszt reklamy w prognozie.
- **Mierzalny plan startu:** komisje chętnie pytają: „skąd weźmie Pan pierwszych 10 klientów?”.
- **Tanie i sprawdzone działania lokalne** (polecenia, wizytówka Google, współpraca z sąsiednimi firmami). Komisja nie oczekuje dużych kampanii.

## 6. Typowe błędy

- „Będę się reklamować w internecie i mediach społecznościowych”.
- Budżet reklamy w tekście inny niż w arkuszu.
- Kanały, które nie pasują do klienta (TikTok dla usług dla seniorów) albo do budżetu (billboardy przy 250 zł miesięcznie).
- Cele sprzedażowe niezgodne z prognozą przychodów.

## 7. Prompt sekcji

```text
SEKCJA 05 – PLAN MARKETINGOWY
Napisz treść pola "{{pole_formularza}}" (limit: {{limit_znakow}}, ton: {{ton}}).
Kolejność: (1) do kogo i jaki główny kanał (segmenty z K7); (2) kanały z K9 – co dokładnie,
dla którego segmentu, z nazwami (grupy, miejsca, partnerzy); (3) budżet: pozycje reklamowe
z K10 (nazwa + cena przepisana dosłownie) oraz miesięczny budżet {{ark_reklama_mies}} – NIE
sumuj kwot; (4) plan pierwszych 90 dni: przed startem / m1 / m2 / m3 – działanie i cel z K9;
(5) utrzymanie klientów z K9.
Nie dodawaj kanałów ani partnerów spoza K9. Brak celu liczbowego w K9 = [BRAK DANYCH: ilu
klientów chcę mieć po 3 miesiącach]. Nie obiecuj efektów kampanii.
```

## 8. Przykład wypełnienia – firma sprzątająca

> **DANE FIKCYJNE – PRZYKŁAD.** Grupy, firmy i liczby są wymyślone. Zmienne `{{ark_…}}` zostawiono celowo: w gotowym tekście podstawia je system z arkusza klientki.

**Skrót kwestionariusza:** Katarzyna, Zielonów. Segmenty z sekcji 03: mieszkańcy Osiedla Słonecznego, wspólnoty („Admin-Dom”, 38 wspólnot), biura i gabinety, biura nieruchomości (3). K9 – kanały: grupa FB „Zielonów – Osiedle Słoneczne” (ok. 1 900 członków, tam była ankieta); wizytówka Google; ulotki do skrzynek na Osiedlu Słonecznym (za zgodą zarządcy); osobista wizyta u zarządcy „Admin-Dom” z ofertą na klatki; e-mail i wizyta w 3 biurach nieruchomości; magnes z numerem telefonu zostawiany po każdym sprzątaniu; rabat 50 zł dla klienta polecającego i poleconego; będzie pytać każdego nowego klienta, skąd się dowiedział. Kosztorys (reklama): logo i ulotki 900 zł, oklejenie auta 1 200 zł, strona-wizytówka z formularzem 1 000 zł. Cele: po 3 miesiącach 12 stałych klientów domowych, 2 biura, 1 wspólnota.

### Wariant standard (~2000 znaków), ton: ciepły

```text
Moimi pierwszymi klientami będą sąsiedzi z Osiedla Słonecznego, małe firmy z Zielonowa i wspólnoty mieszkaniowe. Do każdej z tych grup dotrę w inny sposób, bo każda szuka usług gdzie indziej.

Mieszkańców osiedla znajdę tam, gdzie już ze mną rozmawiali, czyli w grupie „Zielonów – Osiedle Słoneczne” na Facebooku. Grupa ma ok. 1 900 członków i to w niej przeprowadziłam ankietę. Za zgodą zarządcy zostawię też ulotki w skrzynkach na osiedlu. Firmy i wspólnoty odwiedzę osobiście. Z ofertą na sprzątanie klatek pójdę do zarządcy „Admin-Dom”, a do trzech biur nieruchomości wyślę ofertę e-mailem, a potem je odwiedzę. Założę wizytówkę Google, żeby osoby szukające „sprzątanie Zielonów” mogły mnie znaleźć i przeczytać opinie. Każdego nowego klienta zapytam, skąd się o mnie dowiedział. Dzięki temu po trzech miesiącach będę wiedzieć, na który kanał warto wydawać więcej.

Na start przeznaczę z kosztorysu: logo i ulotki – 900 zł, oklejenie samochodu – 1 200 zł, stronę-wizytówkę z formularzem zamówienia – 1 000 zł. Co miesiąc na promocję przeznaczę {{ark_reklama_mies}}.

Plan pierwszych 90 dni:
– przed startem: wizytówka Google, strona, oklejenie auta, ulotki; wpis w grupie osiedlowej z informacją o terminie otwarcia,
– miesiąc 1: rozpoczęcie zleceń dla gabinetu „Fizjo-Ruch” i biura „Bilans”, które podpisały listy intencyjne; pierwsze sprzątania u osób z ankiety,
– miesiąc 2: spotkanie z „Admin-Dom” i oferta na klatki, wizyty w biurach nieruchomości,
– miesiąc 3: cel – 12 stałych klientów domowych, 2 biura i pierwsza wspólnota.

Najbardziej liczę na polecenia. Po każdym sprzątaniu zostawię magnes na lodówkę z moim numerem. Klient, który mnie poleci, i osoba polecona dostaną po 50 zł rabatu. W sprzątaniu ludzie wpuszczają do domu kogoś, komu ufają, dlatego opinia sąsiadki działa lepiej niż każda reklama.
```

### Na co zwrócić uwagę w przykładzie

- Każdy kanał ma nazwę i przypisany segment.
- Kwoty z kosztorysu są przepisane dosłownie, a budżet miesięczny jest zmienną z arkusza. Model nie liczy sumy.
- Cele 90 dni pochodzą z kwestionariusza.
- Ton ciepły widać w ostatnim akapicie (zaufanie, sąsiedzi), a mimo to tekst pozostaje konkretny.
