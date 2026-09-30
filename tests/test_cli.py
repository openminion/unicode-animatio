from __future__ import annotations

import json

import pytest

from unicode_animations import (
    CATEGORY_NAMES,
    SPINNER_NAMES,
    __version__,
    cli,
    spinner_names_for_category,
)


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


def test_main_prints_version(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--version"])

    assert exc_info.value.code == 0
    assert capsys.readouterr().out == f"unicode-animatio {__version__}\n"


def test_main_filters_list_by_category(capsys) -> None:
    assert cli.main(["--list", "--category", "graph"]) == 0

    captured = capsys.readouterr()
    graph_names = spinner_names_for_category("graph")
    assert f"{len(graph_names)} graph spinners available:" in captured.out
    for name in graph_names:
        assert name in captured.out
    assert "terminalblink" not in captured.out


def test_main_searches_by_name_category_and_tags(capsys) -> None:
    assert cli.main(["--search", "knowledge", "--category", "graph"]) == 0

    captured = capsys.readouterr()
    assert '4 graph spinners matching "knowledge" available:' in captured.out
    assert "edgepulse" in captured.out
    assert "terminalblink" not in captured.out

    assert cli.main(["--search", "edgepulse", "--category", "graph"]) == 0
    assert '1 graph spinner matching "edgepulse" available:' in capsys.readouterr().out


def test_main_show_prints_spinner_metadata(capsys) -> None:
    assert cli.main(["--show", "edgepulse"]) == 0

    captured = capsys.readouterr()
    assert "edgepulse" in captured.out
    assert "category: graph" in captured.out
    assert "tags: nodes, edges, knowledge" in captured.out
    assert "python: provider.get('edgepulse')" in captured.out


def test_main_prints_json_for_scripted_catalog_use(capsys) -> None:
    assert cli.main(["--list", "--category", "graph", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert [entry["name"] for entry in payload] == list(spinner_names_for_category("graph"))
    assert payload[0]["category"] == "graph"
    assert payload[0]["tags"] == ["nodes", "edges", "knowledge"]


def test_main_show_json_includes_frames(capsys) -> None:
    assert cli.main(["--show", "edgepulse", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["name"] == "edgepulse"
    assert payload["category"] == "graph"
    assert payload["frames"]


def test_main_rejects_json_without_inspection_mode(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--json"])

    assert exc_info.value.code == 2
    assert "--json requires --list, --categories, --search, or --show" in capsys.readouterr().err


def test_main_rejects_search_with_positional_name(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["edgepulse", "--search", "edge"])

    assert exc_info.value.code == 2
    assert "--search cannot be combined with a spinner name" in capsys.readouterr().err


@pytest.mark.parametrize(
    "args",
    (
        ["--show", "edgepulse", "--search", "graph"],
        ["--categories", "--search", "graph"],
        ["--web", "--search", "graph"],
    ),
)
def test_main_rejects_search_with_other_modes(args, capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(args)

    assert exc_info.value.code == 2
    assert "--search cannot be combined with" in capsys.readouterr().err


def test_main_rejects_unknown_category(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--list", "--category", "unknown"])

    assert exc_info.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_main_requires_list_for_category(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--category", "graph"])

    assert exc_info.value.code == 2
    assert "--category requires --list or --search" in capsys.readouterr().err


def test_main_rejects_unknown_spinner_name(capsys) -> None:
    assert cli.main(["unknown-spinner"]) == 1

    captured = capsys.readouterr()
    assert 'Unknown spinner: "unknown-spinner"' in captured.err
    assert "Run with --list to see all spinners." in captured.err


def test_main_shows_named_spinner_when_stdout_is_not_a_tty(capsys) -> None:
    assert cli.main(["edgepulse"]) == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("edgepulse\n")
    assert f"{len(SPINNER_NAMES)} spinners available" not in captured.out


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
    calls: list[tuple[str, int, bool]] = []

    def fake_serve_demo(*, host: str, port: int, open_browser: bool) -> int:
        calls.append((host, port, open_browser))
        return 17

    monkeypatch.setattr(cli, "serve_demo", fake_serve_demo)

    assert cli.main(["--web"]) == 17
    assert cli.main(["--web", "--host", "0.0.0.0", "--port", "8765", "--no-open"]) == 17
    assert calls == [
        ("127.0.0.1", 0, True),
        ("0.0.0.0", 8765, False),
    ]


def test_main_rejects_web_options_without_web(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--host", "0.0.0.0", "--port", "8765", "--no-open"])

    assert exc_info.value.code == 2
    assert "--host, --port, and --no-open require --web" in capsys.readouterr().err
