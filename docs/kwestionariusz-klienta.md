# Kwestionariusz klienta (wersja 2, 14.10.2026)

Formularz, który klient wypełnia na stronie po zakupie pakietu. Zebrane odpowiedzi wystarczają do wypełnienia wszystkich pól merytorycznych wniosku PUP (lista pól: [rozporządzenie MRPiPS z 21.11.2025, § 2 ust. 3](https://api.sejm.gov.pl/eli/acts/DU/2025/1645/text.pdf)) i do zdobycia punktów w typowej karcie oceny (zob. `docs/jak-dziala-dotacja-2026.md`, rozdz. 10).

## Zasady formularza

| Oznaczenie | Znaczenie |
|---|---|
| **[O]** | pole obowiązkowe, bez niego nie zaczynamy pracy |
| [Z] | zalecane, wpływa na punkty albo jakość |
| [P] | plik (upload: PDF, JPG, PNG, DOCX, maks. 10 MB) |
| 💡 | po co pytamy (tekst pomocniczy widoczny pod polem) |

**Czego NIE zbieramy** (minimalizacja danych, RODO). Klient wpisze to sam w formularzu urzędu:
- PESEL, seria i numer dowodu,
- adres zamieszkania i adres do doręczeń,
- dane poręczycieli (imiona, PESEL, dochody co do złotówki, numery dokumentów),
- numer rachunku bankowego,
- informacje o karalności (wystarczy deklaracja „spełniam warunki”, pkt 1.6),
- dane o zdrowiu ponad informację „mam orzeczenie o niepełnosprawności: tak/nie” (tylko gdy daje punkty lub warunkuje nabór).

> Komunikat na górze formularza: *„Wpisuj tylko prawdę. Wniosek podpisujesz Ty, a część oświadczeń składasz pod rygorem odpowiedzialności karnej. Nie wymyślamy doświadczenia, klientów ani cen. Jeśli czegoś nie masz, napisz »nie mam«. Pomożemy to uczciwie opisać.”*

Szacowany czas wypełnienia: 40–60 min. Można zapisać wersję roboczą i wrócić.

---

## Sekcja 0. Kontakt i zamówienie

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 0.1 | Imię (może być samo imię) **[O]** | tekst | Do kontaktu. Nazwiska nie potrzebujemy |
| 0.2 | E-mail **[O]** | e-mail | Tu wyślemy gotowe treści |
| 0.3 | Telefon [Z] | tel. | Do szybkich pytań, gdy czegoś brakuje. Skraca czas realizacji |
| 0.4 | Pakiet: Podstawowy / Standard / Premium **[O]** | wybór | Zakres prac |
| 0.5 | Do kiedy musisz złożyć wniosek? **[O]** | data | Planujemy kolejkę. Nabory trwają często 1–2 dni |

## Sekcja 1. Urząd i nabór

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 1.1 | Nazwa powiatowego urzędu pracy **[O]** | lista + tekst | Wniosek składa się do PUP właściwego dla **miejsca zamieszkania**. Każdy urząd ma inny formularz i regulamin |
| 1.2 | Link do ogłoszenia o naborze **[O]** (jeśli nabór jeszcze nie ogłoszony: „brak, nabór planowany”) | URL | Z ogłoszenia bierzemy kwotę maksymalną, termin i źródło finansowania |
| 1.3 | Link do regulaminu lub zasad przyznawania **[O]** albo plik [P] | URL / plik | Regulamin wyznacza wykluczenia, limity procentowe w kosztorysie i kartę oceny. Bez niego plan może być niezgodny z zasadami |
| 1.4 | Formularz wniosku z urzędu (DOC/DOCX/PDF) **[O]** [P] | plik | Piszemy treści dokładnie pod pola i limity znaków tego formularza |
| 1.5 | Karta oceny / kryteria punktowe, jeśli urząd je publikuje [Z] [P] | plik / URL | Celujemy w punktowane elementy |
| 1.6 | Potwierdzam, że spełniam warunki z ustawy: (a) jestem zarejestrowany(-a) jako bezrobotny(-a) **albo** absolwent CIS/KIS **albo** opiekun osoby niepełnosprawnej poszukujący pracy; (b) w ostatnich 12 mies. nie prowadziłem(-am) firmy w Polsce i nie miałem(-am) jej zawieszonej; (c) nie prowadzę firmy za granicą; (d) nigdy nie dostałem(-am) bezzwrotnej dotacji na start firmy ani na spółdzielnię socjalną; (e) nie korzystałem(-am) z umorzenia pożyczki z art. 187; (f) w ostatnich 12 mies. nie przerwałem(-am) z własnej winy stażu, szkolenia itp.; (g) nie złożyłem(-am) wniosku w innym PUP; (h) w ostatnich 2 latach nie byłem(-am) skazany(-a) za przestępstwa gospodarcze, skarbowe lub przeciw dokumentom **[O]** | checkbox: „spełniam wszystkie” / „nie jestem pewien – pkt …” | Bez tych warunków wniosek przepada, a pieniądze klienta poszłyby na marne ([ustawa art. 148](https://api.sejm.gov.pl/eli/acts/DU/2025/620/text.pdf)). Przy „nie jestem pewien” kontaktujemy się przed rozpoczęciem pracy |
| 1.7 | Status: bezrobotny / absolwent CIS / absolwent KIS / opiekun osoby niepełnosprawnej **[O]** | wybór | Inny zestaw oświadczeń we wniosku |
| 1.8 | Od kiedy jesteś zarejestrowany(-a) w PUP? (miesiąc/rok) [Z] | data | Ponad 12 mies. w ciągu 2 lat oznacza długotrwale bezrobotnego: pierwszeństwo i punkty |
| 1.9 | Czy w Indywidualnym Planie Działania (IPD) masz wpisaną dotację na firmę? tak / nie / nie wiem [Z] | wybór | Niektóre urzędy tego wymagają (np. Kolbuszowa). Jeśli nie, warto poprosić doradcę o aktualizację IPD przed naborem |
| 1.10 | Czy należysz do którejś grupy? do 30 lat / powyżej 50 lat / powyżej 55 lat / długotrwale bezrobotny / bez kwalifikacji zawodowych / z orzeczeniem o niepełnosprawności / samotnie wychowuję dziecko / Karta Dużej Rodziny / kobieta / niskie kwalifikacje (wykształcenie co najwyżej policealne) / żadna **[O]** | wielokrotny wybór | Grupy z art. 69 ustawy dają pierwszeństwo i punkty, a projekty EFS+ mają własne grupy docelowe. To decyduje, do którego naboru pasujesz |
| 1.11 | Źródło finansowania naboru, jeśli wiesz: Fundusz Pracy / EFS+ (projekt …) / PFRON / nie wiem [Z] | wybór + tekst | EFS+ ma dodatkowe kryteria i często inne limity |
| 1.12 | Kwota, o którą chcesz wnioskować (zł) **[O]** | liczba | Nie może przekroczyć maksimum z ogłoszenia. Kosztorys budujemy co do złotówki |
| 1.13 | Czy już kiedyś składałeś(-aś) wniosek o dotację i dostałeś(-aś) odmowę? Jeśli tak, z jakim uzasadnieniem? [Z] | tekst / plik | Uzasadnienie odmowy to najlepsza wskazówka, co poprawić |

## Sekcja 2. Zabezpieczenie zwrotu (pytamy na początku!)

> 💡 *Każda umowa z PUP wymaga zabezpieczenia ([ustawa art. 150](https://api.sejm.gov.pl/eli/acts/DU/2025/620/text.pdf)). Najczęściej są to dwie osoby poręczające z dochodem ok. 4–5 tys. zł netto. Jeśli nie masz zabezpieczenia, urząd nie podpisze umowy nawet po pozytywnej ocenie. Lepiej to wiedzieć teraz.*

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 2.1 | Jaką formę zabezpieczenia planujesz? poręczenie / weksel z poręczeniem (aval) / blokada środków na koncie / gwarancja bankowa / akt notarialny + inna forma / zastaw rejestrowy / nie wiem **[O]** | wielokrotny wybór | Forma bywa punktowana (np. Grodzisk Maz.: poręczenie 3 pkt, akt notarialny 0) i musi być w treści wniosku |
| 2.2 | Ile osób mogłoby za Ciebie poręczyć? 0 / 1 / 2 / 3+ **[O]** | wybór | Większość urzędów wymaga 2 poręczycieli |
| 2.3 | Dla każdego potencjalnego poręczyciela (bez danych osobowych!): relacja (np. ojciec, siostra, znajomy) · źródło dochodu (umowa o pracę na czas nieokreślony / określony do … / emerytura / renta do … / własna firma: ryczałt czy zasady ogólne / inne) · dochód netto **w przedziale** (< 3 500 / 3 500–4 000 / 4 000–4 500 / 4 500–5 500 / > 5 500 zł) · czy ma kredyty lub raty: tak / nie · wiek: < 70 / 70–75 / > 75 · czy ma współmałżonka, który się zgodzi: tak / nie / bez małżonka **[O, jeśli 2.2 ≥ 1]** | powtarzalny blok | Porównujemy z wymogami regulaminu (próg dochodu, wiek, forma zatrudnienia, zakaz ryczałtowców) i od razu mówimy, czy to wystarczy |
| 2.4 | Czy jesteś w związku małżeńskim? tak – wspólność majątkowa / tak – rozdzielność / nie **[O]** | wybór | Małżonek we wspólności nie może poręczać, a zwykle musi wyrazić zgodę na umowę |
| 2.5 | Czy masz oszczędności lub nieruchomość, które mogłyby posłużyć jako zabezpieczenie? brak / oszczędności ≥ 125% kwoty / nieruchomość / samochód lub maszyna / inne [Z] | wybór | Alternatywy dla poręczenia (blokada, akt notarialny, zastaw) |

**Reguła operacyjna:** jeśli 2.2 = 0 i 2.5 = „brak”, przed przyjęciem zlecenia wysyłamy klientowi informację o ryzyku i proponujemy wstrzymanie (zob. FAQ).

## Sekcja 3. Pomysł na działalność

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 3.1 | Opisz w 3–5 zdaniach, czym będzie zajmować się firma, co sprzedajesz, komu i gdzie **[O]** | tekst (min. 300 znaków) | Podstawa sekcji „opis planowanej działalności” |
| 3.2 | Lista usług lub produktów z ceną, którą planujesz brać (np. „strzyżenie męskie – 50 zł”) **[O]** | tabela: usługa · cena · jednostka · szacowana liczba miesięcznie | Z tego liczymy przychody. Komisje sprawdzają realność cen |
| 3.3 | Kod PKD, jeśli znasz (np. 96.21.Z). Jeśli nie, zostaw puste, dobierzemy [Z] | tekst | Wniosek wymaga **podklasy PKD**. Sprawdzamy też wykluczenia z regulaminu i de minimis |
| 3.4 | Czy działalność wymaga uprawnień, licencji, zezwoleń, koncesji lub wpisu do rejestru (np. sanepid, licencja przewoźnika, uprawnienia SEP, wpis do rejestru działalności regulowanej)? Które już masz? **[O]** | tekst + [P] | Wniosek wymaga tej informacji. Brak uprawnień do kluczowego sprzętu może wykluczyć zakup |
| 3.5 | Czy działalność jest sezonowa? nie / częściowo (opisz miesiące) / tak **[O]** | wybór + tekst | Część urzędów wyklucza działalność sezonową. Sezonowość musi też być widoczna w prognozie miesięcznej |
| 3.6 | Planowana data rozpoczęcia działalności (miesiąc) [Z] | data | Firmę rejestruje się dopiero **po** umowie i wypłacie (do 30 dni od otrzymania środków). Wcześniejsza rejestracja oznacza utratę dotacji |
| 3.7 | Czy ktoś z Twojej rodziny prowadzi lub prowadził taką samą działalność? Czy przejmujesz po kimś firmę, klientów lub sprzęt? **[O]** | tekst | Częste wykluczenie: przejęcie działalności po członku rodziny, ten sam profil w tym samym miejscu |
| 3.8 | Dlaczego właśnie ta działalność? Skąd pomysł, co Cię do niej przygotowało? [Z] | tekst | Uzasadnienie wyboru jest oceniane („pomysł, realność powodzenia”) |

## Sekcja 4. Forma prawna i podatki

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 4.1 | Forma: jednoosobowa działalność gospodarcza (standard) / inna **[O]** | wybór | Niektóre urzędy finansują wyłącznie JDG |
| 4.2 | Forma opodatkowania: skala / liniowy / ryczałt (stawka, jeśli znasz) / nie wiem [Z] | wybór | Wpływa na koszty w prognozie (podatek, składka zdrowotna). Przy „nie wiem” przyjmiemy do prognozy wariant ostrożny i to oznaczymy. Nie doradzamy podatkowo, decyzję podejmujesz Ty lub Twoja księgowa |
| 4.3 | VAT: zwolnienie podmiotowe (do limitu obrotu) / czynny VAT od startu / nie wiem [Z] | wybór | Przy czynnym VAT trzeba zwrócić urzędowi VAT od zakupów (art. 152). Planujemy kwoty brutto i netto |
| 4.4 | ZUS: ulga na start, potem preferencyjny / od razu pełny / nie wiem [Z] | wybór | Koszty stałe w prognozie |
| 4.5 | Kto prowadzi księgowość? sam(-a) / biuro rachunkowe (koszt mies.) / nie wiem [Z] | wybór + kwota | Koszt w prognozie |

## Sekcja 5. Miejsce prowadzenia działalności

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 5.1 | Gdzie będziesz pracować? własny lokal / wynajem / użyczenie (np. od rodziny) / w mieszkaniu (wydzielone pomieszczenie) / mobilnie u klienta / online **[O]** | wybór | Wniosek wymaga adresu i **opisu lokalu**, a przy działalności mobilnej adresu przechowywania sprzętu |
| 5.2 | Miejscowość i ulica lokalu (bez numeru mieszkania, jeśli to Twój dom) **[O]** | tekst | Lokalizacja jest punktowana (dostępność, ruch, parking). Konkretna ulica zamiast „w centrum” |
| 5.3 | Opis lokalu: metraż, liczba pomieszczeń, piętro, witryna, parking, dojazd, media, stan techniczny, co trzeba dostosować **[O]** (jeśli nie mobilnie) | tekst | Pole „opis lokalu”. Możliwa wizja lokalna urzędu, więc opis musi się zgadzać z rzeczywistością |
| 5.4 | Czy masz dokument do lokalu (akt własności, umowa najmu lub użyczenia, list intencyjny wynajmującego)? tak / w trakcie / nie **[O]** + [P] | wybór + plik | Posiadanie lokalu bywa punktowane (np. 1 pkt), a część urzędów wymaga dokumentu najpóźniej przy umowie |
| 5.5 | Czynsz miesięczny i opłaty (zł) [Z] | liczba | Koszty stałe. Czynszu **nie można** opłacić z dotacji |
| 5.6 | Zdjęcia lokalu (2–5) [Z] [P] | pliki | Do konkretnego opisu. Nie trafiają do wniosku |
| 5.7 | Dla działalności mobilnej: obszar działania (gminy, promień km), czym dojeżdżasz, prawo jazdy (kategoria), gdzie przechowujesz sprzęt **[O, jeśli mobilnie]** | tekst | Kryterium „przygotowanie do działalności mobilnej” w kartach oceny |

## Sekcja 6. Kwalifikacje i doświadczenie (tylko prawdziwe, z dokumentami)

> 💡 *To zwykle najwyżej punktowana część (np. Turek: do 10 pkt z 31, Mińsk Maz.: 30 z 55). Liczy się tylko to, co możesz udokumentować.*

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 6.1 | Wykształcenie: poziom, szkoła lub uczelnia, kierunek, rok ukończenia **[O]** | tabela | „Wykształcenie kierunkowe” jest punktowane |
| 6.2 | Kursy, szkolenia, certyfikaty, uprawnienia związane z działalnością: nazwa, organizator, rok, liczba godzin **[O]** (lub „brak”) | tabela + [P] | Każdy udokumentowany kurs to punkty |
| 6.3 | Doświadczenie zawodowe: pracodawca (lub „firma z branży X” przy prośbie o anonimowość), stanowisko, od–do, główne obowiązki związane z planowaną działalnością **[O]** | tabela | Punkty za lata doświadczenia w branży (np. Grodzisk: 1 rok = 1 pkt, ponad 3 lata = 3 pkt) |
| 6.4 | Dokumenty potwierdzające: świadectwa pracy, umowy, referencje, zaświadczenia, dyplomy, portfolio [Z] [P] | pliki | Dokument podnosi wiarygodność i punktację. Bez dokumentu doświadczenie może nie zostać uznane |
| 6.5 | Doświadczenie nieformalne (praca za granicą, dorywcza, hobby, wolontariat) z dowodem: zdjęcia prac, opinie, portfolio [Z] | tekst + [P] | Opisujemy uczciwie jako „umiejętności”, nie jako staż pracy |
| 6.6 | Czy byłeś(-aś) na szkoleniu lub spotkaniu PUP dla przyszłych przedsiębiorców albo u doradcy zawodowego? [Z] | tak/nie + data | Bywa punktowane (np. Nowa Sól: 1 pkt) |
| 6.7 | Inne umiejętności przydatne w firmie (obsługa programów, języki, sprzedaż, social media) [Z] | tekst | Uzupełnienie sekcji „umiejętności” |

## Sekcja 7. Klienci i rynek lokalny

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 7.1 | Kim są Twoi klienci? (np. mieszkańcy gminy X 30–60 lat, firmy budowlane z powiatu, turyści) **[O]** | tekst | Analiza rynku jest punktowana (klienci, potrzeby) |
| 7.2 | Obszar działania: miejscowość, gmina, powiat, promień km, online w całej Polsce **[O]** | tekst | Określa wielkość rynku |
| 7.3 | Skąd wiesz, że jest popyt? Fakty: kolejki u konkurencji, pytania znajomych, brak usługi w okolicy, nowe osiedle, dane z gminy **[O]** | tekst | Komisje oceniają „zapotrzebowanie na rynku”. Konkret zamiast ogólników |
| 7.4 | Jak zdobędziesz pierwszych klientów? (Google Maps, Facebook, ulotki, współpraca z X, polecenia) **[O]** | tekst | Kryterium „strategia zdobycia rynku”, „metody promocji” |
| 7.5 | Czy masz już osoby lub firmy zainteresowane współpracą? Ile i jakie? **[O]** | tekst | Podstawa do listów intencyjnych (sekcja 11) |

## Sekcja 8. Konkurencja

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 8.1 | Wymień 3–5 konkurentów: nazwa, miejscowość lub ulica, link (www, Facebook, Google Maps), orientacyjne ceny, co robią dobrze lub słabo **[O]** (min. 3) | tabela | „Analiza konkurencji, sposoby konkurowania” to stały element kart oceny. Prawdziwe nazwy eliminują generyczny tekst |
| 8.2 | Czym się wyróżnisz? (cena, godziny, dojazd, specjalizacja, jakość, szybkość) **[O]** | tekst | Kryterium „plany wyróżnienia oferty” |
| 8.3 | Największe ryzyka dla firmy i jak sobie z nimi poradzisz (np. choroba, nowa konkurencja, sezon) [Z] | tekst | Analiza SWOT i ryzyk jest punktowana osobno w wielu kartach |

## Sekcja 9. Lista zakupów z dotacji (kosztorys)

> 💡 *Każda pozycja musi mieć ofertę (link, screen lub PDF). Urzędy odrzucają pozycje bez ofert i tną ceny zawyżone. Kupujesz dopiero **po** podpisaniu umowy. Wcześniejsze zakupy nie zostaną rozliczone.*

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 9.1 | Tabela zakupów **[O]**: nazwa i model · ilość · cena brutto za sztukę · nowy / używany · sprzedawca (sklep, firma) · link do oferty · do czego służy w firmie (1 zdanie) | tabela (min. 1 wiersz) | „Szczegółowa specyfikacja wydatków” z uzasadnieniem. Sprawdzamy limity regulaminu |
| 9.2 | Screeny lub PDF ofert, zwłaszcza gdy link może wygasnąć **[O dla pozycji > 1 000 zł]** [P] | pliki | Niektóre urzędy wymagają ofert jako załącznika (np. Piotrków), a przy meblach wizualizacji |
| 9.3 | Sprzęt używany: od kogo (firma handlująca używanym sprzętem / osoba prywatna), wycena lub oferta porównawcza nowego [Z] | tekst + [P] | Używany sprzęt ma osobne zasady: minimalna wartość, rzeczoznawca, deklaracja pochodzenia |
| 9.4 | Czy chcesz kupić samochód lub inny pojazd? Jaki, za ile, do czego? **[O]** | tekst | Zwykle limit 40–50% kwoty, często bez samochodów osobowych poza taxi i nauką jazdy |
| 9.5 | Czy coś z listy kupisz od rodziny, poręczyciela albo z firmy rodziny? **[O]** | tak/nie | **Zakazane** w praktycznie każdym regulaminie. Wtedy zmieniamy sprzedawcę |
| 9.6 | Czy planujesz remont lub adaptację lokalu, reklamę, towar na start, oprogramowanie, stronę www? Kwoty [Z] | tabela | To pozycje z limitami procentowymi albo zakazami. Dopasowujemy je do regulaminu |

## Sekcja 10. Wkład własny i finansowanie

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 10.1 | Co już masz do firmy (sprzęt, narzędzia, samochód, lokal, oprogramowanie)? Wartość szacunkowa **[O]** (lub „nic”) | tabela | Wkład rzeczowy oraz „posiadany sprzęt” są punktowane w części kart |
| 10.2 | Ile własnych pieniędzy dołożysz na start (zł) i na co? [Z] | liczba + tekst | Wkład finansowy bywa punktowany (np. Nowa Sól: powyżej 10% = 2 pkt). Pokrywa też wydatki, których dotacja nie finansuje (czynsz, ZUS, kasa fiskalna) |
| 10.3 | Wydatki już poniesione w ostatnich 6 mies. na przygotowanie firmy, z fakturami (np. kurs, sprzęt) [Z] [P] | tabela + pliki | W niektórych urzędach liczą się jako udokumentowany wkład własny |
| 10.4 | Inne źródła: oszczędności, pomoc rodziny, pożyczka (np. BGK) [Z] | tekst | „Kalkulacja kosztów ze źródłami finansowania” |
| 10.5 | Ile miesięcy wytrzymasz finansowo, jeśli firma na początku zarabia mało? [Z] | wybór: < 3 / 3–6 / > 6 | Realizm prognozy i ocena ryzyka |

## Sekcja 11. Listy intencyjne i deklaracje klientów

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 11.1 | Czy możesz zdobyć list intencyjny, umowę przedwstępną lub deklarację współpracy od przyszłych klientów, kontrahentów albo dostawców? Ile? 0 / 1–2 / 3+ **[O]** | wybór | Punktowane m.in. w Turku, Grodzisku Maz. i Nowej Soli |
| 11.2 | Dla każdej deklaracji: kto (firma lub osoba, branża), czego dotyczy, szacowana wartość lub częstotliwość [Z] | tabela | Dostarczymy wzór listu do podpisu. **Deklaracje muszą być prawdziwe i podpisane przez realne osoby** |
| 11.3 | Skany podpisanych listów [Z] [P] | pliki | Załącznik do wniosku |

## Sekcja 12. Zatrudnienie

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 12.1 | Czy planujesz zatrudnić pracownika w 1. roku? nie / tak: ilu, na jakie stanowisko, od kiedy, wymiar **[O]** | wybór + tekst | „Przewidywane zatrudnienie” i „nowe miejsca pracy” są oceniane. Koszt wchodzi do prognozy |
| 12.2 | Czy ktoś z rodziny będzie pomagać (osoba współpracująca)? [Z] | tekst | Wpływa na koszty (ZUS osoby współpracującej) |

## Sekcja 13. Prognoza – dane wyjściowe

| # | Pytanie | Typ | 💡 Po co pytamy |
|---|---|---|---|
| 13.1 | Ilu klientów lub zleceń miesięcznie w 1., 6. i 12. miesiącu (realnie, nie optymistycznie)? **[O]** | 3 liczby | Wniosek wymaga przychodów i kosztów **miesięcznie w 1. roku z uzasadnieniem** |
| 13.2 | Miesiące słabsze i mocniejsze (sezonowość) [Z] | siatka 12 mies. | Rozkład przychodów |
| 13.3 | Stałe koszty miesięczne, które znasz: czynsz, media, paliwo, telefon, internet, księgowość, ubezpieczenie, materiały na usługę, abonamenty, leasing [Z] | tabela | Koszty w prognozie |
| 13.4 | Koszt materiałów lub towaru na jedną usługę lub sprzedaż (np. farba do włosów 15 zł na klientkę) [Z] | tekst | Marża i próg rentowności |

## Sekcja 14. Zgody i oświadczenia

| # | Pole | Typ |
|---|---|---|
| 14.1 | Oświadczam, że podane informacje są prawdziwe i nie zawierają zmyślonych danych **[O]** | checkbox |
| 14.2 | Rozumiem, że usługa nie gwarantuje przyznania dotacji, a decyzję podejmuje urząd **[O]** | checkbox |
| 14.3 | Zgoda na przetwarzanie danych w celu realizacji usługi (link do polityki prywatności, w tym informacja o narzędziach AI) **[O]** | checkbox |
| 14.4 | Rozumiem, że przed złożeniem muszę sam(-a) sprawdzić i podpisać wniosek **[O]** | checkbox |
| 14.5 | Zgoda na kontakt po decyzji urzędu (ankieta o wyniku) [Z] | checkbox |

---

## Mapa: pole wniosku (rozp. § 2 ust. 3) → pytania kwestionariusza

| Pole wniosku | Pytania |
|---|---|
| pkt 1: dane osobowe | — (klient sam) |
| pkt 2: dodatkowe warunki starosty | 1.3, 1.6, 1.9, 1.10, 3.7 |
| pkt 3: PKD | 3.1, 3.3 |
| pkt 4: opis działalności, uprawnienia | 3.1–3.5, 3.8 |
| pkt 5: adres miejsca, przechowywanie sprzętu | 5.1, 5.2, 5.7 |
| pkt 6: opis lokalu | 5.3–5.6 |
| pkt 7: wykształcenie, szkolenia, doświadczenie | 6.1–6.7 |
| pkt 8: przychody i koszty 1. roku, miesięcznie | 3.2, 4.2–4.5, 5.5, 12.1, 13.1–13.4 |
| pkt 9: specyfikacja wydatków | 9.1–9.6 |
| pkt 10: kalkulacja kosztów i źródła finansowania | 9.1, 10.1–10.4 |
| pkt 11: kwota | 1.12 |
| pkt 12: zabezpieczenie | 2.1–2.5 |
| Karta oceny: rynek, konkurencja, SWOT, deklaracje | 7.1–7.5, 8.1–8.3, 11.1–11.3 |
| Załączniki de minimis | 1.6 (informacyjnie). Formularze wypełnia klient |
