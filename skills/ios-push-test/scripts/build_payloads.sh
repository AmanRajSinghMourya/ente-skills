#!/usr/bin/env bash
# Build the three Apple Push Notifications Console payloads for one phone.
# usage: build_payloads.sh <base64-public-key> <out-dir>
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
cd "$here/payloads" && go run . "$1" "$2"
