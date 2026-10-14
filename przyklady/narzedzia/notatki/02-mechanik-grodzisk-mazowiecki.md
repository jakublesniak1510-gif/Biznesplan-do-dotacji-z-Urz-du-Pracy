@@ naglowek
# Kosztorys i prognoza – warsztat mechaniczny, PUP Grodzisk Mazowiecki

> **DANE FIKCYJNE – PRZYKŁAD.** Wszystkie liczby w tabelach pochodzą z `model.xlsx` w tym katalogu (kopia `model-finansowy/model-finansowy-pup.xlsx` z danymi klienta, przeliczona przez LibreOffice `/usr/bin/soffice --headless --convert-to xlsx`). Plik wygenerował `przyklady/narzedzia/kosztorys_md.py`.
>
> Regulamin: Zarządzenie Dyrektora PUP w Grodzisku Mazowieckim nr 13/2026 z 22.04.2026 (Rozdz. III ust. 2–4: towar do 30% wnioskowanej kwoty, reklama – szyld, tablica, strona – do 15%; wykluczone m.in. remonty i adaptacje, najem, ubezpieczenia, wizytówki i ulotki, leasing, szkolenia, wycena rzeczoznawcy, transport zakupów). Ogłoszenia naboru jeszcze nie ma – maksymalna kwota **[do weryfikacji]**; w arkuszu jako limit kontrolny wpisano limit ustawowy 55 398,78 zł.

@@ kosztorys_intro
Klient jest zwolniony z VAT, więc „do rozliczenia” = brutto. Linki: oferty typu (otomoto.pl dla podnośnika z dokumentacją UDT, Ceneo dla pozostałych pozycji). Przed złożeniem klient dołącza konkretne oferty w PDF. Pozycje „[oferta … – do dołączenia]” wymagają oferty lokalnego dostawcy (hurtownia olejów, kaseton, strona).

**Decyzje przy kosztorysie (limity „samochód / sprzęt używany”):**
- Laweta używana za ok. 25 tys. zł – **nie wpisana**. Zabrałaby ponad 60% dotacji, a regulamin pozwala komisji obniżyć kwotę przy wydatkach nieuzasadnionych lub zawyżonych (§ 6 ust. 6). Zakup używanego pojazdu wymagałby też oświadczenia zbywcy o braku dofinansowania, a urząd może zażądać wyceny rzeczoznawcy (Rozdz. V ust. 9 i 11); koszt wyceny jest wykluczony z dotacji.
- Używany podnośnik od zamykanego warsztatu byłego pracodawcy (5 tys. zł) – **zamieniony na nowy**. Przy zakupie od likwidowanej firmy i rzeczy używanych urząd może żądać wyceny rzeczoznawcy i rozliczyć najwyżej kwotę z wyceny; do tego demontaż, ponowne kotwienie i brak gwarancji.
- Kasa fiskalna – wkład własny. Regulamin Grodziska nie wymienia kasy wśród wykluczeń, ale większość urzędów jej nie finansuje, a ulga na zakup kasy przysługuje niezależnie od dotacji [do weryfikacji: ulga na kasę u księgowej]. Bezpieczniej: wkład własny.
- Sorbent, wanny wychwytowe, gaśnice, odzież – wkład własny (drobne pozycje BHP; ubrania mogą być kwestionowane jako niezwiązane bezpośrednio z usługą).

@@ limity
Limity z regulaminu Grodziska wpisane do arkusza: towar 30%, reklama 15%, remont 0% (wykluczony), sprzęt i inne bez limitu. Udziały liczone od kwoty dotacji (regulamin: „wnioskowanej kwoty”) – kontrola arkusza: OK.

@@ przychody
Ceny robocizny i liczby zleceń przy pełnym obłożeniu – kwestionariusz 3.2. Linia „Części i oleje” to odsprzedaż części do wykonanych napraw (narzut ok. 15%); koszt części jest w materiałach (26% całego przychodu). Rozruch 40% / 60% / 80% – klient zaczyna w nowym miejscu, poza ruchem „z ulicy”. Czas pracy przy autach: 21 dni × 7 h. Obłożenie maks. 63% – zostaje czas na przyjęcia, wyceny i zamawianie części.

@@ koszty
Czynsz 2 200 zł – umowa przedwstępna. Media 450 zł – środek przedziału z kwestionariusza (400–500 zł), zimą ogrzewanie nagrzewnicą może podnieść rachunek. „Inne” 300 zł: odbiór olejów i filtrów (ok. 50 zł), konto firmowe, rezerwa na abonament testera od 2. roku (ok. 1 500 zł rocznie ÷ 12). Księgowość 350 zł (KPiR).

@@ pesymistyczny
Wariant: przychody o 30% niższe w każdym miesiącu, koszty stałe i ZUS bez zmian. Firma nadal ma zysk netto; najniższe saldo gotówki spada do 4 188 zł (wariant bazowy: 5 446 zł). Pierwszy miesiąc w obu wariantach kończy się stratą (rozruch od 40%, pełny czynsz) – pokrywa ją gotówka własna (8 000 zł minus zakupy z wkładu 2 337 zł). Działania z rozmowy z klientem: więcej zleceń od firm (polecenia Bud-Mont), dłuższe soboty, reklama nie mniej niż 200 zł/mies. Opis: sekcja 09 wniosku.

@@ uproszczenia
### Uproszczenia modelu

- Start 1.02.2027 – wszystkie 12 miesięcy przypada na 2027–2028 r., a arkusz liczy na stałych z 2026 r. Po ogłoszeniu wskaźników na 2027 r. (płaca minimalna, podstawy ZUS, składka zdrowotna od 02.2027) trzeba zaktualizować `Stale-2026` i wygenerować plik ponownie.
- Skala podatkowa: zaliczki narastająco w roku kalendarzowym; w styczniu 2028 r. narastanie zaczyna się od zera (stąd 0 zł podatku w 12. miesiącu).
- Brak amortyzacji podnośnika i testera (zakupy z dotacji nie są kosztem podatkowym) – podatek raczej zawyżony.
- Limit zwolnienia z VAT: arkusz porównuje przychód w roku startu z limitem proporcjonalnym – wynik „OK”. Jeśli klient zacznie sprzedawać dużo części firmom, trzeba to sprawdzić ponownie.

@@ docx_tytul
# Treści do wniosku o dofinansowanie podjęcia działalności gospodarczej
Powiatowy Urząd Pracy w Grodzisku Mazowieckim, ul. T. Kościuszki 30, 05-825 Grodzisk Mazowiecki
Regulamin z 22.04.2026 · nabór: do ogłoszenia
Wnioskodawca: Damian [nazwisko] – **DANE FIKCYJNE – PRZYKŁAD**
Działalność: warsztat mechaniki pojazdowej, PKD 95.31.A (+ 47.82.Z) · Kwota: 39 400,00 zł

@@ docx_samemu
- **Wzór wniosku:** pobierz z grodziskmazowiecki.praca.gov.pl → Dokumenty do pobrania wersję z ogłoszenia naboru. Urząd nie pozwala zmieniać kolejności ani treści formularza – można tylko dodać wiersze w tabelach i rozszerzyć uzasadnienia.
- **Strona 1 i część I:** nazwisko i imię, miejsce zamieszkania, telefon, seria i numer dowodu, PESEL, NIP (jeśli nie masz – „nie posiadam”), adres, e-mail, wiek, wykształcenie, dane żony (imię, nazwisko, zawód, źródło dochodu).
- **I.12–14:** pomoc finansowa z PUP („nie korzystałem”), zadłużenie (wpisz prawdę – kredyty, karty; przy kredycie urząd poprosi o zaświadczenie), wcześniejsza działalność („nie prowadziłem”).
- **Część III:** podkreśl „poręczenie”. Poręczyciele (ojciec, szwagier) muszą mieć min. 6 500 zł brutto dochodu po odjęciu rat – szwagier jest na granicy, policz z zaświadczenia. Poręczyciele i żony poręczycieli stawiają się w urzędzie w dniu umowy. Twoja żona podpisuje zgodę na umowę.
- **IV.6:** zaznacz NIE (bez pomocy prawnej i doradztwa).
- **Oświadczenia na końcu wniosku:** przeczytaj każde (objaśnienia: `co-wpisac-samemu.md`) i podpisz. Składasz je pod rygorem odpowiedzialności karnej.
- **Załącznik nr 1 – formularz informacji przy ubieganiu się o pomoc de minimis:** części A, C, D, E (dane w A i C dotyczą planowanej działalności).
- **Dołącz:** dyplom technika, świadectwa pracy, zaświadczenie EOBD, umowę przedwstępną najmu, listy intencyjne Bud-Mont i „Smaki Mazowsza”, oferty do każdej pozycji tabeli IV.3. Kserokopie potwierdź za zgodność z oryginałem.
- **Wizja lokalna:** komisja może obejrzeć halę – opis we wniosku musi się zgadzać ze stanem faktycznym.
- **Sprawdź przed złożeniem:** maksymalną kwotę z ogłoszenia (jeśli niższa niż 39 400 zł – najpierw zmieniamy arkusz) i to, czy urząd udostępnił nowy wzór wniosku.
- **Podpis:** kwalifikowany, zaufany albo czytelny podpis na wniosku i oświadczeniach.
- **Nie rozpoczynaj działalności i niczego nie kupuj przed umową.** Uwaga, zasada tego urzędu: kto nie ma NIP, składa wniosek o wpis do CEIDG w dniu poprzedzającym zawarcie umowy, a działalność rozpoczyna po otrzymaniu środków (regulamin, Rozdz. IV ust. 2 pkt 1). Datę rozpoczęcia we wpisie ustal z pracownikiem urzędu – wcześniejsze rozpoczęcie działalności oznacza odmowę.
