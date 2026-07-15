---
name: review-research-prs
description: Find and inspect pull requests across repositories configured by the research-workflow profile, then request separate authorization for approval and merge. Use when asked to list, review, approve, or merge research or publication PRs.
---

# Review Research PRs

Use `gh-axi`, targeting each profile `github` ID explicitly with `GH_REPO` (or
`-R`) so an additional upstream remote cannot redirect operations. Treat
approval and merge as separate external actions.

## Resolve repositories

1. Discover the root with `git rev-parse --show-toplevel`.
2. Validate `.agents/research-workflow.json` with the profile helper.
3. Read configured repositories from the helper. Stop on unsupported schema,
   missing repositories, invalid paths, or missing remotes.
4. Review every open PR in each configured repository unless the user narrows
   scope. Run `gh-axi pr list --state open --limit 100`; if the returned count
   reaches the limit, report truncation and narrow or paginate before claiming
   completeness.

## Review candidates

For every relevant PR, run:

```sh
gh-axi pr view <number> --reviews --full
gh-axi pr checks <number>
gh-axi pr diff <number> --full
```

Read the diff. Report repository role, title, author, draft/check/review state,
mergeability, model gate, software tests, publication checks, dependency order,
and material risks. Derive validation lanes from the PR template/body and check
names; report missing evidence rather than guessing. `commit_order` describes
publication dependency, not review priority. Green software checks cannot
override a failed model gate. Note that authors cannot self-approve.

## Ask before mutation

Ask inline with numbered choices and a recommendation. Approval authorization
does not authorize merge. After an authorized approval and successful required
checks, ask separately before merge. Only then run the repository's required
merge method and branch policy. Discover that policy from repository
instructions and GitHub settings; if it is unavailable, ask rather than
inventing it. Verify final state.
