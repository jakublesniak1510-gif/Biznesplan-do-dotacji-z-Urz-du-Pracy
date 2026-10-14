# Monitor naborów PUP (`alerty/`)

Wykrywa nabory wniosków o **dofinansowanie podjęcia działalności gospodarczej** („jednorazowe środki na podjęcie działalności”, „dotacje na rozpoczęcie działalności”) we wszystkich **341 powiatowych urzędach pracy**. Przygotowuje treść e-maila z alertem dla subskrybentów z danego województwa. Nabory trwają często 1–5 dni, a cała wartość alertu to szybkość: skan działa 2 razy dziennie (7:10 i 15:10), a ogłoszenie trafia do Issue na GitHubie zwykle kilka godzin po publikacji przez urząd.

Źródła, endpointy, selektory i robots.txt opisuje [`ZRODLA.md`](ZRODLA.md). Ostatni wynik skanu jest w [`dane/raport-skanu.md`](dane/raport-skanu.md) i `dane/nabory-2026.json`.

## Architektura

```text
                    ┌──────────────────────────────┐
 Zielona Linia API ─┤ zrodla.py                    │  pobieranie.py: User-Agent z kontaktem, robots.txt,
 (kategoria 235)    │  ├ pobierz_zielona_linia()   │  Crawl-delay, 1 zapytanie/s na *.praca.gov.pl,
 341 × praca.gov.pl ┤  ├ pobierz_wiele_pup()       │  4 połączenia, ETag/Last-Modified + skrót treści
 /rynek-pracy/…     │  └ uzupelnij_szczegoly()     │
                    └──────────────┬───────────────┘
                                   ▼
                    klasyfikator.py: kategoria (nabór na działalność / PFRON / zapowiedź / zakończenie /
                    spotkanie / inne formy / inne) + daty, tryb, kwota, FP/EFS+/PFRON, liczba miejsc, grupy
                                   ▼
                    stan.py: dane/stan.json – deduplikacja (host#assetEntryId, tytuł+PUP±5 dni),
                    scalanie Zielona Linia ↔ strona urzędu, „nowe od ostatniego skanu”, wstrzymania naborów
                                   ▼
        ┌──────────────────────────┼─────────────────────────────┐
        ▼                          ▼                             ▼
  dane/nabory-2026.json     alert.py: e-mail HTML/tekst,   wysylka.py: CSV/JSON/HTML pod Brevo,
  dane/raport-skanu.md      Issue (Markdown), UTM, grupy   kampania Brevo (szkic), SMTP do właściciela
                            po województwie
```

| Plik | Co robi |
|---|---|
| `monitor/zrodla.py` | pobieranie i parsowanie: Zielona Linia (WordPress REST API) i listy aktualności PUP (wspólny szablon) |
| `monitor/klasyfikator.py` | reguły regex: kategoria wpisu, parser dat („od 20.10.2026 do 24.10.2026”, „w dniach 3–7 listopada”, „do wyczerpania środków”), kwota na osobę a pula naboru, źródło finansowania, liczba miejsc, status („trwa”, „zostały 3 dni”) |
| `monitor/stan.py` | stan w JSON: znane wpisy, nowe, scalanie źródeł, oznaczanie wstrzymanych naborów |
| `monitor/alert.py` | treść e-maila (HTML i tekst), temat, CTA z UTM, Issue |
| `monitor/wysylka.py` | eksport CSV/JSON/HTML, Brevo API, SMTP (konfiguracja w zmiennych środowiskowych) |
| `monitor/pobieranie.py` | uprzejmy klient HTTP |
| `monitor/skan.py`, `monitor/raport.py`, `monitor/cli.py` | przebieg skanu, raport Markdown, wiersz poleceń |
| `pup-lista.csv` | 341 urzędów: `pup_id` (= subdomena), nazwa, województwo, miasto, url, ścieżka aktualności, data potwierdzenia subdomeny |
| `narzedzia/zbuduj_liste_pup.py`, `narzedzia/wykaz-pup.csv` | budowa i weryfikacja listy urzędów (wykaz MRPiPS + subdomeny) |
| `testy/` | pytest z prawdziwymi stronami i odpowiedziami API w `testy/fixtures/` |
| `../.github/workflows/alerty.yml` | harmonogram GitHub Actions |

## Jak uruchomić

```bash
cd alerty
pip install -r requirements.txt        # requests, beautifulsoup4, lxml, pytest
python -m pytest -q                     # testy (bez sieci)

export ALERTY_KONTAKT="alerty@twojadomena.pl"   # kontakt w User-Agent (zalecane)
python -m monitor skanuj                # wszystkie potwierdzone PUP + Zielona Linia (przyrostowo)
python -m monitor skanuj --wojewodztwo śląskie
python -m monitor skanuj --pup tuchola,legnica --zl-od 2026-10-01
python -m monitor raport                # dane/raport-skanu.md: aktywne nabory dziś
python -m monitor eksport --wojewodztwo dolnośląskie --format csv   # dane/eksport/…
python -m monitor wyslij --tylko-nowe   # SMTP/Brevo, jeśli ustawiono zmienne środowiskowe
```

Po `pip install -e .` te same polecenia działają jako `alerty skanuj`, `alerty raport` i `alerty eksport --wojewodztwo X`.

Pliki wynikowe w `dane/`:
- `stan.json`: pamięć monitora (commitowana przez workflow),
- `nabory-2026.json`: wszystkie wykryte nabory na działalność w 2026 r. z polami `status` i `dni_do_konca`,
- `nowe.json`, `nowe-alert.md`: nowe nabory z ostatniego skanu (treść Issue),
- `raport-skanu.md`: raport,
- `cache/`: ETag, skróty treści, robots.txt (poza gitem, w Actions trzymane w `actions/cache`).

**Skan pierwszy raz:** `--zl-od 2026-01-01` pobiera całą historię Zielonej Linii z 2026 r. (18 stron, ok. 9 minut przez `Crawl-delay: 30`). Każdy kolejny skan jest przyrostowy: od ostatniego skanu minus 3 dni.

## Jak dodać źródło

1. **Nowy urząd albo zmiana adresu:** popraw wiersz w `narzedzia/wykaz-pup.csv` (kolumna `kandydaci_subdomen`, kilka wartości rozdzielonych `|`) i uruchom `python narzedzia/zbuduj_liste_pup.py --tylko-niepotwierdzone`. Skrypt sprawdzi `/rynek-pracy/aktualnosci`, `/rynek-pracy/aktualnosci-urzedu` i `/`, a potem zapisze `pup-lista.csv`.
2. **Nowy typ strony:** dopisz funkcję `pobierz_xxx(klient, …) -> tuple[list[Wpis], list[str]]` w `monitor/zrodla.py` i wywołaj ją w `monitor/skan.py`, tak jak `pobierz_zielona_linia`. Zawsze pobieraj przez `Klient.pobierz()`, bo to on pilnuje robots.txt, tempa i cache. Wpis musi mieć `zrodlo`, `tytul`, `url`, `data_publikacji`, a najlepiej też `pup_id` (wtedy działa deduplikacja z innymi źródłami).
3. **Test:** zapisz prawdziwą stronę do `testy/fixtures/` (bez `<script>`) i dodaj test parsera w `testy/test_zrodla.py`.
4. **Nowe sformułowanie w ogłoszeniach** (np. inny zapis dat): dopisz przypadek do `testy/test_klasyfikator.py`, a potem regułę w `monitor/klasyfikator.py`.

## Workflow GitHub Actions

`.github/workflows/alerty.yml`:
- **harmonogram:** cron `10 5,6,13,14 * * *` UTC. GitHub nie zna czasu letniego, więc pierwszy krok przepuszcza tylko przebieg, który w Warszawie wypada o 7 albo 15. Druga para kończy się po kilku sekundach. Ręcznie: „Run workflow” z opcjonalnym województwem,
- **kroki:** testy → `skanuj` → `raport` → `eksport --tylko-nowe` → commit `alerty/dane/*.json|md` do repozytorium → przy nowych naborach **Issue** z etykietą `alert-naborow` (treść = `dane/nowe-alert.md`) → wysyłka **tylko gdy** ustawiono sekret `BREVO_API_KEY` (lub `SMTP_HOST`) → artefakt z raportem (14 dni),
- **bez sekretów w repo:** wszystkie klucze idą przez *Settings → Secrets and variables → Actions*.

Issue to „skrzynka do weryfikacji” dla właściciela: przed wysyłką do subskrybentów sprawdza termin i kwotę w ogłoszeniu oraz zapisuje regulamin i formularz w `baza-pup/` (zob. `marketing/alerty-naborow.md`, sekcja 2).

### Koszt: 0 zł

| Pozycja | Szacunek |
|---|---|
| 2 przebiegi „właściwe” dziennie | ok. 1 min przygotowania + ok. 6 min skanu 341 urzędów (1 zapytanie/s) + do 1 min na ogłoszenia = **ok. 8 min** |
| 2 przebiegi pominięte (druga strefa czasowa) | GitHub zaokrągla każde zadanie w górę, więc **1 min** każdy |
| robots.txt (raz w tygodniu, 341 hostów) | ok. +6 min tygodniowo |
| **Razem** | (2 × 8 + 2 × 1) × 30 + 4 × 6 ≈ **565 min/mies.** |

- **Repozytorium publiczne:** standardowe runnery GitHub są darmowe bez limitu minut.
- **Repozytorium prywatne (GitHub Free):** w cenie jest 2000 min/mies., 500 MB na artefakty i 10 GB cache. Monitor zużywa ok. 28% minut, a artefakty (ok. 100 kB × 60 przebiegów × 14 dni retencji) to kilka MB. Bez karty płatniczej GitHub blokuje przekroczenie limitu zamiast obciążać konto ([dokumentacja: billing GitHub Actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions)).
- Monitor tylko jednego województwa skraca skan do ok. 1 min.

## Mailing: Brevo (darmowy plan)

**Limity planu Free** (stan 10.2026 wg [centrum pomocy Brevo](https://help.brevo.com/hc/en-us/articles/208580669) i [strony newslettera Brevo](https://brevo.com/newsletter-software/), strona cennika nie pokazała liczb): **300 e-maili dziennie**, do 100 000 kontaktów, stopka „Sent with Brevo”. Kampania do ponad 300 odbiorców dochodzi tego dnia tylko do 300 osób, a resztę trzeba ponowić ręcznie. Po wyczerpaniu dziennego limitu nie da się zaplanować kampanii na następny dzień. **Wniosek:** wystarczy na start (np. 1–2 województwa, do ok. 300 subskrybentów na alert). Przy większej liście potrzebny jest plan Starter albo Sender (2500 subskrybentów i 15 000 e-maili/mies. za darmo, zob. `marketing/alerty-naborow.md`).

**Podpięcie:**
1. W Brevo utwórz **listę na każde województwo** (albo jedną listę z atrybutem `WOJEWODZTWO` i segmentami) oraz formularz zapisu z **double opt-in** (szablon potwierdzenia).
2. W sekretach repozytorium ustaw: `BREVO_API_KEY`, `BREVO_NADAWCA_EMAIL` (zweryfikowany nadawca w Brevo), `BREVO_NADAWCA_NAZWA`, `BREVO_LISTY` = JSON `{"śląskie": 3, "dolnośląskie": 4}` (id list).
3. Domyślnie workflow tworzy kampanię jako **szkic** (`POST /v3/emailCampaigns`). Właściciel zatwierdza ją w panelu po weryfikacji Issue. `BREVO_WYSYLAJ=1` wysyła od razu (`/sendNow`), ale tylko gdy klasyfikacja się sprawdziła.
4. W treści HTML link wypisu to znacznik Brevo `{{ unsubscribe }}` (`ALERTY_URL_WYPISZ`). Adres CTA ustawisz w `ALERTY_URL_ZAMOWIENIA` (UTM: `utm_source=alert&utm_medium=email&utm_campaign=[pup_id]&utm_content=[data]`). Dane administratora w stopce: `ALERTY_ADMINISTRATOR`.
5. **Inne narzędzie** (Sender, MailerLite): `python -m monitor eksport --tylko-nowe --format html` daje gotowy HTML, tekst i temat na województwo w `dane/eksport/`. Wystarczy je wkleić albo podać przez API danego narzędzia. CSV (`;`, UTF-8) nadaje się do arkusza „Nabory”.
6. **SMTP** (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM`, `ALERTY_EMAIL_WLASCICIELA`) wysyła alert **tylko właścicielowi** jako „do weryfikacji”. Subskrybenci nie dostają poczty przez SMTP, bo lista i zgody są w narzędziu mailingowym.

## RODO zapisu na alerty

Szczegóły w `prawo/rodo-i-ai.md` (sekcje 2, 3 i 8) i `marketing/alerty-naborow.md` (sekcja 5). Wymogi w skrócie:

- **Zgoda:** osobny, **niezaznaczony** checkbox obejmujący alerty **i informację handlową** (alert zawiera CTA do płatnej usługi). Podstawy: art. 6 ust. 1 lit. a RODO i art. 398 Prawa komunikacji elektronicznej. Pod formularzem skrócona klauzula: administrator, cel, podstawa, odbiorca (Brevo), okres przechowywania, prawa, link do polityki prywatności.
- **Minimum danych:** e-mail i województwo (opcjonalnie powiat i imię). Monitor **nie przetwarza danych osobowych**: w repozytorium i w GitHub Actions są tylko publiczne ogłoszenia urzędów. Lista subskrybentów jest wyłącznie w Brevo.
- **Double opt-in:** kontakt trafia na listę dopiero po kliknięciu linku potwierdzającego. Dowód zgody (data, IP, wersja treści zgody, data potwierdzenia) przechowuje Brevo. Niepotwierdzone zapisy usuwamy po 30 dniach.
- **Rezygnacja:** link „wypisz się” w każdym e-mailu (`{{ unsubscribe }}`, jedno kliknięcie), link „zmień region”, dane administratora w stopce. Dowód zgody trzymamy 3 lata od wycofania **[do weryfikacji z prawnikiem]**.
- **Umowa powierzenia:** zaakceptować DPA Brevo (firma z UE, Francja) i wpisać Brevo do rejestru czynności przetwarzania jako odbiorcę („Alerty / newsletter”).
- **Treść alertu:** krótki opis, termin, kwota i link do ogłoszenia urzędu (nie kopiujemy całych ogłoszeń) oraz zastrzeżenie „wiążące są ogłoszenie i regulamin urzędu, nie gwarantujemy przyznania dotacji”.

## Znane ograniczenia

- **Klasyfikacja regułami:** ok. 7% naborów ma ogólny tytuł („Aktualne nabory wniosków”, „Nabór na 3 formy wsparcia”). Wtedy decyduje treść, a wpis dostaje pewność „średnia”. Ostateczna weryfikacja należy do człowieka (Issue).
- **Daty:** w skanie 14.10.2026 datę naboru (od lub do) miało 85% z 168 wykrytych naborów, a termin końca albo tryb („do wyczerpania środków”) 82%. Kwotę udało się ustalić w 46%. Reszta to nabory ciągłe („do wyczerpania środków”, „do odwołania”) albo ogłoszenia bez dat. Takie wpisy mają status „do weryfikacji (brak dat)” przez 10 dni od publikacji.
- **Kwota:** często podana jako „6-krotność przeciętnego wynagrodzenia” (bez przeliczenia na zł) albo tylko jako pula naboru (opisana jako „pula naboru: X zł”).
- **Lista bez dat:** kilka urzędów pokazuje aktualności tylko w karuzeli na stronie głównej (Krasnystaw, Środa Wlkp.). Za datę publikacji przyjmujemy wtedy datę pierwszego wykrycia.
- **Zmiany w ogłoszeniach** (przedłużenie terminu bez nowego wpisu) nie są wykrywane. Wykrywamy tylko nowe wpisy „wstrzymanie / zakończenie / lista rankingowa”, które zamykają wcześniejszy nabór bez daty końca.
- **Platforma praca.gov.pl** nie wysyła `ETag` ani `Last-Modified`, więc każdy skan pobiera listę od nowa (ok. 110–170 kB na urząd, ok. 50 MB na pełny skan).
