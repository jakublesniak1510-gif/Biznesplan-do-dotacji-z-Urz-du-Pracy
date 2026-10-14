# Przykłady wzorcowe – wnioski o dofinansowanie z PUP

Stan: 14.10.2026. Trzy kompletne wnioski napisane ręcznie tak, jak ma je pisać model według `szablony/00`–`09`, oraz materiały dla klienta. Służą jako:
1. **few-shot** – wzorce stylu i struktury w wywołaniach modelu (zasady niżej),
2. **kalibracja operatora** – jak wygląda „gotowe” po przejściu `docs/checklista-weryfikacji.md`,
3. **materiał pokazowy dla klientów** – co dostają w pakiecie.

> We wszystkich przykładach **osoby, ich rodziny, pracodawcy, poręczyciele i podmioty z listów intencyjnych są fikcyjne** (oznaczone w każdym pliku). Prawdziwe są: urzędy, ich regulaminy, wzory wniosków i karty oceny, miejscowości i ulice, konkurenci (nazwy i adresy z Booksy, autocentrum.pl, oferteo.pl), ceny rynkowe (kb.pl, sklepy), dane GUS i kody PKD 2025. Źródła z linkami – w każdym `raport-kontroli.md`.

## Co tu jest

| Katalog / plik | Zawartość |
|---|---|
| `01-fryzjerka-mobilna-turek/` | PUP Turek, nabór 12–16.10.2026 (rezerwa FP, program dla zwolnionych z przyczyn niedotyczących pracowników), ton **ciepły**, praca mobilna, bez lokalu |
| `02-mechanik-grodzisk-mazowiecki/` | PUP Grodzisk Mazowiecki, regulamin z 22.04.2026 (nabór do ogłoszenia), ton **techniczny**, wynajem hali, decyzje o lawecie i sprzęcie używanym |
| `03-firma-sprzatajaca-kolbuszowa/` | PUP Kolbuszowa, projekt EFS+ (FE dla Podkarpacia), kobieta 57 lat, ton **rzeczowy**, listy intencyjne od wspólnoty i firm |
| w każdym z nich: `kwestionariusz.md` | kwestionariusz wypełniony „jak klient” (potocznie, z brakami) + notatki właściciela i uzupełnienia z telefonu |
| `wniosek.md` | sekcje 01–09 (wariant standard, ~1700–2300 znaków) ułożone w kolejności pól formularza urzędu; na górze tabela „pole formularza → sekcja”; tabele liczbowe z arkusza |
| `kosztorys-i-prognoza.md` | specyfikacja wydatków z linkami do ofert typu, limity regulaminu, przychody, koszty, 12 miesięcy (miesięcznie i kwartalnie), wskaźniki, próg rentowności, scenariusz −30%, kontrole arkusza – **generowany z `model.xlsx`** |
| `model.xlsx` | kopia `model-finansowy/model-finansowy-pup.xlsx` z danymi klienta, przeliczona przez LibreOffice; 1 929 formuł, 0 błędów |
| `raport-kontroli.md` | przejście checklisty A–I, karta oceny urzędu → sekcje, pola → znaki, liczby → komórki arkusza, wynik testu zakazanych zwrotów, lista „do zrobienia przed złożeniem”, źródła |
| `wniosek.docx` | strona tytułowa z instrukcją „co wpisać samemu”, sekcje z nazwami pól urzędu, tabele (nagłówki powtarzane na stronach) |
| `materialy-klienta/` | wzór listu intencyjnego (`.md` + `.docx`), co po przyznaniu (krok po kroku, checklista, kalendarz), 3 wzory odpowiedzi na wezwanie, co wpisać samemu (z objaśnieniem oświadczeń), 20 pytań komisji z przykładowymi odpowiedziami |
| `narzedzia/` | `zbuduj_modele.py` (dane → `model.xlsx` + przeliczenie), `kosztorys_md.py` (arkusz → `kosztorys-i-prognoza.md`), `wniosek_docx.py` (`wniosek.md` → `wniosek.docx`), `md_docx.py` (dowolny `.md` → `.docx`), `sprawdz.py` + `zakazane.txt` (długości, zakazane zwroty, liczby spoza arkusza), `notatki/` (komentarze do kosztorysów i stron tytułowych docx), `dozwolone/` (liczby z kwestionariuszy i źródeł, które mogą wystąpić w tekście) |

### Wyniki z arkuszy

| | Turek – fryzjerka | Grodzisk Maz. – mechanik | Kolbuszowa – sprzątanie |
|---|---|---|---|
| Dotacja / wkład (zakupy) | 15 000,00 / 2 054,10 zł | 39 400,00 / 2 337,00 zł | 24 850,00 / 5 350,50 zł (17,7%) |
| Przychody 12 mies. | 80 895 zł | 181 960 zł | 83 080 zł |
| Zysk netto 12 mies. (średnio / mies.) | 41 625 zł (3 469 zł) | 70 436 zł (5 870 zł) | 50 297 zł (4 191 zł) |
| Próg rentowności | 2 299 zł/mies. (32 usługi) | 6 593 zł/mies. (48 zleceń) | 1 830 zł/mies. (19 zleceń) |
| Próg po ulgach ZUS | 4 187 zł | 8 889 zł | 3 656 zł |
| Wariant −30%: zysk netto (mies.) | 22 801 zł (1 900 zł) | 37 281 zł (3 107 zł) | 29 871 zł (2 489 zł) |
| Najniższe saldo gotówki | 1 946 zł | 5 446 zł (−30%: 4 188 zł) | 2 650 zł |

## Jak używać jako few-shot

**Zasada z `szablony/00-system-prompt.md`:** przykładów nie wysyłamy do modelu przy kliencie **z tej samej branży** – model kopiowałby fakty i zdania. Wysyłamy przykład **z innej branży, w tonie zamówionym dla klienta**, jako wzór stylu, nie treści.

### Który fragment do którego szablonu

| Szablon | Ton klienta → fragment do wklejenia | Uwagi |
|---|---|---|
| `01-opis-dzialalnosci.md` | ciepły → `01-…/wniosek.md` § 01; techniczny → `02-…` § 01 (pola II.1–II.4b); rzeczowy → `03-…` § 01 | przykład 02 pokazuje podział jednego tematu na kilka pól formularza |
| `02-kwalifikacje-i-doswiadczenie.md` | ciepły → `01` § 02 (a–c, pole rozbite na 3); techniczny → `02` § 02; rzeczowy → `03` § 02 | wszystkie trzy pokazują uczciwe luki (brak czeladnika, F-gazów, kursów) i znacznik `[BRAK DANYCH]` |
| `03-analiza-rynku-i-klientow.md` | ciepły → `01` § 03; techniczny → `02` § 03; rzeczowy → `03` § 03 | dane GUS ze źródłem, dowody popytu z liczbami, sezonowość |
| `04-analiza-konkurencji.md` | ciepły → `01` § 04; techniczny → `02` § 04; rzeczowy → `03` § 04 | słabe strony konkurentów tylko z faktów (cennik, brak usługi), przyznanie przewagi konkurenta |
| `05-plan-marketingowy.md` | ciepły → `01` § 05; techniczny → `02` § 05; rzeczowy → `03` § 05 | kanał przypisany do grupy klientów, budżet = kosztorys |
| `06-uzasadnienie-zakupow.md` | opisowy: dowolny § 06; pozycyjny: tabele „Tabela 2” (Turek), „IV.3” (Grodzisk) | przykład 02 – odrzucenie lawety i sprzętu używanego; przykład 03 – limit kwotowy reklamy i wpływ na zrównoważony rozwój (EFS+) |
| `07-analiza-swot.md` | dowolny § 07 w tonie klienta | działania zaradcze w nawiasach, czynniki wewnętrzne/zewnętrzne rozdzielone |
| `08-prognoza-finansowa-opis.md` | dowolny § 08 | **w few-shot podmień liczby na zmienne `{{ark_…}}`** – model nie może widzieć liczb gotowych do skopiowania |
| `09-ryzyka-i-plan-b.md` | tabela → `01` § 09 lub `03` § 09; lista numerowana → `02` § 09 | plan B tylko z kwestionariusza; obowiązki z umowy |
| `10-mapowanie-pol-formularza.md` | tabele „Mapa: pole formularza → sekcja” z trzech wniosków | trzy różne formularze: Turek (załączniki 1–2 + tabele), Grodzisk (II.1–II.4e + Zał. 2), Kolbuszowa (pola EFS+, brak SWOT) |
| `11-przygotowanie-do-uzupelnien.md` | A: `materialy-klienta/odpowiedz-na-wezwanie-wzor.md`; B: `materialy-klienta/pytania-komisji-20.md` | |

### Jak wkleić

W `<szablon_sekcji>` po sekcji „Prompt sekcji” dodaj blok (fragment z `wniosek.md` bez nagłówka i bez linii „*Pole…*”):

```text
PRZYKŁAD STYLU (inna branża, inny klient – NIE kopiuj faktów, liczb ani zdań;
pokazuje ton „{{ton}}”, długość i sposób użycia konkretów):
<przyklad>
[fragment sekcji z przykładu w tym samym tonie]
</przyklad>
```

- Jeden przykład na wywołanie. Dwa lub więcej – model zaczyna uśredniać i powtarzać frazy.
- W sekcji 08 i 06 zastąp kwoty zmiennymi (`{{ark_zysk_netto_12m}}` itd.) albo usuń liczby.
- Po wygenerowaniu uruchom test bliźniaka z checklisty (F): żadne zdanie dłuższe niż 8 słów nie może powtarzać przykładu.

## Jak zrobić nowy przykład

1. **Urząd i dokumenty:** pobierz z `<urząd>.praca.gov.pl` → Dokumenty do pobrania: regulamin/informację, wzór wniosku, kartę oceny (kryteria), ogłoszenie naboru. Zapisz limity (towar, reklama, sprzęt używany, samochód), wykluczenia, wymogi zabezpieczenia. Sprawdź, czy dokument nie dotyczy innego naboru (np. PFRON).
2. **Kwestionariusz:** wypełnij `kwestionariusz.md` według `docs/kwestionariusz-klienta.md` głosem klienta, z realnymi brakami. Braki uzupełniaj w bloku „Uzupełnienia z rozmowy telefonicznej” – **żadnego faktu we wniosku bez źródła w kwestionariuszu**.
3. **Fakty lokalne:** zweryfikuj w sieci miejscowości, ulice, osiedla, konkurentów (nazwa, adres, cennik, ocena), ceny rynkowe (kb.pl), dane GUS (BDL lub polskawliczbach.pl). Słabe strony konkurentów – tylko z publicznych faktów.
4. **Model:** dopisz przykład do słownika `EXAMPLES` w `narzedzia/zbuduj_modele.py` (założenia, pozycje kosztorysu z linkami, limity, usługi, sezonowość, rozruch, koszty stałe) i uruchom:
   ```bash
   python3 przyklady/narzedzia/zbuduj_modele.py <słowo-z-nazwy-katalogu>
   ```
   Sprawdź kontrole (dotacja rozplanowana, limity OK, saldo ≥ 0, obłożenie < 100%, VAT).
5. **Kosztorys:** napisz `narzedzia/notatki/<katalog>.md` (bloki `@@ naglowek`, `kosztorys_intro`, `limity`, `przychody`, `koszty`, `pesymistyczny`, `uproszczenia`, `docx_tytul`, `docx_samemu`) i wygeneruj:
   ```bash
   python3 przyklady/narzedzia/kosztorys_md.py przyklady/<katalog>
   ```
6. **Wniosek:** napisz `wniosek.md` w kolejności pól formularza: tabela mapowania, pola krótkie, sekcje `## 01.`–`## 09.` (każda z linią `*Pole: „…”*`), tabele liczbowe z arkusza. Liczby przepisuj z `kosztorys-i-prognoza.md`.
7. **Kontrola:** dopisz liczby z kwestionariusza do `narzedzia/dozwolone/<katalog>.txt` i uruchom:
   ```bash
   python3 przyklady/narzedzia/sprawdz.py przyklady/<katalog>
   ```
   Cel: każda sekcja 1700–2300 znaków, 0 zakazanych zwrotów, 0 nieznanych liczb.
8. **DOCX:** `python3 przyklady/narzedzia/wniosek_docx.py przyklady/<katalog>`; obejrzyj po konwersji do PDF (`soffice --headless --convert-to pdf`).
9. **Raport:** `raport-kontroli.md` według wzoru – checklista A–I, karta oceny, wynik `sprawdz.py`, źródła.

## Cechy dobrego wniosku a typowe błędy z odrzuconych wniosków

Źródła powodów odrzuceń i uwag komisji: poradniki branżowe, regulaminy urzędów (zapisy o obniżaniu kwot i odmowach) i dane z naborów. Na forach nie znalazłem w tej sesji wątków z cytatami uzasadnień odmów – nie podaję ich.

| Cecha dobrego wniosku (w przykładach) | Typowy błąd | Źródło błędu / uwagi komisji |
|---|---|---|
| Aktualny wzór wniosku z naboru, układ pól nienaruszony, puste rubryki z wpisem „nie dotyczy” | stary wzór formularza, zmieniona kolejność pól, puste rubryki | [infakt.pl, 15 błędów (29.06.2026)](https://www.infakt.pl/blog/?p=83318) – pkt 1, 4, 15; [Zielona Linia](https://zielonalinia.gov.pl/srodki-na-dzialalnosc-gospodarcza-z-urzedu-pracy-na-co-zwrocic-uwage/); regulamin Grodziska Maz. § 5 ust. 2 (zakaz zmiany treści i kolejności); Informacja PUP Turek („bez zmian szaty graficznej”, „nie dotyczy”) |
| Kwota = suma specyfikacji co do grosza, w każdym miejscu wniosku | kwota we wniosku inna niż suma specyfikacji; kwota ponad limit naboru | [infakt.pl](https://www.infakt.pl/blog/?p=83318) – pkt 6–7; [Zielona Linia](https://zielonalinia.gov.pl/srodki-na-dzialalnosc-gospodarcza-z-urzedu-pracy-na-co-zwrocic-uwage/) – „przekroczenie limitu kwoty” |
| Każdy zakup powiązany z konkretną usługą, cena z oferty, świadome skreślenia (druga suszarka, laweta) | zakupy „na zapas”, ceny zawyżone, wydatki niezwiązane z profilem | [Informacja PUP Turek 2026](https://turek.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-turku/informacja-aktualna), cz. IV pkt 2 – obniżenie kwoty przy koszcie „niezasadnym lub zawyżonym”; [regulamin Grodzisk Maz.](https://grodziskmazowiecki.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-grodzisku-mazowieckim/regulamin-w-sprawie-skladania-i-rozpatrywania-wnioskow-o-przyznanie-dofinansowania-podjecia-dzialalnosci-gospodarczej-kwiecien-2026) § 6 ust. 6 – ceny odbiegające od rynkowych, kwota zawyżona; [regulamin Nowa Sól](https://nowasol.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-nowej-soli/1-regulamin-dotacje-2026-1-pdf) § 3 ust. 9 – ograniczenie zakupów |
| Brak pozycji wykluczonych (kasa fiskalna, szkolenia, najem, transport zakupów) – przeniesione na wkład własny albo usunięte | wydatki spoza katalogu urzędu, koszty bieżące z dotacji | [infakt.pl](https://www.infakt.pl/blog/?p=83318) – pkt 14; [poradnikprzedsiebiorcy.pl](https://poradnikprzedsiebiorcy.pl/-na-co-zwrocic-uwage-wypelniajac-wniosek-o-dotacje-z-pup) – „z puli dotacji nie można finansować bieżącej działalności”; [zasady PUP Kolbuszowa](https://kolbuszowa.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-kolbuszowej/informacja-dotyczaca-zasad-udzielania-dofinansowania-2026) pkt 13 |
| Prognoza miesiąc po miesiącu: cena × liczba usług, rozruch, sezon, ZUS i zdrowotna, jedna forma opodatkowania, próg rentowności i wariant −30% | brak danych miesięcznych, kilka form opodatkowania naraz, przychody „z sufitu”, pominięty ZUS | [infakt.pl](https://www.infakt.pl/blog/?p=83318) – pkt 8; `szablony/08` (pominięcie ZUS jako najczęstszy powód obniżenia oceny) |
| PKD 2025 na poziomie podklasy, 1–2 kody spójne z opisem | kod z PKD 2007, kilkanaście kodów „na zapas” | [infakt.pl](https://www.infakt.pl/blog/?p=83318) – pkt 9; [Zielona Linia](https://zielonalinia.gov.pl/srodki-na-dzialalnosc-gospodarcza-z-urzedu-pracy-na-co-zwrocic-uwage/) – „błędny symbol PKD”; przykład 02 (klient podał 45.20.Z) |
| SWOT z prawdziwymi słabymi stronami i działaniem zaradczym przy każdej | SWOT powierzchowny, bez słabości i zagrożeń | [infakt.pl](https://www.infakt.pl/blog/?p=83318) – pkt 10; [Zielona Linia](https://zielonalinia.gov.pl/srodki-na-dzialalnosc-gospodarcza-z-urzedu-pracy-na-co-zwrocic-uwage/) – „niespójny biznesplan… mocne i słabe strony” |
| Spójność: te same liczby, nazwy ryzyk i zakupy w opisie, SWOT, tabelach | dokumenty, które ze sobą nie korespondują | [infakt.pl](https://www.infakt.pl/blog/?p=83318) – pkt 13; karta Turku „całościowość opisu… kompatybilność” (0–4 pkt) |
| Kwalifikacje opisane konkretnie i udokumentowane (lata, pracodawcy, kursy z rokiem), luki nazwane wprost | brak kwalifikacji do wybranej działalności albo kwalifikacje deklarowane bez dokumentów | [bankier.pl (2018)](https://www.bankier.pl/wiadomosc/Skresleni-przez-urzedy-pracy-Firmy-ktorym-nie-przyznano-dotacji-7610070.html) – PUP Poznań: negatywne oceny m.in. za „brak kwalifikacji do prowadzenia wybranego rodzaju działalności”; karty Turku (0–5 + 0–5) i Mińska (30 z 55 pkt) |
| Zabezpieczenie sprawdzone z wymogami urzędu (próg dochodu, liczba poręczycieli) przed złożeniem | forma zabezpieczenia, której urząd nie przyjmie; brak wymaganych dokumentów | [infakt.pl](https://www.infakt.pl/blog/?p=83318) – pkt 11; [Zielona Linia](https://zielonalinia.gov.pl/srodki-na-dzialalnosc-gospodarcza-z-urzedu-pracy-na-co-zwrocic-uwage/) – „pominięte zabezpieczenie lub załączniki” |
| Rodzaj działalności sprawdzony z listą wykluczeń urzędu | działalność wykluczona regulaminem (sezonowa, obwoźna, przejęcie po rodzinie) | [bankier.pl](https://www.bankier.pl/wiadomosc/Skresleni-przez-urzedy-pracy-Firmy-ktorym-nie-przyznano-dotacji-7610070.html) – Gdańsk: wykluczenia branż; `docs/jak-dziala-dotacja-2026.md`, rozdz. 8 |
| Podpisy, załączniki i termin pod kontrolą (lista na stronie tytułowej docx) | brak podpisu, brak załączników, wniosek po terminie, niestawienie się | [infakt.pl](https://www.infakt.pl/blog/?p=83318) – pkt 2, 5, 12; [bankier.pl](https://www.bankier.pl/wiadomosc/Skresleni-przez-urzedy-pracy-Firmy-ktorym-nie-przyznano-dotacji-7610070.html) – Poznań: odstąpienia przy utracie statusu bezrobotnego i niestawieniu się; regulamin Nowa Sól § 3 ust. 3 – nieobecność na komisji = odmowa |
| Firma rejestrowana dopiero po umowie i wypłacie (z wyjątkami urzędu, np. Grodzisk dla osób bez NIP) | działalność rozpoczęta przed umową | [zasady PUP Mińsk Maz.](https://minskmazowiecki.praca.gov.pl/documents/d/minskmazowiecki/zasady-przyznawania-jednorazowych-srodkow-na-podjecie-dzialalnosci-gospodarczej-2025-1-pdf) III pkt 17; wzór wniosku Grodzisk Maz. („wpis do CEIDG… przed zawarciem umowy skutkuje odmową”) |
| Konkret lokalny i głos wnioskodawcy (ulice, firmy, ceny, liczby ze źródłem) | ogólniki („dynamicznie rozwijający się rynek”, „kompleksowa obsługa”) | `szablony/00-system-prompt.md` (lista zakazana); kryteria „rozeznanie rynku” w kartach Turku, Grodziska i Nowej Soli |

## Aktualność i ograniczenia

- Nabory: Turek – trwa (12–16.10.2026); Grodzisk Maz. i Kolbuszowa – do ogłoszenia (przykłady na regulaminach i wzorach z 2026 r.). Przy realnym zleceniu zawsze pracujemy na dokumentach z ogłoszenia.
- Arkusze liczą na stałych z 2026 r., a miesiące działalności przypadają na 2027 r. – po ogłoszeniu wskaźników na 2027 r. zaktualizować `Stale-2026` w szablonie i przebudować modele (`zbuduj_modele.py`).
- Linki w kosztorysach to **oferty typu** (sklepy, porównywarki, Ceneo) z 10.2026 – ceny się zmieniają; klient dołącza konkretne oferty w PDF.
- Opisy konkurentów to fakty z publicznych profili (nazwa, adres, zakres, cennik, ocena) z 14.10.2026 – przed użyciem przykładu jako materiału pokazowego warto je odświeżyć.
