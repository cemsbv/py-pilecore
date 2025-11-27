#!/bin/bash

docker run \
--env RUN_LOCAL=true \
--env VALIDATE_ALL_CODEBASE=false \
--env FIX_PYTHON_ISORT=true \
--env FIX_PYTHON_BLACK=true \
--env FIX_YAML_PRETTIER=true \
--env DEFAULT_BRANCH=main \
--env-file ".github/super-linter.env" \
--env SAVE_SUPER_LINTER_OUTPUT=true \
--env SAVE_SUPER_LINTER_SUMMARY=true \
-v $(pwd):/tmp/lint \
--rm \
ghcr.io/super-linter/super-linter:latest