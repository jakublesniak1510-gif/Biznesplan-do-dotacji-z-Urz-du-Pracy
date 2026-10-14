# Strona WWW – generator statyczny

Statyczna strona usługi (bez frameworka w przeglądarce). Python 3.13 + Jinja2 generuje HTML z szablonów i danych. JavaScript jest tylko w quizie, wyszukiwarce urzędów i formularzach.

```
strona/
├── build.py                 generator: dane + szablony → public/
├── requirements.txt         Jinja2
├── dane/
│   ├── site.json            ustawienia, placeholdery, SEO (title/description), fakty 2026
│   ├── cennik.json          cennik v2 (z operacje/cennik-v2.md)
│   ├── branze.json          9 podstron branżowych
│   ├── przyklad-pup.csv     3 przykładowe urzędy (zapas, gdy brak bazy docelowej)
│   └── tresci/polityka-prywatnosci.md
├── szablony/                szablony Jinja2 + static/ (styl.css, quiz.js, urzedy.js, formularze.js, favicon.svg)
├── narzedzia/sprawdz.py     test linków wewnętrznych, kotwic, sitemap i parsowania HTML5
├── zrzuty/                  zrzuty ekranu (390 px i 1280 px)
└── public/                  WYNIK (nie commitujemy – buduje go CI)
```

## Budowa lokalnie

```bash
pip install -r strona/requirements.txt      # Jinja2
python3 strona/build.py                     # → strona/public/
python3 strona/narzedzia/sprawdz.py         # linki + HTML5 (html5lib opcjonalnie)
python3 -m http.server 8000 -d strona/public   # podgląd: http://localhost:8000/
```

Linki są ścieżkami od korzenia (`/cennik/`), więc podgląd przez `file://` nie zadziała – użyj serwera jak wyżej.

### Skąd generator bierze treści

| Treść | Źródło | Uwagi |
|---|---|---|
| FAQ na stronie głównej (10 pytań) | `docs/faq-dla-klienta.md` | numery pytań w `site.json → faq_strona_glowna`. Zmiana w FAQ = zmiana na stronie po przebudowie |
| Regulamin | `prawo/regulamin-uslugi-szkic.md` | bloki „[Uwaga dla prawnika]” są wycinane, na górze baner „wersja robocza” |
| Polityka prywatności | `strona/dane/tresci/polityka-prywatnosci.md` | napisana na podstawie `prawo/rodo-i-ai.md` (sekcja 6) |
| Podstrony urzędów | `baza-pup/regulaminy-pup-2026.csv` | jeśli plik istnieje i ma wiersze; w przeciwnym razie `dane/przyklad-pup.csv` (strony z banerem „dane przykładowe” i `noindex`). Inny plik: `python3 strona/build.py --csv plik.csv` albo `PUP_CSV=plik.csv` |
| Cennik, branże, SEO | `strona/dane/*.json` | |

CSV musi mieć kolumny z `baza-pup/SCHEMAT.md` (separator `;`, listy ` | `). Generator: pomija linie zaczynające się od `#`, scala nadmiarowe średniki w kolumnie `uwagi` (z ostrzeżeniem), pomija zduplikowane `pup_id`, ostrzega o pustym `url_regulamin` i braku daty weryfikacji. Sekcja „Co to oznacza dla Twojego wniosku” powstaje automatycznie z wartości (limity, poręczyciele, komisja, wkład własny, tryb naboru, kwota powyżej limitu ustawowego itd.).

## Wdrożenie

**GitHub Pages** – `.github/workflows/strona.yml`: przy pushu do `main` (zmiany w `strona/`, bazie PUP, FAQ lub regulaminie) buduje, sprawdza linki i publikuje `strona/public/`. Jednorazowo: *Settings → Pages → Source: GitHub Actions*. Adres i ścieżkę (`user.github.io/repo/` albo własna domena) workflow bierze z `actions/configure-pages`, więc linki działają bez zmian w `site.json`. Przy pull requestach tylko budowa i test. Sekrety nie są potrzebne.

**Netlify / Cloudflare Pages** – build command: `pip install -r strona/requirements.txt && python3 strona/build.py`, publish directory: `strona/public`. `404.html` jest w katalogu głównym (Netlify, Cloudflare i GitHub Pages używają go automatycznie).

Wartości z `site.json` można nadpisać zmiennymi środowiskowymi: `SITE_DOMENA`, `SITE_BASE_PATH`, `SITE_TALLY_URL`, `SITE_ALERTY_FORM_ACTION`, `SITE_KONTAKT_FORM_ACTION`, `SITE_EMAIL`.

## Przed startem: placeholdery do podmiany

Wszystkie są w **`strona/dane/site.json`**. `build.py` wypisuje ostrzeżenie dla każdego, który wciąż zawiera `PODMIEN` albo `example.`. Formularze z placeholderem pokazują żółty komunikat „Tryb podglądu” i nie wysyłają danych.

| Klucz | Teraz | Na co podmienić |
|---|---|---|
| `DOMENA` | `https://example.pl` | docelowa domena (kanoniczne URL, Open Graph, sitemap, robots) |
| `BASE_PATH` | `/` | zostaw `/` przy własnej domenie |
| `TALLY_URL` | `https://tally.so/r/PODMIEN` | link do formularza zamówienia w Tally. Przyciski pakietów dopisują `?pakiet=podstawowy|standard|premium` – w Tally dodaj ukryte pole `pakiet` |
| `ALERTY_FORM_ACTION` | `https://example.com/PODMIEN-brevo-lub-tally-alerty` | adres `action` formularza zapisu w Brevo / Sender / Tally. Pola: `EMAIL`, `WOJEWODZTWO`, `ZGODA_ALERTY`, `ZRODLO` (ukryte), `www` (honeypot). Dopasuj nazwy do narzędzia i **włącz double opt-in** w narzędziu – strona to obiecuje |
| `KONTAKT_FORM_ACTION` | `https://example.com/PODMIEN-tally-kontakt` | formularz kontaktowy (Tally, Formspree, Netlify Forms). Pola: `imie`, `email`, `temat`, `wiadomosc`, `polityka`, `www` |
| `EMAIL` | `kontakt@example.pl` | adres kontaktowy (stopka, kontakt, schema.org) |
| `FIRMA_DANE` | `[PODMIEN: …]` | imię i nazwisko, firma, adres, NIP (stopka, klauzula przy alertach) |
| `NAZWA` | `Biznesplan do PUP` | robocza nazwa serwisu – zmień po wyborze marki |

Poza `site.json`:
- **Regulamin** (`prawo/regulamin-uslugi-szkic.md`) i **polityka prywatności** (`dane/tresci/polityka-prywatnosci.md`) mają pola `[ ]` do uzupełnienia i baner „wersja robocza do konsultacji prawnej” – usuń baner (szablon `szablony/prawny.html`) dopiero po akceptacji prawnika.
- **Limit ustawowy** (`site.json → fakty`) obowiązuje do 30.11.2026. W listopadzie wpisz wartość z komunikatu GUS za III kw. (od 1.12.2026), także `limit_liczba`.
- **Baza urzędów**: dopóki `baza-pup/regulaminy-pup-2026.csv` nie istnieje, strony urzędów powstają z danych przykładowych.
- Zgodnie z `marketing/seo-i-tresci.md` przed publikacją sprawdź wolumeny fraz w Keyword Planner / Search Console.

## Strony

| Ścieżka | Zawartość |
|---|---|
| `/` | obietnica, 3 wyróżniki, 5 kroków, cennik z tabelą i dopłatami, „czego nie robimy”, fakty 2026, branże, FAQ (FAQPage), alerty, CTA |
| `/quiz/` | 10–11 pytań z logiką warunkową (art. 147–148), wynik A/B/C z wyjaśnieniem i następnym krokiem, pobranie .txt, bez wysyłania danych |
| `/cennik/` | pakiety, rundy poprawek, gwarancja, dopłaty, zwroty, porównanie z alternatywami (bez nazw konkurentów) |
| `/jak-dziala/` | proces krok po kroku, co przygotować, terminy u nas i w urzędzie, AI + kontrola człowieka |
| `/branze/`, `/branze/[slug]/` | hub + 9 branż (FAQPage, Service) |
| `/urzedy/`, `/urzedy/[pup_id]/` | lista wg województw z wyszukiwarką + podstrona każdego urzędu z CSV |
| `/regulamin/`, `/polityka-prywatnosci/` | wersje robocze z banerem |
| `/kontakt/`, `/404.html`, `/sitemap.xml`, `/robots.txt` | |

Schema.org: Organization i Service (strona główna, cennik), FAQPage (strona główna, branże), BreadcrumbList (podstrony).
