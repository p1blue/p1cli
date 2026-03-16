# Usage

## Basic Commands

### Query a Package

```bash
uv run p1cli python polars
```

Output:
```markdown
### Class
DataFrame(data=None, schema=None, ...)

    Two-dimensional data structure representing data as a table with rows and columns.

### Function
concat(objs, ...)

    Concatenate DataFrames, Series, or LazyFrames vertically or horizontally.
```

### List Submodules

```bash
uv run p1cli python polars --ls
```

### Query a Submodule

```bash
uv run p1cli python polars.series
uv run p1cli python fastapi.cli
```

## Flags

| Flag | Description |
|------|-------------|
| `--ls` | List available submodules |
| `--signature / --no-signature` | Display signatures (default: on) |
| `--docstrings / --no-docstrings` | Display docstrings (default: on) |
| `--regex <pattern>` | Filter by regex |
| `--json-output` | Output as JSON |
| `--context` | Show CONTEXT.p1cli files |

## Examples

### Filter with Regex

```bash
uv run p1cli python polars --regex "^Data"
```

### JSON Output (for agents)

```bash
uv run p1cli python polars --json-output
```

### Show Context Files

```bash
uv run p1cli python polars --context
```

## Package Support

p1cli supports:
- **Directory modules** — `polars.series`
- **File modules** — `fastapi.cli` (maps to `cli.py`)
- **Nested submodules** — any depth

## Agent Workflow

```bash
# 1. Discover what's available
uv run p1cli python requests --ls

# 2. Get overview with context
uv run p1cli python requests.api --context

# 3. Deep dive into specific functions
uv run p1cli python requests.api --regex "^get"
```
