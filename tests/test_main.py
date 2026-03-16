import pytest
from pathlib import Path
import sys
import subprocess

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from p1cli.p1cli_python.signature import is_public, get_signature, extract_signatures
from p1cli.p1cli_python.docstring import get_docstring, extract_docstrings
from p1cli.p1cli_python import (
    find_package_in_venv,
    resolve_package,
    find_p1cli_file,
    load_p1cli_context,
)


class TestIsPublic:
    def test_public_names(self):
        assert is_public("foo") is True
        assert is_public("DataFrame") is True
        assert is_public("my_function") is True

    def test_private_names(self):
        assert is_public("_foo") is False
        assert is_public("_private") is False

    def test_dunder_names(self):
        assert is_public("__init__") is False
        assert is_public("__name__") is False
        assert is_public("__class__") is False


class TestGetSignature:
    def test_simple_function(self):
        def foo(x, y):
            pass

        sig = get_signature(foo)
        assert sig == "(x, y)"

    def test_function_with_defaults(self):
        def foo(x, y=1, z="hello"):
            pass

        sig = get_signature(foo)
        assert "x" in sig
        assert "y=1" in sig
        assert "z=" in sig

    def test_function_with_args_kwargs(self):
        def foo(*args, **kwargs):
            pass

        sig = get_signature(foo)
        assert sig == "(*args, **kwargs)"

    def test_class_with_init(self):
        class Foo:
            def __init__(self, x, y=1):
                pass

        sig = get_signature(Foo)
        assert "x" in sig
        assert "y=1" in sig

    def test_non_callable(self):
        sig = get_signature(42)
        assert sig == "()"


class TestGetDocstring:
    def test_function_with_docstring(self):
        def foo():
            """This is a docstring."""
            pass

        doc = get_docstring(foo)
        assert doc == "This is a docstring."

    def test_class_with_docstring(self):
        class Foo:
            """Class docstring."""

            pass

        doc = get_docstring(Foo)
        assert doc == "Class docstring."

    def test_no_docstring(self):
        def foo():
            pass

        doc = get_docstring(foo)
        assert doc is None


class TestFindPackageInVenv:
    def test_find_polars(self, tmp_path):
        venv_path = Path.cwd() / ".venv"
        if venv_path.exists():
            result = find_package_in_venv("polars", venv_path)
            assert result is not None
            assert "polars" in result.name.lower()

    def test_find_fastapi(self, tmp_path):
        venv_path = Path.cwd() / ".venv"
        if venv_path.exists():
            result = find_package_in_venv("fastapi", venv_path)
            assert result is not None
            assert "fastapi" in result.name.lower()

    def test_nonexistent_package(self, tmp_path):
        venv_path = Path.cwd() / ".venv"
        if venv_path.exists():
            result = find_package_in_venv("nonexistent_package_xyz", venv_path)
            assert result is None


class TestResolvePackage:
    def test_resolve_polars(self):
        result = resolve_package("polars")
        assert result is not None
        assert "polars" in result.name.lower()

    def test_resolve_fastapi(self):
        result = resolve_package("fastapi")
        assert result is not None
        assert "fastapi" in result.name.lower()

    def test_resolve_nonexistent(self):
        result = resolve_package("nonexistent_package_xyz")
        assert result is None


class TestFindP1cliFile:
    def test_no_p1cli_file(self, tmp_path):
        result = find_p1cli_file(tmp_path)
        assert result is None

    def test_p1cli_in_current_dir(self, tmp_path):
        p1cli = tmp_path / ".p1cli"
        p1cli.write_text("test content")
        result = find_p1cli_file(tmp_path)
        assert result == p1cli

    def test_p1cli_in_parent_dir(self, tmp_path):
        p1cli = tmp_path / ".p1cli"
        p1cli.write_text("test content")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        result = find_p1cli_file(subdir)
        assert result == p1cli


class TestLoadP1cliContext:
    def test_load_existing_file(self, tmp_path):
        p1cli = tmp_path / ".p1cli"
        p1cli.write_text("test content")
        result = load_p1cli_context(p1cli)
        assert result == "test content"

    def test_load_nonexistent_file(self, tmp_path):
        p1cli = tmp_path / "nonexistent"
        result = load_p1cli_context(p1cli)
        assert result is None


class TestInspectModule:
    def test_inspect_polars(self):
        path = resolve_package("polars")
        assert path is not None
        from p1cli.p1cli_python import load_module

        module = load_module(path, "polars")
        assert module is not None
        sigs = extract_signatures(module)
        assert len(sigs) > 0
        assert "DataFrame" in sigs

    def test_inspect_with_regex(self):
        path = resolve_package("polars")
        assert path is not None
        from p1cli.p1cli_python import load_module

        module = load_module(path, "polars")
        assert module is not None
        sigs = extract_signatures(module, regex=r"^Data")
        assert "DataFrame" in sigs
        assert "DataType" in sigs

    def test_inspect_signature_only(self):
        path = resolve_package("polars")
        assert path is not None
        from p1cli.p1cli_python import load_module

        module = load_module(path, "polars")
        assert module is not None
        sigs = extract_signatures(module)
        assert len(sigs) > 0
        assert "DataFrame" in sigs

    def test_inspect_docstrings_only(self):
        path = resolve_package("polars")
        assert path is not None
        from p1cli.p1cli_python import load_module

        module = load_module(path, "polars")
        assert module is not None
        docs = extract_docstrings(module)
        assert len(docs) > 0


class TestCLI:
    def test_cli_polars(self):
        result = subprocess.run(
            ["python", "-m", "p1cli.main", "python", "polars"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 0
        assert "polars" in result.stdout.lower()
        assert "DataFrame" in result.stdout

    def test_cli_fastapi(self):
        result = subprocess.run(
            ["python", "-m", "p1cli.main", "python", "fastapi"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 0
        assert "fastapi" in result.stdout.lower()
        assert "FastAPI" in result.stdout

    def test_cli_regex_filter(self):
        result = subprocess.run(
            ["python", "-m", "p1cli.main", "python", "polars", "--regex", "^Data"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 0
        assert "DataFrame" in result.stdout
        assert "DataType" in result.stdout

    def test_cli_json_output(self):
        result = subprocess.run(
            ["python", "-m", "p1cli.main", "python", "polars", "--json-output"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 0
        assert result.stdout.startswith("{")
        assert '"signatures"' in result.stdout

    def test_cli_not_found(self):
        result = subprocess.run(
            ["python", "-m", "p1cli.main", "python", "nonexistent_package_xyz"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result.returncode == 1
        assert "not found" in result.stderr.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
