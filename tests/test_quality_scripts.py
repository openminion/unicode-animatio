from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_quality_validator() -> ModuleType:
    path = REPO_ROOT / "scripts" / "validate_quality_patterns.py"
    spec = importlib.util.spec_from_file_location("unicode_quality_patterns", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_quality_pattern_validator_passes_current_baselines() -> None:
    subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate_quality_patterns.py"),
            "--check",
            "all",
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def test_quality_validator_uses_the_hatch_wheel_package() -> None:
    validator = _load_quality_validator()

    project = validator._project_info()

    assert project.name == "unicode-animatio"
    assert project.import_root == "unicode_animations"
    assert project.source_root == REPO_ROOT / "src" / "unicode_animations"
