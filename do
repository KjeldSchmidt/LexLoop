#!/usr/bin/env bash

## quality-gates: Run quality checks for deployment confidence
function task_quality_gates {
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

function task_update_api_schema {
  pushd backend/dev_tools
  uv run python openapi_schema.py
  popd
  npx openapi-typescript backend/dev_tools/openapi.json > frontend/src/api/schema.ts
  ./frontend/do fmt
  rm backend/dev_tools/openapi.json
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
