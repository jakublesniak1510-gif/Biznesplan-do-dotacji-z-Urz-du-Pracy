"""Wiersz poleceń: `alerty skanuj`, `alerty raport`, `alerty eksport --wojewodztwo X`, `alerty wyslij`.

Uruchomienie bez instalacji: `cd alerty && python -m monitor skanuj`.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import date
from pathlib import Path

from monitor import konfiguracja as k
from monitor.alert import do_alertu
from monitor.model import Wpis
from monitor.raport import raport_markdown
from monitor.stan import Stan


def _dzis(arg: str | None) -> date:
    return date.fromisoformat(arg) if arg else date.today()


def _wybierz_pup(args, wszystkie):
    pupy = wszystkie
    if args.pup:
        ids = {x.strip() for x in args.pup.split(",")}
        pupy = [p for p in pupy if p.pup_id in ids]
    elif not args.wszystkie_pup:
        pupy = [p for p in pupy if p.subdomena_potwierdzona]
    if args.wojewodztwo:
        pupy = [p for p in pupy if p.wojewodztwo == args.wojewodztwo.lower()]
    if args.limit_pup:
        pupy = pupy[: args.limit_pup]
    return pupy


def cmd_skanuj(args) -> int:
    from monitor.skan import skanuj, zapisz_wyniki
    from monitor.zrodla import IndeksPup, wczytaj_liste_pup

    dzis = _dzis(args.dzis)
    wszystkie = wczytaj_liste_pup()
    indeks = IndeksPup(wszystkie)
    pupy = _wybierz_pup(args, wszystkie)
    zrodla = tuple(z.strip() for z in args.zrodla.split(","))
    stan = Stan.wczytaj()
    wynik = skanuj(
        stan, pupy, indeks, dzis, zrodla=zrodla,
        zl_od=date.fromisoformat(args.zl_od) if args.zl_od else None,
        strony=args.strony, szczegoly=not args.bez_szczegolow,
    )
    if not args.bez_zapisu:
        zapisz_wyniki(stan, wynik)
        k.PLIK_RAPORT.write_text(raport_markdown(stan, dzis), encoding="utf-8")
    print(json.dumps(wynik.statystyki, ensure_ascii=False, indent=1))
    if wynik.bledy:
        print(f"Błędy źródeł ({len(wynik.bledy)}):", file=sys.stderr)
        for kk, v in sorted(wynik.bledy.items()):
            print(f"  {kk}: {v}", file=sys.stderr)
    print(f"Nowe nabory do alertu: {len(wynik.nowe_do_alertu)}")
    for w in wynik.nowe_do_alertu:
        print(f"  [{w.wojewodztwo}] {w.pup_nazwa}: {w.tytul} ({w.nabor_od}–{w.nabor_do} {w.tryb})")
    # Kod 0 nawet przy błędach pojedynczych urzędów; 2 tylko gdy nic nie zadziałało
    nic = not wynik.wpisy and wynik.bledy
    return 2 if nic else 0


def cmd_raport(args) -> int:
    dzis = _dzis(args.dzis)
    stan = Stan.wczytaj()
    tekst = raport_markdown(stan, dzis)
    wyjscie = Path(args.wyjscie) if args.wyjscie else k.PLIK_RAPORT
    wyjscie.write_text(tekst, encoding="utf-8")
    print(tekst)
    return 0


def _wpisy_do_eksportu(args, dzis: date) -> list[Wpis]:
    stan = Stan.wczytaj()
    wpisy = stan.nabory() if args.wszystkie else do_alertu(stan.nabory(), dzis)
    if getattr(args, "tylko_nowe", False):
        nowe = json.loads(k.PLIK_NOWE_JSON.read_text(encoding="utf-8")) if k.PLIK_NOWE_JSON.exists() else []
        klucze = {n["klucz"] for n in nowe}
        wpisy = [w for w in wpisy if w.klucz in klucze]
    if getattr(args, "wojewodztwo", None):
        wpisy = [w for w in wpisy if w.wojewodztwo == args.wojewodztwo.lower()]
    return sorted(wpisy, key=lambda w: (w.wojewodztwo, w.nabor_do or "9999"))


def cmd_eksport(args) -> int:
    from monitor.wysylka import eksport_csv, eksport_json, eksport_kampanii

    dzis = _dzis(args.dzis)
    wpisy = _wpisy_do_eksportu(args, dzis)
    katalog = Path(args.katalog)
    nazwa = f"nabory-{args.wojewodztwo or 'polska'}-{dzis.isoformat()}".replace(" ", "-")
    pliki = []
    if args.format in ("csv", "wszystko"):
        pliki.append(eksport_csv(wpisy, katalog / f"{nazwa}.csv", dzis))
    if args.format in ("json", "wszystko"):
        pliki.append(eksport_json(wpisy, katalog / f"{nazwa}.json", dzis))
    if args.format in ("html", "wszystko"):
        pliki += eksport_kampanii(wpisy, katalog, dzis)
    print(f"Wyeksportowano naborów: {len(wpisy)}")
    for p in pliki:
        print(f"  {p}")
    return 0


def cmd_wyslij(args) -> int:
    from monitor.wysylka import wyslij_alerty

    dzis = _dzis(args.dzis)
    args.wszystkie = False
    wpisy = _wpisy_do_eksportu(args, dzis)
    for linia in wyslij_alerty(wpisy, dzis):
        print(linia)
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="alerty", description="Monitor naborów PUP na podjęcie działalności")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="polecenie", required=True)

    s = sub.add_parser("skanuj", help="pobierz źródła, zaktualizuj stan i pliki w dane/")
    s.add_argument("--zrodla", default="zl,pup", help="zl,pup (domyślnie oba)")
    s.add_argument("--pup", help="lista pup_id po przecinku, np. tuchola,legnica")
    s.add_argument("--wojewodztwo", help="tylko PUP z województwa, np. śląskie")
    s.add_argument("--limit-pup", type=int, default=0)
    s.add_argument("--wszystkie-pup", action="store_true", help="także subdomeny niepotwierdzone")
    s.add_argument("--strony", type=int, default=1, help="ile stron listy aktualności na urząd")
    s.add_argument("--zl-od", help="RRRR-MM-DD: wpisy Zielonej Linii od tej daty (domyślnie przyrostowo)")
    s.add_argument("--bez-szczegolow", action="store_true", help="nie pobieraj pełnych ogłoszeń")
    s.add_argument("--bez-zapisu", action="store_true")
    s.add_argument("--dzis", help="RRRR-MM-DD (testy)")
    s.set_defaults(func=cmd_skanuj)

    r = sub.add_parser("raport", help="raport Markdown z aktualnego stanu")
    r.add_argument("--dzis")
    r.add_argument("--wyjscie")
    r.set_defaults(func=cmd_raport)

    e = sub.add_parser("eksport", help="eksport naborów do CSV/JSON/HTML pod mailing")
    e.add_argument("--wojewodztwo")
    e.add_argument("--format", choices=["csv", "json", "html", "wszystko"], default="wszystko")
    e.add_argument("--wszystkie", action="store_true", help="także zakończone")
    e.add_argument("--tylko-nowe", action="store_true", help="tylko nowe z ostatniego skanu")
    e.add_argument("--katalog", default=str(k.KATALOG_DANE / "eksport"))
    e.add_argument("--dzis")
    e.set_defaults(func=cmd_eksport)

    w = sub.add_parser("wyslij", help="SMTP do właściciela i/lub kampania Brevo (wg zmiennych env)")
    w.add_argument("--wojewodztwo")
    w.add_argument("--tylko-nowe", action="store_true")
    w.add_argument("--dzis")
    w.set_defaults(func=cmd_wyslij)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING, format="%(levelname)s %(message)s")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
