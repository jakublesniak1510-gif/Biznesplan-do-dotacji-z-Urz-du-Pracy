# Wspólne sekcje formularzy PUP 2026 – porównanie 8 wniosków

Próba: 8 formularzy z 8 województw, pobranych w październiku 2026:
**NS** Nowa Sól (lubuskie) · **PO** Poznań (wielkopolskie) · **WA** Warszawa (mazowieckie) · **KR** Kraków (małopolskie) · **ŁÓ** Łódź (łódzkie) · **GD** Gdańsk (pomorskie) · **RZ** Rzeszów (podkarpackie) · **SZ** Szczecin (zachodniopomorskie).
Szczegóły pól są w plikach `[pup_id]-pola.md`. Szablony to `szablony/01–09`.

## 1. Czy formularze mają limity znaków?

**Żaden z 8 formularzy nie podaje limitu znaków.** Ograniczenia są inne:

| Rodzaj ograniczenia | Urzędy | Co to znaczy dla nas |
|---|---|---|
| Wprost „dowolna liczba znaków” | KR (pkt II.4) | Można dać wariant standard |
| **Zakaz zmiany układu i poszerzania wierszy** (liczy się wielkość ramki) | SZ (najostrzej), ŁÓ („bez zmiany szaty graficznej”), PO („bez edycji tekstu na stronach”) | Tekst musi zmieścić się w ramce wydruku, więc wariant krótki albo punkty. Długość trzeba zmierzyć na konkretnym PDF/DOCX |
| Wymóg kroju pisma | WA (Arial 12, interlinia 1,3 – z Zasad) | Przy przepisywaniu do .doc trzymamy ten format |
| Forma odpowiedzi | WA („pytanie–odpowiedź, z zachowaniem kolejności podpunktów”), RZ (zakaz „nie dotyczy”/„brak”) | Generator musi zachować numerację podpunktów i nie zostawiać pustych pól |
| Liczba pozycji w tabelach | KR 13 zakupów, SZ 20 zakupów i 13 kosztów, NS 30 kosztów | Specyfikację dzielimy albo powielamy załącznik |
| Format pliku | KR, ŁÓ, SZ: PDF płaski bez pól formularza; NS, GD, WA: .doc; PO, RZ: .docx | Przy PDF klient wypełnia ręcznie albo przepisujemy treść, więc dostarczamy tekst gotowy do przepisania |

## 2. Macierz sekcji: gdzie występują i pod jaką nazwą

✔ = osobne pole · ◐ = częściowo (wplecione w inne pole, tylko wybór X albo w załączniku) · – = brak

| Sekcja | NS | PO | WA | KR | ŁÓ | GD | RZ | SZ | Ile (✔/◐) | Szablon |
|---|---|---|---|---|---|---|---|---|---|---|
| Opis działalności, produkty i usługi | ✔ IV.4, IV.7 | ✔ 23a (z cennikiem) | ✔ II.1.1–4 | ✔ II.2 + II.4a | ✔ IV.a | ✔ III.4 | ✔ II.2a | ✔ II.4 + VII | **8/8** | 01 |
| Motywy podjęcia działalności | ◐ IV.4 | – | ✔ II.1.2, II.1.5 | – | – | ✔ III.8 | ✔ II.2b | – | 3 + 1 | 01 |
| Uprawnienia, pozwolenia, koncesje | ✔ IV.3 | ✔ 23c | ✔ II.1.8 | ◐ II.4e | ✔ IV.b | ✔ IV.2 | ✔ II.2e | ◐ III.9 | 6 + 2 | 01 / 02 |
| Wykształcenie, szkolenia, doświadczenie | ✔ VII (tabele) | ✔ 26a–f (tabele z godzinami) | ✔ I.11–12 + CV | ✔ II.4e | ✔ III.6–7 (u doradcy) | ✔ IV.4 | ✔ II.4a–d | ✔ III.9 | **8/8** | 02 |
| Wcześniejsza działalność | ✔ | ✔ (+ nierejestrowana) | ✔ | ✔ | ✔ | ✔ | ✔ (także za granicą) | ✔ | **8/8** | 02 |
| Klienci, odbiorcy, popyt | ✔ IV.10 | ◐ 23b (X) + 27c | ✔ II.2.1–3 + II.1.6/9 (dane ze źródłami) | ✔ II.4b | ✔ IV.c | ✔ III.6 | ✔ II.6a–d | ✔ V.1b | 7 + 1 | 03 |
| Kontakty, listy intencyjne, umowy przedwstępne | ✔ IV.9 | ✔ 23b + zał. 11a/b | ✔ II.2.4, II.5.3 | ✔ II.4c | ✔ III.8 | ◐ tylko załącznik | ✔ II.6c | ✔ V.1a–b | 7 + 1 | 03 |
| Konkurencja | ◐ w IV.10 | ◐ checklista 27c | ✔ II.1.10–11 (**3 firmy**) | ✔ III.1 | ✔ IV.e | – | ✔ II.5 (**3 firmy × 5 cech**) | ✔ V.3 | 5 + 2 | 04 |
| Marketing, promocja, pozyskanie klientów | ✔ IV.12 | ◐ 23d (kanał, X) | ✔ II.2.4–5 + zał. 1 | ◐ II.4b | ✔ IV.d | ✔ III.7 | ✔ II.7 | ✔ V.2 | 6 + 2 | 05 |
| Opis lokalu i lokalizacji | ✔ VI | ✔ 25 (szczegółowa tabela) | ✔ II.3.1–7 | ✔ II.5 | ✔ III.3 | ✔ IV.1 | ✔ III.1–2 | ✔ IV.1e | **8/8** | 01 |
| Plusy i minusy lokalizacji / mocne i słabe strony | ◐ IV.8 atuty | – | ✔ II.3.6 | – | – | – | ✔ III.2a | ◐ V.3 (konkurenci) | 2 + 2 | 07 |
| **Pełna analiza SWOT** | – | – | ✔ zał. 2 | – | – | – | – | – | **1/8** | 07 |
| **Ryzyka i działania zaradcze** | – | – | ◐ (SWOT) | ◐ III.3 („wydarzenia na rynku”) | ✔ IV.f | – | – | – | **1 + 2** | 09 |
| Działania już podjęte, przygotowania | – | – | ◐ zał. 1 | ✔ II.4d | ✔ III.5 | ◐ tytuł IV | – | ✔ VII | 3 + 2 | 01 / 05 |
| Plany rozwoju | – | – | ✔ II.1.3 | – | – | – | – | ✔ VII | 2/8 | 01 |
| Innowacyjność | – | ◐ 27c | – | – | – | – | ✔ II.2d | – | 1 + 1 | 01 / 04 |
| Planowane zatrudnienie | ✔ IV.11 | – | ✔ II.5.2 | – | – | ✔ IV.3 | ✔ II.8 | – | 4/8 | 01 |
| Specyfikacja wydatków (tabela) | ✔ IX (3 kategorie) | ✔ 29 | ✔ zał. 4 | ✔ IV | ✔ V | ✔ V | ✔ V.2 (9 kategorii, dostawca) | ✔ zał. 2/2 (bez marki) | **8/8** | 06 |
| **Uzasadnienie każdego zakupu** | ✔ X | ✔ osobny zał. (1) | ✔ zał. 4 | ✔ kolumna IV | ✔ V | ✔ VI | ✔ V.5 | – | **7/8** | 06 |
| Kalkulacja kosztów ze źródłami (dotacja / własne / inne) | ✔ XI | ✔ 30 | ◐ I.17 | ✔ III.2 | ✔ V | ◐ V | ✔ V.2 | ✔ zał. 1 | 6 + 2 | 06 / 08 |
| Wkład własny, posiadane zasoby | ✔ XI (6 mies. wstecz) | ✔ 30B–C | ✔ I.17 | ✔ III.2 | ✔ V | – | ✔ III.4 | ✔ IV.2a–d | 7/8 | 06 / 08 |
| Prognoza – tabela 12 miesięcy | ✔ VIII | ✔ 27a–b | ✔ zał. 3 | ✔ III.3 | – (średnia mies.) | – (miesiąc + rok) | – (miesiąc + rok) | ✔ zał. 3/1 | 5/8 (3 inne) | 08 |
| **Uzasadnienie założeń prognozy (tekst)** | ✔ | ✔ 27c (checklista + tekst) | ✔ zał. 3 | ✔ kolumna | ✔ „sposób obliczenia” | ✔ | ✔ 3 osobne pola (A, B, C–F) | ✔ zał. 3/2 | **8/8** | 08 |
| Cennik, przykładowe ceny | – | ✔ 23a | – | – | – | – | ✔ II.6d | – | 2/8 | 03 / 08 |
| Ekologia / DNSH | – | – | ✔ II.4 + oświadczenia | – | – | – | – | ◐ zakaz paliw kopalnych (zał. 2/1) | 1 + 1 | **brak** |
| Forma zabezpieczenia | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | 8/8 | – |

## 3. Mapowanie na szablony 01–09

| Szablon | W ilu formularzach ma własne pole | Typowe nazwy pól | Uwagi |
|---|---|---|---|
| **01** Opis działalności | 8/8 | „Opis planowanej działalności”, „Specyfika działalności”, „Główny cel przedsięwzięcia”, „Dane dotyczące produktów lub usług”, „Uzasadnienie do wniosku” | Najczęściej dzielony na 2–5 podpól (cel, oferta, motywy, uprawnienia, lokal). Generator musi umieć pociąć tekst według podpunktów |
| **02** Kwalifikacje | 8/8 | „Wiedza i przygotowanie wnioskodawcy”, „Informacje o wykształceniu, szkoleniach, doświadczeniu”, „Przygotowanie właściciela” | Często w **tabelach** (okres, pracodawca, stanowisko, godziny szkolenia). W ŁÓ i SZ dane muszą też być w systemie PUP (u doradcy) |
| **03** Rynek i klienci | 7/8 (+PO checklista) | „Odbiorcy”, „Analiza rynku odbiorców”, „Klient planowanego przedsięwzięcia”, „Specyfika klientów” | WA wymaga **danych liczbowych ze źródłami**. RZ pyta, „na jakiej podstawie stwierdzono zapotrzebowanie” |
| **04** Konkurencja | 5/8 osobno (+2 częściowo) | „Opis konkurencji – min. 3 przykłady”, „Rozeznanie istniejących firm”, „Analiza konkurencji” | WA i RZ: **co najmniej 3 konkretne firmy** (RZ: z adresem, pozycją, cenami i sposobem rywalizacji). W GD brak pola |
| **05** Marketing | 6/8 (+2) | „Sposób promocji i reklamy”, „Opis działań reklamowo-promocyjnych”, „Metoda wejścia na rynek” | WA dokłada plan działań (zał. 1) |
| **06** Uzasadnienie zakupów | 7/8 | „Uzasadnienie celowości i przeznaczenia każdego zakupu”, „Uzasadnienie do planowanych wydatków” | Forma: kolumna tabeli (KR), osobny załącznik (PO, WA) albo tekst ciągły (GD, RZ, ŁÓ). SZ: brak pola i nazwa sprzętu bez marki |
| **07** SWOT | **1/8** (WA zał. 2) | „Analiza SWOT” | Gdzie indziej tylko jako „plusy i minusy lokalizacji” (WA, RZ), „atuty firmy” (NS), „mocne i słabe strony konkurentów” (SZ). Treść 07 służy głównie jako **ściągawka na rozmowę z komisją** i źródło zdań do innych pól |
| **08** Prognoza – opis | 8/8 | „Uzasadnienie przyjętych założeń”, „Sposób obliczenia wysokości przychodu”, „Wyjaśnienia i obliczenia” | Trzy formaty tabel: 12 miesięcy (5), średnia miesięczna (ŁÓ), miesiąc + rok (GD, RZ). Arkusz musi eksportować wszystkie trzy |
| **09** Ryzyka i plan B | **1/8** (ŁÓ IV.f) | „Potencjalne ryzyka wraz z propozycją działań zaradczych” | Częściowo w KR (kolumna „wydarzenia na rynku”). Karty oceny (np. Turek: ryzyka 0–2 pkt) i rozmowy z komisją pytają o ryzyka częściej niż formularze |

## 4. Wnioski produktowe (przewaga nad konkurencją)

1. **Jeden biznesplan nie pasuje do wszystkich urzędów.** Ten sam projekt trzeba pociąć na od 3 (PO, SZ) do ponad 30 (WA) pól. Firmy konkurencyjne sprzedają jeden ogólny dokument. My dostarczamy treść **pole po polu z numeracją danego PUP** (szablon 10 – mapowanie).
2. **Trzy brakujące bloki treści** w naszych szablonach:
   - **Ekologia / DNSH** (WA II.4 i 4 oświadczenia; SZ zakaz urządzeń na paliwa kopalne). Zasada DNSH pochodzi z EFS+, więc może się pojawić w innych projektach unijnych.
   - **Działania już podjęte** (KR II.4d, ŁÓ III.5, SZ VII): krótka lista faktów (umowa najmu, oferty, rozmowy z klientami, szkolenie).
   - **Plany rozwoju i cennik** (WA II.1.3, SZ VII, PO 23a, RZ II.6d): 2–3 zdania o planach i tabela cen średnich.
3. **SWOT i ryzyka (07, 09) rzadko mają własne pole** (po 1 na 8), ale są oceniane w kartach i na rozmowach (NS obowiązkowa prezentacja, TY rozmowa w punktacji, GD/SZ/RZ „przy wątpliwościach”). Sprzedajemy je jako **przygotowanie do rozmowy**, a w formularzu zostawiamy tylko skrót.
4. **Konkurencja „z nazwiska”**: WA i RZ wymagają 3 realnych firm (RZ z adresem i cenami). Kwestionariusz klienta powinien zbierać nazwy konkurentów, a jeśli ich nie ma, wyszukujemy je sami.
5. **Tryb „ramka”**: w PO, ŁÓ i SZ obowiązuje zakaz poszerzania pól. Generator potrzebuje parametru „maks. N znaków na pole”. Wartość mierzymy na wydruku konkretnego formularza (szablon 10, krok 3) i zapisujemy w bazie przy pierwszym zleceniu z danego PUP.
6. **Dane z systemu PUP**: w ŁÓ i SZ kwalifikacje muszą być wpisane u doradcy przed złożeniem wniosku, a w GD, NS, RZ i Słupsku obowiązuje rozmowa z doradcą przed złożeniem. Wysyłamy klientowi checklistę „przed złożeniem” dla jego urzędu.
