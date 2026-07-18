#!/usr/bin/env python3
"""Run package-local release validation for unicode-animatio."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"


def _run(*args: str) -> None:
    print("+", " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def _dist_wheel() -> Path:
    wheels = sorted(DIST_DIR.glob("unicode_animatio-*.whl"))
    if not wheels:
        raise SystemExit("release_check: expected a built wheel under dist/")
    return wheels[-1]


def _fresh_install_smoke() -> None:
    with tempfile.TemporaryDirectory(prefix="unicode-animatio-release-") as tmpdir:
        venv_dir = Path(tmpdir) / "venv"
        _run(sys.executable, "-m", "venv", str(venv_dir))
        pip = venv_dir / "bin" / "pip"
        python = venv_dir / "bin" / "python"
        cli = venv_dir / "bin" / "unicode-animatio"
        _run(str(pip), "install", str(_dist_wheel()))
        _run(
            str(python),
            "-c",
            (
                "from unicode_animations import ("
                "__version__, BRAILLE_SPINNER_NAMES, SPINNER_NAMES); "
                "from unicode_animations.web import build_spinner_payload; "
                "assert __version__; "
                "assert BRAILLE_SPINNER_NAMES is SPINNER_NAMES; "
                "assert len(build_spinner_payload()) == len(SPINNER_NAMES)"
            ),
        )
        _run(str(cli), "--list")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run unicode-animatio release checks.")
    parser.add_argument(
        "--skip-build-clean",
        action="store_true",
        help="Keep existing build/ and dist/ directories before rebuilding.",
    )
    args = parser.parse_args(argv)

    if not args.skip_build_clean:
        shutil.rmtree(BUILD_DIR, ignore_errors=True)
        shutil.rmtree(DIST_DIR, ignore_errors=True)

    _run(sys.executable, "-m", "pytest", "-q")
    _run(sys.executable, "-m", "ruff", "check", ".")
    _run(sys.executable, "-m", "build")
    _fresh_install_smoke()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
