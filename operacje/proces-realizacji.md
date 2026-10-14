# Proces realizacji: od zamówienia do odesłania

Stan na 14.10.2026. Zespół to jedna osoba (właściciel). Wszystko, co da się zautomatyzować bez kodu, robi automat. Właściciel robi tylko to, co wymaga oceny.

## 1. SLA (obietnice terminowe)

| Pakiet | Termin | Liczony od |
|---|---|---|
| Podstawowy, Standard | **48 h robocze** | kompletu danych **i** zaksięgowanej płatności |
| Premium, ekspres | **24 h robocze** | j.w. |
| Poprawki (runda) | 48 h robocze (Premium: 24 h) | otrzymania zbiorczej listy uwag |
| Poprawki po wezwaniu urzędu (gwarancja) | **24 h robocze** | otrzymania skanu wezwania |
| Odpowiedź na e-mail | do 1 dnia roboczego | — |

Zasady:
- „Godziny robocze” to pon.–pt. 9:00–17:00. Zamówienie opłacone po 16:00 albo w weekend liczy się od 9:00 następnego dnia roboczego. Zasadę trzeba wpisać do regulaminu.
- Zegar SLA **staje**, gdy czekamy na dane od klienta (status „Czeka na klienta”).
- **Limit mocy przerobowych:** do 6 nowych planów dziennie w SLA (≈ 15–17 h pracy) i maks. 2 ekspresy dziennie. Po przekroczeniu limitu formularz pokazuje komunikat „Realizacja od [data]” albo zamyka przyjęcia. Można to zrobić ręcznie (edycja tekstu w Tally) albo limitem zgłoszeń w ustawieniach formularza **[do weryfikacji, czy Tally ma limit zgłoszeń w planie darmowym]**.

## 2. Statusy zamówienia (kolumna w CRM)

`Nowe` → `Opłacone` → `Weryfikacja danych` → (`Czeka na klienta`) → `W realizacji` → `Kontrola końcowa` → `Wysłane` → (`Poprawki`) → `Zamknięte` → `Złożone w PUP` → `Wynik: przyznano / odmowa / wezwanie / lista rezerwowa / nie złożono`

## 3. Procedura krok po kroku

| # | Krok | Kto | Narzędzie | Czas właściciela |
|---|---|---|---|---|
| 1 | Klient wypełnia kwestionariusz: PUP, link do ogłoszenia naboru, pomysł, kwalifikacje, lista zakupów, lokal, kwoty, pliki (formularz urzędu, regulamin, oferty). Zgody: regulamin, żądanie rozpoczęcia usługi przed upływem 14 dni, polityka prywatności. **Bez PESEL, numeru dowodu i dokładnego adresu** (zob. `prawo/rodo-i-ai.md`) | klient | Tally (upload plików) | 0 (klient: 15–25 min) |
| 2 | Przekierowanie po wysłaniu formularza na płatność BLIK lub kartą z ID zgłoszenia w `client_reference_id` | automat | Tally → Stripe Payment Link | 0 |
| 3 | Potwierdzenie zamówienia e-mailem (trwały nośnik: regulamin, informacja o odstąpieniu, złożone oświadczenia), wiersz w CRM | automat | Tally → Google Sheets (integracja natywna) + e-mail z Tally lub Make | 0 |
| 4 | Dopasowanie płatności do zgłoszenia (status `Opłacone`) | automat albo ręcznie | Stripe → Make (webhook `checkout.session.completed`) albo ręcznie po e-mailu | 0–2 min |
| 5 | **Weryfikacja danych** według checklisty (sekcja 4). Braki: szablon e-maila „Brakuje nam…”, status `Czeka na klienta` | właściciel | CRM, Gmail (szablony) | 10 min |
| 6 | Sprawdzenie, czy PUP jest w bazie formularzy. Jeśli nie: pobranie formularza i regulaminu, mapowanie pól, wykluczenia, kryteria oceny | właściciel | `szablony/`, folder „Baza PUP” | 0 (albo jednorazowo 30–45 min) |
| 7 | Anonimizacja danych (imię, nazwisko, e-mail i telefon zamienione na tokeny), złożenie promptu z szablonu urzędu i branży, generowanie treści | właściciel + skrypt | skrypt + API modelu | 10 min |
| 8 | Kosztorys i (Standard/Premium) prognoza w arkuszu. Kontrola sum i wykluczeń | właściciel | arkusz z `model-finansowy/` | 10–30 min |
| 9 | (Standard/Premium) Analiza konkurencji: 5–8 firm z okolicy | właściciel | Google Maps, strony firm | 25 min |
| 10 | (Premium) Weryfikacja kosztorysu z ofertami: do 10 pozycji, link + cena + data | właściciel | sklepy internetowe, Allegro, hurtownie | 30 min |
| 11 | **Redakcja i weryfikacja** według checklisty jakości (sekcja 5) | właściciel | edytor DOCX | 35–60 min |
| 12 | Złożenie dokumentu: DOCX (edytowalny, do przeklejenia w formularz) + PDF (podgląd) + arkusz. Nazwa: `PUP-[urząd]-[nr zamówienia]-v1` | skrypt | szablon DOCX (docxtpl/pandoc) + LibreOffice headless do PDF | 5 min |
| 13 | Wysyłka: e-mail z linkiem do plików (link wygasa po 30 dniach), instrukcją „jak przenieść treść do formularza urzędu”, terminem na uwagi (7 dni), opisem gwarancji i rachunkiem lub fakturą | właściciel | Gmail + Google Drive + program do faktur | 5 min |
| 14 | (Premium) Telefon 30 min. Notatka do CRM | właściciel | telefon / Google Meet, Cal.com do rezerwacji | 45 min |
| 15 | Poprawki (sekcja 6) | właściciel | j.w. | średnio 10–20 min |
| 16 | E-mail „Daj znać, kiedy złożysz” (przycisk/link do mini-ankiety z datą złożenia) | automat | Tally + Make / ręcznie | 0 |
| 17 | **Ankieta wyniku** po 60 dniach od złożenia (lub po 75 dniach od wysyłki, jeśli brak daty złożenia), przypomnienia +7 i +21 dni | automat | Tally + e-mail | 0 |
| 18 | Wpis wyniku do bazy skuteczności, wnioski do szablonów | właściciel | arkusz „Skuteczność” | 2 min |
| 19 | Usunięcie plików klienta zgodnie z retencją (zob. `prawo/rodo-i-ai.md`) | właściciel (przypomnienie w kalendarzu) | Drive, Tally, Stripe (metadane zostają) | 2 min/zamówienie (raz w tygodniu, hurtem) |

## 4. Checklista weryfikacji danych (krok 5)

- [ ] Urząd (PUP) jest ustalony i zgodny z miejscem zamieszkania lub zameldowania klienta.
- [ ] Jest link do aktualnego ogłoszenia naboru albo regulaminu. Formularz jest aktualny (data wersji).
- [ ] Rodzaj działalności nie jest wykluczony w regulaminie (np. sezonowa, spółka, handel obwoźny: zależy od urzędu).
- [ ] Wnioskowana kwota mieści się w limicie naboru.
- [ ] Lista zakupów ma ceny. Pozycje wykluczone (np. używane środki trwałe, leasing, opłaty bieżące: zależnie od regulaminu) są oznaczone.
- [ ] Opisane są kwalifikacje: wykształcenie, kursy, doświadczenie, w tym nieformalne.
- [ ] Lokal: jest, w trakcie albo dom. Forma: najem, użyczenie, własność.
- [ ] Planowani klienci i ceny usług są określone, choćby szacunkowo.
- [ ] Wkład własny i jego dokumentacja.
- [ ] Zgody i oświadczenia z kroku 1 są złożone.

**Braki danych: ścieżka eskalacji**

| Dzień | Działanie | Kanał |
|---|---|---|
| D+0 | E-mail z **konkretną listą** braków (pytania zamknięte, przykłady odpowiedzi), status `Czeka na klienta` | e-mail |
| D+2 | Przypomnienie | e-mail (+ SMS, jeśli klient zgodził się na kontakt telefoniczny) |
| D+5 | Telefon albo e-mail z propozycją: „uzupełnimy wersję z polami [UZUPEŁNIJ] do Twojego potwierdzenia” | telefon / e-mail |
| D+14 | Informacja: zamówienie zostanie zawieszone za 16 dni | e-mail |
| D+30 | Zawieszenie | e-mail |
| D+60 | Zamknięcie i zwrot według polityki zwrotów (`cennik-v2.md`) | e-mail |

Zasada: **nie wymyślamy faktów za klienta**, czyli kwalifikacji, doświadczenia, umów, klientów i cen. Jeśli danych brakuje, w dokumencie wstawiamy wyraźne pole `[UZUPEŁNIJ: …]` i komentarz. Model może zaproponować przykładowe sformułowanie, ale klient potwierdza jego prawdziwość.

Jeśli nabór kończy się szybciej, niż klient uzupełni dane, wysyłamy wersję z polami `[UZUPEŁNIJ]` i informacją, co dokładnie musi dopisać przed złożeniem. To nie zwalnia nas z gwarancji dla pozostałych treści.

## 5. Checklista jakości (krok 11)

- [ ] Każde pole formularza danego PUP ma treść. Limity znaków są zachowane.
- [ ] Kwoty w opisie = kosztorys = prognoza = wnioskowana kwota.
- [ ] Każdy wydatek ma uzasadnienie powiązane z opisem działalności i nie jest na liście wykluczeń.
- [ ] Brak obietnic nie do udowodnienia („brak konkurencji”, „pewny zysk”).
- [ ] Konkurencja jest prawdziwa i lokalna (nazwy firm sprawdzone w Mapach).
- [ ] Prognoza jest ostrożna: realistyczne obłożenie, sezonowość, koszty ZUS po uldze.
- [ ] Język prosty, pierwsza osoba, bez ozdobników typowych dla tekstów generowanych.
- [ ] Brak danych, których klient nie podał (fakty sprawdzone z kwestionariuszem).
- [ ] Pola `[UZUPEŁNIJ]` są wyróżnione i wymienione w e-mailu.
- [ ] Nazwy plików i metadane DOCX nie zawierają danych innych klientów.

## 6. Obsługa poprawek

1. Klient odpowiada na e-mail z dokumentem **jedną zbiorczą listą** uwag w ciągu 7 dni. Uwagi może wpisać w komentarzach DOCX.
2. Właściciel kwalifikuje uwagi: korekta / merytoryczna / nowe zamówienie (definicje w `cennik-v2.md`, sekcja 3). Jeśli coś wykracza poza pakiet, wysyła link do dopłaty **przed** wykonaniem.
3. Wersja `v2` z listą zmian w treści e-maila.
4. **Wezwanie z urzędu:** klient przesyła skan, status `Poprawki – wezwanie`, priorytet nad nowymi zamówieniami, termin 24 h. W CRM odnotowujemy, czego dotyczyło wezwanie (kategoria), bo to paliwo do poprawy szablonów.
5. Po 7 dniach bez uwag status `Zamknięte` (e-mail „Zamykamy rundę poprawek, gwarancja po wezwaniu dalej obowiązuje”).

## 7. Zbieranie wyników i baza skuteczności per urząd

**Ankieta wyniku (Tally, 6–8 pytań, ok. 2 min):**
1. Czy wniosek został złożony? (tak / nie, dlaczego)
2. Data złożenia.
3. Czy urząd wzywał do uzupełnień? Czego dotyczyło? (lista + inne)
4. Czy była rozmowa lub komisja?
5. Decyzja: przyznano (kwota) / odmowa / lista rezerwowa / jeszcze czekam.
6. Liczba punktów i próg, jeśli urząd je podał.
7. Powód odmowy (jeśli podano).
8. Zgoda na wykorzystanie wyniku w anonimowej statystyce i (osobno) na opinię z imieniem na stronie.

Zachęta do odpowiedzi: 50 zł rabatu na „rozliczenie dotacji” albo kod polecający (50 zł dla znajomego i 50 zł dla klienta). Przypomnienia: +7 i +21 dni.

**Arkusz „Skuteczność” (jeden wiersz = jedno zamówienie):**

| Kolumna | Przykład |
|---|---|
| ID zamówienia | 2027-0142 |
| PUP | PUP Legnica |
| Nabór (miesiąc/rok, źródło) | 02/2027, EFS+ |
| Branża (kategoria) | usługi beauty |
| Pakiet / dopłaty | Standard + listy intencyjne |
| Wnioskowana kwota | 45 000 zł |
| Złożono? | tak |
| Wezwanie? / kategoria | tak / kosztorys – używany sprzęt |
| Komisja? | nie |
| Decyzja / kwota | przyznano / 40 000 zł |
| Punkty / próg | 17 / 14 |
| Czas od złożenia do decyzji | 34 dni |
| Źródło informacji | ankieta / e-mail / telefon |

**Metryki (liczone co miesiąc):**
- Wskaźnik odpowiedzi na ankietę (cel ≥ 50%).
- **Skuteczność = przyznane / (przyznane + odmowy)** wśród wniosków złożonych i ze znanym wynikiem. Zawsze z liczbą przypadków (n) i okresem.
- Odsetek wezwań i ich kategorie: per urząd i per szablon.
- Średni czas decyzji per urząd (do komunikacji „w Twoim PUP decyzja trwa zwykle ok. X dni”).

**Zasady publikacji:** skuteczność ogólną pokazujemy na stronie dopiero przy n ≥ 50, a per urząd przy n ≥ 10. Formuła: „X z Y klientów, którzy podali wynik, otrzymało dotację (okres, n)”. Nie łączymy tego z wskaźnikami resortu i nie piszemy „97% skuteczności” bez metodologii.

**Pętla uczenia:** co miesiąc 3 najczęstsze kategorie wezwań i odmów, poprawki w szablonach i w checklistach, notatka w `szablony/CHANGELOG` (katalog prowadzi inny pracownik).

## 8. Minimalny stos narzędzi

### Ustalenia z weryfikacji płatności

| Pytanie | Odpowiedź | Źródło |
|---|---|---|
| Czy blok płatności Tally obsługuje BLIK? | **Nie.** Pomoc Tally opisuje wyłącznie płatności kartą („collect credit card payments”). Według zgłoszeń na tablicy feedbacku metody inne niż karta nie są dostępne w bloku płatności Tally | [tally.so/help/payment-forms](https://tally.so/help/payment-forms), [feedback: more payment options](https://tally.so/feedback/board/p/more-payment-options) |
| Czy Stripe obsługuje BLIK w Polsce? | **Tak.** Konta Stripe z PL mogą przyjmować BLIK (PLN, płatność jednorazowa, zwroty pełne i częściowe). BLIK działa w **Checkout i Payment Links** | [docs.stripe.com/payments/blik](https://docs.stripe.com/payments/blik) |
| Prowizja Stripe | BLIK: **1,6% + 1,00 zł**. Karty EOG: 1,5% + 1,00 zł (standardowe), 1,9% + 1,00 zł (premium) | [stripe.com/pl/pricing](https://stripe.com/pl/pricing) |
| Opłaty Tally za płatności | pomoc Tally: „We do not add any extra fees on top of Stripe’s pricing”. Część źródeł wtórnych podaje 5% prowizji Tally w planie darmowym **[do weryfikacji]**. Nie ma to znaczenia, jeśli płatność idzie przez Payment Link | [tally.so/help/payment-forms](https://tally.so/help/payment-forms) |
| Jak połączyć Tally z BLIK | Tally: przekierowanie po wysłaniu formularza („redirect on completion”) na **Stripe Payment Link** z parametrem `client_reference_id` (ID zgłoszenia, maks. 200 znaków, alfanumeryczne). Stripe zwraca go w webhooku `checkout.session.completed`. Czy Tally wstawia wartości pól do URL przekierowania, trzeba sprawdzić **[do weryfikacji]**. Wariant awaryjny: dopasowanie po e-mailu | [docs.stripe.com/payment-links/url-parameters](https://docs.stripe.com/payment-links/url-parameters), [tally.so/help/faq](https://tally.so/help/faq) |

### Rekomendowany stos (MVP)

| Funkcja | Narzędzie | Koszt | Uwagi |
|---|---|---|---|
| Kwestionariusz + upload | **Tally** (plan darmowy: nielimitowane formularze, upload plików, logika warunkowa; limit pliku wg źródeł wtórnych 10 MB) | 0 zł (Pro ok. 29 USD/mies.) | dane w UE, DPA akceptowane z regulaminem ([tally.so/help/gdpr](https://tally.so/help/gdpr)). Limit 10 MB i ceny Pro wg [jetadmin.io](https://www.jetadmin.io/blog/tally-pricing/) **[do weryfikacji na stronie Tally]** |
| Płatność BLIK + karta | **Stripe Payment Links** (jeden link na pakiet i jeden na każdą dopłatę) | 1,6% + 1 zł (BLIK) | zwroty z panelu |
| Alternatywa PL | **Tpay / Przelewy24 / Autopay**. Tpay ma w panelu zakładkę „Linki do płatności” ([landingi.com](https://landingi.com/pl/pomoc/integracja-tpay/)). Czy BLIK działa w ręcznie tworzonym linku, trzeba potwierdzić u operatora. Prowizje wg źródeł wtórnych: Tpay od ok. 1,59%, P24 przez Shopera 1,58% + 0,30–0,39 zł ([attomy.io](https://www.attomy.io/en/post/blik-shopify-a-comprehensive-guide-for-polish-online-shops), [shoper.pl](https://www.shoper.pl/przelewy24)) | % od transakcji | **[do weryfikacji: cennik dla JDG, BLIK w linkach bez sklepu]**. Zaleta: polski operator, polska obsługa. Wada: integracja z Tally ręczna |
| Awaryjnie | przelew tradycyjny na rachunek firmowy z numerem zamówienia w tytule | 0 zł | wolniejsze. Liczy się do zwolnienia z kasy (zob. `prawo/`) |
| Przechowywanie plików | **Google Workspace Business Starter** (Drive z DPA, konto firmowe, Gmail) albo Proton Drive | ok. 30–40 zł/mies. **[do weryfikacji ceny]** | folder per zamówienie, linki z wygasaniem, 2FA, usuwanie zgodnie z retencją |
| Generowanie DOCX/PDF | szablon DOCX ze zmiennymi (**docxtpl** w Pythonie albo **pandoc** z `reference.docx`), konwersja do PDF przez **LibreOffice headless** | 0 zł | DOCX jest ważniejszy niż PDF: klient przekleja treść do formularza urzędu (często w systemie praca.gov.pl) |
| Model językowy | API (Anthropic lub OpenAI), konto firmowe | wg zużycia (~kilka zł/plan) | DPA, retencja i anonimizacja: zob. `prawo/rodo-i-ai.md` |
| CRM | **Google Sheets** (zakładki: Zamówienia, Skuteczność, Baza PUP, Alerty) zasilany z Tally | 0 zł | widoki filtrowane po statusie, formatowanie warunkowe dla SLA (kolumna „termin” = opłacone + 48 h robocze) |
| Automatyzacje | **Make** (plan darmowy) albo Zapier | 0 zł na start | Stripe → arkusz, przypomnienia, ankiety |
| Rezerwacja telefonu (Premium) | Cal.com / Calendly (darmowy plan) | 0 zł | — |
| Faktury / rachunki | program do faktur (np. inFakt, Fakturownia, wFirma) | ok. 0–60 zł/mies. | KSeF dotyczy faktur B2B, faktury dla konsumentów są poza KSeF (zob. `prawo/`) |
| Newsletter / alerty | Sender (darmowo do 2 500 subskrybentów) / MailerLite (darmowo do 250) | 0 zł | zob. `marketing/alerty-naborow.md` |

**Łączny koszt stały MVP: ok. 50–250 zł/mies.** (bez księgowości).

### Przepływ danych (MVP)

```
Strona (cennik) → Tally (kwestionariusz + pliki + zgody)
      └─ przekierowanie → Stripe Payment Link (BLIK/karta, client_reference_id)
Tally → Google Sheets (CRM)      Stripe → (Make) → Google Sheets: status „Opłacone”
Właściciel: weryfikacja → skrypt (anonimizacja + API) → arkusz (kosztorys/prognoza) → DOCX/PDF
Gmail: wysyłka z linkiem do Drive (wygasa) → ankieta Tally po 60 dniach → arkusz „Skuteczność”
```
