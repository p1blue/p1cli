# Main Purpose

This project aims to implement, for python at least, the concept of PaaC, Package as a CLI. The main problem with agents is that they need good context to successfully fullfill the task. A lot of effort have been spend on building pipelines to achieve this. For package specifically, new layer of abstractions have been created, such as MCP, to query up to date documentation. This is good but not perfect: 
  - Up-to-date documentation means working with an up to date package, which is a good thing to consider but not always possible
  - Set up management, token consumption

This project propose to build, on top of cyclopts, an external cli that will turn every package into a CLI to query right in place signature and documentation. The workflow should be something like:

```bash
uv run p1cli polars
```

And output useful information about polars. To go deeper:

```bash
uv run p1cli polars.dataframes
```


> Important note: polars.dataframes may not exists, this is just an example

and return useful information about this module, and so on

We plan to add a small set of flag to display more information, for instance:

```bash
uv run p1cli polars.dataframes --signature [-s] --docstrings [-d] --context [-c] --regex [-r] --json-output
```

The signature flag will, as mkdocs is doing, inspect every NON PRIVATE NOR PROTECTED function or class within this module and return it as text in the terminal
Docstrings, do this for docstrings
regex is to filter

We can combine flags, like for example:

```bash
uv run p1cli polars.dataframes -sd
```

The --context command, that could be renamed, will go and query every .p1cli that is basically a markdown wrapper. This is a proposition of standard to include in libs for enhancing the performance of this tool. Yml metadata, like default markdown, are going to be useful to provide more information


The cli must be very easy to use for an agent, for self discovery. Good documentation on how to use it.


For the moment, we ll start simple and only support project using uv, meaning that the cli will inspect in the .venv folder the correct package.

I have added polars, fastapi in dev depenencies for u to use. Document what you are doing, and write pytest tests, this is important


Maintain your TODO in in artifacts/TODO.md, and global reasoning/discoveries (dont write too much) on artifacts/REASONING.md. This is important to keep track of your work and to be able to share it with others.
