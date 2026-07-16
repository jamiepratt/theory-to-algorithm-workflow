#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
workflow_root="$(cd -- "$script_dir/../.." && pwd)"
publication_root="$workflow_root/clojurecivitas.github.io"
test_deps_file="$workflow_root/.agents/vocabulary-tests.edn"

case "${1:-}" in
  clj)
    test_alias="workflow-vocab-test-clj"
    ;;
  cljs)
    test_alias="workflow-vocab-test-cljs"
    ;;
  *)
    echo "Usage: $0 <clj|cljs>" >&2
    exit 2
    ;;
esac

cd "$publication_root"
test_deps="$(<"$test_deps_file")"
exec clojure -Sdeps "$test_deps" -M:"$test_alias"
