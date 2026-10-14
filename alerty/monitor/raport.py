"""Raport skanu w Markdown: co znaleziono, aktywne nabory dziś, błędy źródeł."""

from __future__ import annotations

from collections import Counter
from datetime import date

from monitor.alert import do_alertu, grupuj_po_wojewodztwie, link_ogloszenia, nazwa_urzedu, opis_dat
from monitor.klasyfikator import opis_terminu, rozbij_tytul_zl, status
from monitor.stan import Stan


def raport_markdown(stan: Stan, dzis: date, rok: int = 2026) -> str:
    info = stan.dane.get("ostatni_skan_info", {})
    st = info.get("statystyki", {})
    bledy = info.get("bledy", {})
    nabory = [w for w in stan.nabory() if (w.data_publikacji or "")[:4] == str(rok)]
    aktywne = do_alertu(nabory, dzis)
    statusy = Counter(status(w, dzis) or "zakończenie/wyniki" for w in nabory)

    linie = [
        f"# Raport skanu naborów PUP – {dzis.strftime('%d.%m.%Y')}",
        "",
        f"Ostatni skan: {stan.dane.get('ostatni_skan', '–')}. Plik danych: `dane/nabory-{rok}.json`.",
        "",
        "## Podsumowanie",
        "",
        f"- **Aktywne nabory dziś (trwają, zapowiedziane albo do weryfikacji): {len(aktywne)}**",
        f"- Wszystkie wykryte wpisy o naborach na działalność w {rok} r. (w stanie monitora): {len(nabory)}",
        "- Statusy: " + ", ".join(f"{kk}: {v}" for kk, v in statusy.most_common()),
        f"- Zielona Linia: {st.get('zielonalinia_wpisy', '–')} wpisów z kategorii „Informacje z regionów” od {st.get('zielonalinia_od', '–')}",
        f"- Strony PUP: sprawdzono {st.get('pup_sprawdzone', 0)}, poprawnie {st.get('pup_ok', 0)}, "
        f"wpisów na listach {st.get('pup_wpisy', 0)}; dociągnięte ogłoszenia: {st.get('szczegoly_pobrane', 0)}"
        f"/{st.get('szczegoly_kandydaci', 0)}",
        f"- Nowe wpisy w tym skanie: {st.get('nowe', 0)}, w tym do alertu: {st.get('nowe_do_alertu', 0)}",
        f"- Zapytania HTTP: {st.get('http', {}).get('zapytania', '–')}, błędy: {st.get('http', {}).get('bledy', '–')}, "
        f"zablokowane przez robots.txt: {st.get('http', {}).get('zablokowane_robots', '–')}",
        "",
        "## Aktywne nabory dziś",
        "",
    ]
    if not aktywne:
        linie.append("Brak aktywnych naborów w monitorowanych źródłach.")
    for woj, lista in grupuj_po_wojewodztwie(aktywne).items():
        linie += [f"### {woj} ({len(lista)})", "", "| Urząd | Ogłoszenie | Termin | Ile zostało | Kwota | Źródło | Status | Opublikowano |",
                  "|---|---|---|---|---|---|---|---|"]
        for w in lista:
            tytul = rozbij_tytul_zl(w.tytul)[1].replace("|", "/")
            linie.append(
                f"| {nazwa_urzedu(w)} | [{tytul[:90]}]({link_ogloszenia(w)}) | {opis_dat(w)} | {opis_terminu(w, dzis)} "
                f"| {w.kwota_opis or '–'} | {', '.join(w.zrodla_finansowania) or '–'} | {status(w, dzis)} "
                f"| {w.data_publikacji} ({', '.join(w.zrodla)}) |"
            )
        linie.append("")
    uwagi = stan.dane.get("uwagi_skanu") or []
    if uwagi:
        linie += ["## Uwagi", ""] + [f"- {u}" for u in uwagi] + [""]
    if bledy:
        linie += ["## Błędy i blokady źródeł", "", "| Źródło | Błąd |", "|---|---|"]
        linie += [f"| {kk} | {v} |" for kk, v in sorted(bledy.items())]
        linie.append("")
    kat = st.get("kategorie", {})
    if kat:
        linie += ["## Klasyfikacja wpisów z tego skanu", "", "| Kategoria | Liczba |", "|---|---|"]
        linie += [f"| {kk} | {v} |" for kk, v in sorted(kat.items(), key=lambda x: -x[1])]
        linie.append("")
    return "\n".join(linie) + "\n"
