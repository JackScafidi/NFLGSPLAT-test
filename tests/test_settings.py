"""Machine settings: environment variables, then local.yaml, then defaults."""
import subprocess
import sys
from pathlib import Path

import pytest

from nfl_gsplat import settings as st
from nfl_gsplat.errors import SetupError

REPO = Path(__file__).resolve().parents[1]


def _load(tmp_path, yaml_text=None, **env):
    local = tmp_path / "local.yaml"
    if yaml_text is not None:
        local.write_text(yaml_text, encoding="utf-8")
    return st.load(environ=env, local_yaml=local)


def test_repo_root_is_found_from_the_code_not_the_working_directory():
    assert st.REPO_ROOT == REPO
    assert (st.REPO_ROOT / "pyproject.toml").is_file()


def test_defaults_sit_inside_the_repo(tmp_path):
    s = _load(tmp_path)
    assert s.data_root == REPO / "data"
    assert s.body_models == REPO / "data" / "body_models"
    assert s.diag_dir == REPO / "outputs" / "diag"
    assert s.python_nflgsplat is None and s.python_smplx is None
    assert all(p.is_absolute() for p in (s.data_root, s.body_models, s.diag_dir))


def test_local_yaml_overrides_the_defaults(tmp_path):
    nfl, diag, py = tmp_path / "nfl", tmp_path / "diag", tmp_path / "smplx312" / "python.exe"
    s = _load(tmp_path, f"data_root: {nfl.as_posix()}\ndiag_dir: {diag.as_posix()}\n"
                        f"python_smplx: {py.as_posix()}\n")
    assert s.data_root == nfl
    assert s.diag_dir == diag
    assert s.python_smplx == py


def test_environment_overrides_local_yaml(tmp_path):
    s = _load(tmp_path, f"diag_dir: {(tmp_path / 'diag').as_posix()}\n", NFLG_DIAG_DIR=str(tmp_path / "env"))
    assert s.diag_dir == tmp_path / "env"


def test_body_models_follow_the_data_root_unless_set(tmp_path):
    nfl, models = tmp_path / "nfl", tmp_path / "models"
    assert _load(tmp_path, f"data_root: {nfl.as_posix()}\n").body_models == nfl / "body_models"
    s = _load(tmp_path, f"data_root: {nfl.as_posix()}\nbody_models: {models.as_posix()}\n")
    assert s.body_models == models


def test_relative_paths_are_taken_from_the_repo_root(tmp_path):
    s = _load(tmp_path, "data_root: ../shared-data\n", NFLG_DIAG_DIR="scratch/diag")
    assert s.data_root == (REPO / "../shared-data").resolve()
    assert s.diag_dir == REPO / "scratch" / "diag"


def test_an_unknown_key_in_local_yaml_fails_loudly(tmp_path):
    # A typo must not silently fall back to the default.
    with pytest.raises(SetupError, match="diag_dri"):
        _load(tmp_path, "diag_dri: somewhere\n")


def test_local_yaml_that_is_not_a_mapping_fails_loudly(tmp_path):
    with pytest.raises(SetupError, match="local.yaml"):
        _load(tmp_path, "- just\n- a list\n")


def test_a_missing_local_yaml_is_fine(tmp_path):
    assert not (tmp_path / "local.yaml").exists()
    assert _load(tmp_path).data_root == REPO / "data"


def test_an_unset_environment_python_points_at_the_fix(tmp_path):
    s = _load(tmp_path)
    with pytest.raises(SetupError, match="python_smplx.*local.yaml"):
        s.python("smplx")


def test_a_set_environment_python_must_exist(tmp_path):
    s = _load(tmp_path, f"python_nflgsplat: {(tmp_path / 'nope' / 'python.exe').as_posix()}\n")
    with pytest.raises(SetupError, match="does not exist"):
        s.python("nflgsplat")


def test_a_set_environment_python_is_returned(tmp_path):
    exe = tmp_path / "python.exe"
    exe.write_text("")
    s = _load(tmp_path, f"python_nflgsplat: {exe.as_posix()}\n")
    assert s.python("nflgsplat") == exe


def test_an_unknown_environment_name_fails_loudly(tmp_path):
    with pytest.raises(SetupError, match="gsplat"):
        _load(tmp_path).python("gsplat")


def test_the_example_file_lists_every_setting():
    import yaml
    example = yaml.safe_load((REPO / "local.example.yaml").read_text(encoding="utf-8"))
    assert set(example) == set(st.KEYS)


def test_local_yaml_is_gitignored():
    out = subprocess.run(["git", "check-ignore", "-q", "local.yaml"], cwd=REPO)
    assert out.returncode == 0


def test_shell_output_exports_every_path(tmp_path):
    exe = tmp_path / "python.exe"
    exe.write_text("")
    env = {"NFLG_PY_SMPLX": str(exe), "NFLG_DIAG_DIR": str(tmp_path / "diag")}
    lines = st.shell_exports(st.load(environ=env, local_yaml=tmp_path / "none.yaml"))
    assert f"export NFLG_DIAG_DIR='{(tmp_path / 'diag').as_posix()}'" in lines
    assert f"export NFLG_PY_SMPLX='{exe.as_posix()}'" in lines
    assert f"export NFLG_REPO_ROOT='{REPO.as_posix()}'" in lines
    assert not any(line.startswith("export NFLG_PY_NFLGSPLAT=") for line in lines)   # unset stays unset


def test_the_command_line_prints_the_shell_exports(tmp_path):
    out = subprocess.run([sys.executable, "-m", "nfl_gsplat.settings", "--shell"],
                         cwd=tmp_path, capture_output=True, text=True, check=True)
    assert f"export NFLG_REPO_ROOT='{REPO.as_posix()}'" in out.stdout.splitlines()
