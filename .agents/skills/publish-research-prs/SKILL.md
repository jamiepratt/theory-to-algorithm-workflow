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

## Protect other contributors

Treat `articles.authored_namespaces` as exact relative path-segment sequences
owned by this workflow inside the publication repository, not loose substring
matches. Before committing, inspect every staged path. Before pushing, inspect
every path in commits not yet on the configured remote. A clean working tree
does not make an outgoing commit safe.

If any publication-repository path falls outside every authored namespace and
might affect Civitas content, shared rendering, build behavior, or another
contributor:

1. Warn with the exact paths and likely impact.
2. If the current request did not explicitly authorize those named effects,
   stop before commit or push and ask for confirmation.
3. Treat broad instructions such as “commit all” or “push everything” as
   insufficient unless the cross-contributor paths and impact were already
   surfaced to the user. One confirmation may cover both commit and push when
   the warning explicitly says so.

Exception: do not pause for confirmation when the commit and push are confined
to a focused non-default branch solely to create or update a PR. Still audit,
warn, and record the outside/shared paths and impact in the PR and handoff. This
exception does not cover direct pushes to the default, deployment, or another
shared branch; force pushes; approval; or merge.

Never stage unrelated work. Record explicit authorization in the handoff.

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

Immediately before the first publication-repository push, inspect the scoped
diff for cross-page rendering risk and run exactly one configured gate after
the final change:

- Default to `scoped_publication_gate`, which recursively finds publishable
  article sources by the configured article marker and renders their matching
  pages in each authored namespace. Exclude generated helper, evidence, and
  gate pages without article metadata. Treat current articles as examples, not
  a fixed list; add newly introduced comparable authored namespaces to the
  configured scope and `articles.authored_namespaces`.
- Use `full_publication_gate` only when the diff may change rendering outside
  that scope, such as shared Quarto configuration, themes, styles, brand files,
  extensions, filters, templates, includes, navigation/listings or their input
  metadata, shared resources, or publication build tooling.

Do not run both unless acceptance criteria explicitly require both. Record the
selected gate and, for a full-site render, the cross-page risk that required it.
Do not push after failure.

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
