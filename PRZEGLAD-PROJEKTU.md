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

## 4. Odbiór pracy (uzupełnię po przeglądzie)

_Sekcja wypełniana po sprawdzeniu plików pracowników._
