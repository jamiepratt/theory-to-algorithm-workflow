#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
workspace="$(cd "$script_dir/../../../.." && pwd)"
repo="$workspace/clojurecivitas.github.io"
src_dir="$repo/src"

if [[ ! -d "$repo/.git" ]]; then
  echo "Civitas repository not found: $repo" >&2
  exit 1
fi

mtime() {
  stat -f %m "$1" 2>/dev/null || stat -c %Y "$1"
}

is_article() {
  local file="$1"
  [[ -f "$file" && "$file" == *.clj ]] && rg -q ':clay' "$file"
}

latest=""
latest_mtime=0

consider() {
  local file="$1"
  local modified
  is_article "$file" || return 0
  modified="$(mtime "$file")"
  if (( modified > latest_mtime )); then
    latest="$file"
    latest_mtime="$modified"
  fi
}

while IFS= read -r -d '' entry; do
  path="${entry:3}"
  if [[ "$path" == *" -> "* ]]; then
    path="${path##* -> }"
  fi
  [[ "$path" == src/* ]] && consider "$repo/$path"
done < <(git -C "$repo" status --porcelain=v1 -z --untracked-files=all)

if [[ -z "$latest" ]]; then
  while IFS= read -r -d '' file; do
    consider "$file"
  done < <(find "$src_dir" -type f -name '*.clj' -print0)
fi

if [[ -z "$latest" ]]; then
  echo "No Clay article source found under $src_dir" >&2
  exit 1
fi

relative="${latest#"$src_dir/"}"
stem="${relative%.clj}"
qmd="$repo/site/$stem.qmd"
html="$repo/site/_site/$stem.html"
url="http://127.0.0.1:8765/$stem.html"
stale=false

if [[ ! -f "$html" ]] || (( latest_mtime > $(mtime "$html") )); then
  stale=true
fi

printf 'REPO=%q\n' "$repo"
printf 'SOURCE=%q\n' "$latest"
printf 'CLAY_SOURCE=%q\n' "$relative"
printf 'QMD=%q\n' "$qmd"
printf 'HTML=%q\n' "$html"
printf 'URL=%q\n' "$url"
printf 'STALE=%s\n' "$stale"
