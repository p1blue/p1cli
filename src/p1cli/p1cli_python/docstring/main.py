import re
from typing import Any


def is_public(name: str) -> bool:
    return not name.startswith("_")


def get_docstring(obj: Any) -> str | None:
    try:
        doc = getattr(obj, "__doc__", None)
        if doc:
            return doc.strip()
    except Exception:
        pass
    return None


def extract_docstrings(module: Any, regex: str | None = None) -> dict[str, str]:
    pattern = re.compile(regex) if regex else None
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
        doc = get_docstring(obj)
        if doc:
            results[name] = doc
    return results
