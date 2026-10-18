#!/usr/bin/env python3
"""Terminal demo that previews unicode_animations spinners using the Python API."""

from __future__ import annotations

import argparse
import sys
import time

from unicode_animations import SPINNER_NAMES, spinners

HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"
CLEAR_LINE = "\r\x1b[2K"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Show unicode_animations spinners directly from Python.",
    )
    parser.add_argument("name", nargs="?", help="Specific spinner name to run")
    parser.add_argument(
        "--seconds-per-spinner",
        type=float,
        default=1.6,
        help="How long to animate each spinner when showing all (default: 1.6)",
    )
    parser.add_argument(
        "--loops",
        type=int,
        default=1,
        help="How many full passes through all spinners (default: 1)",
    )
    parser.add_argument("--list", action="store_true", help="List spinner names and exit")
    return parser


def _print_list() -> None:
    print(f"{len(SPINNER_NAMES)} spinners:\n")
    for name in SPINNER_NAMES:
        _print_spinner(name)


def _print_spinner(name: str) -> None:
    spinner = spinners[name]
    print(f"  {spinner.frames[0]}  {name} ({len(spinner.frames)} frames, {spinner.interval}ms)")


def _animate(name: str, seconds: float) -> None:
    spinner = spinners[name]
    end_time = time.monotonic() + seconds
    idx = 0

    while time.monotonic() < end_time:
        frame = spinner.frames[idx % len(spinner.frames)]
        sys.stdout.write(f"{CLEAR_LINE}  {frame}  {name} ({spinner.interval}ms)")
        sys.stdout.flush()
        time.sleep(spinner.interval / 1000)
        idx += 1


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.list and args.name is not None:
        parser.error("a spinner name cannot be combined with --list")
    if args.seconds_per_spinner <= 0:
        parser.error("--seconds-per-spinner must be greater than 0")
    if args.loops < 1:
        parser.error("--loops must be at least 1")

    if args.list:
        _print_list()
        return 0

    if args.name is not None and args.name not in spinners:
        print(f'Unknown spinner: "{args.name}"', file=sys.stderr)
        print("Run with --list to see available names.", file=sys.stderr)
        return 1

    if not sys.stdout.isatty():
        if args.name is not None:
            _print_spinner(args.name)
        else:
            _print_list()
        return 0

    names = [args.name] if args.name is not None else list(SPINNER_NAMES)

    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

    try:
        loop_count = 1 if args.name is not None else args.loops
        for _ in range(loop_count):
            for name in names:
                _animate(name, args.seconds_per_spinner)
                if args.name is None:
                    sys.stdout.write(f"{CLEAR_LINE}  \u2714  {name}\n")
                    sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(f"{CLEAR_LINE}{SHOW_CURSOR}\n")
        sys.stdout.flush()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
