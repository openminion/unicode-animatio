"""Terminal demo CLI for unicode_animations."""

from __future__ import annotations

import argparse
import os
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass

from .catalog import (
    CATEGORY_NAMES,
    SPINNER_CATEGORIES,
    SPINNER_NAMES,
    spinner_names_for_category,
    spinners,
)
from .web import serve_demo

HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"
MAGENTA = "\x1b[35m"
GRAY = "\x1b[90m"
CYAN = "\x1b[36m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
BLUE = "\x1b[34m"
WHITE = "\x1b[37m"
RESET = "\x1b[0m"
CLEAR_LINE = "\r\x1b[2K"

COLOR_STYLES = {
    "magenta": MAGENTA,
    "gray": GRAY,
    "cyan": CYAN,
    "green": GREEN,
    "yellow": YELLOW,
    "blue": BLUE,
    "white": WHITE,
}


@dataclass(frozen=True)
class PreviewStyle:
    color_enabled: bool
    frame_style: str
    text_style: str
    detail_style: str


def _resolve_preview_style(
    *,
    color: str,
    foreground: str,
    is_tty: bool,
    no_color: bool | None = None,
) -> PreviewStyle:
    no_color_active = bool(os.environ.get("NO_COLOR")) if no_color is None else no_color
    color_enabled = color == "always" or (color == "auto" and is_tty)
    if color == "never" or no_color_active:
        color_enabled = False
    if not color_enabled:
        return PreviewStyle(
            color_enabled=False,
            frame_style="",
            text_style="",
            detail_style="",
        )
    return PreviewStyle(
        color_enabled=True,
        frame_style=COLOR_STYLES[foreground],
        text_style=BOLD,
        detail_style=DIM,
    )


def _styled(text: str, code: str) -> str:
    return f"{code}{text}{RESET}" if code else text


def _render_preview_line(
    *,
    frame: str,
    spinner_name: str,
    interval: int,
    count: str,
    style: PreviewStyle,
) -> str:
    return (
        f"{CLEAR_LINE}  {_styled(frame, style.frame_style)}  "
        f"{_styled(spinner_name, style.text_style)} "
        f"{_styled(f'{interval}ms', style.detail_style)}  "
        f"{_styled(count, style.detail_style)}"
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="unicode-animatio",
        description="Preview Unicode and ASCII terminal animations.",
    )
    parser.add_argument("name", nargs="?", help="Spinner name to preview")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-l", "--list", action="store_true", help="List available spinners")
    mode.add_argument("--categories", action="store_true", help="List spinner categories")
    mode.add_argument("-w", "--web", action="store_true", help="Open browser demo")
    parser.add_argument("--category", choices=CATEGORY_NAMES, help="Filter --list by category")
    parser.add_argument("--port", type=int, default=0, help="Port for --web mode (default: auto)")
    parser.add_argument(
        "--color",
        choices=("auto", "always", "never"),
        default="auto",
        help="Colorize terminal preview output (default: auto)",
    )
    parser.add_argument(
        "--foreground",
        choices=tuple(COLOR_STYLES),
        default="magenta",
        help="Foreground color for animated frames when color is enabled",
    )
    return parser


def _print_categories() -> None:
    print(f"{len(CATEGORY_NAMES)} categories available:\n")
    for category in CATEGORY_NAMES:
        print(f"  {category} ({len(spinner_names_for_category(category))} spinners)")


def _print_list(category: str | None = None) -> None:
    names = SPINNER_NAMES if category is None else spinner_names_for_category(category)
    label = "spinners" if category is None else f"{category} spinners"
    print(f"{len(names)} {label} available:\n")
    for name in names:
        spinner = spinners[name]
        category_name = SPINNER_CATEGORIES[name]
        print(
            f"  {spinner.frames[0]}  {name} "
            f"[{category_name}] ({len(spinner.frames)} frames, {spinner.interval}ms)"
        )


def _animate(
    name: str | None,
    *,
    color: str = "auto",
    foreground: str = "magenta",
) -> int:
    names = list(SPINNER_NAMES)

    if not sys.stdout.isatty():
        _print_list()
        return 0

    current = names.index(name) if name else 0
    single = name is not None
    frame_idx = 0
    ticks_on_current = 0
    ticks_per_spinner = 40
    preview_style = _resolve_preview_style(
        color=color,
        foreground=foreground,
        is_tty=True,
    )

    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

    try:
        while True:
            spinner_name = names[current]
            spinner = spinners[spinner_name]
            frame = spinner.frames[frame_idx % len(spinner.frames)]
            count = "" if single else f"[{current + 1}/{len(names)}]"

            sys.stdout.write(
                _render_preview_line(
                    frame=frame,
                    spinner_name=spinner_name,
                    interval=spinner.interval,
                    count=count,
                    style=preview_style,
                )
            )
            sys.stdout.flush()

            time.sleep(spinner.interval / 1000)
            frame_idx += 1
            ticks_on_current += 1

            if not single and ticks_on_current >= ticks_per_spinner:
                ticks_on_current = 0
                frame_idx = 0
                current = (current + 1) % len(names)
    except KeyboardInterrupt:
        sys.stdout.write("\n")
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.category and not args.list:
        parser.error("--category requires --list")

    if args.web:
        return serve_demo(port=args.port, open_browser=True)

    if args.list:
        _print_list(args.category)
        return 0

    if args.categories:
        _print_categories()
        return 0

    if args.name and args.name not in spinners:
        print(f'Unknown spinner: "{args.name}"', file=sys.stderr)
        print("Run with --list to see all spinners.", file=sys.stderr)
        return 1

    return _animate(args.name, color=args.color, foreground=args.foreground)


if __name__ == "__main__":
    raise SystemExit(main())
