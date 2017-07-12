#!/usr/bin/env bash
SRC_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
${SRC_PATH}/src/scrape.py "$@"