from __future__ import annotations

import json
import threading
import urllib.request

from unicode_animations import BRAILLE_SPINNER_NAMES
from unicode_animations.web import build_demo_html, build_spinner_payload, create_demo_server


def test_build_spinner_payload_shape() -> None:
    payload = build_spinner_payload()
    assert sorted(payload.keys()) == sorted(BRAILLE_SPINNER_NAMES)

    for name in BRAILLE_SPINNER_NAMES:
        entry = payload[name]
        assert isinstance(entry["frames"], list)
        assert len(entry["frames"]) > 0
        assert isinstance(entry["interval"], int)
        assert entry["interval"] > 0


def test_build_demo_html_contains_expected_markers() -> None:
    html = build_demo_html()
    assert "unicode-animations" in html
    assert "spinnerPanel" in html
    assert "fetch('/spinners.json')" in html


def test_demo_server_serves_index_and_spinner_json() -> None:
    server = create_demo_server(port=0)
    host, port = server.server_address
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        with urllib.request.urlopen(f"http://{host}:{port}/", timeout=5) as response:
            html_body = response.read().decode("utf-8")
            assert response.status == 200
            assert "unicode-animations" in html_body

        with urllib.request.urlopen(f"http://{host}:{port}/spinners.json", timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
            assert response.status == 200
            assert sorted(payload.keys()) == sorted(BRAILLE_SPINNER_NAMES)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
