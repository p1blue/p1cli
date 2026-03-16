# p1cli Documentation

## Overview

p1cli queries Python packages directly from your `.venv` to extract signatures and docstrings. No internet, no MCP, no outdated docs.

## Requirements

- Python 3.13+
- uv (for package management)
- Packages must be installed in `.venv`

## Installation

```bash
uv pip install -e .
```

Or run directly:
```bash
uv run p1cli <command>
```

## Commands

### Query a Package

```bash
uv run p1cli python polars
```

Output:
```
=== polars ===
DataFrame(data=None, schema=None, ...)
    Two-dimensional data structure...
DataType()
    Base class for all Polars...
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

### Filter with Regex

```bash
uv run p1cli python polars --regex "^Data"
```

### JSON Output

```bash
uv run p1cli python polars --json-output
```

## Flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--ls` | | false | List submodules |
| `--signature` | -s | true | Show signatures |
| `--docstrings` | -d | true | Show docstrings |
| `--regex` | -r | | Filter by regex |
| `--json-output` | -j | false | JSON output |
| `--context` | -c | false | Show `.p1cli` file |

## .p1cli Files

Place a `.p1cli` file in a package directory to add custom context:

```bash
echo "# Custom notes" > .venv/lib/python3.13/site-packages/mypackage/.p1cli
uv run p1cli python mypackage --context
```

## For Agents

p1cli is designed for AI agents that need accurate package information:

1. **Run in project context**: The agent must run p1cli from a directory with `.venv`
2. **JSON output**: Use `--json-output` for reliable parsing
3. **Submodule exploration**: Use `--ls` to discover available modules, then query them directly

Example agent workflow:
```bash
# Discover what's available
uv run p1cli python requests --ls

# Query a specific submodule
uv run p1cli python requests.api
```
