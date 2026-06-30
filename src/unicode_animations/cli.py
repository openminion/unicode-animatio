"""Terminal demo CLI for unicode_animations."""

from __future__ import annotations

import argparse
import sys
import time
from collections.abc import Sequence

from .braille import BRAILLE_SPINNER_NAMES, spinners
from .web import serve_demo

HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"
MAGENTA = "\x1b[35m"
RESET = "\x1b[0m"
CLEAR_LINE = "\r\x1b[2K"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="unicode-animations",
        description="Preview unicode braille spinner animations.",
    )
    parser.add_argument("name", nargs="?", help="Spinner name to preview")
    parser.add_argument("-l", "--list", action="store_true", help="List available spinners")
    parser.add_argument("-w", "--web", action="store_true", help="Open browser demo")
    parser.add_argument("--port", type=int, default=0, help="Port for --web mode (default: auto)")
    return parser


def _print_list() -> None:
    names = list(BRAILLE_SPINNER_NAMES)
    print(f"{len(names)} spinners available:\n")
    for name in names:
        spinner = spinners[name]
        print(f"  {spinner.frames[0]}  {name} ({len(spinner.frames)} frames, {spinner.interval}ms)")


def _animate(name: str | None) -> int:
    names = list(BRAILLE_SPINNER_NAMES)

    if not sys.stdout.isatty():
        _print_list()
        return 0

    current = names.index(name) if name else 0
    single = name is not None
    frame_idx = 0
    ticks_on_current = 0
    ticks_per_spinner = 40

    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

    try:
        while True:
            spinner_name = names[current]
            spinner = spinners[spinner_name]
            frame = spinner.frames[frame_idx % len(spinner.frames)]
            count = "" if single else f"[{current + 1}/{len(names)}]"

            sys.stdout.write(
                f"{CLEAR_LINE}  {MAGENTA}{frame}{RESET}  {BOLD}{spinner_name}{RESET} "
                f"{DIM}{spinner.interval}ms{RESET}  {DIM}{count}{RESET}"
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

    if args.web:
        return serve_demo(port=args.port, open_browser=True)

    if args.list:
        _print_list()
        return 0

    if args.name and args.name not in spinners:
        print(f'Unknown spinner: "{args.name}"', file=sys.stderr)
        print("Run with --list to see all spinners.", file=sys.stderr)
        return 1

    return _animate(args.name)


if __name__ == "__main__":
    raise SystemExit(main())
