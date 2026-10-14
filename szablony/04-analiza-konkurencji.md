# 04 – Analiza konkurencji

> Typowe nazwy pola: „Analiza konkurencji”, „Konkurencja na rynku lokalnym”, „Główni konkurenci i przewaga konkurencyjna”.
> Część formularzy wymaga tabeli, część tylko opisu. Ten szablon daje oba warianty, a o wyborze decyduje mapowanie pól (`10-mapowanie-pol-formularza.md`).

## 1. Cel sekcji

Pokazać, że **znasz z nazwy** 3–5 firm lub osób, które robią to samo na Twoim terenie. Trzeba też pokazać, że wiesz, **co oferują, za ile i gdzie mają słabe punkty**, i potrafisz uczciwie powiedzieć, **czym się wyróżnisz**. Komisja nie oczekuje, że konkurencji nie ma. Odpowiedź „brak konkurencji” jest dla niej sygnałem, że wnioskodawca nie zrobił rozpoznania.

## 2. Dane wejściowe z kwestionariusza

| Kod | Dane | Uwagi |
|---|---|---|
| K8 | 3–5 konkurentów: nazwa, miejscowość lub adres, oferta, ceny (źródło: cennik www, telefon, wizyta, z datą), słabe strony (na podstawie opinii Google, rozmów, własnej obserwacji) | słabe strony muszą być **sprawdzalne**, bez obrażania |
| K8 | substytuty (np. „robię sam”, „telefonem”, duże sieci, internet) | 1–2 |
| K8 | własna przewaga – według klienta | model może ją przeformułować, ale nie dodaje nowych przewag |
| K5 | własne ceny | do porównania |
| K10 | sprzęt z kosztorysu, który daje przewagę | spójność z sekcją 06 |

## 3. Struktura

1. **Zdanie wprowadzające:** ilu konkurentów rozpoznałeś, na jakim obszarze i kiedy (np. „we wrześniu 2026 r.”).
2. **Tabela konkurentów** (3–5 wierszy):

   | Konkurent (miejscowość) | Oferta | Ceny | Słabe strony | Moja przewaga wobec niego |
   |---|---|---|---|---|

3. **Substytuty:** 1–3 zdania.
4. **Podsumowanie przewagi:** 2–4 konkretne wyróżniki (cena, termin, zasięg, sprzęt, uprawnienia, godziny, specjalizacja), każdy możliwy do sprawdzenia.
5. **Pozycja cenowa:** jedno zdanie, gdzie są Twoje ceny na tle konkurencji (tylko gdy ceny są w K5 i K8).

**Wariant bez tabeli** (pole tylko tekstowe): każdy konkurent w osobnym akapicie: nazwa → oferta i ceny → słabość → moja przewaga.

## 4. Długość – trzy warianty

| Wariant | Znaki | Co zawiera |
|---|---|---|
| krótki | ~800 | 3 konkurentów w 1–2 zdaniach każdy (bez tabeli), 2 wyróżniki |
| standard | ~2000 | tabela 3–4 konkurentów + substytuty + podsumowanie przewagi |
| długi | ~4000 | tabela 5 konkurentów + szerszy opis każdego (źródła informacji, opinie klientów), substytuty, pozycjonowanie cenowe, jak zareagujesz, jeśli konkurent obniży ceny |

Tabela liczy się do limitu znaków. W formularzach PDF tabelę często trzeba zamienić na tekst. Sprawdź to w mapowaniu.

## 5. Co punktuje komisja

- **Nazwy i ceny,** czyli dowód rzeczywistego rozpoznania. Komisja często zna lokalnych przedsiębiorców i sprawdza, czy opis jest rzetelny.
- **Rzeczowe słabe strony** (terminy, zasięg, godziny, brak usługi X), a nie oceny („nieprofesjonalni”).
- **Przewaga wynikająca z zasobów z wniosku:** sprzęt z kosztorysu, kwalifikacje z sekcji 02, lokalizacja z sekcji 01.
- **Realizm:** przyznanie, że konkurent jest w czymś lepszy, zwiększa wiarygodność.

## 6. Typowe błędy

- „Na rynku lokalnym nie ma konkurencji”.
- Konkurenci anonimowi („inne salony w mieście”).
- Przewaga „wyższa jakość i niższe ceny” bez liczb.
- Obraźliwe opinie o konkurentach (komisja to wyłapuje, a tekst może trafić do konkurenta).
- Ceny konkurencji bez daty i źródła. Ceny się zmieniają, więc trzeba wiedzieć, skąd pochodzą.

## 7. Prompt sekcji

```text
SEKCJA 04 – ANALIZA KONKURENCJI
Napisz treść pola "{{pole_formularza}}" (limit: {{limit_znakow}}, ton: {{ton}},
format: {{tabela | tekst}}).
Kolejność: (1) ilu konkurentów, jaki obszar, kiedy sprawdzone (z K8); (2) konkurenci z K8 –
nazwa, miejscowość, oferta, ceny (ze źródłem/datą, jeśli podane), słabe strony, moja przewaga
wobec każdego; (3) substytuty z K8; (4) 2–4 wyróżniki – tylko te, które wynikają z K8, K2/K3,
K5, K6 lub K10; (5) pozycja cenowa na tle konkurencji (tylko gdy ceny są w K5 i K8).
Słabe strony opisuj rzeczowo i sprawdzalnie (termin, zasięg, zakres usług, opinie z podaną
oceną) – bez epitetów. Nie dodawaj konkurentów, cen ani opinii spoza K8. Nie pisz, że
konkurencji nie ma. Jeśli w K8 jest mniej niż 3 konkurentów – [BRAK DANYCH: dopisz min.
3 konkurentów z nazwą, ofertą i ceną].
Przy formacie "tabela": kolumny Konkurent | Oferta | Ceny | Słabe strony | Moja przewaga.
```

## 8. Przykład wypełnienia – fotograf

> **DANE FIKCYJNE – PRZYKŁAD.** Wszystkie studia, osoby, ceny i oceny są wymyślone.

**Skrót kwestionariusza:** Michał, 29 lat, Zielonów. Oferta: reportaż ślubny 4 500 zł (cały dzień, 2 korpusy, ujęcia z drona, galeria online, termin oddania 21 dni); sesja rodzinna lub noworodkowa 450 zł (30 zdjęć, plener lub dom klienta); zdjęcia nieruchomości i produktów dla firm od 300 zł. Dojazd w powiecie wliczony w cenę, wolne terminy na cały sezon 2027. Kosztorys (K10): drugi korpus, obiektyw szerokokątny 16–35 mm, dron z kamerą. Uprawnienia: operator drona A2 CofC (2024). 2021–2025 drugi fotograf na umowy o dzieło dla „Kadr – Fotografia Ślubna” (ok. 60 ślubów). Konkurencja sprawdzona 09.2026 (cenniki www, telefony, opinie Google): (1) Foto-Studio Remek, Zielonów, Rynek 3: studio, dokumenty, komunie, ślub 3 800 zł; relacja do obiadu, zdjęcia na pendrive, oddanie do 8 tygodni. (2) Kadr – Fotografia Ślubna, miasto wojewódzkie (45 km): ślub 6 500–8 000 zł, bardzo wysoka jakość, terminy na sezon 2027 prawie zajęte, dojazd płatny, nie robi zdjęć dla firm. (3) Paweł N., freelancer, Lipy: ślub 2 500 zł, jeden aparat, opinie Google 3,4/5 (skargi na terminy oddania). Substytut: biura nieruchomości robią zdjęcia telefonem.

### Wariant standard (~2000 znaków, z tabelą), ton: techniczny

```text
We wrześniu 2026 r. sprawdziłem trzech fotografów, którzy obsługują śluby i sesje w Zielonowie i okolicy. Korzystałem z ich cenników na stronach, rozmów telefonicznych i opinii w Google.

| Konkurent | Oferta | Ceny | Słabe strony | Moja przewaga |
|---|---|---|---|---|
| Foto-Studio Remek, Zielonów, Rynek 3 | studio, zdjęcia do dokumentów, komunie, śluby | ślub 3 800 zł | relacja tylko do obiadu, zdjęcia na pendrive, oddanie do 8 tygodni | relacja przez cały dzień, galeria online, oddanie w 21 dni |
| Kadr – Fotografia Ślubna (45 km) | reportaże ślubne | 6 500–8 000 zł + dojazd | terminy na sezon 2027 prawie zajęte, nie robi zdjęć dla firm | wolne terminy w 2027 r., brak opłaty za dojazd w powiecie, cena 4 500 zł |
| Paweł N., Lipy | śluby, sesje | ślub 2 500 zł | jeden aparat, opinie 3,4/5, skargi na terminy oddania | dwa korpusy (zapas na wypadek awarii), stały termin oddania |

Substytutem moich usług dla firm są zdjęcia robione telefonem przez pracowników biur nieruchomości. Dla nich przygotuję zdjęcia wnętrz z obiektywem szerokokątnym i zdjęcia z drona. Żaden z trzech opisanych fotografów nie ma w ofercie zdjęć dla firm.

Na czym polega moja przewaga:
– pracuję na dwóch korpusach, więc awaria aparatu nie przerywa relacji ze ślubu,
– mam uprawnienia operatora drona A2 CofC (2024) i mogę legalnie wykonywać ujęcia z powietrza,
– zdjęcia oddaję w ciągu 21 dni w galerii online,
– przez cztery lata jako drugi fotograf zrobiłem ok. 60 ślubów, więc znam przebieg dnia ślubu i miejsca w okolicy.

Ze swoją ceną 4 500 zł za ślub jestem między fotografem z Zielonowa (3 800 zł) a studiem z miasta wojewódzkiego (od 6 500 zł). Studio „Kadr” ma większe doświadczenie i rozpoznawalność. Konkurować z nim zamierzam dostępnością terminów i brakiem opłat za dojazd, a nie ceną.
```

### Na co zwrócić uwagę w przykładzie

- Słabe strony konkurentów są sprawdzalne (zakres, terminy, ocena z liczbą), bez epitetów.
- Tekst przyznaje, że jeden konkurent jest mocniejszy, co zwiększa wiarygodność.
- Przewagi wynikają z kwestionariusza: sprzętu (spójnego z kosztorysem), uprawnień i doświadczenia.
- Ton techniczny widać w nazwach sprzętu i uprawnień (korpusy, obiektyw szerokokątny, A2 CofC).
- Model nie liczył różnic w cenach, tylko przepisał ceny z kwestionariusza.
