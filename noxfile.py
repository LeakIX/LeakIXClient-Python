"""Nox sessions for local multi-version testing.

Reproduces the CI test matrix locally. Requires the target Python
interpreters to be available (e.g. via `uv python install 3.11 3.12 3.13
3.14`). CI remains the source of truth; this is for local reproduction.
"""

import nox

nox.options.default_venv_backend = "uv|virtualenv"

PYTHON_VERSIONS = ["3.11", "3.12", "3.13", "3.14"]


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run the test suite on a specific Python version."""
    session.run_install(
        "uv",
        "sync",
        "--group",
        "dev",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("pytest", "tests/")
