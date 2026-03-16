import inspect
from typing import Any


def is_public(name: str) -> bool:
    return not name.startswith("_")


def get_signature(obj: Any) -> str:
    try:
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


def extract_signatures(module: Any, regex: str | None = None) -> dict[str, str]:
    import re

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
        sig = get_signature(obj)
        if sig:
            results[name] = sig
    return results


def extract_signatures_grouped(
    module: Any, regex: str | None = None
) -> dict[str, list[dict]]:
    import re

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
        sig = get_signature(obj)
        if sig:
            groups[obj_type].append({"name": name, "signature": sig})

    return {k: v for k, v in groups.items() if v}
