#!/usr/bin/env python3
"""Run package-local release validation for unicode-animatio."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
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


def _assert_license_metadata(text: str) -> None:
    assert "License-Expression: MIT\n" in text
    assert "License-File: LICENSE\n" in text


def _check_distribution_metadata() -> None:
    wheel = _dist_wheel()
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        metadata_name = next(name for name in names if name.endswith(".dist-info/METADATA"))
        _assert_license_metadata(archive.read(metadata_name).decode("utf-8"))
        assert any(name.endswith(".dist-info/licenses/LICENSE") for name in names)

    sdist = next(DIST_DIR.glob("unicode_animatio-*.tar.gz"))
    with tarfile.open(sdist) as archive:
        names = archive.getnames()
        metadata_name = next(name for name in names if name.endswith("/PKG-INFO"))
        metadata_file = archive.extractfile(metadata_name)
        assert metadata_file is not None
        _assert_license_metadata(metadata_file.read().decode("utf-8"))
        assert any(name.endswith("/LICENSE") for name in names)


def _fresh_install_smoke() -> None:
    with tempfile.TemporaryDirectory(prefix="unicode-animatio-release-") as tmpdir:
        venv_dir = Path(tmpdir) / "venv"
        _run(sys.executable, "-m", "venv", str(venv_dir))
        pip = venv_dir / "bin" / "pip"
        python = venv_dir / "bin" / "python"
        cli = venv_dir / "bin" / "unicode-animatio"
        web_cli = venv_dir / "bin" / "unicode-animatio-web"
        _run(str(pip), "install", str(_dist_wheel()))
        _run(
            str(python),
            "-c",
            (
                "from importlib.metadata import distribution; "
                "from unicode_animations import ("
                "__version__, BRAILLE_SPINNER_NAMES, SPINNER_NAMES); "
                "from unicode_animations.web import build_spinner_payload; "
                "dist = distribution('unicode-animatio'); "
                "assert dist.metadata['License-Expression'] == 'MIT'; "
                "assert 'LICENSE' in dist.metadata.get_all('License-File'); "
                "assert any(str(path).endswith('unicode_animations/py.typed') "
                "for path in dist.files); "
                "matches = tuple(ep for ep in dist.entry_points "
                "if ep.group == 'openminion.cli.animation_providers' "
                "and ep.name == 'unicode'); "
                "assert len(matches) == 1; "
                "provider = matches[0].load()(); "
                "assert provider.provider_id == 'unicode'; "
                "assert provider.names() == SPINNER_NAMES; "
                "assert provider.get('braille').name == 'braille'; "
                "assert __version__; "
                "assert BRAILLE_SPINNER_NAMES is SPINNER_NAMES; "
                "assert len(build_spinner_payload()) == len(SPINNER_NAMES)"
            ),
        )
        _run(str(cli), "--list")
        _run(str(web_cli), "--version")


def main() -> int:
    for directory in (BUILD_DIR, DIST_DIR):
        if directory.exists():
            shutil.rmtree(directory)

    _run(sys.executable, "-m", "pytest", "-q")
    _run(sys.executable, "-m", "ruff", "check", ".")
    _run(sys.executable, "-m", "build")
    _check_distribution_metadata()
    _fresh_install_smoke()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
