# RODO i AI: przetwarzanie danych klientów

Stan na 14.10.2026. Materiał roboczy do konsultacji z prawnikiem lub IOD. Usługodawca (JDG) jest **administratorem** danych klientów. Narzędzia (Tally, Stripe, Google, dostawca AI, newsletter) są **podmiotami przetwarzającymi** albo, w części, odrębnymi administratorami.

## 1. Zasada naczelna: zbieramy tylko to, czego potrzebuje treść wniosku

Treść wniosku musi opisywać **pomysł, kwalifikacje, zakupy i rynek**. Do tego nie potrzeba danych identyfikacyjnych z formularza urzędu. Te klient wpisuje sam bezpośrednio w formularz PUP.

| Kategoria | Zbieramy? | Po co / uwagi |
|---|---|---|
| Imię, e-mail | ✔ | umowa, kontakt, wysyłka |
| Telefon | opcjonalnie (Premium: ✔) | konsultacja, pilne braki |
| PUP (nazwa) + powiat / gmina prowadzenia działalności | ✔ | dopasowanie formularza, lokalna konkurencja |
| **Dokładny adres zamieszkania / zameldowania** | ✘ | niepotrzebny. Klient wpisuje go sam w formularz urzędu |
| **PESEL, nr dowodu, data urodzenia** | ✘ | zamiast daty urodzenia pytanie zamknięte „Czy masz poniżej 30 lat?” (nabory „dla osób do 30 r.ż.”) |
| Status na rynku pracy (bezrobotny, poszukujący, opiekun itp.) | ✔ (pytanie zamknięte) | warunek kwalifikacji |
| Wykształcenie, kursy, doświadczenie | ✔ | opis kwalifikacji |
| Pomysł, branża, PKD, lokal, klienci, ceny | ✔ | treść wniosku |
| Lista zakupów z cenami, oferty (pliki) | ✔ | kosztorys. Prosimy o oferty **bez** danych osobowych sprzedawców prywatnych |
| Wkład własny, kwoty | ✔ | kosztorys, punktacja |
| Dane o zdrowiu / niepełnosprawności | ✘, wyjątkowo ✔ tylko ścieżka PFRON: pytanie „tak/nie” + stopień, **wyraźna zgoda** (art. 9 ust. 2 lit. a RODO), **nie trafia do promptu** | szczególna kategoria danych |
| Dane osób trzecich (poręczyciele, małżonek) | ✘ | — |
| Skany zaświadczeń z PUP, CV | ✘ (prosimy nie wysyłać) | jeśli klient je wgra: nie przetwarzamy, usuwamy i informujemy |
| Dane płatnicze (karta, BLIK) | ✘ (widzi je tylko Stripe) | my mamy tylko status płatności, kwotę, e-mail, ID |

**Kwestionariusz:** przy każdym polu tekstowym umieścić podpowiedź „Nie podawaj PESEL, adresu ani numeru dowodu”. Na górze formularza: klauzula informacyjna (skrót) + link do polityki prywatności.

## 2. Podstawy prawne

| Cel | Podstawa | Dane |
|---|---|---|
| Wykonanie umowy (przygotowanie Dokumentu, poprawki, gwarancja) | art. 6 ust. 1 lit. b RODO | kwestionariusz, pliki, korespondencja |
| Rozliczenia, księgowość, podatki | art. 6 ust. 1 lit. c RODO (ustawa o rachunkowości, ordynacja podatkowa) | imię, e-mail, kwota, data, dokument sprzedaży |
| Obrona przed roszczeniami, reklamacje | art. 6 ust. 1 lit. f RODO | dane zamówienia, korespondencja (bez pełnych treści, po okresie retencji plików) |
| Ankieta wyniku i statystyka skuteczności | art. 6 ust. 1 lit. f RODO (poprawa usługi). Publikacja anonimowej statystyki = dane zagregowane | wynik, PUP, branża, pakiet (pseudonim) |
| Opinia z imieniem na stronie | art. 6 ust. 1 lit. a RODO (zgoda) | imię, inicjał nazwiska, miasto, treść opinii |
| Alerty naborów / newsletter | zgoda (art. 6 ust. 1 lit. a RODO) + zgoda na informację handlową na podstawie art. 398 Prawa komunikacji elektronicznej ([ifirma.pl](https://www.ifirma.pl/blog/prawo-komunikacji-elektronicznej-juz-opublikowane-nowe-zasady-zgod-marketingowych-w-2024-roku/), [legeartis](https://czasopismo.legeartis.org/2024/08/przesylanie-informacji-handlowych-prawo-komunikacji-elektronicznej-uprzednia-zgoda-marketing-bezposredni/)) | e-mail, powiat/województwo, imię (opcjonalnie) |
| Niepełnosprawność (PFRON) | art. 9 ust. 2 lit. a RODO (wyraźna zgoda) | tak/nie, stopień |

## 3. Retencja (ile trzymamy)

| Dane | Okres | Jak usuwamy |
|---|---|---|
| Odpowiedzi w Tally i pliki wgrane przez klienta | do 30 dni (eksport do folderu zamówienia, potem usunięcie zgłoszenia w Tally) | ręcznie raz w tygodniu albo automatyczne usuwanie, jeśli dostępne w planie **[do weryfikacji: auto-usuwanie w Tally może wymagać wyższego planu]** |
| Folder zamówienia (kwestionariusz, pliki, Dokument, wersje) | **90 dni od dostarczenia** (pokrywa rundę poprawek i gwarancję po wezwaniu) | usunięcie folderu + kosza. Przypomnienie w kalendarzu „piątek: retencja” |
| Folder przy dopłacie „ponowne złożenie” / „rozliczenie” | do 12 mies. od zamówienia (cel: umowa) | j.w. |
| CRM: dane zamówienia bez treści (imię, e-mail, PUP, pakiet, daty, status, kwota) | **3 lata** od wykonania usługi (roszczenia) **[do weryfikacji z prawnikiem: przedawnienie dla tego typu umowy]** | usunięcie wiersza albo anonimizacja |
| Dokumenty księgowe i ewidencja płatności | **5 lat** od końca roku podatkowego | archiwum księgowe |
| Baza skuteczności | po 90 dniach tylko w formie pseudonimowej (ID zamówienia bez imienia i e-maila); po 3 latach dane wyłącznie zagregowane | arkusz „Skuteczność” bez kolumn identyfikujących |
| Lista alertów | do wycofania zgody. Dowód zgody (data, IP, tekst zgody, potwierdzenie double opt-in) przez 3 lata od wycofania **[do weryfikacji]** | narzędzie newsletterowe |
| Korespondencja e-mail | 1 rok od zamknięcia zamówienia (reklamacje można dochodzić później, ale dane zamówienia są w CRM) | etykieta w Gmailu + filtr retencji |
| Dane u dostawcy AI (API) | **Anthropic:** wejścia i wyjścia usuwane automatycznie w ciągu 30 dni. **OpenAI:** logi monitoringu nadużyć do 30 dni, stan aplikacji Responses API 30 dni (ustawiać `store=false`). Szczegóły w sekcji 5 | po stronie dostawcy |

## 4. Anonimizacja (pseudonimizacja) przed wysłaniem do modelu

Uczciwie: zastąpienie imienia tokenem to **pseudonimizacja**, a nie anonimizacja w rozumieniu RODO. Opis pomysłu + powiat + branża + wiek < 30 może w małym powiecie wskazywać na osobę. Dlatego mimo pseudonimizacji **potrzebna jest umowa powierzenia (DPA) z dostawcą AI**.

**Procedura (skrypt + kontrola ręczna, ok. 2 min):**
1. Do promptu trafiają **tylko pola merytoryczne** z kwestionariusza (pomysł, kwalifikacje, zakupy, rynek). Nigdy całe zgłoszenie ani wgrane pliki.
2. Skrypt podmienia: imię i nazwisko z pól formularza → `[KLIENT]`; e-mail, telefon, numery 11-cyfrowe (PESEL), NIP, IBAN, kody pocztowe, adresy (ulica + numer) → `[USUNIĘTO]`; nazwy wskazanych przez klienta firm prywatnych osób → `[FIRMA_1]`.
3. Miejscowość: zostawiamy **powiat lub miasto** (potrzebne do opisu rynku), usuwamy ulice i nazwy osiedli.
4. Kontrola ręczna podglądu promptu: wolne pola tekstowe (np. „opisz siebie”) bywają pełne danych.
5. Po wygenerowaniu skrypt odwraca tokeny lokalnie (`[KLIENT]` → imię) w Dokumencie.
6. Oferty, CV i zaświadczenia **nie** idą do modelu. Ceny z ofert przepisujemy do arkusza.
7. Dane o zdrowiu (PFRON) nigdy nie trafiają do promptu. Treść o niepełnosprawności, jeśli potrzebna, redaguje człowiek.

## 5. Dostawca AI: ustalenia z weryfikacji

| | **Anthropic (API Claude)** | **OpenAI (API)** |
|---|---|---|
| Trenowanie na danych | **nie**: „Anthropic may not train models on Customer Content from Services” ([Commercial Terms](https://www.anthropic.com/legal/commercial-terms)). Retained data „never used for model training without your express permission” ([API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention)) | **nie domyślnie**: „data sent to the OpenAI API is not used to train or improve OpenAI models” bez opt-in ([Your data](https://developers.openai.com/api/docs/guides/your-data)) |
| Domyślna retencja | wejścia i wyjścia usuwane automatycznie **w ciągu 30 dni** od otrzymania/wygenerowania ([polityka retencji – organizacje, stan 1.07.2026](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data)) | logi monitoringu nadużyć **do 30 dni**. Responses API: stan aplikacji **30 dni** domyślnie ([Your data](https://developers.openai.com/api/docs/guides/your-data)) |
| Wyjątki | treści oznaczone przez systemy trust & safety: **do 2 lat** (oceny klasyfikacji do 7 lat). Files API do usunięcia przez użytkownika. Część najnowszych modeli („Covered Models”) wymaga 30-dniowej retencji i nie jest objęta ZDR | dłużej, jeśli wymaga tego prawo lub ochrona przed szkodą |
| Zero Data Retention | dostępne w ramach uzgodnień (nie dla Batch, Files API, code execution i Covered Models) | po akceptacji OpenAI. Część endpointów niekwalifikowana |
| DPA | **tak**: DPA włączona do Commercial Terms przez odesłanie ([DPA](https://www.anthropic.com/legal/data-processing-addendum)). Konta konsumenckie (Free/Pro) DPA **nie mają**, więc **używać wyłącznie API / konta komercyjnego** | strona „Your data” nie opisuje DPA. OpenAI udostępnia DPA dla klientów API **[do weryfikacji: aktualny link i akceptacja w panelu]** |
| Lokalizacja / transfer | USA. W DPA standardowe klauzule umowne (SCC). Certyfikacja EU-US Data Privacy Framework według źródeł wtórnych ([companyscope.io](https://companyscope.io/vendors/anthropic)) **[do weryfikacji na dataprivacyframework.gov]** | USA. Rezydencja danych EOG (`eu.api.openai.com`) wymaga ZDR lub zmodyfikowanego monitoringu nadużyć |

**Rekomendacje:**
- Korzystać **wyłącznie z API na koncie organizacji (firmowym)**, nigdy z czatu konsumenckiego, i nie wklejać danych klientów do aplikacji czatowych.
- Nie używać Files API ani Batch API dla danych klientów (dłuższa retencja). Wystarczy zwykłe wywołanie Messages / Responses (`store=false`).
- W polityce prywatności wymienić dostawcę AI z nazwy jako odbiorcę danych, z informacją o transferze do USA i podstawie (DPF/SCC).
- Rozważyć wniosek o ZDR, gdy wolumen urośnie (u obu dostawców wymaga to uzgodnienia).

## 6. Polityka prywatności: punkty do treści

1. Administrator: dane firmy, kontakt w sprawach danych (e-mail).
2. Jakie dane zbieramy i skąd (kwestionariusz, płatność, e-mail, ankieta, newsletter) **oraz czego nie zbieramy** (PESEL, adres, nr dowodu).
3. Cele i podstawy prawne (tabela z sekcji 2).
4. Odbiorcy: Tally (formularze, UE), Stripe (płatności), Google (poczta, pliki), [dostawca AI] (generowanie treści, dane pseudonimizowane), narzędzie newsletterowe, Make (automatyzacje), biuro rachunkowe, program do faktur. Rola: podmioty przetwarzające albo odrębni administratorzy (Stripe w zakresie obowiązków regulacyjnych **[do weryfikacji]**).
5. Przekazywanie poza EOG: dostawca AI (USA), ewentualnie Google, Stripe. Podstawa: DPF albo SCC.
6. Informacja o użyciu AI: co trafia do modelu, pseudonimizacja, brak trenowania, retencja u dostawcy, weryfikacja przez człowieka. Brak zautomatyzowanego podejmowania decyzji wywołującego skutki prawne (art. 22 RODO): model nie decyduje o niczym, decyzje podejmuje urząd i klient.
7. Okresy przechowywania (tabela z sekcji 3).
8. Prawa: dostęp, sprostowanie, usunięcie, ograniczenie, przenoszenie, sprzeciw (lit. f), cofnięcie zgody, skarga do Prezesa UODO.
9. Dobrowolność: podanie danych jest dobrowolne, ale niezbędne do wykonania usługi.
10. Pliki cookies i analityka strony (osobny baner, jeśli analityka niebędąca niezbędną).
11. Bezpieczeństwo (skrót sekcji 7).
12. Data aktualizacji polityki.

## 7. Bezpieczeństwo plików

| Obszar | Minimum |
|---|---|
| Konta | 2FA (klucz lub aplikacja) na Google, Tally, Stripe, koncie AI, newsletterze, Make. Menedżer haseł. Osobne konto firmowe (nie prywatny Gmail) |
| Urządzenie | szyfrowanie dysku (FileVault / BitLocker), blokada ekranu, aktualizacje, brak pobierania plików klientów na urządzenia współdzielone |
| Pliki | folder per zamówienie (`2027-0142_PUP-Legnica`), dostęp tylko właściciela. Udostępnianie klientowi linkiem imiennym (konto Google klienta) albo linkiem z datą wygaśnięcia. Nigdy linki „każdy z linkiem” bez wygasania |
| Klucze API | w menedżerze sekretów lub zmiennych środowiskowych, nie w repozytorium ani w arkuszu. Osobny klucz dla produkcji, limity wydatków w panelu |
| Logi skryptów | bez treści promptów z danymi. Logujemy tylko ID zamówienia, czas i liczbę tokenów |
| Kopie zapasowe | szablony i baza PUP: kopia. Foldery klientów: bez dodatkowych kopii poza Drive (inaczej retencja jest nie do opanowania) |
| E-mail | dane klienta tylko w wątku zamówienia. Nie przesyłać plików klientów dalej (np. do partnerów) bez zgody |
| Naruszenia | procedura: ocena ryzyka → zgłoszenie do UODO w **72 h**, jeśli jest ryzyko dla osób (art. 33 RODO) → zawiadomienie osób przy wysokim ryzyku (art. 34) → wpis do rejestru naruszeń (zawsze, także niezgłaszanych) |

## 8. Rejestr czynności przetwarzania (art. 30 RODO)

Zwolnienie dla firm poniżej 250 pracowników **nie** obejmuje przetwarzania, które nie ma charakteru sporadycznego (art. 30 ust. 5 RODO). U nas przetwarzanie jest stałe, więc **rejestr jest obowiązkowy**. Prowadzić w arkuszu.

| Czynność | Cel | Kategorie osób | Kategorie danych | Odbiorcy | Transfer poza EOG | Retencja | Zabezpieczenia |
|---|---|---|---|---|---|---|---|
| Realizacja zamówień | wykonanie umowy | klienci | identyfikacyjne podstawowe, kontaktowe, zawodowe (kwalifikacje), opis działalności, finansowe (kwoty planu) | Tally, Google, dostawca AI, Make | tak (AI: USA; DPF/SCC) | 90 dni pliki / 3 lata CRM | 2FA, szyfrowanie, pseudonimizacja |
| Płatności i rozliczenia | obowiązek prawny | klienci | imię, e-mail, kwota, data, ID | Stripe, program do faktur, biuro rachunkowe | wg Stripe **[do weryfikacji]** | 5 lat od końca roku | 2FA |
| Ankieta wyników / statystyka | uzasadniony interes | klienci | wynik, PUP, branża | Tally, Google | nie | 90 dni identyfikowalnie, potem pseudonim | j.w. |
| Alerty / newsletter | zgoda | subskrybenci | e-mail, powiat, imię (opcj.) | narzędzie newsletterowe | wg narzędzia | do wycofania zgody | double opt-in, 2FA |
| Ścieżka PFRON (szczególne kategorie) | umowa + wyraźna zgoda | klienci z niepełnosprawnością | informacja o niepełnosprawności i stopniu | Google (nie AI) | nie | 90 dni | dostęp tylko właściciela |
| Opinie na stronie | zgoda | klienci | imię, inicjał, miasto, opinia | hosting strony | wg hostingu | do wycofania zgody | — |

Dodatkowo:
- **Umowy powierzenia (DPA):** zebrać i zarchiwizować PDF/zrzuty akceptacji od: Tally ([GDPR](https://tally.so/help/gdpr): dane w Europie, DPA akceptowana z regulaminem), Google Workspace, Anthropic/OpenAI, narzędzie newsletterowe, Make.
- **DPIA:** prawdopodobnie niewymagana (mała skala, brak profilowania i decyzji automatycznych), ale udokumentować krótką ocenę „dlaczego nie” **[do weryfikacji z IOD/prawnikiem]**.
- **IOD:** niewymagany (art. 37 RODO: brak przetwarzania na dużą skalę szczególnych kategorii jako głównej działalności).
