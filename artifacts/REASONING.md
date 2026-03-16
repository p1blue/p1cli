# Reasoning - p1cli

## Decisions

1. **Package discovery**: Uses `uv tree` to find installed packages, falls back to scanning `.venv/lib/pythonX.X/site-packages` directly.

2. **Signature extraction**: Uses Python's `inspect.signature()` for callable objects.

3. **Cyclopts flags**: Uses `--no-*` pattern for disabling flags (e.g., `--no-signature`) since cyclopts treats booleans as presence/absence flags with `--no-` prefix.

4. **Context files**: Looks for `.p1cli` files in the package directory or parent directories.

5. **Dist-info filtering**: Excludes `.dist-info` directories when scanning site-packages to get actual package paths.
