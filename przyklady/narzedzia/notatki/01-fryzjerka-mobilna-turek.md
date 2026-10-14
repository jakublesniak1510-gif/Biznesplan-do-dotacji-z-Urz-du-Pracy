@@ naglowek
# Kosztorys i prognoza – fryzjerka mobilna, PUP Turek

> **DANE FIKCYJNE – PRZYKŁAD.** Wszystkie liczby w tabelach pochodzą z `model.xlsx` w tym katalogu: kopia `model-finansowy/model-finansowy-pup.xlsx` z danymi klientki, przeliczona przez LibreOffice (`/usr/bin/soffice --headless --convert-to xlsx`). Plik wygenerował skrypt `przyklady/narzedzia/kosztorys_md.py` – po każdej zmianie arkusza generujemy go od nowa, nie poprawiamy liczb ręcznie.
>
> Regulamin: „Informacja dotycząca przyznawania środków na podjęcie działalności gospodarczej w PUP w Turku w 2026 roku” (stan na 06.08.2026). Nabór 12–16.10.2026, 38 822 zł na 1 osobę.

@@ kosztorys_intro
Klientka jest zwolniona z VAT, więc „do rozliczenia” = kwota brutto. Ceny netto wpisano tak, żeby brutto odpowiadało ofercie typu z października 2026 r. (porównywarki i sklepy internetowe). Linki prowadzą do **ofert typu** albo do wyszukiwarki ofert (Ceneo) – przed złożeniem wniosku klientka zapisuje konkretną ofertę do PDF i dołącza ją do wniosku. Pozycje oznaczone „[oferta … – do dołączenia]” wymagają oferty od lokalnego wykonawcy (hurtownia, drukarnia, oklejanie aut).

Kasa fiskalna jest w wkładzie własnym, bo PUP Turek nie finansuje kasy (Informacja 2026, cz. IV pkt 1 ppkt 8). Fryzjerka musi ją mieć od pierwszej usługi.

@@ limity
PUP Turek nie podaje limitów procentowych dla kategorii – w arkuszu wpisano 100% (brak limitu), a remont 0%, bo klientka go nie planuje. Turek ocenia za to „faktycznie niezbędne wydatki odpowiadające profilowi działalności” (kryterium 1 karty) i może obniżyć kwotę przy kosztach „niezasadnych lub zawyżonych” (cz. IV pkt 2). Dlatego skreślono drugą suszarkę i fotel hydrauliczny, a kwota (15 000 zł) jest wyraźnie niższa od 38 822 zł z ogłoszenia. Wykluczenia z Informacji (kasa fiskalna, szkolenia, wynajem lokalu, transport zakupów, leasing) – sprawdzone, żadna pozycja z dotacji ich nie dotyczy.

@@ przychody
Liczba usług przy pełnym obłożeniu pochodzi z kwestionariusza (3.2), rozruch 50% / 70% / 90% z odpowiedzi 13.1 („od razu te z zeszytu”), sezonowość z 3.5 i 13.2. Czas pracy z klientem: 21 dni × 6 h (bez dojazdów). Najwyższe obłożenie wychodzi poniżej 100%, więc plan jest wykonalny w czasie pracy jednej osoby. Dopłaty za dojazd poza Turek (10–20 zł) nie są w przychodach – to ostrożne założenie.

@@ koszty
Paliwo 650 zł/mies. to środek przedziału podanego przez klientkę (600–700 zł). Biuro rachunkowe 200 zł – wycena biura z Turku. OC 40 zł – szacunek klientki („nie wiem, 40?”), do potwierdzenia ofertą ubezpieczyciela. Kasa, Booksy i konto – 150 zł. Brak czynszu i mediów (praca mobilna, sprzęt w mieszkaniu klientki).

@@ pesymistyczny
Arkusz liczy wariant, w którym przychody w każdym miesiącu są o 30% niższe, a koszty stałe, ZUS i składka zdrowotna zostają bez zmian (materiały spadają razem z przychodem). Wynik: firma dalej ma zysk netto, a najniższe saldo gotówki jest takie samo jak w wariancie bazowym (1 946 zł), bo przypada na start – po zakupach z dotacji i wkładu własnego, przed pierwszym przychodem. Działania na wypadek niższych przychodów (z rozmowy z klientką 14.10.2026): stała współpraca z domem seniora co 6 tygodni, karnety rodzinne, mniej płatnej reklamy. Opisane w sekcji 09 wniosku.

**Słaby punkt do omówienia z klientką:** saldo na starcie 1 946 zł. Jeśli pierwszy miesiąc będzie słabszy niż 50% planu, klientka dopłaci z oszczędności domowych (pensja męża). Komisja może o to zapytać.

@@ uproszczenia
### Uproszczenia modelu, o których trzeba wiedzieć

- Start 1.12.2026 – 11 z 12 miesięcy przypada na 2027 r., a arkusz liczy na stałych z 2026 r. (płaca minimalna, ZUS, składka zdrowotna). Po ogłoszeniu wskaźników na 2027 r. trzeba zaktualizować arkusz `Stale-2026` i wygenerować ten plik ponownie.
- Ryczałt 8,5% dla całego przychodu (usługi fryzjerskie). Model nie dzieli przychodu na stawki.
- Brak amortyzacji: zakupy z dotacji nie są kosztem w rachunku wyników (ostrożnie – podatek raczej zawyżony niż zaniżony).
- Zysk netto to dochód przed prywatnymi wydatkami klientki. Opłaty domowe pokrywa pensja męża (kwestionariusz 10.4).

@@ docx_tytul
# Treści do wniosku o dofinansowanie podjęcia działalności gospodarczej
Powiatowy Urząd Pracy w Turku, ul. Komunalna 6, 62-700 Turek
Nabór 12–16.10.2026 (rezerwa Funduszu Pracy, program dla osób zwolnionych z przyczyn niedotyczących pracowników)
Wnioskodawczyni: Joanna [nazwisko] – **DANE FIKCYJNE – PRZYKŁAD**
Działalność: mobilny zakład fryzjerski, PKD 96.21.Z · Kwota: 15 000,00 zł

@@ docx_samemu
- **Wzór wniosku:** pobierz z turek.praca.gov.pl → Dokumenty do pobrania („Wniosek o dofinansowanie podjęcia działalności gospodarczej”, .docx). Nie zmieniaj układu formularza – Turek wymaga wypełnienia bez zmian szaty graficznej.
- **Dane wnioskodawcy (str. 1):** imię i nazwisko, PESEL, adres zamieszkania i do doręczeń, adres do doręczeń elektronicznych (jeśli masz), telefon, e-mail, NIP (zaznacz „nie posiadam”). Zaznacz „Osoba bezrobotna”.
- **„Czy wnioskodawca wcześniej prowadził działalność”:** zaznacz NIE.
- **Adres przechowywania sprzętu:** dopisz numer budynku i mieszkania na os. Wyzwolenia.
- **Zabezpieczenie:** zaznacz „poręczenie”. Poręczyciele (brat, teść) przygotują zaświadczenia o dochodach; mąż musi wyrazić zgodę na umowę (wspólność majątkowa).
- **Załącznik nr 3 – oświadczenia bezrobotnego:** przeczytaj każde (objaśnienia: `co-wpisac-samemu.md`), zaznacz „nie otrzymałam” przy pomocy de minimis, jeśli to prawda, i podpisz. Składasz je pod rygorem odpowiedzialności karnej.
- **Załącznik nr 6 – pozostałe oświadczenia:** podpisz (zgoda na wizytację, informowanie o zmianach).
- **Formularz informacji przy ubieganiu się o pomoc de minimis:** wypełnij części dotyczące Ciebie i planowanej działalności.
- **Uzupełnij przed złożeniem:** pełną nazwę ośrodka szkoleniowego z Konina z zaświadczenia (sekcja 02a – miejsce oznaczone „BRAK DANYCH”).
- **Dołącz:** kopie zaświadczeń z kursów, świadectwa pracy, list intencyjny domu seniora „Spokojna Przystań”, wydruki ofert do każdej pozycji z Tabeli 2.
- **Podpisz:** wniosek (str. „Oświadczam, że dane…”), Załącznik nr 1 (Analiza finansowa), Załącznik nr 2, Załączniki nr 3 i 6.
- **Złożenie:** 12–16.10.2026, w siedzibie PUP (7:30–15:30) albo przez praca.gov.pl, e-Doręczenia lub ePUAP z podpisem kwalifikowanym albo zaufanym. Nie wysyłaj samym e-mailem.
- **Nie rejestruj firmy i niczego nie kupuj przed podpisaniem umowy z urzędem.** Zakupy sprzed umowy nie zostaną rozliczone.
