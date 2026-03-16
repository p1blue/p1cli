# TODO - p1cli

## Done
- [x] Set up basic CLI structure with cyclopts
- [x] Implement package discovery via uv tree / site-packages scanning
- [x] Implement --signature flag to inspect public functions/classes
- [x] Implement --docstrings flag  
- [x] Implement --regex filter flag
- [x] Implement --json-output flag
- [x] Implement --context flag and .p1cli file support
- [x] Write comprehensive pytest tests (31 tests)
- [x] Final verification

## Future improvements
- Add support for submodule inspection (e.g., polars.dataframes)
- Add short flags (-s, -d, etc.)
- Improve signature formatting for complex types
- Add support for other package managers (pip, poetry)
