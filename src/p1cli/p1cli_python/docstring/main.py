import inspect
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


def get_object_type(obj: Any) -> str:
    if inspect.isclass(obj):
        return "Class"
    elif inspect.isfunction(obj):
        return "Function"
    elif inspect.ismethod(obj):
        return "Method"
    elif inspect.isbuiltin(obj):
        return "Builtin"
    elif inspect.iscoroutinefunction(obj):
        return "Coroutine"
    else:
        return "Other"


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


def extract_docstrings_grouped(
    module: Any, regex: str | None = None
) -> dict[str, list[dict]]:
    pattern = re.compile(regex) if regex else None
    groups: dict[str, list[dict]] = {
        "Class": [],
        "Function": [],
        "Method": [],
        "Coroutine": [],
        "Builtin": [],
        "Other": [],
    }

    for name in dir(module):
        if not is_public(name):
            continue
        if pattern and not pattern.search(name):
            continue
        try:
            obj = getattr(module, name)
        except Exception:
            continue

        obj_type = get_object_type(obj)
        doc = get_docstring(obj)
        if doc:
            groups[obj_type].append({"name": name, "docstring": doc})

    return {k: v for k, v in groups.items() if v}
