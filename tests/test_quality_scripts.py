from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

BASELINES = (
    (
        "MAX_FILE_LOC_BASELINE",
        "_max_file_loc_rows",
        "# Format: path<TAB>loc<TAB>reason",
        ("src/fixture/large.py", 1200, "reason"),
    ),
    (
        "METHOD_LOC_BASELINE",
        "_method_loc_rows",
        "# Format: path<TAB>qualname<TAB>loc<TAB>reason",
        ("src/fixture/large.py", "large", 120, "reason"),
    ),
    (
        "HELPER_DUPLICATES_BASELINE",
        "_helper_duplicate_rows",
        "# Format: directory<TAB>function<TAB>files<TAB>reason",
        ("src/fixture", "_same", "src/fixture/a.py,src/fixture/b.py,src/fixture/c.py", "reason"),
    ),
    (
        "FILENAME_UNDERSCORE_BASELINE",
        "_filename_underscore_rows",
        "# Format: path<TAB>underscore_count",
        ("scripts/old_file_name.py", 3),
    ),
    (
        "BROAD_EXCEPTION_BASELINE",
        "_broad_exception_rows",
        "# Format: path<TAB>total<TAB>silent_pass<TAB>reason",
        ("src/fixture/large.py", 2, 1, "reason"),
    ),
    (
        "PATH_STRUCTURE_BASELINE",
        "_path_structure_rows",
        "# Format: source_relative_path<TAB>finding",
        ("old.py", "old finding"),
    ),
)


def _load_quality_validator() -> ModuleType:
    path = REPO_ROOT / "scripts" / "validate_quality_patterns.py"
    spec = importlib.util.spec_from_file_location("unicode_quality_patterns", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def baseline_case(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    validator = _load_quality_validator()
    rows = {}
    paths = []
    for baseline_name, collector_name, header, row in BASELINES:
        path = tmp_path / f"{baseline_name.lower()}.tsv"
        monkeypatch.setattr(validator, baseline_name, path)
        validator._write_tsv(path, header, [row])
        rows[collector_name] = [row]
        paths.append(path)
        monkeypatch.setattr(
            validator,
            collector_name,
            lambda _project, name=collector_name: rows[name],
        )
    project = validator.ProjectInfo("fixture", "fixture", tmp_path / "src" / "fixture", frozenset())
    return validator, project, rows, paths


@pytest.mark.parametrize(
    ("collector", "regression"),
    [
        ("_max_file_loc_rows", ("src/fixture/new.py", 1200, "reason")),
        ("_max_file_loc_rows", ("src/fixture/large.py", 1201, "reason")),
        ("_method_loc_rows", ("src/fixture/new.py", "large", 120, "reason")),
        ("_method_loc_rows", ("src/fixture/large.py", "large", 121, "reason")),
        (
            "_helper_duplicate_rows",
            ("src/fixture", "_new", "src/fixture/a.py,src/fixture/b.py", "reason"),
        ),
        (
            "_helper_duplicate_rows",
            ("src/fixture", "_same", "src/fixture/a.py,src/fixture/d.py", "reason"),
        ),
        ("_filename_underscore_rows", ("scripts/new_file_name.py", 3)),
        ("_filename_underscore_rows", ("scripts/old_file_name.py", 4)),
        ("_broad_exception_rows", ("src/fixture/new.py", 1, 0, "reason")),
        ("_broad_exception_rows", ("src/fixture/large.py", 3, 1, "reason")),
        ("_broad_exception_rows", ("src/fixture/large.py", 2, 2, "reason")),
        ("_path_structure_rows", ("new.py", "new finding")),
    ],
)
def test_baseline_writer_rejects_new_debt_without_writing(baseline_case, collector, regression):
    validator, project, rows, paths = baseline_case
    rows[collector] = [regression]
    before = [path.read_bytes() for path in paths]

    with pytest.raises(SystemExit, match="baseline"):
        validator.write_baselines(project)

    assert [path.read_bytes() for path in paths] == before


def test_baseline_writer_accepts_equal_reduced_and_removed_debt(baseline_case):
    validator, project, rows, paths = baseline_case
    for path in (paths[0], paths[1], paths[2], paths[4]):
        path.write_text(path.read_text().replace("\treason\n", "\tbespoke reason\n"))
    before = [path.read_bytes() for path in paths]
    validator.write_baselines(project)
    assert [path.read_bytes() for path in paths] == before

    rows["_max_file_loc_rows"] = [("src/fixture/large.py", 1100, "reason")]
    rows["_method_loc_rows"] = [("src/fixture/large.py", "large", 110, "reason")]
    rows["_helper_duplicate_rows"] = [
        ("src/fixture", "_same", "src/fixture/a.py,src/fixture/b.py", "reason")
    ]
    rows["_filename_underscore_rows"] = [("scripts/old_file_name.py", 2)]
    rows["_broad_exception_rows"] = [("src/fixture/large.py", 1, 0, "reason")]
    rows["_path_structure_rows"] = []
    validator.write_baselines(project)
    assert b"1100" in paths[0].read_bytes()
    assert all(
        b"bespoke reason" in path.read_bytes() for path in (paths[0], paths[1], paths[2], paths[4])
    )
    assert b"old finding" not in paths[-1].read_bytes()

    for collector in rows:
        rows[collector] = []
    validator.write_baselines(project)
    assert all(len(path.read_text().splitlines()) == 1 for path in paths)


def test_baseline_writer_rejects_mixed_update(baseline_case):
    validator, project, rows, paths = baseline_case
    rows["_max_file_loc_rows"] = [("src/fixture/large.py", 1100, "reason")]
    rows["_method_loc_rows"] = [("src/fixture/large.py", "large", 121, "reason")]
    before = [path.read_bytes() for path in paths]

    with pytest.raises(SystemExit, match="baseline"):
        validator.write_baselines(project)

    assert [path.read_bytes() for path in paths] == before


def test_missing_baseline_does_not_admit_debt(baseline_case):
    validator, project, _rows, paths = baseline_case
    paths[0].unlink()
    before = [path.read_bytes() for path in paths[1:]]

    with pytest.raises(SystemExit, match="baseline"):
        validator.write_baselines(project)

    assert [path.read_bytes() for path in paths[1:]] == before
    assert not paths[0].exists()


def test_baseline_writer_cli_rejects_122_line_method(tmp_path: Path):
    script = tmp_path / "scripts" / "validate_quality_patterns.py"
    script.parent.mkdir()
    shutil.copy2(REPO_ROOT / "scripts" / "validate_quality_patterns.py", script)
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "fixture"\n')
    source = tmp_path / "src" / "fixture" / "large.py"
    source.parent.mkdir(parents=True)
    source.write_text("def large():\n" + "    pass\n" * 121)
    baseline_dir = tmp_path / "scripts" / "baselines"
    baseline_dir.mkdir()
    baseline = baseline_dir / "method_loc_baseline.tsv"
    baseline.write_text(
        "# Format: path<TAB>qualname<TAB>loc<TAB>reason\nsrc/fixture/large.py\tlarge\t110\treason\n"
    )
    for name, content in (
        ("max_file_loc_baseline.tsv", "# Format: path<TAB>loc<TAB>reason\n"),
        (
            "helper_duplicates_baseline.tsv",
            "# Format: directory<TAB>function<TAB>files<TAB>reason\n",
        ),
        (
            "filename_underscore_hygiene.tsv",
            "# Format: path<TAB>underscore_count\nscripts/validate_quality_patterns.py\t2\n",
        ),
        ("broad_exception_baseline.tsv", "# Format: path<TAB>total<TAB>silent_pass<TAB>reason\n"),
        ("path_structure_hygiene.tsv", "# Format: source_relative_path<TAB>finding\n"),
    ):
        (baseline_dir / name).write_text(content)
    before = {path.name: path.read_bytes() for path in baseline_dir.iterdir()}

    result = subprocess.run(
        [sys.executable, str(script), "--write-baselines"], capture_output=True, text=True
    )

    assert result.returncode != 0
    assert result.stderr.strip() == (
        "baseline growth rejected:\nmethod_loc_baseline.tsv: src/fixture/large.py/large"
    )
    assert {path.name: path.read_bytes() for path in baseline_dir.iterdir()} == before


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
