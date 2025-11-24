#!/bin/bash

docker run \
--env VALIDATE_ALL_CODEBASE=false \
--env RUN_LOCAL=true \
--env FIX_PYTHON_ISORT=true \
--env FIX_PYTHON_BLACK=true \
--env FIX_YAML_PRETTIER=true \
--env DEFAULT_BRANCH=main \
--env VALIDATE_JSCPD=false \
--env VALIDATE_CSS=false \
--env VALIDATE_BASH=false \
--env VALIDATE_YAML=false \
--env VALIDATE_PYTHON_PYLINT=false \
--env VALIDATE_NATURAL_LANGUAGE=false \
--env VALIDATE_MARKDOWN=false \
--env FILTER_REGEX_EXCLUDE=.*tests/.* \
--env LINTER_RULES_PATH=/ \
--env PYTHON_BLACK_CONFIG_FILE=pyproject.toml \
--env PYTHON_ISORT_CONFIG_FILE=pyproject.toml \
--env PYTHON_MYPY_CONFIG_FILE=pyproject.toml \
--env PYTHON_FLAKE8_CONFIG_FILE=.flake8 \
-v $(pwd):/tmp/lint \
--rm \
ghcr.io/super-linter/super-linter:v8