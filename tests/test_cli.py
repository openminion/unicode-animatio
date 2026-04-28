from __future__ import annotations

from unicode_animations import BRAILLE_SPINNER_NAMES, cli


def test_main_list_prints_all_spinner_names(capsys) -> None:
    assert cli.main(["--list"]) == 0

    captured = capsys.readouterr()
    assert "18 spinners available:" in captured.out
    for name in BRAILLE_SPINNER_NAMES:
        assert name in captured.out


def test_main_rejects_unknown_spinner_name(capsys) -> None:
    assert cli.main(["unknown-spinner"]) == 1

    captured = capsys.readouterr()
    assert 'Unknown spinner: "unknown-spinner"' in captured.err
    assert "Run with --list to see all spinners." in captured.err


def test_main_web_mode_delegates_to_server(monkeypatch) -> None:
    calls: list[tuple[int, bool]] = []

    def fake_serve_demo(*, port: int, open_browser: bool) -> int:
        calls.append((port, open_browser))
        return 17

    monkeypatch.setattr(cli, "serve_demo", fake_serve_demo)

    assert cli.main(["--web", "--port", "8765"]) == 17
    assert calls == [(8765, True)]
