import datetime as dt

from pup_gen.schemat import WynikGeneracji, WynikPola


def wynik(fin, teksty: dict[str, tuple[str, int | None]], id_zlecenia="test-1", pup_id="zielonow",
          ton="ciepły", data: dt.datetime | None = None) -> WynikGeneracji:
    pola = [WynikPola(id=i, nazwa_w_formularzu=f"Pole {i}", sekcje=["01"], limit_znakow=limit, tekst=t,
                      tekst_ze_zmiennymi=t, liczba_znakow=len(t)) for i, (t, limit) in teksty.items()]
    return WynikGeneracji(id_zlecenia=id_zlecenia, imie="Anna", miejscowosc="Borków",
                          pup="Powiatowy Urząd Pracy w Zielonowie", pup_id=pup_id, formularz="wzór testowy",
                          ton=ton, data=data or dt.datetime(2026, 10, 14, 12, 0), model="test", tryb="dry-run",
                          pola=pola, ark=fin.ark, ark_wartosci=dict(fin.wartosci))
