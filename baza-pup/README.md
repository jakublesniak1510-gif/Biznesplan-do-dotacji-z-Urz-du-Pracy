# Baza regulaminów PUP 2026

Baza zasad przyznawania dofinansowania podjęcia działalności gospodarczej w **30 powiatowych urzędach pracy** (16 miast wojewódzkich, 6 urzędów opisanych w `docs/jak-dziala-dotacja-2026.md` i 8 urzędów z różnych województw i różnej wielkości). Stan na **14.10.2026**.

To jest nasza przewaga: konkurencja (Firmove, Biznesplany24, WROSKO) pisze jeden ogólny biznesplan. My wiemy, **jak dany urząd liczy punkty, czego zakazuje i ile miejsca ma w formularzu**.

## Zawartość katalogu

| Plik / katalog | Co zawiera |
|---|---|
| `SCHEMAT.md` | Definicje 36 kolumn CSV (obowiązujące) |
| `regulaminy-pup-2026.csv` | 30 wierszy, UTF-8, separator `;`, listy rozdzielone ` \| ` |
| `formularze/` | 25 formularzy wniosków `[pup_id]-wniosek-2026.pdf\|docx`. Pliki `.doc` przekonwertowano do `.docx`. Piotrków Tryb. pominięty (PDF 12,8 MB > 5 MB, link w CSV) |
| `pola-formularzy/` | Pola opisowe 8 formularzy z 8 województw + `WSPOLNE-SEKCJE.md` (porównanie i mapowanie na `szablony/01–09`) |
| `kalendarz-naborow-2026.md` | 150 naborów 2026 (Zielona Linia + strony PUP) z rozkładem po miesiącach |

## Jak korzystać

1. **Przy przyjęciu zlecenia** sprawdzamy, czy urząd klienta (właściwy dla **miejsca zamieszkania**) jest w CSV (`pup_id`). Jeśli go nie ma, robimy dla niego wiersz według procedury z punktu „Aktualizacja” i dopisujemy do bazy.
2. **Przed kwestionariuszem** czytamy kolumny `wykluczenia_dzialalnosci`, `limit_*`, `sprzet_uzywany`, `wklad_wlasny`, `zabezpieczenia`, `dochod_poreczyciela_min_zl`. Od tego zależy, czy pomysł klienta w ogóle przejdzie (np. handel w Zambrowie, mobilny fryzjer w Białymstoku, samochód w Opolu) i czy klient ma realne zabezpieczenie.
3. **Przy pisaniu treści** bierzemy kolumnę `kryteria_punktowane` (co punktuje komisja) i plik `pola-formularzy/[pup_id]-pola.md` (jakie są pola i ile miejsca). Szablon `szablony/10-mapowanie-pol-formularza.md` rozpisuje treść na pola.
4. **Przy przygotowaniu klienta** sprawdzamy `komisja_rozmowa` i `wizja_lokalna`. Gdy jest „tak” albo „przy wątpliwościach”, dodajemy ściągawkę na rozmowę (SWOT, ryzyka). Gdy wizja jest „możliwa/tak”, lokal musi istnieć i wyglądać jak w opisie.
5. **Kalendarz** służy do alertów i do rozmów sprzedażowych („w Pana urzędzie nabory były w marcu i wrześniu, okno 2–3 dni”).

Zasada nadrzędna, jak w całej bazie: **puste pole = nie ustalono w źródle. Nie zgadujemy.** Zanim podamy klientowi konkretną wartość, sprawdzamy ją w linku z kolumny `zrodla`, bo regulaminy zmieniają się w ciągu roku (Poznań: 2 aneksy, Warszawa: wersja z 10.09.2026).

### Jak czytać niektóre kolumny

- `komisja_rozmowa`: **tak** = obowiązkowa prezentacja albo wezwanie każdego wnioskodawcy, także gdy rozmowa wchodzi do punktacji albo wnioskodawca ma prawo udziału (Nowa Sól, Kielce, Tychy, Legnica). **przy wątpliwościach** = komisja „może zaprosić” lub „w razie potrzeby”. Puste = regulamin o rozmowie milczy.
- `limit_*_pct`: tylko limity **procentowe**. Limity kwotowe (np. reklama do 2 000 zł) są w `uwagi`. `0` = wprost zakazane.
- `liczba_poreczycieli` / `dochod_poreczyciela_min_zl`: wariant podstawowy (zwykle poręczenie cywilne). Brutto czy netto, wyjątki i warianty z avalem opisano w `uwagi`.
- `kwota_max_zl`: maksimum z ostatniego naboru albo z zasad 2026. Gdy urząd pisze tylko „do 6-krotności przeciętnego wynagrodzenia”, pole jest puste, a informacja trafia do `uwagi`.

## Kompletność danych

- **Kompletne (19):** regulamin lub zasady 2026 przeczytane, znany ostatni nabór, co najmniej 24 z 36 kolumn wypełnione: Nowa Sól, Kolbuszowa, Turek, Mińsk Maz., Warszawa, Łódź, Poznań, Szczecin, Bydgoszcz, Olsztyn, Opole, Rzeszów, Zielona Góra, Lublin, Tychy, Kędzierzyn-Koźle, Gorlice, Zambrów, Piotrków Tryb.
- **Częściowe (11):** Grodzisk Maz. i Kraków (regulamin jest, brak ogłoszenia naboru 2026), Gdańsk (konkurs rozstrzygnięty, brak dat naboru), Białystok (regulamin z 22.06.2026, brak naboru dla bezrobotnych), Kielce/MUP (zasady są, brak naboru i kwoty), Słupsk (zasady są, komunikat ZL bez dat, brak formularza na stronie), Legnica (regulamin bez punktacji i bez dochodu poręczyciela – jest w osobnym zarządzeniu), Wrocław i Bartoszyce (brak regulaminu, zasady odtworzone z formularza i ogłoszenia), Katowice i Brodnica (tylko ogłoszenia naboru).

### Urzędy, dla których nie znaleziono regulaminu 2026

| Urząd | Co znaleziono zamiast regulaminu | Co zrobić |
|---|---|---|
| PUP Katowice | Harmonogram naborów 2026 (4.03, 15.06) i ogłoszenia w ZL. Na stronie brak zasad i formularza dotacji | Telefon do urzędu albo pismo o udostępnienie zasad (informacja publiczna) |
| PUP Brodnica | Ogłoszenie naboru 1–2.07.2026 (FP, 32 000 zł) | Jw. |
| PUP we Wrocławiu | Ulotka „Dotacja krok po kroku 2026” i formularz z zasadami (limity 20%/30%, tylko nowe rzeczy) | Formularz wystarcza do pisania treści. O kartę oceny trzeba zapytać |
| PUP Bartoszyce | Formularz na nabór 1–9.04.2026 zawiera wyłączenia i zasady zabezpieczeń | Jw. |

Uwaga techniczna: **Opole** opublikowało regulamin jako skan bez warstwy tekstowej. Odczytano go wizualnie (11 stron) i dane są w bazie. **Mińsk Maz.**: plik „Zasady rozpatrywania wniosków 2026” to skan, którego nie odczytano (główne Zasady 2026 są tekstowe i przeczytane).

## Statystyki (30 urzędów)

**Rozmowa z komisją:** 4 urzędy „tak” (Nowa Sól – obowiązkowa prezentacja, nieobecność = odmowa; Kielce – wezwanie każdego; Tychy – rozmowa w punktacji; Legnica – prawo udziału), 7 „przy wątpliwościach” (Mińsk Maz., Gdańsk, Szczecin, Bydgoszcz, Rzeszów, Kędzierzyn-Koźle, Słupsk), 19 bez zapisu. **Wizja lokalna** przewidziana w 14 urzędach (2 „tak”: Grodzisk Maz., Poznań; 12 „możliwa”).

**Kwota maksymalna** (15 urzędów z kwotą w zł): **mediana 35 000 zł**, średnia ok. 37 800 zł, rozpiętość 30 000 zł (Gdańsk, Bydgoszcz, Lublin) – 57 377 zł (Rzeszów, projekt EFS+ 18–29). W kalendarzu kwoty z ogłoszeń wynoszą 23 000 zł (Lubliniec) – 52 600 zł (Bartoszyce). Pozostałe urzędy podają „do 6-krotności przeciętnego wynagrodzenia” albo nie podają kwoty.

**Źródła finansowania ostatnich naborów:** FP + EFS+ równolegle 15, tylko EFS+ 6, tylko FP 4, brak danych 5. **Tryb:** terminowy 24, do wyczerpania 4.

**Rozkład limitów procentowych** (liczba urzędów; „—” = brak limitu procentowego w źródle):

| Pozycja | 0% (zakaz) | 5% | 10% | 15% | 20% | 30% | 40% | 50% | — |
|---|---|---|---|---|---|---|---|---|---|
| Reklama | 1 (Olsztyn) | 2 (Opole, Rzeszów) | 5 | 1 (Grodzisk) | 2 (Poznań, Białystok) | 1 (Warszawa) | – | – | 18 |
| Towar / materiały | 2 (Kielce, Słupsk) | – | – | – | 4 | 7 | – | 3 (Warszawa, Poznań, Gorlice) | 14 |
| Remont / adaptacja | 8 | – | 3 | – | 4 | 2 (Wrocław, Poznań) | – | – | 13 |
| Samochód | 5 (Warszawa, Opole, K-Koźle, Gorlice, Słupsk) | – | – | – | 1 (Zambrów) | 1 (Zielona Góra) | 2 (Lublin, Piotrków) | 4 | 17 |

(Wiele urzędów ogranicza wydatki **kwotowo**: reklama do 1 500–10 000 zł, telefon do 1 000–4 000 zł, komputer do 4 000–8 000 zł, towar do 4 000–25 000 zł – szczegóły w `uwagi`).

**Najczęstsze wykluczenia** (22 urzędy z listą wykluczeń):

| Wykluczenie | Liczba urzędów |
|---|---|
| Zakupy od rodziny / działalność tożsama z rodziną / przejęcie od rodziny | 17 |
| Działalność sezonowa | 12 |
| Przejęcie istniejącej działalności | 9 |
| Wynajem, wypożyczalnie | 9 |
| Handel obwoźny, obnośny, targowiska | 8 |
| Rolnictwo | 8 |
| Spółki (tylko JDG) | 8 |
| Usługi medyczne, paramedyczne, kosmetologia, tatuaż bez kwalifikacji | 8 |
| Lombard, komis, kantor, pożyczki | 8 |
| Akwizycja, ajencja, MLM | 6 |
| Siedziba poza miastem/powiatem | 6 |
| Alkohol i tytoń | 6 |
| Hazard, agencje towarzyskie | 6 |
| Wróżbiarstwo, ezoteryka | 6 |
| Franczyza | 5 |
| Dropshipping / sprzedaż tylko internetowa | 5 |

**Zabezpieczenia** (28 urzędów z danymi): poręczenie 27, blokada rachunku 26, weksel z poręczeniem (aval) 23, gwarancja bankowa 23, weksel in blanco 20, akt notarialny 19, zastaw 18. Kilka urzędów **zawęża** katalog: Białystok – tylko aval albo gwarancja; Gdańsk i Opole – poręczenie albo blokada. **Liczba poręczycieli:** 2 w 20 urzędach, 1 w 5. **Minimalny dochód poręczyciela** (18 urzędów): mediana ok. 5 050 zł, rozpiętość 3 900 zł netto (Bartoszyce) – 7 000 zł brutto (Warszawa). Część urzędów liczy brutto, część netto po odjęciu rat.

**Wkład własny:** wymagany w 2 urzędach (Gorlice min. 25%, Zambrów min. 10%), punktowany w 8 (Nowa Sól, Kolbuszowa, Turek, Poznań, Gdańsk, Olsztyn, Zielona Góra, Lublin), brak zapisu w 20.

**Karty oceny** (15 urzędów z punktacją): od 8 pkt (Poznań, próg 6) do 100 pkt (Tychy, próg 60). Typowo 20–40 pkt z progiem ok. 50–65% maksimum. **Okres prowadzenia:** 12 mies. wszędzie poza Piotrkowem Tryb. (15 mies.).

## 10 najciekawszych różnic między urzędami

1. **Zabezpieczenie na podwójną kwotę** – Zielona Góra wymaga, by każda forma zabezpieczenia opiewała na **200%** dotacji ([zasady](https://zielonagora.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-zielonej-gorze/zasady-przyznawania-dofinansowania-na-podjecie-dzialalnosci-gospodarczej-przez-bezrobotnego)). Gdańsk przyjmuje blokadę 120% ([regulamin](https://gdansk.praca.gov.pl/documents/2125750/59739378/Regulamin+przyznawania+jednorazowych+%C5%9Brodk%C3%B3w+na+rozpocz%C4%99cie+dzia%C5%82alno%C5%9Bci+gospodarczej.doc/69e5fa3c-dd17-2c8d-33f6-4e561940a796?t=1772012496970)), Kolbuszowa 125%.
2. **Wkład własny obowiązkowy** – Gorlice: co najmniej **25%** kwoty ([kryteria 2026](https://gorlice.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-gorlicach/kryteria-i-preferencje-dofinansowania-podjecia-dzialalnosci-gospodarczej-w-2026-roku)), Zambrów 10% ([kryteria](https://zambrow.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-zambrowie/kryteria-przyznawania-srodkow-na-podjecie-dzialalnosci-gospodarczej-2026-4-docx)). W większości urzędów wkład jest tylko punktowany albo nieistotny.
3. **Skala punktacji od 8 do 100 pkt** – Poznań ocenia wniosek na **8 pkt** (próg 6, a 0 pkt za lokal po wizytacji odrzuca wniosek; [karta](https://poznan.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-poznaniu/00-karta-oceny-ostateczna)). Tychy mają 13 kryteriów po 0–15 pkt, maks. **100**, próg 60, a **rozmowa z komisją wchodzi do punktów** ([regulamin](https://tychy.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-tychach/regulamin-dyrektora-pup-tychy-2026)).
4. **Towar: od zakazu do 50%** – Kielce/MUP i Słupsk **w ogóle nie finansują towarów i materiałów** (Słupsk nawet do produkcji) ([Kielce](https://mupkielce.praca.gov.pl/documents/d/miejski-urzad-pracy-w-kielcach/zasady-przyznawania-dofinansowania-podjecia-dzialalnosci-gospodarczej-obowiazujace-w-miejskim-urzedzie-pracy-w-kielcach-w-2026-r-1), [Słupsk](https://slupsk.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-slupsku/zasady-przyznawania-jednorazowo-srodkow-na-podjecie-dzialalnosci-gospodarczej)). Warszawa, Poznań i Gorlice pozwalają na 50%. Sklep z dotacji ma sens tylko w części urzędów.
5. **Reklama: od zakazu do 30%** – Olsztyn/MUP wyklucza koszty reklamy firmy ([regulamin](https://mupolsztyn.praca.gov.pl/documents/d/miejski-urzad-pracy-w-olsztynie/regulamin-dotacje-mup-od-01-01-26-docx)), Tychy dają 1 500 zł, a Warszawa do **30%** ([zasady 10.09.2026](https://warszawa.praca.gov.pl/documents/8188477/69156016/Zasady+10.09.2026.docx/cee64284-e9d5-ecbf-e59a-a75d28b2f4ad?t=1789550866060)).
6. **Pojazdy** – Opole zakazuje **wszystkich** pojazdów (także roweru) i telefonu komórkowego ([regulamin, skan](https://opole.praca.gov.pl/documents/1938491/68446221/REGULAMIN+PRZYZNAWANIA+JEDNORAZOWO+%C5%9ARODK%C3%93W+NA+PODJ%C4%98CIE+DZIA%C5%81ALNO%C5%9ACI+GOSPODARCZEJ.pdf/8ad2a7e9-5d56-873d-6af9-ddcd9dea879e?t=1787727303616)). Warszawa wyklucza też taxi i przewóz osób jako działalność. Kolbuszowa i Gdańsk dopuszczają samochód do 50% kwoty, Lublin dla taxi nawet do 75%.
7. **Białystok – najdłuższa lista wykluczeń** (27 pozycji), w tym **mobilne usługi fryzjerskie, kosmetyczne i mechaniczne**, działalność koncesjonowana i ta sama branża co własna firma w ostatnich 5 latach ([regulamin 22.06.2026](https://bialystok.praca.gov.pl/documents/1938834/57616930/Regulamin+przyznawania+%C5%9Brodk%C3%B3w+na+podj%C4%99cie+dzia%C5%82alno%C5%9Bci+gospodarczej+2026+r..pdf/f6d9e895-408f-8346-0f8e-901ebaa8f3a0?t=1782716410384)). Zambrów wyklucza **całą działalność handlową**.
8. **Taxi i Uber odwrotnie** – Poznań finansuje taxi tylko przy współpracy z korporacją albo aplikacją typu Uber/Bolt ([zasady](https://poznan.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-poznaniu/zasady-2026-wersja-ostateczna)), a Bartoszyce **wykluczają przewóz osób na żądanie (PKD 49.33.Z)** oraz sprzedaż wyłącznie internetową ([formularz z warunkami](https://bartoszyce.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-bartoszycach/wniosek-o-przyznanie-bezrobotnemu-jednorazowo-srodkow-na-podjecie-dzialalnosci-gospodarczej-2026-nabor-od-dnia-01-04-2026-r-do-dnia-09-04-2026-r-)).
9. **Sprawdzanie długów** – Słupsk **odmawia** przy wpisie w Krajowym Rejestrze Długów, Warszawa każe podpisać upoważnienie do KRD, Turek wyklucza zadłużonych wobec urzędu, a Szczecin wymaga ugody z komornikiem pod rygorem odrzucenia ([kryteria Szczecin](https://szczecin.praca.gov.pl/documents/4284075/4480676/Kryteria+przyznawania+przez+Powiatowy+Urz%C4%85d+Pracy+w+Szczecinie+dofinansowania++podj%C4%99cia+dzia%C5%82alno%C5%9Bci+gospodarczej.pdf/a1e3a12a-a744-8ca4-b24e-870b92c4462c?t=1772444335155)). Kwestionariusz musi pytać o zadłużenia.
10. **Punkty za rzeczy, na które klient nie ma wpływu przy pisaniu** – Szczecin daje do 3 pkt za **długość rejestracji w PUP** i do 5 pkt za **formę zabezpieczenia** (blokada albo poręczenie + akt = 5, reszta = 1). Lublin daje do 3 pkt za **zatrudnienie pracownika w 6 miesięcy** ([regulamin](https://lublin.praca.gov.pl/documents/1790672/47575322/Regulamin+przyznawania+%C5%9Brodk%C3%B3w+na+podj%C4%99cie+dzia%C5%82alno%C5%9Bci++gospodarczej+w+PUP++w++Lublinie+-+obowi%C4%85zuj%C4%85cy+od+26.02.2026.doc/eb61b82e-5910-ebfd-e4b8-bcebb12827e0?t=1771854904648)), Nowa Sól punktuje udział w spotkaniach PUP. To porady strategiczne dla klienta, nie tylko treść wniosku.

Inne warte uwagi: Piotrków Tryb. – **15 miesięcy** prowadzenia firmy ([zasady 2026](https://piotrkowtrybunalski.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-piotrkowie-trybunalskim/2026-zasady-przyznawania-jednorazowo-srodkow-na-podjecie-dzialalnosci-gospodarczej)). Warszawa – wniosek **Arial 12, interlinia 1,3** i sekcja ekologiczna DNSH. Bartoszyce – 3 900 zł netto dochodu poręczyciela „zabezpiecza” 17 000 zł dotacji (przy 52 600 zł potrzeba łącznie ok. 12 tys. zł dochodów poręczycieli). Łódź otwiera nabory o 8:30 i wstrzymuje je po kilku dniach (4 fale w 2026). Wrocław opublikował ogłoszenie naboru jako obraz JPG.

## Procedura aktualizacji (co miesiąc, ok. 2–3 h)

1. **Nowe nabory (co tydzień lub co miesiąc):** pobrać posty z Zielonej Linii przez API:
   `https://zielonalinia.gov.pl/wp-json/wp/v2/posts?per_page=100&search=dzia%C5%82alno%C5%9Bci%20gospodarczej&after=RRRR-MM-DDT00:00:00&_fields=date,link,title,content`
   (także `search=dotacj` i `search=jednorazowo środków`). Dopisać nabory do `kalendarz-naborow-2026.md`. Dla urzędów z bazy zaktualizować `nabor_ostatni_od/do`, `kwota_max_zl`, `liczba_miejsc`, `zrodlo_finansowania`.
2. **Zmiany regulaminów (co miesiąc, dla 30 urzędów):** na stronie `https://[pup].praca.gov.pl` sprawdzić: „Dokumenty do pobrania”, „Nabory wniosków”, „Dla bezrobotnych → Formy wsparcia → Dofinansowanie podjęcia działalności”. Sygnały zmiany: nowa nazwa pliku (np. „Zasady 10.09.2026”), parametr `?t=` w linku `/documents/…`, słowo „aneks”, nowy numer zarządzenia. Przy zmianie pobrać plik, przeczytać i poprawić wiersz. W `uwagi` dopisać datę zmiany, w `zweryfikowano` wpisać dzisiejszą datę.
3. **Formularze:** porównać nowy formularz z `formularze/[pup_id]-wniosek-2026.*` (rozmiar, data). Przy zmianie podmienić plik i zaktualizować `pola-formularzy/[pup_id]-pola.md`, jeśli istnieje.
4. **Limit ustawowy:** po komunikacie GUS o przeciętnym wynagrodzeniu (ok. 10.11, 10.02, 10.05, 10.08) zaktualizować kwotę 6× w docs. Urzędy z „do 6-krotności” w `uwagi` automatycznie zmieniają maksimum.
5. **Urzędy częściowe** (lista wyżej): co miesiąc ponawiać szukanie regulaminu. Jeśli w ciągu kwartału nic się nie pojawi, wysłać e-mail z prośbą o zasady (dostęp do informacji publicznej).
6. **Walidacja po każdej zmianie:** wczytać CSV w Pythonie (`csv`, `delimiter=';'`) i sprawdzić 36 kolumn w każdym wierszu, liczby w kolumnach kwot i punktów, procenty 0–100, daty `RRRR-MM-DD`, linki `https://`.
7. **Nowy urząd z zamówienia:** sprawdzić subdomenę (`[nazwa].praca.gov.pl`, wyjątki: `gupkrakow`, `mupkielce`, `mupolsztyn`, `kedzierzyn-kozle`), przejść sekcje z pkt 2, wypełnić wiersz według `SCHEMAT.md`, pobrać formularz, sporządzić `[pup_id]-pola.md`.
