# pup-gen – silnik treści do wniosku o dofinansowanie z PUP

Pakiet zamienia kwestionariusz klienta w paczkę dla właściciela usługi:

1. **arkusz finansowy** – kopia `model-finansowy/model-finansowy-pup.xlsx` wypełniona danymi klienta i przeliczona w LibreOffice (kosztorys, prognoza 12 mies., ZUS, podatek, próg rentowności);
2. **treści pól wniosku** – pisze je model Claude według `szablony/00`–`09`, pod pola i limity znaków formularza konkretnego urzędu (mapa formularza). Liczby trafiają do tekstu tylko jako zmienne `{{ark_*}}` z arkusza;
3. **kontrola jakości** – zakazane zwroty, obietnice, znaczniki `[BRAK DANYCH]`, długość pól, spójność liczb, regulamin urzędu, podobieństwo do wcześniejszych planów do tego samego PUP;
4. **DOCX dla klienta** (opcjonalnie PDF) i osobny **raport kontroli dla właściciela**.

Właściciel zawsze sprawdza wynik według `docs/checklista-weryfikacji.md`. Raport kontroli pokazuje, od czego zacząć.

---

## 1. Instalacja

Wymagania: Python 3.13, LibreOffice (`soffice`, domyślnie `/usr/bin/soffice`; inna ścieżka: zmienna `PUP_GEN_SOFFICE`).

```bash
cd generator
pip install -e ".[test]"          # anthropic, openpyxl, python-docx, pydantic (+ pytest)
pip install -e ".[pdf]"           # opcjonalnie pypdf: odczyt pól PDF z /MaxLen w `pup-gen mapuj`
python -m pytest -q               # testy (offline, z prawdziwym LibreOffice)
```

Po instalacji dostępna jest komenda `pup-gen` (to samo co `python -m pup_gen.cli`).

## 2. Klucz API

Bez klucza wszystko działa offline z **atrapą modelu** (`KlientAtrapa`). Atrapa składa deterministyczny tekst z faktów kwestionariusza o długości 85–98% limitu. Sprawdza się w niej cały przebieg (arkusz, prompty, podstawianie zmiennych, kontrola, DOCX), ale **tekstu z atrapy nie wysyłamy klientowi**.

Prawdziwe generowanie włącza zmienna środowiskowa:

```bash
export ANTHROPIC_API_KEY=sk-ant-...      # albo: ant auth login
export PUP_GEN_MODEL=claude-opus-5-5     # opcjonalnie, to jest wartość domyślna
export PUP_GEN_EFFORT=high               # opcjonalnie: low | medium | high | xhigh | max
```

Ustawienia wywołania (`pup_gen/llm.py`, `KlientClaude`), zgodne z aktualnymi zaleceniami SDK `anthropic` 1.x:

| Ustawienie | Wartość | Po co |
|---|---|---|
| model | `claude-opus-5-5` | domyślny model; zmiana: `--model` lub `PUP_GEN_MODEL` |
| myślenie | `thinking: {type: "adaptive"}` + `output_config.effort` (domyślnie `high`) | Opus 5.5 nie pozwala wyłączyć myślenia; głębokość reguluje `effort` (domyślny w API to `medium`, dlatego ustawiamy go jawnie) |
| prompt caching | 3 punkty `cache_control`: prompt systemowy → dane klienta + arkusz → szablon sekcji | system jest wspólny dla wszystkich zleceń, dane klienta dla wszystkich pól jednego zlecenia |
| odmowa modelu | `fallbacks: "default"` (beta `server-side-fallback-2026-07-01`), potem sprawdzenie `stop_reason == "refusal"` | przy odmowie API samo ponawia na zalecanym modelu zapasowym |
| limity | `max_tokens=16000`, streaming + `get_final_message()` | długie odpowiedzi z myśleniem bez przekroczenia czasu HTTP |
| ponowienia | SDK: `max_retries=4` (429, 5xx, połączenie); generator: druga próba, gdy brak bloku `<tekst>`; jedna prośba o skrócenie z dokładną nadwyżką, gdy tekst przekracza limit | |

Logi (`-v`) zawierają tylko id pola, długości, liczby tokenów i `request_id`, bez treści kwestionariusza. Błędy walidacji kwestionariusza nie wypisują wartości pól.

## 3. Przebieg krok po kroku (dla właściciela)

1. **Kwestionariusz → JSON.** Odpowiedzi klienta zapisz według schematu `Kwestionariusz` (`pup_gen/schemat.py`; przykłady w `przyklady/kwestionariusz-*.json`). Walidacja od razu odrzuca PESEL i numer dowodu (także w tekście), ceny ≤ 0, sumę zakupów z dotacji większą niż kwota wnioskowana i kwotę wyższą niż maksimum naboru.
2. **Mapa formularza.** Dla nowego wzoru wniosku:
   ```bash
   pup-gen mapuj --formularz wniosek_PUP.docx --pup "Powiatowy Urząd Pracy w …" --out mapa.json
   ```
   Wynik jest heurystyczny (`"status": "DO RĘCZNEJ KOREKTY"`). Popraw w nim limity, sekcje i kolejność według `szablony/10-mapowanie-pol-formularza.md` (patrz pkt 4). Przy skanie najpierw OCR (`ocrmypdf -l pol`).
3. **Generowanie:**
   ```bash
   pup-gen generuj --kwestionariusz klient.json --mapa mapa.json --out wyniki/zielonow/2026-10-anna
   #   [--regulamin zielonow] [--dry-run] [--pdf] [--model …] [--effort …] [--archiwum wyniki/]
   ```
   Katalog wyniku:
   | Plik | Dla kogo |
   |---|---|
   | `PUP-<miasto>_<id>_wniosek_v1.docx` (+ `.pdf` z `--pdf`) | klient: strona tytułowa „co wpisać i podpisać samemu”, pola w kolejności formularza z nazwami jak w formularzu, tabele z arkusza `Do-wniosku` |
   | `arkusz-<id>.xlsx` | klient i właściciel: przeliczony arkusz |
   | `raport-kontroli-WLASCICIEL.md` / `.docx`, `raport-kontroli.json` | **tylko właściciel** |
   | `wynik.json`, `kwestionariusz.json`, `mapa.json`, `regulamin.json` | dane do ponownej kontroli |
4. **Raport kontroli.** Najpierw usuń wszystkie pozycje **BLOKUJE**, potem rozstrzygnij **OSTRZEŻENIA**. Znaczniki `[BRAK DANYCH: …]` (w DOCX podświetlone na żółto) to pytania do klienta: uzupełnij odpowiedź albo usuń zdanie.
5. **Poprawki ręczne.** Możesz poprawić teksty w `wynik.json` (pole `tekst`) i uruchomić samą kontrolę:
   ```bash
   pup-gen sprawdz --wynik wyniki/zielonow/2026-10-anna     # kod wyjścia 1, gdy coś BLOKUJE
   ```
   Uwaga: `sprawdz` nie przebudowuje DOCX. Po większych zmianach wygeneruj paczkę ponownie albo popraw DOCX ręcznie.
6. **Checklista** `docs/checklista-weryfikacji.md`: zwłaszcza części A (kwalifikowalność), D (prawdziwość: konkurenci, listy intencyjne) i E (zgodność z formularzem). Tych punktów automat nie sprawdzi.
7. **Archiwum.** Trzymaj wyniki w `wyniki/<pup>/<id>/` (katalog jest w `.gitignore`). Kontrola porównuje nowy plan ze wszystkimi `wynik.json` w archiwum, które mają ten sam `pup_id` (test bliźniaka). Ostrzega też, gdy w ciągu 3 miesięcy do tego samego urzędu poszedł plan w tym samym tonie.

### Co dokładnie sprawdza kontrola (`pup_gen/kontrola.py`)

| Nr | Kontrola | Poziom |
|---|---|---|
| 1 | frazy z LISTY ZAKAZANEJ (parsowanej z `szablony/00-system-prompt.md`, z odmianą przez rdzenie wyrazów) | BLOKUJE; frazy warunkowe („(bez źródła)”, „(bez podania cen…)”) – OSTRZEŻENIE |
| 2 | znaczniki `[BRAK DANYCH: …]` zebrane jako pytania do klienta | OSTRZEŻENIE |
| 3 | długość pola: > 100% limitu / < 85% limitu | BLOKUJE / OSTRZEŻENIE |
| 4 | każda kwota (zł) i każdy procent w tekście musi wynikać z `ark_*` albo z kwestionariusza (tolerancja ±1 zł / 0,1% kwoty, ±0,5 p.p.) | BLOKUJE |
| 5 | regulamin: PKD i opis vs `wykluczenia_dzialalnosci`, działalność sezonowa, przejęcie po rodzinie, limity % kategorii, pojazdy, sprzęt używany, zakup od rodziny, liczba poręczycieli; pozycje często wykluczone z katalogu (kasa fiskalna, leasing, czynsz…) | BLOKUJE / OSTRZEŻENIE |
| 6 | podobieństwo do planów do tego samego PUP: wspólne fragmenty 8-wyrazowe, cosinus TF-IDF (≥ 0,60), Jaccard trójek wyrazów (≥ 0,20); rotacja tonu | OSTRZEŻENIE |
| 7 | obietnice z zasady 8 promptu („na pewno”, „gwarantuję”…; „zawsze”, „100%” jako OSTRZEŻENIE) | BLOKUJE |
| + | ostrzeżenia arkusza (`Zalozenia!B27:B34`): ujemna gotówka, niskie saldo startowe, nierozplanowana dotacja, przekroczony limit kategorii, obłożenie > 100%, limit VAT, błędy formuł; niepodstawione `{{…}}`; wzmianki o AI; tekst w 3. osobie | różne |

## 4. Jak dodać urząd i mapę formularza

**Regulamin urzędu.** Dopisz wiersz do `baza-pup/regulaminy-pup-2026.csv` (kolumny według `baza-pup/SCHEMAT.md`, separator `;`, listy rozdzielone ` | `). Generator szuka `pup_id` kolejno w: pliku z `--regulamin-csv`, w `baza-pup/regulaminy-pup-2026.csv` i w `przyklady/regulaminy-przyklad.csv` (dwa fikcyjne urzędy do testów). Gdy regulaminu brak, limity kategorii w arkuszu wynoszą 100%, a raport ostrzega, że regulaminu nie sprawdzono. Limity kategorii z regulaminu trafiają do `Kosztorys!B33:B37`.

**Mapa formularza** (`MapaFormularza`, przykłady: `przyklady/mapa-krotka-6-pol.json`, `przyklady/mapa-dluga-14-pol.json`). Każde pole ma:

| Klucz | Znaczenie |
|---|---|
| `id`, `nazwa_w_formularzu` | numer i nazwa dokładnie jak w formularzu (tak trafiają do DOCX) |
| `limit_znakow` | limit do generowania (ze spacjami, już z marginesem 0,95 / 0,90 z szablonu 10). Brak limitu → 2000 |
| `sekcje` | `"01"`–`"09"` (szablon sekcji), `"tabela:kosztorys"`, `"tabela:kalkulacja_miesieczna"`, `"tabela:kalkulacja_kwartalna"`, `"tabela:wskazniki"` (tabele z arkusza `Do-wniosku`), `"dane:kwota_dotacji"`, `"dane:wklad_wlasny"`, `"dane:forma_opodatkowania"`, `"dane:pkd"`, `"dane:data_startu"` |
| `podzial_limitu` | dla pól łączonych, np. `{"03": 0.55, "04": 0.45}` (suma 1,0) |
| `format` | `tekst`, `tabela` (sekcja 06 → wariant pozycyjny), `4_pola` (SWOT), `zaznaczenie`, `liczba` |
| `uwagi` | nietypowe pytanie z formularza dosłownie – model dostaje je w `<parametry>` |

`poza_zakresem` (dane osobowe, zabezpieczenie, oświadczenia) trafia na stronę tytułową DOCX jako lista „wpisujesz sam(a)”.

Wariant długości wynika z limitu: do 1200 znaków „krótki”, do 3000 „standard”, powyżej „długi”.

## 5. Koszt API na plan

`pup-gen koszt` liczy tokeny na podstawie rzeczywistych promptów (szablony + dane przykładowego klienta + mapa). Z kluczem API i flagą `--dokladnie` liczy tokeny wejścia przez `count_tokens`. Cennik ze skilla `claude-api` (stan na 2026-10-06), USD za 1 mln tokenów:

| Model | wejście | wyjście | odczyt cache | zapis cache (5 min) |
|---|---:|---:|---:|---:|
| `claude-opus-5-5` (domyślny) | 4,00 | 20,00 | 0,20 | 5,00 |
| `claude-sonnet-5-5` | 2,00 | 10,00 | 0,20 | 2,50 |

Szacunek dla fryzjerki (wynik `pup-gen koszt`): przyjęto 2,5 znaku na token, odpowiedź ≈ 95% limitu + 300 tokenów bloku `<kontrola>`, myślenie = 1× widocznej odpowiedzi, 15% pól ze skracaniem.

| Formularz | Pola tekstowe | Tokeny wejścia (przed cache) | Tokeny wyjścia | **Opus 5.5 z cache** | bez cache | Sonnet 5.5 z cache |
|---|---:|---:|---:|---:|---:|---:|
| krótki (6 pól) | 6 | ≈ 80 tys. | ≈ 15 tys. | **≈ 0,45 USD (≈ 1,7 zł)** | 0,66 USD | 0,23 USD |
| długi (14 pól, 11 tekstowych) | 11 | ≈ 143 tys. | ≈ 25 tys. | **≈ 0,70 USD (≈ 2,6 zł)** | 1,16 USD | 0,36 USD |

Przy intensywnym myśleniu (`--mnoznik-myslenia 2`) długi formularz kosztuje ok. 0,95 USD. Realnie należy liczyć **0,5–1 USD na plan** (kurs 3,70 zł/USD to założenie, parametr `--kurs`). Największą część kosztu stanowi wyjście z myśleniem. Cache obniża koszt planu o ok. 40%: blok danych klienta (≈ 7 tys. tokenów) i prompt systemowy (≈ 3 tys.) są czytane z cache przy każdym kolejnym polu. Rzeczywiste zużycie każdego pola zapisuje się w `wynik.json` (`tokeny`). Po pierwszych zleceniach porównaj je z szacunkiem.

## 6. Struktura pakietu

| Plik | Zawartość |
|---|---|
| `pup_gen/schemat.py` | modele pydantic: `Kwestionariusz`, `RegulaminPUP`, `MapaFormularza`, `WynikGeneracji`; wykrywanie PESEL i numeru dowodu (sumy kontrolne) |
| `pup_gen/finanse.py` | wypełnienie arkusza (tylko komórki wejściowe), przeliczenie `soffice --headless --convert-to xlsx` (osobny profil LibreOffice na każde wywołanie), odczyt `ark_*`, kontroli i tabel `Do-wniosku`, polskie formatowanie liczb |
| `pup_gen/prompty.py` | czytanie `szablony/*.md` (część PROMPT z pliku 00; sekcje 1–7 szablonów, bez przykładów), składanie bloków pod cache, warianty długości |
| `pup_gen/llm.py` | `KlientClaude` (SDK anthropic), `KlientAtrapa` (offline) |
| `pup_gen/kontrola.py` | kontrola jakości i raport Markdown |
| `pup_gen/dokument.py` | DOCX dla klienta, DOCX raportu |
| `pup_gen/przebieg.py` | cały przebieg zlecenia, ponowna kontrola katalogu |
| `pup_gen/mapowanie.py` | heurystyczne mapowanie formularza PDF/DOCX |
| `pup_gen/koszt.py` | szacunek tokenów i kosztu |
| `pup_gen/cli.py` | komenda `pup-gen` |
| `przyklady/` | 3 kwestionariusze (fryzjerka mobilna, mechanik, firma sprzątająca – spójne z przykładami w `szablony/`), 2 mapy, fikcyjne regulaminy |
| `tests/` | pytest (62 testy): schemat, arkusz z prawdziwym LibreOffice, prompty, SDK z transportem w pamięci, kontrola, podobieństwo, pełny `--dry-run`, mapowanie, koszt |

Przykład kontrolny: kwestionariusz fryzjerki ma te same dane wejściowe co przykład w arkuszu. Test sprawdza, że po wypełnieniu i przeliczeniu wychodzą liczby z `szablony/08` (87 415 zł przychodu, 42 429 zł zysku netto, 61 191 zł w scenariuszu −30%).

## 7. Znane ograniczenia

- **Atrapa to nie model.** Teksty z `--dry-run` są poprawne formalnie (fakty, liczby, długość), ale schematyczne. Dlatego test podobieństwa między przykładami z atrapy zawsze ostrzega. Jakość prawdziwych tekstów trzeba ocenić na pierwszych zleceniach z kluczem API: tego środowiska nie dało się przetestować z prawdziwym modelem.
- **Szacunek tokenów bez klucza** opiera się na proporcji 2,5 znaku/token. Dokładne liczby daje `pup-gen koszt --dokladnie` (z kluczem) albo pole `tokeny` w `wynik.json`.
- **Arkusz:** w szablonie jest **48** nazwanych komórek `ark_*` (zadanie mówiło o 51; czytamy wszystkie, jakie są). Mieści 20 pozycji kosztorysu i 5 usług – więcej odrzuca walidacja. Ceny netto liczone są z cen brutto z ofert (`brutto / (1 + VAT)`), więc możliwe są różnice o 1 grosz (raport pokazuje je jako INFO). Uproszczenia modelu finansowego opisuje `model-finansowy/INSTRUKCJA.md`, pkt 9.
- **Spójność liczb** sprawdza tylko liczby z jednostką `zł` / `%`. Liczby bez jednostki (np. „30 klientów”) i daty sprawdza właściciel. Zbiór dozwolonych procentów jest szeroki (obejmuje wszystkie liczby z kwestionariusza), więc błędny procent równy przypadkowej liczbie z kwestionariusza przejdzie.
- **Zakazane zwroty** wykrywa dopasowanie rdzeni wyrazów: synonimów spoza listy nie wykryje. Pojedyncze słowa z listy („kluczowy”, „synergia”) blokują także w neutralnym kontekście. Właściciel może wtedy świadomie zostawić tekst.
- **Wykluczenia regulaminu** porównywane są tekstowo z opisem, nazwami usług i PKD. Interpretacja regulaminu (katalog wydatków, podstawa liczenia limitów) zostaje po stronie właściciela.
- **`pup-gen mapuj`** jest heurystyczny: rozpoznaje numerowane nagłówki pól i zapisy typu „max. 2000 znaków”, „do 300 słów”, „1 strona”, „N linii”. Nie rozpoznaje pól w tabelach z wieloma kolumnami ani układu SWOT 2×2. Wynik zawsze wymaga ręcznej korekty. Pola AcroForm (`/MaxLen`) wypisuje tylko z zainstalowanym `pypdf`. Bez niego PDF czyta przez `pdftotext`.
- **`pup-gen sprawdz`** przelicza kontrolę po ręcznych zmianach w `wynik.json`, ale nie odtwarza DOCX.
- **Tryb `4_pola` (SWOT)** generuje jeden tekst z czterema nagłówkami. Rozkład na cztery pola formularza robi się przy przepisywaniu.
- Kwestionariusz w JSON trzeba dziś przygotować ręcznie albo z eksportu formularza na stronie. Konwertera z formularza www nie ma.
