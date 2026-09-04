# py-pilecore
Public python SDK for the CEMS PileCore web-API

[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Coverage Status](https://coveralls.io/repos/github/cemsbv/py-pilecore/badge.svg)](https://coveralls.io/github/cemsbv/py-pilecore)


This repository is created by [CEMS BV](https://cemsbv.nl/) and is a public python wrapper around the CEMS [PileCore web-API](https://nuclei.cemsbv.io/#/pilecore/api).

# Installation

To install a package in this repository run:

`$ pip install py-pilecore`

Or, in a [uv](https://docs.astral.sh/uv/) project:

`$ uv add py-pilecore`


## ENV VARS

To use `py-pilecore` add the follow ENV vars to your environment. Or provide them when asked.

```
* NUCLEI_TOKEN
    - Your NUCLEI user token
```

You can obtain your `NUCLEI_TOKEN` on [NUCLEI](https://nuclei.cemsbv.io/#/). 
Go to `personal-access-tokens` and create a new user token.

# Contribution

## Environment

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. The
pinned dependency set lives in `uv.lock`, which is committed to the repository.

Create the development environment (a `.venv` in the repository root) with every
optional dependency group installed:

```bash
uv sync --all-extras
```

That installs the project itself in editable mode as well. Prefix commands with
`uv run` to run them inside that environment without activating it, or activate it
the usual way with `source .venv/bin/activate`.

The test matrix covers Python 3.11 through 3.13. `uv` picks an interpreter that
satisfies `requires-python` automatically; pass `--python 3.11` to `uv sync` to
develop against the oldest supported version.

## Documentation

Build the docs:

```bash
uv sync --extra docs
uv run sphinx-build -b html docs public
```

## Format

We format our code with black and isort.

```bash
uv run black --config "pyproject.toml" src/pypilecore tests notebooks
uv run isort --settings-path "pyproject.toml" src/pypilecore tests notebooks
```

## Lint

To maintain code quality we use the [GitHub super-linter](https://github.com/super-linter/super-linter).

### Reproduce the full CI lint job (Docker)

The CI lint job runs the super-linter Docker image. To reproduce it exactly,
run the `run_super_linter.sh` bash script from the root directory (requires
Docker):

```bash
./run_super_linter.sh
```

Like CI, this lints only the files changed against `main` and auto-fixes
black/isort formatting in place.

### Run the Python linters without Docker

The active Python linters are pinned in the `lint` optional-dependency group.
CI lints only the Python files changed against `main` (and excludes `tests/`),
so collect that file list first, then run each linter against it:

```bash
uv sync --extra lint
FILES=$(git diff --name-only main...HEAD -- '*.py' | grep -v '^tests/')

uv run black --check --config "pyproject.toml" $FILES
uv run isort --check-only --settings-path "pyproject.toml" $FILES
uv run flake8 --config ".flake8" $FILES
```

`mypy` needs a caveat: super-linter runs it **without installing the project**,
so unresolved third-party imports (matplotlib, numpy, pandas) become `Any` and
their errors disappear. Reproduce that with a throwaway environment that has
only `mypy` in it:

```bash
uv run --isolated --no-project --with mypy==2.1.0 \
  mypy --config-file "pyproject.toml" --no-install-types $FILES
```

Running `mypy` in a fully-installed environment reports extra import-related
errors that CI does not, so the Docker script above remains authoritative.

## UnitTest

Test the software with the use of coverage:

```bash
uv sync --extra test
uv run coverage run -m pytest
```

## Dependencies

Direct dependencies and their version ranges are declared in `pyproject.toml`.
The fully resolved set is locked in `uv.lock`, which is committed and must stay
in sync with `pyproject.toml`.

Refresh the lock file after editing `pyproject.toml`:

```bash
uv lock
```

Update everything to the newest versions allowed by the declared ranges:

```bash
uv lock --upgrade
```

Update a single package:

```bash
uv lock --upgrade-package <name>
```

Install exactly what the lock file says, failing if it is out of date (this is
what CI does):

```bash
uv sync --locked --all-extras
```

Renovate also maintains `uv.lock` automatically: it bumps the ranges in
`pyproject.toml` and refreshes the lock in the same pull request, and
`lockFileMaintenance` periodically refreshes transitive dependencies.
