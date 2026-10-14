# Raport kontroli – warsztat mechaniczny, PUP Grodzisk Mazowiecki

> **DANE FIKCYJNE – PRZYKŁAD.** Przejście `docs/checklista-weryfikacji.md` przed wysłaniem treści klientowi. Data: 14.10.2026. ✔ sprawdzone, ⚠ wymaga działania przed złożeniem, – nie dotyczy.

## A. Kwalifikowalność klienta i naboru

| Punkt | Wynik | Jak sprawdzono |
|---|---|---|
| ⛔ Warunki z art. 148 | ✔ | „spełniam wszystkie”; firmy nie prowadził |
| ⛔ PUP właściwy dla miejsca zamieszkania | ✔ | mieszka w Grodzisku Maz. |
| ⛔ Regulamin tego naboru | ⚠ | naboru jeszcze nie ogłoszono. Pracujemy na regulaminie z 22.04.2026 (Zarządzenie nr 13/2026) i kryteriach z kwietnia 2026. Plik „kryteria… sierpień 2026” dotyczy PFRON – nie ma zastosowania. Po ogłoszeniu: sprawdzić kwotę maksymalną, źródło finansowania i wzór wniosku |
| Grupa docelowa (EFS+/program) | ⚠ | nieznana do czasu ogłoszenia; klient nie należy do grup z art. 69 (0 z 6 pkt w kryterium 1) |
| ⛔ Zabezpieczenie realne | ⚠ | Grodzisk: poręczenie = 2 osoby z min. 6 500 zł brutto po odjęciu rat; aval = 1 osoba z min. 7 500 zł brutto. Ojciec ok. 7 000 zł brutto – OK; szwagier ok. 9 000 − 2 300 zł raty = ok. 6 700 zł – na granicy. Klient dostał ostrzeżenie na piśmie (kwestionariusz, notatka do sekcji 2) |
| IPD | ✔ | doradca wpisał dotację do IPD (Grodzisk nie wymaga, ale pomaga) |

## B. Zgodność z regulaminem

| Punkt | Wynik | Uwagi |
|---|---|---|
| ⛔ Działalność nie jest wykluczona | ✔ | naprawa pojazdów – nie jest na liście wyłączeń (rolnictwo, sektory de minimis, spółki) |
| ⛔ Kwota ≤ maksimum z ogłoszenia i ≤ 6× przeciętne wynagrodzenie | ⚠ / ✔ | 39 400,00 zł ≤ 55 398,78 zł; maksimum z ogłoszenia – do sprawdzenia |
| ⛔ Pozycje w katalogu | ✔ | brak: remontu hali, najmu, ubezpieczeń, wizytówek i ulotek, leasingu, szkoleń, wyceny rzeczoznawcy, transportu zakupów (Rozdz. III ust. 4) |
| ⛔ Limity % od wnioskowanej kwoty | ✔ | towar 4 068,25 zł = 10,3% (limit 30%); reklama (kaseton, baner, strona) 2 706,00 zł = 6,9% (limit 15%) |
| Sprzęt używany | ✔ | brak – świadoma decyzja (wycena rzeczoznawcy przy zakupie od likwidowanej firmy, oświadczenie o braku dofinansowania, brak gwarancji); opis w kwestionariuszu 9.3 i w `kosztorys-i-prognoza.md` |
| Samochód | ✔ | laweta skreślona (ponad 60% dotacji, celowość, wymogi dla rzeczy używanych) |
| Załączniki | ✔ | lista w `wniosek.docx` i `co-wpisac-samemu.md` |

## C. Spójność liczb

| Punkt | Wynik | Uwagi |
|---|---|---|
| ⛔ Suma kosztorysu = kwota | ✔ | 39 400,00 zł: pola krótkie, sekcja 06, Tabela IV.3, Tabela IV.1 (32 625,75 + 4 068,25 + 2 706,00), IV.2, `Kosztorys!K26` |
| ⛔ Uzasadnienie i oferta przy każdej pozycji | ⚠ | uzasadnienia w Tabeli IV.3; oferty typu (otomoto, Ceneo) – klient dołącza konkretne oferty PDF, w tym od lokalnej hurtowni olejów i wykonawcy kasetonu |
| ⛔ Prognoza 12 miesięcy osobno | ✔ | formularz ma tylko tabelę średniomiesięczną – rozkład miesięczny dołączamy jako załącznik (sekcja 08 + `kosztorys-i-prognoza.md`, sekcja 5) |
| Ceny vs konkurencja | ✔ | kb.pl Grodzisk: olej 71,30 zł, tarcze i klocki przód 271 zł, sprzęgło 896 zł – ceny klienta równe lub niższe |
| Koszty kompletne | ✔ | czynsz, media, ZUS (ulga → preferencyjny z chorobowym), zdrowotna na skali (8 050 zł/rok), księgowość, odbiór odpadów, rezerwa na licencję testera |
| Sezonowość | ✔ | 0,90–1,10 (wrzesień–listopad i marzec–kwiecień wyżej) |
| Wynik realny | ✔ | strata w 1. miesiącu (−217 zł), zysk od 2. miesiąca; obłożenie maks. 63% |
| VAT | ✔ | zwolnienie podmiotowe; arkusz: przychód w roku startu poniżej limitu proporcjonalnego |
| Wkład własny | ✔ | 8 000 zł gotówki, zakupy z wkładu 2 337,00 zł, narzędzia ok. 6 000 zł |
| Zatrudnienie | ✔ | brak w 1. roku (pomocnik „za 2 lata” – opisany warunkowo, bez kosztów w arkuszu) |
| Liczby tekst = tabele | ✔ | `sprawdz.py`: 0 nieznanych liczb |

## D. Prawdziwość danych

| Punkt | Wynik | Uwagi |
|---|---|---|
| ⛔ Kwalifikacje tylko z kwestionariusza | ✔ | szkolenie Common Rail opisane uczciwie jako bez zaświadczenia i nie wpisane do dokumentów; brak F-gazów opisany wprost; nie dopisano „kół dwumasowych”, „regeneracji zacisków” ani pomiarów, o których klient nie mówił |
| ⛔ Konkurenci prawdziwi | ✔ | 4 z 4: nazwy i adresy z katalogu autocentrum.pl (14.10.2026). Opinie klienta o „drogich” i „odległych terminach” u konkretnych firm **usunięte** – brak źródła; opisy firm neutralne |
| ⛔ Listy intencyjne | ✔ | dwa skany z 10.10.2026 w zleceniu (firmy fikcyjne w przykładzie) |
| Lokal | ✔ | opis = zdjęcia + odpowiedzi (5.3); wylewka 20 cm wg wynajmującego – do potwierdzenia przy montażu podnośnika; Grodzisk przeprowadza wizję lokalną |
| Uprawnienia | ✔ | bez F-gazów → bez serwisu klimatyzacji; dozór UDT podnośnika oznaczony „do weryfikacji” |
| Obietnice | ✔ | brak; „termin 2–3 dni” to deklaracja organizacji pracy z kwestionariusza 8.2 |

## E. Zgodność z formularzem

| Punkt | Wynik | Uwagi |
|---|---|---|
| ⛔ Aktualny formularz | ⚠ | wzór ze strony ma podstawę prawną sprzed 1.06.2025 (stara ustawa, rozp. 2017). Treści ułożone pod jego pola; po ogłoszeniu naboru sprawdzić nowy wzór |
| ⛔ Limity znaków | ✔ | formularz bez limitów; regulamin § 5 ust. 2 pozwala zwiększać uzasadnienia i wiersze tabel, zabrania zmiany kolejności i treści |
| Pola osobowe | ✔ | pozostawione klientowi (strona tytułowa docx) |
| Zabezpieczenie | ✔ | „poręczenie” (3 pkt w kryterium 11) |
| PKD | ✔ | 95.31.A i 47.82.Z wg PKD 2025 (Dz.U. 2024 poz. 1936); klient podał kod z PKD 2007 (45.20.Z) – poprawione |
| Wymogi formalne | ✔ | „wpisać: brak, nie posiadam, nie wymagane” zamiast pustych rubryk – w polach krótkich |
| Zasada CEIDG w Grodzisku | ✔ | osoba bez NIP składa wniosek o wpis w dniu poprzedzającym umowę, działalność rozpoczyna po otrzymaniu środków (Rozdz. IV ust. 2 pkt 1) – instrukcja w docx |

## F. Test zakazanych zwrotów i „generycznego AI”

```bash
python3 narzedzia/sprawdz.py 02-mechanik-grodzisk-mazowiecki
```

```text
== 02-mechanik-grodzisk-mazowiecki
1) Długość sekcji (znaki ze spacjami, cel 1700–2300):
   sekcja 01:  2065  OK
   sekcja 02:  1816  OK
   sekcja 03:  1898  OK
   sekcja 04:  1747  OK
   sekcja 05:  1766  OK
   sekcja 06:  2080  OK
   sekcja 07:  1772  OK
   sekcja 08:  1845  OK
   sekcja 09:  1917  OK
2) Zakazane zwroty:
   razem trafień: 0
3) Kwoty i procenty spoza arkusza i listy dozwolonych:
   nieznanych liczb: 0
```

Ręcznie: ton techniczny – nazwy czynności (odczyt kodów EOBD, parametry bieżące, adaptacje, rozrząd na blokadach, kotwienie podnośnika, wymiana płynu bez zapowietrzenia ABS), parametry sprzętu (4 t, 270 l, 400 V, 20 t), procedury. Głos klienta: „wolę naprawiać”, „powiedzieć uczciwie, co jest pilne, a co może poczekać”. Konkrety lokalne: Kałęczyn i ul. Wylotowa, Książenice, Milanówek, Jaktorów, Żabia Wola, 4 firmy z adresami, ceny kb.pl, dane GUS.

## Karta oceny PUP Grodzisk Mazowiecki (kwiecień 2026, maks. 37 pkt)

| Kryterium | Pkt | Gdzie we wniosku | Dowód / ryzyko |
|---|---|---|---|
| 1. Grupy z art. 69 | 0–6 | – | klient nie należy do żadnej (0 pkt) – nie da się tego poprawić treścią |
| 2. Przygotowanie: wykształcenie kierunkowe / kursy / doświadczenie | 0–1 / 0–1 / 0–3 | 02, II.3b | technik pojazdów samochodowych (2012), szkolenie EOBD z zaświadczeniem, 8 lat (> 3 lata) – świadectwa pracy |
| 3. Lokal (dokument) / posiadany sprzęt | 0–1 / 0–1 | II.2, II.3c, IV.2, 06 | umowa przedwstępna najmu (⚠ regulamin mówi o „umowie najmu” – lepiej podpisać umowę przyrzeczoną przed złożeniem); narzędzia własne ok. 6 000 zł |
| 4. Przedsięwzięcie: lokalizacja, innowacyjność, zapotrzebowanie, miejsca pracy | 0–3 | 01, 03 | 70 dawnych klientów, 2 firmy z listami; zatrudnienie dopiero za ok. 2 lata (warunkowo) |
| 5. Celowość i racjonalność wydatków | 0–5 | 06, IV.3 | każda pozycja z uzasadnieniem technicznym; laweta i używany podnośnik świadomie odrzucone |
| 6. Rozpoznanie rynku i konkurencji / oświadczenia kontrahentów | 0–1 / 0–1 | 03, 04 / II.3c | 4 konkurentów z adresami, ceny kb.pl / 2 listy intencyjne |
| 7. Spójny i przejrzysty opis | 0–2 | 01 | pola II.1–II.4 bez powtórzeń, te same liczby co w arkuszu |
| 8. Analiza rynku i SWOT: klienci / ryzyka / szanse długotrwałego prowadzenia | 0–1 / 0–1 / 0–1 | 03 / 09 / 07, 08 | ryzyka z działaniami (8 pozycji); próg po ulgach ZUS (8 889 zł) podany wprost |
| 9. Analiza ekonomiczna | 0–3 | 08, tabela średniomiesięczna, IV.1–IV.2 | rozkład miesięczny w załączniku, próg rentowności, wariant −30% |
| 10. Ocena ogólna, czytelność, wizja lokalna | 0–3 | całość, II.2 | opis hali zgodny ze zdjęciami |
| 11. Forma zabezpieczenia | 3 / 2 / 1 / 0 | III | poręczenie = 3 pkt (⚠ dochód szwagra) |

## Pole formularza → sekcja → znaki

| Pole Grodzisk | Sekcja | Znaki |
|---|---|---|
| II.1, II.2, II.4a, II.4b | 01 | 2 065 |
| I.11 Przebieg pracy i kwalifikacje | 02 | 1 816 |
| II.4c – rynek odbiorców | 03 | 1 898 |
| II.4c – konkurencja | 04 | 1 747 |
| II.4e marketing | 05 | 1 766 |
| IV.3 uzasadnienie zakupu (opis zbiorczy) | 06 | 2 080 (+ tabela) |
| Zał. 2 SWOT | 07 | 1 772 |
| Załącznik – uzasadnienie założeń | 08 | 1 845 |
| Zał. 2 WNIOSKI | 09 | 1 917 |

## Liczby w tekście a arkusz

| Liczba | Źródło w `model.xlsx` |
|---|---|
| 39 400,00 zł; 2 337,00 zł; 8 000 zł | `ark_dotacja`, `ark_kosztorys_wklad`, `ark_wklad_wlasny` |
| 32 625,75 / 4 068,25 / 2 706,00 zł; 10,3%; 6,9% | `ark_kat_sprzet`, `ark_kat_towar`, `ark_kat_reklama`, `Kosztorys!D34`, `D35` |
| 181 960; 105 857; 5 667; 70 436; 5 870 zł | `ark_przychod_12m`, `ark_koszty_12m`, `ark_podatek_12m`, `ark_zysk_netto_12m`, `ark_zysk_netto_mies` |
| 6 593 zł / 48 zleceń; 8 889 zł; 16 701 zł; 61% | `ark_prog_rent_zl`, `ark_prog_rent_szt`, `ark_prog_rent_pelny_zus`, `ark_przychod_sredni_od_m4`, `ark_margines` |
| 127 372; 37 281; 3 107; 4 188; 5 446 zł | `_pes` + `ark_min_saldo` |
| 3 980 zł; 26%; 456,18 zł; 8 050 zł; 63% | `ark_koszty_stale_mies`, `ark_materialy_pct`, `ark_zus_m12`, `ark_zdrowotna_12m`, `ark_oblozenie_max` |
| tabela średniomiesięczna | `Do-wniosku!O7:O22` i `Przychody!O28:O32` ÷ 12 |

## Do zrobienia przed złożeniem

1. ⚠ Po ogłoszeniu naboru: maksymalna kwota, źródło finansowania, aktualny wzór wniosku – jeśli kwota maks. < 39 400 zł, zmieniamy arkusz (np. strona www lub laptop na wkład własny) i generujemy treści ponownie.
2. ⚠ Zaświadczenia o dochodach poręczycieli – policzyć dochód szwagra po odjęciu raty (próg 6 500 zł brutto).
3. ⚠ Umowa najmu (przyrzeczona) zamiast przedwstępnej – pewniejszy punkt za lokal.
4. ⚠ Oferty PDF do 16 pozycji; dla podnośnika – potwierdzenie dostawcy co do kotwienia w posadzce i dokumentacji UDT.
5. ⚠ Umowa z firmą odbierającą oleje przepracowane (przed startem).

## Źródła (sprawdzone 14.10.2026)

- Regulamin PUP Grodzisk Maz. z 22.04.2026: <https://grodziskmazowiecki.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-grodzisku-mazowieckim/regulamin-w-sprawie-skladania-i-rozpatrywania-wnioskow-o-przyznanie-dofinansowania-podjecia-dzialalnosci-gospodarczej-kwiecien-2026>
- Kryteria i punktacja (kwiecień 2026): <https://grodziskmazowiecki.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-grodzisku-mazowieckim/kryteria-i-punktacja-do-regulaminu-kwiecien-2026>
- Wzór wniosku: <https://grodziskmazowiecki.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-grodzisku-mazowieckim/wniosek-w-sprawie-dofinansowania-bezrobotnemu-absolwentowi-cis-absolwentowi-kis-opiekunowi-podjecia-dzialalnosci-gospodarczej-2025-1>
- Konkurenci (katalog firm, Grodzisk Maz.): <https://www.autocentrum.pl/firmy/wszystkie/mazowieckie/grodzisk-mazowiecki/>
- Średnie ceny warsztatów w Grodzisku Maz. (kb.pl, 29.04.2026): <https://kb.pl/cenniki/miejskie/warsztat-samochodowy/grodzisk-mazowiecki>
- Grodzisk Maz.: 34 904 mieszkańców (GUS, 31.12.2024, za polskawliczbach.pl): <https://www.polskawliczbach.pl/Grodzisk_Mazowiecki>
- Kałęczyn (gm. Grodzisk Maz.), położenie: <https://en.wikipedia.org/wiki/Ka%C5%82%C4%99czyn,_Gmina_Grodzisk_Mazowiecki>; ul. Wylotowa w Kałęczynie (ogłoszenia działek): <https://adresowo.pl/dzialki/kaleczyn-d/>
- Hale do wynajęcia w gminie (rząd wielkości czynszu, Kałęczyn 80 m² ok. 2 500 zł): <https://www.otodom.pl/pl/wyniki/wynajem/haleimagazyny/mazowieckie/grodziski/grodzisk-mazowiecki/kaleczyn>
- Oferta typu podnośnika z dokumentacją CE/UDT: <https://www.otomoto.pl/oferta/podnosnik-dwukolumnowy-euro-trade-sae-40-4000-kg-automatyczny-elektrohydrauliczny-ce-udt-ID6IaxBY.html>
- PKD 2025 (Dz.U. 2024 poz. 1936): <https://api.sejm.gov.pl/eli/acts/DU/2024/1936/text.pdf>
