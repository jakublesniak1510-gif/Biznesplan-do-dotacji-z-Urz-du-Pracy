"""Szacunek tokenów i kosztu API na jeden plan.

Cennik: skill `claude-api` (stan cennika z 2026-10-06), USD za 1 mln tokenów. Zapis do cache (TTL 5 min)
kosztuje 1,25× ceny wejścia, odczyt z cache – cenę z kolumny `cache_odczyt`.
Bez klucza API tokeny wejścia szacujemy z liczby znaków; z kluczem – liczymy dokładnie (count_tokens).
"""

from __future__ import annotations

from dataclasses import dataclass

from .llm import KlientClaude, ZapytanieLLM

CENNIK_USD_ZA_MTOK = {
    "claude-opus-5-5": {"wejscie": 4.00, "wyjscie": 20.00, "cache_odczyt": 0.20},
    "claude-sonnet-5-5": {"wejscie": 2.00, "wyjscie": 10.00, "cache_odczyt": 0.20},
    "claude-haiku-5-5": {"wejscie": 0.10, "wyjscie": 0.50, "cache_odczyt": 0.01},
}
MNOZNIK_ZAPISU_CACHE = 1.25
ZNAKI_NA_TOKEN = 2.5        # ostrożnie dla polskiego tekstu i JSON-a z polskimi znakami (tokenizer Opus 4.7+)
TOKENY_KONTROLI = 300       # blok <kontrola> w odpowiedzi
UDZIAL_SKROCEN = 0.15       # ok. 15% pól wymaga jednej prośby o skrócenie


@dataclass
class SzacunekPola:
    pole_id: str
    system: int
    dane_klienta: int
    szablony: int
    polecenie: int
    wyjscie_widoczne: int


@dataclass
class Szacunek:
    model: str
    pola: list[SzacunekPola]
    mnoznik_myslenia: float
    usd: float
    usd_bez_cache: float
    tokeny_wejscia: int
    tokeny_wyjscia: int
    dokladne: bool

    def tabela(self, kurs_pln: float) -> str:
        lin = [f"Model: {self.model} · tokeny wejścia {'policzone (count_tokens)' if self.dokladne else 'oszacowane z liczby znaków'}",
               f"Pola tekstowe: {len(self.pola)} · myślenie (adaptive): ×{self.mnoznik_myslenia} tokenów widocznej odpowiedzi",
               "",
               f"{'pole':<8}{'system':>8}{'klient':>8}{'szablon':>9}{'param.':>8}{'wyjście':>9}"]
        for p in self.pola:
            lin.append(f"{p.pole_id:<8}{p.system:>8}{p.dane_klienta:>8}{p.szablony:>9}{p.polecenie:>8}{p.wyjscie_widoczne:>9}")
        lin += ["",
                f"Tokeny wejścia (łącznie, przed cache): {self.tokeny_wejscia:_}".replace("_", " "),
                f"Tokeny wyjścia (z myśleniem i skróceniami): {self.tokeny_wyjscia:_}".replace("_", " "),
                f"Koszt na plan z prompt caching: {self.usd:.2f} USD ≈ {self.usd * kurs_pln:.2f} zł",
                f"Koszt na plan bez cache:        {self.usd_bez_cache:.2f} USD ≈ {self.usd_bez_cache * kurs_pln:.2f} zł",
                f"(kurs przyjęty do przeliczenia: {kurs_pln} zł/USD)"]
        return "\n".join(lin)


def _tokeny(tekst: str) -> int:
    return int(len(tekst) / ZNAKI_NA_TOKEN) + 1


def szacuj(zapytania: list[ZapytanieLLM], model: str, mnoznik_myslenia: float = 1.0,
           klient: KlientClaude | None = None) -> Szacunek:
    ceny = CENNIK_USD_ZA_MTOK[model]
    c_in, c_out, c_read = ceny["wejscie"] / 1e6, ceny["wyjscie"] / 1e6, ceny["cache_odczyt"] / 1e6
    c_write = c_in * MNOZNIK_ZAPISU_CACHE
    pola: list[SzacunekPola] = []
    usd = usd_bez = 0.0
    wej = wyj = 0
    widziane_szablony: set[str] = set()
    for i, z in enumerate(zapytania):
        s, d, t, p = (_tokeny(x) for x in (z.system, z.dane_klienta, z.szablony, z.polecenie))
        if klient is not None:  # dokładnie: całość z count_tokens, proporcje bloków z liczby znaków
            razem = klient.policz_tokeny(z)
            skala = razem / (s + d + t + p)
            s, d, t, p = (int(x * skala) for x in (s, d, t, p))
        out = int(z.limit_znakow * 0.95 / ZNAKI_NA_TOKEN) + TOKENY_KONTROLI
        out_calk = int(out * (1 + mnoznik_myslenia) * (1 + UDZIAL_SKROCEN))
        pola.append(SzacunekPola(z.pole_id, s, d, t, p, out))
        # wejście: system + dane klienta zapisane przy 1. polu, potem czytane; szablon – zapis przy 1. użyciu
        koszt_wej = (s + d) * (c_write if i == 0 else c_read)
        koszt_wej += t * (c_read if z.szablony in widziane_szablony else c_write) + p * c_in
        widziane_szablony.add(z.szablony)
        koszt_wej += UDZIAL_SKROCEN * ((s + d + t) * c_read + (p + out) * c_in)  # tura skracania
        usd += koszt_wej + out_calk * c_out
        usd_bez += (s + d + t + p) * c_in * (1 + UDZIAL_SKROCEN) + out_calk * c_out
        wej += s + d + t + p
        wyj += out_calk
    return Szacunek(model, pola, mnoznik_myslenia, round(usd, 4), round(usd_bez, 4), wej, wyj, klient is not None)
