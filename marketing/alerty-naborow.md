# Darmowe alerty naborów: jak je zbudować

Stan na 14.10.2026. Cel: e-mail „Nabór w Twoim PUP” w dniu ogłoszenia, z linkiem do ogłoszenia i CTA do zamówienia. Sama informacja jest dostępna za darmo (Zielona Linia, agregatory), więc przewagą jest **szybkość, personalizacja per powiat i lista mailingowa**.

## 1. Źródła: co sprawdziłem

| Źródło | Czy publikuje nabory na działalność? | Forma techniczna | Ocena |
|---|---|---|---|
| **Zielona Linia** ([zielonalinia.gov.pl](https://zielonalinia.gov.pl/)), Centrum Informacyjno-Konsultacyjne Służb Zatrudnienia | **Tak.** Kategoria „Informacje z regionów”, wpisy typu „PUP Tuchola – Nabór wniosków o dofinansowanie podjęcia działalności gospodarczej” (14.10.2026), „PUP Legnica – …” (13.10.2026), „PUP Żory – …” (7.10.2026). W 2026 r. ok. 135 takich wpisów (I–X) | WordPress. **Publiczne REST API** działa: `https://zielonalinia.gov.pl/wp-json/wp/v2/posts?search=działalności&per_page=100&_fields=date,title,link`. Adres `/feed/` przekierowuje na stronę główną (RSS niedostępny w teście 14.10.2026) | **Źródło nr 1 do automatyzacji**, ale **niepełne**: obejmuje tylko część z 341 PUP i publikuje z opóźnieniem 0–3 dni po urzędzie (np. Zambrów: PUP 14.01, ZL 16.01.2026) |
| **Strony PUP** (`[nazwa].praca.gov.pl`) | **Tak**, to źródło pierwotne | Wszystkie PUP mają **jednolity szablon** na portalu praca.gov.pl. Aktualności są pod `https://[pup].praca.gov.pl/rynek-pracy/aktualnosci` (sprawdzone dla Legnicy, Katowic i Tucholi: tytuły w nagłówkach h2/h3, np. „NABÓR WNIOSKÓW O DOFINANSOWANIE PODJĘCIA DZIAŁALNOŚCI GOSPODARCZEJ”). `robots.txt` pozwala indeksować (`Allow: /`) | **Najlepsze źródło**: jeden parser dla wszystkich urzędów |
| **BIP PUP** | czasem (ogłoszenia, regulaminy) | różne systemy BIP | uzupełniająco, nie automatyzować na start |
| **praca.gov.pl** (portal centralny, e-usługi) | wnioski składa się elektronicznie przez praca.gov.pl. Czy portal centralny ma listę naborów, nie potwierdziłem **[do weryfikacji]** | — | — |
| **Profile FB urzędów** | często duplikują aktualności, czasem szybciej | brak API dla stron publicznych bez uprawnień | ręcznie: obserwować profile PUP z regionów MVP |
| Agregatory (konkurencja) | [Atlas Dotacji](https://atlasdotacji.pl/dotacje-z-urzedu-pracy) ma **RSS** `https://atlasdotacji.pl/feed/nabory.xml` (50 pozycji, różne programy, nie tylko PUP). [Biznesplany24](https://biznesplany24.pl/) publikuje listę naborów PUP | RSS / HTML | do **kontroli kompletności**, nie jako główne źródło (cudza praca, regulaminy serwisów) |

## 2. MVP ręczne: 2 województwa

**Skala:** w kraju działa 341 PUP ([MRPiPS, stan na koniec 2025](https://lesko.praca.gov.pl/documents/d/urzad-pracy/2025-zatrudnienie-w-urzedach-pracy)), średnio ok. 21 na województwo. W dużych województwach (mazowieckie, śląskie) jest ich więcej. Przyjmij **40–60 PUP dla 2 województw** **[policzyć dokładnie z list WUP]**.

**Codzienna rutyna (pon.–pt., rano):**

| Krok | Czas |
|---|---|
| Zielona Linia: zapytanie do API (zakładka w przeglądarce) i przejrzenie wpisów z ostatniej doby | 3 min |
| Strony aktualności 40–60 PUP (folder zakładek „Otwórz wszystkie”, szukanie słowa „nabór”) | 20–30 min |
| Sprawdzenie nowego ogłoszenia: termin, kwota, forma składania, link do regulaminu i formularza. Wpis do arkusza „Nabory” | 5 min na nabór |
| Wysyłka alertu do segmentu (powiat/województwo) z szablonu | 5–10 min na nabór |
| **Razem** | **ok. 30–45 min dziennie**, w szczycie (luty–kwiecień) do 60 min |

**Arkusz „Nabory”:** PUP | województwo | data ogłoszenia | termin od–do | „do wyczerpania środków”? | maks. kwota | forma (elektronicznie praca.gov.pl / papier) | grupa (np. do 30 r.ż., PFRON, EFS+) | link do ogłoszenia | link do regulaminu/formularza | wysłano alert (data, liczba odbiorców) | zamówienia z alertu.

Formularz i regulamin z każdego nowego naboru zapisujemy od razu w „Bazie PUP”. Przy okazji alertu baza formularzy rośnie sama.

## 3. Automatyzacja (od stycznia 2027 albo od razu, jeśli właściciel programuje)

**Etap 1 (1–2 dni pracy): skrypt dzienny**
1. Lista adresów `https://[pup].praca.gov.pl/rynek-pracy/aktualnosci` dla PUP z regionów MVP, potem z całej Polski.
2. Pobranie strony raz dziennie (rano, z przerwą 2–5 s między urzędami, własny User-Agent z adresem e-mail), wyciągnięcie tytułów i linków z nagłówków h2/h3.
3. Filtr: tytuł zawiera „nabór” i („działalności” | „dotacj” | „własny biznes” | „samozatrudn”). Osobny filtr dla PFRON i EFS+.
4. Porównanie z wczoraj (plik/arkusz z widzianymi linkami), nowe pozycje → e-mail do właściciela („do weryfikacji”).
5. Drugi strumień: API Zielonej Linii (`wp-json/wp/v2/posts?search=…&after=[wczoraj]`).
6. Właściciel weryfikuje (2–5 min na nabór) i jednym kliknięciem wysyła alert z szablonu.

```text
for pup in lista_pup:
    html = get(f"https://{pup}.praca.gov.pl/rynek-pracy/aktualnosci")
    for tytul, link in naglowki(html):
        if pasuje(tytul) and link not in widziane:
            nowe.append((pup, tytul, link)); widziane.add(link)
nowe += zielona_linia_api(search="działalności", after=wczoraj)
wyslij_do_wlasciciela(nowe)
```

Uruchamianie: cron na tanim VPS albo GitHub Actions (harmonogram) albo Make (moduł HTTP + parser tekstu). Koszt 0–20 zł/mies.

**Etap 2: monitoring zmian i pełna Polska**
- Wszystkie 341 urzędy (lista subdomen z WUP / sitemap praca.gov.pl).
- Wykrywanie **zmian** w istniejących ogłoszeniach (przedłużenie, zawieszenie „wyczerpanie środków”) przez hash treści strony ogłoszenia.
- Narzędzia bez kodu do monitorowania zmian stron (np. Distill, Visualping) nadają się do kilkunastu stron. Przy 341 urzędach wychodzi drogo, więc lepszy jest własny skrypt **[do weryfikacji limitów darmowych planów]**.
- Publiczna strona „Aktualne nabory PUP 2027” (SEO) generowana z arkusza.

**Zasady:** nie przeciążać serwerów (1 zapytanie na urząd dziennie), respektować `robots.txt`, linkować do źródła, nie kopiować całych ogłoszeń (krótki opis + link).

## 4. Narzędzie do newslettera (darmowy plan)

| Narzędzie | Darmowy plan | Uwagi |
|---|---|---|
| **Sender** | do **2 500 subskrybentów, 15 000 e-maili/mies.**, automatyzacje, formularze, landing pages. Branding Sendera ([sender.net/pricing](https://www.sender.net/pricing/)) | **rekomendacja na start**: duży limit, firma z UE (Litwa) **[do weryfikacji: lokalizacja danych i DPA]** |
| MailerLite | do **250 subskrybentów, 2 500 e-maili/mies.**, 3 aktywne automatyzacje, 3 formularze ([mailerlite.com/pricing](https://www.mailerlite.com/pricing)) | limit wyczerpie się szybko (źródła wtórne podawały wcześniej 500/1000, aktualna strona: 250) |
| Brevo | darmowy plan z dziennym limitem wysyłki ([brevo.com/pricing](https://www.brevo.com/pricing/)) | strona nie pokazała liczb **[do weryfikacji]** |

Wymagania: **double opt-in**, segmentacja po województwie/powiecie (pole lub tag), szablony, automatyzacja powitalna. Double opt-in jest standardem w tych narzędziach, ale dostępność w darmowym planie trzeba sprawdzić **[do weryfikacji]**.

## 5. Formularz zapisu i RODO

**Pola:** e-mail (wymagane), województwo (lista), powiat (lista zależna albo tekst), imię (opcjonalnie), „Czego szukasz?” (PUP / PFRON / LGD / pożyczka – opcjonalnie).

**Zgody (osobne, niezaznaczone domyślnie):**
> ☐ Chcę otrzymywać e-mailem bezpłatne alerty o naborach wniosków na dotacje na założenie firmy w wybranym regionie oraz informacje o usługach [nazwa] (informacja handlowa). Zgodę mogę wycofać w każdej chwili linkiem w e-mailu.

Podstawa: zgoda (art. 6 ust. 1 lit. a RODO) i zgoda na informację handlową drogą elektroniczną (art. 398 Prawa komunikacji elektronicznej, zob. [ifirma.pl](https://www.ifirma.pl/blog/prawo-komunikacji-elektronicznej-juz-opublikowane-nowe-zasady-zgod-marketingowych-w-2024-roku/)). Ponieważ alert zawiera CTA do płatnej usługi, zgoda musi obejmować **informację handlową**, nie tylko „alerty”.

**Pod formularzem (klauzula skrócona):** administrator, cel (alerty i informacja handlowa), podstawa (zgoda), odbiorca (narzędzie newsletterowe), okres (do wycofania zgody), prawa, link do polityki prywatności.

**Double opt-in:** e-mail „Potwierdź zapis” → kliknięcie → dopiero wtedy kontakt trafia na listę. Przechowujemy dowód: data i godzina zapisu, IP, treść zgody (wersja), data potwierdzenia. W każdym e-mailu link „wypisz się” (1 klik) i dane administratora. Kontakty niepotwierdzone usuwamy po 30 dniach.

## 6. Treść e-maila alertu (szablon)

**Temat:** `Nabór w PUP [Miasto]: dotacja na firmę do [kwota] zł – wnioski od [data]`
**Preheader:** `Termin: [od–do / do wyczerpania środków]. Co przygotować i jak zdążyć.`

> Cześć [Imię],
>
> **PUP w [Mieście] ogłosił nabór wniosków o dofinansowanie podjęcia działalności gospodarczej.**
>
> - **Termin:** [od – do] [⚠️ „do wyczerpania środków”: liczy się kolejność]
> - **Kwota:** do [kwota] zł [jeśli podana w ogłoszeniu]
> - **Dla kogo:** [osoby bezrobotne / do 30 r.ż. / osoby z niepełnosprawnością (PFRON)]
> - **Jak złożyć:** [elektronicznie przez praca.gov.pl / osobiście]
> - **Ogłoszenie i regulamin:** [link do strony urzędu]
>
> **Co przygotować już dziś:**
> 1. Listę zakupów z cenami (linki do ofert).
> 2. Dokumenty potwierdzające kwalifikacje (kursy, świadectwa pracy).
> 3. Pomysł na lokal i pierwszych klientów (np. listy intencyjne).
>
> **Nie masz czasu pisać?** Odpowiesz na pytania o swój pomysł, a w **48 h** dostaniesz gotowe treści do wniosku w układzie formularza PUP [Miasto], z kosztorysem. Jeśli urząd wezwie do poprawek, poprawimy je gratis.
>
> **[Przycisk: Zamów treści do wniosku – od 299 zł]**
>
> Nie wiesz, czy się kwalifikujesz? **[Sprawdź w 2 minuty]** (quiz)
>
> Powodzenia!
> [Imię], [nazwa usługi]
>
> *Alert ma charakter informacyjny. Wiążące są ogłoszenie i regulamin urzędu. Nie gwarantujemy przyznania dotacji.*
> *Otrzymujesz tę wiadomość, bo zapisałeś(-aś) się na alerty dla województwa [X]. [Wypisz się] · [Zmień region] · [Administrator danych: firma, adres, NIP]*

**Automatyzacje:**
- Powitanie po zapisie: „Jak działa dotacja z PUP w 3 krokach” + quiz + informacja, kiedy zwykle są nabory (zob. dane w `plan-startu-do-stycznia-2027.md`).
- Przypomnienie 3 dni przed końcem naboru (tylko dla segmentu tego powiatu, jeśli termin jest znany).
- Raz w miesiącu poza sezonem: „Co nowego”: PFRON, LGD, „Wsparcie w starcie”.

**Mierniki:** liczba zapisów na tydzień, open rate (cel > 40%: e-mail jest oczekiwany), CTR na CTA (cel > 5%), zamówienia z alertów (UTM `utm_source=alert&utm_campaign=[pup]`).
