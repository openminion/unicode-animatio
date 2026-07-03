from __future__ import annotations

from pathlib import Path

from unicode_animations import BRAILLE_SPINNER_NAMES

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_MARKDOWN = [
    ROOT / "README.md",
    ROOT / "API_COMPATIBILITY.md",
    ROOT / "RELEASING.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "source-tree-owner-map.md",
    ROOT / "CONTRIBUTING.md",
]


def test_required_public_package_docs_exist() -> None:
    required_paths = [
        ROOT / "README.md",
        ROOT / "API_COMPATIBILITY.md",
        ROOT / "RELEASING.md",
        ROOT / "docs" / "README.md",
        ROOT / "docs" / "source-tree-owner-map.md",
        ROOT / "scripts" / "release_check.py",
    ]
    missing = [path.relative_to(ROOT).as_posix() for path in required_paths if not path.exists()]
    assert missing == []


def test_public_markdown_surfaces_avoid_machine_local_paths() -> None:
    blocked_fragments = ["/Users/", "file://"]

    for path in PUBLIC_MARKDOWN:
        text = path.read_text(encoding="utf-8")
        for fragment in blocked_fragments:
            assert fragment not in text, f"{path.name} leaked {fragment}"


def test_readme_lists_all_spinner_families() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Available animations" in text
    for name in BRAILLE_SPINNER_NAMES:
        assert f"`{name}`" in text
