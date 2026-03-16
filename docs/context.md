# Context Files

Context files provide human-written hints to help AI agents navigate packages. The `CONTEXT.p1cli` format is a lightweight proposal for adding package-level documentation that agents can read alongside signatures and docstrings.

## Why Context Files?

When working with a new package, AI agents face a challenge: signatures and docstrings tell you *how* to use a function, but not *why* it exists or how it fits into the bigger picture. Context files bridge this gap by providing:

- **High-level overview** — What the package/module does
- **Architecture hints** — How it's organized
- **Navigation guidance** — Key entry points
- **Usage patterns** — Common workflows

They intentionally avoid duplicating what's already in signatures and docstrings.

## The CONTEXT.p1cli Format

The `.p1cli` extension indicates a human-written context file for p1cli. The naming follows the pattern:
- `CONTEXT.p1cli` — Package/module context
- Future: `.p1cli` files for specific guidance

This format is intentionally simple—just markdown—so it's easy for maintainers to add.

Then, using the `--context` flag with p1cli will include the content of these files in the output, giving agents richer information to work with.

## How It Works

When you use `--context`, p1cli searches for `CONTEXT.p1cli` files in your package and merges them:

1. Start in the package directory (e.g., `polars/`)
2. Search each parent directory up to the root
3. Merge all found context files

This hierarchical approach means submodules inherit context from their parent packages—a sub-module of `polars` will get both its own context and `polars`' context.

## Creating Context Files

Place a `CONTEXT.p1cli` file in your package directory:

```markdown
# My Package

## What this package does

A brief overview...

## Key modules

- `client.py` - Main client
- `models.py` - Data models

## Common workflows

1. Initialize client
2. Call API methods
3. Handle responses
```

## Example Context for p1cli

```markdown
# p1cli_python

Core module for resolving and loading Python packages from `.venv`.

## How it works

1. resolve_package() - Entry point
2. find_package_in_venv() - Scans site-packages
3. load_module() - Uses importlib

## Package resolution logic

- If package starts with "p1cli.", look in src/
- Otherwise, use uv tree to find packages
- Supports directory and file modules
```

## What to Include

Context files should contain:
- **High-level overview** — What the package/module does
- **Architecture** — How it's organized
- **Navigation hints** — Key entry points
- **Common patterns** — Typical usage patterns

They should NOT duplicate what's in signatures/docstrings.

## For Package Maintainers

Add a `CONTEXT.p1cli` to your package to help AI agents understand your code better. It's especially useful for:

- Complex packages with many modules
- Internal/undocumented packages
- Helping agents understand your coding patterns

## The .p1cli Proposal

This is an experimental approach to providing AI-agent-friendly documentation. The key ideas:

1. **Lightweight** — Just markdown files, no special tooling
2. **Hierarchical** — Context flows from parent to child
3. **Non-duplicative** — Supplements, doesn't replace, signatures/docstrings
4. **Human-first** — Written by humans for humans, readable by agents

Feedback and contributions welcome at https://github.com/p1blue/p1cli
