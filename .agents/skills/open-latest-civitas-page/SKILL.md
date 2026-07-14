---
name: open-latest-civitas-page
description: Render and open the most recently edited Clojure Civitas article in Codex's internal browser. Use when asked to open, show, preview, or refresh the latest edited Civitas blog page locally.
---

# Open Latest Civitas Page

Use Codex's internal browser, never Chrome, for this workflow.

## Find the page

Run:

```sh
.agents/skills/open-latest-civitas-page/scripts/find-latest-page.sh
```

The script prefers modified or untracked Clay article sources in the nested Civitas repository, then falls back to the newest Clay article source. Read its `SOURCE`, `CLAY_SOURCE`, `QMD`, `HTML`, `URL`, and `STALE` fields.

## Render when needed

If `STALE=true`, render only the selected article:

```sh
cd clojurecivitas.github.io
clojure -M:clay -A:markdown "$CLAY_SOURCE"
quarto render "$QMD"
```

`CLAY_SOURCE` is relative to `src/`; `QMD` may be absolute. If rendering fails, report the command and error instead of opening an older page.

## Serve and open

Reuse a healthy server already listening on port 8765. Otherwise start one from the workspace root and keep it alive while the preview is needed:

```sh
python3 -m http.server 8765 --directory clojurecivitas.github.io/site/_site
```

Use the `browser:control-in-app-browser` skill to open `URL` in the internal browser. Reload the existing tab when it already shows that URL. Confirm the page loads and inspect the browser console for errors.

When handing off, name the source opened and its local URL.
