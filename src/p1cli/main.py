import logging

import cyclopts

from p1cli.p1cli_python.main import resolve_package, load_module
from p1cli.p1cli_python.main import find_p1cli_file, load_p1cli_context, list_submodules
from p1cli.p1cli_python.signature import extract_signatures
from p1cli.p1cli_python.docstring import extract_docstrings

import json
import sys

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s: %(message)s",
)

app = cyclopts.App()


@app.command
def python(
    package: str,
    ls: bool = False,
    signature: bool = True,
    docstrings: bool = True,
    context: bool = False,
    regex: str | None = None,
    json_output: bool = False,
) -> None:
    """Query Python package signatures and documentation in place.

    Flags (use --no-* to disable):
      --ls / --no-ls             List available submodules
      --signature / --no-signature   Display function/class signatures
      --docstrings / --no-docstrings Display docstrings
      --context / --no-context      Display .p1cli context file
      --json-output / --no-json-output Output as JSON
    """
    package_path = resolve_package(package)
    if not package_path:
        print(f"Error: Package '{package}' not found in .venv", file=sys.stderr)
        sys.exit(1)

    if ls:
        submodules = list_submodules(package_path)
        if json_output:
            print(json.dumps({"submodules": submodules}, indent=2))
        else:
            for sm in submodules:
                print(sm)
        return

    if not any([signature, docstrings, context]):
        signature = True
        docstrings = True

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


if __name__ == "__main__":
    app()
