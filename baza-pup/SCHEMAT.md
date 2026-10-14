# Schemat bazy regulaminów PUP (`regulaminy-pup-2026.csv`)

Jeden wiersz = jeden powiatowy urząd pracy. Kodowanie UTF-8, separator `;` (średnik), bo w polach są przecinki. Puste pole = nie ustalono. Listy w polu rozdzielamy ` | `.

| Kolumna | Typ | Opis |
|---|---|---|
| `pup_id` | slug | np. `krakow`, `nowa-sol`, `warszawa` (bez polskich znaków) |
| `nazwa_pup` | tekst | pełna nazwa, np. „Powiatowy Urząd Pracy w Nowej Soli" / „Urząd Pracy m.st. Warszawy" |
| `powiat` | tekst | |
| `wojewodztwo` | tekst | małymi literami, np. `małopolskie` |
| `miasto` | tekst | siedziba urzędu |
| `url_pup` | url | strona główna, zwykle `https://[pup].praca.gov.pl` |
| `url_regulamin` | url | aktualny regulamin / zasady przyznawania środków |
| `url_formularz` | url | formularz wniosku (PDF/DOCX) |
| `data_regulaminu` | RRRR-MM-DD | data obowiązywania regulaminu |
| `kwota_max_zl` | liczba | maksymalna kwota dofinansowania w ostatnim naborze |
| `zrodlo_finansowania` | `FP` / `EFS+` / `FP | EFS+` | |
| `grupy_docelowe` | tekst | np. `do 30 lat | 55+ | kobiety | długotrwale bezrobotni` (dla EFS+) |
| `nabor_ostatni_od` | RRRR-MM-DD | |
| `nabor_ostatni_do` | RRRR-MM-DD | |
| `nabor_tryb` | `terminowy` / `ciągły` / `do wyczerpania środków` | |
| `liczba_miejsc` | liczba | jeśli podano |
| `okres_prowadzenia_mies` | liczba | minimalny okres prowadzenia działalności (ustawowo 12) |
| `wklad_wlasny` | `wymagany` / `punktowany` / `nie` | |
| `limit_reklama_pct` | liczba | % kwoty dotacji na reklamę/stronę www |
| `limit_towar_pct` | liczba | % na towar handlowy / materiały |
| `limit_remont_pct` | liczba | % na remont/adaptację lokalu |
| `limit_samochod_pct` | liczba | % na zakup pojazdu; `0` = zakaz |
| `sprzet_uzywany` | `tak` / `nie` / `warunki: ...` | |
| `zabezpieczenia` | lista | np. `poręczenie | weksel z poręczeniem | blokada rachunku | akt notarialny | gwarancja bankowa | zastaw` |
| `liczba_poreczycieli` | liczba | przy poręczeniu |
| `dochod_poreczyciela_min_zl` | liczba | minimalny dochód poręczyciela |
| `wykluczenia_dzialalnosci` | lista | np. `handel obwoźny | sezonowa | komis | lombard | przejęcie od rodziny` |
| `karta_oceny_max_pkt` | liczba | |
| `karta_oceny_prog_pkt` | liczba | próg pozytywnej oceny |
| `kryteria_punktowane` | lista | skrót: `kwalifikacje | doświadczenie | analiza rynku | wkład własny | listy intencyjne | lokal | zabezpieczenie` |
| `komisja_rozmowa` | `tak` / `nie` / `przy wątpliwościach` | |
| `wizja_lokalna` | `tak` / `nie` / `możliwa` | |
| `termin_uzupelnien_dni` | liczba | |
| `uwagi` | tekst | wszystko, co nietypowe |
| `zrodla` | lista url | skąd dane |
| `zweryfikowano` | RRRR-MM-DD | data sprawdzenia |

Każda wartość musi pochodzić z regulaminu lub ogłoszenia urzędu. Czego nie ma w źródle, zostawiamy puste. Nie zgadujemy.
