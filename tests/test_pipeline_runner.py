"""Pipeline runner core, with fake stages (small Python commands that write files)."""
import json
import sys
from pathlib import Path

import pytest

from nfl_gsplat.errors import PipelineError
from nfl_gsplat.pipeline import runner as rn
from nfl_gsplat.pipeline.runner import Stage


def _py(code: str) -> tuple[str, ...]:
    """A command run by the stage's interpreter: ``python -c code {play}``."""
    return ("-c", code, "{play}")


# Each fake stage is one line of Python; sys.argv[1] is the play-dir.
COPY = "import sys,shutil,pathlib as p; d=p.Path(sys.argv[1]); shutil.copy(d/'{a}', d/'{b}')"
APPEND = "import sys,pathlib as p; f=p.Path(sys.argv[1])/'{f}'; f.write_text(f.read_text()+'{s}')"


def _copy(a, b):
    return _py(COPY.format(a=a, b=b))


def _append(f, s):
    return _py(APPEND.format(f=f, s=s))


def _chain():
    """source.txt -> a.txt -> b.txt, with b.txt then rewritten in place."""
    return [
        Stage("one", commands=(_copy("source.txt", "a.txt"),), inputs=("source.txt",), outputs=("a.txt",)),
        Stage("two", commands=(_copy("a.txt", "b.txt"),), inputs=("a.txt",), outputs=("b.txt",)),
        Stage("three", commands=(_append("b.txt", "!"),), inputs=("b.txt",), outputs=("b.txt",)),
    ]


def _run(stages, play, **kw):
    kw.setdefault("python_for", lambda env: sys.executable)
    kw.setdefault("echo", lambda line: None)
    return rn.run(stages, play, **kw)


@pytest.fixture
def play(tmp_path):
    d = tmp_path / "play"
    d.mkdir()
    (d / "source.txt").write_text("hello")
    return d


def test_runs_the_stages_in_order_and_records_them(play):
    rep = _run(_chain(), play)
    assert rep.ran == ["one", "two", "three"]
    assert (play / "b.txt").read_text() == "hello!"
    m = json.loads((play / rn.MANIFEST).read_text())
    assert [m["stages"][s]["status"] for s in ("one", "two", "three")] == ["ok"] * 3


def test_a_second_run_runs_nothing(play):
    _run(_chain(), play)
    rep = _run(_chain(), play)
    assert rep.ran == []
    assert (play / "b.txt").read_text() == "hello!"     # the in-place stage did not run twice


def test_a_changed_source_reruns_from_the_stage_that_reads_it(play):
    _run(_chain(), play)
    (play / "source.txt").write_text("bye")
    rep = _run(_chain(), play)
    assert rep.ran == ["one", "two", "three"]
    assert (play / "b.txt").read_text() == "bye!"


def test_a_rerun_that_writes_the_same_bytes_stops_the_cascade(play):
    stages = _chain()
    _run(stages, play)
    rep = _run(stages, play, force=("one",))
    assert rep.ran == ["one"]            # a.txt came out identical, so two and three stay done


def test_a_changed_setting_reruns_only_the_stages_that_use_it(play):
    def stages(mark):
        return [
            Stage("one", commands=(_copy("source.txt", "a.txt"),), inputs=("source.txt",), outputs=("a.txt",)),
            Stage("tag", commands=(_py("import sys,pathlib as p; (p.Path(sys.argv[1])/'t.txt').write_text(sys.argv[2])")
                                   + ("{mark}",),),
                  inputs=("a.txt",), outputs=("t.txt",), settings=("mark",)),
        ]
    _run(stages("x"), play, play_settings={"mark": "x"})
    rep = _run(stages("x"), play, play_settings={"mark": "y"})
    assert rep.ran == ["tag"]
    assert (play / "t.txt").read_text() == "y"


def test_a_changed_code_file_reruns_its_stage(play, tmp_path):
    code = tmp_path / "stage_two.py"
    code.write_text("# v1\n")
    stages = _chain()
    stages[1] = Stage("two", commands=stages[1].commands, inputs=("a.txt",), outputs=("b.txt",), code=(code,))
    _run(stages, play)
    code.write_text("# v2\n")
    rep = _run(stages, play)
    assert rep.ran == ["two", "three"]


def test_a_failing_stage_stops_the_run_and_resumes_there(play):
    stages = _chain()
    stages[1] = Stage("two", commands=(_py("import sys; print('boom happened'); sys.exit(3)"),),
                      inputs=("a.txt",), outputs=("b.txt",))
    with pytest.raises(rn.StageFailed, match="two") as exc:
        _run(stages, play)
    log = play / "logs" / "two.log"
    assert "boom happened" in log.read_text(encoding="utf-8")
    assert str(log) in str(exc.value)
    m = json.loads((play / rn.MANIFEST).read_text())
    assert m["stages"]["two"]["status"] == "failed" and "three" not in m["stages"]
    rep = _run(_chain(), play)          # fixed: resumes at two; one is not run again
    assert rep.ran == ["two", "three"]


def test_a_missing_declared_output_fails_the_stage(play):
    stages = [Stage("one", commands=(_py("pass"),), inputs=("source.txt",), outputs=("never.txt",))]
    with pytest.raises(rn.StageFailed, match="never.txt"):
        _run(stages, play)


def test_an_input_nothing_provides_fails_before_anything_runs(play):
    stages = _chain() + [Stage("four", commands=(_py("pass"),), inputs=("missing.txt",), outputs=())]
    with pytest.raises(PipelineError, match="missing.txt"):
        _run(stages, play)
    assert not (play / "a.txt").exists()


def test_reading_a_file_only_a_later_stage_writes_is_a_declaration_error(play):
    stages = [Stage("early", commands=(_py("pass"),), inputs=("late.txt",), outputs=()),
              Stage("late", commands=(_py("pass"),), inputs=(), outputs=("late.txt",))]
    with pytest.raises(PipelineError, match="late.txt.*later stage"):
        _run(stages, play)


def test_a_stage_whose_condition_is_off_is_skipped_and_optional_inputs_may_be_absent(play):
    stages = [
        Stage("extra", commands=(_copy("source.txt", "extra.txt"),), inputs=("source.txt",),
              outputs=("extra.txt",), when=lambda s: s.get("extra", False)),
        Stage("use", commands=(_copy("source.txt", "u.txt"),), inputs=("source.txt",),
              optional_inputs=("extra.txt",), outputs=("u.txt",)),
    ]
    rep = _run(stages, play)
    assert rep.ran == ["use"] and rep.skipped == ["extra"]
    rep = _run(stages, play, play_settings={"extra": True})
    assert rep.ran == ["extra", "use"]          # the optional input appeared, so use reruns


def test_a_hand_edited_final_file_reruns_from_its_first_writer(play):
    _run(_chain(), play)
    (play / "b.txt").write_text("tampered")
    rep = _run(_chain(), play)
    assert rep.ran == ["two", "three"]
    assert (play / "b.txt").read_text() == "hello!"


def test_dry_run_reports_and_runs_nothing(play):
    rep = _run(_chain(), play, dry_run=True)
    assert rep.ran == [] and [s for s, _why in rep.would_run] == ["one", "two", "three"]
    assert not (play / "a.txt").exists()


def test_each_stage_logs_its_commands_and_output(play):
    _run([Stage("hi", commands=(_py("print('stage says hi')"),), inputs=(), outputs=())], play)
    text = (play / "logs" / "hi.log").read_text(encoding="utf-8")
    assert "stage says hi" in text and "-c" in text


def test_builtin_copy_runs_in_process(play):
    stages = [Stage("cp", commands=(("@copy", "source.txt", "c.txt"),), inputs=("source.txt",), outputs=("c.txt",))]
    assert _run(stages, play).ran == ["cp"]
    assert (play / "c.txt").read_text() == "hello"


def test_the_interpreter_comes_from_the_stages_environment(play):
    seen = []

    def python_for(env):
        seen.append(env)
        return sys.executable
    _run([Stage("s", commands=(_py("pass"),), inputs=(), outputs=(), env="smplx")], play, python_for=python_for)
    assert seen == ["smplx"]


def test_code_files_include_the_package_modules_a_script_imports(tmp_path):
    files = rn.code_files(Path("scripts/08d_field_offset.py"))
    names = {f.as_posix() for f in files}
    assert "scripts/08d_field_offset.py" in names
    assert any(n.startswith("nfl_gsplat/") for n in names)
    assert all(not n.startswith("nfl_gsplat/pipeline/") for n in names)
