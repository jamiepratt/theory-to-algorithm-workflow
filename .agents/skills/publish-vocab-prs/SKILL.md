---
name: publish-vocab-prs
description: Commit vocabulary-estimation work with appropriate messages, push branches, and create pull requests in the top-level and nested Civitas repositories. Use when asked to commit, publish, push, or open PRs for this workspace.
---

# Publish Vocabulary PRs

Use `gh-axi` for GitHub operations. Never merge in this workflow.

## Establish scope

Inspect both repositories independently:

- Workspace: `/Users/jamiep/Documents/vocab size estimation`
- Civitas: `/Users/jamiep/Documents/vocab size estimation/clojurecivitas.github.io`

Read each repository's status, current branch, remotes, and diffs. Preserve unrelated or pre-existing changes. Stage only files belonging to the user's requested work.

If a repository that must be pushed has no remote, do not invent one. Explain the limitation and ask a concise numbered question before committing work that cannot complete the requested publish flow.

The Civitas repository owns publication. The shared subtree `clojurecivitas.github.io/src/language_learning/vocabulary_estimation/` is deliberately tracked by both repositories. When it changes, record the intended change in both repositories: commit the nested repository first, then the top-level repository.

If changes are mixed and cannot be separated safely, stop and ask a concise numbered question.

## Validate during iteration

Run checks proportional to the staged change before committing. For changed Clojure files:

1. Run `clj-paren-repair` on the changed files.
2. Run relevant tests or evaluation probes.
3. For article changes, render only the affected page according to the workspace `AGENTS.md` and inspect it in Codex's internal browser when visual behavior changed.

Do not hide failed checks. Summarize any check that could not run.

## Commit

Create or switch to a focused branch using the `codex/` prefix when the current branch is unsuitable. Determine the base branch from `origin/HEAD`; do not assume its name.

Choose a concise imperative commit subject that describes the outcome. Prefer a useful scope when clear, for example:

```text
docs(vocabulary): add terminology notes
fix(simulator): improve sample contrast
```

Stage explicit paths with `git add -- <paths>`. Review `git diff --cached` before committing. Do not amend, rebase, reset, or overwrite existing commits unless the user explicitly requests it.

## Run the pre-push gate

After the final Civitas commit and immediately before the first push, run from the Civitas repository:

```sh
quarto render site
```

Run this full 229-page build once per publish attempt, not during the edit/render loop. If it fails, do not push. Fix the failure or report the external prerequisite when it is unrelated to the change.

## Push and create PRs

For each repository with a new commit:

1. Push with upstream tracking: `git push -u origin <branch>`.
2. Create a ready PR with `gh-axi pr create` from that repository.
3. Use a clear title derived from the commit and a body containing `Summary` and `Tests` sections.
4. If both repositories changed, create distinct PRs and explain their relationship.

Report each commit, branch, and PR URL. Emit Codex git directives only for operations that actually succeeded.
