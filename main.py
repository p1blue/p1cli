import json
import logging
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import cyclopts

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


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


def find_package_in_venv(package_name: str, venv_path: Path) -> Path | None:
    site_packages = (
        venv_path
        / "lib"
        / f"python{sys.version_info.major}.{sys.version_info.minor}"
        / "site-packages"
    )
    if not site_packages.exists():
        return None
    pkg_dirs = [
        d
        for d in site_packages.iterdir()
        if d.is_dir() and not d.name.endswith(".dist-info")
    ]
    for d in pkg_dirs:
        if d.name.replace("-", "_") == package_name.replace("-", "_"):
            return d
        if d.name.startswith(package_name.replace("-", "_") + "-"):
            return d
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


def is_public(name: str) -> bool:
    return not name.startswith("_")


def get_signature(obj: Any) -> str:
    try:
        import inspect

        if callable(obj):
            sig = inspect.signature(obj)
            params = []
            for name, param in sig.parameters.items():
                if param.kind == inspect.Parameter.POSITIONAL_ONLY:
                    param_str = f"{name}"
                elif param.kind == inspect.Parameter.VAR_POSITIONAL:
                    param_str = f"*{name}"
                elif param.kind == inspect.Parameter.VAR_KEYWORD:
                    param_str = f"**{name}"
                elif param.default is inspect.Parameter.empty:
                    param_str = f"{name}"
                else:
                    param_str = f"{name}={param.default}"
                params.append(param_str)
            return f"({', '.join(params)})"
    except (ValueError, TypeError):
        pass
    return "()"


def get_docstring(obj: Any) -> str | None:
    try:
        doc = getattr(obj, "__doc__", None)
        if doc:
            return doc.strip()
    except Exception:
        pass
    return None


def inspect_module(
    module_path: Path,
    module_name: str,
    signature: bool = False,
    docstrings: bool = False,
    regex: str | None = None,
) -> dict | None:
    module = None
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location(module_name, str(module_path))
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
    except Exception as e:
        logger.debug(f"Failed to import module from {module_path}: {e}")

    if module is None:
        try:
            module = get_module_from_package(module_name)
        except Exception as e2:
            logger.debug(f"Failed to import module {module_name}: {e2}")
            return None

    pattern = None
    if regex:
        pattern = re.compile(regex)

    results = {}
    for name in dir(module):
        if not is_public(name):
            continue
        if pattern and not pattern.search(name):
            continue
        try:
            obj = getattr(module, name)
        except Exception:
            continue
        item_info = {}
        if signature:
            item_info["signature"] = get_signature(obj)
        if docstrings:
            doc = get_docstring(obj)
            if doc:
                item_info["docstring"] = doc
        if item_info:
            results[name] = item_info

    return results


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


app = cyclopts.App()


@app.default
def main(
    package: str,
    signature: bool = True,
    docstrings: bool = True,
    context: bool = False,
    regex: str | None = None,
    json_output: bool = False,
) -> None:
    """Query package signatures and documentation in place.

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
        module_results = inspect_module(
            package_path, package, signature, docstrings, regex
        )
        if module_results:
            results["members"] = module_results

    if json_output:
        import json

        print(json.dumps(results, indent=2))
    else:
        if ".p1cli" in results:
            print(f"=== .p1cli Context ({p1cli_path}) ===")
            print(results[".p1cli"]["context"])
            print()
        if "members" in results:
            print(f"=== {package} ===")
            for name, info in results["members"].items():
                sig = info.get("signature", "")
                print(f"{name}{sig}")
                if docstrings and "docstring" in info:
                    doc = info["docstring"]
                    if doc:
                        first_line = doc.split("\n")[0][:80]
                        print(f"    {first_line}")


if __name__ == "__main__":
    app()
