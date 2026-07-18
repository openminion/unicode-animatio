from __future__ import annotations

import pytest

from unicode_animations import CATEGORY_NAMES, SPINNER_NAMES, cli, spinner_names_for_category


def test_main_list_prints_all_spinner_names(capsys) -> None:
    assert cli.main(["--list"]) == 0

    captured = capsys.readouterr()
    assert f"{len(SPINNER_NAMES)} spinners available:" in captured.out
    for name in SPINNER_NAMES:
        assert name in captured.out


def test_main_lists_categories_with_counts(capsys) -> None:
    assert cli.main(["--categories"]) == 0

    captured = capsys.readouterr()
    assert f"{len(CATEGORY_NAMES)} categories available:" in captured.out
    for category in CATEGORY_NAMES:
        count = len(spinner_names_for_category(category))
        assert f"{category} ({count} spinners)" in captured.out


def test_main_filters_list_by_category(capsys) -> None:
    assert cli.main(["--list", "--category", "graph"]) == 0

    captured = capsys.readouterr()
    graph_names = spinner_names_for_category("graph")
    assert f"{len(graph_names)} graph spinners available:" in captured.out
    for name in graph_names:
        assert name in captured.out
    assert "terminalblink" not in captured.out


def test_main_rejects_unknown_category(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--list", "--category", "unknown"])

    assert exc_info.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_main_requires_list_for_category(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--category", "graph"])

    assert exc_info.value.code == 2
    assert "--category requires --list" in capsys.readouterr().err


def test_main_rejects_unknown_spinner_name(capsys) -> None:
    assert cli.main(["unknown-spinner"]) == 1

    captured = capsys.readouterr()
    assert 'Unknown spinner: "unknown-spinner"' in captured.err
    assert "Run with --list to see all spinners." in captured.err


def test_main_rejects_invalid_color_mode(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--color", "sometimes"])

    assert exc_info.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_preview_style_honors_non_tty_auto_and_no_color() -> None:
    assert not cli._resolve_preview_style(  # noqa: SLF001 - CLI helper contract.
        color="auto",
        foreground="magenta",
        is_tty=False,
        no_color=False,
    ).color_enabled
    assert not cli._resolve_preview_style(  # noqa: SLF001 - CLI helper contract.
        color="always",
        foreground="magenta",
        is_tty=True,
        no_color=True,
    ).color_enabled


def test_preview_style_supports_explicit_foreground_color() -> None:
    style = cli._resolve_preview_style(  # noqa: SLF001 - CLI helper contract.
        color="always",
        foreground="gray",
        is_tty=False,
        no_color=False,
    )

    assert style.color_enabled
    assert style.frame_style == cli.GRAY


def test_preview_line_keeps_raw_frame_unchanged() -> None:
    style = cli._resolve_preview_style(  # noqa: SLF001 - CLI helper contract.
        color="always",
        foreground="cyan",
        is_tty=True,
        no_color=False,
    )
    line = cli._render_preview_line(  # noqa: SLF001 - CLI helper contract.
        frame="⠋",
        spinner_name="braille",
        interval=80,
        count=f"[1/{len(SPINNER_NAMES)}]",
        style=style,
    )

    assert "⠋" in line
    assert "\x1b[36m⠋\x1b[0m" in line
    assert cli.spinners["braille"].frames[0] == "⠋"


def test_main_web_mode_delegates_to_server(monkeypatch) -> None:
    calls: list[tuple[int, bool]] = []

    def fake_serve_demo(*, port: int, open_browser: bool) -> int:
        calls.append((port, open_browser))
        return 17

    monkeypatch.setattr(cli, "serve_demo", fake_serve_demo)

    assert cli.main(["--web", "--port", "8765"]) == 17
    assert calls == [(8765, True)]
