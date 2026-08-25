#!/bin/sh
# One-click launcher for the pathconv GUI on Linux.
# Requires pathconv to be installed first (pipx install / pip install .),
# which puts the `pathconv` GUI command on your PATH.
if ! command -v pathconv >/dev/null 2>&1; then
    echo "pathconv is not installed. Install it first, e.g.:" >&2
    echo "    pipx install git+https://github.com/nghiadang391/pathconv.git" >&2
    exit 1
fi
exec pathconv "$@"
