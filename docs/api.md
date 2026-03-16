# API Reference

## CLI Commands

### python

Query Python package signatures and documentation.

```bash
uv run p1cli python <package> [options]
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `package` | str | required | Package name to query |
| `--ls` | flag | false | List submodules |
| `--signature` | flag | true | Show signatures |
| `--docstrings` | flag | true | Show docstrings |
| `--regex` | str | None | Filter by regex |
| `--context` | flag | false | Show context files |
| `--json-output` | flag | false | JSON output |

## Python API

### resolve_package

Find the path to a package in `.venv`.

```python
from p1cli.p1cli_python import resolve_package

path = resolve_package("polars")
# => Path to polars package
```

### load_module

Load a Python module for inspection.

```python
from p1cli.p1cli_python import load_module

module = load_module(path, "polars")
# => Loaded module object
```

### extract_signatures

Extract all signatures from a module.

```python
from p1cli.p1cli_python.signature import extract_signatures

sigs = extract_signatures(module)
# => {"DataFrame": "(data=None, ...)", ...}
```

### extract_docstrings

Extract all docstrings from a module.

```python
from p1cli.p1cli_python.docstring import extract_docstrings

docs = extract_docstrings(module)
# => {"DataFrame": "Two-dimensional data structure...", ...}
```

## Output Formats

### Text Output (default)

```markdown
### Class
DataFrame(data=None, schema=None)

    Two-dimensional data structure...

### Function
concat(objs, ...)

    Concatenate DataFrames...
```

### JSON Output

```json
{
  "grouped": {
    "Class": [
      {"name": "DataFrame", "signature": "(...)", "docstring": "..."}
    ],
    "Function": [
      {"name": "concat", "signature": "(...)", "docstring": "..."}
    ]
  }
}
```
