#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
workflow_root="$(cd -- "$script_dir/../.." && pwd)"

cd "$workflow_root"

exec clojure \
  -Sdeps '{:paths [".agents/vocabulary-preview/src" ".agents/vocabulary-preview/test"]}' \
  -M \
  -e "(require '[clojure.test :as test]
               'vocabulary-estimation.preview-html-test)
      (let [{:keys [fail error]}
            (test/run-tests 'vocabulary-estimation.preview-html-test)]
        (System/exit (if (zero? (+ fail error)) 0 1)))"
