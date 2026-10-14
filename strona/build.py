#!/usr/bin/env python3
"""Generator statycznej strony „Biznesplan do PUP”.

Użycie:
    python3 strona/build.py                 # buduje strona/public/
    SITE_DOMENA=https://moja.pl SITE_BASE_PATH=/ python3 strona/build.py   # nadpisanie site.json
    python3 strona/build.py --csv plik.csv  # inna baza urzędów
    PUP_CSV=plik.csv python3 strona/build.py

Wymaga: Python 3.11+ i Jinja2 (pip install -r strona/requirements.txt).
Dane: strona/dane/, szablony: strona/szablony/, wynik: strona/public/.
Baza urzędów: domyślnie ../baza-pup/regulaminy-pup-2026.csv (jeśli istnieje
i ma wiersze), w przeciwnym razie strona/dane/przyklad-pup.csv.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import shutil
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
    from markupsafe import Markup
except ImportError:  # pragma: no cover
    sys.exit("Brak Jinja2. Zainstaluj: pip install -r strona/requirements.txt")

ROOT = Path(__file__).resolve().parent          # strona/
REPO = ROOT.parent
DANE = ROOT / "dane"
SZABLONY = ROOT / "szablony"
PUBLIC = ROOT / "public"

OSTRZEZENIA: list[str] = []


def ostrzez(msg: str) -> None:
    OSTRZEZENIA.append(msg)


# --------------------------------------------------------------------------
# Pomocnicze
# --------------------------------------------------------------------------

def slugify(txt: str) -> str:
    txt = txt.replace("ł", "l").replace("Ł", "L")
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode()
    txt = re.sub(r"[^a-zA-Z0-9]+", "-", txt).strip("-").lower()
    return txt


def fmt_zl(val) -> str:
    """40000 -> '40 000 zł' (twarda spacja jako separator tysięcy)."""
    if val in (None, ""):
        return ""
    try:
        num = float(str(val).replace(" ", "").replace(" ", "").replace(",", "."))
    except ValueError:
        return str(val)
    if num.is_integer():
        s = f"{int(num):,}".replace(",", " ")
    else:
        s = f"{num:,.2f}".replace(",", " ").replace(".", ",")
    return f"{s} zł"


def parse_data(val: str) -> date | None:
    if not val:
        return None
    for f in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(val.strip(), f).date()
        except ValueError:
            pass
    return None


def fmt_data(val) -> str:
    d = val if isinstance(val, date) else parse_data(str(val or ""))
    if not d:
        return str(val or "")
    return f"{d.day}.{d.month:02d}.{d.year}"


def lista(val: str) -> list[str]:
    if not val:
        return []
    return [x.strip() for x in str(val).split("|") if x.strip()]


def liczba(val: str) -> float | None:
    if val in (None, ""):
        return None
    try:
        return float(str(val).replace(",", ".").replace("%", "").strip())
    except ValueError:
        return None


NBSP = "\u00a0"


def typografia(html_txt: str) -> str:
    """Twarde spacje w węzłach tekstowych: liczby (1 350), jednostki (299 zł, 24 h), jednoliterowe spójniki."""
    out, w_skrypcie = [], False
    for part in re.split(r"(<[^>]+>)", html_txt):
        if part.startswith("<"):
            low = part[:8].lower()
            if low.startswith(("<script", "<style")):
                w_skrypcie = True
            elif low.startswith(("</script", "</style")):
                w_skrypcie = False
            out.append(part)
            continue
        if not w_skrypcie and part.strip():
            part = re.sub(r"(\d) (\d{3})(?!\d)", r"\1" + NBSP + r"\2", part)
            part = re.sub(r"(\d) (zł|h|dni|mies\.|tys\.|pkt|%|lat)(?![\w])", r"\1" + NBSP + r"\2", part)
            part = re.sub(r"(?<![\w\-])([wzioauWZIOAU]) ", r"\1" + NBSP, part)
        out.append(part)
    return "".join(out)


def strip_tags(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


# --------------------------------------------------------------------------
# Mini-Markdown (nagłówki, akapity, listy, tabele, cytaty, pogrubienia, linki)
# --------------------------------------------------------------------------

def md_inline(txt: str) -> str:
    txt = txt.replace("\\*", "\x00")
    codes: list[str] = []

    def _code(m):
        codes.append(m.group(1))
        return f"\x01{len(codes) - 1}\x01"

    txt = re.sub(r"`([^`]+)`", _code, txt)
    txt = html.escape(txt, quote=False)
    txt = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+|/[^)\s]*|#[^)\s]*)\)",
                 lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', txt)
    txt = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", txt)
    txt = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", txt)
    txt = re.sub(r"\x01(\d+)\x01", lambda m: f"<code>{html.escape(codes[int(m.group(1))])}</code>", txt)
    return txt.replace("\x00", "*")


def md_to_html(md: str, toc: list | None = None, h_offset: int = 0) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    def is_block_start(s: str) -> bool:
        return bool(re.match(r"^(#{1,6} |\s*[-*] |\s*\d+\. |>|\||---\s*$)", s))

    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^(#{1,6}) (.+)$", line)
        if m:
            lvl = min(6, len(m.group(1)) + h_offset)
            text = m.group(2).strip()
            hid = slugify(strip_tags(md_inline(text)))[:60]
            if toc is not None and lvl == 2:
                toc.append((hid, strip_tags(md_inline(text))))
            out.append(f'<h{lvl} id="{hid}">{md_inline(text)}</h{lvl}>')
            i += 1
            continue
        if re.match(r"^---\s*$", line):
            out.append("<hr>")
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < n and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            head = cells[0]
            body = [c for c in cells[1:] if not all(re.match(r"^:?-+:?$", x) for x in c)]
            t = ['<div class="tbl-wrap"><table class="tbl"><thead><tr>']
            t += [f'<th scope="col">{md_inline(h)}</th>' for h in head]
            t.append("</tr></thead><tbody>")
            for r in body:
                t.append("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue
        if line.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            out.append(f"<blockquote>{md_to_html(chr(10).join(buf))}</blockquote>")
            continue
        lm = re.match(r"^(\s*)([-*]|\d+\.) (.*)$", line)
        if lm:
            ordered = lm.group(2)[0].isdigit()
            tag = "ol" if ordered else "ul"
            items: list[list[str]] = []
            while i < n:
                cur = lines[i]
                mm = re.match(r"^([-*]|\d+\.) (.*)$", cur)
                if mm and (mm.group(1)[0].isdigit()) == ordered:
                    items.append([mm.group(2)])
                    i += 1
                elif cur.startswith(("  ", "\t")) and cur.strip() and items:
                    items[-1].append(cur.strip())
                    i += 1
                elif not cur.strip() and i + 1 < n and lines[i + 1].startswith(("  ", "\t")) and items:
                    i += 1
                else:
                    break
            parts = [f"<{tag}>"]
            for it in items:
                first, rest = it[0], it[1:]
                li = md_inline(first)
                sub_quote = [r for r in rest if r.startswith(">")]
                sub_list = [r for r in rest if re.match(r"^([-*]|\d+\.) ", r)]
                plain = [r for r in rest if r not in sub_quote and r not in sub_list]
                for p in plain:
                    li += "<br>" + md_inline(p)
                if sub_list:
                    li += md_to_html("\n".join(sub_list))
                if sub_quote:
                    li += f"<blockquote>{md_to_html(chr(10).join(re.sub(r'^>\s?', '', q) for q in sub_quote))}</blockquote>"
                parts.append(f"<li>{li}</li>")
            parts.append(f"</{tag}>")
            out.append("".join(parts))
            continue
        buf = []
        while i < n and lines[i].strip() and not (buf and is_block_start(lines[i])):
            buf.append(lines[i].strip())
            i += 1
        para = ""
        for j, b in enumerate(buf):
            sep = "" if j == 0 else ("<br>" if b.startswith("–") else " ")
            para += sep + md_inline(b)
        out.append(f"<p>{para}</p>")
    return "\n".join(out)


# --------------------------------------------------------------------------
# Źródła treści
# --------------------------------------------------------------------------

def wczytaj_faq(path: Path) -> dict[int, dict]:
    if not path.exists():
        ostrzez(f"Brak pliku FAQ: {path}")
        return {}
    txt = path.read_text(encoding="utf-8")
    faq: dict[int, dict] = {}
    cur = None
    buf: list[str] = []

    def zapisz():
        if cur:
            body = "\n".join(buf).strip()
            body = re.sub(r"\n---\s*$", "", body).strip()
            faq[cur[0]] = {"nr": cur[0], "q": cur[1], "a_html": md_to_html(body)}

    for line in txt.split("\n"):
        m = re.match(r"^\*\*(\d+)\.\s+(.+?)\*\*\s*$", line)
        if m:
            zapisz()
            cur = (int(m.group(1)), m.group(2).strip())
            buf = []
        elif line.startswith("## ") or line.strip() == "---":
            zapisz()
            cur = None
            buf = []
        elif cur:
            buf.append(line)
    zapisz()
    return faq


def przygotuj_regulamin(path: Path, url_polityki: str) -> str:
    if not path.exists():
        ostrzez(f"Brak szkicu regulaminu: {path}")
        return "Brak treści."
    md = path.read_text(encoding="utf-8")
    md = re.sub(r"^# ⚠️.*\n", "", md, count=1, flags=re.M)
    md = re.sub(r"^# .*\n", "", md, count=1, flags=re.M)
    # usunięcie notatek dla prawnika (bloki cytatu z „[Uwaga dla prawnika]”)
    bloki, buf = [], []
    for line in md.split("\n"):
        if line.startswith(">"):
            buf.append(line)
            continue
        if buf:
            if "Uwaga dla prawnika" not in "\n".join(buf):
                bloki.extend(buf)
            buf = []
        bloki.append(line)
    if buf and "Uwaga dla prawnika" not in "\n".join(buf):
        bloki.extend(buf)
    md = "\n".join(bloki)
    md = md.replace("Komentarze dla prawnika są w blokach **[Uwaga dla prawnika]**. ", "")
    md = re.sub(r"\s*\(zob\. `[^`]+`\)", "", md)
    md = md.replace("Polityka prywatności [link]", f"[Polityka prywatności]({url_polityki})")
    return md


def wczytaj_pup(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8-sig")
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    reader = csv.reader(lines, delimiter=";")
    header = [h.strip() for h in next(reader)]
    wymagane = {"pup_id", "nazwa_pup", "wojewodztwo"}
    if not wymagane.issubset(header):
        ostrzez(f"{path.name}: brak wymaganych kolumn {sorted(wymagane - set(header))}")
        return []
    idx_uwagi = header.index("uwagi") if "uwagi" in header else None
    rows = []
    for nr, row in enumerate(reader, start=2):
        if len(row) > len(header) and idx_uwagi is not None:
            extra = len(row) - len(header)
            ostrzez(f"{path.name}, wiersz {nr}: {extra} nadmiarowych średników – scalam w kolumnie „uwagi”")
            row = row[:idx_uwagi] + [";".join(row[idx_uwagi:idx_uwagi + extra + 1])] + row[idx_uwagi + extra + 1:]
        if len(row) < len(header):
            row = row + [""] * (len(header) - len(row))
        d = {h: (v or "").strip() for h, v in zip(header, row)}
        if not d.get("pup_id") and not d.get("nazwa_pup"):
            continue
        rows.append(d)
    return rows


def ocena_pup(d: dict, dzis: date, przyklad_plik: bool, limit_ust: float | None = None) -> dict:
    """Wzbogaca wiersz CSV o pola do szablonu i wnioski „co to oznacza”."""
    pid = slugify(d.get("pup_id") or d.get("nazwa_pup"))
    uwagi = d.get("uwagi", "")
    przyklad = przyklad_plik or "[PRZYKŁAD]" in uwagi
    uwagi = uwagi.replace("[PRZYKŁAD]", "").strip()
    woj = (d.get("wojewodztwo") or "").strip().lower() or "nieustalone"

    kwota = liczba(d.get("kwota_max_zl"))
    nab_od, nab_do = parse_data(d.get("nabor_ostatni_od")), parse_data(d.get("nabor_ostatni_do"))
    zweryf = parse_data(d.get("zweryfikowano"))

    if nab_do and nab_do >= dzis and (not nab_od or nab_od <= dzis):
        nabor_status = ("trwa", "Nabór trwa")
    elif nab_od and nab_od > dzis:
        nabor_status = ("wkrotce", "Nabór zapowiedziany")
    elif nab_od or nab_do:
        nabor_status = ("zakonczony", "Ostatni nabór zakończony")
    else:
        nabor_status = ("brak", "Brak danych o naborze")

    w: list[dict] = []  # wnioski: {typ: ok|uwaga|info, t: tekst}
    if kwota:
        w.append({"typ": "info", "t": f"Kosztorys budujemy do {fmt_zl(kwota)} – maksimum z ostatniego naboru. Komisja może przyznać mniej, więc każda pozycja musi mieć uzasadnienie i ofertę."})
        if limit_ust and kwota > limit_ust:
            w.append({"typ": "uwaga", "t": f"Ta kwota przekracza obecny limit ustawowy ({fmt_zl(limit_ust)}). Liczy się limit z dnia zawarcia umowy, więc w kolejnym naborze maksimum może być niższe."})
    else:
        w.append({"typ": "info", "t": "Maksymalnej kwoty nie ustaliliśmy w źródle. Sprawdzimy ją w ogłoszeniu o naborze, zanim przygotujemy kosztorys."})
    if d.get("zrodlo_finansowania", "").upper().startswith("EFS") or "EFS" in d.get("zrodlo_finansowania", ""):
        grupy = lista(d.get("grupy_docelowe"))
        t = "Nabór z EFS+ ma grupy docelowe" + (f": {', '.join(grupy)}" if grupy else "") + ". Sprawdź, czy do którejś należysz – inaczej wniosek odpadnie formalnie."
        w.append({"typ": "uwaga", "t": t})
    samochod = liczba(d.get("limit_samochod_pct"))
    if samochod is not None:
        if samochod == 0:
            w.append({"typ": "uwaga", "t": "Samochodu nie kupisz z dotacji – regulamin wyklucza pojazdy."})
        else:
            w.append({"typ": "info", "t": f"Pojazd może kosztować najwyżej {samochod:g}% kwoty dotacji."})
    remont = liczba(d.get("limit_remont_pct"))
    if remont is not None:
        if remont == 0:
            w.append({"typ": "uwaga", "t": "Remont i adaptacja lokalu są wykluczone. Jeśli lokal wymaga prac, opiszemy je jako wkład własny."})
        else:
            w.append({"typ": "info", "t": f"Na remont lub adaptację lokalu możesz przeznaczyć do {remont:g}% kwoty."})
    towar = liczba(d.get("limit_towar_pct"))
    if towar is not None:
        w.append({"typ": "info", "t": f"Towar i materiały: do {towar:g}% kwoty. W handlu i sklepie internetowym kosztorys opieramy na wyposażeniu."})
    reklama = liczba(d.get("limit_reklama_pct"))
    if reklama is not None:
        w.append({"typ": "info", "t": f"Reklama i strona www: do {reklama:g}% kwoty."})
    if d.get("sprzet_uzywany"):
        su = d["sprzet_uzywany"]
        if su.lower() == "nie":
            w.append({"typ": "uwaga", "t": "Sprzęt używany jest wykluczony – w kosztorysie tylko nowe rzeczy."})
        elif su.lower() != "tak":
            w.append({"typ": "info", "t": "Sprzęt używany tylko na warunkach regulaminu: " + re.sub(r"^warunki:\s*", "", su) + "."})
    porecz = liczba(d.get("liczba_poreczycieli"))
    dochod = liczba(d.get("dochod_poreczyciela_min_zl"))
    if porecz:
        t = f"Przy poręczeniu potrzebujesz {int(porecz)} {'poręczyciela' if porecz == 1 else 'poręczycieli'}"
        if dochod:
            t += f" z dochodem co najmniej {fmt_zl(dochod)}"
        w.append({"typ": "uwaga", "t": t + ". Sprawdź to przed zamówieniem – bez zabezpieczenia urząd nie podpisze umowy."})
    elif d.get("zabezpieczenia"):
        w.append({"typ": "uwaga", "t": "Zabezpieczenie jest obowiązkowe. Dopuszczone formy: " + ", ".join(lista(d["zabezpieczenia"])) + "."})
    if d.get("wklad_wlasny") == "wymagany":
        w.append({"typ": "uwaga", "t": "Wkład własny jest wymagany. Uwzględnimy go w kalkulacji kosztów ze źródłami finansowania."})
    elif d.get("wklad_wlasny") == "punktowany":
        w.append({"typ": "ok", "t": "Wkład własny daje punkty. Jeśli możesz dołożyć własne środki lub sprzęt, opiszemy je tak, żeby komisja je policzyła."})
    kryt = " ".join(lista(d.get("kryteria_punktowane"))).lower()
    if "intencyj" in kryt or "kontrahent" in kryt:
        w.append({"typ": "ok", "t": "Urząd punktuje kontakty z przyszłymi klientami lub kontrahentami. Warto zebrać listy intencyjne (dopłata 79 zł: szablon i do 3 listów)."})
    if "kwalifikacj" in kryt or "wykształc" in kryt or "doświadcz" in kryt or "przygotowanie" in kryt:
        w.append({"typ": "ok", "t": "Kwalifikacje i doświadczenie są w karcie oceny. Zbierz dokumenty (dyplomy, certyfikaty, świadectwa pracy) – opiszemy je pod kryteria."})
    if d.get("komisja_rozmowa") == "tak":
        w.append({"typ": "uwaga", "t": "Przed komisją trzeba się stawić osobiście. Przygotuj krótką prezentację pomysłu – w Premium robimy próbę rozmowy."})
    elif d.get("komisja_rozmowa") == "przy wątpliwościach":
        w.append({"typ": "info", "t": "Komisja zaprasza na rozmowę tylko przy wątpliwościach. Im jaśniejszy wniosek, tym mniejsza szansa na dodatkowe pytania."})
    if d.get("wizja_lokalna") in ("tak", "możliwa"):
        w.append({"typ": "uwaga", "t": "Urząd może obejrzeć lokal. Opis we wniosku musi zgadzać się z rzeczywistością."})
    okres = liczba(d.get("okres_prowadzenia_mies"))
    if okres and okres > 12:
        w.append({"typ": "uwaga", "t": f"Firmę trzeba prowadzić co najmniej {okres:g} miesięcy – dłużej niż minimum ustawowe (12)."})
    if d.get("nabor_tryb") == "do wyczerpania środków":
        w.append({"typ": "uwaga", "t": "Nabór trwa do wyczerpania środków. Liczy się gotowy wniosek w dniu otwarcia – przygotuj go wcześniej."})
    if d.get("termin_uzupelnien_dni"):
        w.append({"typ": "info", "t": f"Na uzupełnienie braków urząd daje {d['termin_uzupelnien_dni']} dni. Wezwanie prześlij nam od razu – poprawki robimy w 24 h robocze w ramach gwarancji."})
    if lista(d.get("wykluczenia_dzialalnosci")):
        w.append({"typ": "uwaga", "t": "Regulamin wyklucza część działalności (lista wyżej). Jeśli Twój pomysł jest na liście, nie przyjmiemy zlecenia i zwrócimy 100% ceny."})

    stare = bool(zweryf and (dzis - zweryf).days > 180)
    if not zweryf:
        ostrzez(f"PUP {pid}: brak daty weryfikacji")
    for pole in ("url_regulamin",):
        if not d.get(pole):
            ostrzez(f"PUP {pid}: puste pole {pole}")

    return {
        **d,
        "id": pid,
        "woj": woj,
        "woj_slug": slugify(woj),
        "przyklad": przyklad,
        "uwagi_txt": uwagi,
        "kwota_txt": fmt_zl(kwota) if kwota else "",
        "zrodlo_txt": " i ".join(lista(d.get("zrodlo_finansowania"))),
        "nabor_od_txt": fmt_data(nab_od) if nab_od else "",
        "nabor_do_txt": fmt_data(nab_do) if nab_do else "",
        "nabor_status": nabor_status,
        "zweryf_txt": fmt_data(zweryf) if zweryf else "",
        "zweryf_stare": stare,
        "data_reg_txt": fmt_data(d.get("data_regulaminu")) if d.get("data_regulaminu") else "",
        "l_zabezp": lista(d.get("zabezpieczenia")),
        "l_wykl": lista(d.get("wykluczenia_dzialalnosci")),
        "l_kryt": lista(d.get("kryteria_punktowane")),
        "l_grupy": lista(d.get("grupy_docelowe")),
        "l_zrodla": [u for u in lista(d.get("zrodla")) if u.startswith("http")],
        "wnioski": w,
    }


# --------------------------------------------------------------------------
# Budowa
# --------------------------------------------------------------------------

def jsonld(obj) -> Markup:
    s = json.dumps(obj, ensure_ascii=False, indent=None, separators=(",", ":"))
    return Markup(s.replace("</", "<\\/"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", help="ścieżka do CSV z bazą urzędów (nadpisuje domyślną)")
    ap.add_argument("--out", default=str(PUBLIC), help="katalog wynikowy (domyślnie strona/public)")
    args = ap.parse_args()

    site = json.loads((DANE / "site.json").read_text(encoding="utf-8"))
    cennik = json.loads((DANE / "cennik.json").read_text(encoding="utf-8"))
    branze = json.loads((DANE / "branze.json").read_text(encoding="utf-8"))
    out = Path(args.out).resolve()
    # Nadpisanie z ENV (np. w GitHub Actions: adres i ścieżka z actions/configure-pages)
    for k in ("DOMENA", "BASE_PATH", "TALLY_URL", "ALERTY_FORM_ACTION", "KONTAKT_FORM_ACTION", "EMAIL"):
        if os.environ.get("SITE_" + k):
            site[k] = os.environ["SITE_" + k]

    base = site["BASE_PATH"]
    if not base.startswith("/"):
        base = "/" + base
    if not base.endswith("/"):
        base += "/"
    domena = site["DOMENA"].rstrip("/")
    dzis = date.today()

    def u(path: str = "") -> str:
        return base + path.lstrip("/")

    def abs_url(path: str = "") -> str:
        return domena + u(path)

    def tally(pakiet: str | None = None) -> str:
        url = site["TALLY_URL"]
        if pakiet:
            url += ("&" if "?" in url else "?") + "pakiet=" + pakiet
        return url

    # --- baza urzędów ---
    zr = site["zrodla_tresci"]
    csv_path = None
    przyklad_plik = False
    kandydat = args.csv or os.environ.get("PUP_CSV")
    if kandydat:
        csv_path = Path(kandydat).resolve()
    else:
        docelowy = (ROOT / zr["pup_csv"]).resolve()
        if docelowy.exists() and wczytaj_pup(docelowy):
            csv_path = docelowy
        else:
            if docelowy.exists():
                ostrzez(f"{docelowy} istnieje, ale nie ma poprawnych wierszy – używam danych przykładowych")
            csv_path = (ROOT / zr["pup_csv_przyklad"]).resolve()
            przyklad_plik = True
    if not csv_path.exists():
        sys.exit(f"Brak pliku CSV: {csv_path}")
    przyklad_plik = przyklad_plik or csv_path == (ROOT / zr["pup_csv_przyklad"]).resolve()
    pupy_raw = wczytaj_pup(csv_path)
    pupy = []
    widziane = set()
    for d in pupy_raw:
        p = ocena_pup(d, dzis, przyklad_plik, site["fakty"].get("limit_liczba"))
        if p["id"] in widziane:
            ostrzez(f"Zduplikowany pup_id: {p['id']} – pomijam kolejne wystąpienie")
            continue
        widziane.add(p["id"])
        pupy.append(p)
    pupy.sort(key=lambda p: (p["woj"], p.get("miasto") or p.get("nazwa_pup")))
    woj_kolejnosc = site["wojewodztwa"]
    pupy_wg_woj: dict[str, list] = {}
    for p in pupy:
        pupy_wg_woj.setdefault(p["woj"], []).append(p)
    pupy_wg_woj = dict(sorted(pupy_wg_woj.items(),
                              key=lambda kv: woj_kolejnosc.index(kv[0]) if kv[0] in woj_kolejnosc else 99))

    # --- FAQ ---
    faq_all = wczytaj_faq((ROOT / zr["faq"]).resolve())
    faq_home = [faq_all[n] for n in site["faq_strona_glowna"] if n in faq_all]
    if len(faq_home) != len(site["faq_strona_glowna"]):
        ostrzez("Nie wszystkie pytania FAQ ze strony głównej znaleziono w docs/faq-dla-klienta.md")

    # --- teksty prawne ---
    toc_reg: list = []
    toc_pol: list = []
    reg_html = md_to_html(przygotuj_regulamin((ROOT / zr["regulamin"]).resolve(), u("polityka-prywatnosci/")), toc_reg)
    pol_md = (ROOT / zr["polityka"]).read_text(encoding="utf-8")
    pol_md = re.sub(r"^# .*\n", "", pol_md, count=1)
    pol_html = md_to_html(pol_md, toc_pol)

    # --- Jinja ---
    env = Environment(loader=FileSystemLoader(str(SZABLONY)), autoescape=select_autoescape(["html", "xml"]),
                      undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
    env.filters["zl"] = fmt_zl
    env.filters["data"] = fmt_data
    env.filters["jsonld"] = jsonld
    env.globals.update(u=u, abs_url=abs_url, tally=tally, site=site, cennik=cennik, branze=branze,
                       pupy=pupy, pupy_wg_woj=pupy_wg_woj, przyklad_plik=przyklad_plik,
                       rok=dzis.year, placeholder=lambda v: "PODMIEN" in str(v) or "example." in str(v))

    org = {"@type": "Organization", "@id": abs_url("#org"), "name": site["NAZWA"], "url": abs_url(), "email": site["EMAIL"]}
    service = {
        "@type": "Service", "name": "Treści do wniosku o dofinansowanie podjęcia działalności gospodarczej z PUP",
        "serviceType": "Przygotowanie treści wniosku o dotację z urzędu pracy", "provider": {"@id": abs_url("#org")},
        "areaServed": {"@type": "Country", "name": "Polska"},
        "offers": [{"@type": "Offer", "name": f"Pakiet {p['nazwa']}", "price": str(p["cena"]), "priceCurrency": "PLN",
                    "url": abs_url("cennik/")} for p in cennik["pakiety"]],
    }

    def faq_ld(items):
        return {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": strip_tags(q.get("a_html") or q.get("a", ""))}}
            for q in items]}

    def crumbs_ld(crumbs):
        return {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": abs_url(path)} for i, (name, path) in enumerate(crumbs)]}

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    sitemap: list[tuple[str, str, str]] = []

    def render(tpl: str, path: str, seo: dict, crumbs: list | None = None, ld: list | None = None,
               sitemap_prio: str | None = "0.6", **ctx):
        crumbs_full = [("Strona główna", "")] + (crumbs or [])
        graph = list(ld or [])
        if crumbs:
            graph.append(crumbs_ld(crumbs_full))
        ld_obj = {"@context": "https://schema.org", "@graph": graph} if graph else None
        html_out = env.get_template(tpl).render(
            seo=seo, path=path, canonical=abs_url(path), crumbs=crumbs_full if crumbs else None,
            ld=jsonld(ld_obj) if ld_obj else None, **ctx)
        target = out / path / "index.html" if (path == "" or path.endswith("/")) else out / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(typografia(html_out), encoding="utf-8")
        if sitemap_prio:
            sitemap.append((abs_url(path), sitemap_prio, ctx.get("lastmod", site["STAN_NA"])))

    S = site["seo"]
    render("index.html", "", S["index"], ld=[org, service, faq_ld(faq_home)], sitemap_prio="1.0", faq=faq_home)
    render("quiz.html", "quiz/", S["quiz"], crumbs=[("Quiz kwalifikacyjny", "quiz/")], sitemap_prio="0.9",
           quiz_config=jsonld({
               "wojewodztwa": site["wojewodztwa"],
               "pupy": [{"id": p["id"], "nazwa": p["nazwa_pup"], "woj": p["woj"], "url": u(f"urzedy/{p['id']}/")} for p in pupy],
               "linki": {"zamow": tally(), "alert": u("") + "#alerty", "urzedy": u("urzedy/"), "cennik": u("cennik/"),
                         "kontakt": u("kontakt/"), "jak": u("jak-dziala/")},
               "stan_na": site["STAN_NA_TXT"],
           }))
    render("cennik.html", "cennik/", S["cennik"], crumbs=[("Cennik", "cennik/")], ld=[org, service], sitemap_prio="0.9")
    render("jak-dziala.html", "jak-dziala/", S["jak-dziala"], crumbs=[("Jak to działa", "jak-dziala/")], sitemap_prio="0.8")
    render("branze.html", "branze/", S["branze"], crumbs=[("Branże", "branze/")], sitemap_prio="0.7")
    for b in branze:
        render("branza.html", f"branze/{b['slug']}/", {"title": b["title"], "description": b["description"]},
               crumbs=[("Branże", "branze/"), (b["nazwa"], f"branze/{b['slug']}/")],
               ld=[service, faq_ld(b["faq"])], sitemap_prio="0.7", b=b)
    render("urzedy.html", "urzedy/", S["urzedy"], crumbs=[("Urzędy pracy", "urzedy/")], sitemap_prio="0.7")
    for p in pupy:
        tytul = f"Dotacja z PUP {p.get('miasto') or p['nazwa_pup']}: kwota, nabór, regulamin"
        opis = (f"{p['nazwa_pup']}: " + (f"do {p['kwota_txt']}, " if p["kwota_txt"] else "")
                + "limity w kosztorysie, zabezpieczenia, karta oceny i komisja. Co to oznacza dla Twojego wniosku.")
        render("urzad.html", f"urzedy/{p['id']}/", {"title": tytul, "description": opis[:300]},
               crumbs=[("Urzędy pracy", "urzedy/"), (p.get("miasto") or p["nazwa_pup"], f"urzedy/{p['id']}/")],
               sitemap_prio="0.5" if p["przyklad"] else "0.6", lastmod=parse_data(p.get("zweryfikowano")) and p["zweryfikowano"] or site["STAN_NA"],
               p=p, robots="noindex,follow" if p["przyklad"] else None)
    render("prawny.html", "regulamin/", S["regulamin"], crumbs=[("Regulamin", "regulamin/")], sitemap_prio="0.2",
           tresc=Markup(reg_html), toc=toc_reg, naglowek="Regulamin świadczenia usługi")
    render("prawny.html", "polityka-prywatnosci/", S["polityka-prywatnosci"], crumbs=[("Polityka prywatności", "polityka-prywatnosci/")],
           sitemap_prio="0.2", tresc=Markup(pol_html), toc=toc_pol, naglowek="Polityka prywatności")
    render("kontakt.html", "kontakt/", S["kontakt"], crumbs=[("Kontakt", "kontakt/")], sitemap_prio="0.4")
    render("404.html", "404.html", S["404"], sitemap_prio=None)

    # --- sitemap, robots, statyczne ---
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio, lastmod in sitemap:
        sm.append(f"  <url><loc>{html.escape(loc)}</loc><lastmod>{lastmod}</lastmod><priority>{prio}</priority></url>")
    sm.append("</urlset>")
    (out / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {abs_url('sitemap.xml')}\n", encoding="utf-8")
    shutil.copytree(SZABLONY / "static", out / "assets")
    (out / ".nojekyll").write_text("", encoding="utf-8")

    # --- raport ---
    for k in ("DOMENA", "TALLY_URL", "ALERTY_FORM_ACTION", "KONTAKT_FORM_ACTION", "EMAIL", "FIRMA_DANE"):
        if "PODMIEN" in site[k] or "example." in site[k]:
            ostrzez(f"Placeholder do podmiany w dane/site.json: {k} = {site[k]}")
    if przyklad_plik:
        ostrzez("Podstrony urzędów zbudowane z DANYCH PRZYKŁADOWYCH (dane/przyklad-pup.csv, noindex)")

    stron = len(list(out.rglob("*.html")))
    print(f"Zbudowano {stron} stron HTML w {out}")
    print(f"Baza urzędów: {csv_path} (liczba urzędów: {len(pupy)})")
    if OSTRZEZENIA:
        print(f"\nOstrzeżenia ({len(OSTRZEZENIA)}):")
        for o in OSTRZEZENIA:
            print("  - " + o)
    return 0


if __name__ == "__main__":
    sys.exit(main())
