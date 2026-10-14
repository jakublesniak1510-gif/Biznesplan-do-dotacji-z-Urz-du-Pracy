# 01 – Opis planowanej działalności

> Typowe nazwy pola w formularzach PUP: „Opis planowanego przedsięwzięcia”, „Charakterystyka planowanej działalności”, „Przedmiot i zakres działalności”, „Rodzaj działalności i jej uzasadnienie”.
> Sekcja otwiera część opisową wniosku. Komisja czyta ją pierwszą i na jej podstawie wyrabia sobie zdanie o całym wniosku.

## 1. Cel sekcji

Komisja ma w 2 minuty zrozumieć:
1. **co** konkretnie będziesz robić (usługi lub produkty, a nie „branża”);
2. **gdzie i jak** (adres lub tryb pracy, zasięg, godziny);
3. **w jakiej formie** (PKD, forma prawna, opodatkowanie, VAT, data startu);
4. **dlaczego właśnie Ty i dlaczego teraz** (motywacja oparta na faktach z Twojego życia zawodowego).

## 2. Dane wejściowe z kwestionariusza

| Kod | Dane | Obowiązkowe? |
|---|---|---|
| K5 | przedmiot działalności, lista usług lub produktów z cenami | tak |
| K5 | PKD (główny i dodatkowe; według **PKD 2025**, którą od 2025 r. stosuje się przy nowych wpisach w CEIDG) | tak; jeśli klient nie zna kodów, dobiera je właściciel, nie model |
| K5 | forma prawna (zwykle jednoosobowa działalność gospodarcza), forma opodatkowania, VAT (czynny / zwolniony) | tak |
| K6 | lokalizacja: adres lokalu albo tryb mobilny lub online, zasięg w km, obsługiwane miejscowości, godziny pracy | tak |
| K6 | lokal: własny lub najem, metraż, stan umowy (np. umowa przedwstępna), koszt | gdy dotyczy |
| K13 | motywacja: skąd pomysł, jakie zdarzenia do niego doprowadziły | tak |
| K3 | doświadczenie (1–2 zdania nawiązania; szczegóły w sekcji 02) | tak |
| — | planowana data rozpoczęcia (z arkusza: `Zalozenia!B8`) | tak |

Jeśli brakuje PKD, formy opodatkowania lub adresu, model wstawia `[BRAK DANYCH: …]`. **Model nie dobiera kodów PKD.**

## 3. Struktura

1. **Akapit otwierający (2–3 zdania):** co, gdzie, od kiedy. Bez wstępów typu „Celem niniejszego…”.
2. **Zakres usług lub produktów:** lista albo zdania z cenami z kwestionariusza; zaznacz, co jest usługą główną, a co dodatkową.
3. **Lokalizacja i organizacja pracy:** adres lub tryb, zasięg (miejscowości), godziny, sposób przyjmowania zleceń.
4. **Dane formalne:** PKD (kod + nazwa), forma prawna, forma opodatkowania, VAT. Najlepiej jako krótka lista albo jedno zdanie na każdą daną.
5. **Motywacja:** dlaczego ten pomysł, oparta na faktach. Na koniec 1 zdanie łączące z doświadczeniem (odesłanie do sekcji 02).

Przy limicie poniżej 1000 znaków punkty 3 i 4 łącz w jeden akapit. Motywację skróć do jednego zdania.

## 4. Długość – trzy warianty

| Wariant | Znaki ze spacjami | Co zawiera |
|---|---|---|
| krótki | ~800 (600–1000) | co i gdzie (1 zdanie), 3–4 główne usługi bez cen, PKD + forma opodatkowania, 1 zdanie motywacji |
| standard | ~2000 (1700–2300) | pełna struktura 1–5; ceny 3–6 usług; godziny pracy; motywacja 2–4 zdania |
| długi | ~4000 (3400–4500) | jak standard + dokładny opis organizacji pracy (przyjmowanie zleceń, czas realizacji, standard obsługi), opis lokalu lub pojazdu, plan rozwoju oferty w 12 mies. (tylko jeśli jest w kwestionariuszu), szersza historia motywacji |

## 5. Co punktuje komisja

- **Konkret zamiast hasła:** nazwy usług, ceny, adres, godziny. Komisja punktuje „przejrzystość i realność przedsięwzięcia”.
- **Spójność PKD z opisem i kosztorysem.** Każda usługa z opisu mieści się w PKD, a każdy zakup z kosztorysu służy którejś usłudze.
- **Realny lokal albo tryb pracy:** umowa przedwstępna najmu, zgoda właściciela, tytuł prawny do lokalu. Komisje pytają o to wprost.
- **Motywacja oparta na doświadczeniu, nie na marzeniach:** „klienci pytali”, „pracodawca zamknął zakład”, „robiłem to dorywczo przez 3 lata”.
- **Zgodność z regulaminem PUP:** niektóre urzędy nie finansują wybranych PKD (np. handlu obwoźnego, działalności sezonowej). Sprawdza to właściciel przed pisaniem.

## 6. Typowe błędy

- Opis branży zamiast opisu firmy („Branża motoryzacyjna w Polsce…”).
- Lista 15 kodów PKD „na zapas”. Komisja traktuje to jako brak pomysłu. Wystarczą 1–3 kody, spójne z opisem.
- Brak ceny lub zakresu: „usługi fryzjerskie na najwyższym poziomie”.
- Motywacja „zawsze marzyłam o własnej firmie” bez żadnego faktu.
- Sprzeczności z kosztorysem (w opisie lokal, w kosztorysie brak czynszu i remontu).

## 7. Prompt sekcji (wklejany jako `<szablon_sekcji>`)

```text
SEKCJA 01 – OPIS PLANOWANEJ DZIAŁALNOŚCI
Napisz treść pola "{{pole_formularza}}" (limit: {{limit_znakow}} znaków ze spacjami, ton: {{ton}}).
Kolejność: (1) co, gdzie i od kiedy – bez wstępu; (2) usługi/produkty z cenami z K5 –
zaznacz usługę główną; (3) lokalizacja, zasięg (nazwy miejscowości z K6), godziny, sposób
przyjmowania zleceń; (4) dane formalne: PKD 2025 (kod + nazwa – TYLKO z K5), forma prawna,
forma opodatkowania, VAT, data startu; (5) motywacja z K13 oparta na faktach z K3, zakończona
odesłaniem do opisu doświadczenia.
Nie dobieraj PKD samodzielnie. Jeśli w K5 brakuje kodu – [BRAK DANYCH: kod PKD 2025 dla …].
Nie opisuj branży ogólnie. Nie wymieniaj usług, których nie ma w K5.
Przy limicie < 1000 znaków: punkty (3) i (4) w jednym akapicie, motywacja w 1 zdaniu.
```

## 8. Przykład wypełnienia – mechanik samochodowy

> **DANE FIKCYJNE – PRZYKŁAD.** Osoba, miejscowości (Lipy, Zielonów, powiat zielonowski), ulice i firmy są wymyślone. Przykład służy do kalibracji przez właściciela. Nie wysyłamy go do modelu przy kliencie z tej samej branży.

**Skrót kwestionariusza:** Tomasz, 41 lat, Lipy (gm. Lipy). Technik pojazdów samochodowych (2004). 2010–2025 mechanik, od 2018 kierownik zmiany w „Auto-Serwis Majewski” w Zielonowie (zakład zamknięty 11.2025, właściciel przeszedł na emeryturę). Certyfikat F-gazowy (klimatyzacja samochodowa, 2022). Garaż 90 m² z kanałem i bramą dla dostawczaków, ul. Polna 12 w Lipach (przy drodze powiatowej do Zielonowa), umowa przedwstępna najmu z 02.10.2026, 1 200 zł/mies. Auta osobowe i dostawcze do 3,5 t. Zlecenia telefonicznie i na miejscu, proste naprawy w dniu przyjęcia. Usługi: olej i filtry (robocizna 80 zł), klocki i tarcze (150 zł/oś), diagnostyka komputerowa (100 zł), serwis klimatyzacji (250 zł z czynnikiem), zawieszenie, rozrząd (od 600 zł). PKD główny 95.31.A; sprzedaż części: kod nieustalony. Skala podatkowa, czynny VAT (klienci firmowi). Start 01.2027. Pn–pt 8–17, sob. 8–13. Motywacja: dawni klienci z Lip i okolicznych wsi dojeżdżali 18 km do Zielonowa i pytają, gdzie teraz naprawiać auta.

### Wariant standard (~2000 znaków), ton: techniczny

```text
Od stycznia 2027 r. uruchomię warsztat mechaniki pojazdowej w Lipach, w garażu z kanałem przy ul. Polnej 12, przy drodze powiatowej do Zielonowa. Zajmę się naprawami mechanicznymi samochodów osobowych i dostawczych do 3,5 t.

Zakres usług i ceny robocizny:
– wymiana oleju i filtrów – 80 zł,
– wymiana klocków i tarcz hamulcowych – 150 zł za oś,
– diagnostyka komputerowa (odczyt i kasowanie błędów, parametry bieżące) – 100 zł,
– serwis klimatyzacji z uzupełnieniem czynnika – 250 zł,
– naprawy zawieszenia oraz wymiana rozrządu – od 600 zł, wycena po oględzinach.
Usługą główną będą naprawy bieżące i serwis okresowy. Klimatyzację wykonuję na podstawie certyfikatu F-gazowego, który mam od 2022 r.

Lokal ma 90 m², kanał i bramę dla aut dostawczych. Mam umowę przedwstępną najmu z 2 października 2026 r. (1 200 zł miesięcznie). Warsztat będzie czynny od poniedziałku do piątku w godz. 8–17 i w soboty w godz. 8–13. Zlecenia przyjmę telefonicznie i na miejscu. Prostsze naprawy wykonam w dniu przyjęcia auta.

Dane formalne:
– forma prawna: jednoosobowa działalność gospodarcza,
– PKD 2025: 95.31.A Naprawa mechaniczna i serwisowa pojazdów silnikowych, z wyłączeniem motocykli; sprzedaż części klientom – [BRAK DANYCH: kod PKD 2025 dla sprzedaży części, ustalić z księgową],
– opodatkowanie: zasady ogólne (skala podatkowa),
– VAT: czynny podatnik od początku działalności, bo część klientów to firmy, które odliczają VAT.

Pomysł wziął się z mojej pracy. Przez 15 lat naprawiałem auta w Auto-Serwisie Majewski w Zielonowie, a od 2018 r. byłem tam kierownikiem zmiany. Duża część stałych klientów dojeżdżała do nas z Lip i okolicznych wsi, czyli 18 km w jedną stronę. Po zamknięciu zakładu w listopadzie 2025 r. wielu z nich pyta mnie, gdzie teraz naprawiać samochody. Swoje przygotowanie zawodowe opisuję w części o kwalifikacjach.
```

### Wariant krótki (~800 znaków), ton: rzeczowy

```text
Od stycznia 2027 r. otworzę warsztat mechaniki pojazdowej w Lipach, przy ul. Polnej 12 (garaż 90 m² z kanałem, umowa przedwstępna najmu z 02.10.2026 r.). Będę wykonywał serwis okresowy, wymianę hamulców, diagnostykę komputerową, serwis klimatyzacji i naprawy zawieszenia samochodów do 3,5 t. Przykładowe ceny robocizny: wymiana oleju 80 zł, diagnostyka 100 zł, klimatyzacja 250 zł. Warsztat będzie czynny od poniedziałku do soboty. Działalność jednoosobowa, PKD 2025: 95.31.A, skala podatkowa, czynny VAT. Przez 15 lat pracowałem jako mechanik w Zielonowie, ostatnie lata jako kierownik zmiany. Po zamknięciu zakładu dawni klienci z Lip i okolic pytają, gdzie mogą teraz naprawiać auta bez dojazdu 18 km do miasta.
```

### Na co zwrócić uwagę w przykładzie

- Wszystkie ceny, daty i nazwy pochodzą ze skrótu kwestionariusza. Model nie dodał żadnego kursu ani klienta.
- Brakujący kod PKD jest oznaczony znacznikiem, a nie zgadnięty.
- Ton techniczny widać w nazwach czynności („odczyt i kasowanie błędów, parametry bieżące”) i parametrach lokalu.
- Brak fraz z listy zakazanej. Słowo „konkurencyjne” w ogóle się nie pojawia, bo porównanie cen należy do sekcji 04.
