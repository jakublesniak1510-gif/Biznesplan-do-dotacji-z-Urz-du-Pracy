# Raport kontroli – fryzjerka mobilna, PUP Turek

> **DANE FIKCYJNE – PRZYKŁAD.** Raport pokazuje, jak właściciel przechodzi `docs/checklista-weryfikacji.md` przed wysłaniem treści klientce. Data kontroli: 14.10.2026. Oznaczenia: ✔ sprawdzone, ⚠ wymaga działania klientki przed złożeniem, – nie dotyczy.

## A. Kwalifikowalność klientki i naboru

| Punkt checklisty | Wynik | Jak sprawdzono |
|---|---|---|
| ⛔ Warunki z art. 148 (pyt. 1.6) | ✔ | „spełniam wszystkie”; firmy nigdy nie prowadziła (Turek pyta o to osobno – klientka zaznacza NIE) |
| ⛔ PUP właściwy dla miejsca zamieszkania | ✔ | mieszka w Turku → PUP Turek |
| ⛔ Regulamin tego naboru | ✔ | „Informacja… w PUP w Turku w 2026 roku” (stan 06.08.2026, plik `informacja-aktualna`) + ogłoszenie naboru 12–16.10.2026 (rezerwa FP, 38 822 zł na 1 osobę) |
| Warunek programu (grupa docelowa) | ✔ | program dla bezrobotnych zwolnionych z przyczyn niedotyczących pracowników, w tym przy likwidacji pracodawcy. Świadectwo pracy: wypowiedzenie z powodu likwidacji salonu (skan w zleceniu) |
| ⛔ Zabezpieczenie realne wg wymogów Turku | ✔ | Turek: 2 poręczycieli ≥ 4 900 zł brutto (po odjęciu zobowiązań) albo 1 z ≥ 8 500 zł brutto, zgoda małżonka wnioskodawczyni. Brat (UoP na czas nieokreślony, ok. 5 600 zł brutto) i teść (emerytura ok. 6 000 zł brutto) – spełniają według deklaracji |
| IPD | ⚠ | Turek nie wymaga dotacji w IPD; klientka dopyta doradczynię (pyt. 1.9 „nie wiem”) |

## B. Zgodność z regulaminem

| Punkt checklisty | Wynik | Uwagi |
|---|---|---|
| ⛔ Rodzaj działalności nie jest wykluczony | ✔ | usługi fryzjerskie; Informacja Turku nie wyklucza branż, de minimis bez ograniczeń dla tej działalności |
| ⛔ Kwota ≤ maksimum z ogłoszenia i ≤ 6× przeciętne wynagrodzenie | ✔ | 15 000,00 zł ≤ 38 822 zł ≤ 55 398,78 zł |
| ⛔ Pozycje w katalogu, brak zakazanych | ✔ | Turek wyklucza m.in. kasę fiskalną, szkolenia, wynajem lokalu, transport zakupów, leasing, koszty przygotowania wniosku (cz. IV pkt 1). Kasa → wkład własny. Żadna pozycja z dotacji nie jest na liście wykluczeń |
| ⛔ Limity procentowe | – | Turek nie ma limitów %; kontrola arkusza `Kosztorys!E33:E37` = OK |
| Sprzęt używany | – | brak (wszystko nowe) |
| Samochód | – | brak zakupu (własna Toyota Yaris 2013) |
| Załączniki z regulaminu na liście dla klientki | ✔ | `wniosek.docx` strona 1 i `materialy-klienta/co-wpisac-samemu.md` |

## C. Spójność liczb

| Punkt checklisty | Wynik | Uwagi |
|---|---|---|
| ⛔ Suma kosztorysu = kwota wnioskowana | ✔ | 15 000,00 zł w: polach krótkich, sekcji 06, Tabeli 2, Tabeli 1, `model.xlsx` (`Kosztorys!K26`, `Zalozenia!B5`) |
| ⛔ Każda pozycja ma uzasadnienie i ofertę | ⚠ | uzasadnienia: Tabela 2. Linki to **oferty typu** lub wyszukiwarka (Ceneo); 5 pozycji wymaga oferty lokalnego wykonawcy (hurtownia, oklejanie, strona, drukarnia). Klientka dołącza wydruki przed złożeniem |
| ⛔ Prognoza 12 miesięcy osobno | ✔ | `kosztorys-i-prognoza.md`, sekcja 5 (miesiąc po miesiącu i kwartalnie) |
| Ceny usług = cennik klientki i w zakresie konkurencji | ✔ | 70 / 40 / 45 / 180 / 180 zł; konkurencja: GOLD ANGEL od 60 zł, kb.pl Turek średnio 77,60 zł (krótkie) i 228 zł (farbowanie) |
| Koszty kompletne (ZUS, zdrowotna, księgowość, paliwo, materiały) | ✔ | ulga na start 6 mies. → preferencyjny z chorobowym (456,18 zł), zdrowotna ryczałt (6 977 zł/rok) |
| Sezonowość widoczna w rozkładzie | ✔ | mnożniki 0,85–1,15 (grudzień, maj–czerwiec wyżej; styczeń–luty niżej) |
| Wynik realny | ✔ | zysk od 1. miesiąca uzasadniony listą 37 osób i rozruchem od 50%; obłożenie maks. 75% |
| VAT | – | zwolnienie podmiotowe; arkusz: przychód poniżej limitu |
| Wkład własny = deklaracja | ✔ | 4 000 zł gotówki (`Zalozenia!B7`), zakupy z wkładu 2 054,10 zł |
| Liczby w tekście = tabele | ✔ | skrypt `narzedzia/sprawdz.py` – 0 liczb spoza arkusza i listy dozwolonych (wynik niżej) |

## D. Prawdziwość danych

| Punkt checklisty | Wynik | Uwagi |
|---|---|---|
| ⛔ Kwalifikacje tylko z kwestionariusza | ✔ | kurs 300 h (2023), koloryzacja (2024), barbering (2025, bez certyfikatu – tak opisane), prawo jazdy B. Brak czeladnika opisany wprost. Nie dopisano kursów ani lat |
| ⛔ Konkurenci prawdziwi, sprawdzone ≥ 2 | ✔ | 4 z 4 sprawdzone w Booksy 14.10.2026 (nazwy, adresy, ceny, oceny); Beznazwa – ok. 17 km na N od Turku (współrzędne wsi). Kontrola wykryła zakład z dojazdem w Turku (Fryzjer dla Ciebie), o którym klientka nie wiedziała – dopisany, wyróżnik zmieniony z „jedyna z dojazdem” na „osoby leżące, koloryzacja w domu, soboty”. Słabe strony konkurentów opisane tylko faktami z cennika (np. „bez dojazdu”) |
| ⛔ Listy intencyjne istnieją | ⚠ | list od domu seniora „Spokojna Przystań” – klientka dostarczy skan; bez skanu usuwamy zdanie z sekcji 03 i punkt z SWOT |
| Lokal = rzeczywistość | – | działalność mobilna; miejsce przechowywania opisane zgodnie z rozmową (szafa w mieszkaniu, nie piwnica) |
| Uprawnienia | ✔ | brak wymaganych zezwoleń; kasa fiskalna od pierwszej usługi |
| Brak obietnic | ✔ | zatrudnienie opisane warunkowo („jeśli pracy będzie więcej… za rok lub dwa”) – tak jak powiedziała klientka |

## E. Zgodność z formularzem PUP Turek

| Punkt | Wynik | Uwagi |
|---|---|---|
| ⛔ Aktualny formularz | ✔ | `wniosek-propozycja.docx` (podstawa: ustawa z 20.03.2025 i rozporządzenie z 21.11.2025) |
| ⛔ Limity znaków | ✔ | formularz Turku nie podaje limitów (wykropkowane linie, „w przypadku braku miejsca – załącznik nr 2”). Wariant standard ~2000 znaków/sekcja |
| Pola osobowe puste z dopiskiem | ✔ | lista w `wniosek.docx` (strona tytułowa) |
| Forma zabezpieczenia jak w formularzu | ✔ | „poręczenie” |
| PKD w formacie podklasy | ✔ | 96.21.Z „Działalność fryzjerska” – rozporządzenie RM w sprawie PKD 2025 (Dz.U. 2024 poz. 1936) |
| Oświadczenia i de minimis jako „do podpisania przez Ciebie” | ✔ | `co-wpisac-samemu.md` |
| Wymogi formalne urzędu | ✔ | Turek: „wszystkie pozycje… muszą zostać wypełnione, w przypadku gdy… nie dotyczy – należy wpisać »nie dotyczy«”, bez zmian szaty graficznej – w polach krótkich wpisano „nie dotyczy” |

## F. Brak „generycznego AI” – test zakazanych zwrotów

Polecenie (z katalogu `przyklady/`):

```bash
python3 narzedzia/sprawdz.py 01-fryzjerka-mobilna-turek
```

Wynik z 14.10.2026:

```text
== 01-fryzjerka-mobilna-turek
1) Długość sekcji (znaki ze spacjami, cel 1700–2300):
   sekcja 01:  1726  OK
   sekcja 02:  1914  OK
   sekcja 03:  1854  OK
   sekcja 04:  1802  OK
   sekcja 05:  1822  OK
   sekcja 06:  1817  OK
   sekcja 07:  1906  OK
   sekcja 08:  1710  OK
   sekcja 09:  1884  OK
2) Zakazane zwroty:
   razem trafień: 0
3) Kwoty i procenty spoza arkusza i listy dozwolonych:
   nieznanych liczb: 0
```

Skrypt sprawdza `wniosek.md` i `wniosek.docx` według 46 reguł z `narzedzia/zakazane.txt` (lista z `szablony/00-system-prompt.md` z odmianami, np. `kompleksow`, `indywidualn\w* podejści`, `\bzawsze\b`, `gwarantuj`). Pomija cytaty nazw pól urzędu (linie „*Pole…*”) i tabelę mapowania.

Ręcznie sprawdzone dodatkowo:
- konkrety: ulice (Kaliska, pl. Wojska Polskiego 5, Komunalna 2, Pietrzaków 2), osiedla (Wyzwolenia, Spółdzielców), 8 gmin z nazwy, 4 konkurentów z cenami, modele sprzętu, dane GUS ze źródłem ✔;
- pierwsza osoba, głos klientki (zwroty z kwestionariusza: „za darmo”, „klientki dzwoniły, gdzie teraz chodzić”, „zeszyt”) ✔;
- ton ciepły: sytuacje z życia (babcia po udarze, wanienka, upięcie rano w domu panny młodej), bez patosu i wykrzykników ✔;
- test bliźniaka: pierwszy wniosek do PUP Turek w rejestrze – brak porównania; dwa pozostałe przykłady idą do innych urzędów i mają inny ton.

## C (karta). Karta oceny PUP Turek – które sekcje odpowiadają na które kryteria

Karta z „Informacji… 2026”: maks. 31 pkt, próg 16 pkt. Punktów nie przewidujemy – kolumna „ryzyko” mówi, gdzie komisja może obciąć.

| Kryterium karty | Pkt | Gdzie we wniosku | Dowód / ryzyko |
|---|---|---|---|
| 1. Wydatki faktycznie niezbędne, zgodne z profilem | 0–1 | 06 + Tabela 2 | każda pozycja powiązana z usługą; skreślona druga suszarka i fotel hydrauliczny; kwota 15 000 zł z 38 822 zł |
| 2. Miejsce – działalność mobilna: przygotowanie, dojazd, uprawnienia do kierowania, pozyskanie klienta, promocja, mobilne wyposażenie | 0–2 | 01, pola krótkie, 05, 06 | prawo jazdy B od 2012, własne auto, zasięg 25 km z nazwami gmin, przenośna umywalka, wanienka, walizka, lampa, oklejone auto |
| 3a. Rozeznanie rynku: dostawcy, odbiorcy, konkurencja, wyróżnik | 0–2 | 03, 04, pola krótkie (dostawcy) | 4 konkurentów z cenami i ocenami, dane GUS, hurtownia w Kaliszu |
| 3b. Umowy przedwstępne, listy intencyjne | 0–1 | 03, 07 | ⚠ 1 list (dom seniora) – tylko jeśli skan dotrze |
| 4. Opłacalność, sposób wyliczenia przychodów, prognoza | 0–5 | 08, Tabela 4, kosztorys | cena × liczba usług, rozruch, sezonowość, próg 2 299 zł, wariant −30% |
| 5a. Innowacyjny, niszowy rodzaj działalności | 0–2 | 01, 04 | strzyżenie osób leżących i koloryzacja w domu klienta; ryzyko: w Turku już dojeżdżają 2 zakłady, więc komisja może nie uznać usługi za niszową |
| 5b. Ryzyka i działania zaradcze | 0–2 | 09, 07 | 6 ryzyk, działania z rozmowy z klientką; wariant −30% z liczbami |
| 5c. Wykształcenie, kwalifikacje, kursy | 0–5 | 02a, 02c | ryzyko: brak szkoły zawodowej i czeladnika; kurs 300 h + 2 szkolenia |
| 5d. Udokumentowane doświadczenie w branży | 0–5 | 02b | ok. 3 lata w salonie (świadectwo pracy) + praca nieformalna opisana jako nieformalna |
| 5e. Udział środków własnych (finansowy, rzeczowy) | 0–2 | pola krótkie (zasoby), 06, Tabela 1 | 2 054,10 zł zakupów z wkładu + samochód i narzędzia |
| 6. Całościowość opisu: przejrzystość, spójność założeń, realność | 0–4 | całość | liczby z jednego arkusza, te same nazwy ryzyk w 07 i 09 |

## Pole formularza → sekcja → liczba znaków

| Pole Turek | Sekcja | Znaki |
|---|---|---|
| Zał. 2 – motywacja, opis działalności głównej i dodatkowej, rozwój | 01 | 1 726 |
| Wykształcenie / Doświadczenie / Umiejętności i szkolenia | 02 (02a–02c) | 1 914 |
| Analiza popytu | 03 | 1 854 |
| Analiza konkurencji | 04 | 1 802 |
| Reklama i promocja | 05 | 1 822 |
| Zał. 1 Tabela 2 – uzasadnienia + Posiadane zasoby | 06 | 1 817 (+ tabela) |
| Analiza SWOT (Tabela 1 i 2) | 07 | 1 906 |
| Uzasadnienie przyjętych założeń (do Tabeli 4) | 08 | 1 710 |
| Identyfikacja ryzyka (Tabela 3) | 09 | 1 884 |

## Liczby w tekście a arkusz

| Liczba w tekście | Komórka / nazwa w `model.xlsx` |
|---|---|
| 15 000,00 zł; 2 054,10 zł; 4 000 zł | `ark_dotacja`, `ark_kosztorys_wklad`, `ark_wklad_wlasny` |
| 7 539,90 / 3 278,10 / 3 198,00 / 984,00 zł | `ark_kat_sprzet`, `ark_kat_towar`, `ark_kat_reklama`, `ark_kat_inne` |
| 80 895 zł; 32 923 zł; 6 347 zł; 41 625 zł; 3 469 zł | `ark_przychod_12m`, `ark_koszty_12m`, `ark_podatek_12m`, `ark_zysk_netto_12m`, `ark_zysk_netto_mies` |
| 2 299 zł / 32 usługi; 4 187 zł | `ark_prog_rent_zl`, `ark_prog_rent_szt`, `ark_prog_rent_pelny_zus` |
| 7 426 zł; 5 198 zł | `ark_przychod_sredni_od_m4`, `Prognoza!C32` |
| 56 627 zł; 22 801 zł; 1 900 zł; 1 946 zł | `ark_przychod_12m_pes`, `ark_zysk_netto_12m_pes`, `ark_zysk_netto_mies_pes`, `ark_min_saldo` |
| 1 260 zł; 10%; 456,18 zł; 6 977 zł; 75% | `ark_koszty_stale_mies`, `ark_materialy_pct`, `ark_zus_m12`, `ark_zdrowotna_12m`, `ark_oblozenie_max` |
| Tabela 4 (miesięcznie) | wartości roczne z `Do-wniosku!O7:O22` ÷ 12 |

## Do zrobienia przed złożeniem (lista dla klientki)

1. ⚠ Skan listu intencyjnego domu seniora „Spokojna Przystań” (wzór: `materialy-klienta/list-intencyjny-wzor.md`).
2. ⚠ Pełna nazwa ośrodka szkoleniowego z Konina – zastąpić znacznik `[BRAK DANYCH]` w sekcji 02a.
3. ⚠ Wydruki ofert do 17 pozycji Tabeli 2 (linki w `kosztorys-i-prognoza.md`); ceny mogą się różnić o kilka procent – wtedy poprawiamy arkusz, a nie tekst.
4. ⚠ Oferta OC działalności (w arkuszu szacunek 40 zł/mies.).
5. Zaświadczenia o dochodach poręczycieli i zgoda męża – przy umowie.

## Źródła faktów (sprawdzone 14.10.2026)

- Ogłoszenie naboru PUP Turek 12–16.10.2026: <https://turek.praca.gov.pl/strona-glowna/-/asset_publisher/Qat7ebECUfDp/content/dofinansowanie-na-podjecie-dzialalnosci-gospodarczej?p_r_p_assetEntryId=69659875>
- Informacja PUP Turek 2026 (kryteria, wykluczenia, zabezpieczenia): <https://turek.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-turku/informacja-aktualna>
- Wzór wniosku PUP Turek: <https://turek.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-turku/wniosek-propozycja>
- Liczba ludności powiatu tureckiego i struktura wieku (GUS BDL w Strategii rozwiązywania problemów społecznych powiatu 2026–2036): <https://powiat.turek.pl/media/att/psrps_powiatu_tureckiego_na_lata_2026_2036_wer_4_06_10.pdf>
- Turek: 24 315 mieszkańców, 24,4% w wieku 65+ (GUS, 31.12.2024, za polskawliczbach.pl): <https://www.polskawliczbach.pl/Turek>
- Konkurenci i ceny (Booksy – listingi salonów w Turku i okolicy, m.in. Fryzjer dla Ciebie, Majewski Hair, NEW LOOK, GOLD ANGEL): <https://booksy.com/pl-pl/s/fryzjer/17163_brudzew>, <https://booksy.com/pl-pl/s/konsultacja-fryzjerska/17159_malanow>
- Średnie ceny fryzjerskie w Turku (kb.pl, 29.04.2026): <https://kb.pl/cenniki/miejskie/fryzjer/turek/>
- Położenie wsi Beznazwa (gm. Władysławów): <https://en.wikipedia.org/wiki/Beznazwa>
- PKD 2025 (Dz.U. 2024 poz. 1936): <https://api.sejm.gov.pl/eli/acts/DU/2024/1936/text.pdf>
- Osiedla Wyzwolenia i Spółdzielców w Turku (ogłoszenia mieszkań): <https://adresowo.pl/mieszkania/turek-A/os-wyzwolenia-P/>
