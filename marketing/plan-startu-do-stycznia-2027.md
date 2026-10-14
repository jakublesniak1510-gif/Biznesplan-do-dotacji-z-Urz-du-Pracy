# Plan startu: 15.10.2026 → pierwsze nabory w styczniu 2027

Stan na 14.10.2026. Koncepcja zakładała 3 tygodnie. To za mało: same formularze 10–15 urzędów, regulamin z prawnikiem i ewentualna interpretacja VAT zajmują kilka tygodni. Plan obejmuje **9 tygodni pracy** (15.10–20.12) i bufor świąteczny. Zakładany czas właściciela: 25–30 h tygodniowo.

## 0. Kiedy naprawdę są nabory? (dane, nie założenia)

Policzyłem wpisy o naborach na podjęcie działalności gospodarczej opublikowane na [Zielonej Linii](https://zielonalinia.gov.pl/) w 2026 r. (przez jej publiczne API WordPress, tytuły zawierające „nabór” i „działalność”). To próbka, nie pełna lista: w Polsce działa **341 PUP** obsługujących 380 powiatów (MRPiPS, [„Zatrudnienie w urzędach pracy” – stan na koniec 2025 r.](https://lesko.praca.gov.pl/documents/d/urzad-pracy/2025-zatrudnienie-w-urzedach-pracy)).

| Miesiąc 2026 | I | II | III | IV | V | VI | VII | VIII | IX | X (do 14.10) |
|---|---|---|---|---|---|---|---|---|---|---|
| Wpisy o naborach | 4 | 14 | 12 | **21** | 12 | 19 | 12 | 8 | 19 | 9 |

Wnioski:
- **Styczeń jest cichy** (4 wpisy w 2026 r.: Mrągowo, Przasnysz, Legnica, Łuków). **Szczyt zaczyna się w lutym** i trwa do czerwca, z drugą falą we wrześniu. Kluczowe jest więc gotowość **od połowy stycznia**, a pełna moc w **lutym–kwietniu 2027**.
- **Nabory trwają też teraz** (październik 2026: m.in. Gorzów Wlkp., Tuchola, Legnica, Turek, Oborniki, Żory, Myszków-PFRON). To okazja, żeby 3 plany testowe zrobić dla **prawdziwych klientów** z tych naborów, za symboliczną opłatą w zamian za opinię i zgodę na studium przypadku.
- Część urzędów ogłasza nabory „do wyczerpania środków”. Alert w dniu publikacji daje realną przewagę klientowi i nam.

## 1. Kamienie milowe

| # | Kamień milowy | Termin |
|---|---|---|
| KM1 | Decyzje formalne: JDG, konsultacja podatkowa, wniosek o interpretację VAT (zob. `prawo/forma-prawna-i-obowiazki.md`) | 25.10.2026 |
| KM2 | **12–15 formularzy i regulaminów PUP** zebranych i zmapowanych (2 województwa) | 8.11.2026 |
| KM3 | Szablony v1 + model finansowy v1 + **3 plany testowe** dostarczone i ocenione | 22.11.2026 |
| KM4 | Strona, cennik, regulamin i polityka (po prawniku), płatności BLIK działają na produkcji, JDG zarejestrowana | 6.12.2026 |
| KM5 | Alerty naborów (MVP ręczne) działają, lista ma ≥ 100 zapisów, start marketingu | 13.12.2026 |
| KM6 | Gotowość operacyjna na sezon: 20 PUP w bazie, checklisty, limity mocy, 5 opinii | 15.01.2027 |

## 2. Harmonogram tygodniowy

| Tydz. | Daty | Zadania | Wynik |
|---|---|---|---|
| **0** | 15–18.10 | Wybór 2 województw MVP (kryteria: własny region + region z dużą liczbą naborów w danych Zielonej Linii). Lista wszystkich PUP w tych województwach (linki do stron *.praca.gov.pl). Założenie arkusza CRM i „Baza PUP” | lista ok. 40–60 urzędów (2 województwa) |
| **1** | 19–25.10 | Konsultacja z księgowym (VAT „doradztwo”, forma opodatkowania, PKD). **Wniosek o interpretację indywidualną** (40 zł). Konto Stripe (test), konto API (firmowe). Pobranie formularzy i regulaminów z 6–8 PUP | **KM1**. Pierwsze 8 formularzy |
| **2** | 26.10–1.11 | Pobranie kolejnych 6–7 formularzy (razem 12–15). Mapowanie pól (nazwy, limity znaków, wymagane załączniki), wykluczenia wydatków, kryteria oceny i punktacja. Notatka „co różni urzędy” | **KM2** (zapas do 8.11) |
| **3** | 2–8.11 | Kwestionariusz w Tally v1 (logika: PUP → pytania). Szablony promptów v1: 3 branże bazowe (usługi beauty, usługi budowlane/remontowe, usługi online/kreatywne). Szkic regulaminu i polityki prywatności do prawnika | kwestionariusz + szablony v1 |
| **4** | 9–15.11 | Model finansowy v1 (kosztorys, prognoza, kontrole sum). Skrypt: anonimizacja → generowanie → DOCX. **Plan testowy 1** (wewnętrzny, wymyślona persona) z pomiarem czasu każdego kroku | pierwszy DOCX end-to-end |
| **5** | 16–22.11 | **Plany testowe 2 i 3** dla prawdziwych osób z trwających naborów (np. przez grupy FB / znajomych), 49–99 zł albo za darmo w zamian za opinię i zgodę na anonimowe studium przypadku. Poprawki szablonów. Rejestracja JDG (jeśli testy płatne ponad limit nierejestrowanej: 10 813,50 zł/kw.) | **KM3**. Zmierzony czas na pakiet (porównać z `operacje/cennik-v2.md`) |
| **6** | 23–29.11 | Strona: główna, cennik, FAQ, „jak to działa”, 3 podstrony branżowe, stopka z danymi firmy. Teksty z `marketing/seo-i-tresci.md`. Konfiguracja Payment Links (BLIK) + przekierowanie z Tally. Regulamin po uwagach prawnika | strona na domenie (staging) |
| **7** | 30.11–6.12 | Płatności na produkcji (test BLIK za 1 zł). E-maile transakcyjne (potwierdzenie z regulaminem i oświadczeniami = trwały nośnik). Polityka prywatności, rejestr czynności, DPA zebrane. Quiz „Sprawdź, czy się kwalifikujesz” | **KM4** |
| **8** | 7–13.12 | Alerty MVP: lista PUP do monitorowania, formularz zapisu z double opt-in, szablon e-maila (zob. `marketing/alerty-naborow.md`). Start w grupach FB (pomoc, bez linków). 3 pierwsze nagrania TikTok/Reels. Lista 20 biur rachunkowych do kontaktu | **KM5** |
| **9** | 14–20.12 | Kontakt z 20 biurami rachunkowymi (oferta partnerska). Kolejne 5 PUP do bazy (cel: 20). Publikacja 2 artykułów SEO („Dotacja z PUP 2027 – kiedy nabory w [województwo]”, „Ile wynosi dotacja z PUP w 2027”). Nagrania na zapas na święta | partnerzy w toku, treści na zapas |
| bufor | 21.12–3.01 | Święta. Tylko alerty (jeśli coś się pojawi) i odpowiedzi w grupach. Aktualizacja kwot na 2027: płaca minimalna, przeciętne wynagrodzenie (maks. dotacja = 6 × przeciętne wynagrodzenie) | — |
| **10–11** | 4–17.01.2027 | Pierwsze nabory: obsługa pierwszych zamówień, codzienne alerty, retargeting zapisanych na listę („nabór w Twoim powiecie”). Dokładanie PUP do bazy na żądanie | **KM6** |
| luty–kwiecień | — | Szczyt sezonu: limit 6 planów dziennie, priorytet SLA, ankiety wyników od klientów z października–listopada | — |

**Ryzyka harmonogramu:**

| Ryzyko | Wpływ | Mitygacja |
|---|---|---|
| Brak odpowiedzi na interpretację VAT przed sezonem (do 3 mies.) | decyzja o VAT w ciemno | startujemy jako czynny podatnik VAT albo ze zwolnieniem po opinii doradcy (zob. `prawo/`) |
| Urzędy publikują nowe formularze 2027 dopiero w styczniu | szablony z 2026 mogą się zdezaktualizować | mapujemy formularze 2026, a w styczniu robimy szybką aktualizację (~15 min/urząd, jeśli zmiany są kosmetyczne) |
| Prawnik nie zdąży z regulaminem | brak legalnej sprzedaży konsumentom | zlecić w tyg. 3, termin oddania do 30.11 |
| Testy pokażą, że weryfikacja trwa 2× dłużej | stawka godzinowa spada | podnieść ceny przed startem albo uprościć Podstawowy |

## 3. Przychody poza sezonem: inne programy, do których pasują te same szablony

| Program | Aktualny w 2026? | Opis | Co dopasować w szablonach |
|---|---|---|---|
| **Pożyczka „Pierwszy biznes – Wsparcie w starcie”** (BGK, Fundusz Pracy / EFS+) | **tak, ale nabory wstrzymywane**: według PFP nabór zawieszono 30.03.2026 z powodu wyczerpania alokacji. Wznowienie ogłoszą na stronie i w social mediach ([pfp.com.pl](https://www.pfp.com.pl/pozyczki/wsparcie-w-starcie/)). W innych makroregionach nabory zamykano m.in. 13.08.2026 **[do weryfikacji per region]** | Preferencyjna pożyczka na start firmy: do ok. **184 662,60 zł** (od 1.09.2026, 20-krotność przeciętnego wynagrodzenia), **0,25%** rocznie, spłata do 7 lat, karencja do 12 mies. Możliwe jednorazowe umorzenie do 50% pożyczki (maks. 6-krotność przeciętnego wynagrodzenia). Grupy docelowe są szersze niż w PUP: m.in. studenci ostatniego roku, osoby niezatrudnione, osoby o niskich dochodach ([pfp.com.pl](https://www.pfp.com.pl/pozyczki/wsparcie-w-starcie/), [ifirma.pl](https://www.ifirma.pl/blog/wsparcie-w-starcie-2026-na-czym-polega-program-dla-zakladajacych-pierwszy-biznes/)) | biznesplan z oceną zdolności spłaty (rata w prognozie), wyższe kwoty. Konkurencja: Biznesplany24 bierze 1 400–1 900 zł |
| **Premia LGD na podjęcie działalności pozarolniczej** (PS WPR 2023–2027, LEADER/RLKS, interwencja I.13.1; dawniej PROW) | **tak**: nabory ogłasza każda LGD w swoim harmonogramie, np. LGD „Zielony Wierzchołek Śląska” nabór 1/2026: 6–20.02.2026 ([lipie.pl – ogłoszenie](https://lipie.pl/sites/default/files/2026-01/Og%C5%82oszenie%20o%20naborze%201-2026%20-%20do%20gmin%20na%20tablic%C4%99-1.pdf)) | Premia (ryczałt) dla osób zakładających firmę na obszarach wiejskich LGD. Kwoty ustala lokalna strategia (LSR), w źródłach do ok. 150 tys. zł ([money.pl](https://www.money.pl/gospodarka/wlasna-firma-w-2026-r-skad-wziac-pieniadze-na-biznes-7294410912119264a.html)) **[do weryfikacji per LGD]**. Wniosek i biznesplan na formularzach ARiMR, operacja do 2 lat od umowy | inny formularz (ARiMR), wskaźniki LSR (np. utworzone miejsca pracy), kryteria lokalne. Dopłata „inny program” albo osobny pakiet LGD (wyższa cena, dłuższy dokument) |
| **Środki PFRON na podjęcie działalności dla osób z niepełnosprawnością** (art. 12a ustawy o rehabilitacji, przez PUP) | **tak**: zasady na 2026 publikują PUP-y, np. [Bydgoszcz](https://bydgoszcz.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-bydgoszczy/zasady_przyznawania_srodkow_dot_pfron_2026), [Oborniki](https://oborniki.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-obornikach/zasady-dotacje-pfron-2026). Nabór PUP Myszków-PFRON w październiku 2026 ([Zielona Linia](https://zielonalinia.gov.pl/pup-myszkow-ii-nabor-wnioskow-dotacja-na-podjecie-dzialalnosci-gospodarczej-pfron/)) | Jednorazowe środki dla bezrobotnych lub poszukujących pracy osób z niepełnosprawnością: ustawowo do 6× przeciętnego wynagrodzenia (zobowiązanie na 12 mies.) albo 6–15× (24 mies.). Urzędy ustalają niższe limity, np. Bydgoszcz maks. 35 000 zł w 2026 r., Słupsk do 30 000 zł ([lexlege – art. 12a](https://lexlege.pl/ustawa-o-rehabilitacji-zawodowej-i-spolecznej-oraz-zatrudnianiu-osob-niepelnosprawnych/art-12a/)) | prawie identyczny wniosek jak PUP. Dane o zdrowiu: wyraźna zgoda, poza promptem (zob. `prawo/rodo-i-ai.md`). Komunikacja: dostępność strony |
| **Dotacje EFS+ (projekty PUP i operatorów zewnętrznych)** | **tak, regionalnie**: np. PUP Legnica (FE dla Dolnego Śląska, średnio ok. 28 000 zł, nabór do 30.09.2026), PUP Zawiercie „Własny biznes z EFS+” (do 30 000 zł, marzec 2026) ([Zielona Linia – Legnica](https://zielonalinia.gov.pl/pup-legnica-nabor-na-przyznania-srodkow-na-podjecie-dzialalnosci-gospodarczej/), [Zielona Linia – Zawiercie](https://zielonalinia.gov.pl/pup-zawiercie-wlasny-biznes-z-efs-nabor-wnioskow/)). Projekty operatorów (fundacje, agencje rozwoju) z dotacją i wsparciem pomostowym zależą od konkursów programów regionalnych FE 2021–2027 **[do weryfikacji, które regiony mają nabory uczestników w 2027]** | Środki EFS+ na start firmy: przez PUP (te same zasady co dotacja PUP) albo w projektach, gdzie operator rekrutuje uczestników, szkoli i ocenia biznesplany | formularze operatorów (biznesplan + rekrutacja). Alerty: śledzić także operatorów w regionach MVP |
| *Bonus:* refundacja kosztów wyposażenia stanowiska pracy (dla pracodawców, PUP) | tak, nabory w PUP (np. [PUP Opatów, EFS](https://opatow.praca.gov.pl/documents/d/powiatowy-urzad-pracy-w-opatowie/ogloszenie-na-strone-doposazenie-efs-pdf)) | Pracodawca dostaje refundację za utworzenie stanowiska dla bezrobotnego. Podobna struktura wniosku (opis, kosztorys) | kanał B2B przez biura rachunkowe. Zweryfikować popyt **[do weryfikacji]** |

**Kalendarz przychodów (hipoteza):**

| Okres | Główne źródło |
|---|---|
| styczeń–czerwiec | dotacje PUP (szczyt luty–kwiecień), PFRON, LGD (nabory wiosenne) |
| lipiec–sierpień | „rozliczenie dotacji” dla klientów z wiosny, „Wsparcie w starcie” (jeśli nabór otwarty), EFS+ operatorów |
| wrzesień–listopad | druga fala naborów PUP, ponowne złożenia po odmowach |
| grudzień | przygotowanie bazy na nowy rok, zapisy na alerty |
