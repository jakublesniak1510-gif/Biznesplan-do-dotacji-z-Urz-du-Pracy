# 11 – Przygotowanie do uzupełnień i rozmowy z komisją

Plik ma dwie części:
- **A.** Szablon odpowiedzi na **wezwanie urzędu do uzupełnienia lub wyjaśnienia wniosku** (pismo od PUP z terminem).
- **B.** **20 najczęstszych pytań komisji** (w urzędach, które zapraszają na rozmowę) i instrukcja, jak klient ma się przygotować, żeby odpowiadać **własnymi słowami**.

---

## A. Odpowiedź na wezwanie do uzupełnienia wniosku

### A1. Zasady

1. **Termin jest w piśmie** (zwykle 7–14 dni). Liczy się dzień doręczenia. Po terminie wniosek może zostać pozostawiony bez rozpatrzenia. Pierwsze, co robimy po otrzymaniu wezwania: wpisujemy termin do kalendarza i ustalamy z klientem, jak złoży odpowiedź (osobiście, pocztą, przez praca.gov.pl lub ePUAP – zgodnie z pismem).
2. **Odpowiadamy punkt po punkcie,** w tej samej kolejności i z tą samą numeracją co w wezwaniu. Nie dodajemy rzeczy, o które urząd nie pytał.
3. **Spójność liczb.** Jeśli uzupełnienie zmienia kosztorys, kwotę dotacji albo prognozę, **najpierw poprawiamy arkusz** (`model-finansowy-pup.xlsx`): `Kosztorys`, a potem przeliczenie i kontrole w `Zalozenia`. Dopiero potem przepisujemy nowe tabele z `Do-wniosku`. Model językowy nie przelicza kwot w piśmie.
4. **Fakty tylko od klienta.** Gdy urząd prosi o wyjaśnienie (np. „skąd przyjęto liczbę klientów”), odpowiedź opiera się na kwestionariuszu i nowych informacjach od klienta. Jeśli ich brakuje, w szkicu zostaje `[BRAK DANYCH: …]` i pytamy klienta.
5. **Klient podpisuje i składa pismo sam.** My przygotowujemy treść.

### A2. Typy wezwań i jak reagować

| Typ | Przykład z pisma | Co robimy |
|---|---|---|
| brak dokumentu / załącznika | „brak oferty cenowej dla poz. 8”, „brak tytułu prawnego do lokalu” | lista załączników do dostarczenia przez klienta. W piśmie tylko: „W załączeniu przedkładam…” |
| błąd formalny | brak podpisu, data, niewypełnione pole | klient poprawia na formularzu. W piśmie tylko informacja, co poprawiono |
| prośba o wyjaśnienie | „proszę uzasadnić koszt paliwa 700 zł/mies.”, „skąd liczba 30 usług miesięcznie” | odpowiedź merytoryczna 300–1 200 znaków na punkt, według szablonu właściwej sekcji (06, 08…) |
| zmiana kosztorysu / negocjacje | „komisja proponuje obniżenie wydatków na towar do 20% dotacji”, „pozycja X niekwalifikowalna” | zmiana w arkuszu → tabela „przed / po” → nowa specyfikacja z `Do-wniosku` |
| zmiana kwoty dotacji | „proponowana kwota dofinansowania: 22 000 zł” | arkusz: `Zalozenia!B5`, przesunięcie pozycji na wkład własny lub rezygnacja z pozycji. Klient decyduje, czy się zgadza |

### A3. Szablon pisma

```text
{{miejscowosc}}, dnia {{data}}

{{imie_nazwisko}}
{{adres}}
{{pesel_lub_nr_wniosku}}

Powiatowy Urząd Pracy w {{miejscowosc_PUP}}
{{adres_PUP}}

Dotyczy: wniosku o przyznanie środków na podjęcie działalności gospodarczej
z dnia {{data_wniosku}}, znak sprawy: {{znak_sprawy}}

W odpowiedzi na wezwanie z dnia {{data_wezwania}} (doręczone {{data_doreczenia}})
przedstawiam uzupełnienia i wyjaśnienia:

1. {{punkt_1_z_wezwania – krótko, czego dotyczy}}
{{odpowiedź – 1–3 akapity albo "W załączeniu przedkładam …"}}

2. {{punkt_2_z_wezwania}}
{{odpowiedź}}

[jeśli zmienia się kosztorys:]
3. Zmiany w specyfikacji wydatków
W związku z {{powód – np. sugestią komisji}} wprowadzam następujące zmiany:
| Poz. | Nazwa | Było (zł) | Jest (zł) | Finansowanie | Powód zmiany |
|------|-------|-----------|-----------|--------------|--------------|
| …    | …     | …         | …         | …            | …            |
Po zmianach łączna kwota wydatków z dotacji wynosi {{ark_kosztorys_dotacja}},
a z wkładu własnego {{ark_kosztorys_wklad}}. Zaktualizowaną specyfikację
i kalkulację przychodów i kosztów załączam.

Pozostałe elementy wniosku pozostają bez zmian.

Załączniki:
1. {{…}}
2. {{…}}

                                                    {{podpis}}
```

### A4. Prompt do szkicu odpowiedzi

```text
Przygotowujesz szkic odpowiedzi na wezwanie powiatowego urzędu pracy do uzupełnienia wniosku
o dofinansowanie. Obowiązują wszystkie zasady promptu systemowego (pierwsza osoba, fakty tylko
z kwestionariusza i <nowe_informacje_od_klienta>, liczby tylko z <arkusz> jako {{ark_…}},
zero obietnic). Dodatkowo:
1. Odpowiadaj na KAŻDY punkt wezwania, w tej samej kolejności i numeracji.
2. Nie dodawaj informacji, o które urząd nie pytał.
3. Ton uprzejmy i rzeczowy, bez tłumaczenia się i bez polemiki z urzędem.
4. Przy punktach "brak dokumentu" pisz tylko: "W załączeniu przedkładam …" + nazwa dokumentu.
5. Przy wyjaśnieniach – 300–1200 znaków na punkt, według szablonu właściwej sekcji.
6. Jeśli wezwanie dotyczy zmiany kosztorysu: tabela "przed/po" z <kosztorys_przed> i
   <kosztorys_po> (kwoty przepisane), sumy wyłącznie jako {{ark_…}}.
7. Brak informacji = [BRAK DANYCH: …].
Zwróć: <pismo>…</pismo> i <lista_zalacznikow_do_dostarczenia_przez_klienta>…</…>.
```

### A5. Przykład – fryzjerka mobilna

> **DANE FIKCYJNE – PRZYKŁAD.** Wezwanie, daty i znak sprawy są wymyślone.

**Wezwanie (skrót):** 1) Brak dokumentów dotyczących zakupu używanego climazonu (poz. 8). 2) Proszę uzasadnić koszt paliwa 700 zł miesięcznie. 3) Komisja proponuje obniżenie wydatków na towar (poz. 13) do 4 000 zł netto.
**Nowe informacje od klientki:** ma zdjęcia climazonu i oświadczenie sprzedającej o niefinansowaniu ze środków publicznych. Planuje średnio 5 wizyt dziennie, przeciętnie 12 km w obie strony; auto spala 6,5 l/100 km. Zgadza się zmniejszyć towar. Różnicę 1 000 zł netto pokryje z wkładu własnego (po zmianie w arkuszu: poz. 13 dotacja 4 000 zł netto, nowa poz. 18 „Farby i kosmetyki – część 2”, 1 000 zł netto, wkład własny).

```text
1. Dokumenty dotyczące zakupu używanego climazonu (poz. 8 specyfikacji)
W załączeniu przedkładam oświadczenie sprzedającej, że urządzenie w ciągu ostatnich 7 lat nie zostało zakupione ze środków publicznych, oraz zdjęcia urządzenia z widoczną tabliczką znamionową.

2. Uzasadnienie kosztu paliwa 700 zł miesięcznie
Usługi wykonuję w domach klientek, dlatego dojazd jest podstawowym kosztem mojej pracy. Planuję średnio 5 wizyt dziennie, a przeciętny dojazd do klientki i z powrotem to ok. 12 km. Mój samochód spala 6,5 l benzyny na 100 km. Kwotę 700 zł przyjęłam razem z bieżącą eksploatacją auta, czyli olejem, oponami i drobnymi naprawami.

3. Zmiana wydatków na towar (poz. 13)
Zgodnie z sugestią komisji zmniejszam wydatek z dotacji na farby i kosmetyki do 4 000 zł netto. Pozostałą część pierwszego zapasu kupię z wkładu własnego:
| Poz. | Nazwa | Było (zł) | Jest (zł) | Finansowanie | Powód zmiany |
| 13 | Pierwszy zapas farb, oksydantów i kosmetyków | 6 150,00 | 4 920,00 | dotacja | sugestia komisji |
| 18 | Farby i kosmetyki – część 2 | – | 1 230,00 | wkład własny | przeniesienie z poz. 13 |
Po zmianach łączna kwota wydatków z dotacji wynosi {{ark_kosztorys_dotacja}}, a z wkładu własnego {{ark_kosztorys_wklad}}. Zaktualizowaną specyfikację wydatków oraz kalkulację przychodów i kosztów załączam.

Pozostałe elementy wniosku pozostają bez zmian.
```

Uwagi do przykładu:
- Kwoty brutto w tabeli (4 920,00 i 1 230,00) pochodzą z arkusza po zmianie (`Kosztorys`, kolumna K), a nie z obliczeń modelu.
- Zmniejszenie wydatków z dotacji obniża wnioskowaną kwotę. Właściciel ustala z klientką, czy zmienić `Zalozenia!B5` (wnioskowana kwota), czy dopisać inną pozycję. W piśmie musi to być jednoznaczne.
- W uzasadnieniu paliwa model nie przeliczył kilometrów na litry ani złotówki, tylko podał założenia. Wyliczenie (np. 5 × 12 km × 21 dni) właściciel może dopisać ręcznie po sprawdzeniu.

---

## B. Rozmowa z komisją – 20 najczęstszych pytań

### B1. Jak klient ma się przygotować (instrukcja do przekazania klientowi)

> Nie uczymy się odpowiedzi na pamięć. Komisja od razu słyszy wyuczony tekst i wtedy dopytuje szczegółowo. Przygotowujemy **fakty i liczby**, a zdania układasz sam/a, tak jak rozmawiasz ze znajomym, który pyta o Twój pomysł.

1. **Przeczytaj swój wniosek dwa razy** w całości. Komisja ma go przed sobą i pyta o to, co napisałeś/aś.
2. **Dostaniesz „kartę faktów”** (generowaną promptem z pkt B3): przy każdym pytaniu 3–5 punktów, a nie gotowe zdania. Punkty to Twoje liczby, nazwy i przykłady.
3. **Powiedz każdą odpowiedź na głos 2–3 razy**, za każdym razem trochę inaczej. Nagraj się telefonem i odsłuchaj. Odpowiedź na jedno pytanie powinna trwać 30–90 sekund.
4. **Liczby, które musisz znać bez kartki:** kwota dotacji i wkład własny, łączna wartość zakupów, 3–5 głównych cen, planowany przychód miesięczny po rozruchu, średni zysk miesięczny, próg rentowności (w złotych i w liczbie usług), ZUS w pierwszych miesiącach i po ulgach.
5. **Mów o konkretach:** nazwy miejscowości, klientów, konkurentów, sprzętu. „Klientki z salonu przy Kościuszki pytały mnie…” brzmi wiarygodnie. „Jest duże zapotrzebowanie” brzmi jak wyuczona formułka.
6. **Gdy nie znasz odpowiedzi,** powiedz: „Tego nie sprawdziłem/am, ale dowiem się i mogę uzupełnić”. To lepsze niż zgadywanie. Nie wymyślaj liczb na rozmowie.
7. **Nie obiecuj:** zamiast „na pewno się uda” mów „planuję”, „zakładam”, „sprawdziłem/am, że…”.
8. **Zabierz:** dowód osobisty, kopię wniosku, oferty i linki do zakupów, umowę (przedwstępną) najmu, listy intencyjne, dyplomy i zaświadczenia, wydruk tabel z arkusza.

### B2. Lista pytań

| # | Pytanie komisji | Po co pyta | Skąd fakty | Wskazówka do odpowiedzi | Czego unikać |
|---|---|---|---|---|---|
| 1 | Proszę krótko opowiedzieć o swoim pomyśle. | sprawdza, czy rozumiesz własny plan | sekcja 01 | 1 minuta: co, gdzie, dla kogo, od kiedy, dlaczego Ty | czytania z kartki, historii branży |
| 2 | Dlaczego własna firma, a nie praca na etacie? | motywacja, ryzyko szybkiej rezygnacji | 01 (motywacja), K13 | prawdziwy powód z Twojego życia zawodowego, np. pytania klientów albo zamknięcie zakładu | „bo nie ma pracy” jako jedynego powodu |
| 3 | Jakie ma Pan/i doświadczenie w tej branży? | wiarygodność | 02 | pracodawcy, lata, konkretne prace. Jeden przykład trudnego zlecenia | zawyżania stanowisk |
| 4 | Czy do tej działalności potrzebne są uprawnienia? Czy je Pan/i ma? | wymogi prawne | 02, dokumenty | nazwa uprawnienia, rok, dokument przy sobie. Jeśli nie są wymagane, powiedz to wprost | mówienia „chyba nie trzeba” |
| 5 | Kim będą klienci i skąd Pan/i wie, że kupią? | realność popytu | 03 | 2–3 grupy klientów, dowody: listy intencyjne, ankieta, dawni klienci (liczby) | „wszyscy mieszkańcy” |
| 6 | Kto jest konkurencją i czym się Pan/i wyróżni? | rozpoznanie rynku | 04 | 2–3 nazwy, ich ceny, Twoja konkretna różnica. Przyznaj, w czym są dobrzy | „nie ma konkurencji”, krytykowania konkurentów |
| 7 | Skąd weźmie Pan/i pierwszych klientów? | start sprzedaży | 05 (plan 90 dni) | pierwsze 2–3 działania i nazwiska lub firmy, z którymi już rozmawiałeś/aś | „z internetu” |
| 8 | Jak ustalił/a Pan/i ceny? | spójność z rynkiem i prognozą | 04, `Przychody` | porównanie z konkurencją + koszt materiału + czas usługi | „tak sobie wymyśliłem/am” |
| 9 | Gdzie będzie działać firma? Czy ma Pan/i lokal / tytuł prawny? | wykonalność, wymogi PUP | 01, umowa | adres, metraż, rodzaj umowy, koszt. Dla firmy mobilnej: auto i zasięg | niejasnych odpowiedzi o lokalu |
| 10 | Do czego potrzebny jest [najdroższy sprzęt]? | kwalifikowalność wydatków | 06 | konkretna usługa, którą ten sprzęt umożliwia, i ile razy w miesiącu go użyjesz | „przyda się” |
| 11 | Dlaczego nowy (albo używany) i skąd ta cena? | racjonalność kosztów | 06, oferty | liczba porównanych ofert, przedział cen, dlaczego ta oferta | braku ofert przy sobie |
| 12 | Co już Pan/i ma i co wnosi Pan/i sam/a? | zaangażowanie, ryzyko | 06 (zasoby), `Zalozenia!B7` | sprzęt, auto, wkład gotówkowy i jego źródło | ukrywania, że część sprzętu już masz |
| 13 | Ile planuje Pan/i zarabiać i skąd te liczby? | realizm prognozy | 08, `Przychody` | cena × liczba usług, rozruch w pierwszych miesiącach. Podaj przychód miesięczny po rozruchu | liczb innych niż we wniosku |
| 14 | Jakie będą koszty miesięczne? Czy uwzględnił/a Pan/i ZUS i podatek? | kompletność kosztów | 08, `Koszty` | koszty stałe, materiały, ZUS (ulga na start, potem preferencyjny), składka zdrowotna, forma opodatkowania | „ZUS jeszcze nie liczyłem/am” |
| 15 | Kiedy firma zacznie zarabiać? Jaki jest próg rentowności? | opłacalność | `Prognoza`, 08 | miesiąc pierwszego zysku, próg w złotych i w liczbie usług miesięcznie | pomylenia przychodu z zyskiem |
| 16 | Co, jeśli przychody będą o 30% niższe albo przyjdzie słaby sezon? | odporność | 08, 09 | liczby ze scenariusza pesymistycznego + 2 konkretne działania z planu B | „to się nie zdarzy” |
| 17 | Co będzie po zakończeniu ulg w ZUS? | trwałość po 2,5 roku | `Prognoza!C29`, 08 | próg rentowności po ulgach i jak go osiągniesz (więcej klientów, nowe usługi) | zaskoczenia pytaniem |
| 18 | Jaka forma opodatkowania i dlaczego? VAT? | świadomość formalna | 01, `Zalozenia` | forma + jedno zdanie uzasadnienia (np. niskie koszty → ryczałt). Zwolnienie z VAT lub VAT czynny i dlaczego | „księgowa wybierze” bez żadnego uzasadnienia |
| 19 | Kto poprowadzi księgowość? Jak rozliczy Pan/i dotację? | rozliczenie środków | 02 (luki), umowa z PUP | biuro rachunkowe (nazwa, jeśli wybrane), faktury na każdą pozycję, zakupy w terminie z umowy, przechowywanie dokumentów | nieznajomości terminu rozliczenia |
| 20 | Czy zna Pan/i obowiązki z umowy: okres prowadzenia firmy, zabezpieczenie zwrotu? | ryzyko zwrotu dotacji | umowa z PUP, regulamin | minimalny okres prowadzenia działalności, forma zabezpieczenia (np. poręczenie, weksel, blokada rachunku), kto jest poręczycielem | niepewności co do poręczyciela |

### B3. Prompt do „karty faktów” (przygotowanie klienta)

```text
Przygotuj "kartę faktów" na rozmowę z komisją PUP dla wnioskodawcy. Dostajesz: gotowy wniosek
(sekcje 01–09), <arkusz> ze zmiennymi ark_* (wartości już podstawione) i listę 20 pytań.
Dla KAŻDEGO pytania podaj:
- 3–5 punktów-faktów (krótkie równoważniki, NIE gotowe zdania do nauczenia): liczby, nazwy,
  przykłady – wyłącznie z wniosku i arkusza;
- 1 prawdopodobne pytanie dopytujące komisji;
- [BRAK DANYCH: …], jeśli wniosek nie daje podstaw do odpowiedzi – to sygnał, że klient musi
  się przygotować.
Na początku karty: "Liczby, które musisz znać" – dotacja, wkład własny, wartość zakupów,
3–5 cen, przychód miesięczny po rozruchu, średni zysk netto miesięcznie, próg rentowności
(zł i liczba usług), ZUS teraz i po ulgach.
Język prosty, bez fraz z listy zakazanej. Nie dodawaj żadnych faktów spoza wniosku i arkusza.
```

### B4. Przykład fragmentu karty faktów – fryzjerka mobilna

> **DANE FIKCYJNE – PRZYKŁAD** (wartości z arkusza przykładowego).

**Liczby, które musisz znać:** dotacja 26 000 zł, wkład własny 3 000 zł · zakupy z dotacji 25 995 zł · strzyżenie damskie 80 zł, męskie 45 zł, koloryzacja 200 zł · przychód po rozruchu ok. 8 200 zł/mies. · zysk netto średnio ok. 3 500 zł/mies. · próg rentowności ok. 2 600 zł/mies. (ok. 32 usługi), po ulgach ok. 4 500 zł · ZUS: 0 zł przez 6 mies. (ulga na start), potem ok. 456 zł + zdrowotna.

**Pytanie 16 – Co, jeśli przychody będą o 30% niższe?**
- przychód roczny w wariancie −30%: ok. 61 200 zł; zysk netto ok. 1 900 zł/mies.;
- drugi DPS w gminie Lipy i zakład opiekuńczy w Zielonowie;
- pakiety rodzinne (3–4 osoby podczas jednej wizyty);
- mniej płatnej reklamy (250 zł/mies.);
- *komisja może dopytać:* „Czy rozmawiała Pani już z tym DPS?” → [BRAK DANYCH: czy był kontakt z drugim DPS]
