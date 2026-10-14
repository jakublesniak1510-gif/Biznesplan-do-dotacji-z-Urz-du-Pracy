# Biznesplan do dotacji z Urzędu Pracy

Usługa dla osób bezrobotnych, które składają w powiatowym urzędzie pracy (PUP) wniosek o **dofinansowanie podjęcia działalności gospodarczej**. Klient wypełnia kwestionariusz o swoim pomyśle. W 24–48 h dostaje gotowe treści do pól wniosku **swojego** urzędu: opis działalności i kwalifikacji, analizę rynku i konkurencji, specyfikację zakupów z uzasadnieniem i prognozę finansową na 12 miesięcy. Treści powstają z pomocą AI według szablonów, liczby liczy arkusz, a każdy plan właściciel sprawdza według checklisty.

**Czego nie robimy:** nie gwarantujemy dotacji, nie składamy wniosku za klienta, nie wymyślamy danych.

## Czym różnimy się od istniejących usług

| | Wzory z sieci | Firmy „pod klucz" | Ta usługa |
|---|---|---|---|
| Cena | 29–120 zł | 1 350–1 450 zł | **299 / 449 / 649 zł** |
| Czas | od ręki | 7–14 dni | **24–48 h** |
| Dopasowanie do urzędu | brak | ogólne | **regulamin, limity, karta oceny i formularz konkretnego PUP** (baza 30 urzędów) |
| Poprawki po wezwaniu urzędu | brak | zwykle płatne | **gratis w każdym pakiecie** |
| Alerty o naborach | brak | brak | **automatyczny monitor 341 urzędów, e-mail w dniu ogłoszenia** |
| Kontrola jakości | brak | ręczna | **automatyczna: zakazane zwroty, spójność liczb z arkuszem, limity regulaminu, podobieństwo planów do tego samego PUP** |

## Kluczowe fakty 2026 (źródła: `docs/jak-dziala-dotacja-2026.md`)

| Fakt | Stan na 14.10.2026 |
|---|---|
| Podstawa prawna | ustawa z 20.03.2025 o rynku pracy i służbach zatrudnienia (art. 147–153), rozporządzenie MRPiPS z 21.11.2025 |
| Limit ustawowy | 6 × przeciętne wynagrodzenie = **55 398,78 zł** (od 1.09.2026; aktualizacja 1.12.2026) |
| Limity urzędów | zwykle **30–49 tys. zł**, mediana w bazie 35 tys. zł |
| Obowiązki | min. 12 mies. działalności (Piotrków: 15), zawieszenie łącznie ≤ 6 mies., zakaz etatu |
| Zabezpieczenie | obowiązkowe, najczęściej 2 poręczycieli (mediana dochodu ok. 5 050 zł) lub blokada rachunku |
| Nabory | przez cały rok, szczyt luty–kwiecień i wrzesień; 81 ze 150 naborów 2026 trwało 1–7 dni |

## Jak to działa

1. **Quiz kwalifikacyjny** na stronie (warunki z art. 148, zabezpieczenie, nabór).
2. **Zamówienie i płatność** (Tally → Stripe Payment Link z BLIK).
3. **Kwestionariusz** z uploadem regulaminu i formularza urzędu, linkami do ofert zakupowych.
4. **Generator** (`generator/`): mapowanie pól formularza, arkusz finansowy, treści sekcji, automatyczna kontrola jakości, DOCX + raport dla właściciela.
5. **Kontrola właściciela** według `docs/checklista-weryfikacji.md`, wysyłka DOCX/PDF/XLSX z instrukcją „co wpisać samemu".
6. **Poprawki i wezwania** z urzędu w ramach gwarancji; po decyzji ankieta i rejestr wyników per PUP.

## Struktura repozytorium

| Ścieżka | Co zawiera |
|---|---|
| `PRZEGLAD-PROJEKTU.md` | ocena koncepcji, decyzje, podział pracy, odbiór etapów |
| `docs/` | ściągawka prawna 2026 ze źródłami, kwestionariusz klienta, checklista weryfikacji, FAQ |
| `baza-pup/` | **baza regulaminów 30 PUP** (CSV, 36 kolumn), 25 formularzy wniosków, analiza wspólnych sekcji 8 formularzy, kalendarz 150 naborów 2026 |
| `szablony/` | prompt systemowy z zasadami anty-generyczności, 9 szablonów sekcji, mapowanie pól, obsługa wezwań |
| `model-finansowy/` | arkusz XLSX (1 929 formuł): ZUS i podatki 2026, kosztorys z limitami, prognoza 12 mies., tabele do wniosku |
| `generator/` | **silnik produktu** w Pythonie: schemat danych, arkusz, prompty, Claude API z atrapą offline, 7 kontroli jakości, DOCX, CLI `pup-gen`; 62 testy |
| `przyklady/` | **3 wzorcowe wnioski** pod prawdziwe urzędy (Turek, Grodzisk Maz., Kolbuszowa) z arkuszami i DOCX; materiały klienta: list intencyjny, co po przyznaniu, odpowiedzi na wezwania, co wpisać samemu, 20 pytań komisji |
| `alerty/` | **monitor naborów**: API Zielonej Linii + 341 stron PUP, klasyfikator, treść alertu, eksport do mailingu; 85 testów; workflow cron |
| `strona/` | **statyczna strona WWW** (49 podstron): landing, quiz, cennik, 9 branż, 30 urzędów, regulamin, RODO; workflow GitHub Pages |
| `operacje/` | konkurencja z cenami, cennik v2, proces realizacji i stos narzędzi |
| `prawo/` | forma prawna i obowiązki (JDG, VAT, kasa), szkic regulaminu usługi, RODO i AI |
| `marketing/` | plan startu do stycznia 2027, alerty, SEO i treści |

## Uruchomienie

```bash
# generator (offline, atrapa modelu; prawdziwe API po ustawieniu ANTHROPIC_API_KEY)
cd generator && pip install -e . && python -m pytest -q
pup-gen generuj --kwestionariusz przyklady/fryzjerka-mobilna.json --mapa przyklady/mapa-dluga.json --dry-run --out /tmp/wynik

# monitor naborów
cd alerty && pip install -r requirements.txt && python -m pytest -q && python -m monitor.cli skanuj

# strona
cd strona && pip install -r requirements.txt && python3 build.py && python3 narzedzia/sprawdz.py
```

## Co podmienić przed startem sprzedaży

1. `strona/dane/site.json`: domena, nazwa marki, link do formularza Tally, adres formularza alertów (Brevo), e-mail, dane firmy.
2. Włączyć GitHub Pages (Settings → Pages → GitHub Actions); workflow `strona.yml` publikuje stronę.
3. Dodać sekret `BREVO_API_KEY`, żeby workflow `alerty.yml` wysyłał alerty (bez niego tworzy Issue z treścią).
4. Ustawić `ANTHROPIC_API_KEY` tam, gdzie uruchamiany jest generator.
5. Konsultacja prawnika: `prawo/regulamin-uslugi-szkic.md`, polityka prywatności, interpretacja indywidualna ws. VAT.
6. Zarejestrować JDG (PKD 70.20.Z), konto firmowe, Stripe z BLIK.

## Status (14.10.2026)

| Obszar | Status |
|---|---|
| Wiedza o dotacji 2026, kwestionariusz, checklista, FAQ | ✅ |
| Szablony AI, model finansowy | ✅ |
| Baza 30 urzędów, formularze, kalendarz naborów | ✅ (11 urzędów z danymi częściowymi, 4 bez regulaminu 2026) |
| Generator wniosków | ✅ offline; do sprawdzenia jakość tekstów z prawdziwym modelem |
| Monitor naborów | ✅ działa, skan z 14.10: 15 aktywnych naborów |
| Strona WWW | ✅ zbudowana, placeholdery do podmiany |
| Wzorcowe wnioski i materiały klienta | ✅ |
| Rejestracja firmy, płatności, prawnik, domena | ⏳ po stronie właściciela |
| Pierwsze zlecenia z prawdziwym modelem, pomiar czasu | ⏳ |
