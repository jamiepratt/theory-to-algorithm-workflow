---
name: review-vocab-prs
description: Show and inspect open pull requests for the vocabulary-estimation workspace and nested Civitas repository, then ask whether to approve or merge them. Use when asked to list, review, approve, or merge open PRs.
---

# Review Vocabulary PRs

Use `gh-axi` for all GitHub operations. Treat approval and merge as separate external actions.

## Find open PRs

Run from both repositories:

- `/Users/jamiep/Documents/vocab size estimation`
- `/Users/jamiep/Documents/vocab size estimation/clojurecivitas.github.io`

First inspect `git remote -v`. Skip a repository with no GitHub remote and say why. For each configured repository, start with:

```sh
gh-axi pr list --state open --limit 30
```

Use the default summary fields because the installed `gh-axi` exposes only a small set of optional `--fields`. If no configured repository has open PRs, say so and stop.

## Review each candidate

For each relevant PR, inspect:

```sh
gh-axi pr view <number> --reviews --full
gh-axi pr checks <number>
gh-axi pr diff <number> --full
```

Read the actual diff. Report repository, title, author, draft state, checks, review state, mergeability, tests, and material risks. Green checks alone are not enough to recommend approval.

If the current GitHub user authored the PR, note that GitHub does not permit self-approval. Do not represent merge readiness as an approval.

## Ask before acting

After the review, ask inline with numbered choices. Include the PR number and make the recommendation explicit, for example:

1. Approve PR #123 — recommended; diff and checks look sound.
2. Request changes on PR #123 — state the blocking concern.
3. Leave PR #123 unreviewed.

For multiple PRs, ask which PR numbers the choice applies to. Do not use a modal question.

Only after explicit confirmation, submit the review:

```sh
gh-axi pr review <number> --approve --body "Reviewed: changes and checks look sound."
```

or request changes with `--request-changes` and a specific body.

Approval does not authorize merge. After approval and successful required checks, separately ask whether to merge. Only after explicit merge confirmation run `gh-axi pr merge <number>` with the repository's required merge method and branch-deletion policy. Verify the final PR state and report it.
