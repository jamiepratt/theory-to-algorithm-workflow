# ADR 0001: Workflow plus complete case study

Status: accepted — 2026-07-15

## Decision

Position the repository as a reusable theory-to-algorithm workflow demonstrated
through one complete vocabulary-estimation case study.

## Why

The history contains more durable value than a standalone scorer: explicit
estimands, executable teaching, versioned assumptions, deterministic evidence,
and a candidate that remained unpublished as the target after failing its
precommitted gate. Keeping the complete case study makes those practices
inspectable rather than aspirational.

## Consequences

- Generic workflow and agent interfaces must not require Clojure or Civitas.
- Vocabulary-specific terminology remains in case-study docs and profile data.
- V1 remains the target and v2 remains a non-promoted checkpoint.
- Future research is tracked in GitHub issues, not a repository roadmap.
