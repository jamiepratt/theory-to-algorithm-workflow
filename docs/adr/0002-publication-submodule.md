# ADR 0002: Publication repository as submodule authority

Status: accepted — 2026-07-15

## Decision

Track `jamiepratt/clojurecivitas.github.io` as the
`clojurecivitas.github.io/` Git submodule. It owns article source, executable
models, fixtures, evidence, tests, and publication configuration. Root owns the
workflow, contract, profile, and reusable skills.

## Why

Previously, root tracked selected files inside an independently cloned Git
repository. Two histories could claim the same source and drift. A submodule
makes ownership and the exact publication commit explicit.

## Consequences

- Clone with `--recurse-submodules` or run `git submodule update --init`.
- Commit/push publication changes before the parent pointer.
- The root commit records one exact publication commit.
- Root MIT licensing covers root-owned material only; the submodule retains its
  own license.
