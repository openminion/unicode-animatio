from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TERMINAL_DEMO = ROOT / "examples" / "terminal_demo.py"


def _run_terminal_demo(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TERMINAL_DEMO), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def test_terminal_demo_rejects_empty_spinner_name() -> None:
    result = _run_terminal_demo("")

    assert result.returncode == 1
    assert 'Unknown spinner: ""' in result.stderr
    assert result.stdout == ""


def test_terminal_demo_rejects_list_with_spinner_name() -> None:
    result = _run_terminal_demo("edgepulse", "--list")

    assert result.returncode == 2
    assert "a spinner name cannot be combined with --list" in result.stderr
