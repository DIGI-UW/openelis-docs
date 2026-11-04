#!/usr/bin/env bash
# Run a docs_hooks.py subcommand. Without python3 the hook does nothing rather than block work.
command -v python3 >/dev/null 2>&1 || exit 0
exec python3 "$(dirname "$0")/docs_hooks.py" "$@"
