---
name: p1cli
description: Query Python package signatures and documentation from .venv — no internet required. Use this skill when you need to explore Python packages, understand APIs, or get documentation for packages in your local virtual environment.
---

# p1cli - Query Python Packages Locally

This skill helps you use p1cli to explore Python packages directly from your `.venv`

## When to Use This Skill

Use this skill when you need to:
- Explore a Python package's API
- Get function/class signatures
- Read docstrings from installed packages
- Understand package structure
- Query packages for AI agent context

## Installation

```bash
uv tool install p1cli
```

Or run directly:
```bash
uv run p1cli <command>
```

## Core Commands

### Query a package for signatures
```bash
p1cli python <package>
```

### Include docstrings
```bash
p1cli python <package> --docstrings
```

### Query a specific submodule
```bash
p1cli python polars.series
p1cli python fastapi.cli
```

### List package contents
```bash
p1cli python <package> --ls
```

### Use regex to filter
```bash
p1cli python <package> --regex "load.*"
```

### Output as JSON
```bash
p1cli python <package> --json-output
```

### Include human-written context
```bash
p1cli python <package> --context
```

## CONTEXT.p1cli Files

The `.p1cli` format provides human-written context for AI agents. Place `CONTEXT.p1cli` files in your package directories.

**Key principles:**
- High-level overview (not duplicate of docstrings)
- Architecture hints
- Navigation guidance
- Common usage patterns

**Hierarchy:** Context files in parent directories are inherited by submodules.

## Examples

### Get all functions in a module
```bash
p1cli python requests
```

### Get specific class with docstrings
```bash
p1cli python polars.DataFrame --docstrings
```

### Find methods matching a pattern
```bash
p1cli python pandas.DataFrame --regex "to_.*"
```

### List what's available in a package
```bash
p1cli python numpy --ls
```

### Use with --json-output for structured output
```bash
p1cli python fastapi --json-output
```

## For Package Maintainers

Add `CONTEXT.p1cli` files to your packages to help AI agents understand your code:
- What the package does
- Key modules and their purposes
- Common workflows
- Architecture decisions

See https://p1blue.github.io/p1cli/context/ for format details.
