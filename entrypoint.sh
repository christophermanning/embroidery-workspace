#!/bin/bash

# needed to dynamically load pattern modules
export PYTHONPATH=$(find /src/patterns/* -maxdepth 0 -type d -not -path \"*pycache*\" | paste -sd:)

exec "$@"
