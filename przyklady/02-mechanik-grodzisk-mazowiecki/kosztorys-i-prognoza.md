# Kosztorys i prognoza – warsztat mechaniczny, PUP Grodzisk Mazowiecki

> **DANE FIKCYJNE – PRZYKŁAD.** Wszystkie liczby w tabelach pochodzą z `model.xlsx` w tym katalogu (kopia `model-finansowy/model-finansowy-pup.xlsx` z danymi klienta, przeliczona przez LibreOffice `/usr/bin/soffice --headless --convert-to xlsx`). Plik wygenerował `przyklady/narzedzia/kosztorys_md.py`.
>
> Regulamin: Zarządzenie Dyrektora PUP w Grodzisku Mazowieckim nr 13/2026 z 22.04.2026 (Rozdz. III ust. 2–4: towar do 30% wnioskowanej kwoty, reklama – szyld, tablica, strona – do 15%; wykluczone m.in. remonty i adaptacje, najem, ubezpieczenia, wizytówki i ulotki, leasing, szkolenia, wycena rzeczoznawcy, transport zakupów). Ogłoszenia naboru jeszcze nie ma – maksymalna kwota **[do weryfikacji]**; w arkuszu jako limit kontrolny wpisano limit ustawowy 55 398,78 zł.

## 1. Założenia wpisane do arkusza (`model.xlsx`, arkusz `Zalozenia`)

| Parametr | Wartość |
|---|---|
| Nazwa / branża | Warsztat mechaniczny – Kałęczyn, gm. Grodzisk Maz. (DANE FIKCYJNE – przykład) |
| Kwota dotacji z PUP (zł) | 39 400,00 |
| Maksymalna kwota dotacji wg ogłoszenia naboru (zł) | 55 398,78 |
| Wkład własny – gotówka wniesiona na start (zł) | 8 000,00 |
| Data rozpoczęcia działalności | 01.02.2027 |
| Forma opodatkowania | skala |
| Stawka ryczałtu (gdy forma = ryczałt) | 8,5% |
| Ulga na start (6 mies. bez składek społecznych) | TAK |
| Liczba miesięcy ulgi na start | 6 |
| Preferencyjne składki ZUS ("mały ZUS") | TAK |
| Liczba miesięcy składek preferencyjnych | 24 |
| Mały ZUS plus (opcjonalnie, po okresie preferencyjnym) | NIE |
| Podstawa wymiaru – Mały ZUS plus (zł/mies.) | 3 000,00 |
| Dobrowolne ubezpieczenie chorobowe | TAK |
| Czynny podatnik VAT | NIE |
| Stawka VAT na sprzedaż (gdy czynny VAT) | 23% |
| Dni robocze w miesiącu | 21 |
| Godziny pracy z klientem dziennie | 7 |
| Spadek przychodów – scenariusz pesymistyczny | 30% |

## 2. Specyfikacja wydatków (arkusz `Kosztorys`)

Klient jest zwolniony z VAT, więc „do rozliczenia” = brutto. Linki: oferty typu (otomoto.pl dla podnośnika z dokumentacją UDT, Ceneo dla pozostałych pozycji). Przed złożeniem klient dołącza konkretne oferty w PDF. Pozycje „[oferta … – do dołączenia]” wymagają oferty lokalnego dostawcy (hurtownia olejów, kaseton, strona).

**Decyzje przy kosztorysie (limity „samochód / sprzęt używany”):**
- Laweta używana za ok. 25 tys. zł – **nie wpisana**. Zabrałaby ponad 60% dotacji, a regulamin pozwala komisji obniżyć kwotę przy wydatkach nieuzasadnionych lub zawyżonych (§ 6 ust. 6). Zakup używanego pojazdu wymagałby też oświadczenia zbywcy o braku dofinansowania, a urząd może zażądać wyceny rzeczoznawcy (Rozdz. V ust. 9 i 11); koszt wyceny jest wykluczony z dotacji.
- Używany podnośnik od zamykanego warsztatu byłego pracodawcy (5 tys. zł) – **zamieniony na nowy**. Przy zakupie od likwidowanej firmy i rzeczy używanych urząd może żądać wyceny rzeczoznawcy i rozliczyć najwyżej kwotę z wyceny; do tego demontaż, ponowne kotwienie i brak gwarancji.
- Kasa fiskalna – wkład własny. Regulamin Grodziska nie wymienia kasy wśród wykluczeń, ale większość urzędów jej nie finansuje, a ulga na zakup kasy przysługuje niezależnie od dotacji [do weryfikacji: ulga na kasę u księgowej]. Bezpieczniej: wkład własny.
- Sorbent, wanny wychwytowe, gaśnice, odzież – wkład własny (drobne pozycje BHP; ubrania mogą być kwestionowane jako niezwiązane bezpośrednio z usługą).

| Lp. | Pozycja | Kategoria | Nowy/używany | Ilość | Cena jedn. netto | Wartość netto | VAT | Brutto | Do rozliczenia | Finansowanie | Oferta typu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Podnośnik dwukolumnowy 4 t elektrohydrauliczny z montażem i dokumentacją UDT | sprzęt | nowy | 1 | 7 725,00 | 7 725,00 | 1 776,75 | 9 501,75 | 9 501,75 | dotacja | [otomoto.pl](https://www.otomoto.pl/oferta/podnosnik-dwukolumnowy-euro-trade-sae-40-4000-kg-automatyczny-elektrohydrauliczny-ce-udt-ID6IaxBY.html) |
| 2 | Tester diagnostyczny wielomarkowy (klasa Launch X-431 / Autel MaxiSys) z aktualizacją 12 mies. | sprzęt | nowy | 1 | 4 800,00 | 4 800,00 | 1 104,00 | 5 904,00 | 5 904,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-tester+diagnostyczny+launch+x431) |
| 3 | Kompresor tłokowy 270 l, 400 V | sprzęt | nowy | 1 | 2 600,00 | 2 600,00 | 598,00 | 3 198,00 | 3 198,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-kompresor+270l+400v) |
| 4 | Klucz udarowy pneumatyczny 1/2" + akumulatorowy, z kompletem nasadek udarowych | sprzęt | nowy | 1 | 1 400,00 | 1 400,00 | 322,00 | 1 722,00 | 1 722,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-klucz+udarowy+1/2) |
| 5 | Prasa hydrauliczna warsztatowa 20 t | sprzęt | nowy | 1 | 1 300,00 | 1 300,00 | 299,00 | 1 599,00 | 1 599,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-prasa+hydrauliczna+20t) |
| 6 | Zestaw blokad rozrządu (VAG, PSA, Renault, Ford, Opel – benzyna i diesel) | sprzęt | nowy | 1 | 900,00 | 900,00 | 207,00 | 1 107,00 | 1 107,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-blokada+rozrzadu+zestaw) |
| 7 | Wysysarka/zlewarka do oleju pneumatyczna 80 l | sprzęt | nowy | 1 | 750,00 | 750,00 | 172,50 | 922,50 | 922,50 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-zlewarka+oleju+pneumatyczna+80l) |
| 8 | Podnośnik żaba 3 t niskoprofilowy + 2 pary stojaków | sprzęt | nowy | 1 | 700,00 | 700,00 | 161,00 | 861,00 | 861,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-podnosnik+zaba+3t+niski) |
| 9 | Prostownik z funkcją rozruchu i zasilacz stabilizujący do kodowania | sprzęt | nowy | 1 | 800,00 | 800,00 | 184,00 | 984,00 | 984,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-zasilacz+do+kodowania+samochodu) |
| 10 | Myjka do części z pompą | sprzęt | nowy | 1 | 650,00 | 650,00 | 149,50 | 799,50 | 799,50 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-myjka+do+czesci+z+pompa) |
| 11 | Urządzenie do wymiany płynu hamulcowego | sprzęt | nowy | 1 | 900,00 | 900,00 | 207,00 | 1 107,00 | 1 107,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-urzadzenie+do+wymiany+plynu+hamulcowego) |
| 12 | Laptop do diagnostyki, katalogów części i kosztorysów | sprzęt | nowy | 1 | 2 400,00 | 2 400,00 | 552,00 | 2 952,00 | 2 952,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-laptop+15,6+16gb) |
| 13 | Stół warsztatowy z imadłem + szafka narzędziowa | sprzęt | nowy | 1 | 1 600,00 | 1 600,00 | 368,00 | 1 968,00 | 1 968,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-stol+warsztatowy+z+imadlem) |
| 14 | Oleje silnikowe (2 × 60 l), filtry, płyny – pierwszy zapas | towar | nowy | 1 | 3 307,52 | 3 307,52 | 760,73 | 4 068,25 | 4 068,25 | dotacja | [oferta hurtowni motoryzacyjnej – do dołączenia] |
| 15 | Kaseton z nazwą na halę + baner przy drodze | reklama | nowy | 1 | 1 000,00 | 1 000,00 | 230,00 | 1 230,00 | 1 230,00 | dotacja | [oferta firmy reklamowej – do dołączenia] |
| 16 | Strona www z mapą dojazdu i formularzem zgłoszenia | reklama | nowy | 1 | 1 200,00 | 1 200,00 | 276,00 | 1 476,00 | 1 476,00 | dotacja | [oferta wykonawcy – do dołączenia] |
| 17 | Kasa fiskalna online | sprzęt | nowy | 1 | 1 200,00 | 1 200,00 | 276,00 | 1 476,00 | 1 476,00 | wkład własny | [ceneo.pl](https://www.ceneo.pl/;szukaj-kasa+fiskalna+online) |
| 18 | Gaśnice, apteczka, sorbent, wanny wychwytowe (BHP i ochrona środowiska) | inne | nowy | 1 | 400,00 | 400,00 | 92,00 | 492,00 | 492,00 | wkład własny | [ceneo.pl](https://www.ceneo.pl/;szukaj-sorbent+do+oleju) |
| 19 | Ubranie robocze i obuwie ochronne | inne | nowy | 1 | 300,00 | 300,00 | 69,00 | 369,00 | 369,00 | wkład własny | [ceneo.pl](https://www.ceneo.pl/;szukaj-ubranie+robocze+mechanika) |
| | **RAZEM** | | | | | 33 932,52 | 7 804,48 | 41 737,00 | **41 737,00** | | |
| | w tym z dotacji | | | | | | | | **39 400,00** | dotacja | |
| | w tym z wkładu własnego | | | | | | | | **2 337,00** | wkład własny | |

Kontrola arkusza: OK – dotacja rozplanowana; suma kategorii = suma z dotacji: OK.

### Limity kategorii według regulaminu urzędu

| Kategoria | Limit wpisany do arkusza | Suma z dotacji (zł) | Udział w dotacji | Status |
|---|---|---|---|---|
| sprzęt | brak limitu % | 32 625,75 | 82,8% | OK |
| towar | 30% | 4 068,25 | 10,3% | OK |
| reklama | 15% | 2 706,00 | 6,9% | OK |
| remont | wykluczone | 0,00 | 0,0% | OK |
| inne | brak limitu % | 0,00 | 0,0% | OK |

Limity z regulaminu Grodziska wpisane do arkusza: towar 30%, reklama 15%, remont 0% (wykluczony), sprzęt i inne bez limitu. Udziały liczone od kwoty dotacji (regulamin: „wnioskowanej kwoty”) – kontrola arkusza: OK.

## 3. Przychody – założenia (arkusz `Przychody`)

| Usługa | Cena (zł) | Liczba / mies. przy pełnym obłożeniu | Czas 1 usługi (h) |
|---|---|---|---|
| Serwis olejowy – robocizna (olej + filtry) | 70 | 40 | 0,5 |
| Hamulce i zawieszenie – robocizna (średnio na zlecenie) | 230 | 22 | 1,5 |
| Diagnostyka komputerowa i elektryka | 120 | 18 | 0,75 |
| Rozrząd / sprzęgło – robocizna (średnio) | 700 | 4 | 5 |
| Części i oleje odsprzedane klientom (średnio na zlecenie) | 110 | 36 | 0 |

| | 02.2027 | 03.2027 | 04.2027 | 05.2027 | 06.2027 | 07.2027 | 08.2027 | 09.2027 | 10.2027 | 11.2027 | 12.2027 | 01.2028 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Rozruch | 40% | 60% | 80% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| Sezonowość | 0,9 | 1,05 | 1,1 | 1,05 | 1 | 0,9 | 0,9 | 1,05 | 1,1 | 1,1 | 0,95 | 0,9 |
| Serwis olejowy – robocizna (olej + filtry) (szt.) | 14 | 25 | 35 | 42 | 40 | 36 | 36 | 42 | 44 | 44 | 38 | 36 |
| Hamulce i zawieszenie – robocizna (średnio na zlecenie) (szt.) | 8 | 14 | 19 | 23 | 22 | 20 | 20 | 23 | 24 | 24 | 21 | 20 |
| Diagnostyka komputerowa i elektryka (szt.) | 6 | 11 | 16 | 19 | 18 | 16 | 16 | 19 | 20 | 20 | 17 | 16 |
| Rozrząd / sprzęgło – robocizna (średnio) (szt.) | 1 | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| Części i oleje odsprzedane klientom (średnio na zlecenie) (szt.) | 13 | 23 | 32 | 38 | 36 | 32 | 32 | 38 | 40 | 40 | 34 | 32 |
| Obłożenie czasu pracy | 19% | 39% | 53% | 61% | 59% | 54% | 54% | 61% | 63% | 63% | 57% | 54% |

Ceny robocizny i liczby zleceń przy pełnym obłożeniu – kwestionariusz 3.2. Linia „Części i oleje” to odsprzedaż części do wykonanych napraw (narzut ok. 15%); koszt części jest w materiałach (26% całego przychodu). Rozruch 40% / 60% / 80% – klient zaczyna w nowym miejscu, poza ruchem „z ulicy”. Czas pracy przy autach: 21 dni × 7 h. Obłożenie maks. 63% – zostaje czas na przyjęcia, wyceny i zamawianie części.

## 4. Koszty stałe miesięcznie (arkusz `Koszty`)

| Pozycja | zł / mies. |
|---|---|
| Czynsz – najem hali w Kałęczynie | 2 200 |
| Media (prąd 400 V, woda, ogrzewanie) | 450 |
| Telefon i internet | 100 |
| Księgowość (biuro rachunkowe, KPiR) | 350 |
| Ubezpieczenie OC działalności | 80 |
| Paliwo (dojazdy po części, do klientów) | 300 |
| Reklama bieżąca | 200 |
| Inne (licencja testera od 2. roku – rezerwa, odbiór olejów i odpadów, konto) | 300 |
| **Razem koszty stałe** | **3 980** |
| Materiały (koszt zmienny) | 26% przychodu |

Czynsz 2 200 zł – umowa przedwstępna. Media 450 zł – środek przedziału z kwestionariusza (400–500 zł), zimą ogrzewanie nagrzewnicą może podnieść rachunek. „Inne” 300 zł: odbiór olejów i filtrów (ok. 50 zł), konto firmowe, rezerwa na abonament testera od 2. roku (ok. 1 500 zł rocznie ÷ 12). Księgowość 350 zł (KPiR).

## 5. Kalkulacja 12 miesięcy – układ kwartalny (arkusz `Do-wniosku`, tabela 1a)

| Pozycja | Kw. I (mies. 1–3) | Kw. II (mies. 4–6) | Kw. III (mies. 7–9) | Kw. IV (mies. 10–12) | Razem 12 mies. |
|---|---|---|---|---|---|
| **Przychody ze sprzedaży** | **31 650** | **49 630** | **51 050** | **49 630** | **181 960** |
| **Koszty razem, w tym:** | **21 679** | **27 075** | **28 784** | **28 320** | **105 857** |
| – zakup materiałów i towarów | 8 229 | 12 904 | 13 273 | 12 904 | 47 310 |
| – czynsz – najem hali w Kałęczynie | 6 600 | 6 600 | 6 600 | 6 600 | 26 400 |
| – media (prąd 400 V, woda, ogrzewanie) | 1 350 | 1 350 | 1 350 | 1 350 | 5 400 |
| – telefon i internet | 300 | 300 | 300 | 300 | 1 200 |
| – księgowość (biuro rachunkowe, KPiR) | 1 050 | 1 050 | 1 050 | 1 050 | 4 200 |
| – ubezpieczenie OC działalności | 240 | 240 | 240 | 240 | 960 |
| – paliwo (dojazdy po części, do klientów) | 900 | 900 | 900 | 900 | 3 600 |
| – reklama bieżąca | 600 | 600 | 600 | 600 | 2 400 |
| – inne (licencja testera od 2. roku – rezerwa, odbiór olejów i odpadów, konto) | 900 | 900 | 900 | 900 | 3 600 |
| – składki ZUS (społeczne) | 0 | 0 | 1 369 | 1 369 | 2 737 |
| – składka zdrowotna | 1 510 | 2 231 | 2 202 | 2 108 | 8 050 |
| **Dochód (przychody − koszty)** | **9 971** | **22 555** | **22 266** | **21 310** | **76 103** |
| Podatek dochodowy | 0 | 752 | 2 936 | 1 979 | 5 667 |
| **Dochód netto (po podatku)** | **9 971** | **21 803** | **19 330** | **19 331** | **70 436** |

Kontrola arkusza: suma kwartałów = suma miesięcy – OK.

### Ten sam rachunek miesiąc po miesiącu (wymóg rozporządzenia: przychody i koszty w 1. roku miesięcznie)

| Pozycja | 02.2027 | 03.2027 | 04.2027 | 05.2027 | 06.2027 | 07.2027 | 08.2027 | 09.2027 | 10.2027 | 11.2027 | 12.2027 | 01.2028 | Razem |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Przychody ze sprzedaży | 5 670 | 10 920 | 15 060 | 17 490 | 16 780 | 15 360 | 15 360 | 17 490 | 18 200 | 18 200 | 16 070 | 15 360 | 181 960 |
| Koszty razem, w tym: | 5 887 | 7 252 | 8 540 | 9 334 | 9 102 | 8 638 | 9 054 | 9 749 | 9 981 | 9 981 | 9 285 | 9 054 | 105 857 |
| – składki ZUS (społeczne) | 0 | 0 | 0 | 0 | 0 | 0 | 456 | 456 | 456 | 456 | 456 | 456 | 2 737 |
| – składka zdrowotna | 433 | 433 | 645 | 807 | 759 | 665 | 624 | 766 | 813 | 813 | 671 | 624 | 8 050 |
| Dochód (przychody − koszty) | -217 | 3 668 | 6 520 | 8 156 | 7 678 | 6 722 | 6 307 | 7 741 | 8 219 | 8 219 | 6 785 | 6 307 | 76 103 |
| Podatek dochodowy | 0 | 0 | 0 | 0 | 0 | 752 | 832 | 1 020 | 1 084 | 1 084 | 895 | 0 | 5 667 |
| Dochód netto (po podatku) | -217 | 3 668 | 6 520 | 8 156 | 7 678 | 5 970 | 5 475 | 6 721 | 7 135 | 7 135 | 5 890 | 6 307 | 70 436 |

## 6. Wskaźniki i próg rentowności (arkusze `Prognoza` i `Do-wniosku`, tabela 3)

| Wskaźnik | Scenariusz bazowy | Scenariusz −30% przychodów |
|---|---|---|
| Przychody w 12 mies. (zł) | 181 960 | 127 372 |
| Koszty w 12 mies. (zł) | 105 857 | 88 862 |
| Zysk roczny przed opodatkowaniem (zł) | 76 103 | 38 510 |
| Podatek dochodowy w 12 mies. (zł) | 5 667 | 1 229 |
| ZYSK ROCZNY NETTO (zł) | 70 436 | 37 281 |
| Średni zysk netto miesięcznie (zł) | 5 870 | 3 107 |
| Rentowność sprzedaży netto | 38,7% | 29,3% |
| Próg rentowności – przychód miesięczny (zł) | 6 593 | 6 593 |
| Próg rentowności – liczba sprzedaży / mies. | 48 | 48 |
| Zwrot z dotacji (zysk netto roczny ÷ dotacja) | 178,8% | 94,6% |
| Okres zwrotu dotacji (mies.) | 6,7 | 12,7 |
| Gotówka na koniec 12. miesiąca (zł) | 76 099 | 42 944 |
| Najniższe saldo gotówki w 12 mies. (zł) | 5 446 | 4 188 |
| Próg rentowności po okresie ulg ZUS (pełny ZUS) – przychód mies. (zł) | 8 889 | – |
| Średni przychód miesięczny od 4. miesiąca (zł) | 16 701 | 11 691 |
| Margines bezpieczeństwa (średni przychód od m4 vs próg) | 61% | 44% |
| Pierwszy miesiąc z dodatnim wynikiem netto | 2 | – |
| Najwyższe obłożenie czasu pracy | 63% | – |

Próg rentowności = średnie miesięczne koszty stałe z ZUS i składką zdrowotną (4 879 zł) ÷ (1 − udział materiałów 26%). Średnia cena jednej usługi w roku: 140,18 zł, stąd liczba usług w progu.

## 7. Scenariusz pesymistyczny (przychody o 30% niższe w każdym miesiącu)

Wariant: przychody o 30% niższe w każdym miesiącu, koszty stałe i ZUS bez zmian. Firma nadal ma zysk netto; najniższe saldo gotówki spada do 4 188 zł (wariant bazowy: 5 446 zł). Pierwszy miesiąc w obu wariantach kończy się stratą (rozruch od 40%, pełny czynsz) – pokrywa ją gotówka własna (8 000 zł minus zakupy z wkładu 2 337 zł). Działania z rozmowy z klientem: więcej zleceń od firm (polecenia Bud-Mont), dłuższe soboty, reklama nie mniej niż 200 zł/mies. Opis: sekcja 09 wniosku.

## 8. Kontrole spójności arkusza (`Zalozenia`, wiersze 27–34)

| Kontrola | Wynik |
|---|---|
| Kwota dotacji ≤ maksymalna kwota z naboru | OK |
| Wydatki z dotacji ≤ kwota dotacji | OK |
| Kwota dotacji nierozplanowana w kosztorysie (zł) | 0 |
| Limity kategorii wg regulaminu | OK |
| Najniższe saldo gotówki w 12 mies. – scenariusz bazowy (zł) | 5 446,26 |
| Najniższe saldo gotówki – scenariusz pesymistyczny (zł) | 4 187,52 |
| Najwyższe obłożenie godzin pracy | 63% |
| Przychód vs limit zwolnienia z VAT (rok startu proporcjonalnie, rok następny) | OK (poniżej limitu) |

### Uproszczenia modelu

- Start 1.02.2027 – wszystkie 12 miesięcy przypada na 2027–2028 r., a arkusz liczy na stałych z 2026 r. Po ogłoszeniu wskaźników na 2027 r. (płaca minimalna, podstawy ZUS, składka zdrowotna od 02.2027) trzeba zaktualizować `Stale-2026` i wygenerować plik ponownie.
- Skala podatkowa: zaliczki narastająco w roku kalendarzowym; w styczniu 2028 r. narastanie zaczyna się od zera (stąd 0 zł podatku w 12. miesiącu).
- Brak amortyzacji podnośnika i testera (zakupy z dotacji nie są kosztem podatkowym) – podatek raczej zawyżony.
- Limit zwolnienia z VAT: arkusz porównuje przychód w roku startu z limitem proporcjonalnym – wynik „OK”. Jeśli klient zacznie sprzedawać dużo części firmom, trzeba to sprawdzić ponownie.
