# 07 – Analiza SWOT

> Typowe nazwy pola: „Analiza SWOT”, „Mocne i słabe strony przedsięwzięcia, szanse i zagrożenia”.
> Formularze PUP zwykle mają tabelę 2×2 albo cztery osobne pola. Część urzędów prosi też o krótkie wnioski z analizy.

## 1. Cel sekcji

Pokazać, że oceniasz swój pomysł **trzeźwo**: znasz swoje atuty, nie ukrywasz słabości i wiesz, co z otoczenia może pomóc, a co zaszkodzić. Komisja szuka tu przede wszystkim **spójności z resztą wniosku** i **uczciwości**.

- **S – mocne strony** i **W – słabe strony**: czynniki **wewnętrzne** (Ty, Twoje umiejętności, sprzęt, lokal, finanse).
- **O – szanse** i **T – zagrożenia**: czynniki **zewnętrzne** (rynek, klienci, konkurencja, przepisy, sezon, ceny).

Najczęstszy błąd to pomylenie tych dwóch grup (np. „doświadczenie” wpisane jako szansa).

## 2. Dane wejściowe

| Źródło | Dane |
|---|---|
| K2, K3 | kwalifikacje i doświadczenie → S |
| K6, K10 | lokal, sprzęt, zasoby własne → S lub W |
| K7 | popyt, dowody, segmenty → O |
| K8 | konkurencja, jej słabości → O; jej siła → T |
| K11 | wkład własny, poduszka finansowa → S lub W |
| K12 | ryzyka wskazane przez klienta → W i T (szczegóły i plan B w sekcji 09) |
| K7 | sezonowość → T lub O |

## 3. Struktura

1. **Tabela lub cztery listy**, po 3–5 punktów w każdej. Każdy punkt to jedno konkretne zdanie (z liczbą, nazwą lub faktem).
2. **Wnioski z analizy** (jeśli pole na to pozwala), 2–4 zdania:
   - jak wykorzystam mocne strony, żeby skorzystać z szans (S→O),
   - jak ograniczę słabe strony i zagrożenia (W/T → działanie, odesłanie do sekcji 09).

Zasady:
- Słabe strony muszą być **prawdziwe i konkretne**. „Jestem perfekcjonistką” to nie słabość. „Nie prowadziłam dotąd księgowości, dlatego zlecę ją biuru” to tak.
- Do każdej słabości i zagrożenia warto dopisać w nawiasie działanie zaradcze, jeśli limit na to pozwala.
- Szanse i zagrożenia **lokalne i aktualne**, a nie ogólnogospodarcze („inflacja”, „pandemia”), chyba że klient wskazał konkretny wpływ.

## 4. Długość – warianty

| Wariant | Znaki | Co zawiera |
|---|---|---|
| krótki | ~800 | 3 punkty × 4 ćwiartki, równoważniki zdań |
| standard | ~2000 | 4 punkty × 4 ćwiartki, pełne zdania, działania zaradcze w nawiasach, 2 zdania wniosków |
| długi | ~4000 | 5 punktów × 4 ćwiartki z rozwinięciem, wnioski S→O, W→T, odesłania do sekcji 03, 04, 09 |

## 5. Co punktuje komisja

- **Spójność:** mocne strony pokrywają się z sekcją 02, szanse z dowodami popytu z 03, zagrożenia z konkurencją z 04 i ryzykami z 09.
- **Uczciwe słabe strony z planem zaradczym.** Komisja ocenia to wyżej niż listę samych zalet.
- **Konkret:** „15 lat w jednym warsztacie, w tym 7 jako kierownik zmiany” zamiast „doświadczenie”.
- **Brak sprzeczności:** słabą stroną nie może być „brak doświadczenia”, jeśli w sekcji 02 jest go 15 lat.

## 6. Typowe błędy

- Pomylenie czynników wewnętrznych z zewnętrznymi.
- Ogólniki: „wysoka jakość usług”, „dynamiczny rozwój rynku”.
- Pozorne słabości („zbyt duże zaangażowanie”).
- Zagrożenia, które podważają cały pomysł, bez żadnego planu (np. „brak klientów”).

## 7. Prompt sekcji

```text
SEKCJA 07 – ANALIZA SWOT
Napisz treść pola/pól "{{pole_formularza}}" (limit: {{limit_znakow}}, ton: {{ton}},
format: {{tabela | 4 listy | 4 osobne pola}}).
S i W – tylko czynniki wewnętrzne (K2, K3, K6, K10, K11). O i T – tylko zewnętrzne (K7, K8,
K12, sezonowość). 3–5 punktów w każdej ćwiartce, każdy z konkretem (liczba, nazwa, fakt).
Słabe strony – prawdziwe, z K12 lub wynikające wprost z kwestionariusza (np. brak
doświadczenia w księgowości, jedna osoba w firmie, lokal poza centrum); przy każdej –
działanie zaradcze w nawiasie, jeśli jest w K12 lub da się je wskazać bez nowych faktów.
Nie dodawaj zagrożeń ogólnokrajowych bez związku z K7/K8/K12.
Jeśli limit pozwala – 2–4 zdania wniosków: S→O oraz W/T→działania (odesłanie do części o ryzykach).
Sprawdź spójność z sekcjami 02–04: żadna słabość nie może przeczyć mocnym stronom.
```

## 8. Przykład wypełnienia – mechanik samochodowy

> **DANE FIKCYJNE – PRZYKŁAD.** Lipy, Zielonów, „Auto-Serwis Majewski”, „Moto-Fix”, „Trans-Lip” są wymyślone.

**Skrót kwestionariusza (uzupełnienie do sekcji 01):** K10: z dotacji podnośnik dwukolumnowy, tester diagnostyczny OBD, stacja do klimatyzacji, kompresor z kluczami pneumatycznymi. Własne narzędzia ręczne (zestaw kluczy, nasadki) już ma. K7: z rozmów z dawnymi klientami wynika, że większość ma auta 10–20-letnie. List intencyjny od firmy przewozowej „Trans-Lip” (6 busów, serwis okresowy). Najbliższy warsztat mechaniczny poza Lipami to „Moto-Fix” w Zielonowie (18 km), z terminami 7–10 dni. K12: brak doświadczenia w rozliczeniach (zleci biuru rachunkowemu); pracuje sam, więc choroba oznacza przestój (pilne naprawy przekaże koledze z warsztatu w Borkowie – ustne porozumienie); części zamawia w hurtowni w Zielonowie (dostawy 2 razy dziennie), bez własnego magazynu; przy drogich częściach uprzedza o koszcie i proponuje zamienniki; zimą część klientów odkłada naprawy niepilne; ceny części rosną; „Moto-Fix” może obniżyć ceny; mało aut przejeżdża przez Lipy, więc nie będzie klientów „z ulicy”. K11: wkład własny 4 000 zł, oszczędności na 3 miesiące życia.

### Wariant standard (~2000 znaków, 4 listy), ton: rzeczowy

```text
MOCNE STRONY
– 15 lat pracy jako mechanik w jednym warsztacie, od 2018 r. jako kierownik zmiany.
– Certyfikat F-gazowy do serwisu klimatyzacji samochodowej (2022).
– Lokal gotowy do pracy: 90 m² z kanałem, umowa przedwstępna najmu.
– Wkład własny 4 000 zł i oszczędności na 3 miesiące życia, więc nie muszę wypłacać pieniędzy z firmy w okresie rozruchu.

SŁABE STRONY
– Nie prowadziłem dotąd rozliczeń firmy (księgowość zlecę biuru rachunkowemu).
– Pracuję sam, więc choroba oznacza przestój warsztatu (pilne naprawy przekażę koledze z warsztatu w Borkowie, z którym mam ustne porozumienie).
– Lokal jest poza miastem i mało kto przejeżdża obok, więc nie będzie klientów „z ulicy” (opieram się na dawnych klientach z Zielonowa, którzy już pytają o warsztat).
– Nie mam magazynu części, każdą część zamawiam w hurtowni (dostawy 2 razy dziennie skracają czas oczekiwania).

SZANSE
– Po zamknięciu Auto-Serwisu Majewski w listopadzie 2025 r. dawni klienci z Lip i okolic szukają nowego warsztatu.
– Na terminy w najbliższym warsztacie, „Moto-Fix” w Zielonowie, czeka się 7–10 dni.
– Firma przewozowa „Trans-Lip” (6 busów) wyraziła w liście intencyjnym chęć zlecania serwisu okresowego.
– Klienci jeżdżą głównie autami 10–20-letnimi, które częściej wymagają napraw.

ZAGROŻENIA
– Rosnące ceny części mogą zniechęcać klientów do napraw (uprzedzę o koszcie przed naprawą i zaproponuję tańsze zamienniki).
– „Moto-Fix” może obniżyć ceny lub skrócić terminy.
– Ewentualna utrata zleceń od „Trans-Lip” oznaczałaby spadek przychodów (w planie B uwzględniam przychody o 30% niższe).
– Zimą część klientów odkłada naprawy niepilne.

WNIOSKI
Doświadczenie i gotowy lokal pozwolą mi szybko przejąć klientów, którzy zostali bez warsztatu po zamknięciu zakładu w Zielonowie. Słabe strony ograniczę przez zlecenie księgowości i współpracę z warsztatem w Borkowie w razie choroby. Szczegóły opisuję w części o ryzykach.
```

### Na co zwrócić uwagę w przykładzie

- Szanse to fakty zewnętrzne z kwestionariusza (zamknięcie zakładu, terminy konkurenta, list intencyjny), a nie „rozwój motoryzacji”.
- Słabe strony są prawdziwe i mają działania zaradcze w nawiasach.
- Wszystkie działania zaradcze w nawiasach (warsztat w Borkowie, zamienniki, hurtownia) pochodzą z K12. Gdyby ich tam nie było, model wstawiłby `[BRAK DANYCH: co zrobię, gdy …]`, a nie wymyślał rozwiązanie.
- Ustne porozumienie z innym warsztatem to fakt, o który komisja może dopytać na rozmowie. Weryfikujący odnotowuje go w `<kontrola>` jako punkt do przygotowania klienta (patrz `11-przygotowanie-do-uzupelnien.md`).
