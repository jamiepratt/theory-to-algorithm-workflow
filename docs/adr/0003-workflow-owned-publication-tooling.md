# ADR 0003: Keep case-study tooling in the workflow repository

Status: accepted — 2026-07-16

## Decision

Keep vocabulary-specific preview and test invocation in this workflow
repository. Preserve Civitas's standard Clay entry point, project preview
defaults, and author-expansion hook; keep case-specific test aliases out of its
shared project configuration.

The workflow profile calls root-owned wrappers. Those wrappers inject
case-specific Clay and Clojure CLI configuration while running article source,
test runners, and immutable resources from the Civitas submodule.

## Why

Civitas is a shared publication repository. Changing its default Clay command
or adding aliases for one authored namespace changes contributor-facing tooling
for everyone. The root workflow repository already owns orchestration and is
the narrower place for those policies.

Clay's standard CLI and extension points remain available to contributors in
their preferred editor, REPL, or command-line workflow. The case study can
still provide a richer local preview without presenting that preference as a
Civitas-wide default.

## Consequences

- `.agents/scripts/vocabulary_preview.sh` owns the specialized local preview.
- `.agents/scripts/vocabulary_tests.sh` injects aliases from
  `.agents/vocabulary-tests.edn`.
- `.agents/research-workflow.json` is the command mapping consumed by skills.
- Vocabulary source, tests, runners, fixtures, and publication inputs remain in
  the Civitas submodule.
- Civitas's `resources/` classpath and global Quarto `*.cljc` resource handling
  are separate publication decisions and are not changed by this boundary.
- Changes to shared Civitas tooling require their own explicit rationale and
  contributor-impact audit.
