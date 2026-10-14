#!/usr/bin/env python3
"""Kontrola przykładowego wniosku: długość sekcji, zakazane zwroty, liczby spoza arkusza.

Użycie:
  python3 przyklady/narzedzia/sprawdz.py przyklady/01-fryzjerka-mobilna-turek

Sprawdza:
  1. wniosek.md – liczbę znaków (ze spacjami) w każdej sekcji 01–09 (cel wariantu standard: 1700–2300),
  2. wniosek.md i wniosek.docx – zwroty z narzedzia/zakazane.txt,
  3. kwoty i procenty w sekcjach 01–09 – czy występują w model.xlsx (wartości przeliczone)
     albo na liście dozwolonych liczb z kwestionariusza (narzedzia/dozwolone/<katalog-przykładu>.txt).
Kod wyjścia 0 = brak zakazanych zwrotów i brak nieznanych liczb.
"""
import re, sys, os, glob
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))

def load_rules():
    rules = []
    for line in open(os.path.join(HERE, "zakazane.txt"), encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#"):
            rules.append((line, re.compile(line, re.I)))
    return rules

def sections(md):
    """Zwraca {nr: tekst} dla nagłówków '## 0X.' – bez linii z opisem pola (kursywa) i bez podsekcji '### Tabela'."""
    out, cur, skip = {}, None, False
    for line in md.splitlines():
        m = re.match(r"^## (0[1-9])\.", line)
        if m:
            cur, skip = m.group(1), False
            out[cur] = []
            continue
        if line.startswith("## ") or line.startswith("---"):
            cur = None
            continue
        if cur is None:
            continue
        if line.startswith("### Tabela"):
            skip = True
            continue
        if line.startswith("### "):
            skip = False
            continue
        if skip or line.startswith("*Pol"):
            continue
        out[cur].append(line)
    res = {}
    for k, lines in out.items():
        txt = "\n".join(lines).strip()
        txt = re.sub(r"\*\*(.+?)\*\*", r"\1", txt)  # pogrubienia markdown nie liczą się do znaków
        res[k] = txt
    return res

def fmt_variants(x):
    """Zapis polski liczby: 1 234,56 / 1 234 / 12% / 12,5%."""
    v = set()
    if x is None or isinstance(x, str):
        return v
    for dec in (0, 2):
        r = round(x + 1e-9, dec)
        s = f"{r:,.{dec}f}".replace(",", " ").replace(".", ",")
        v.add(s)
        v.add(s.replace(" ", ""))
    return v

def model_numbers(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    nums = set()
    for ws in wb:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, (int, float)) and not isinstance(c.value, bool):
                    nums |= fmt_variants(c.value)
                    if abs(c.value) < 1.5:  # udziały -> procenty
                        for dec in (0, 1):
                            p = round(c.value * 100, dec)
                            nums.add((f"{p:.{dec}f}").replace(".", ",") + "%")
    # średnie miesięczne z rocznych (Tabela 4 w formularzach "miesięcznie")
    dw = wb["Do-wniosku"]
    for r in range(7, 23):
        val = dw.cell(r, 15).value
        if isinstance(val, (int, float)):
            nums |= fmt_variants(val / 12)
    return nums

def numbers_in(text):
    pat = re.compile(r"(\d{1,3}(?: \d{3})+(?:,\d+)?|\d+(?:,\d+)?)\s?(zł|%)")
    return [(m.group(1) + ("%" if m.group(2) == "%" else ""), m.start()) for m in pat.finditer(text)]

def docx_text(path):
    try:
        import docx
    except ImportError:
        return ""
    d = docx.Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            parts.append(" | ".join(c.text for c in r.cells))
    return "\n".join(parts)

def main(folder):
    rules = load_rules()
    md = open(os.path.join(folder, "wniosek.md"), encoding="utf-8").read()
    secs = sections(md)
    ok = True
    print(f"== {folder}")
    print("1) Długość sekcji (znaki ze spacjami, cel 1700–2300):")
    for k in sorted(secs):
        n = len(secs[k])
        flag = "OK" if 1700 <= n <= 2300 else "UWAGA"
        print(f"   sekcja {k}: {n:5d}  {flag}")
    print("2) Zakazane zwroty:")
    hits = 0
    # pomijamy cytaty nazw pól urzędu (linie "*Pole…") i tabelę mapowania – to język formularza, nie wnioskodawcy
    md_lines, in_map = [], False
    for l in md.splitlines():
        if l.startswith("## Mapa"):
            in_map = True
        elif l.startswith("## ") or l.startswith("---"):
            in_map = False
        if not in_map and not l.startswith("*Pol"):
            md_lines.append(l)
    texts = {"wniosek.md": "\n".join(md_lines)}
    dx = os.path.join(folder, "wniosek.docx")
    if os.path.exists(dx):
        texts["wniosek.docx"] = docx_text(dx)
    for name, txt in texts.items():
        for raw, rx in rules:
            for m in rx.finditer(txt):
                ctx = txt[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
                print(f"   [{name}] '{raw}': …{ctx}…")
                hits += 1
    print(f"   razem trafień: {hits}")
    ok &= hits == 0
    print("3) Kwoty i procenty spoza arkusza i listy dozwolonych:")
    allowed = model_numbers(os.path.join(folder, "model.xlsx"))
    extra = os.path.join(HERE, "dozwolone", os.path.basename(os.path.normpath(folder)) + ".txt")
    if os.path.exists(extra):
        for line in open(extra, encoding="utf-8"):
            line = line.split("#")[0].strip().replace(" zł", "")
            if line:
                allowed.add(line)
    unknown = 0
    for k, txt in sorted(secs.items()):
        for num, pos in numbers_in(txt):
            if num not in allowed and num.replace(" ", "") not in allowed:
                ctx = txt[max(0, pos - 50): pos + 20].replace("\n", " ")
                print(f"   sekcja {k}: {num}  …{ctx}…")
                unknown += 1
    print(f"   nieznanych liczb: {unknown}")
    ok &= unknown == 0
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
