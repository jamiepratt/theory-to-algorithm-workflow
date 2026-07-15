---
name: publish-research-prs
description: Commit scoped research-workflow changes, run configured gates, publish repositories in profile order, and create pull requests. Use when asked to commit, publish, push, or open PRs across configured research and publication repositories.
---

# Publish Research PRs

Use `gh-axi`, targeting each profile `github` ID explicitly with `GH_REPO` (or
`-R`) so an additional upstream remote cannot redirect operations. Never merge
in this workflow.

## Resolve scope

1. Discover the root with `git rev-parse --show-toplevel`.
2. Validate the profile with `.agents/scripts/research_workflow.py validate`.
3. Read ordered repositories from the helper's `repositories` command. Reject
   unsupported schema, missing repositories, invalid paths, or missing remotes.
4. Inspect status, current branch, remote, default branch, and diff in every
   configured repository. Scope means the files implementing the user's request;
   if status mixes inseparable work, ask. Preserve unrelated changes; stage
   explicit paths. Skip clean repositories.

For a submodule change, commit and publish the configured source repository
before staging the owner repository's pointer. Never copy source across the
boundary.

## Validate and commit

Run checks proportional to the change, using commands from the profile and
repository instructions. Run configured repository validation when that
repository changed; do not rerun an unchanged submodule unless acceptance
explicitly requires it. `articles.repository` identifies the publication
repository. For article changes, render only affected pages while iterating.
Reuse a cleanly based focused branch; otherwise create a `codex/` branch,
deriving its base from the configured remote's symbolic `HEAD`.

Review `git diff --cached`, then commit with an imperative subject. Do not amend,
rebase, reset, or overwrite history without explicit authorization.

Immediately before the first publication-repository push, run the configured
`full_publication_gate` once. Do not push after failure.

## Push and open PRs

Process repositories by `commit_order`:

1. Push with upstream tracking.
2. Create a ready PR with `gh-axi pr create` against the configured `github`
   repository.
3. Include `Summary`, `Model validation`, `Software tests`, and `Publication
   checks`, marking non-applicable lanes explicitly.
4. A source commit is publishable when it is reachable from the configured
   remote, its PR exists, and required checks are recorded. Then commit the
   owner's submodule pointer and publish its PR. If repository policy requires
   the source PR merged first, wait for that merge.

Use one outcome-focused commit unless independent concerns need separate
review. Always use separate commits and PRs for separate repositories.

Report commit, branch, and PR URL per repository.
