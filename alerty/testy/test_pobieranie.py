"""Uprzejme pobieranie bez sieci: robots.txt, Crawl-delay, ETag/Last-Modified, skrót treści."""

from monitor.pobieranie import Klient, grupa_hosta


class FakeOdp:
    def __init__(self, status=200, tekst="", naglowki=None):
        self.status_code = status
        self.text = tekst
        self.headers = {"Content-Type": "text/plain" if tekst.startswith("User") else "text/html; charset=UTF-8"}
        self.headers.update(naglowki or {})
        self.encoding = "utf-8"


class FakeSesja:
    def __init__(self, odpowiedzi):
        self.odpowiedzi = odpowiedzi  # url -> FakeOdp lub funkcja(headers) -> FakeOdp
        self.headers = {}
        self.wywolania = []

    def get(self, url, headers=None, timeout=None):
        self.wywolania.append((url, dict(headers or {})))
        o = self.odpowiedzi.get(url, FakeOdp(404, "nie ma"))
        return o(headers or {}) if callable(o) else o


def test_robots_blokuje(fixture_tekst, tmp_path):
    sesja = FakeSesja({
        "https://zielonalinia.gov.pl/robots.txt": FakeOdp(200, fixture_tekst("robots-zielonalinia.txt")),
        "https://zielonalinia.gov.pl/wp-json/wp/v2/posts": FakeOdp(200, "[]"),
    })
    k = Klient(sesja=sesja, odstep_s=0, katalog_cache=tmp_path)
    assert not k.dozwolone("https://zielonalinia.gov.pl/wp-admin/admin-ajax.php")
    assert k.dozwolone("https://zielonalinia.gov.pl/wp-json/wp/v2/posts")
    assert k.opoznienie_dla("https://zielonalinia.gov.pl/wp-json/wp/v2/posts") == 30.0  # Crawl-delay: 30
    odp = k.pobierz("https://zielonalinia.gov.pl/wp-admin/x")
    assert odp.blad == "zablokowane przez robots.txt"


def test_robots_praca_gov_pl(fixture_tekst, tmp_path):
    sesja = FakeSesja({"https://tuchola.praca.gov.pl/robots.txt": FakeOdp(200, fixture_tekst("robots-praca-gov-pl.txt"))})
    k = Klient(sesja=sesja, odstep_s=0, katalog_cache=tmp_path)
    assert k.dozwolone("https://tuchola.praca.gov.pl/rynek-pracy/aktualnosci")
    assert k.opoznienie_dla("https://tuchola.praca.gov.pl/rynek-pracy/aktualnosci") == 0
    assert grupa_hosta("tuchola.praca.gov.pl") == grupa_hosta("legnica.praca.gov.pl") == "praca.gov.pl"


def test_etag_i_skrot(tmp_path):
    url = "https://example.org/strona"

    def strona(headers):
        if headers.get("If-None-Match") == '"v1"':
            return FakeOdp(304, "")
        return FakeOdp(200, "<html>treść</html>", {"ETag": '"v1"'})

    sesja = FakeSesja({"https://example.org/robots.txt": FakeOdp(404, ""), url: strona})
    k = Klient(sesja=sesja, odstep_s=0, katalog_cache=tmp_path)
    pierwsza = k.pobierz(url)
    assert pierwsza.status == 200 and pierwsza.tekst == "<html>treść</html>" and not pierwsza.niezmieniona
    k.zapisz_cache()
    # nowy klient czyta cache z dysku i wysyła If-None-Match
    k2 = Klient(sesja=sesja, odstep_s=0, katalog_cache=tmp_path)
    druga = k2.pobierz(url)
    assert druga.status == 304 and druga.niezmieniona
    assert sesja.wywolania[-1][1]["If-None-Match"] == '"v1"'
    # robots.txt zapamiętany: drugi klient nie pobiera go ponownie
    assert sum(1 for u, _ in sesja.wywolania if u.endswith("robots.txt")) == 1


def test_user_agent_z_kontaktem(tmp_path):
    k = Klient(sesja=FakeSesja({}), katalog_cache=tmp_path)
    ua = k.sesja.headers["User-Agent"]
    assert ua.startswith("AlertyNaborowPUP/") and "kontakt:" in ua
