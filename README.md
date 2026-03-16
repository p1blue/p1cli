# p1cli - Package as a CLI

This project aims to introduce the concept of PaaC, Package as a CLI. Query Python package signatures and documentation directly from your `.venv` — no internet connection required, no extra mcp setup. Built for agents that need accurate, in-place package introspection.

## Why?

Agents need good context to succeed. Currently, this is solved with:
- **MCP servers** - extra setup, token costs, potential drift from actual code
- **External docs** - may be outdated, requires internet

p1cli takes a different approach: query the actual code in your `.venv`. What you see is what actually exists — no abstraction layers, no sync issues.

## Install

```bash
uv pip install -e .
```

## Agent Skill

p1cli is also available as an installable skill for AI agents:

```bash
npx skills add p1blue/p1cli@p1cli
```

This enables agents to use p1cli commands directly.

## Quick Usage

```bash
# Query a package
uv run p1cli python polars

# Filter with regex
uv run p1cli python polars --regex "^Data"

# List submodules
uv run p1cli python polars --ls

# Query a submodule
uv run p1cli python polars.series

# JSON output (great for agents)
uv run p1cli python polars --json-output
```

## Flags

| Flag | Description |
|------|-------------|
| `--ls` | List available submodules |
| `--signature / --no-signature` | Display function/class signatures (default: on) |
| `--docstrings / --no-docstrings` | Display docstrings (default: on) |
| `--regex <pattern>` | Filter by regex |
| `--json-output` | Output as JSON |
| `--context` | Show `.p1cli` context file if present |

## License

MIT © 2026 p1blue

## Disclaimers

This is mainly vibe coded to quickly try out this and test the idea. So far, it helps me a lot with agent workflows, this is a global intuition that I have. It could be useful to run benchmarks on this.

Also, I'm currently working almost exclusively with python, and I don't have much time to spend for now, so only python is available. Feel free to implement other languages if you want to
