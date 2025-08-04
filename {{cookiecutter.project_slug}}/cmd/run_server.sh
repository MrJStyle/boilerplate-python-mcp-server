#!/bin/bash

# Enable .env
set -a
. ./.env
set +a

set -x

exec uv run {{ cookiecutter.package_entrypoint }} --transport streamable-http --host 0.0.0.0 --port 9080
