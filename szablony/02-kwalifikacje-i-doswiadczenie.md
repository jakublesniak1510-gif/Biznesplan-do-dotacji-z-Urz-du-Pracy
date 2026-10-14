# 02 – Kwalifikacje i doświadczenie zawodowe

> Typowe nazwy pola: „Kwalifikacje i doświadczenie wnioskodawcy związane z planowaną działalnością”, „Przygotowanie zawodowe”, „Posiadane wykształcenie, kwalifikacje, doświadczenie”.
> W wielu PUP ta sekcja dostaje osobną ocenę punktową. Do wniosku dołącza się kopie dokumentów: dyplomów, świadectw pracy, zaświadczeń.

## 1. Cel sekcji

Pokazać komisji, że **umiesz wykonywać usługę** i **dasz radę prowadzić firmę**. Każde twierdzenie musi dać się potwierdzić dokumentem albo konkretnym faktem z historii zawodowej.

## 2. Dane wejściowe z kwestionariusza

| Kod | Dane | Uwagi |
|---|---|---|
| K2 | wykształcenie (szkoła, kierunek, rok), zawód wyuczony | z rokiem |
| K2 | kursy, szkolenia, certyfikaty, uprawnienia (nazwa, organizator, rok, liczba godzin – jeśli podano) | tylko te podane przez klienta |
| K2 | prawo jazdy, uprawnienia (np. SEP, UDT, F-gazy) | gdy mają znaczenie dla usługi |
| K3 | doświadczenie: pracodawca (nazwa, miejscowość), stanowisko, okres, obowiązki | chronologicznie |
| K3 | doświadczenie nieformalne: praca dorywcza, umowy zlecenia, pomoc w rodzinnej firmie, wolontariat, hobby z efektami | nazywamy je wprost jako nieformalne |
| K4 | od kiedy bezrobotna/y, powód utraty pracy | tylko jeśli klient chce o tym pisać |
| K10/K11 | elementy prowadzenia firmy, które klient już zna (zamówienia, kasa, grafik, kontakt z dostawcami) | z doświadczenia w K3 |
| — | dokumenty, które klient może dołączyć | lista załączników |

## 3. Struktura

1. **Zdanie otwierające:** zawód i łączny staż w branży (liczba lat tylko wtedy, gdy wynika z dat w K3).
2. **Wykształcenie i uprawnienia:** szkoła, zawód, rok, dokument.
3. **Kursy i szkolenia:** tylko te związane z planowaną działalnością, z rokiem.
4. **Doświadczenie zawodowe:** pracodawcy chronologicznie (od najnowszego albo najstarszego, zawsze tak samo). Przy każdym 1–2 zdania o **obowiązkach związanych z planowaną firmą**.
5. **Doświadczenie nieformalne** (jeśli jest): zlecenia, praca dorywcza, wolontariat.
6. **Umiejętności „firmowe”:** obsługa kasy, zamawianie towaru, grafik, rozliczanie z klientem, kontakt z dostawcami.
7. **Luki i sposób ich uzupełnienia:** np. księgowość zlecona biuru rachunkowemu, planowany kurs. Tylko jeśli są w kwestionariuszu albo wynikają z niego wprost.
8. (opcjonalnie) **Lista dokumentów potwierdzających** dołączonych do wniosku.

## 4. Długość – trzy warianty

| Wariant | Znaki | Co zawiera |
|---|---|---|
| krótki | ~800 | 1 zdanie o wykształceniu, 2–3 najważniejsze kursy, staż i ostatni pracodawca, 1 zdanie o prowadzeniu firmy |
| standard | ~2000 | pełna struktura 1–7; obowiązki przy każdym pracodawcy; luki |
| długi | ~4000 | jak standard + szczegółowe przykłady prac (rodzaje zleceń, liczba klientów z K3), opis umiejętności organizacyjnych, pełna lista dokumentów |

## 5. Co punktuje komisja

- **Związek kwalifikacji z PKD:** dyplom lub świadectwo w zawodzie, uprawnienia wymagane przepisami (np. F-gazy do klimatyzacji, SEP do instalacji elektrycznych).
- **Udokumentowany staż:** świadectwa pracy, umowy, referencje. Niektóre PUP punktują staż od 1, 3 albo 5 lat.
- **Szkolenia z prowadzenia firmy** (np. organizowane przez PUP), jeśli klient je odbył.
- **Uczciwość co do luk:** komisja lepiej ocenia wnioskodawcę, który pisze, że księgowość zleci biuru rachunkowemu, niż takiego, który twierdzi, że „zna się na wszystkim”.
- **Spójność z rozmową:** na rozmowie komisja dopytuje o każdy kurs i pracodawcę z tej sekcji (patrz `11-przygotowanie-do-uzupelnien.md`).

## 6. Typowe błędy

- „Wieloletnie doświadczenie” zamiast liczby lat i nazw pracodawców.
- Kursy niezwiązane z działalnością (np. obsługa wózka widłowego u fryzjerki) dopisane „dla objętości”.
- Zawyżanie: „prowadziłam salon”, gdy klientka była pracownicą. To łatwo wychodzi na rozmowie.
- Brak dat. Komisja nie może wtedy policzyć stażu.

## 7. Prompt sekcji

```text
SEKCJA 02 – KWALIFIKACJE I DOŚWIADCZENIE
Napisz treść pola "{{pole_formularza}}" (limit: {{limit_znakow}}, ton: {{ton}}).
Kolejność: (1) zawód i staż – liczbę lat podaj tylko, jeśli wynika z dat w K3 (nie zaokrąglaj
w górę); (2) wykształcenie i uprawnienia z K2 z rokiem; (3) kursy z K2 związane z planowaną
działalnością; (4) pracodawcy z K3 chronologicznie – przy każdym obowiązki związane z
planowaną firmą; (5) doświadczenie nieformalne z K3 – nazwij je jako nieformalne;
(6) umiejętności potrzebne do prowadzenia firmy, wynikające z K3; (7) luki i jak je uzupełnię
(tylko z kwestionariusza).
Nie zmieniaj stanowisk ani zakresu obowiązków na wyższe niż w K3. Nie dodawaj kursów.
Jeśli brakuje roku lub nazwy organizatora kursu – [BRAK DANYCH: …].
Na końcu (jeśli limit pozwala) jedno zdanie: jakie dokumenty dołączam (tylko te z kwestionariusza).
```

## 8. Przykład wypełnienia – fryzjerka mobilna

> **DANE FIKCYJNE – PRZYKŁAD.** Osoba, salony, DPS i miejscowości (Borków, Zielonów) są wymyślone.

**Skrót kwestionariusza:** Anna, 34 lata, Borków. ZSZ, zawód fryzjer. Dyplom czeladnika (Cech Rzemiosł Różnych w Zielonowie, 2012). Kursy: koloryzacja (szkolenie producenta farb, 2019, 16 h); fryzury okolicznościowe i upięcia (2021, 3 dni). 2012–2017 fryzjerka w „Fryzjer Ela” w Borkowie (strzyżenia damskie, męskie, dziecięce); 2017–03.2026 fryzjerka w „Studio Włosów Iza” w Zielonowie, ul. Kościuszki 8 (strzyżenia, koloryzacje, upięcia; od 2020 opieka nad praktykantkami; zamawianie farb u hurtownika, obsługa kasy fiskalnej). Od 2022 umowa zlecenie z DPS „Pod Lipami” w Borkowie: raz w miesiącu strzyżenie mieszkańców (część leżących lub na wózkach). Dawne klientki z salonu pytały o wizyty domowe. Ok. 15 upięć ślubnych rocznie w domach klientek (ostatnie 3 lata, w ramach pracy w salonie). Prawo jazdy B od 2010, własne auto. Bezrobotna od 04.2026 (zamknięcie salonu). Księgowość chce zlecić biuru rachunkowemu. O szkoleniu z zakładania firmy nie napisała.

### Wariant standard (~2000 znaków), ton: ciepły

```text
Jestem fryzjerką od 14 lat. W 2012 r. uzyskałam dyplom czeladnika w zawodzie fryzjer (Cech Rzemiosł Różnych w Zielonowie). Od tego czasu pracuję w zawodzie bez dłuższych przerw.

Pierwsze pięć lat, od 2012 do 2017 r., pracowałam w salonie „Fryzjer Ela” w Borkowie. Tam nauczyłam się szybkiej i dokładnej pracy przy strzyżeniach damskich, męskich i dziecięcych. Od 2017 r. do marca 2026 r. pracowałam w „Studio Włosów Iza” przy ul. Kościuszki w Zielonowie. Wykonywałam strzyżenia, koloryzacje i upięcia. Od 2020 r. opiekowałam się też praktykantkami. W salonie zamawiałam farby i kosmetyki u hurtownika i obsługiwałam kasę fiskalną, więc znam codzienną stronę prowadzenia zakładu. Pracę straciłam, gdy salon zamknięto w marcu 2026 r.

Swoje umiejętności uzupełniałam na kursach. W 2019 r. ukończyłam 16-godzinne szkolenie z koloryzacji prowadzone przez producenta farb. W 2021 r. przeszłam trzydniowy kurs fryzur okolicznościowych i upięć. Przez ostatnie trzy lata robiłam około 15 upięć ślubnych rocznie, zwykle w domach panien młodych, bo tak było im wygodniej rano w dniu ślubu.

Pracę u klienta znam też z innej strony. Od 2022 r. na umowę zlecenie raz w miesiącu strzygę mieszkańców Domu Pomocy Społecznej „Pod Lipami” w Borkowie. Nauczyłam się tam pracować przy łóżku i na wózku, cierpliwie i bez pośpiechu. Właśnie z tych wizyt i z pytań dawnych klientek wziął się pomysł na wizyty domowe.

Mam prawo jazdy kategorii B od 2010 r. i własny samochód, więc dojazdy do klientów nie będą problemem. Rozliczenia podatkowe i ZUS zlecę biuru rachunkowemu, żeby całą uwagę poświęcić klientkom. [BRAK DANYCH: czy ukończyła szkolenie z zakładania i prowadzenia firmy, np. w PUP – jeśli tak, nazwa i rok].

Do wniosku dołączam dyplom czeladniczy, zaświadczenia z kursów, świadectwa pracy i umowę zlecenia z DPS.
```

### Na co zwrócić uwagę w przykładzie

- Staż „14 lat” wynika z dat (2012–2026). Model go nie zaokrąglił.
- Ton ciepły widać w opisie sytuacji (praca przy łóżku, upięcia rano w dniu ślubu). Nie ma za to patosu ani wyrażenia „pasja”.
- Wnioskodawczyni nie prowadziła salonu i tekst tego nie sugeruje. Mowa tylko o zamówieniach i kasie, czyli o tym, co faktycznie robiła.
- Brakująca informacja o szkoleniu jest oznaczona znacznikiem do uzupełnienia.
