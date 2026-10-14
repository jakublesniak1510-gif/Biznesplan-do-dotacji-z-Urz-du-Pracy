@@ naglowek
# Kosztorys i prognoza – firma sprzątająca, PUP Kolbuszowa (EFS+)

> **DANE FIKCYJNE – PRZYKŁAD.** Wszystkie liczby w tabelach pochodzą z `model.xlsx` w tym katalogu (kopia `model-finansowy/model-finansowy-pup.xlsx` z danymi klientki, przeliczona przez LibreOffice `/usr/bin/soffice --headless --convert-to xlsx`). Plik wygenerował `przyklady/narzedzia/kosztorys_md.py`.
>
> Zasady: „Informacja dotycząca zasad udzielania dofinansowania podjęcia działalności gospodarczej w ramach projektu »Aktywizacja osób bezrobotnych z powiatu kolbuszowskiego (III)«” (EFS+, FE dla Podkarpacia 2021–2027), 2026 r., pkt 13: wykluczone m.in. remonty i adaptacje, transport zakupów, opłaty eksploatacyjne, szkolenia, samochód osobowy (poza nauką jazdy i taxi), środek transportu powyżej 50% dofinansowania, towary powyżej 30% dofinansowania, rzeczy używane od firm niehandlujących używanym sprzętem, kasa fiskalna, ubezpieczenia, telefon/tablet powyżej 2 000 zł, **wydatki reklamowe powyżej 2 000 zł**, doradztwo powyżej 1 000 zł, współwłasność. Ostatni nabór: 6–7.07.2026, do 40 000 zł.

@@ kosztorys_intro
Klientka jest zwolniona z VAT – „do rozliczenia” = brutto. Linki: wyszukiwarka ofert Ceneo dla konkretnych modeli Kärcher i Unger (oferty typu); środki czystości, oklejenie, strona i druk – oferty lokalnych wykonawców do dołączenia.

**Dlaczego część zakupów jest z wkładu własnego:** karta oceny Kolbuszowej punktuje udział środków własnych w całkowitych kosztach przedsięwzięcia: 5–14,99% = 8 pkt, 15–24,99% = 12 pkt, od 25% = 16 pkt; formularz wymaga min. 5%. Parownica, zestaw Unger, drabina, ulotki, odzież i druga część chemii (razem 5 350,50 zł) idą z oszczędności klientki. Udział: 5 350,50 ÷ 30 200,50 = 17,7% → przedział 12 pkt. Próg 25% wymagałby ok. 2 900 zł więcej wkładu (przy tej samej dotacji) – klientka woli zostawić rezerwę 2 650 zł na start. To świadoma decyzja, opisana klientce.

**Limity:** towar 2 218 zł = 8,9% dofinansowania (limit 30%). Każdy wydatek reklamowy poniżej 2 000 zł: oklejenie 1 599 zł, strona 1 845 zł (z dotacji), ulotki 553,50 zł (wkład). Brak telefonu, kasy, samochodu, rzeczy używanych.

@@ limity
W arkuszu: towar 30%, remont 0% (wykluczony), reklama 100% – limit Kolbuszowej jest kwotowy na każdy wydatek (≤ 2 000 zł), a nie procentowy, więc sprawdzono go ręcznie (wyżej). Sprzęt i inne – bez limitu.

@@ przychody
Ceny i liczba zleceń przy pełnym obłożeniu – kwestionariusz 3.2. Listy intencyjne (biuro 2 razy w tygodniu, gabinet 3 razy, 2 klatki co tydzień) dają ok. 30 wizyt miesięcznie od startu; resztę planu (kolejne biuro i 2–3 klatki) klientka pozyska w pierwszych miesiącach – stąd rozruch 50% / 70% / 85%. Sezonowość z 3.5 i 13.2 (okna wiosną i przed świętami, słabiej latem). Czas pracy z klientami: 21 dni × 7 h; obłożenie maks. 86% w grudniu – plan wykonalny dla jednej osoby, ale bez dużego zapasu (zob. ryzyko zdrowotne w sekcji 09 wniosku).

@@ koszty
Paliwo 400 zł – krótkie trasy w promieniu 15 km (kwestionariusz 13.3). OC 60 zł – wycena ubezpieczyciela podana przez klientkę. Środki czystości zużywane w usługach: 7% przychodu (klientka: 5–7%, przyjęto górną granicę). Brak czynszu i mediów – sprzęt w garażu własnym.

@@ pesymistyczny
Wariant: przychody o 30% niższe w każdym miesiącu, koszty stałe i ZUS bez zmian. Firma nadal ma zysk netto. Najniższe saldo gotówki (2 650 zł) jest takie samo w obu wariantach, bo przypada na start – po zakupach z dotacji i wkładu, przed pierwszym przychodem. Klientka nie ma innych dochodów; wydatki domowe ok. 2 000 zł miesięcznie (kwestionariusz 10.4) – zysk netto w wariancie pesymistycznym jest od nich wyższy, ale w pierwszym miesiącu (rozruch 50%) trzeba je pokryć z rezerwy. Działania na wypadek niższych przychodów (rozmowa 14.10.2026): więcej okien i mieszkań, ulotki w nowych blokach, rozmowa z zarządcą spółdzielni o klatkach.

@@ uproszczenia
### Uproszczenia modelu

- Start 1.03.2027 – 12 miesięcy przypada na 2027–2028 r., a arkusz liczy na stałych z 2026 r. Po ogłoszeniu wskaźników na 2027 r. zaktualizować `Stale-2026` i wygenerować plik ponownie.
- Ryczałt 8,5% dla wszystkich usług sprzątania [do weryfikacji z księgową: stawka dla PKWiU 81.21 i 81.22].
- Brak amortyzacji sprzętu z dotacji – podatek raczej zawyżony.
- Kasa fiskalna: arkusz jej nie zawiera. Obowiązek zależy od obrotu z osobami prywatnymi – jeśli powstanie, kasę klientka kupi z własnych środków (Kolbuszowa jej nie finansuje).

@@ docx_tytul
# Treści do wniosku o dofinansowanie podjęcia działalności gospodarczej
Powiatowy Urząd Pracy w Kolbuszowej – projekt „Aktywizacja osób bezrobotnych z powiatu kolbuszowskiego (III)”, EFS+
Wzór wniosku obowiązujący od 16.06.2026 · kolejny nabór: do ogłoszenia
Wnioskodawczyni: Bożena [nazwisko] – **DANE FIKCYJNE – PRZYKŁAD**
Działalność: usługi sprzątania, PKD 81.21.Z (+ 81.22.B, 96.10.Z) · Kwota: 24 850,00 zł

@@ docx_samemu
- **Wzór wniosku:** pobierz z kolbuszowa.praca.gov.pl → Dokumenty do pobrania wersję z ogłoszenia naboru (ten przykład – wzór od 16.06.2026).
- **Nagłówek i część III:** imię i nazwisko, adres zamieszkania i do doręczeń, PESEL, NIP („brak”), telefon, e-mail, adres do e-Doręczeń (jeśli masz). Pkt 11–14: wcześniejsza działalność w Polsce i za granicą („nie prowadziłam”), dotacje i umorzenie pożyczki („nie”).
- **Tabela pkt 10:** wpisz pełne nazwy zakładów pracy z świadectw pracy.
- **Okres prowadzenia działalności:** zaznacz „co najmniej 18 miesięcy” (10 pkt) – to Twoje zobowiązanie w umowie.
- **IX. Zabezpieczenie:** zaznacz „poręczenie”. Syn i brat (dochód netto min. 4 100 zł każdy po odjęciu rat) wypełniają „Oświadczenie poręczyciela” na druku urzędu; syn potwierdza je w zakładzie pracy, brat dołącza decyzję o emeryturze lub waloryzacji. Synowa i bratowa wyrażają zgodę osobiście w urzędzie.
- **Oświadczenia na końcu wniosku:** zaznacz właściwe kratki (np. „nie byłam skazana”, „nie wykonywałam działalności”) i podpisz. Objaśnienia: `co-wpisac-samemu.md`. Składasz je pod rygorem odpowiedzialności karnej.
- **Formularz informacji przy ubieganiu się o pomoc de minimis** i oświadczenie o pomocy de minimis z ostatnich 3 lat.
- **Dołącz:** dyplom ZSZ, świadectwa pracy, zaświadczenie ze szkolenia z szorowarki (jeśli znajdziesz – jeśli nie, usuń to zdanie z sekcji 02), kopię prawa jazdy i dowodu rejestracyjnego Dacii, dokument garażu (spółdzielcze prawo), 3 listy intencyjne, oferty do każdej pozycji tabeli VI, załącznik własny „Analiza SWOT i analiza ryzyka” (sekcje 07 i 09).
- **IPD:** dotacja musi być w Twoim Indywidualnym Planie Działania – jest.
- **Podpis:** na wniosku i oświadczeniach (papier albo e-podpis zgodnie z ogłoszeniem).
- **Nie zakładaj firmy i nic nie kupuj przed podpisaniem umowy.** Działalność rozpoczynasz w ciągu 30 dni od otrzymania środków.
