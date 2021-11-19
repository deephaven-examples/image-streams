#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker build --build-arg TAG=${VERSION:-latest} --tag deephaven-image-streams "${__dir}"
