"""Treść alertu e-mail (HTML + tekst) i treść Issue na GitHubie. Grupowanie po województwie."""

from __future__ import annotations

import html
from collections import defaultdict
from datetime import date
from urllib.parse import urlencode

from monitor import konfiguracja as k
from monitor.klasyfikator import (
    DOTACJA_PFRON,
    STATUSY_AKTYWNE,
    ZAPOWIEDZ,
    opis_terminu,
    rozbij_tytul_zl,
    status,
)
from monitor.model import Wpis

BEZ_WOJEWODZTWA = "nieustalone"


def link_ogloszenia(w: Wpis) -> str:
    """Zawsze linkujemy do źródła pierwotnego (strona urzędu), Zielona Linia jako zapas."""
    return w.url if w.zrodlo == "pup" else (w.url_urzedu or w.url)


def url_cta(w: Wpis, dzis: date, baza: str | None = None) -> str:
    baza = baza or k.URL_ZAMOWIENIA
    parametry = {
        "utm_source": "alert",
        "utm_medium": "email",
        "utm_campaign": w.pup_id or "pup",
        "utm_content": dzis.isoformat(),
    }
    if w.pup_id:
        parametry["pup"] = w.pup_id
    return f"{baza}{'&' if '?' in baza else '?'}{urlencode(parametry)}"


def do_alertu(wpisy: list[Wpis], dzis: date) -> list[Wpis]:
    """Wpisy, które warto wysłać: nabór na działalność (także PFRON i zapowiedzi), wciąż aktualny."""
    return [w for w in wpisy if status(w, dzis) in STATUSY_AKTYWNE]


def grupuj_po_wojewodztwie(wpisy: list[Wpis]) -> dict[str, list[Wpis]]:
    grupy: dict[str, list[Wpis]] = defaultdict(list)
    for w in wpisy:
        grupy[w.wojewodztwo or BEZ_WOJEWODZTWA].append(w)
    for lista in grupy.values():
        lista.sort(key=lambda w: (w.nabor_do or "9999", w.pup_nazwa))
    return dict(sorted(grupy.items()))


def nazwa_urzedu(w: Wpis) -> str:
    if w.pup_nazwa:
        return w.pup_nazwa
    miasto, _ = rozbij_tytul_zl(w.tytul)
    return f"PUP {miasto}" if miasto else "Urząd pracy"


def _data_pl(iso: str) -> str:
    if not iso:
        return ""
    r, m, d = iso.split("-")
    return f"{d}.{m}.{r}"


def opis_dat(w: Wpis) -> str:
    if w.nabor_od and w.nabor_do:
        if w.nabor_od == w.nabor_do:
            return f"tylko {_data_pl(w.nabor_od)}"
        return f"{_data_pl(w.nabor_od)} – {_data_pl(w.nabor_do)}"
    if w.nabor_do:
        return f"do {_data_pl(w.nabor_do)}"
    if w.nabor_od and w.tryb == "do wyczerpania środków":
        return f"od {_data_pl(w.nabor_od)} do wyczerpania środków"
    if w.nabor_od:
        return f"od {_data_pl(w.nabor_od)}"
    if w.tryb:
        return w.tryb
    return "sprawdź w ogłoszeniu"


def opis_rodzaju(w: Wpis) -> str:
    if w.kategoria == DOTACJA_PFRON:
        return "środki PFRON na rozpoczęcie działalności (osoby z niepełnosprawnością)"
    if w.kategoria == ZAPOWIEDZ:
        return "zapowiedź naboru na podjęcie działalności"
    return "dofinansowanie podjęcia działalności gospodarczej"


def skrot_urzedu(w: Wpis) -> str:
    """„Powiatowy Urząd Pracy w Legnicy” → „PUP w Legnicy” (do tematu e-maila)."""
    nazwa = nazwa_urzedu(w)
    for pelna, skrot in (("Powiatowy Urząd Pracy", "PUP"), ("Miejski Urząd Pracy", "MUP"),
                         ("Grodzki Urząd Pracy", "GUP"), ("Sądecki Urząd Pracy", "SUP"), ("Urząd Pracy", "UP")):
        if nazwa.startswith(pelna):
            return skrot + nazwa[len(pelna):]
    return nazwa


def temat_emaila(wpisy: list[Wpis], wojewodztwo: str) -> str:
    if len(wpisy) == 1:
        w = wpisy[0]
        kwota = ", do " + f"{w.kwota_max_zl:,}".replace(",", " ") + " zł" if w.kwota_max_zl else ""
        kiedy = f", wnioski {opis_dat(w)}" if (w.nabor_od or w.nabor_do) else ""
        return f"Nabór na dotację na firmę – {skrot_urzedu(w)}{kwota}{kiedy}"
    liczba = len(wpisy)
    slowo = "nabory" if liczba % 10 in (2, 3, 4) and liczba % 100 not in (12, 13, 14) else "naborów"
    return f"{liczba} {slowo} na dotacje na firmę – woj. {wojewodztwo}"


def _wiersze(w: Wpis, dzis: date) -> list[tuple[str, str]]:
    wiersze = [("Rodzaj", opis_rodzaju(w)), ("Termin", f"{opis_dat(w)} ({opis_terminu(w, dzis)})")]
    if w.kwota_opis:
        wiersze.append(("Kwota", w.kwota_opis))
    if w.zrodla_finansowania:
        wiersze.append(("Źródło", ", ".join(w.zrodla_finansowania)))
    if w.grupy_docelowe:
        wiersze.append(("Dla kogo", ", ".join(w.grupy_docelowe)))
    if w.liczba_miejsc:
        wiersze.append(("Liczba miejsc", str(w.liczba_miejsc)))
    return wiersze


def tekst_alertu(wpisy: list[Wpis], wojewodztwo: str, dzis: date) -> str:
    linie = [
        "Cześć,",
        "",
        f"nowe nabory wniosków o dotację na założenie firmy (woj. {wojewodztwo}):",
        "",
    ]
    for w in wpisy:
        linie.append(f"■ {nazwa_urzedu(w)}")
        linie.append(f"  {rozbij_tytul_zl(w.tytul)[1]}")
        for etykieta, wartosc in _wiersze(w, dzis):
            linie.append(f"  {etykieta}: {wartosc}")
        linie.append(f"  Ogłoszenie i regulamin: {link_ogloszenia(w)}")
        linie.append(f"  Zamów treści do wniosku (od {k.CENA_OD}, 48 h): {url_cta(w, dzis)}")
        linie.append("")
    linie += [
        "Co przygotować już dziś: listę zakupów z cenami, dokumenty o kwalifikacjach, pomysł na lokal i klientów.",
        "",
        "Nie masz czasu pisać? W 48 h dostaniesz gotowe treści do wniosku w układzie formularza Twojego PUP.",
        f"Nie wiesz, czy się kwalifikujesz? Sprawdź w 2 minuty: {k.URL_QUIZ}",
        "",
        "Alert ma charakter informacyjny. Wiążące są ogłoszenie i regulamin urzędu. Nie gwarantujemy przyznania dotacji.",
        f"Otrzymujesz tę wiadomość, bo zapisałeś(-aś) się na alerty dla województwa {wojewodztwo}.",
        f"Wypisz się: {k.URL_WYPISZ}",
        k.DANE_ADMINISTRATORA,
    ]
    return "\n".join(linie)


def html_alertu(wpisy: list[Wpis], wojewodztwo: str, dzis: date) -> str:
    e = html.escape
    karty = []
    for w in wpisy:
        wiersze = "".join(
            f'<tr><td style="padding:2px 12px 2px 0;color:#555;white-space:nowrap">{e(a)}</td>'
            f'<td style="padding:2px 0">{e(b)}</td></tr>'
            for a, b in _wiersze(w, dzis)
        )
        karty.append(
            f"""
<div style="border:1px solid #d9e2ec;border-radius:8px;padding:16px;margin:0 0 16px">
  <div style="font-size:13px;color:#486581;text-transform:uppercase;letter-spacing:.04em">{e(nazwa_urzedu(w))}</div>
  <h2 style="font-size:18px;margin:4px 0 10px;color:#102a43">{e(rozbij_tytul_zl(w.tytul)[1])}</h2>
  <table role="presentation" style="font-size:15px;border-collapse:collapse">{wiersze}</table>
  <p style="margin:12px 0 0"><a href="{e(link_ogloszenia(w))}" style="color:#0b69a3">Ogłoszenie i regulamin na stronie urzędu</a></p>
  <p style="margin:14px 0 0"><a href="{e(url_cta(w, dzis))}" style="display:inline-block;background:#0b7a4b;color:#fff;text-decoration:none;padding:10px 18px;border-radius:6px;font-weight:bold">Zamów treści do wniosku – od {e(k.CENA_OD)}</a></p>
</div>"""
        )
    return f"""<!doctype html>
<html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(temat_emaila(wpisy, wojewodztwo))}</title></head>
<body style="margin:0;background:#f5f7fa;font-family:Arial,Helvetica,sans-serif;color:#102a43">
<div style="max-width:620px;margin:0 auto;padding:20px 16px;background:#ffffff">
  <p style="font-size:16px">Cześć,</p>
  <p style="font-size:16px">nowe nabory wniosków o dotację na założenie firmy w województwie <strong>{e(wojewodztwo)}</strong>:</p>
  {''.join(karty)}
  <p style="font-size:15px"><strong>Co przygotować już dziś:</strong> listę zakupów z cenami (linki do ofert),
  dokumenty potwierdzające kwalifikacje, pomysł na lokal i pierwszych klientów.</p>
  <p style="font-size:15px"><strong>Nie masz czasu pisać?</strong> Odpowiesz na pytania o swój pomysł, a w 48 h dostaniesz
  gotowe treści do wniosku w układzie formularza Twojego PUP, z kosztorysem. Jeśli urząd wezwie do poprawek, poprawimy je gratis.</p>
  <p style="font-size:15px">Nie wiesz, czy się kwalifikujesz? <a href="{e(k.URL_QUIZ)}" style="color:#0b69a3">Sprawdź w 2 minuty</a>.</p>
  <hr style="border:none;border-top:1px solid #d9e2ec;margin:20px 0">
  <p style="font-size:12px;color:#627d98">Alert ma charakter informacyjny. Wiążące są ogłoszenie i regulamin urzędu.
  Nie gwarantujemy przyznania dotacji.<br>Otrzymujesz tę wiadomość, bo zapisałeś(-aś) się na alerty dla województwa
  {e(wojewodztwo)}. <a href="{e(k.URL_WYPISZ)}" style="color:#627d98">Wypisz się</a> · {e(k.DANE_ADMINISTRATORA)}<br>{e(k.NAZWA_USLUGI)}</p>
</div></body></html>
"""


def markdown_issue(nowe: list[Wpis], dzis: date) -> str:
    """Treść Issue „nowe nabory do weryfikacji” dla właściciela (przed wysyłką do subskrybentów)."""
    if not nowe:
        return ""
    linie = [
        f"Skan z {dzis.strftime('%d.%m.%Y')} znalazł **{len(nowe)}** nowych naborów (do weryfikacji przed wysyłką alertu).",
        "",
    ]
    for woj, lista in grupuj_po_wojewodztwie(nowe).items():
        linie.append(f"### {woj}")
        linie.append("")
        linie.append("| Urząd | Ogłoszenie | Termin | Kwota | Źródło | Status |")
        linie.append("|---|---|---|---|---|---|")
        for w in lista:
            tytul = rozbij_tytul_zl(w.tytul)[1].replace("|", "/")
            linie.append(
                f"| {nazwa_urzedu(w)} | [{tytul}]({link_ogloszenia(w)}) | {opis_dat(w)} ({opis_terminu(w, dzis)}) "
                f"| {w.kwota_opis or '–'} | {', '.join(w.zrodla_finansowania) or '–'} | {status(w, dzis)} |"
            )
        linie.append("")
    linie.append("Checklista: [ ] termin i kwota zgodne z ogłoszeniem · [ ] link do regulaminu i formularza zapisany w bazie PUP · [ ] alert wysłany do segmentu")
    return "\n".join(linie) + "\n"
