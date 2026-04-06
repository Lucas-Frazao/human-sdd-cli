"""Tests for CLI commands (offline/no-AI mode)."""

import tempfile
from pathlib import Path

from click.testing import CliRunner

from human_sdd_cli.cli.main import cli


class TestInitCommand:
    def test_init_creates_structure(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(cli, ["init", "--path", tmpdir, "--name", "test-project"])
            assert result.exit_code == 0
            root = Path(tmpdir)
            assert (root / ".sdd").exists()
            assert (root / "docs" / "constitution.md").exists()
            assert (root / "docs" / "philosophy.md").exists()
            assert (root / "docs" / "workflow.md").exists()
            assert (root / "specs").is_dir()
            assert (root / "templates").is_dir()

    def test_init_idempotent(self):
        """Running init twice should not overwrite existing constitution."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            runner.invoke(cli, ["init", "--path", tmpdir, "--name", "test"])
            # Modify constitution
            const_path = Path(tmpdir) / "docs" / "constitution.md"
            const_path.write_text("CUSTOM CONSTITUTION")
            # Run again
            result = runner.invoke(cli, ["init", "--path", tmpdir, "--name", "test"])
            assert result.exit_code == 0
            assert const_path.read_text() == "CUSTOM CONSTITUTION"


class TestSpecifyCommand:
    def test_specify_no_ai(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            # Init first
            runner.invoke(cli, ["init", "--path", tmpdir, "--name", "test"])
            # Specify
            result = runner.invoke(cli, [
                "specify",
                "--idea", "A calculator that adds numbers",
                "--path", tmpdir,
                "--no-ai",
            ])
            assert result.exit_code == 0
            specs_dir = Path(tmpdir) / "specs"
            feature_dirs = list(specs_dir.iterdir())
            assert len(feature_dirs) == 1
            assert (feature_dirs[0] / "spec.md").exists()

    def test_specify_auto_numbering(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            runner.invoke(cli, ["init", "--path", tmpdir, "--name", "test"])
            # First feature
            runner.invoke(cli, [
                "specify", "--idea", "Feature A", "--path", tmpdir, "--no-ai",
            ])
            # Second feature
            runner.invoke(cli, [
                "specify", "--idea", "Feature B", "--path", tmpdir, "--no-ai",
            ])
            specs_dir = Path(tmpdir) / "specs"
            dirs = sorted(d.name for d in specs_dir.iterdir() if d.is_dir())
            assert dirs[0].startswith("001-")
            assert dirs[1].startswith("002-")


class TestCheckNoCodeCommand:
    def test_clean_file_passes(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            specs = root / "specs" / "001-test"
            specs.mkdir(parents=True)
            (specs / "spec.md").write_text("# Spec\n\nJust prose, no code.\n")
            result = runner.invoke(cli, [
                "check-no-code", "--feature", "001-test", "--path", tmpdir,
            ])
            assert result.exit_code == 0
            assert "PASSED" in result.output

    def test_dirty_file_fails(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            specs = root / "specs" / "001-test"
            specs.mkdir(parents=True)
            (specs / "spec.md").write_text("# Spec\n\n```python\nprint('hi')\n```\n")
            result = runner.invoke(cli, [
                "check-no-code", "--feature", "001-test", "--path", tmpdir,
            ])
            assert result.exit_code != 0
            assert "FAILED" in result.output


class TestTraceCommand:
    def test_trace_report(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            feature = root / "specs" / "001-auth"
            feature.mkdir(parents=True)
            (feature / "spec.md").write_text(
                "# Functional Requirements\n- REQ-001: Login\n- REQ-002: Logout\n"
            )
            (feature / "tasks.md").write_text(
                "# Tasks\n- [x] TASK-001: Do login (traces: REQ-001)\n"
            )
            result = runner.invoke(cli, [
                "trace", "--feature", "001-auth", "--path", tmpdir,
            ])
            assert result.exit_code == 0
            assert (feature / "traceability.md").exists()
