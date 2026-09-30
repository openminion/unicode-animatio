"""Terminal demo CLI for unicode_animations."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass

from . import __version__
from .catalog import (
    CATEGORY_NAMES,
    SPINNER_NAMES,
    SpinnerMetadata,
    metadata_for_spinner,
    search_spinner_names,
    spinner_names_for_category,
    spinners,
)
from .web import _port_number, serve_demo

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
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("name", nargs="?", help="Spinner name to preview")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-l", "--list", action="store_true", help="List available spinners")
    mode.add_argument("--categories", action="store_true", help="List spinner categories")
    mode.add_argument("--show", metavar="NAME", help="Show one spinner preset")
    mode.add_argument("-w", "--web", action="store_true", help="Open browser demo")
    parser.add_argument("--category", choices=CATEGORY_NAMES, help="Filter --list or --search")
    parser.add_argument(
        "--search",
        metavar="TEXT",
        help="Search preset names, categories, and tags",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--host", help="Host for --web mode (default: 127.0.0.1)")
    parser.add_argument("--port", type=_port_number, help="Port for --web mode (default: auto)")
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not open a browser in --web mode",
    )
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


def _metadata_payload(
    metadata: SpinnerMetadata,
    *,
    include_frames: bool = False,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "name": metadata.name,
        "category": metadata.category,
        "tags": list(metadata.tags),
        "frame_count": metadata.frame_count,
        "interval_ms": metadata.interval_ms,
        "frame_width": metadata.frame_width,
        "preview_frame": metadata.preview_frame,
        "motion": metadata.motion,
        "description": metadata.description,
    }
    if include_frames:
        payload["frames"] = list(spinners[metadata.name].frames)
    return payload


def _print_json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _print_categories(*, json_output: bool = False) -> None:
    if json_output:
        _print_json(
            [
                {
                    "name": category,
                    "count": len(spinner_names_for_category(category)),
                }
                for category in CATEGORY_NAMES
            ]
        )
        return

    print(f"{len(CATEGORY_NAMES)} categories available:\n")
    for category in CATEGORY_NAMES:
        print(f"  {category} ({len(spinner_names_for_category(category))} spinners)")


def _print_list(
    *,
    category: str | None = None,
    search: str = "",
    json_output: bool = False,
) -> None:
    names = search_spinner_names(search, category=category)
    metadata = tuple(metadata_for_spinner(name) for name in names)
    if json_output:
        _print_json([_metadata_payload(item) for item in metadata])
        return

    category_label = f"{category} " if category else ""
    noun = "spinner" if len(names) == 1 else "spinners"
    match_label = f' matching "{search}"' if search else ""
    print(f"{len(names)} {category_label}{noun}{match_label} available:\n")
    for item in metadata:
        print(
            f"  {item.preview_frame}  {item.name} "
            f"[{item.category}] ({item.frame_count} frames, {item.interval_ms}ms) "
            f"tags: {', '.join(item.tags)}"
        )


def _print_show(name: str, *, json_output: bool = False) -> int:
    if name not in spinners:
        print(f'Unknown spinner: "{name}"', file=sys.stderr)
        print("Run with --list to see all spinners.", file=sys.stderr)
        return 1

    metadata = metadata_for_spinner(name)
    if json_output:
        _print_json(_metadata_payload(metadata, include_frames=True))
        return 0

    print(f"{metadata.name}")
    print(f"  category: {metadata.category}")
    print(f"  tags: {', '.join(metadata.tags)}")
    print(f"  frames: {metadata.frame_count}")
    print(f"  interval: {metadata.interval_ms}ms")
    print(f"  width: {metadata.frame_width}")
    print(f"  motion: {metadata.motion}")
    print(f"  use: {metadata.description}")
    print(f"  preview: {metadata.preview_frame}")
    print(f"  python: provider.get({metadata.name!r})")
    return 0


def _animate(
    name: str | None,
    *,
    color: str = "auto",
    foreground: str = "magenta",
) -> int:
    if not sys.stdout.isatty():
        if name is not None:
            return _print_show(name)
        _print_list()
        return 0

    names: list[str] = list(SPINNER_NAMES)
    current = names.index(name) if name is not None else 0
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
    search_requested = args.search is not None

    if args.category and not (args.list or search_requested):
        parser.error("--category requires --list or --search")
    if args.json and not (
        args.list or args.categories or args.show is not None or search_requested
    ):
        parser.error("--json requires --list, --categories, --search, or --show")
    if not args.web and (args.host is not None or args.port is not None or args.no_open):
        parser.error("--host, --port, and --no-open require --web")
    if search_requested and (args.show is not None or args.categories or args.web):
        parser.error("--search cannot be combined with --show, --categories, or --web")
    if search_requested and args.name is not None:
        parser.error("--search cannot be combined with a spinner name")
    if args.show is not None and args.name is not None:
        parser.error("--show cannot be combined with a spinner name")

    if args.web:
        return serve_demo(
            host=args.host or "127.0.0.1",
            port=args.port or 0,
            open_browser=not args.no_open,
        )

    if args.show is not None:
        return _print_show(args.show, json_output=args.json)

    if args.list:
        _print_list(category=args.category, search=args.search or "", json_output=args.json)
        return 0

    if search_requested:
        _print_list(category=args.category, search=args.search, json_output=args.json)
        return 0

    if args.categories:
        _print_categories(json_output=args.json)
        return 0

    if args.name is not None and args.name not in spinners:
        print(f'Unknown spinner: "{args.name}"', file=sys.stderr)
        print("Run with --list to see all spinners.", file=sys.stderr)
        return 1

    return _animate(args.name, color=args.color, foreground=args.foreground)


if __name__ == "__main__":
    raise SystemExit(main())
