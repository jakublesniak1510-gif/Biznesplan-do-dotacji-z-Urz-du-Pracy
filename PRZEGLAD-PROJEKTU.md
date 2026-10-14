# Przegląd projektu – ocena i polecenia (14.10.2026)

Ocena koncepcji „Biznesplan do dotacji z Urzędu Pracy" w wersji z briefu.
Werdykt: pomysł dobry, nisza realna, ale koncepcja ma kilka błędów faktycznych i poważne luki,
które zdecydują o tym, czy klienci dostaną dotację. Poniżej: co poprawić, co dodać, komu co zlecono.

## 1. Co poprawić (błędy i słabe założenia)

| # | Założenie w koncepcji | Problem | Decyzja |
|---|---|---|---|
| 1 | „Urzędy przyznają zwykle 25–40 tys. zł" | Ustawowy limit to wielokrotność przeciętnego wynagrodzenia (ok. 50+ tys. zł w 2026). Każdy PUP ustala własny, niższy limit. Kwoty Kolbuszowa/Brodnica podane bez źródła. | Pisać „zwykle 25–45 tys. zł, limit zależy od urzędu", podawać tylko kwoty z linkiem do regulaminu. |
| 2 | Warunki (12 mies. bez firmy itd.) opisane wg starej ustawy | Od 1.06.2025 obowiązuje nowa ustawa o rynku pracy i służbach zatrudnienia. Warunki trzeba zweryfikować w nowym brzmieniu, także krąg uprawnionych (opiekunowie osób z niepełnosprawnościami, absolwenci CIS/KIS). | Pracownik 1 weryfikuje ze źródłami → `docs/jak-dziala-dotacja-2026.md`. |
| 3 | „Większość naborów na początku roku, poza naborami sprzedaż spada" | Nabory z Funduszu Pracy faktycznie często w I kw., ale nabory z EFS+ (programy regionalne, grupy docelowe: do 30 lat, 50+, kobiety, długotrwale bezrobotni) idą przez cały rok. | Strategia całoroczna: alerty obejmują wszystkie źródła, treści SEO per grupa docelowa. |
| 4 | Premium = „przygotowanie do rozmowy w urzędzie" | W wielu PUP nie ma rozmowy z komisją, ocena jest wyłącznie punktowa na podstawie wniosku. Klient płaci 200 zł więcej za coś, czego może nie użyć. | Premium przebudować: wsparcie przy wezwaniu do uzupełnień, weryfikacja kosztorysu z ofertami, instrukcja „co po przyznaniu" (umowa, zabezpieczenie, rozliczenie). |
| 5 | „Formularz Tally i płatność BLIK" | Tally nie ma własnego BLIK. Działa przez Stripe (BLIK dostępny w PL) albo trzeba dołożyć bramkę (P24/Tpay/Autopay). | Pracownik 3 sprawdza i proponuje stos narzędzi. |
| 6 | Cennik 249/399/599 | Nie wiadomo, co to „1 poprawka". Brak gwarancji poprawek po wezwaniu urzędu, która jest najtańszym i najsilniejszym argumentem sprzedażowym. Brak dopłat (ekspres, drugi urząd, listy intencyjne). | Cennik v2 → `operacje/cennik-v2.md`. |
| 7 | „Koszt to Twój czas, 1–2 h na plan" | Nie policzono poprawek, telefonów, zbierania danych od klienta. Przy 40 planach to 80–120 h/mies. dla jednej osoby, w sezonie równolegle z marketingiem. | Policzyć realny czas na pakiet i stawkę godzinową; limit zamówień/tydzień. |
| 8 | „AI tworzy treści dopasowane do pól formularza" | Największe ryzyko produktu: komisja w jednym urzędzie dostaje kilka wniosków od Ciebie w tym samym stylu. Jednakowe plany = podejrzenie, że wnioskodawca nie zna własnego biznesu. | Prompt systemowy z zakazem fraz generycznych, parametr tonu, test „czy dwa plany do tego samego PUP nie brzmią identycznie" w checkliście. |
| 9 | Forma sprzedaży nieokreślona | Przy 6–15 tys. zł/mies. działalność nierejestrowana odpada (od 2026 limit kwartalny 225 % płacy minimalnej = 10 813,50 zł/kwartał). Zwolnienie z VAT (limit 240 tys. zł od 2026) może nie przysługiwać, bo przepisy wyłączają „doradztwo" – ryzyko VAT 23 % od pierwszej sprzedaży. | JDG od startu, PKD 2025: 70.20.Z. Wniosek o interpretację indywidualną ws. VAT jeszcze w październiku → `prawo/forma-prawna-i-obowiazki.md`. |
| 10 | „Dane w biznesplanie muszą być prawdziwe" (tylko kwalifikacje) | Dotyczy też kosztorysu: urzędy żądają ofert/screenów cen. Zmyślona cena = wezwanie do uzupełnień lub odrzucenie. | Kwestionariusz wymaga linku/screena do każdej pozycji zakupowej. |
| 11 | Harmonogram „3 tygodnie" | 10–15 formularzy, szablony, model, 3 plany testowe, strona, regulamin i alerty w 3 tygodnie u jednej osoby to nierealne. | Plan 8–9 tygodni do połowy grudnia → `marketing/plan-startu-do-stycznia-2027.md`. |

## 2. Co dodać (brakujące elementy)

1. **Katalog wydatków i limity** – każdy regulamin ma procenty (reklama, towar, remont), zakazy (kaucje, leasing, samochód, koszty bieżące) i zasady dla sprzętu używanego. Bez tego kosztorys przepada. Checklista + kolumna limitów w arkuszu.
2. **Zabezpieczenie zwrotu** – poręczyciel, weksel, blokada rachunku, akt notarialny. To częsty powód, dla którego klient wycofuje się po zapłaceniu za plan. Pytać o to w kwestionariuszu na początku.
3. **Karta oceny punktowej** – większość PUP publikuje kryteria (kwalifikacje, wkład własny, analiza rynku, listy intencyjne). Treści mają celować w punktowane pola, nie w „ładny biznesplan".
4. **Pomoc de minimis** – formularz informacji, limit, branże wykluczone. Klient o tym nie wie.
5. **Listy intencyjne / deklaracje klientów** – szablon dla klienta; podnoszą punkty w wielu urzędach. Osobna dopłata lub element Standard.
6. **RODO i AI** – minimalizacja danych (bez PESEL/adresu w promptach), polityka prywatności, retencja plików, zasady retencji danych w API dostawcy modelu. Regulamin usługi z prawem odstąpienia i wyraźnym „nie gwarantujemy dotacji".
7. **Pomiar skuteczności** – ankieta po decyzji urzędu, baza wyników per PUP. Za rok to będzie główny argument sprzedażowy i dane do kalibracji szablonów.
8. **Lead magnet przed alertami** – quiz „Sprawdź, czy się kwalifikujesz" zbiera e-maile cały rok, nie tylko w naborze.
9. **Druga noga poza sezonem** – te same szablony pasują do pożyczki BGK „Pierwszy biznes – Wsparcie w starcie", premii LGD/PROW, środków PFRON, projektów EFS+ operatorów; plus usługa rozliczenia dotacji po przyznaniu.
10. **Model finansowy jako produkt, nie dodatek** – arkusz z ZUS 2026 (ulga na start → preferencyjny → pełny), składką zdrowotną wg formy opodatkowania, progiem rentowności i scenariuszem −30 %. To odróżnia plan od treści „z czatu".

## 3. Polecenia dla pracowników (Opus 5.5), realizacja równoległa

| Pracownik | Zakres | Pliki |
|---|---|---|
| 1 – Dokumentacja i wiedza o dotacji | Weryfikacja faktów 2026 ze źródłami, kwestionariusz, checklista, FAQ, README v2 | `docs/`, `README.md` |
| 2 – Szablony AI i model finansowy | Prompt systemowy z zasadami anty-generyczności, 9 szablonów sekcji z przykładami branżowymi, mapowanie pól formularza, arkusz XLSX z formułami i stałymi 2026 | `szablony/`, `model-finansowy/` |
| 3 – Marketing, prawo, operacje | Badanie konkurencji i cen, cennik v2, proces realizacji i stos narzędzi, forma prawna, szkic regulaminu, RODO/AI, harmonogram do stycznia 2027, alerty naborów, SEO i treści | `operacje/`, `prawo/`, `marketing/` |

Zasady dla wszystkich: po polsku, konkretnie, każdy fakt o przepisach i kwotach ze źródłem, czego nie da się potwierdzić – oznaczyć „[do weryfikacji]". Nic nie zmyślamy, bo klient podpisuje wniosek pod rygorem zwrotu dotacji.

## 4. Odbiór pracy (14.10.2026, po sprawdzeniu plików)

Wszystkie trzy zlecenia przyjęte. Łącznie 31 plików, w tym arkusz XLSX (1 929 formuł, 0 błędów po przeliczeniu w LibreOffice).

### Co pracownicy ustalili ponad moją ocenę (korekty także moich założeń)

| Temat | Ustalenie | Źródło w repo |
|---|---|---|
| Limit ustawowy | 6 × przeciętne wynagrodzenie = 55 398,78 zł od 1.09.2026. Urzędy dają zwykle 28–49 tys. zł. Kwoty Kolbuszowa 40 tys. i Brodnica 32 tys. potwierdzone w ogłoszeniach z lipca 2026. | `docs/jak-dziala-dotacja-2026.md` |
| Terminy naborów | Styczeń jest **cichy** (urzędy czekają na podział Funduszu Pracy). Szczyt: luty–kwiecień, potem czerwiec–lipiec i wrzesień–październik. Nabory trwają też teraz. Hasło „ruszaj przed styczniem" zostaje, ale cel to luty. | `docs/`, `marketing/alerty-naborow.md` |
| Zawieszenie firmy | Nie ma „zakazu zawieszenia": można zawiesić łącznie do 6 mies., ten czas nie liczy się do obowiązkowych 12. | `docs/jak-dziala-dotacja-2026.md` |
| Moje błędy w briefie | Wykluczenie pojazdów w de minimis jest nieaktualne (rozp. 2023/2831); FEnIKS nie finansuje dotacji PUP (robią to programy regionalne EFS+); w projektach EFS+ grupa to zwykle 55+, nie 50+. | tamże, tabela weryfikacji |
| Naszej usługi nie da się opłacić z dotacji | Rozliczane są tylko wydatki od dnia umowy. Nie obiecywać tego klientom. | tamże |
| Działalność nierejestrowana | Od 2026 limit kwartalny 10 813,50 zł. JDG konieczna od startu. | `prawo/forma-prawna-i-obowiazki.md` |
| VAT | Limit zwolnienia 240 tys. zł, ale „doradztwo" jest wyłączone ze zwolnienia. Interpretacja indywidualna (40 zł) do złożenia w październiku, zanim ruszy sprzedaż. | tamże |
| Kasa fiskalna | Zwolnienie przy płatnościach wyłącznie na rachunek (poz. 42 rozporządzenia). Zero gotówki. | tamże |
| Płatność BLIK | Tally sam nie obsługuje BLIK. Rozwiązanie: Tally → przekierowanie na Stripe Payment Link (BLIK dostępny, 1,6 % + 1 zł) z numerem zgłoszenia. | `operacje/proces-realizacji.md` |
| Konkurencja | „Pod klucz" 1 350–1 450 zł, 7–14 dni; wzory 29–120 zł; weryfikacja wniosku 169 zł. Luka: 24–48 h, 300–650 zł, pod formularz konkretnego PUP, alerty. | `operacje/konkurencja.md` |
| Cennik v2 | 299 / 449 / 649 zł, gwarancja poprawek po wezwaniu w każdym pakiecie, dopłaty (ekspres 99, ponowne złożenie 149, inny program 199, listy intencyjne 79, rozliczenie 249). Czas właściciela 1,75 / 2,9 / 4,8 h; przy 40 planach to ok. 140 h/mies. – sufit dla jednej osoby. | `operacje/cennik-v2.md` |
| Alerty naborów | Zielona Linia publikuje nabory (ok. 135 wpisów w 2026, otwarte API, RSS nie działa). Wszystkie PUP mają wspólny szablon stron `[pup].praca.gov.pl`, więc wystarczy jeden skrypt monitorujący. | `marketing/alerty-naborow.md` |
| Model finansowy | Stałe 2026 ze źródłami pierwotnymi (płaca min. 4 806 zł, pełny ZUS 1 926,76 zł, preferencyjny 456,18 zł, zdrowotna min. 432,54 zł). Przy starcie firmy w grudniu 11 miesięcy przypada na 2027 r. – po ogłoszeniu stałych 2027 dodać arkusz `Stale-2027`. | `model-finansowy/INSTRUKCJA.md` |

Dwie kwoty przeciętnego wynagrodzenia za II kw. 2026 w repo (9 233,13 zł i 9 396,33 zł) to dwie różne miary GUS: pierwsza (gospodarka narodowa) liczy limit dotacji, druga (sektor przedsiębiorstw) jest w arkuszu tylko informacyjnie. Nie ma sprzeczności.

### Decyzje, które zostają po stronie właściciela

1. **Ceny:** README podaje v1 (249/399/599), `operacje/cennik-v2.md` proponuje 299/449/649. Rekomenduję v2 – przy VAT 23 % w cenie stawka godzinowa i tak spada o ok. 20 zł/h.
2. **VAT:** złożyć wniosek o interpretację indywidualną teraz. Do czasu odpowiedzi kalkulować ceny tak, jakby VAT był należny.
3. **Zakres Premium:** przebudowany (uzupełnienia, weryfikacja kosztorysu z ofertami, instrukcja „co po przyznaniu"). Przygotowanie do komisji tylko tam, gdzie urząd ją prowadzi (np. Nowa Sól – obowiązkowa).
4. **Regulamin i RODO:** szkice w `prawo/` wymagają konsultacji z prawnikiem przed startem sprzedaży.

### Otwarte punkty „[do weryfikacji]" (zebrane)

- Limit dotacji od 1.12.2026 (komunikat GUS za III kw. ok. 10.11.2026).
- Rola FERS i PFRON jako osobnych ścieżek; dostępność gwarancji bankowych dla bezrobotnych.
- Czy pisanie biznesplanów to „doradztwo" dla VAT i kasy fiskalnej; czy BLIK przez Stripe spełnia warunek zwolnienia z kasy.
- Tally: przekazywanie pól w adresie przekierowania, prowizja w planie darmowym. Alternatywy Tpay/P24/Autopay dla linku płatniczego.
- Kody PKD 2025 w przykładach branżowych (źródła wtórne).
- Warunki Małego ZUS plus i zwolnienie dotacji z PIT w modelu finansowym.
- Ceny WROSKO, biznesnagotowo.pl, oferty z OLX/Useme (nie udało się pobrać).
- Udział wezwań do uzupełnień (założono 25–30 %) i koszt API na plan (założono ok. 6 zł) – do zmierzenia na pierwszych zamówieniach.

### Następne zlecenia (kolejność)

1. Baza regulaminów 20–30 PUP w arkuszu (kwota, limity %, wykluczenia, zabezpieczenie, karta oceny, komisja/wizja) – fundament pod mapowanie pól.
2. Trzy plany testowe przez cały proces (fryzjerka mobilna, mechanik, firma sprzątająca) z pomiarem czasu – kalibracja cennika i szablonów.
3. Strona + quiz kwalifikacyjny + zapis na alerty + formularz Tally z płatnością Stripe.
4. Skrypt monitorujący nabory (API Zielonej Linii + strony PUP) i pierwszy mailing w grudniu.
5. Wzór listu intencyjnego i instrukcja dla klienta.

## 5. Etap 2 – z dokumentacji w produkt lepszy od konkurencji (start 14.10.2026)

Właściciel przekazał pełne pełnomocnictwo: decyzje podejmuję sam, bez pytań.

### Decyzje podjęte

| Decyzja | Uzasadnienie |
|---|---|
| Cennik v2 obowiązuje: 299 / 449 / 649 zł, gwarancja poprawek po wezwaniu w każdym pakiecie, dopłaty wg `operacje/cennik-v2.md` | Konkurencja „pod klucz" bierze 1 350–1 450 zł; zostajemy 2–5× tańsi i jedyni z gwarancją w cenie bazowej |
| Ceny traktujemy jako brutto z VAT 23 % do czasu interpretacji indywidualnej | Ryzyko wyłączenia „doradztwa" ze zwolnienia; lepiej nie podnosić cen po starcie |
| Przewaga nr 1 to **baza regulaminów 30 PUP** i podstrony per urząd | Żaden konkurent nie pokazuje publicznie limitów, wykluczeń i kart oceny konkretnych urzędów. To jednocześnie najlepszy SEO i dowód kompetencji |
| Przewaga nr 2 to **monitor naborów** z alertami e-mail działający automatycznie (GitHub Actions, koszt 0 zł) | Nabory trwają 1–5 dni; kto pierwszy powiadomi, ten sprzedaje |
| Przewaga nr 3 to **automatyczna kontrola jakości** w generatorze: zakazane zwroty, spójność liczb z arkuszem, limity regulaminu, test podobieństwa planów do tego samego PUP | Komisje odrzucają szablonowe wnioski; konkurencja nie ma takiej kontroli |
| Generator działa offline z atrapą modelu, prawdziwe API włącza klucz | W tym środowisku nie ma klucza; produkt musi być testowalny bez kosztów |
| Strona statyczna, bez frameworka, publikowana z GitHub Pages | Zero kosztów utrzymania, szybkość, SEO; właściciel podmienia tylko domenę i linki do Tally/Brevo |
| Trzy wzorcowe wnioski pisane ręcznie przez pracownika, pod prawdziwe karty oceny | Służą jako few-shot dla modelu i jako materiał pokazowy; jakość wzorca wyznacza jakość produktu |

### Pakiety pracy etapu 2 (równolegle, Opus 5.5)

| # | Pakiet | Katalog | Kryterium odbioru |
|---|---|---|---|
| A | Baza regulaminów 30 PUP + formularze + wspólne sekcje + kalendarz naborów 2026 | `baza-pup/` | CSV zgodny ze schematem, każda wartość ze źródłem, ≥ 40 naborów w kalendarzu |
| B | Generator wniosków (Python): schemat, arkusz, prompty, Claude API z atrapą, kontrola jakości, DOCX, CLI | `generator/` | `pytest` zielony, 3 przykłady przechodzą `--dry-run` do DOCX |
| C | Strona WWW: landing, quiz kwalifikacyjny, cennik, 9 branż, podstrony urzędów z CSV, regulamin, RODO, workflow Pages | `strona/`, `.github/workflows/strona.yml` | build bez błędów, linki wewnętrzne sprawdzone, zrzuty 390/1280 px |
| D | Monitor naborów: Zielona Linia + strony PUP, klasyfikator, alerty, eksport do mailingu, workflow cron | `alerty/`, `.github/workflows/alerty.yml` | `pytest` zielony, prawdziwy skan z dzisiejszymi naborami |
| E | Trzy wzorcowe wnioski pod prawdziwe urzędy + materiały klienta (list intencyjny, co po przyznaniu, odpowiedzi na wezwania, pytania komisji) | `przyklady/` | liczby zgodne z arkuszem, zero zakazanych zwrotów, trzy różne tony |

### Odbiór etapu 2 (14.10.2026)

Wszystkie pięć pakietów przyjęte po własnej weryfikacji (testy uruchomione przeze mnie, budowa strony powtórzona, CSV zwalidowany, przykłady przepuszczone przez skrypt kontrolny).

| Pakiet | Wynik odbioru |
|---|---|
| A – Baza PUP | 30 urzędów, 36 kolumn, CSV poprawny. 19 kompletnych, 11 częściowych, 4 bez regulaminu 2026 (Katowice, Brodnica, Wrocław, Bartoszyce). 25 formularzy pobranych, 8 przeanalizowanych pole po polu. Kalendarz: 150 naborów 2026, 81 trwało 1–7 dni. Odkrycia: Kielce i Słupsk zakazują towaru handlowego z dotacji, Opole zakazuje wszystkich pojazdów, Zielona Góra wymaga zabezpieczenia na 200 % kwoty, Gorlice wymagają 25 % wkładu własnego. Żaden formularz nie podaje limitów znaków, ogranicza tylko rozmiar ramki. |
| B – Generator | 62 testy zaliczone (z prawdziwym LibreOffice). Walidacja odrzuca PESEL i numer dowodu. Test regresji: arkusz daje dokładnie liczby z szablonu 08. Koszt API: 0,5–1 USD na plan (Opus 5.5 z cache), ok. 2–4 zł. Brak: jakość tekstów z prawdziwym modelem nie sprawdzona (brak klucza), `mapuj` nie rozpoznaje tabel wielokolumnowych. |
| C – Strona | 49 stron HTML, 2 158 linków sprawdzonych, 0 błędów, walidator W3C 0 błędów, brak przewijania poziomego na 390 px, quiz przetestowany w Playwright w 3 scenariuszach. Podstrony urzędów same ostrzegają o kwocie wyższej niż limit ustawowy (Rzeszów 57 377 zł) i o braku regulaminu. Placeholdery zebrane w jednym pliku. |
| D – Monitor | 85 testów zaliczonych. Prawdziwy skan 14.10: 15 aktywnych naborów (m.in. Legnica 19–28.10 do 28 000 zł, Tuchola 19–20.10, Turek 12–16.10 do 38 822 zł). Endpoint Zielonej Linii potwierdzony (WordPress REST, kategoria 235, Crawl-delay 30 s). 341 z 341 subdomen PUP potwierdzonych. Brak: kwotę ma tylko 46 % wpisów, przedłużenia terminów bez nowego wpisu nie są wykrywane. |
| E – Przykłady | 3 wnioski pod prawdziwe karty oceny (Turek, Grodzisk Maz., Kolbuszowa), 3 tony, 0 zakazanych zwrotów, 0 liczb spoza arkusza, sekcje 1 700–2 300 znaków. Przykład uczciwości: w Turku pracownik znalazł konkurentkę z dojazdem, więc wyróżnik klientki zmienił z „jedyna z dojazdem" na obsługę osób leżących. Materiały klienta kompletne. |

### Co zostaje do zrobienia po stronie właściciela

1. Rejestracja JDG, konto firmowe, Stripe z BLIK, domena, nazwa marki.
2. Interpretacja indywidualna ws. VAT (teraz), prawnik do regulaminu i polityki prywatności.
3. Włączenie GitHub Pages i sekretu Brevo; podmiana placeholderów w `strona/dane/site.json`.
4. Pierwsze 3–5 zleceń z prawdziwym modelem i pomiar czasu na pakiet; kalibracja promptów na podstawie `przyklady/`.
5. W listopadzie: nowy limit ustawowy (GUS za III kw.), stałe ZUS/PIT 2027 do arkusza, uzupełnienie 11 częściowych urzędów w bazie.
