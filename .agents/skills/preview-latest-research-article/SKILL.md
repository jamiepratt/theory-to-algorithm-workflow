---
name: preview-latest-research-article
description: Render and preview the most recently edited executable research article using the repository profile and protected internal-browser verification. Use when asked to open, show, preview, refresh, or visually verify a research article.
---

# Preview Latest Research Article

Use Codex's internal browser, never a user browser.

## Resolve configuration

1. Run `git rev-parse --show-toplevel` from the current worktree.
2. Run `python3 <root>/.agents/scripts/research_workflow.py validate --root <root>`.
3. Stop on unsupported schema, missing repository, or invalid path.
4. Run the helper's `latest-article` command and read its JSON output. Do not
   reconstruct repository paths or source-to-page mapping.

## Render and serve

If `stale` is true, run each `targeted_render` command in order from the
returned publication repository. Report the failing command; never open stale
output after a failed render.

Start or reuse the returned `live_preview` command from that repository. Keep
the process alive. Read the actual serving origin from its output because the
server may choose another port when the preferred one is occupied. Join that
origin to `preview_path`, then open it with the
`browser:control-in-app-browser` skill. Use the returned `url` only when its
origin matches the running server. For a healthy pre-existing server whose
startup output is unavailable, confirm its listener and require HTTP 200 at the
exact URL.

## Protect and verify

Follow `browser_policy` from the profile. Never reload, navigate, resize, or
close the user's reading tab. Use a separate verification tab and check every
configured item, including page styling, navigation, console, mobile layout,
labels, and theme contrast. Require `pin_matches_head` unless intentionally
previewing an unpublished publication commit. Report source, selection basis,
pinned commit, repository `HEAD`, and URL.
