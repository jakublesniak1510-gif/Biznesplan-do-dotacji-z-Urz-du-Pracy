# 06 – Uzasadnienie zakupów (specyfikacja wydatków z dotacji)

> Typowe nazwy pola: „Szczegółowa specyfikacja wydatków wraz z uzasadnieniem”, „Uzasadnienie planowanych zakupów”, „Kalkulacja kosztów i źródła finansowania”.
> W wielu formularzach to **tabela z kolumną „uzasadnienie” przy każdej pozycji**. Wtedy stosujemy wariant pozycyjny (pkt 4). Liczby (kwoty, sumy, VAT) pochodzą zawsze z arkusza `Kosztorys` i `Do-wniosku`.

## 1. Cel sekcji

Dla **każdej pozycji kosztorysu** komisja chce wiedzieć:
1. **po co:** którą usługę z sekcji 01 umożliwia ta pozycja;
2. **dlaczego ta cena:** skąd kwota (oferta, porównanie, średnia rynkowa z K10);
3. **dlaczego nowy albo używany:** z uzasadnieniem (trwałość, gwarancja, higiena, cena);
4. **czy mieści się w katalogu wydatków** z regulaminu PUP (kategoria, limit %).

Ocenę kwalifikowalności robi **właściciel** na podstawie regulaminu konkretnego PUP. Model tylko opisuje zgodność, którą właściciel wskazał w danych.

## 2. Dane wejściowe

| Źródło | Dane |
|---|---|
| arkusz `Kosztorys` (przekazywany jako lista) | nazwa, kategoria, nowy/używany, ilość, kwota do rozliczenia, finansowanie (dotacja / wkład własny), link do oferty |
| arkusz – zmienne | `{{ark_kosztorys_dotacja}}`, `{{ark_kosztorys_wklad}}`, `{{ark_kosztorys_razem}}`, `{{ark_dotacja}}`, sumy kategorii `{{ark_kat_sprzet}}`, `{{ark_kat_towar}}`, `{{ark_kat_reklama}}`, `{{ark_kat_remont}}`, `{{ark_kat_inne}}` |
| K10 | uzasadnienie klienta: po co, z jakich ofert wybrał, dlaczego używany, co już ma (np. auto, laptop) |
| K5 | usługi, żeby powiązać zakup z usługą |
| notatka właściciela | wymogi regulaminu PUP: kategorie i limity, zasady dla sprzętu używanego (np. oświadczenie sprzedającego, zakaz zakupu od rodziny), wymóg ofert lub linków |

## 3. Struktura

**Wariant opisowy** (jedno pole tekstowe):
1. **Zdanie wprowadzające:** na co przeznaczę dotację (kategorie) i z czego sfinansuję resztę: `{{ark_kosztorys_dotacja}}` z dotacji i `{{ark_kosztorys_wklad}}` z wkładu własnego.
2. **Grupy zakupów** (np. sprzęt do usług, wyposażenie mobilne, towar, reklama). Przy każdej grupie: pozycje z kwotami przepisanymi z arkusza, po co, dlaczego taka cena, nowy czy używany.
3. **Zasoby, które już mam** (z K10): pokazują, że dotacja nie finansuje rzeczy zbędnych.
4. **Zgodność z regulaminem:** kategorie i limity (bez porad prawnych, tylko fakty od właściciela).

**Wariant pozycyjny** (kolumna „uzasadnienie” przy każdym wierszu), 200–400 znaków na pozycję:
`[po co – usługa] + [dlaczego ta cena – oferta/porównanie] + [nowy/używany – powód]`.

## 4. Długość – warianty

| Wariant | Znaki | Co zawiera |
|---|---|---|
| krótki | ~800 | kategorie z sumami (`{{ark_kat_…}}`), 1 zdanie „po co” na kategorię, informacja o sprzęcie używanym |
| standard | ~2000 | grupy z pozycjami i kwotami, po co, uzasadnienie ceny dla droższych pozycji, nowy/używany, zasoby własne |
| długi | ~4000 | każda pozycja osobno (po co, cena, porównanie ofert, nowy/używany), zasoby własne, zgodność z katalogiem i limitami |
| pozycyjny | 200–400 na pozycję | patrz pkt 3 |

## 5. Co punktuje komisja

- **Związek każdego zakupu z usługą.** Pozycja bez związku (np. laptop „do firmy” u fryzjerki bez wyjaśnienia) bywa wykreślana z kosztorysu.
- **Racjonalna cena:** średnia półka, porównanie co najmniej 2–3 ofert, linki. Najdroższy model wymaga uzasadnienia, a najtańszy budzi pytanie o trwałość.
- **Sprzęt używany z uzasadnieniem i dokumentami** (np. oświadczenie, że w ostatnich 7 latach nie kupiono go ze środków publicznych, umowa kupna-sprzedaży). Wymogi zależą od regulaminu PUP.
- **Brak pozycji niedozwolonych** w danym urzędzie (często: zakup od członków rodziny, wydatki przed podpisaniem umowy, opłaty administracyjne, czasem samochód powyżej limitu). Sprawdza to właściciel.
- **Zgodność z limitami kategorii** (np. towar do 30%, reklama do 20%) – kontrola w `Kosztorys!E33:E37`.
- **Wkład własny:** nawet jeśli regulamin go nie wymaga, pokazuje zaangażowanie wnioskodawcy.

## 6. Typowe błędy

- Kwoty w tekście inne niż w tabeli specyfikacji (zawsze przepisuj z `Do-wniosku`, sekcja 2).
- „Sprzęt niezbędny do prowadzenia działalności”: to zdanie pasuje do każdej pozycji i niczego nie wyjaśnia.
- Brak informacji, czy kwoty są netto czy brutto (zależy od statusu VAT: arkusz liczy „kwotę do rozliczenia”).
- Towar na sprzedaż opisany jak sprzęt (inna kategoria i inne limity).

## 7. Prompt sekcji

```text
SEKCJA 06 – UZASADNIENIE ZAKUPÓW
Napisz treść pola "{{pole_formularza}}" (limit: {{limit_znakow}}, ton: {{ton}},
format: {{opisowy | pozycyjny}}).
Dane o pozycjach bierzesz z listy <kosztorys> (nazwa, kategoria, nowy/używany, ilość, kwota,
finansowanie). Kwoty pozycji przepisuj dosłownie. Sumy – wyłącznie jako zmienne:
{{ark_kosztorys_dotacja}}, {{ark_kosztorys_wklad}}, {{ark_kat_…}}. NIE sumuj sam.
Przy każdej pozycji/grupie: (a) po co – którą usługę z K5 umożliwia; (b) dlaczego ta cena –
z K10 (oferty, porównanie); (c) nowy czy używany i dlaczego – z K10.
Dodaj zdanie o zasobach, które już mam (K10). Zgodność z regulaminem opisz tylko na podstawie
notatki właściciela (kategorie, limity, dokumenty dla sprzętu używanego).
Brak uzasadnienia ceny lub celu w K10 = [BRAK DANYCH: dlaczego ta oferta / do czego służy X].
Kwoty podawaj z dopiskiem "brutto" (zwolniony z VAT) albo "netto" (czynny VAT) – zgodnie z <parametry>.
Format pozycyjny: dla każdej pozycji osobny akapit 200–400 znaków, zaczynający się od nazwy pozycji.
```

## 8. Przykład wypełnienia – fryzjerka mobilna (dane zgodne z arkuszem przykładowym)

> **DANE FIKCYJNE – PRZYKŁAD.** Pozycje i kwoty pochodzą z przykładowego `model-finansowy-pup.xlsx` (arkusz `Kosztorys`). Klientka jest zwolniona z VAT, więc kwoty są brutto. Oferty i porównania cen w skrócie kwestionariusza są wymyślone.

**Skrót K10 i notatki właściciela:** Ma własny samochód (Skoda Fabia 2014) i telefon. Myjka przenośna: porównała 3 oferty (1 090–1 690 zł netto), wybrała środkową, bo ma podgrzewanie wody i zbiornik 20 l. Nożyczki: dwie pary ze stali japońskiej, bo tanie nożyczki tępią się po kilku miesiącach. Climazon (przyspiesza koloryzację): nowy kosztuje ok. 3 900 zł netto, a używany 1 500 zł od osoby prywatnej, sprawdzony na miejscu, z umową kupna-sprzedaży. Kasa fiskalna online: obowiązkowa od pierwszej sprzedaży usług fryzjerskich (informacja z biura rachunkowego). Sterylizator UV: wymóg higieny przy pracy u klientów. Towar: farby i oksydanty na pierwsze 2–3 miesiące, z hurtowni, z której korzystała w salonie. Reklama: oklejenie auta (auto jako „szyld” firmy mobilnej), strona z rezerwacją online. Regulamin PUP (notatka): towar do 30% dotacji, reklama do 20%, sprzęt używany dozwolony z oświadczeniem sprzedającego o niefinansowaniu ze środków publicznych w ostatnich 7 latach.

### Wariant standard (~2000 znaków), ton: ciepły

```text
Z dotacji przeznaczę {{ark_kosztorys_dotacja}} na sprzęt, materiały i reklamę potrzebne do pracy w domach klientów. Z wkładu własnego kupię za {{ark_kosztorys_wklad}} tablet i drukowane materiały reklamowe. Jestem zwolniona z VAT, więc podaję kwoty brutto.

Sprzęt do usług – {{ark_kat_sprzet}}. Do strzyżenia i stylizacji kupię nożyczki proste i degażówki (2 214 zł), maszynkę bezprzewodową z trymerem (1 353 zł), dwie suszarki (1 107 zł) oraz prostownicę z lokówką (861 zł). Nożyczki wybrałam ze stali japońskiej, bo tanie po kilku miesiącach się tępią i szarpią włosy. Do mycia głowy w domu klienta potrzebuję przenośnej myjki z podgrzewaniem wody (1 476 zł). Porównałam trzy oferty i wybrałam środkową, bo ma zbiornik 20 l. Klientka siedzi na składanym fotelu (799,50 zł), a przy słabym świetle pomoże lampa akumulatorowa (325,95 zł). Climazon (1 500 zł) skraca czas koloryzacji. Kupię go używanego od osoby prywatnej, bo nowy kosztuje ok. 3 900 zł netto. Przed zakupem sprawdzę go na miejscu i spiszę umowę, a sprzedająca złoży oświadczenie wymagane przez urząd. Narzędzia będę dezynfekować w sterylizatorze UV (1 107 zł). Sprzęt przewiozę w walizce z organizerami (738 zł). Kasa fiskalna online (2 214 zł) jest obowiązkowa od pierwszej usługi fryzjerskiej.

Materiały – {{ark_kat_towar}}. Farby, oksydanty i kosmetyki na pierwsze 2–3 miesiące kupię w hurtowni, z którą pracowałam w salonie. Pozostałe akcesoria – peleryny, ręczniki, szczotki i klipsy – kosztują {{ark_kat_inne}}.

Reklama – {{ark_kat_reklama}}. Oklejenie samochodu (2 214 zł) zastąpi mi szyld, bo firma mobilna nie ma witryny. Strona z rezerwacją online (2 460 zł) pozwoli klientkom umawiać się o każdej porze.

Mam już samochód i telefon, więc nie ujmuję ich w kosztorysie. Udział towaru i reklamy w dotacji mieści się w limitach regulaminu urzędu.
```

### Wariant pozycyjny – dwie przykładowe pozycje (200–400 znaków)

```text
Przenośna myjka do włosów z podgrzewaniem wody – 1 476 zł brutto, nowa. Pozwala umyć głowę w domu klientki bez dostępu do umywalki, co jest niezbędne przy koloryzacji. Porównałam trzy oferty (1 090–1 690 zł netto). Wybrałam środkową, bo ma podgrzewanie i zbiornik 20 l.

Climazon przenośny – 1 500 zł, używany, od osoby prywatnej. Skraca czas działania farby, więc w ciągu dnia obsłużę więcej klientek. Nowy kosztuje ok. 3 900 zł netto. Używany sprawdzę przed zakupem, zawrę umowę kupna-sprzedaży i dołączę oświadczenie sprzedającej wymagane przez urząd.
```

### Na co zwrócić uwagę w przykładzie

- Kwoty pozycji są przepisane z arkusza, a sumy kategorii i finansowania podane jako zmienne `{{ark_…}}`. Model niczego nie zsumował.
- Każda pozycja ma swoje „po co”, a droższe pozycje także uzasadnienie ceny.
- Zdanie o limitach opiera się na notatce właściciela i na kontroli w arkuszu (`Kosztorys!E33:E37` = OK).
- „Niezbędne” pojawia się tylko raz, z konkretnym powodem (mycie bez umywalki).
