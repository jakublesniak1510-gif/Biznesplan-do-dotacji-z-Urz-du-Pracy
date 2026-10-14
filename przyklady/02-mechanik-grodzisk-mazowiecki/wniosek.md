# Wniosek – treści do formularza PUP Grodzisk Mazowiecki (warsztat mechaniczny)

> **DANE FIKCYJNE – PRZYKŁAD.** Wnioskodawca, jego dawni pracodawcy, wynajmujący halę i firmy z listów intencyjnych są wymyśleni. Miejscowości i ulice, konkurenci (katalog autocentrum.pl), średnie ceny (kb.pl), dane GUS, regulamin i wzór wniosku są prawdziwe (źródła: `raport-kontroli.md`).
>
> Formularz: „Wniosek w sprawie dofinansowania bezrobotnemu, absolwentowi CIS, absolwentowi KIS, opiekunowi, podjęcia działalności gospodarczej”, PUP w Grodzisku Mazowieckim (wzór ze strony urzędu, pobrany 14.10.2026). Regulamin z 22.04.2026 (Zarządzenie nr 13/2026), kryteria oceny z kwietnia 2026 (maks. 37 pkt). Nabór: jeszcze nieogłoszony – **[do weryfikacji: maksymalna kwota i obowiązujący wzór wniosku z ogłoszenia]**.
> Ton: **techniczny**. Wariant: **standard** (~2000 znaków na sekcję). Liczby: z `model.xlsx` w tym katalogu.

## Mapa: pole formularza → sekcja

| Część wniosku Grodzisk | Pole formularza (dosłownie) | Sekcja | Gdzie poniżej |
|---|---|---|---|
| Strona 1 | „symbol i przedmiot planowanej działalności gospodarczej według PKD-2025 na poziomie podklasy”, „Wnioskowana kwota dofinansowania” | 01 (dane) | „Pola krótkie” |
| I. Informacja o wnioskodawcy | pkt 1–10, 12–14 (dane, dowód, PESEL, współmałżonek, pomoc PUP, zadłużenie, wcześniejsza działalność) | – | wpisuje klient (`co-wpisac-samemu.md`) |
| | pkt 11 „Przebieg pracy zawodowej oraz posiadane kwalifikacje przydatne do prowadzenia planowanej działalności” | 02 | 02 |
| II. Opis projektowanego przedsięwzięcia | 1. „Rodzaj zamierzonej działalności gospodarczej (krótki opis…)” | 01 | 01 – II.1 |
| | 2. „Zamierzam prowadzić działalność gospodarczą pod adresem… w lokalu…” | 01 | 01 – II.2 |
| | 3. „Działania podjęte na rzecz działalności: a) pozwolenia… b) kursy… c) przedwstępne umowy, oświadczenia o współpracy… d) inne” | 02, 03 | „Pola krótkie” |
| | 4a. „krótki opis celu i charakteru przyszłej działalności… motywy podjęcia działalności” | 01 | 01 – II.4a |
| | 4b. „podstawowe dane o firmie: forma opodatkowania, rodzaj działalności, oferowane produkty i usługi, atuty firmy” | 01 | 01 – II.4b |
| | 4c. „analiza rynku odbiorców, konkurencji, czyli otoczenia na którym firma zamierza działać” | 03 + 04 | 03 i 04 (jedno pole, dwa akapity) |
| | 4d. „ewentualne zatrudnienie pracownika(ów) w przyszłości” | 01 | „Pola krótkie” |
| | 4e. „opis działań marketingowych…” | 05 | 05 |
| III. Zabezpieczenie | forma zabezpieczenia | – | klient podkreśla „poręczenie” |
| IV. Plan finansowy | 1) „kalkulacja kosztów związanych z podjęciem działalności… z podaniem źródeł ich finansowania” | arkusz | Tabela IV.1 |
| | 2) „środki przeznaczone na podjęcie działalności, źródła ich finansowania” | arkusz | Tabela IV.2 |
| | 3) „szczegółowa specyfikacja wydatków… NAZWA / UZASADNIENIE ZAKUPU / KWOTA” | 06 | 06 + Tabela IV.3 |
| | 6) pomoc prawna, konsultacje, doradztwo | – | NIE |
| Zał. nr 2 | „Analiza mocnych i słabych stron… szans… zagrożeń” | 07 | 07 |
| | „WNIOSKI” (wykorzystanie silnych stron i szans; ograniczenie słabych stron i zagrożeń) | 09 | 09 |
| Analiza finansowa | „Analiza finansowa przychodów i kosztów… (w ujęciu średniomiesięcznym)” | arkusz | Tabela „Analiza finansowa” |
| Załącznik własny („Inne dokumenty mające związek z planowaną działalnością”) | uzasadnienie założeń i prognoza 12 mies. miesięcznie (wymóg rozp. § 2 ust. 3 pkt 8; regulamin § 5 ust. 2 dopuszcza zwiększenie uzasadnień) | 08 | 08 + `kosztorys-i-prognoza.md` |

Kryteria oceny PUP Grodzisk (37 pkt) a sekcje: `raport-kontroli.md`, część „Karta oceny”.

---

## Pola krótkie

| Pole | Treść |
|---|---|
| Symbol PKD-2025 (podklasa) | 95.31.A Naprawa mechaniczna i serwisowa pojazdów silnikowych, z wyłączeniem motocykli; 47.82.Z Sprzedaż detaliczna części i akcesoriów do pojazdów silnikowych (dodatkowo) |
| Wnioskowana kwota dofinansowania | 39 400,00 zł (słownie: trzydzieści dziewięć tysięcy czterysta złotych 00/100) |
| II.3 a) uzyskane pozwolenia, zaświadczenia, certyfikaty | Działalność nie wymaga zezwoleń. Dyplom technika pojazdów samochodowych (2012). Serwisu klimatyzacji nie wykonuję – nie mam certyfikatu F-gazowego. Podnośnik zostanie zgłoszony do dozoru technicznego zgodnie z dokumentacją producenta [do weryfikacji: rodzaj dozoru UDT dla wybranego modelu]. |
| II.3 b) odbyte kursy, szkolenia | Szkolenie „Diagnostyka układów sterowania silnikiem (EOBD)”, 16 h, 2021 (zaświadczenie). Szkolenie z diagnostyki wtryskiwaczy Common Rail, 8 h, 2023 (bez zaświadczenia – nie dołączam). |
| II.3 c) przedwstępne umowy, oświadczenia o współpracy | Umowa przedwstępna najmu hali w Kałęczynie na 3 lata. Listy intencyjne z 10.10.2026: Bud-Mont (Grodzisk Maz., 4 busy) i „Smaki Mazowsza” (Jaktorów, 2 samochody dostawcze). |
| II.3 d) inne | Ustne porozumienie z warsztatem w Jaktorowie o przejmowaniu pilnych napraw w razie mojej choroby. Umowa z firmą odbierającą oleje przepracowane – do podpisania przed startem. |
| II.4d zatrudnienie | W pierwszym roku nie planuję zatrudnienia. Jeśli pracy będzie więcej, po ok. 2 latach zatrudnię pomocnika. |
| Forma opodatkowania (II.4b) | zasady ogólne (skala podatkowa); zwolnienie podmiotowe z VAT |

---

## 01. Opis przedsięwzięcia (część II, pkt 1, 2, 4a, 4b)

### II.1 Rodzaj zamierzonej działalności

Usługi: warsztat mechaniki pojazdowej dla samochodów osobowych i dostawczych do 3,5 t. Zakres: serwis olejowy, układ hamulcowy, zawieszenie i układ kierowniczy, rozrządy z pompą wody, sprzęgła, diagnostyka komputerowa EOBD i elektryka. Dodatkowo sprzedaż części i olejów do wykonywanych napraw.

### II.2 Adres i lokal

Kałęczyn, ul. Wylotowa (gm. Grodzisk Mazowiecki), ok. 3 km na północ od centrum Grodziska. Lokal usługowy: hala murowana 75 m², brama 3,2 × 3 m, posadzka betonowa (wylewka ok. 20 cm), zasilanie 400 V, woda, WC, ogrzewanie nagrzewnicą elektryczną, utwardzony plac na 4 auta. Kanału nie ma. Lokal jest własnością osoby prywatnej. W załączeniu umowa przedwstępna najmu na 3 lata, czynsz 2 200 zł miesięcznie.

### II.4a Cel i charakter działalności, motywy

Przez 8 lat (09.2018–08.2026) pracowałem jako mechanik w 3-stanowiskowym warsztacie w Milanówku. Od 2023 r., gdy szef chorował, przyjmowałem auta, robiłem wyceny, zamawiałem części i układałem grafik hali. Warsztat zamknięto 31.08.2026, bo właściciel sprzedał działkę. Ok. 70 klientów z Milanówka i Grodziska ma mój numer, a 25 z nich już pytało, gdzie teraz naprawiam. Mogę iść na etat do ASO, ale tam podzespoły wymienia się w całości. Ja chcę naprawiać: zdiagnozować usterkę, wymienić zużyty element i powiedzieć klientowi uczciwie, co jest pilne, a co może poczekać. Celem jest warsztat dla aut 8–20-letnich, którymi jeździ większość klientów z okolicy, i dla małych firm z busami.

### II.4b Podstawowe dane o firmie

– Forma: jednoosobowa działalność, zasady ogólne (skala), zwolnienie z VAT. Start: 1 lutego 2027 r., po wypłacie środków.
– Usługi i ceny robocizny: serwis olejowy 70 zł; hamulce i zawieszenie – średnio 230 zł na zlecenie (klocki i tarcze na osi ok. 200 zł); diagnostyka komputerowa 120 zł; rozrząd lub sprzęgło – średnio 700 zł. Części do naprawy sprzedaję z narzutem ok. 15%.
– Godziny: pn–pt 8–17, sob. 8–13.
– Atuty: 8 lat praktyki w warsztacie i 5 lat w hurtowni części – dobieram część po VIN w katalogu TecDoc w kilka minut i wiem, gdzie kupić taniej. Przed naprawą podaję koszt i daję wybór części w 2–3 wariantach cenowych, a wymienione części pokazuję klientowi.

## 02. Przebieg pracy zawodowej oraz kwalifikacje (część I, pkt 11)

Jestem technikiem pojazdów samochodowych (technikum samochodowe w Żyrardowie, dyplom technika 2012). W branży motoryzacyjnej pracuję od 2013 r., z tego 8 lat jako mechanik.

Przebieg pracy:
– 09.2018–08.2026 – mechanik, warsztat „Auto-Mechanika P.” w Milanówku (3 stanowiska), umowa o pracę. Zakres: serwis olejowy i przeglądy okresowe, układ hamulcowy (klocki, tarcze, płyn hamulcowy), zawieszenie i układ kierowniczy, wymiana rozrządu z pompą wody na blokadach, wymiana sprzęgieł, diagnostyka komputerowa: odczyt i kasowanie kodów usterek, analiza parametrów bieżących, adaptacje po wymianie podzespołów. Na co dzień pracowałem testerami Launch i Delphi. Od 2023 r. dodatkowo przyjmowałem auta, przygotowywałem wyceny, zamawiałem części i układałem grafik hali, gdy właściciel chorował. Rozwiązanie umowy za porozumieniem stron po zamknięciu warsztatu.
– 2013–08.2018 – magazynier, potem sprzedawca na zapleczu w hurtowni części samochodowych w Pruszkowie. Dobór części po numerze VIN w katalogu TecDoc, obsługa zwrotów i reklamacji. Stąd znam rynek dostawców i różnice między częściami oryginalnymi i zamiennikami.

Kursy:
– „Diagnostyka układów sterowania silnikiem (EOBD)”, 16 h, 2021 r., szkolenie w hurtowni części w Warszawie (zaświadczenie).
– Diagnostyka wtryskiwaczy Common Rail, 8 h, 2023 r. (zaświadczenia nie otrzymałem).
Prawo jazdy kat. B od 2011 r.

Umiejętności przydatne w firmie: rozmowa z klientem przy przyjęciu auta, wycena i uzgodnienie zakresu naprawy, reklamacje części w hurtowni, Excel w podstawowym zakresie.

Uprawnień F-gazowych nie mam, dlatego nie oferuję serwisu klimatyzacji. Kurs F-gazowy planuję w drugim roku działalności. Księgowość (KPiR) prowadzić będzie biuro rachunkowe.

Do wniosku dołączam kopie: dyplomu technika, dwóch świadectw pracy i zaświadczenia ze szkolenia EOBD.

## 03. Analiza rynku odbiorców (część II, pkt 4c – akapit 1)

Obszar działania: Grodzisk Mazowiecki (34 904 mieszkańców, GUS, 31.12.2024) z sąsiednimi wsiami gminy – Kałęczyn i Książenice – oraz gminy Milanówek, Jaktorów i Żabia Wola, w promieniu ok. 10–15 km od hali.

Odbiorcy:
1. Kierowcy prywatni z autami 8–20-letnimi. Najlepiej znam grupę VAG i auta francuskie. Potrzebują napraw bieżących: hamulców, zawieszenia, rozrządu, sprzęgła, diagnostyki kontrolki silnika. Oczekują wyceny przed naprawą i krótkiego terminu. Z obserwacji wiem, że w nowych domach w Książenicach i Kałęczynie często są dwa auta na rodzinę.
2. Małe firmy z samochodami dostawczymi do 3,5 t (budowlane, cateringowe, kurierskie). Dla nich liczy się przestój – auto musi wrócić na trasę w 1–2 dni. Serwis okresowy co 20–30 tys. km daje regularne zlecenia.

Dowody popytu:
– ok. 70 stałych klientów z warsztatu w Milanówku ma mój numer telefonu, 25 z nich już zapytało o nowe miejsce,
– list intencyjny firmy Bud-Mont z Grodziska: serwis okresowy i naprawy 4 busów (Renault Master, Ford Transit),
– list intencyjny firmy „Smaki Mazowsza” z Jaktorowa: serwis i hamulce 2 samochodów Fiat Ducato.

Sprzedaż metodą bezpośrednią: zgłoszenia telefoniczne, przez stronę i na miejscu, termin w 2–3 dni robocze. Proste naprawy wykonuję w dniu przyjęcia. Hala leży przy drodze do Grodziska, ma utwardzony dojazd i plac na 4 auta, więc klient może zostawić auto rano i odebrać po pracy.

Dostawcy: części zamawiam w hurtowniach motoryzacyjnych, które znam z pięciu lat pracy w Pruszkowie – wiem, jak działają tam rabaty, zwroty i reklamacje części.

Sezonowość: najwięcej zleceń mam od września do listopada (przygotowanie do zimy: akumulatory, hamulce, płyny) oraz w marcu i kwietniu. Mniej w lipcu i sierpniu (urlopy) oraz w styczniu i lutym. Firmy zlecają serwis z ustalonym terminem, więc część tych prac mogę przesunąć na spokojniejsze tygodnie. Sezonowość jest ujęta w prognozie miesięcznej.

## 04. Analiza konkurencji (część II, pkt 4c – akapit 2)

Dla Grodziska Mazowieckiego katalog autocentrum.pl wymienia ok. 15 firm motoryzacyjnych. Wybrałem cztery warsztaty mechaniczne w mieście, ok. 3–5 km od hali w Kałęczynie:
1. Bosch Service Wocar, ul. Królewska 50 – warsztat działający pod marką sieci Bosch. Konkuruje rozpoznawalną marką.
2. ASO Mikrus Filutowscy, ul. Chełmońskiego 12a – autoryzowana stacja obsługi (ASO).
3. Auto Best Sp. z o.o., ul. Żyrardowska 48 – warsztat mechaniczny.
4. AUTO-GAZ, ul. Poniatowskiego 36 – mechanika pojazdowa, z nazwy także instalacje gazowe.
Poza nimi działają mniejsze warsztaty jednoosobowe. Moja hala jest w Kałęczynie, więc klienci z północnej części gminy nie muszą wjeżdżać do centrum Grodziska.

Ceny: według kb.pl średnia robocizna w Grodzisku i okolicach (29.04.2026) to: wymiana oleju i filtrów 71,30 zł, przednie tarcze i klocki 271 zł, sprzęgło 896 zł, pompa wody 285 zł. Moje stawki: serwis olejowy 70 zł, hamulce i zawieszenie średnio 230 zł, rozrząd lub sprzęgło średnio 700 zł – na poziomie średniej lub nieco poniżej, bo hala poza centrum ma niższy czynsz.

Czym się wyróżnię:
– naprawa uszkodzonego elementu zamiast wymiany całego zespołu tam, gdzie jest to technicznie uzasadnione,
– wycena przed naprawą i części w 2–3 wariantach cenowych z katalogu TecDoc, wymienione części oddaję klientowi,
– termin w 2–3 dni robocze i sobota do 13,
– dla firm: serwis okresowy busów ustalany z wyprzedzeniem.

Serwisy sieciowe i ASO mają przewagę w wyposażeniu (np. geometria, klimatyzacja, specjalistyczne testery marek) i w rozpoznawalności. Tych usług nie oferuję: geometrię i opony odsyłam do wulkanizacji, a klimatyzację – do czasu uzyskania F-gazów – do serwisów z uprawnieniami. Konkuruję terminem, ceną robocizny i znajomością starszych aut.

## 05. Opis działań marketingowych (część II, pkt 4e)

Odbiorcy z sekcji 03 to dwie grupy, dlatego promocję prowadzę dwutorowo. Pierwszych klientów mam z dawnego warsztatu i z dwóch firm, więc nie potrzebuję dużej kampanii – muszą się dowiedzieć, gdzie teraz jestem. Nie planuję ulotek ani prasy: kierowcy szukają mechanika w Google albo z polecenia.

Kierowcy prywatni:
– kaseton z nazwą na hali i baner przy drodze do Grodziska – hala jest poza centrum, więc oznakowanie przy drodze prowadzi klientów do bramy,
– wizytówka Google z mapą i opiniami – kierowcy szukają warsztatu przez wyszukiwarkę „mechanik Grodzisk”,
– strona www z mapą dojazdu, cennikiem podstawowych usług i formularzem zgłoszenia,
– wpisy w lokalnych grupach mieszkańców Grodziska na Facebooku,
– SMS z nowym adresem do ok. 70 dawnych klientów, których numery mam w telefonie.

Firmy:
– osobiste spotkanie i stała oferta na serwis okresowy (Bud-Mont i „Smaki Mazowsza” już zadeklarowały współpracę),
– polecenia od firm – Bud-Mont zna inne firmy z busami.

Budżet: z dotacji kaseton z banerem 1 230 zł i strona www 1 476 zł. Bieżąco 200 zł miesięcznie na reklamę w internecie.

Plan pierwszych 3 miesięcy:
– przed startem: wizytówka Google, strona, kaseton i baner, SMS do dawnych klientów,
– luty: pierwsze serwisy busów z listów intencyjnych, prośba do każdego klienta o opinię w Google,
– marzec–kwiecień: wpisy w grupach lokalnych przed sezonem wiosennym,


Przekaz na kasetonie, banerze i stronie jest ten sam: naprawy aut osobowych i dostawczych do 3,5 t, termin 2–3 dni robocze, sobota do 13. To wyróżniki, które opisałem w analizie konkurencji.

Utrzymanie klientów: po serwisie olejowym naklejam na szybę kartkę z przebiegiem następnej wymiany, a przed zimą wysyłam stałym klientom SMS z przypomnieniem o przeglądzie hamulców i akumulatora.

## 06. Szczegółowa specyfikacja wydatków z uzasadnieniem (część IV, pkt 3)

*Pole: kolumna „UZASADNIENIE ZAKUPU” w tabeli IV.3. Poniżej opis zbiorczy, pod nim tabela pozycji.*

Z dotacji 39 400,00 zł kupię wyposażenie stanowiska naprawczego, narzędzia specjalistyczne, pierwszy zapas olejów i filtrów oraz oznakowanie warsztatu. Z wkładu własnego za 2 337,00 zł kupię kasę fiskalną, sprzęt BHP i ochrony środowiska oraz odzież roboczą. Jestem zwolniony z VAT, więc podaję kwoty brutto.

Stanowisko i urządzenia – 32 625,75 zł. Hala nie ma kanału, dlatego podstawą jest podnośnik dwukolumnowy 4 t z montażem na kotwach i dokumentacją do UDT (9 501,75 zł). Kupuję nowy: używany od likwidowanego warsztatu wymagałby wyceny rzeczoznawcy, demontażu i ponownego kotwienia, bez gwarancji. Tester wielomarkowy klasy Launch X-431 z aktualizacją na 12 miesięcy (5 904,00 zł) obsługuje odczyt kodów, parametry bieżące i adaptacje – bez niego nie wykonam diagnostyki ani kasowania błędów po naprawie. Kompresor 270 l na 400 V (3 198,00 zł) zasila klucze pneumatyczne (1 722,00 zł) i zlewarkę oleju (922,50 zł). Prasa 20 t (1 599,00 zł) służy do wymiany tulei, łożysk i sworzni. Blokady rozrządu (1 107,00 zł) są warunkiem poprawnej wymiany rozrządu w silnikach VAG, PSA, Renault, Ford i Opel. Żaba niskoprofilowa 3 t ze stojakami (861,00 zł) mieści się pod obniżone auta, a moja stara żaba 2 t zostaje jako zapas. Zasilacz do kodowania (984,00 zł) chroni elektronikę podczas programowania. Urządzenie do płynu hamulcowego (1 107,00 zł) pozwala wymienić płyn bez zapowietrzenia układu ABS. Myjka do części (799,50 zł), stół z imadłem i szafka (1 968,00 zł) oraz laptop z katalogami części i programem do kosztorysów (2 952,00 zł) uzupełniają stanowisko.

Towar – 4 068,25 zł (10,3% kwoty, limit regulaminu 30%): oleje w beczkach 60 l i filtry do najczęstszych modeli – kupowane hurtowo są tańsze niż na sztuki.

Reklama – 2 706,00 zł (6,9% kwoty, limit 15%): kaseton z banerem i strona www.

Mam już własne narzędzia ręczne o wartości ok. 6 000 zł (wózek z kluczami i nasadkami, klucz dynamometryczny, ściągacze, lampy) oraz samochód do dowozu części. Dlatego nie ma ich w kosztorysie. Ceny pochodzą z ofert internetowych z października 2026 r. Wszystkie zakupy są nowe.

### Tabela IV.3 – szczegółowa specyfikacja wydatków w ramach dofinansowania

| Lp. | Nazwa | Uzasadnienie zakupu | Kwota (zł) |
|---|---|---|---|
| 1 | Podnośnik dwukolumnowy 4 t, elektrohydrauliczny, z montażem i dokumentacją UDT | hala bez kanału; podniesienie auta do hamulców, zawieszenia, sprzęgła, wydechu; nowy z gwarancją i montażem na kotwach | 9 501,75 |
| 2 | Tester diagnostyczny wielomarkowy z aktualizacją 12 mies. | odczyt i kasowanie kodów EOBD, parametry bieżące, adaptacje i kodowanie po wymianie części | 5 904,00 |
| 3 | Kompresor tłokowy 270 l, 400 V | zasilanie narzędzi pneumatycznych i zlewarki; zbiornik 270 l przy pracy kluczem udarowym | 3 198,00 |
| 4 | Klucz udarowy pneumatyczny 1/2" + akumulatorowy, nasadki udarowe | odkręcanie kół, śrub wahaczy i amortyzatorów; akumulatorowy do pracy poza halą | 1 722,00 |
| 5 | Prasa hydrauliczna 20 t | wymiana łożysk piast, tulei wahaczy, sworzni | 1 599,00 |
| 6 | Zestaw blokad rozrządu (VAG, PSA, Renault, Ford, Opel) | ustawienie faz rozrządu przy wymianie paska lub łańcucha zgodnie z procedurą producenta | 1 107,00 |
| 7 | Zlewarka/wysysarka oleju pneumatyczna 80 l | serwis olejowy bez rozlewania oleju, zbiórka oleju do utylizacji | 922,50 |
| 8 | Podnośnik żaba 3 t niskoprofilowy + 2 pary stojaków | prace na kołach, aut niskich i przy zajętym podnośniku | 861,00 |
| 9 | Prostownik z rozruchem i zasilacz do kodowania | stabilne napięcie przy diagnostyce i kodowaniu, rozruch aut z rozładowanym akumulatorem | 984,00 |
| 10 | Myjka do części z pompą | czyszczenie zacisków i elementów przed montażem | 799,50 |
| 11 | Urządzenie do wymiany płynu hamulcowego | wymiana płynu pod ciśnieniem, bez zapowietrzenia układu ABS | 1 107,00 |
| 12 | Laptop | tester (oprogramowanie), katalog TecDoc, kosztorysy i faktury | 2 952,00 |
| 13 | Stół warsztatowy z imadłem + szafka narzędziowa | stanowisko do prac przy podzespołach, przechowywanie narzędzi specjalnych | 1 968,00 |
| 14 | Oleje silnikowe (2 × 60 l), filtry, płyny | pierwszy zapas na ok. 2 miesiące, zakup hurtowy taniej niż na sztuki (towar 10,3%) | 4 068,25 |
| 15 | Kaseton z nazwą na halę + baner przy drodze | oznakowanie hali poza centrum, widoczne z drogi do Grodziska | 1 230,00 |
| 16 | Strona www z mapą dojazdu i formularzem | zgłoszenia napraw i dojazd do hali poza centrum | 1 476,00 |
| | **Razem** | | **39 400,00** |

## 07. Analiza mocnych i słabych stron, szans i zagrożeń (Zał. nr 2)

**MOCNE STRONY**
– 8 lat pracy mechanika (2018–2026) w pełnym zakresie mechaniki i diagnostyki, w tym 3 lata przyjmowania aut, wycen i zamówień części.
– 5 lat w hurtowni części: dobór części po VIN w TecDoc i znajomość dostawców.
– Dyplom technika pojazdów samochodowych i szkolenie EOBD.
– Hala gotowa do pracy (75 m², 400 V, wylewka pod podnośnik), umowa przedwstępna na 3 lata.
– Własne narzędzia ręczne (ok. 6 000 zł) i 8 000 zł gotówki na start.
– Praktyka z testerami Launch i Delphi oraz katalogiem TecDoc.

**SŁABE STRONY**
– Brak certyfikatu F-gazowego – nie wykonuję serwisu klimatyzacji (kurs w 2. roku).
– Pracuję sam – choroba oznacza przestój (pilne naprawy przejmie warsztat w Jaktorowie).
– Hala poza centrum i bez ruchu „z ulicy” (kaseton, baner, wizytówka Google).
– Nie prowadziłem firmy (KPiR prowadzi biuro rachunkowe).
– Brak sprzętu do geometrii i opon (te usługi odsyłam do wulkanizacji).

**SZANSE**
– Zamknięcie warsztatu w Milanówku – ok. 70 klientów zna mnie z nazwiska, 25 już pytało o nowe miejsce.
– Listy intencyjne dwóch firm na serwis 6 samochodów dostawczych.
– Nowa zabudowa jednorodzinna w Kałęczynie i Książenicach (obserwacja z okolicy, bez danych liczbowych).
– Średnie ceny robocizny w Grodzisku (kb.pl) są wyższe lub równe moim.
– Bud-Mont zna inne firmy z busami – możliwe kolejne zlecenia z polecenia.

**ZAGROŻENIA**
– Rosnące ceny części mogą odkładać naprawy (warianty części w 2–3 cenach).
– Duże serwisy mogą obniżyć ceny lub skrócić terminy.
– Rezygnacja firm z listów intencyjnych (więcej klientów prywatnych, polecenia między firmami).
– Słabsze miesiące: lipiec–sierpień i styczeń–luty (przesuwam na nie zlecenia firm z ustalonym terminem).
– Zimą wyższe rachunki za ogrzewanie hali nagrzewnicą (media w kosztach: 450 zł miesięcznie).

## 09. Wnioski z analizy – ograniczenie słabych stron i zagrożeń (Zał. nr 2, „WNIOSKI”)

*Pole: „WNIOSKI” pod tabelą SWOT – formularz Grodziska nie ma osobnej rubryki na ryzyka, dlatego plan działań na wypadek ryzyk jest tutaj.*

Silne strony wykorzystam od pierwszego dnia: dawni klienci i dwie firmy z busami dają zlecenia od startu, a znajomość TecDoc i dostawców obniża koszt części dla klienta. Ryzyka i działania:

1. Choroba (pracuję sam). Pilne naprawy przejmie warsztat w Jaktorowie, z którym mam ustne porozumienie. Zlecenia firm mają ustalone terminy, więc można je przesunąć. Opłacam dobrowolne ubezpieczenie chorobowe.
2. Awaria podnośnika. Podnośnik jest nowy, na gwarancji, z serwisem dostawcy. Na czas naprawy proste prace wykonuję na żabie i stojakach.
3. Wzrost cen części. Klient wybiera część z 2–3 wariantów cenowych, więc sam decyduje o koszcie naprawy.
4. Mniej klientów niż w planie. Więcej zleceń dla firm – Bud-Mont współpracuje z innymi firmami z busami. Wydłużam pracę w soboty. Reklamy nie tnę poniżej 200 zł miesięcznie – to minimum, które utrzymuję.
5. Słabe miesiące (lipiec–sierpień, styczeń–luty). Zlecenia firm z ustalonym terminem przesuwam na spokojniejsze tygodnie.
6. Rezygnacja firm z listów intencyjnych. Podstawą są klienci prywatni – ok. 70 osób z Milanówka i Grodziska. Busy firm to dodatkowe, regularne zlecenia.
7. Brak uprawnień F-gazowych. Klientów z naprawą klimatyzacji odsyłam do serwisu z uprawnieniami, a kurs zrobię w drugim roku.
8. Ochrona środowiska. Olej przepracowany zbieram do beczek, odbiera go firma z umową. Pod auta stosuję wanny wychwytowe i sorbent (zakup z wkładu własnego).

Sprawdziłem też wariant z przychodami niższymi o 30%: zysk netto wyniesie średnio 3 107 zł miesięcznie, a najniższe saldo gotówki 4 188 zł. Szczegóły w uzasadnieniu założeń.

Pierwszy miesiąc kończy się niewielką stratą, bo przychód buduje się od 40% planu. Pokrywam ją z gotówki na start. Żona pracuje na etacie, co daje rodzinie stały dochód w okresie rozruchu. Znam obowiązki z umowy: 12 miesięcy działalności, bez etatu i bez zawieszania ponad 6 miesięcy łącznie, rozliczenie w 2 miesiące od startu.

## 08. Uzasadnienie przyjętych założeń finansowych (załącznik do analizy finansowej)

*Pole: załącznik własny – formularz Grodziska ma tylko tabelę średniomiesięczną, a rozporządzenie wymaga przychodów i kosztów w 1. roku miesięcznie z uzasadnieniem założeń.*

Przychody. Liczę cenę robocizny razy liczbę zleceń. Przy pełnym obłożeniu zakładam miesięcznie: 40 serwisów olejowych po 70 zł, 22 naprawy hamulców i zawieszenia po średnio 230 zł, 18 diagnostyk po 120 zł, 4 rozrządy lub sprzęgła po średnio 700 zł oraz sprzedaż części przy 36 zleceniach po średnio 110 zł. Liczby opieram na moim obłożeniu w Milanówku, ok. 70 dawnych klientach i 6 busach z listów intencyjnych. Przez pierwsze 3 miesiące przyjąłem 40%, 60% i 80% sprzedaży, potem pełną. Uwzględniłem sezon: więcej we wrześniu–listopadzie i w marcu–kwietniu, mniej w lipcu–sierpniu i styczniu–lutym. W najbardziej pracowitym miesiącu wykorzystam 63% czasu pracy przy autach (21 dni po 7 godzin).

Koszty. Stałe – 3 980 zł miesięcznie: czynsz 2 200 zł, media 450 zł, biuro rachunkowe 350 zł, paliwo 300 zł, reklama 200 zł, telefon 100 zł, OC 80 zł, odbiór odpadów, konto i rezerwa na licencję testera 300 zł. Części i materiały to 26% przychodu. ZUS: 6 miesięcy ulgi na start, potem składki preferencyjne (456,18 zł w 12. miesiącu). Składka zdrowotna w roku: 8 050 zł. Opodatkowanie: skala.

Wynik 12 miesięcy: przychody 181 960 zł, koszty z ZUS i zdrowotną 105 857 zł, podatek 5 667 zł, zysk netto 70 436 zł, średnio 5 870 zł miesięcznie. Pierwszy miesiąc z zyskiem: drugi.

Próg rentowności: 6 593 zł przychodu miesięcznie, czyli ok. 48 zleceń. Po rozruchu planuję średnio 16 701 zł miesięcznie, więc margines bezpieczeństwa to 61%. Po zakończeniu ulg ZUS próg wzrośnie do 8 889 zł.

Wariant −30%: przychody 127 372 zł, zysk netto 37 281 zł (3 107 zł miesięcznie), najniższe saldo gotówki 4 188 zł. Działania w tym wariancie opisuję we wnioskach z analizy SWOT.

Płynność: po zakupach z dotacji i wkładu najniższe saldo wynosi 5 446 zł. Przychód przekracza limit zwolnienia z VAT dopiero przy wyższej sprzedaży niż w planie – arkusz to sprawdza.

---

## Tabela „Analiza finansowa przychodów i kosztów” (w ujęciu średniomiesięcznym)

Średnia z 12 miesięcy = wartość roczna z arkusza ÷ 12, zaokrąglona do pełnych złotych (zasada urzędu: do 0,49 w dół, od 0,50 w górę). Rozkład na miesiące: `kosztorys-i-prognoza.md`, sekcja 5.

| Wyszczególnienie | Miesięcznie (zł) |
|---|---|
| **A. PRZYCHODY (OBROTY) OGÓŁEM** | **15 163** |
| 2. Ze sprzedaży usług (robocizna) | 11 588 |
| 3. Ze sprzedaży towarów (części i oleje do napraw) | 3 575 |
| **B. KOSZTY OGÓŁEM** (bez ZUS) | **7 922** |
| 1. Koszty materialne – b) materiały i części zamienne | 3 942 |
| 2. Koszty najmu lokalu | 2 200 |
| 3. Opłaty eksploatacyjne (energia, woda, ogrzewanie) | 450 |
| 4. Transport – a) własny (paliwo) | 300 |
| 7. Koszty usług zewnętrznych (księgowość, odbiór odpadów, licencja testera, konto) | 650 |
| 8. Inne koszty (reklama, telefon) | 300 |
| 9. Ubezpieczenie firmy (OC) | 80 |
| 5–6. Wynagrodzenia i narzuty | 0 |
| **DOCHÓD BRUTTO** | **7 241** |
| SKŁADKI ZUS (społeczne średnio 228 zł + zdrowotna średnio 671 zł) | 899 |
| **E. ZYSK BRUTTO** | **6 342** |
| F. PODATEK DOCHODOWY | 472 |
| **ZYSK NETTO** | **5 870** |
| Spłata innych zobowiązań | 0 |

## Tabela IV.1 – Kalkulacja kosztów związanych z podjęciem działalności i źródła finansowania

| Lp. | Rodzaj kosztu | Wysokość kosztu (zł) | Źródło finansowania |
|---|---|---|---|
| 1 | Maszyny, urządzenia i wyposażenie (poz. 1–13 Tabeli IV.3) | 32 625,75 | dofinansowanie PUP |
| 2 | Towar: oleje, filtry, płyny | 4 068,25 | dofinansowanie PUP |
| 3 | Reklama: kaseton z banerem, strona www | 2 706,00 | dofinansowanie PUP |
| 4 | Kasa fiskalna online | 1 476,00 | środki własne |
| 5 | Gaśnice, apteczka, sorbent, wanny wychwytowe | 492,00 | środki własne |
| 6 | Ubranie robocze i obuwie ochronne | 369,00 | środki własne |
| | **Razem** | **41 737,00** | |

Czynsz, media i ZUS w pierwszych miesiącach pokrywam z pozostałej gotówki własnej i z przychodów – nie z dotacji.

## Tabela IV.2 – Środki przeznaczone na podjęcie działalności i źródła ich finansowania

| Lp. | Źródło finansowania | Rodzaj pozyskanych środków | Kwota (zł) |
|---|---|---|---|
| 1 | Dofinansowanie: Powiatowy Urząd Pracy w Grodzisku Mazowieckim | gotówka | 39 400,00 |
| 2 | Oszczędności własne | na kasę fiskalną, BHP, odzież i pierwsze miesiące działalności | 8 000,00 |
| 3 | Posiadane maszyny i urządzenia | narzędzia ręczne, wózek narzędziowy, klucz dynamometryczny, żaba 2 t (wartość szacunkowa) | 6 000,00 |
| 3 | Posiadany środek transportu | Skoda Octavia kombi 2012 (dowóz części) | [wartość szacunkowa – wpisuje klient] |
| 4–6 | Darowizna, kredyt, pożyczka | brak | 0 |
| | **Razem ogółem** (bez wartości samochodu) | | **53 400,00** |
