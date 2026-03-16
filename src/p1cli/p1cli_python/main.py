import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any

import cyclopts

from .docstring import extract_docstrings
from .signature import extract_signatures

logger = logging.getLogger(__name__)


def find_package_in_venv(package_name: str, venv_path: Path) -> Path | None:
    site_packages = (
        venv_path
        / "lib"
        / f"python{sys.version_info.major}.{sys.version_info.minor}"
        / "site-packages"
    )
    if not site_packages.exists():
        return None

    parts = package_name.split(".")
    base_name = parts[0].replace("-", "_")

    pkg_dirs = [
        d
        for d in site_packages.iterdir()
        if d.is_dir() and not d.name.endswith(".dist-info")
    ]

    parent_path = None
    for d in pkg_dirs:
        if d.name.replace("-", "_") == base_name:
            parent_path = d
            break
        if d.name.startswith(base_name + "-"):
            parent_path = d
            break

    if parent_path is None:
        return None

    if len(parts) == 1:
        return parent_path

    current_path = parent_path
    for part in parts[1:]:
        next_path = current_path / part
        if next_path.exists() and next_path.is_dir():
            current_path = next_path
        else:
            py_file = current_path / f"{part}.py"
            if py_file.exists() and py_file.is_file():
                return py_file
            return None

    return current_path


def get_package_path(package_name: str) -> Path | None:
    try:
        result = subprocess.run(
            ["uv", "tree", "--depth", "1"],
            capture_output=True,
            text=True,
            check=True,
        )
        for line in result.stdout.splitlines():
            if package_name in line:
                venv_path = Path.cwd() / ".venv"
                if venv_path.exists():
                    return find_package_in_venv(package_name, venv_path)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return None


def resolve_package(package_name: str) -> Path | None:
    path = get_package_path(package_name)
    if path:
        return path
    venv_path = Path.cwd() / ".venv"
    if venv_path.exists():
        path = find_package_in_venv(package_name, venv_path)
        if path:
            return path
    return None


def get_module_from_package(package_name: str) -> Any:
    parts = package_name.split(".")
    if len(parts) == 1:
        return __import__(package_name)
    pkg = __import__(parts[0])
    for part in parts[1:]:
        pkg = getattr(pkg, part)
    return pkg


def load_module(module_path: Path, module_name: str) -> Any | None:
    try:
        import importlib

        if module_path.is_file():
            spec = importlib.util.spec_from_file_location(module_name, str(module_path))
        else:
            spec = importlib.util.spec_from_file_location(
                module_name, str(module_path / "__init__.py")
            )

        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            return module
    except Exception as e:
        logger.debug(f"Failed to import module from {module_path}: {e}")

    try:
        import importlib

        return importlib.import_module(module_name)
    except Exception as e2:
        logger.debug(f"Failed to import module {module_name}: {e2}")
        return None


def find_p1cli_file(module_path: Path) -> Path | None:
    for parent in [module_path] + list(module_path.parents):
        p1cli_file = parent / ".p1cli"
        if p1cli_file.exists():
            return p1cli_file
    return None


def load_p1cli_context(p1cli_path: Path) -> str | None:
    try:
        return p1cli_path.read_text()
    except Exception as e:
        logger.error(f"Failed to read .p1cli file: {e}")
        return None


def list_submodules(package_path: Path) -> list[str]:
    submodules = []
    for item in package_path.iterdir():
        if item.is_file():
            if item.suffix == ".py" and not item.name.startswith("_"):
                submodules.append(item.stem)
        elif item.is_dir():
            init_file = item / "__init__.py"
            if init_file.exists() and not item.name.startswith("_"):
                submodules.append(item.name)
    return sorted(submodules)


python_app = cyclopts.App()


@python_app.command
def ls(
    package: str,
    json_output: bool = False,
) -> None:
    """List available submodules in a package."""
    package_path = resolve_package(package)
    if not package_path:
        print(f"Error: Package '{package}' not found in .venv", file=sys.stderr)
        sys.exit(1)

    submodules = list_submodules(package_path)

    if json_output:
        print(json.dumps({"submodules": submodules}, indent=2))
    else:
        for sm in submodules:
            print(sm)


@python_app.default
def python(
    package: str,
    signature: bool = True,
    docstrings: bool = True,
    context: bool = False,
    regex: str | None = None,
    json_output: bool = False,
) -> None:
    """Query Python package signatures and documentation in place.

    Flags (use --no-* to disable):
      --signature / --no-signature   Display function/class signatures
      --docstrings / --no-docstrings Display docstrings
      --context / --no-context      Display .p1cli context file
      --json-output / --no-json-output Output as JSON
    """
    if not any([signature, docstrings, context]):
        signature = True
        docstrings = True

    package_path = resolve_package(package)
    if not package_path:
        print(f"Error: Package '{package}' not found in .venv", file=sys.stderr)
        sys.exit(1)

    results = {}
    p1cli_path = None
    if context:
        p1cli_path = find_p1cli_file(package_path)
        if p1cli_path:
            results[".p1cli"] = {"context": load_p1cli_context(p1cli_path)}

    if signature or docstrings:
        module = load_module(package_path, package)
        if module is None:
            print(f"Error: Could not load module '{package}'", file=sys.stderr)
            sys.exit(1)

        if signature:
            results["signatures"] = extract_signatures(module, regex)
        if docstrings:
            results["docstrings"] = extract_docstrings(module, regex)

    if json_output:
        print(json.dumps(results, indent=2))
    else:
        if ".p1cli" in results:
            print(f"=== .p1cli Context ({p1cli_path}) ===")
            print(results[".p1cli"]["context"])
            print()
        if "signatures" in results:
            print(f"=== {package} ===")
            for name, sig in results["signatures"].items():
                print(f"{name}{sig}")
                if (
                    docstrings
                    and "docstrings" in results
                    and name in results["docstrings"]
                ):
                    doc = results["docstrings"][name]
                    if doc:
                        first_line = doc.split("\n")[0][:80]
                        print(f"    {first_line}")
