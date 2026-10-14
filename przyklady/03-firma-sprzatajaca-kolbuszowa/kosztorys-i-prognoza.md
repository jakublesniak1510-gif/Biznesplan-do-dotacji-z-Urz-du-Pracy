# Kosztorys i prognoza – firma sprzątająca, PUP Kolbuszowa (EFS+)

> **DANE FIKCYJNE – PRZYKŁAD.** Wszystkie liczby w tabelach pochodzą z `model.xlsx` w tym katalogu (kopia `model-finansowy/model-finansowy-pup.xlsx` z danymi klientki, przeliczona przez LibreOffice `/usr/bin/soffice --headless --convert-to xlsx`). Plik wygenerował `przyklady/narzedzia/kosztorys_md.py`.
>
> Zasady: „Informacja dotycząca zasad udzielania dofinansowania podjęcia działalności gospodarczej w ramach projektu »Aktywizacja osób bezrobotnych z powiatu kolbuszowskiego (III)«” (EFS+, FE dla Podkarpacia 2021–2027), 2026 r., pkt 13: wykluczone m.in. remonty i adaptacje, transport zakupów, opłaty eksploatacyjne, szkolenia, samochód osobowy (poza nauką jazdy i taxi), środek transportu powyżej 50% dofinansowania, towary powyżej 30% dofinansowania, rzeczy używane od firm niehandlujących używanym sprzętem, kasa fiskalna, ubezpieczenia, telefon/tablet powyżej 2 000 zł, **wydatki reklamowe powyżej 2 000 zł**, doradztwo powyżej 1 000 zł, współwłasność. Ostatni nabór: 6–7.07.2026, do 40 000 zł.

## 1. Założenia wpisane do arkusza (`model.xlsx`, arkusz `Zalozenia`)

| Parametr | Wartość |
|---|---|
| Nazwa / branża | Firma sprzątająca – Kolbuszowa (DANE FIKCYJNE – przykład) |
| Kwota dotacji z PUP (zł) | 24 850,00 |
| Maksymalna kwota dotacji wg ogłoszenia naboru (zł) | 40 000,00 |
| Wkład własny – gotówka wniesiona na start (zł) | 8 000,00 |
| Data rozpoczęcia działalności | 01.03.2027 |
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
| Godziny pracy z klientem dziennie | 7 |
| Spadek przychodów – scenariusz pesymistyczny | 30% |

## 2. Specyfikacja wydatków (arkusz `Kosztorys`)

Klientka jest zwolniona z VAT – „do rozliczenia” = brutto. Linki: wyszukiwarka ofert Ceneo dla konkretnych modeli Kärcher i Unger (oferty typu); środki czystości, oklejenie, strona i druk – oferty lokalnych wykonawców do dołączenia.

**Dlaczego część zakupów jest z wkładu własnego:** karta oceny Kolbuszowej punktuje udział środków własnych w całkowitych kosztach przedsięwzięcia: 5–14,99% = 8 pkt, 15–24,99% = 12 pkt, od 25% = 16 pkt; formularz wymaga min. 5%. Parownica, zestaw Unger, drabina, ulotki, odzież i druga część chemii (razem 5 350,50 zł) idą z oszczędności klientki. Udział: 5 350,50 ÷ 30 200,50 = 17,7% → przedział 12 pkt. Próg 25% wymagałby ok. 2 900 zł więcej wkładu (przy tej samej dotacji) – klientka woli zostawić rezerwę 2 650 zł na start. To świadoma decyzja, opisana klientce.

**Limity:** towar 2 218 zł = 8,9% dofinansowania (limit 30%). Każdy wydatek reklamowy poniżej 2 000 zł: oklejenie 1 599 zł, strona 1 845 zł (z dotacji), ulotki 553,50 zł (wkład). Brak telefonu, kasy, samochodu, rzeczy używanych.

| Lp. | Pozycja | Kategoria | Nowy/używany | Ilość | Cena jedn. netto | Wartość netto | VAT | Brutto | Do rozliczenia | Finansowanie | Oferta typu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Odkurzacz piorący Kärcher Puzzi 10/1 | sprzęt | nowy | 1 | 3 900,00 | 3 900,00 | 897,00 | 4 797,00 | 4 797,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-karcher+puzzi+10/1) |
| 2 | Odkurzacz plecakowy Kärcher BV 5/1 Bp (schody, klatki) | sprzęt | nowy | 1 | 1 550,00 | 1 550,00 | 356,50 | 1 906,50 | 1 906,50 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-karcher+bv+5/1) |
| 3 | Odkurzacz na sucho Kärcher T 10/1 Adv HEPA | sprzęt | nowy | 1 | 1 100,00 | 1 100,00 | 253,00 | 1 353,00 | 1 353,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-karcher+t+10/1+adv) |
| 4 | Szorowarka kompaktowa Kärcher BR 30/4 C | sprzęt | nowy | 1 | 6 900,00 | 6 900,00 | 1 587,00 | 8 487,00 | 8 487,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-karcher+br+30/4+c) |
| 5 | Myjka do okien Kärcher WV 6 Plus | sprzęt | nowy | 1 | 400,00 | 400,00 | 92,00 | 492,00 | 492,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-karcher+wv+6+plus) |
| 6 | Wózek serwisowy z prasą do mopów i workiem na odpady | sprzęt | nowy | 1 | 1 100,00 | 1 100,00 | 253,00 | 1 353,00 | 1 353,00 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-wozek+serwisowy+do+sprzatania+z+prasa) |
| 7 | Mopy płaskie i ściereczki z mikrofibry w 4 kolorach (system stref), uchwyty | inne | nowy | 1 | 650,00 | 650,00 | 149,50 | 799,50 | 799,50 | dotacja | [ceneo.pl](https://www.ceneo.pl/;szukaj-mop+plaski+mikrofibra+zestaw) |
| 8 | Środki czystości – koncentraty z dozownikami (Ecolabel), pierwszy zapas na 3 mies. | towar | nowy | 1 | 1 803,25 | 1 803,25 | 414,75 | 2 218,00 | 2 218,00 | dotacja | [oferta hurtowni chemii profesjonalnej – do dołączenia] |
| 9 | Oklejenie samochodu folią z nazwą i telefonem | reklama | nowy | 1 | 1 300,00 | 1 300,00 | 299,00 | 1 599,00 | 1 599,00 | dotacja | [oferta firmy reklamowej – do dołączenia] |
| 10 | Strona www – wizytówka z cennikiem i formularzem | reklama | nowy | 1 | 1 500,00 | 1 500,00 | 345,00 | 1 845,00 | 1 845,00 | dotacja | [oferta wykonawcy – do dołączenia] |
| 11 | Parownica Kärcher SC 5 EasyFix (sprzątanie bez chemii) | sprzęt | nowy | 1 | 1 300,00 | 1 300,00 | 299,00 | 1 599,00 | 1 599,00 | wkład własny | [ceneo.pl](https://www.ceneo.pl/;szukaj-karcher+sc+5+easyfix) |
| 12 | Zestaw do mycia okien Unger (ściągaczki, kij teleskopowy, wiadro) | sprzęt | nowy | 1 | 700,00 | 700,00 | 161,00 | 861,00 | 861,00 | wkład własny | [ceneo.pl](https://www.ceneo.pl/;szukaj-unger+zestaw+do+mycia+okien) |
| 13 | Drabina aluminiowa 3 × 9 szczebli | sprzęt | nowy | 1 | 600,00 | 600,00 | 138,00 | 738,00 | 738,00 | wkład własny | [ceneo.pl](https://www.ceneo.pl/;szukaj-drabina+aluminiowa+3x9) |
| 14 | Ulotki i wizytówki | reklama | nowy | 1 | 450,00 | 450,00 | 103,50 | 553,50 | 553,50 | wkład własny | [oferta drukarni – do dołączenia] |
| 15 | Odzież robocza i obuwie ochronne | inne | nowy | 1 | 300,00 | 300,00 | 69,00 | 369,00 | 369,00 | wkład własny | [ceneo.pl](https://www.ceneo.pl/;szukaj-odziez+robocza+damska) |
| 16 | Środki czystości – druga część zapasu | towar | nowy | 1 | 1 000,00 | 1 000,00 | 230,00 | 1 230,00 | 1 230,00 | wkład własny | [oferta hurtowni – do dołączenia] |
| | **RAZEM** | | | | | 24 553,25 | 5 647,25 | 30 200,50 | **30 200,50** | | |
| | w tym z dotacji | | | | | | | | **24 850,00** | dotacja | |
| | w tym z wkładu własnego | | | | | | | | **5 350,50** | wkład własny | |

Kontrola arkusza: OK – dotacja rozplanowana; suma kategorii = suma z dotacji: OK.

### Limity kategorii według regulaminu urzędu

| Kategoria | Limit wpisany do arkusza | Suma z dotacji (zł) | Udział w dotacji | Status |
|---|---|---|---|---|
| sprzęt | brak limitu % | 18 388,50 | 74,0% | OK |
| towar | 30% | 2 218,00 | 8,9% | OK |
| reklama | brak limitu % | 3 444,00 | 13,9% | OK |
| remont | wykluczone | 0,00 | 0,0% | OK |
| inne | brak limitu % | 799,50 | 3,2% | OK |

W arkuszu: towar 30%, remont 0% (wykluczony), reklama 100% – limit Kolbuszowej jest kwotowy na każdy wydatek (≤ 2 000 zł), a nie procentowy, więc sprawdzono go ręcznie (wyżej). Sprzęt i inne – bez limitu.

## 3. Przychody – założenia (arkusz `Przychody`)

| Usługa | Cena (zł) | Liczba / mies. przy pełnym obłożeniu | Czas 1 usługi (h) |
|---|---|---|---|
| Sprzątanie biura / gabinetu – wizyta ok. 2 h | 100 | 24 | 2 |
| Sprzątanie klatki schodowej – wizyta | 90 | 18 | 1,5 |
| Mycie okna dwuskrzydłowego | 45 | 30 | 0,4 |
| Sprzątanie jednorazowe: mieszkanie lub po remoncie (średnio) | 450 | 3 | 6 |
| Pranie wykładziny lub tapicerki (średnio na zlecenie) | 250 | 3 | 2,5 |

| | 03.2027 | 04.2027 | 05.2027 | 06.2027 | 07.2027 | 08.2027 | 09.2027 | 10.2027 | 11.2027 | 12.2027 | 01.2028 | 02.2028 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Rozruch | 50% | 70% | 85% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| Sezonowość | 1,1 | 1,2 | 1,05 | 1 | 0,85 | 0,85 | 1 | 1,05 | 1,05 | 1,15 | 0,85 | 0,85 |
| Sprzątanie biura / gabinetu – wizyta ok. 2 h (szt.) | 13 | 20 | 21 | 24 | 20 | 20 | 24 | 25 | 25 | 28 | 20 | 20 |
| Sprzątanie klatki schodowej – wizyta (szt.) | 10 | 15 | 16 | 18 | 15 | 15 | 18 | 19 | 19 | 21 | 15 | 15 |
| Mycie okna dwuskrzydłowego (szt.) | 17 | 25 | 27 | 30 | 26 | 26 | 30 | 32 | 32 | 35 | 26 | 26 |
| Sprzątanie jednorazowe: mieszkanie lub po remoncie (średnio) (szt.) | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| Pranie wykładziny lub tapicerki (średnio na zlecenie) (szt.) | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| Obłożenie czasu pracy | 44% | 67% | 70% | 77% | 67% | 67% | 77% | 79% | 79% | 86% | 67% | 67% |

Ceny i liczba zleceń przy pełnym obłożeniu – kwestionariusz 3.2. Listy intencyjne (biuro 2 razy w tygodniu, gabinet 3 razy, 2 klatki co tydzień) dają ok. 30 wizyt miesięcznie od startu; resztę planu (kolejne biuro i 2–3 klatki) klientka pozyska w pierwszych miesiącach – stąd rozruch 50% / 70% / 85%. Sezonowość z 3.5 i 13.2 (okna wiosną i przed świętami, słabiej latem). Czas pracy z klientami: 21 dni × 7 h; obłożenie maks. 86% w grudniu – plan wykonalny dla jednej osoby, ale bez dużego zapasu (zob. ryzyko zdrowotne w sekcji 09 wniosku).

## 4. Koszty stałe miesięcznie (arkusz `Koszty`)

| Pozycja | zł / mies. |
|---|---|
| Czynsz / najem lokalu (nie dotyczy – sprzęt w garażu własnym) | 0 |
| Media (nie dotyczy) | 0 |
| Telefon i internet | 60 |
| Księgowość (biuro rachunkowe, ryczałt) | 180 |
| Ubezpieczenie OC działalności | 60 |
| Paliwo i eksploatacja auta | 400 |
| Reklama bieżąca | 100 |
| Inne (worki, rękawice, konto firmowe, drobne naprawy) | 120 |
| **Razem koszty stałe** | **920** |
| Materiały (koszt zmienny) | 7% przychodu |

Paliwo 400 zł – krótkie trasy w promieniu 15 km (kwestionariusz 13.3). OC 60 zł – wycena ubezpieczyciela podana przez klientkę. Środki czystości zużywane w usługach: 7% przychodu (klientka: 5–7%, przyjęto górną granicę). Brak czynszu i mediów – sprzęt w garażu własnym.

## 5. Kalkulacja 12 miesięcy – układ kwartalny (arkusz `Do-wniosku`, tabela 1a)

| Pozycja | Kw. I (mies. 1–3) | Kw. II (mies. 4–6) | Kw. III (mies. 7–9) | Kw. IV (mies. 10–12) | Razem 12 mies. |
|---|---|---|---|---|---|
| **Przychody ze sprzedaży** | **17 795** | **20 710** | **22 970** | **21 605** | **83 080** |
| **Koszty razem, w tym:** | **5 501** | **5 705** | **7 564** | **7 468** | **26 237** |
| – zakup materiałów i towarów | 1 246 | 1 450 | 1 608 | 1 512 | 5 816 |
| – telefon i internet | 180 | 180 | 180 | 180 | 720 |
| – księgowość (biuro rachunkowe, ryczałt) | 540 | 540 | 540 | 540 | 2 160 |
| – ubezpieczenie OC działalności | 180 | 180 | 180 | 180 | 720 |
| – paliwo i eksploatacja auta | 1 200 | 1 200 | 1 200 | 1 200 | 4 800 |
| – reklama bieżąca | 300 | 300 | 300 | 300 | 1 200 |
| – inne (worki, rękawice, konto firmowe, drobne naprawy) | 360 | 360 | 360 | 360 | 1 440 |
| – składki ZUS (społeczne) | 0 | 0 | 1 369 | 1 369 | 2 737 |
| – składka zdrowotna | 1 495 | 1 495 | 1 827 | 1 827 | 6 645 |
| **Dochód (przychody − koszty)** | **12 294** | **15 005** | **15 406** | **14 137** | **56 843** |
| Podatek dochodowy | 1 449 | 1 697 | 1 758 | 1 642 | 6 546 |
| **Dochód netto (po podatku)** | **10 845** | **13 308** | **13 648** | **12 495** | **50 297** |

Kontrola arkusza: suma kwartałów = suma miesięcy – OK.

### Ten sam rachunek miesiąc po miesiącu (wymóg rozporządzenia: przychody i koszty w 1. roku miesięcznie)

| Pozycja | 03.2027 | 04.2027 | 05.2027 | 06.2027 | 07.2027 | 08.2027 | 09.2027 | 10.2027 | 11.2027 | 12.2027 | 01.2028 | 02.2028 | Razem |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Przychody ze sprzedaży | 4 365 | 6 575 | 6 855 | 7 470 | 6 620 | 6 620 | 7 470 | 7 750 | 7 750 | 8 365 | 6 620 | 6 620 | 83 080 |
| Koszty razem, w tym: | 1 724 | 1 879 | 1 898 | 1 941 | 1 882 | 1 882 | 2 397 | 2 417 | 2 749 | 2 792 | 2 338 | 2 338 | 26 237 |
| – składki ZUS (społeczne) | 0 | 0 | 0 | 0 | 0 | 0 | 456 | 456 | 456 | 456 | 456 | 456 | 2 737 |
| – składka zdrowotna | 498 | 498 | 498 | 498 | 498 | 498 | 498 | 498 | 831 | 831 | 498 | 498 | 6 645 |
| Dochód (przychody − koszty) | 2 641 | 4 696 | 4 957 | 5 529 | 4 738 | 4 738 | 5 073 | 5 333 | 5 001 | 5 573 | 4 282 | 4 282 | 56 843 |
| Podatek dochodowy | 350 | 538 | 561 | 614 | 541 | 542 | 575 | 599 | 584 | 637 | 503 | 502 | 6 546 |
| Dochód netto (po podatku) | 2 291 | 4 158 | 4 396 | 4 915 | 4 197 | 4 196 | 4 498 | 4 734 | 4 417 | 4 936 | 3 779 | 3 780 | 50 297 |

## 6. Wskaźniki i próg rentowności (arkusze `Prognoza` i `Do-wniosku`, tabela 3)

| Wskaźnik | Scenariusz bazowy | Scenariusz −30% przychodów |
|---|---|---|
| Przychody w 12 mies. (zł) | 83 080 | 58 156 |
| Koszty w 12 mies. (zł) | 26 237 | 23 828 |
| Zysk roczny przed opodatkowaniem (zł) | 56 843 | 34 328 |
| Podatek dochodowy w 12 mies. (zł) | 6 546 | 4 457 |
| ZYSK ROCZNY NETTO (zł) | 50 297 | 29 871 |
| Średni zysk netto miesięcznie (zł) | 4 191 | 2 489 |
| Rentowność sprzedaży netto | 60,5% | 51,4% |
| Próg rentowności – przychód miesięczny (zł) | 1 830 | 1 830 |
| Próg rentowności – liczba sprzedaży / mies. | 19 | 19 |
| Zwrot z dotacji (zysk netto roczny ÷ dotacja) | 202,4% | 120,2% |
| Okres zwrotu dotacji (mies.) | 5,9 | 10,0 |
| Gotówka na koniec 12. miesiąca (zł) | 52 946 | 32 520 |
| Najniższe saldo gotówki w 12 mies. (zł) | 2 650 | 2 650 |
| Próg rentowności po okresie ulg ZUS (pełny ZUS) – przychód mies. (zł) | 3 656 | – |
| Średni przychód miesięczny od 4. miesiąca (zł) | 7 254 | 5 078 |
| Margines bezpieczeństwa (średni przychód od m4 vs próg) | 75% | 64% |
| Pierwszy miesiąc z dodatnim wynikiem netto | 1 | – |
| Najwyższe obłożenie czasu pracy | 86% | – |

Próg rentowności = średnie miesięczne koszty stałe z ZUS i składką zdrowotną (1 702 zł) ÷ (1 − udział materiałów 7%). Średnia cena jednej usługi w roku: 96,83 zł, stąd liczba usług w progu.

## 7. Scenariusz pesymistyczny (przychody o 30% niższe w każdym miesiącu)

Wariant: przychody o 30% niższe w każdym miesiącu, koszty stałe i ZUS bez zmian. Firma nadal ma zysk netto. Najniższe saldo gotówki (2 650 zł) jest takie samo w obu wariantach, bo przypada na start – po zakupach z dotacji i wkładu, przed pierwszym przychodem. Klientka nie ma innych dochodów; wydatki domowe ok. 2 000 zł miesięcznie (kwestionariusz 10.4) – zysk netto w wariancie pesymistycznym jest od nich wyższy, ale w pierwszym miesiącu (rozruch 50%) trzeba je pokryć z rezerwy. Działania na wypadek niższych przychodów (rozmowa 14.10.2026): więcej okien i mieszkań, ulotki w nowych blokach, rozmowa z zarządcą spółdzielni o klatkach.

## 8. Kontrole spójności arkusza (`Zalozenia`, wiersze 27–34)

| Kontrola | Wynik |
|---|---|
| Kwota dotacji ≤ maksymalna kwota z naboru | OK |
| Wydatki z dotacji ≤ kwota dotacji | OK |
| Kwota dotacji nierozplanowana w kosztorysie (zł) | 0 |
| Limity kategorii wg regulaminu | OK |
| Najniższe saldo gotówki w 12 mies. – scenariusz bazowy (zł) | 2 649,50 |
| Najniższe saldo gotówki – scenariusz pesymistyczny (zł) | 2 649,50 |
| Najwyższe obłożenie godzin pracy | 86% |
| Przychód vs limit zwolnienia z VAT (rok startu proporcjonalnie, rok następny) | OK (poniżej limitu) |

### Uproszczenia modelu

- Start 1.03.2027 – 12 miesięcy przypada na 2027–2028 r., a arkusz liczy na stałych z 2026 r. Po ogłoszeniu wskaźników na 2027 r. zaktualizować `Stale-2026` i wygenerować plik ponownie.
- Ryczałt 8,5% dla wszystkich usług sprzątania [do weryfikacji z księgową: stawka dla PKWiU 81.21 i 81.22].
- Brak amortyzacji sprzętu z dotacji – podatek raczej zawyżony.
- Kasa fiskalna: arkusz jej nie zawiera. Obowiązek zależy od obrotu z osobami prywatnymi – jeśli powstanie, kasę klientka kupi z własnych środków (Kolbuszowa jej nie finansuje).
