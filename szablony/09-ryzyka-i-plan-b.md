# 09 – Ryzyka i plan B

> Typowe nazwy pola: „Analiza ryzyka”, „Zagrożenia dla realizacji przedsięwzięcia i sposoby ich ograniczenia”, „Co zrobi Pan/Pani, jeśli…”, „Plan awaryjny”.
> Ta sekcja rozwija zagrożenia i słabe strony z SWOT (07) oraz scenariusz pesymistyczny z prognozy (08).

## 1. Cel sekcji

Pokazać komisji, że:
1. wiesz, **co konkretnie może pójść nie tak** w Twojej firmie;
2. masz **działania zapobiegawcze** zaplanowane już teraz;
3. masz **plan B**, czyli to, co zrobisz, jeśli ryzyko się zmaterializuje;
4. utrzymasz działalność przez okres wymagany umową z PUP (zwykle co najmniej 12 miesięcy). Od tego zależy, czy nie trzeba będzie zwracać dotacji.

## 2. Dane wejściowe

| Źródło | Dane |
|---|---|
| K12 | ryzyka wskazane przez klienta + jego pomysły na zapobieganie i plan B |
| K7 | sezonowość (ryzyko słabych miesięcy) |
| K8 | konkurencja (ryzyko reakcji konkurentów) |
| K10, arkusz `Koszty` | ubezpieczenie, rezerwy, sprzęt zapasowy |
| K11 | wkład własny, oszczędności, inne dochody gospodarstwa |
| arkusz | `{{ark_zysk_netto_mies_pes}}`, `{{ark_min_saldo_pes}}`, `{{ark_prog_rent_zl}}` – liczby scenariusza −30% |
| sekcja 07 | lista zagrożeń i słabych stron, żeby zachować spójność |

## 3. Struktura

1. **Zdanie wprowadzające:** ile ryzyk zidentyfikowałeś i jak je oceniasz. Bez dramatyzowania i bez bagatelizowania.
2. **Tabela ryzyk** (4–6 wierszy) albo akapity, jeśli pole nie przyjmuje tabel:

   | Ryzyko | Co by się stało | Jak zapobiegam | Plan B |
   |---|---|---|---|

   Typowe grupy ryzyk do sprawdzenia w K12: **popyt** (mniej klientów, sezon), **zdrowie i dostępność** (choroba, jedna osoba w firmie), **sprzęt i lokal** (awaria, kradzież, wypowiedzenie najmu), **koszty** (wzrost cen materiałów, paliwa), **konkurencja**, **formalne** (uprawnienia, przepisy branżowe, RODO).
3. **Scenariusz finansowy −30%:** jedno lub dwa zdania z liczbami z arkusza i odesłaniem do sekcji 08.
4. **Utrzymanie działalności przez okres umowy:** z czego pokryjesz koszty w najgorszym miesiącu (oszczędności, dochody domowe z K11).

Kolumny „prawdopodobieństwo” i „wpływ” dodawaj tylko wtedy, gdy formularz ich wymaga. Ocenę bierz z K12 albo od właściciela. Model sam jej nie nadaje.

## 4. Długość – warianty

| Wariant | Znaki | Co zawiera |
|---|---|---|
| krótki | ~800 | 3 najważniejsze ryzyka w zdaniach (ryzyko → zapobieganie → plan B), 1 zdanie o scenariuszu −30% |
| standard | ~2000 | tabela 4–5 ryzyk + scenariusz −30% + utrzymanie przez okres umowy |
| długi | ~4000 | tabela 6 ryzyk z rozwinięciem, osobny akapit o każdym ryzyku krytycznym, sygnały ostrzegawcze (po czym poznam, że ryzyko się realizuje: np. „mniej niż X rezerwacji na kolejny miesiąc” – tylko z K12), harmonogram reakcji |

## 5. Co punktuje komisja

- **Ryzyka specyficzne dla branży i klienta**, a nie ogólne („kryzys gospodarczy”).
- **Plan B, który da się wykonać** zasobami z wniosku (sprzęt, umiejętności, kontakty).
- **Spójność z SWOT i prognozą:** te same zagrożenia, a w scenariuszu −30% te same liczby co w arkuszu.
- **Świadomość obowiązków wobec PUP:** utrzymanie działalności, rozliczenie dotacji, przechowywanie dokumentów zakupów.

## 6. Typowe błędy

- „Nie przewiduję ryzyk” albo „ryzyko jest minimalne”.
- Plan B: „zamknę firmę” albo „poszukam pracy na etacie”. Komisja czyta to jako zapowiedź zwrotu dotacji.
- Plan B oparty na zasobach, których klient nie ma (np. „zatrudnię pracownika” bez pieniędzy na to w prognozie).
- Liczby scenariusza −30% inne niż w arkuszu.

## 7. Prompt sekcji

```text
SEKCJA 09 – RYZYKA I PLAN B
Napisz treść pola "{{pole_formularza}}" (limit: {{limit_znakow}}, ton: {{ton}},
format: {{tabela | tekst}}).
Kolejność: (1) zdanie wprowadzające; (2) 4–6 ryzyk z K12 (uzupełnione o sezonowość z K7 i
konkurencję z K8, jeśli tam są) – dla każdego: co by się stało, jak zapobiegam, plan B –
WYŁĄCZNIE działania z K12/K10/K11; (3) scenariusz −30%: {{ark_zysk_netto_mies_pes}},
{{ark_min_saldo_pes}} + odesłanie do części finansowej; (4) jak utrzymam firmę przez okres
umowy z urzędem – źródła z K11.
Nie przypisuj prawdopodobieństwa ani wpływu, jeśli nie podano ich w K12.
Jeśli dla ryzyka brak planu B w K12 – [BRAK DANYCH: co zrobię, gdy …].
Plan B nie może zakładać zamknięcia firmy ani podjęcia pracy na etacie w okresie umowy.
Spójność z sekcją 07: te same zagrożenia, te same nazwy.
```

## 8. Przykład wypełnienia – fotograf

> **DANE FIKCYJNE – PRZYKŁAD.** Osoby i firmy są wymyślone. Zmienne `{{ark_…}}` podstawia system z arkusza tego klienta.

**Skrót K12/K10/K11:** (1) Sezonowość: śluby głównie od maja do września; od listopada do marca mało zleceń, więc wtedy sesje świąteczne w domach klientów, zdjęcia dla firm i nieruchomości (całoroczne). (2) Awaria aparatu w dniu ślubu: drugi korpus i drugi obiektyw w kosztorysie; serwis w mieście wojewódzkim. (3) Choroba w dniu ślubu: porozumienie o wzajemnych zastępstwach z fotografką z Borkowa (Ola M.); zapis w umowie z parą o fotografie zastępczym. (4) Utrata zdjęć: kopia na dwóch dyskach i w chmurze (abonament w kosztach stałych) w dniu zlecenia. (5) Mniej ślubów niż w planie: rezerwacje z wyprzedzeniem i zaliczka przy podpisaniu umowy; jeśli mimo to będzie ich mniej – więcej zdjęć dla biur nieruchomości (3 biura zainteresowane), sesje rodzinne. (6) Dron: każdy lot sprawdzany pod kątem stref w aplikacji, zgoda właściciela terenu; ubezpieczenie OC operatora drona w kosztach. K11: żona pracuje na etacie, oszczędności 6 000 zł poza wkładem własnym.

### Wariant standard (~2000 znaków, z tabelą), ton: ciepły

```text
Najbardziej obawiam się kilku rzeczy, które w fotografii zdarzają się naprawdę: sezonowości ślubów, awarii sprzętu i choroby w dniu, którego nie da się powtórzyć. Na każdą z nich mam przygotowany sposób.

| Ryzyko | Co by się stało | Jak zapobiegam | Plan B |
|---|---|---|---|
| Mało zleceń od listopada do marca | spadek przychodów zimą | zdjęcia dla firm i biur nieruchomości przez cały rok | sesje świąteczne w domach klientów, więcej zleceń od trzech zainteresowanych biur |
| Awaria aparatu w dniu ślubu | przerwana relacja | pracuję na dwóch korpusach i mam drugi obiektyw | dokończenie relacji na zapasowym sprzęcie, naprawa w serwisie w mieście wojewódzkim |
| Moja choroba w dniu ślubu | para bez fotografa | porozumienie o zastępstwach z fotografką z Borkowa, zapis w umowie z parą | zastępstwo przez fotografkę z Borkowa |
| Utrata zdjęć | brak pamiątki ze ślubu, utrata zaufania | kopia na dwóch dyskach i w chmurze w dniu zlecenia | odtworzenie z kopii |
| Mniej ślubów niż planuję | niższe przychody latem | rezerwacje z wyprzedzeniem, zaliczki | więcej sesji rodzinnych i zleceń dla firm |
| Loty dronem | kara lub szkoda | sprawdzam strefy przed każdym lotem, mam zgodę właściciela terenu i ubezpieczenie OC operatora | rezygnacja z ujęć z powietrza w danym miejscu |

Sprawdziłem też, co się stanie, jeśli przychody będą o 30% niższe od planu. Zysk netto wyniesie wtedy średnio {{ark_zysk_netto_mies_pes}} miesięcznie, a najniższe saldo gotówki {{ark_min_saldo_pes}}. Szczegóły opisuję w części finansowej.

Firmę zamierzam prowadzić znacznie dłużej niż wymaga umowa z urzędem. Na najsłabsze miesiące mam 6 000 zł oszczędności poza wkładem własnym, a domowe wydatki pokrywa w tym czasie pensja żony.
```

### Na co zwrócić uwagę w przykładzie

- Każde działanie w tabeli pochodzi z K12, K10 lub K11. Model nie wymyślił np. „ubezpieczenia sprzętu”, którego klient nie podał.
- Plan B nie zakłada zamknięcia firmy.
- Liczby scenariusza −30% są zmiennymi, identycznymi jak w sekcji 08.
- Ryzyka mają te same nazwy co zagrożenia w sekcji 07 tego klienta. Gdy SWOT i ryzyka powstają w osobnych wywołaniach, przekaż modelowi listę zagrożeń z 07 jako kontekst.
