# Źródła danych monitora naborów

Stan na 14.10.2026. Wszystko poniżej sprawdziłem zapytaniami z 14.10.2026. Przykładowe odpowiedzi są zapisane w `testy/fixtures/`.

## Podsumowanie

| Źródło | Rola w monitorze | Technika | robots.txt | Ocena |
|---|---|---|---|---|
| **Zielona Linia**, kategoria „Informacje z regionów” | strumień nr 1: wpisy „PUP X – Nabór wniosków…” z treścią (daty, kwota) | WordPress REST API, JSON | `Crawl-delay: 30`, API dozwolone | stabilne i szybkie, ale **niepełne i z opóźnieniem 0–3 dni** |
| **Strony PUP** `https://[pup].praca.gov.pl/rynek-pracy/aktualnosci` | strumień nr 2 (źródło pierwotne): lista 10–15 najnowszych aktualności urzędu | HTML, wspólny szablon (Liferay, motyw `nnk-theme`) | `Allow: /`, bez Crawl-delay | **341 z 341** urzędów obsłużonych jednym parserem |
| praca.gov.pl (portal centralny) | brak | `www.praca.gov.pl` przekierowuje na `/eurzad/` (e-usługi, aplikacja JS). Na `https://praca.gov.pl/robots.txt` odpowiada 404 | – | **brak publicznego agregatu naborów** |
| psz.praca.gov.pl (Wortal PSZ) | brak | – | `User-agent: ClaudeBot` → `Disallow: /*`, dla pozostałych `Allow: /` | nie pobierałem treści. Urzędy i nabory są i tak na subdomenach PUP |
| Profile urzędów na Facebooku | brak (tylko obserwacja ręczna) | Graph API wymaga uprawnień do strony, a scrapowania nie robimy (regulamin Meta) | – | ręcznie, np. dla PUP z regionów MVP |
| RSS asset publishera (Liferay) | brak | link `/-/asset_publisher/[id]/rss` ma tylko część urzędów (z 8 sprawdzonych nietypowych stron tylko Łowicz) | – | niepewne, nie używamy |

## 1. Zielona Linia: WordPress REST API

**Endpoint:** `GET https://zielonalinia.gov.pl/wp-json/wp/v2/posts`

| Parametr | Wartość w monitorze | Opis |
|---|---|---|
| `categories` | `235` | „Informacje z regionów” (2110 wpisów ogółem, 1796 od 1.01.2026) |
| `after` | `RRRR-MM-DDT00:00:00` | tylko wpisy opublikowane po dacie. Monitor bierze datę ostatniego udanego skanu minus 3 dni, a przy pierwszym uruchomieniu 45 dni wstecz |
| `per_page` | `100` | maksimum WordPressa |
| `page` | 1…`X-WP-TotalPages` | stronicowanie |
| `orderby`, `order` | `date`, `desc` | |
| `_fields` | `id,date,modified,link,title,content` | odchudzona odpowiedź (bez `yoast_head` itd.) |
| `search` | nie używamy | pełnotekstowe (`search=działalności` daje 943 wpisy). Lepiej pobrać całą kategorię i klasyfikować lokalnie, bo tytuły bywają ogólne („Środki z Funduszu Pracy – zaproszenie do składania wniosków”) |

Pozostałe kategorie (`/wp-json/wp/v2/categories`): 20 „Rynek pracy na co dzień”, 234 „Rynek pracy w mediach”, 9 „Rynek pracy w prawie”, 236 „Poradniki wideo”, 622 „Informacje prasowe” i inne. Do naborów potrzebna jest tylko kategoria 235.

**Nagłówki odpowiedzi:** `X-WP-Total`, `X-WP-TotalPages`, `Link: <…&page=2>; rel="next"`, `Cache-Control: no-cache`, `X-Robots-Tag: noindex`. **Brak `ETag` i `Last-Modified`** (CDN BunnyCDN), więc tańsze zapytania warunkowe nie są możliwe. Ograniczamy się parametrem `after`.

**RSS:** `https://zielonalinia.gov.pl/feed/` i `/category/informacje-z-regionow/feed/` zwracają 301 na stronę HTML, więc RSS nie działa.

**robots.txt** (`https://zielonalinia.gov.pl/robots.txt`):

```text
User-agent: *
Crawl-delay: 30
Disallow: /tmp/
Disallow: /private/
Disallow: /admin/
Disallow: /wp-admin/
Disallow: /wp-includes/
```

`/wp-json/` nie jest zablokowany. Monitor respektuje `Crawl-delay: 30`, czyli robi co najwyżej 1 zapytanie na 30 s. Dzienny skan przyrostowy to 1–2 zapytania, pełne uzupełnienie od stycznia to 18 stron, ok. 9 minut.

**Przykładowe zapytanie** (prawdziwe, 14.10.2026):

```bash
curl -s 'https://zielonalinia.gov.pl/wp-json/wp/v2/posts?categories=235&after=2026-10-13T00:00:00&per_page=100&_fields=id,date,link,title,content' \
  -A 'AlertyNaborowPUP/1.0 (kontakt: alerty@twojadomena.pl)'
```

**Odpowiedź** (fragment, jeden element tablicy):

```json
{
  "id": 17086,
  "date": "2026-10-14T13:41:18",
  "link": "https://zielonalinia.gov.pl/pup-tuchola-nabor-wnioskow-o-dofinansowanie-podjecia-dzialalnosci-gospodarczej/",
  "title": {"rendered": "PUP Tuchola &#8211; Nabór wniosków o dofinansowanie podjęcia działalności gospodarczej"},
  "content": {"rendered": "<h3>Powiatowy Urząd Pracy w Tucholi ogłasza nabór wniosków o dofinansowanie podjęcia działalności gospodarczej.</h3>\n<p>Wnioski przyjmowane będą w terminie<strong> od 19.10.2026 r. do 20.10.2026 r.</strong></p>\n<p>Wysokość dofinansowania nie może przekroczyć kwoty 6-krotności przeciętnego wynagrodzenia.</p>\n<p><a href=\"https://tuchola.praca.gov.pl/strona-glowna/-/asset_publisher/Qat7ebECUfDp/content/nabor-wnioskow-o-dofinansowanie-podjecia-dzialalnosci-gospodarczej-1?p_r_p_assetEntryId=69834237\">Więcej informacji znajduje się na stronie urzędu.</a></p>\n<p><strong>Źródło:</strong> Powiatowy Urząd Pracy w Tucholi</p>"}
}
```

Co z tego bierzemy:
- **urząd:** prefiks tytułu (`PUP Tuchola – …`, także `MUP`, `GUP`, `UPP`, `UP m.st. Warszawa`) oraz **link do strony urzędu** w treści (subdomena → `pup_id` z `pup-lista.csv`). Link wskazuje to samo ogłoszenie co lista na stronie PUP (ten sam `assetEntryId`), więc monitor łączy oba źródła w jeden wpis.
- **daty, kwotę, źródło finansowania, liczbę miejsc:** z treści, regułami z `monitor/klasyfikator.py`.

**Zasięg 2026 (I–X):** w kategorii 235 jest 1796 wpisów. Klasyfikator oznaczył **164** jako nabory na podjęcie działalności (144 FP/EFS+ i 20 PFRON), 30 jako spotkania informacyjne o zakładaniu firmy, a resztę jako inne formy (staże, bony, KFS, doposażenie) albo inne informacje. Wcześniejsze szacunki z wyszukiwarki („ok. 135”) były zaniżone. Linki do stron urzędów w treści wpisów pokrywają **ok. 310 z 341** urzędów, więc Zielona Linia nie obejmuje wszystkich PUP.

## 2. Strony PUP: wspólny szablon praca.gov.pl

Wszystkie powiatowe urzędy pracy mają strony na jednej platformie (Liferay, „Wortal PSZ”, motyw `nnk-theme`) pod adresem `https://[subdomena].praca.gov.pl`. Lista aktualności urzędu jest pod **`/rynek-pracy/aktualnosci`** (334 urzędy). Wyjątki są zapisane w kolumnie `sciezka_aktualnosci` w `pup-lista.csv`: Łowicz ma `/rynek-pracy/aktualnosci-urzedu`, a 6 urzędów (Inowrocław, Krasnystaw, Piła, Poznań, Prudnik, Przeworsk) pokazuje aktualności tylko na stronie głównej `/`.

**Selektory** (sprawdzone na Tucholi, Legnicy, Katowicach, Żorach i Gorzowie Wlkp. oraz przy weryfikacji wszystkich 341 subdomen):

| Element | Selektor CSS | Przykład |
|---|---|---|
| element listy | `.nnk-article-list .nnk-article-list-article-content` | 10 na stronie (Żory: 15) |
| data publikacji | `.nnk-article-list-article-publish-date` | `08.10.2026` |
| link | `.nnk-article-link-underline a[href]` | `https://tuchola.praca.gov.pl/rynek-pracy/aktualnosci/-/asset_publisher/8VCc6CLiHUaO/content/nabor-…-1?p_r_p_assetEntryId=69834237` |
| tytuł | `h3` wewnątrz linku (`h3.my-2.text-5`) | `Nabór wniosków o dofinansowanie podjęcia działalności gospodarczej` |
| zajawka | `.nnk-article-list-article-summary` | pierwsze ok. 150 znaków treści |
| stronicowanie | `.pagination a[href]` z parametrem `…AssetPublisherPortlet_INSTANCE_[id]_cur=2` | „Strona 1 z 74” |
| **strona ogłoszenia: tytuł** | `.asset-full-content .asset-title` | |
| **strona ogłoszenia: treść** | `.asset-full-content .asset-content .journal-content-article` | pełny tekst z datami i kwotami |
| nazwa urzędu (weryfikacja) | `h1.sr-only` | `Aktualności urzędu - Powiatowy Urząd Pracy w Tucholi` |
| wariant zapasowy (karuzela na stronie głównej, bez dat) | `a[href*='/-/asset_publisher/'][href*='/content/']` + `.nnk_slider-asset-title` | Krasnystaw, Środa Wlkp. |

**Stały identyfikator ogłoszenia** to parametr `p_r_p_assetEntryId`. To samo ogłoszenie bywa pod `/strona-glowna/-/asset_publisher/Qat7ebECUfDp/…` (link z Zielonej Linii) i pod `/rynek-pracy/aktualnosci/-/asset_publisher/8VCc6CLiHUaO/…` (lista urzędu). Kluczem deduplikacji jest `host#assetEntryId`.

**Nagłówki:** `Cache-Control: private, no-cache, no-store, must-revalidate`, **brak `ETag` i `Last-Modified`**. Monitor zapamiętuje skrót SHA-256 treści i nie parsuje strony, która się nie zmieniła. Zapytania warunkowe (`If-None-Match` / `If-Modified-Since`) wysyła automatycznie, gdy serwer poda nagłówki, więc jest gotowy na zmianę konfiguracji.

**robots.txt** (identyczny na wszystkich subdomenach, np. `https://tuchola.praca.gov.pl/robots.txt`):

```text
User-Agent: *
Allow: /
Disallow: /*/be/be/*
Disallow: /*/en/en/*
… (kombinacje wersji językowych be/en/ru/uk)
Disallow: /*?*backUrl=*
Sitemap: https://tuchola.praca.gov.pl/sitemap.xml
```

Aktualności są dozwolone. Nie ma `Crawl-delay`, a mimo to monitor traktuje wszystkie `*.praca.gov.pl` jak **jeden serwer**: najwyżej 1 zapytanie na sekundę łącznie i 4 równoległe połączenia. Pełny skan 341 urzędów to ok. 6 minut i ok. 340 zapytań, czyli 1 zapytanie na urząd. Do tego dochodzą robots.txt raz w tygodniu i najwyżej 40 stron ogłoszeń na skan.

## 3. Lista urzędów (`pup-lista.csv`)

- **Wykaz urzędów:** MRPiPS, „Wskaźniki efektywności podstawowych form aktywizacji zawodowej uzyskane w powiatowych urzędach pracy w roku 2025” (załącznik do informacji DF-VIII.6022.8.2026, [gov.pl/attachment/97f4922b-…](https://www.gov.pl/attachment/97f4922b-ed14-467c-8fe0-ec52678a2c57)). Zawiera 340 urzędów z podziałem na województwa. Dodałem **Miejski Urząd Pracy w Radomiu**, którego w tym zestawieniu nie ma, choć działa (`mupradom.praca.gov.pl`, wpisy w Zielonej Linii). Razem **341**, tyle samo, ile podaje MRPiPS na koniec 2025 r.
- **Subdomeny:** 293 z linków w treści wpisów Zielonej Linii, 38 ustalonych ręcznie (urzędy miejskie, grodzkie i „dla powiatu …”, np. `torun` = PUP dla Powiatu Toruńskiego, `muptorun` = PUP dla Miasta Torunia, `uppkrakow`, `gupkrakow`, `supnowysacz`, `ozarowmazowiecki` = powiat warszawski zachodni), 10 wygenerowanych z nazwy miasta.
- **Weryfikacja** (`narzedzia/zbuduj_liste_pup.py`, 14.10.2026): subdomenę uznajemy za potwierdzoną, gdy odpowiada 200, ma listę aktualności i w nagłówku strony widnieje nazwa urzędu zgodna z wykazem. **Potwierdzone: 341 z 341** (kolumna `subdomena_potwierdzona` = data sprawdzenia).

## 4. Czego nie robimy (świadomie)

- Nie scrapujemy Facebooka ani psz.praca.gov.pl (robots.txt blokuje tam ClaudeBota; monitor ma własny User-Agent, ale nie potrzebuje tego serwisu).
- Nie kopiujemy całych ogłoszeń do alertu: krótki opis, daty, kwota i link do źródła.
- Nie pobieramy BIP-ów (różne systemy). Regulaminy i formularze trafiają do `baza-pup/` ręcznie przy weryfikacji naboru.
- Agregatory konkurencji (Atlas Dotacji RSS, Biznesplany24) służą tylko do ręcznej kontroli kompletności.
