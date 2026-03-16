# Installation

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

## Install

```bash
cd /path/to/your/project
uv pip install -e .
```

## Verify

```bash
uv run p1cli --help
```

## Development

Since p1cli queries packages from your `.venv`, developing p1cli itself requires special handling:

```bash
# p1cli resolves "p1cli" from src/ when no .venv package exists
uv run p1cli python p1cli
```

This allows you to test p1cli on itself without installing it.
