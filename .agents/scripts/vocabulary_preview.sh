#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
workflow_root="$(cd -- "$script_dir/../.." && pwd)"
publication_root="$workflow_root/clojurecivitas.github.io"
preview_dependency="$workflow_root/.agents/vocabulary-preview"

cd "$publication_root"

exec clojure \
  -Sdeps "{:deps {local/vocabulary-preview {:local/root \"$preview_dependency\"}}}" \
  -M:dev \
  -m vocabulary-estimation.preview \
  "$@"
