from __future__ import annotations

import json
import threading
import urllib.request

import pytest

from unicode_animations import CATEGORY_NAMES, SPINNER_CATEGORIES, SPINNER_NAMES, __version__, web
from unicode_animations.web import build_demo_html, build_spinner_payload, create_demo_server, main


def test_build_spinner_payload_shape() -> None:
    payload = build_spinner_payload()
    assert tuple(payload) == SPINNER_NAMES

    for name in SPINNER_NAMES:
        entry = payload[name]
        assert isinstance(entry["frames"], list)
        assert len(entry["frames"]) > 0
        assert isinstance(entry["interval"], int)
        assert entry["interval"] > 0
        assert entry["interval_ms"] == entry["interval"]
        assert entry["category"] == SPINNER_CATEGORIES[name]
        assert entry["tags"]
        assert entry["frame_count"] == len(entry["frames"])
        assert entry["frame_width"] >= 1
        assert entry["preview_frame"] == entry["frames"][0]
        assert entry["motion"] in {"low", "medium", "high"}
        assert entry["description"]


def test_build_demo_html_contains_expected_markers() -> None:
    html = build_demo_html()
    assert "unicode-animatio" in html
    assert f"{len(SPINNER_NAMES)} deterministic Unicode" in html
    assert "18 braille spinner animations" not in html
    assert "spinnerGallery" in html
    assert "Reduced motion" in html
    assert "Copy snippet" in html
    assert "fetch('/spinners.json')" in html
    assert f"const categoryNames = {json.dumps(CATEGORY_NAMES)};" in html
    assert "const categories = ['all', ...categoryNames];" in html

    details_start = html.index('<aside class="details"')
    details_end = html.index("</aside>", details_start)
    assert details_start < html.index('id="copyCurrent"') < details_end


def test_build_demo_html_honors_and_persists_display_preferences() -> None:
    html = build_demo_html()

    assert "(prefers-color-scheme: light)" in html
    assert "(prefers-reduced-motion: reduce)" in html
    assert "unicode-animatio:theme" in html
    assert "unicode-animatio:motion" in html
    assert "window.localStorage.getItem" in html
    assert "window.localStorage.setItem" in html
    assert "setReducedMotion(savedMotion ? savedMotion === 'reduce' : systemMotion)" in html


def test_build_demo_html_exposes_keyboard_selection_and_live_status() -> None:
    html = build_demo_html()

    assert 'role="listbox"' in html
    assert "card.setAttribute('role', 'option')" in html
    assert "card.tabIndex = name === selectedName ? 0 : -1" in html
    assert "ArrowLeft" in html
    assert "ArrowRight" in html
    assert "event.key === 'Home'" in html
    assert "event.key === 'End'" in html
    assert 'aria-hidden="true"' in html
    assert 'id="copyStatus"' in html
    assert 'id="resultsStatus"' in html
    assert 'aria-describedby="resultsStatus"' in html
    assert 'id="emptyState"' in html
    assert 'aria-label="Search animations"' in html
    assert "resultsStatus.textContent" in html
    assert "const query = searchInput.value.trim();" in html
    assert "const normalizedQuery = query.toLowerCase();" in html
    assert "matching “${query}”" in html
    assert "emptyState.textContent = visible.length > 0 ? '' : 'No matching animations.'" in html
    assert html.count('role="status"') == 2
    assert html.count('aria-live="polite"') == 1


def test_main_prints_version(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])

    assert exc_info.value.code == 0
    assert capsys.readouterr().out == f"unicode-animatio-web {__version__}\n"


@pytest.mark.parametrize("port", ("-1", "65536", "nope"))
def test_main_rejects_out_of_range_port(port, capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--port", port, "--no-open"])

    assert exc_info.value.code == 2
    assert "port must be an integer between 0 and 65535" in capsys.readouterr().err


def test_main_accepts_port_bounds(monkeypatch) -> None:
    calls: list[int] = []

    def fake_serve_demo(*, host: str, port: int, open_browser: bool) -> int:
        calls.append(port)
        return 0

    monkeypatch.setattr(web, "serve_demo", fake_serve_demo)

    assert main(["--port", "0", "--no-open"]) == 0
    assert main(["--port", "65535", "--no-open"]) == 0
    assert calls == [0, 65535]


def test_demo_server_serves_index_and_spinner_json() -> None:
    server = create_demo_server(port=0)
    host, port = server.server_address
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        with urllib.request.urlopen(f"http://{host}:{port}/", timeout=5) as response:
            html_body = response.read().decode("utf-8")
            assert response.status == 200
            assert "unicode-animatio" in html_body

        with urllib.request.urlopen(f"http://{host}:{port}/spinners.json", timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
            assert response.status == 200
            assert tuple(payload) == SPINNER_NAMES
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
