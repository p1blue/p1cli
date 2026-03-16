import logging

import cyclopts

from p1cli.p1cli_python import python as python_cmd

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s: %(message)s",
)

app = cyclopts.App()


@app.command
def python(
    package: str,
    signature: bool = True,
    docstrings: bool = True,
    context: bool = False,
    regex: str | None = None,
    json_output: bool = False,
) -> None:
    """Query Python package signatures and documentation in place.

    Flags (use --no-* to disable):
      --signature / --no-signature   Display function/class signatures
      --docstrings / --no-docstrings Display docstrings
      --context / --no-context      Display .p1cli context file
      --json-output / --no-json-output Output as JSON
    """
    python_cmd(
        package=package,
        signature=signature,
        docstrings=docstrings,
        context=context,
        regex=regex,
        json_output=json_output,
    )


if __name__ == "__main__":
    app()
