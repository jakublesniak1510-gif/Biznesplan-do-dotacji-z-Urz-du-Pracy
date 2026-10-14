# Biznesplan do dotacji z Urzędu Pracy – wersja 2

Usługa dla osób bezrobotnych, które chcą złożyć w powiatowym urzędzie pracy (PUP) wniosek o **dofinansowanie podjęcia działalności gospodarczej**. Klient wypełnia kwestionariusz o swoim pomyśle. W 24–48 h dostaje gotowe treści do pól wniosku **swojego** urzędu:
- opis działalności i kwalifikacji,
- analizę rynku i konkurencji,
- specyfikację zakupów z uzasadnieniem,
- prognozę finansową na 12 miesięcy.

Treści przygotowujemy z pomocą AI. Każdy plan właściciel sprawdza ręcznie według checklisty, zanim trafi do klienta.

## Dla kogo

- Osoby zarejestrowane jako bezrobotne, absolwenci CIS/KIS, opiekunowie osób niepełnosprawnych poszukujący pracy. To krąg uprawnionych z art. 147 ustawy z 20.03.2025 o rynku pracy i służbach zatrudnienia.
- Osoby, które mają pomysł i poręczycieli lub inne zabezpieczenie, ale nie wiedzą, jak napisać wniosek pod regulamin i kartę oceny urzędu.
- Klient chce taniej i szybciej niż u doradcy „pod klucz” (ok. 1 350–1 450 zł wg `operacje/konkurencja.md`), ale z treścią pisaną pod konkretny PUP, a nie z szablonu.

**Czego nie robimy:** nie gwarantujemy dotacji, nie składamy wniosku za klienta, nie reprezentujemy go przed urzędem, nie wymyślamy danych.

## Kluczowe fakty 2026 (szczegóły i źródła: `docs/jak-dziala-dotacja-2026.md`)

| Fakt | Stan na 14.10.2026 |
|---|---|
| Podstawa prawna | ustawa z 20.03.2025 (Dz.U. 2025 poz. 620, w mocy od 1.06.2025), art. 147–153, oraz rozporządzenie MRPiPS z 21.11.2025 (Dz.U. 2025 poz. 1645) |
| Limit ustawowy | 6 × przeciętne wynagrodzenie = **55 398,78 zł** (od 1.09.2026) |
| Limity urzędów w praktyce | zwykle **28–49 tys. zł** (Brodnica 32 tys., Kolbuszowa 40 tys., Łódź 49 tys.) |
| Obowiązki | min. 12 mies. działalności, zawieszenie łącznie ≤ 6 mies. (nie liczy się do 12), zakaz etatu, rozliczenie w 2 mies. od startu |
| Zabezpieczenie | obowiązkowe, najczęściej 2 poręczycieli. Główny powód rezygnacji klientów |
| Nabory | przez cały rok (luty–marzec, czerwiec–lipiec, wrzesień–październik), a nie „głównie w styczniu”. W 2026 r. środki FP mocno obcięte |

## Jak to działa – krok po kroku

1. **Kwalifikacja** (bezpłatny quiz na stronie): warunki z art. 148, zabezpieczenie, nabór w PUP.
2. **Zamówienie i płatność**: pakiet Podstawowy / Standard / Premium.
3. **Kwestionariusz** (`docs/kwestionariusz-klienta.md`): klient wgrywa regulamin naboru i formularz urzędu, linki do ofert zakupowych, dokumenty kwalifikacji.
4. **Weryfikacja kompletności** (właściciel, do 4 h): braki, ryzyka (np. brak poręczycieli, wykluczona branża), kontakt z klientem.
5. **Generowanie treści** według szablonów (`szablony/`) i modelu finansowego (`model-finansowy/`), pod pola formularza danego PUP.
6. **Kontrola jakości** według `docs/checklista-weryfikacji.md`: regulamin, limity, spójność liczb, prawdziwość, brak generycznego AI, test podobieństwa do innych planów do tego samego PUP.
7. **Wysyłka**: DOCX, PDF i arkusz plus instrukcja „co wpisać i podpisać samemu”.
8. **Poprawki**: runda poprawek, wsparcie przy wezwaniu do uzupełnień (min. 7 dni urzędowego terminu).
9. **Po decyzji urzędu**: ankieta o wyniku, opcjonalnie instrukcja „co po przyznaniu” lub pomoc w rozliczeniu.

Pakiety: w koncepcji v1 249 / 399 / 599 zł. Propozycja v2 z nowym zakresem i gwarancją poprawek po wezwaniu: `operacje/cennik-v2.md` (do decyzji właściciela).

## Struktura repozytorium

Katalogi powstają równolegle (stan na 14.10.2026).

| Ścieżka | Zawartość | Odpowiedzialny |
|---|---|---|
| `README.md` | ten plik | pracownik 1 |
| `PRZEGLAD-PROJEKTU.md` | ocena koncepcji, decyzje, podział pracy | właściciel |
| `docs/jak-dziala-dotacja-2026.md` | ściągawka prawna i praktyczna ze źródłami: uprawnieni, kwoty, de minimis, zabezpieczenia, nabory, wykluczenia, limity, karty oceny, komisja, rozliczenie | pracownik 1 |
| `docs/kwestionariusz-klienta.md` | pełny kwestionariusz z oznaczeniem pól obowiązkowych, wskazówkami „po co pytamy” i mapą pól wniosku | pracownik 1 |
| `docs/checklista-weryfikacji.md` | lista kontrolna przed wysyłką | pracownik 1 |
| `docs/faq-dla-klienta.md` | 25 pytań i odpowiedzi dla klientów | pracownik 1 |
| `szablony/` | prompt systemowy (zasady anty-generyczności), szablony sekcji wniosku, mapowanie pól | pracownik 2 |
| `model-finansowy/` | arkusz XLSX z prognozą 12 mies., ZUS i podatki 2026, instrukcja | pracownik 2 |
| `marketing/` | strategia, plan startu, SEO, alerty naborów | pracownik 3 |
| `prawo/` | forma prawna, regulamin usługi, RODO i AI | pracownik 3 |
| `operacje/` | cennik v2, konkurencja, proces realizacji, stos narzędzi | pracownik 3 |

## Status prac (14.10.2026)

| Obszar | Status |
|---|---|
| Weryfikacja faktów 2026 ze źródłami | ✅ gotowe (`docs/`). Otwarte punkty oznaczone „[do weryfikacji]” |
| Kwestionariusz, checklista, FAQ | ✅ wersja 1 do przeglądu |
| Szablony AI, model finansowy | 🔄 w toku (pracownik 2) |
| Marketing, prawo, operacje | 🔄 w toku (pracownik 3) |
| Strona, formularz, płatności | ⏳ nie rozpoczęte |
| Plany testowe (3 branże × 2 urzędy) | ⏳ nie rozpoczęte |

## Następne kroki

1. **Przegląd `docs/` przez właściciela.** Decyzja o korektach komunikacji: „nabory przez cały rok”, „55+ w EFS+”, brak „zakazu zawieszenia”, brak zakazu pojazdów w de minimis.
2. **Zaktualizować limit ustawowy w listopadzie 2026** (komunikat GUS za III kw., obowiązuje od 1.12.2026) w `docs/`, FAQ i na stronie.
3. **Zbudować formularz** z kwestionariusza: logika warunkowa (mobilnie, poręczyciele, sprzęt używany), upload plików, zapis wersji roboczej, bez pól PESEL i adresu.
4. **Baza regulaminów PUP**: arkusz z kolumnami: kwota maks., limity %, wykluczenia, zabezpieczenie, karta oceny, rozmowa/wizja. Start od 20–30 powiatów z największym ruchem.
5. **3 plany testowe** przez pełny proces z checklistą. Pomiar czasu realizacji, kalibracja cennika.
6. **Wzór listu intencyjnego** i instrukcja dla klienta (punkty w kartach oceny).
7. **Alerty naborów**: monitoring stron PUP i zielonalinia.gov.pl, mailing do bazy z quizu.
8. **Ankieta po decyzji urzędu** i rejestr wyników per PUP jako argument sprzedażowy na 2027.
9. Zamknąć punkty „[do weryfikacji]”: rola FERS w dotacjach PUP, PFRON jako druga ścieżka, dostępność gwarancji bankowych, aktualna PKD w formularzach.
