# Kosztorys i prognoza – fryzjerka mobilna, PUP Turek

> **DANE FIKCYJNE – PRZYKŁAD.** Wszystkie liczby w tabelach pochodzą z `model.xlsx` w tym katalogu: kopia `model-finansowy/model-finansowy-pup.xlsx` z danymi klientki, przeliczona przez LibreOffice (`/usr/bin/soffice --headless --convert-to xlsx`). Plik wygenerował skrypt `przyklady/narzedzia/kosztorys_md.py` – po każdej zmianie arkusza generujemy go od nowa, nie poprawiamy liczb ręcznie.
>
> Regulamin: „Informacja dotycząca przyznawania środków na podjęcie działalności gospodarczej w PUP w Turku w 2026 roku” (stan na 06.08.2026). Nabór 12–16.10.2026, 38 822 zł na 1 osobę.

## 1. Założenia wpisane do arkusza (`model.xlsx`, arkusz `Zalozenia`)

| Parametr | Wartość |
|---|---|
| Nazwa / branża | Fryzjerka mobilna – Turek (DANE FIKCYJNE – przykład) |
| Kwota dotacji z PUP (zł) | 15 000,00 |
| Maksymalna kwota dotacji wg ogłoszenia naboru (zł) | 38 822,00 |
| Wkład własny – gotówka wniesiona na start (zł) | 4 000,00 |
| Data rozpoczęcia działalności | 01.12.2026 |
| Forma opodatkowania | ryczałt |
| Stawka ryczałtu (gdy forma = ryczałt) | 8,5% |
| Ulga na start (6 mies. bez składek społecznych) | TAK |
| Liczba miesięcy ulgi na start | 6 |
| Preferencyjne składki ZUS ("mały ZUS") | TAK |
| Liczba miesięcy składek preferencyjnych | 24 |
| Mały ZUS plus (opcjonalnie, po okresie preferencyjnym) | NIE |
| Podstawa wymiaru – Mały ZUS plus (zł/mies.) | 3 000,00 |
| Dobrowolne ubezpieczenie chorobowe | TAK |
| Czynny podatnik VAT | NIE |
| Stawka VAT na sprzedaż (gdy czynny VAT) | 8% |
| Dni robocze w miesiącu | 21 |
| Godziny pracy z klientem dziennie | 6 |
| Spadek przychodów – scenariusz pesymistyczny | 30% |

## 2. Specyfikacja wydatków (arkusz `Kosztorys`)

Klientka jest zwolniona z VAT, więc „do rozliczenia” = kwota brutto. Ceny netto wpisano tak, żeby brutto odpowiadało ofercie typu z października 2026 r. (porównywarki i sklepy internetowe). Linki prowadzą do **ofert typu** albo do wyszukiwarki ofert (Ceneo) – przed złożeniem wniosku klientka zapisuje konkretną ofertę do PDF i dołącza ją do wniosku. Pozycje oznaczone „[oferta … – do dołączenia]” wymagają oferty od lokalnego wykonawcy (hurtownia, drukarnia, oklejanie aut).

Kasa fiskalna jest w wkładzie własnym, bo PUP Turek nie finansuje kasy (Informacja 2026, cz. IV pkt 1 ppkt 8). Fryzjerka musi ją mieć od pierwszej usługi.

| Lp. | Pozycja | Kategoria | Nowy/używany | Ilość | Cena jedn. netto | Wartość netto | VAT | Brutto | Do rozliczenia | Finansowanie | Oferta typu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Przenośna umywalka fryzjerska z kranem, zbiornikiem i regulacją wysokości | sprzęt | nowy | 1 | 640,00 | 640,00 | 147,20 | 787,20 | 787,20 | dotacja | [kaufland.pl](https://www.kaufland.pl/product/463416684/) |
| 2 | Nadmuchiwana wanienka do mycia głowy w łóżku | sprzęt | nowy | 2 | 65,00 | 130,00 | 29,90 | 159,90 | 159,90 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-wanienka+do+mycia+glowy+w+lozku) |
| 3 | Maszynka bezprzewodowa Wahl Magic Clip Cordless | sprzęt | nowy | 1 | 520,00 | 520,00 | 119,60 | 639,60 | 639,60 | dotacja | [okazje.info.pl](https://www.okazje.info.pl/szukaj/wahl-maszynka-do-strzyzenia-wlosow-magic-clip-5-star-cordless/ceny.html) |
| 4 | Trymer bezprzewodowy Wahl Detailer Li | sprzęt | nowy | 1 | 430,00 | 430,00 | 98,90 | 528,90 | 528,90 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-wahl+detailer+li) |
| 5 | Suszarka Parlux Advance Light 2200 W | sprzęt | nowy | 1 | 490,00 | 490,00 | 112,70 | 602,70 | 602,70 | dotacja | [notino.pl](https://www.notino.pl/parlux/advance-light-suszarka-do-wlosow/) |
| 6 | Prostownica BaByliss PRO EP Technology 5.0 (24 mm) | sprzęt | nowy | 1 | 300,00 | 300,00 | 69,00 | 369,00 | 369,00 | dotacja | [notino.pl](https://www.notino.pl/babyliss-pro/straighteners-ep-technology-50-2072e-prostownica-do-wlosow/) |
| 7 | Nożyczki Jaguar Pre Style Relax 5,5" + degażówki Jaguar Ergo Pre Style 5,5" | sprzęt | nowy | 1 | 620,00 | 620,00 | 142,60 | 762,60 | 762,60 | dotacja | [kaufland.pl](https://www.kaufland.pl/product/306979817/) |
| 8 | Sterylizator UV-C i myjka ultradźwiękowa do narzędzi | sprzęt | nowy | 1 | 450,00 | 450,00 | 103,50 | 553,50 | 553,50 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-sterylizator+uv+fryzjerski) |
| 9 | Walizka fryzjerska na kółkach z organizerami | sprzęt | nowy | 1 | 450,00 | 450,00 | 103,50 | 553,50 | 553,50 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-walizka+fryzjerska+na+kolkach) |
| 10 | Krzesło fryzjerskie składane z regulacją wysokości | sprzęt | nowy | 1 | 520,00 | 520,00 | 119,60 | 639,60 | 639,60 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-krzeslo+fryzjerskie+skladane) |
| 11 | Lampa LED akumulatorowa na statywie | sprzęt | nowy | 1 | 280,00 | 280,00 | 64,40 | 344,40 | 344,40 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-lampa+led+akumulatorowa+statyw) |
| 12 | Odkurzacz ręczny akumulatorowy (sprzątanie włosów u klienta) | sprzęt | nowy | 1 | 400,00 | 400,00 | 92,00 | 492,00 | 492,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-odkurzacz+reczny+akumulatorowy) |
| 13 | Tablet 10" do kalendarza wizyt i zdjęć fryzur | sprzęt | nowy | 1 | 900,00 | 900,00 | 207,00 | 1 107,00 | 1 107,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-tablet+10+cali) |
| 14 | Peleryny, ręczniki (30 szt.), grzebienie, szczotki, klipsy, miski, pędzle | inne | nowy | 1 | 800,00 | 800,00 | 184,00 | 984,00 | 984,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-peleryna+fryzjerska) |
| 15 | Farby, oksydanty, rozjaśniacze, szampony – pierwszy zapas na 2–3 mies. | towar | nowy | 1 | 2 665,12 | 2 665,12 | 612,98 | 3 278,10 | 3 278,10 | dotacja | [oferta hurtowni fryzjerskiej – do dołączenia przez klientkę] |
| 16 | Oklejenie samochodu folią z logo i telefonem | reklama | nowy | 1 | 1 100,00 | 1 100,00 | 253,00 | 1 353,00 | 1 353,00 | dotacja | [oferta lokalnej firmy reklamowej – do dołączenia] |
| 17 | Logo i strona www z kalendarzem rezerwacji | reklama | nowy | 1 | 1 500,00 | 1 500,00 | 345,00 | 1 845,00 | 1 845,00 | dotacja | [oferta wykonawcy strony – do dołączenia] |
| 18 | Kasa fiskalna online (wyłączona z dofinansowania w PUP Turek) | sprzęt | nowy | 1 | 1 220,00 | 1 220,00 | 280,60 | 1 500,60 | 1 500,60 | wkład własny | [ceneo.pl](https://www.ceneo.pl/;szukaj-kasa+fiskalna+online) |
| 19 | Ulotki, wizytówki, karnety stałej klientki | reklama | nowy | 1 | 300,00 | 300,00 | 69,00 | 369,00 | 369,00 | wkład własny | [oferta drukarni – do dołączenia] |
| 20 | Tunika robocza – 2 szt. | inne | nowy | 1 | 150,00 | 150,00 | 34,50 | 184,50 | 184,50 | wkład własny | [ceneo.pl](https://www.ceneo.pl/;szukaj-tunika+fryzjerska) |
| | **RAZEM** | | | | | 13 865,12 | 3 188,98 | 17 054,10 | **17 054,10** | | |
| | w tym z dotacji | | | | | | | | **15 000,00** | dotacja | |
| | w tym z wkładu własnego | | | | | | | | **2 054,10** | wkład własny | |

Kontrola arkusza: OK – dotacja rozplanowana; suma kategorii = suma z dotacji: OK.

### Limity kategorii według regulaminu urzędu

| Kategoria | Limit wpisany do arkusza | Suma z dotacji (zł) | Udział w dotacji | Status |
|---|---|---|---|---|
| sprzęt | brak limitu % | 7 539,90 | 50,3% | OK |
| towar | brak limitu % | 3 278,10 | 21,9% | OK |
| reklama | brak limitu % | 3 198,00 | 21,3% | OK |
| remont | wykluczone | 0,00 | 0,0% | OK |
| inne | brak limitu % | 984,00 | 6,6% | OK |

PUP Turek nie podaje limitów procentowych dla kategorii – w arkuszu wpisano 100% (brak limitu), a remont 0%, bo klientka go nie planuje. Turek ocenia za to „faktycznie niezbędne wydatki odpowiadające profilowi działalności” (kryterium 1 karty) i może obniżyć kwotę przy kosztach „niezasadnych lub zawyżonych” (cz. IV pkt 2). Dlatego skreślono drugą suszarkę i fotel hydrauliczny, a kwota (15 000 zł) jest wyraźnie niższa od 38 822 zł z ogłoszenia. Wykluczenia z Informacji (kasa fiskalna, szkolenia, wynajem lokalu, transport zakupów, leasing) – sprawdzone, żadna pozycja z dotacji ich nie dotyczy.

## 3. Przychody – założenia (arkusz `Przychody`)

| Usługa | Cena (zł) | Liczba / mies. przy pełnym obłożeniu | Czas 1 usługi (h) |
|---|---|---|---|
| Strzyżenie damskie z myciem i modelowaniem | 70 | 35 | 0,75 |
| Strzyżenie męskie / dziecięce | 40 | 25 | 0,5 |
| Strzyżenie seniora w domu (także osoby leżące) | 45 | 25 | 0,6 |
| Koloryzacja z farbą (włosy krótkie i średnie) | 180 | 12 | 2 |
| Upięcie okolicznościowe / ślubne | 180 | 3 | 1,5 |

| | 12.2026 | 01.2027 | 02.2027 | 03.2027 | 04.2027 | 05.2027 | 06.2027 | 07.2027 | 08.2027 | 09.2027 | 10.2027 | 11.2027 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Rozruch | 50% | 70% | 90% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| Sezonowość | 1,15 | 0,85 | 0,85 | 0,95 | 1,05 | 1,1 | 1,15 | 1 | 0,95 | 1,05 | 0,95 | 1 |
| Strzyżenie damskie z myciem i modelowaniem (szt.) | 20 | 21 | 27 | 33 | 37 | 39 | 40 | 35 | 33 | 37 | 33 | 35 |
| Strzyżenie męskie / dziecięce (szt.) | 14 | 15 | 19 | 24 | 26 | 28 | 29 | 25 | 24 | 26 | 24 | 25 |
| Strzyżenie seniora w domu (także osoby leżące) (szt.) | 14 | 15 | 19 | 24 | 26 | 28 | 29 | 25 | 24 | 26 | 24 | 25 |
| Koloryzacja z farbą (włosy krótkie i średnie) (szt.) | 7 | 7 | 9 | 11 | 13 | 13 | 14 | 12 | 11 | 13 | 11 | 12 |
| Upięcie okolicznościowe / ślubne (szt.) | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| Obłożenie czasu pracy | 38% | 39% | 49% | 62% | 69% | 72% | 75% | 65% | 62% | 69% | 62% | 65% |

Liczba usług przy pełnym obłożeniu pochodzi z kwestionariusza (3.2), rozruch 50% / 70% / 90% z odpowiedzi 13.1 („od razu te z zeszytu”), sezonowość z 3.5 i 13.2. Czas pracy z klientem: 21 dni × 6 h (bez dojazdów). Najwyższe obłożenie wychodzi poniżej 100%, więc plan jest wykonalny w czasie pracy jednej osoby. Dopłaty za dojazd poza Turek (10–20 zł) nie są w przychodach – to ostrożne założenie.

## 4. Koszty stałe miesięcznie (arkusz `Koszty`)

| Pozycja | zł / mies. |
|---|---|
| Czynsz / najem lokalu (nie dotyczy – praca mobilna) | 0 |
| Media (nie dotyczy) | 0 |
| Telefon i internet | 70 |
| Księgowość (biuro rachunkowe) | 200 |
| Ubezpieczenie OC działalności | 40 |
| Paliwo i eksploatacja auta | 650 |
| Reklama bieżąca (Facebook, Google) | 150 |
| Inne (abonament Booksy, konto firmowe, serwis kasy) | 150 |
| **Razem koszty stałe** | **1 260** |
| Materiały (koszt zmienny) | 10% przychodu |

Paliwo 650 zł/mies. to środek przedziału podanego przez klientkę (600–700 zł). Biuro rachunkowe 200 zł – wycena biura z Turku. OC 40 zł – szacunek klientki („nie wiem, 40?”), do potwierdzenia ofertą ubezpieczyciela. Kasa, Booksy i konto – 150 zł. Brak czynszu i mediów (praca mobilna, sprzęt w mieszkaniu klientki).

## 5. Kalkulacja 12 miesięcy – układ kwartalny (arkusz `Do-wniosku`, tabela 1a)

| Pozycja | Kw. I (mies. 1–3) | Kw. II (mies. 4–6) | Kw. III (mies. 7–9) | Kw. IV (mies. 10–12) | Razem 12 mies. |
|---|---|---|---|---|---|
| **Przychody ze sprzedaży** | **14 060** | **22 540** | **22 470** | **21 825** | **80 895** |
| **Koszty razem, w tym:** | **6 681** | **7 529** | **8 891** | **9 823** | **32 923** |
| – zakup materiałów i towarów | 1 406 | 2 254 | 2 247 | 2 183 | 8 090 |
| – telefon i internet | 210 | 210 | 210 | 210 | 840 |
| – księgowość (biuro rachunkowe) | 600 | 600 | 600 | 600 | 2 400 |
| – ubezpieczenie OC działalności | 120 | 120 | 120 | 120 | 480 |
| – paliwo i eksploatacja auta | 1 950 | 1 950 | 1 950 | 1 950 | 7 800 |
| – reklama bieżąca (Facebook, Google) | 450 | 450 | 450 | 450 | 1 800 |
| – inne (abonament Booksy, konto firmowe, serwis kasy) | 450 | 450 | 450 | 450 | 1 800 |
| – składki ZUS (społeczne) | 0 | 0 | 1 369 | 1 369 | 2 737 |
| – składka zdrowotna | 1 495 | 1 495 | 1 495 | 2 492 | 6 977 |
| **Dochód (przychody − koszty)** | **7 379** | **15 011** | **13 579** | **12 002** | **47 972** |
| Podatek dochodowy | 1 132 | 1 852 | 1 730 | 1 633 | 6 347 |
| **Dochód netto (po podatku)** | **6 247** | **13 159** | **11 849** | **10 369** | **41 625** |

Kontrola arkusza: suma kwartałów = suma miesięcy – OK.

### Ten sam rachunek miesiąc po miesiącu (wymóg rozporządzenia: przychody i koszty w 1. roku miesięcznie)

| Pozycja | 12.2026 | 01.2027 | 02.2027 | 03.2027 | 04.2027 | 05.2027 | 06.2027 | 07.2027 | 08.2027 | 09.2027 | 10.2027 | 11.2027 | Razem |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Przychody ze sprzedaży | 4 210 | 4 365 | 5 485 | 6 870 | 7 680 | 7 990 | 8 325 | 7 275 | 6 870 | 7 680 | 6 870 | 7 275 | 80 895 |
| Koszty razem, w tym: | 2 179 | 2 195 | 2 307 | 2 445 | 2 526 | 2 557 | 3 047 | 2 942 | 2 902 | 3 315 | 3 234 | 3 274 | 32 923 |
| – składki ZUS (społeczne) | 0 | 0 | 0 | 0 | 0 | 0 | 456 | 456 | 456 | 456 | 456 | 456 | 2 737 |
| – składka zdrowotna | 498 | 498 | 498 | 498 | 498 | 498 | 498 | 498 | 498 | 831 | 831 | 831 | 6 977 |
| Dochód (przychody − koszty) | 2 031 | 2 170 | 3 178 | 4 425 | 5 154 | 5 433 | 5 278 | 4 333 | 3 968 | 4 365 | 3 636 | 4 001 | 47 972 |
| Podatek dochodowy | 337 | 350 | 445 | 563 | 631 | 658 | 648 | 558 | 524 | 579 | 510 | 544 | 6 347 |
| Dochód netto (po podatku) | 1 694 | 1 820 | 2 733 | 3 862 | 4 523 | 4 775 | 4 630 | 3 775 | 3 444 | 3 786 | 3 126 | 3 457 | 41 625 |

## 6. Wskaźniki i próg rentowności (arkusze `Prognoza` i `Do-wniosku`, tabela 3)

| Wskaźnik | Scenariusz bazowy | Scenariusz −30% przychodów |
|---|---|---|
| Przychody w 12 mies. (zł) | 80 895 | 56 627 |
| Koszty w 12 mies. (zł) | 32 923 | 29 500 |
| Zysk roczny przed opodatkowaniem (zł) | 47 972 | 27 127 |
| Podatek dochodowy w 12 mies. (zł) | 6 347 | 4 326 |
| ZYSK ROCZNY NETTO (zł) | 41 625 | 22 801 |
| Średni zysk netto miesięcznie (zł) | 3 469 | 1 900 |
| Rentowność sprzedaży netto | 51,5% | 40,3% |
| Próg rentowności – przychód miesięczny (zł) | 2 299 | 2 299 |
| Próg rentowności – liczba sprzedaży / mies. | 32 | 32 |
| Zwrot z dotacji (zysk netto roczny ÷ dotacja) | 277,5% | 152,0% |
| Okres zwrotu dotacji (mies.) | 4,3 | 7,9 |
| Gotówka na koniec 12. miesiąca (zł) | 43 570 | 24 746 |
| Najniższe saldo gotówki w 12 mies. (zł) | 1 946 | 1 946 |
| Próg rentowności po okresie ulg ZUS (pełny ZUS) – przychód mies. (zł) | 4 187 | – |
| Średni przychód miesięczny od 4. miesiąca (zł) | 7 426 | 5 198 |
| Margines bezpieczeństwa (średni przychód od m4 vs próg) | 69% | 56% |
| Pierwszy miesiąc z dodatnim wynikiem netto | 1 | – |
| Najwyższe obłożenie czasu pracy | 75% | – |

Próg rentowności = średnie miesięczne koszty stałe z ZUS i składką zdrowotną (2 069 zł) ÷ (1 − udział materiałów 10%). Średnia cena jednej usługi w roku: 72,62 zł, stąd liczba usług w progu.

## 7. Scenariusz pesymistyczny (przychody o 30% niższe w każdym miesiącu)

Arkusz liczy wariant, w którym przychody w każdym miesiącu są o 30% niższe, a koszty stałe, ZUS i składka zdrowotna zostają bez zmian (materiały spadają razem z przychodem). Wynik: firma dalej ma zysk netto, a najniższe saldo gotówki jest takie samo jak w wariancie bazowym (1 946 zł), bo przypada na start – po zakupach z dotacji i wkładu własnego, przed pierwszym przychodem. Działania na wypadek niższych przychodów (z rozmowy z klientką 14.10.2026): stała współpraca z domem seniora co 6 tygodni, karnety rodzinne, mniej płatnej reklamy. Opisane w sekcji 09 wniosku.

**Słaby punkt do omówienia z klientką:** saldo na starcie 1 946 zł. Jeśli pierwszy miesiąc będzie słabszy niż 50% planu, klientka dopłaci z oszczędności domowych (pensja męża). Komisja może o to zapytać.

## 8. Kontrole spójności arkusza (`Zalozenia`, wiersze 27–34)

| Kontrola | Wynik |
|---|---|
| Kwota dotacji ≤ maksymalna kwota z naboru | OK |
| Wydatki z dotacji ≤ kwota dotacji | OK |
| Kwota dotacji nierozplanowana w kosztorysie (zł) | 0 |
| Limity kategorii wg regulaminu | OK |
| Najniższe saldo gotówki w 12 mies. – scenariusz bazowy (zł) | 1 945,90 |
| Najniższe saldo gotówki – scenariusz pesymistyczny (zł) | 1 945,90 |
| Najwyższe obłożenie godzin pracy | 75% |
| Przychód vs limit zwolnienia z VAT (rok startu proporcjonalnie, rok następny) | OK (poniżej limitu) |

### Uproszczenia modelu, o których trzeba wiedzieć

- Start 1.12.2026 – 11 z 12 miesięcy przypada na 2027 r., a arkusz liczy na stałych z 2026 r. (płaca minimalna, ZUS, składka zdrowotna). Po ogłoszeniu wskaźników na 2027 r. trzeba zaktualizować arkusz `Stale-2026` i wygenerować ten plik ponownie.
- Ryczałt 8,5% dla całego przychodu (usługi fryzjerskie). Model nie dzieli przychodu na stawki.
- Brak amortyzacji: zakupy z dotacji nie są kosztem w rachunku wyników (ostrożnie – podatek raczej zawyżony niż zaniżony).
- Zysk netto to dochód przed prywatnymi wydatkami klientki. Opłaty domowe pokrywa pensja męża (kwestionariusz 10.4).
