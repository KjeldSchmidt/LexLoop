#!/usr/bin/env bash

## quality-gates: Run quality checks for deployment confidence
function task_quality_gates {
  task_check_api_schema
  ./backend/do quality-gates
  ./frontend/do quality-gates
  ./infrastructure/do quality-gates
}

## fmt: Validate formatting
function task_fmt {
  ./backend/do fmt
  ./frontend/do fmt
  ./infrastructure/do fmt
}

## fmt-check: Validate formatting
function task_fmt_check {
  ./backend/do fmt_check
  ./infrastructure/do fmt_check
  ./frontend/do fmt_check
}

## setup: Perform a best-effort repository setup
function task_setup {
  ./backend/do setup
  git config core.hooksPath .githooks
}

## update-api-schema: Regenerate backend/openapi.json and frontend/src/api/schema.ts
function task_update_api_schema {
  # DB_URL is required at import time; schema dump does not connect.
  export DB_URL="${DB_URL:-postgresql+psycopg://schema-check:schema-check@127.0.0.1:5432/schema_check}"
  if [ -f backend/.env ]; then
    set -a
    # shellcheck disable=SC1091
    source backend/.env
    set +a
  fi

  pushd backend/dev_tools >/dev/null
  uv run python openapi_schema.py ../openapi.json
  popd >/dev/null
  (cd frontend && npm exec -- openapi-typescript ../backend/openapi.json -o src/api/schema.ts)
  ./frontend/do fmt
}

## check-api-schema: Fail if committed OpenAPI or schema.ts are stale
function task_check_api_schema {
  local tmp
  tmp=$(mktemp -d)
  # Expand path when setting trap; local tmp is unbound when EXIT runs.
  trap "rm -rf '$tmp'" EXIT

  export DB_URL="${DB_URL:-postgresql+psycopg://schema-check:schema-check@127.0.0.1:5432/schema_check}"
  if [ -f backend/.env ]; then
    set -a
    # shellcheck disable=SC1091
    source backend/.env
    set +a
  fi

  pushd backend/dev_tools >/dev/null
  uv run python openapi_schema.py "$tmp/openapi.json"
  popd >/dev/null

  if ! diff -q backend/openapi.json "$tmp/openapi.json" >/dev/null; then
    echo "backend/openapi.json is stale. Run: ./do update-api-schema" >&2
    diff -u backend/openapi.json "$tmp/openapi.json" >&2 || true
    exit 1
  fi

  (cd frontend && npm exec -- openapi-typescript ../backend/openapi.json -o "$tmp/schema.ts")
  (cd frontend && npx prettier --write --config .prettierrc.json "$tmp/schema.ts" >/dev/null)

  if ! diff -q frontend/src/api/schema.ts "$tmp/schema.ts" >/dev/null; then
    echo "frontend/src/api/schema.ts is stale. Run: ./do update-api-schema" >&2
    diff -u frontend/src/api/schema.ts "$tmp/schema.ts" >&2 || true
    exit 1
  fi

  echo "OpenAPI and schema.ts are up to date ✅"
}

#-------- All task definitions go above this line --------#

# Bash Strict Mode - For details, see
# https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425
set -u     # Raise error when using undefined variables
set -e     # Raise error if any command has a non-zero exit status
# set -x   # Enable this optionally to print every command executed by bash
set -o pipefail  # Prevent pipelines from masking errors

function task_usage {
    echo "Usage: $0"
    sed -n 's/^##//p' <"$0" | column -t -s ':' |  sed -E $'s/^/\t/'
}

cmd=${1:-}
shift || true
resolved_command=$(echo "task_${cmd}" | sed 's/-/_/g')
if [[ "$(LC_ALL=C type -t "${resolved_command}")" == "function" ]]; then
    pushd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null
    ${resolved_command} "$@"
else
    task_usage
    if [ -n "${cmd}" ]; then
      echo "'$cmd' could not be resolved - please use one of the above tasks"
      exit 1
    fi
fi
