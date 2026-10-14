from types import SimpleNamespace

import pytest

from pup_gen import prompty
from pup_gen.llm import BETA_FALLBACK, DOMYSLNY_MODEL, BladLLM, KlientAtrapa, KlientClaude, klient_domyslny
from pup_gen.przebieg import parsuj_odpowiedz, podstaw

from conftest import mapa


class _Strumien:
    def __init__(self, wiadomosc):
        self.wiadomosc = wiadomosc

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def get_final_message(self):
        return self.wiadomosc


class _AtrapaSDK:
    """Udaje anthropic.Anthropic – zapisuje parametry, nie łączy się z siecią."""

    def __init__(self, stop_reason="end_turn"):
        self.parametry = None
        self.stop_reason = stop_reason
        self.beta = SimpleNamespace(messages=SimpleNamespace(stream=self._stream))

    def _stream(self, **kw):
        self.parametry = kw
        return _Strumien(SimpleNamespace(
            content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text="<tekst>\nA\n</tekst>")],
            stop_reason=self.stop_reason, stop_details=SimpleNamespace(category="cyber"), model=kw["model"],
            usage=SimpleNamespace(input_tokens=10, output_tokens=5, cache_read_input_tokens=7000,
                                  cache_creation_input_tokens=0)))


def _zapytanie(kw, regulamin, fin, pole_id="IV.1"):
    pole = next(p for p in mapa().pola if p.id == pole_id)
    return prompty.zbuduj_zapytanie(kw, pole, fin, regulamin)


def test_klient_claude_parametry(kw, regulamin, fin_szablonu, monkeypatch):
    monkeypatch.delenv("PUP_GEN_MODEL", raising=False)
    sdk = _AtrapaSDK()
    odp = KlientClaude(klient=sdk).generuj(_zapytanie(kw, regulamin, fin_szablonu))
    p = sdk.parametry
    assert p["model"] == DOMYSLNY_MODEL == "claude-opus-5-5"
    assert p["thinking"] == {"type": "adaptive"} and p["output_config"]["effort"] in ("low", "medium", "high", "xhigh", "max")
    assert p["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert p["messages"][0]["content"][0]["cache_control"] == {"type": "ephemeral"}
    assert p["betas"] == [BETA_FALLBACK] and p["fallbacks"] == "default"
    assert "budget_tokens" not in str(p) and "temperature" not in p
    assert odp.tekst_surowy == "<tekst>\nA\n</tekst>" and odp.tokeny["cache_odczyt"] == 7000


def test_klient_claude_skracanie_dopisuje_historie(kw, regulamin, fin_szablonu):
    sdk = _AtrapaSDK()
    klient = KlientClaude(klient=sdk)
    z = _zapytanie(kw, regulamin, fin_szablonu)
    pierwsza = klient.generuj(z)
    klient.generuj(z, prompty.prosba_o_skrocenie(2100, 1900), pierwsza)
    role = [m["role"] for m in sdk.parametry["messages"]]
    assert role == ["user", "assistant", "user"]
    assert sdk.parametry["messages"][1]["content"] is pierwsza.tresc_asystenta


def test_klient_claude_odmowa(kw, regulamin, fin_szablonu):
    with pytest.raises(BladLLM, match="odmówił"):
        KlientClaude(klient=_AtrapaSDK("refusal")).generuj(_zapytanie(kw, regulamin, fin_szablonu))


def test_atrapa_deterministyczna_i_w_limicie(kw, regulamin, fin_szablonu):
    for pole in mapa().pola:
        if not pole.sekcje_tekstowe:
            continue
        z = _zapytanie(kw, regulamin, fin_szablonu, pole.id)
        a, b = KlientAtrapa().generuj(z), KlientAtrapa().generuj(z)
        assert a.tekst_surowy == b.tekst_surowy
        tekst, kontrola = parsuj_odpowiedz(a.tekst_surowy)
        dl = len(podstaw(tekst, fin_szablonu.ark))
        assert 0.8 * z.limit_znakow <= dl <= z.limit_znakow, (pole.id, dl, z.limit_znakow)
        assert "zmienne_arkusza" in kontrola


def test_klient_domyslny_bez_klucza(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    assert isinstance(klient_domyslny(), KlientAtrapa)
    assert isinstance(klient_domyslny(dry_run=True), KlientAtrapa)


# ------------------------------------------------------------------ prawdziwe SDK, transport w pamięci
def _klient_sdk(handler):
    import anthropic
    try:
        import httpx2 as httpx
    except ImportError:  # starsze SDK (0.x) używają httpx
        import httpx
    return anthropic.Anthropic(api_key="sk-test", max_retries=0,
                               http_client=anthropic.DefaultHttpxClient(transport=httpx.MockTransport(handler))), httpx


SSE = "".join(f"event: {e}\ndata: {d}\n\n" for e, d in [
    ("message_start", '{"type":"message_start","message":{"id":"msg_1","type":"message","role":"assistant",'
                      '"model":"claude-opus-5-5","content":[],"stop_reason":null,"stop_sequence":null,'
                      '"usage":{"input_tokens":12,"output_tokens":1,"cache_read_input_tokens":5000,'
                      '"cache_creation_input_tokens":0}}}'),
    ("content_block_start", '{"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}'),
    ("content_block_delta", '{"type":"content_block_delta","index":0,"delta":{"type":"text_delta",'
                            '"text":"<tekst>\\nOd grudnia 2026 r. strzygę w Borkowie.\\n</tekst>"}}'),
    ("content_block_stop", '{"type":"content_block_stop","index":0}'),
    ("message_delta", '{"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null},'
                      '"usage":{"output_tokens":30}}'),
    ("message_stop", '{"type":"message_stop"}'),
])


def test_zapytanie_http_przez_sdk(kw, regulamin, fin_szablonu):
    """Sprawdza prawdziwe żądanie HTTP budowane przez SDK (bez sieci): nagłówek bety, fallback, cache."""
    import json
    zadania = []

    def handler(req):
        zadania.append(req)
        return httpx.Response(200, content=SSE.encode(), headers={"content-type": "text/event-stream"})

    sdk, httpx = _klient_sdk(handler)
    odp = KlientClaude(klient=sdk).generuj(_zapytanie(kw, regulamin, fin_szablonu))
    req = zadania[0]
    body = json.loads(req.content)
    assert req.url.path == "/v1/messages" and req.headers["anthropic-beta"] == BETA_FALLBACK
    assert body["model"] == "claude-opus-5-5" and body["fallbacks"] == "default" and body["stream"] is True
    assert body["thinking"] == {"type": "adaptive"}
    assert body["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert [b.get("cache_control") for b in body["messages"][0]["content"]] == [{"type": "ephemeral"}] * 2 + [None]
    assert parsuj_odpowiedz(odp.tekst_surowy)[0] == "Od grudnia 2026 r. strzygę w Borkowie."
    assert odp.tokeny == {"wejscie": 12, "wyjscie": 30, "cache_odczyt": 5000, "cache_zapis": 0}


def test_blad_400_z_sdk(kw, regulamin, fin_szablonu):
    sdk, httpx = _klient_sdk(lambda req: httpx.Response(
        400, json={"type": "error", "error": {"type": "invalid_request_error", "message": "zle"}}))
    with pytest.raises(BladLLM, match="400"):
        KlientClaude(klient=sdk).generuj(_zapytanie(kw, regulamin, fin_szablonu))
