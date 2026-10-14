"""Komenda `pup-gen`: generuj | mapuj | sprawdz | koszt."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

from pydantic import ValidationError

from . import KATALOG_PRZYKLADOW, KATALOG_WYNIKOW, PLIK_MODELU


def _bledy_walidacji(e: ValidationError) -> str:
    """Komunikaty bez wartości wejściowych (żeby nie wypisać danych osobowych)."""
    return "\n".join(f"  - {'.'.join(str(x) for x in b['loc']) or '(całość)'}: {b['msg']}" for b in e.errors())


def _wczytaj_kwestionariusz(plik: Path):
    from .schemat import Kwestionariusz
    try:
        return Kwestionariusz.model_validate_json(plik.read_text(encoding="utf-8"))
    except ValidationError as e:
        sys.exit(f"Kwestionariusz {plik.name} jest niepoprawny:\n{_bledy_walidacji(e)}")


def _wczytaj_mape(plik: Path):
    from .schemat import MapaFormularza
    try:
        return MapaFormularza.model_validate_json(plik.read_text(encoding="utf-8"))
    except ValidationError as e:
        sys.exit(f"Mapa formularza {plik.name} jest niepoprawna:\n{_bledy_walidacji(e)}")


def cmd_generuj(a: argparse.Namespace) -> int:
    from . import przebieg
    from .finanse import BladArkusza
    from .llm import BladLLM, klient_domyslny

    kw = _wczytaj_kwestionariusz(a.kwestionariusz)
    mapa = _wczytaj_mape(a.mapa)
    pup_id = a.regulamin or kw.nabor.pup_id or mapa.pup_id
    regulamin = przebieg.wczytaj_regulamin(pup_id, a.regulamin_csv)
    if pup_id and regulamin is None:
        print(f"UWAGA: nie znaleziono regulaminu „{pup_id}” w bazie – kontrola regulaminu będzie niepełna.")
    bez_klucza = not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))
    if bez_klucza and not a.dry_run:
        print("Brak ANTHROPIC_API_KEY – uruchamiam tryb --dry-run (atrapa modelu).")
    dry = a.dry_run or bez_klucza
    klient = klient_domyslny(dry_run=dry, model=a.model, effort=a.effort)
    try:
        wynik, raport, pliki = przebieg.generuj(kw, mapa, regulamin, klient, a.out, archiwum=a.archiwum,
                                                pdf=a.pdf, tryb="dry-run" if dry else "api")
    except (BladArkusza, BladLLM) as e:
        sys.exit(f"Błąd: {e}")
    tokeny = {}
    for p in wynik.pola:
        for k, v in p.tokeny.items():
            tokeny[k] = tokeny.get(k, 0) + v
    print(f"Gotowe: {len([p for p in wynik.pola if p.tekst])} pól tekstowych, model {wynik.model}.")
    print(f"  dokument dla klienta:  {pliki.docx}")
    if pliki.pdf:
        print(f"  PDF:                   {pliki.pdf}")
    print(f"  arkusz:                {pliki.arkusz}")
    print(f"  raport (właściciel):   {pliki.raport}")
    print(f"  kontrola: {raport.liczba('BLOKUJE')} BLOKUJE, {raport.liczba('OSTRZEŻENIE')} OSTRZEŻENIE, "
          f"{len(raport.braki)} × BRAK DANYCH · tokeny: {tokeny}")
    if raport.blokuje:
        print("  ⛔ Są błędy blokujące – nie wysyłaj klientowi przed poprawą (szczegóły w raporcie).")
    return 0


def cmd_mapuj(a: argparse.Namespace) -> int:
    from .mapowanie import mapuj
    try:
        mapa = mapuj(a.formularz, pup=a.pup or "", formularz=a.nazwa or "")
    except ValueError as e:
        sys.exit(f"Błąd: {e}")
    tekst = json.dumps(mapa, ensure_ascii=False, indent=2)
    if a.out:
        a.out.write_text(tekst, encoding="utf-8")
        print(f"Zapisano {a.out} ({len(mapa['pola'])} pól). Sprawdź i popraw przed generowaniem.")
    else:
        print(tekst)
    return 0


def cmd_sprawdz(a: argparse.Namespace) -> int:
    from . import przebieg
    if not (a.wynik / "wynik.json").exists():
        sys.exit(f"Brak {a.wynik / 'wynik.json'}")
    raport = przebieg.sprawdz_katalog(a.wynik, a.archiwum)
    print(f"Raport: {a.wynik / 'raport-kontroli-WLASCICIEL.md'}")
    print(f"{raport.liczba('BLOKUJE')} BLOKUJE, {raport.liczba('OSTRZEŻENIE')} OSTRZEŻENIE, "
          f"{raport.liczba('INFO')} INFO, {len(raport.braki)} × BRAK DANYCH")
    return 1 if raport.blokuje else 0


def cmd_koszt(a: argparse.Namespace) -> int:
    from . import finanse, przebieg, prompty
    from .koszt import CENNIK_USD_ZA_MTOK, szacuj
    from .llm import KlientClaude

    kw = _wczytaj_kwestionariusz(a.kwestionariusz)
    mapa = _wczytaj_mape(a.mapa)
    regulamin = przebieg.wczytaj_regulamin(kw.nabor.pup_id)
    # do szacunku wystarczą wartości zapisane w szablonie arkusza (bez przeliczania w LibreOffice)
    wartosci, kontrole, _ = finanse.odczytaj(PLIK_MODELU)
    fin = finanse.WynikFinansowy(plik=PLIK_MODELU, wartosci=wartosci, kontrole=kontrole,
                                 ark={n: finanse.formatuj_ark(n, v) for n, v in wartosci.items()})
    dane = prompty.blok_danych_klienta(kw, fin, regulamin)
    zapytania = [prompty.zbuduj_zapytanie(kw, p, fin, regulamin, dane_klienta=dane)
                 for p in mapa.pola if p.sekcje_tekstowe]
    klient = KlientClaude(model=a.model) if a.dokladnie and os.environ.get("ANTHROPIC_API_KEY") else None
    modele = [a.model] if a.model else list(CENNIK_USD_ZA_MTOK)
    for model in modele:
        sz = szacuj(zapytania, model, a.mnoznik_myslenia, klient if klient and klient.model == model else None)
        print(sz.tabela(a.kurs) if model == modele[0] else
              f"\n{model}: {sz.usd:.2f} USD ≈ {sz.usd * a.kurs:.2f} zł na plan (bez cache {sz.usd_bez_cache:.2f} USD)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pup-gen", description="Treści do wniosku o dofinansowanie z PUP")
    parser.add_argument("-v", "--verbose", action="store_true", help="logi INFO (bez treści kwestionariusza)")
    sub = parser.add_subparsers(dest="komenda", required=True)

    g = sub.add_parser("generuj", help="arkusz + treści pól + kontrola + DOCX")
    g.add_argument("--kwestionariusz", type=Path, required=True)
    g.add_argument("--mapa", type=Path, required=True, help="mapa pól formularza (JSON)")
    g.add_argument("--regulamin", help="pup_id z bazy regulaminów (domyślnie z kwestionariusza)")
    g.add_argument("--regulamin-csv", type=Path, help="inny plik bazy regulaminów")
    g.add_argument("--dry-run", action="store_true", help="atrapa modelu zamiast API")
    g.add_argument("--out", type=Path, required=True, help="katalog wyniku, np. wyniki/zielonow/<id>")
    g.add_argument("--archiwum", type=Path, default=KATALOG_WYNIKOW,
                   help="katalog wcześniejszych planów do testu podobieństwa (domyślnie <repo>/wyniki)")
    g.add_argument("--pdf", action="store_true", help="dodatkowo PDF przez LibreOffice")
    g.add_argument("--model", help="model Claude (domyślnie claude-opus-5-5 lub PUP_GEN_MODEL)")
    g.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"], help="domyślnie high")
    g.set_defaults(func=cmd_generuj)

    m = sub.add_parser("mapuj", help="heurystyczne pola i limity z formularza PDF/DOCX")
    m.add_argument("--formularz", type=Path, required=True)
    m.add_argument("--out", type=Path)
    m.add_argument("--pup", help="nazwa urzędu do wpisania w mapie")
    m.add_argument("--nazwa", help="nazwa formularza")
    m.set_defaults(func=cmd_mapuj)

    s = sub.add_parser("sprawdz", help="sama kontrola gotowego wyniku")
    s.add_argument("--wynik", type=Path, required=True, help="katalog z wynik.json")
    s.add_argument("--archiwum", type=Path, default=KATALOG_WYNIKOW)
    s.set_defaults(func=cmd_sprawdz)

    k = sub.add_parser("koszt", help="szacunek tokenów i kosztu API na plan")
    k.add_argument("--kwestionariusz", type=Path, default=KATALOG_PRZYKLADOW / "kwestionariusz-fryzjerka-mobilna.json")
    k.add_argument("--mapa", type=Path, default=KATALOG_PRZYKLADOW / "mapa-dluga-14-pol.json")
    k.add_argument("--model", choices=["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5"])
    k.add_argument("--mnoznik-myslenia", type=float, default=1.0,
                   help="tokeny myślenia jako wielokrotność widocznej odpowiedzi (effort high ≈ 1,0)")
    k.add_argument("--kurs", type=float, default=3.70, help="zł za 1 USD (założenie)")
    k.add_argument("--dokladnie", action="store_true", help="policz tokeny wejścia przez API (wymaga klucza)")
    k.set_defaults(func=cmd_koszt)

    a = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO if a.verbose else logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
