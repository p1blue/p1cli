# p1cli — Package as a CLI

**Query Python package signatures and documentation directly from your `.venv` — no internet required.**

p1cli is built for AI agents that need accurate, in-place package introspection. Instead of setting up MCP servers or relying on potentially outdated external docs, query the actual code in your local environment.

## Why p1cli?

| Approach | Pros | Cons |
|----------|------|------|
| **p1cli** | Always accurate, no setup, free | Only works locally |
| **MCP servers** | Rich features | Extra setup, token costs, potential drift |
| **External docs** | Comprehensive | May be outdated, requires internet |

## Quick Example

```bash
# Query a package
uv run p1cli python polars

# List submodules
uv run p1cli python polars --ls

# Query a submodule
uv run p1cli python polars.series

# JSON output for agents
uv run p1cli python polars --json-output
```

## Key Features

- **Local-first** — Queries packages in your `.venv`, no internet needed
- **Agent-optimized** — Clean JSON output for programmatic use
- **Smart grouping** — Classes, functions, methods automatically categorized
- **Context files** — Human-written hints to help agents navigate

## Who is this for?

- **AI agents** that need reliable package information
- **Developers** who want quick access to local package APIs
- **Teams** working offline or with private packages

## Agent Skill

p1cli is available as an installable skill for AI agents:

```bash
npx skills add p1blue/p1cli@p1cli
```

This enables agents to use p1cli commands directly.
