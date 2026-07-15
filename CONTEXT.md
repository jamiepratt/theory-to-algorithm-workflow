# Working context

## Repository identity

This repository demonstrates a reusable theory-to-algorithm workflow through a
vocabulary-estimation case study. Root owns workflow documentation, decisions,
the model contract, profile, and reusable skills. The
`clojurecivitas.github.io` submodule owns executable articles, model code,
fixtures, evidence, tests, and publication rendering.

## Vocabulary

- **Estimand:** the quantity an algorithm claims to estimate.
- **Baseline:** the current versioned algorithm used for comparison.
- **Candidate:** an experimental algorithm that changes one declared
  assumption.
- **Precommitted gate:** acceptance criteria frozen before held-out evidence is
  examined.
- **Promotion:** making a candidate the current target after every required
  model check passes.
- **Non-promotion:** retaining the baseline while preserving the candidate and
  its evidence as a historical checkpoint.
- **Software gate:** tests that establish implementation behavior.
- **Publication gate:** rendering and browser checks that establish publishable
  presentation. Neither substitutes for the model gate.

## Current case-study status

- Estimand: receptive knowledge of lemma–surface-form pairs in a fixed,
  versioned pool.
- Current target: `stratified-beta-binomial-v1`.
- Experimental checkpoint: `continuous-pair-frequency-logistic-v2`.
- V2 decision: not promoted. Aggregate coverage and error improved, but the
  held-out candidate missed worst-cell coverage, worst-cell MAE ratio, and
  median-length requirements. V1 therefore remains current.
- Neither article describes the scorer currently deployed at Lexibench.

## Stable invariants

- Pair-frequency data distinguishes lemmas, not senses. Context selects an
  intended meaning but does not create sense-specific frequency.
- Preserve raw `:correct`, `:wrong`, and `:dont-know` events. V1 collapses the
  last two only for inference.
- V1 selection is non-adaptive: one unseen item per stratum per round.
- Frequency is a proxy, not calibrated item difficulty.
- Report pool ID/version, algorithm ID/version, estimate, and interval together;
  never report an unqualified count of “words known.”
- Preserve immutable inputs and original events for deterministic replay.

## Authority order

1. Tested implementation and immutable evidence.
2. [Current scoring contract](docs/language-learning/vocabulary-estimation/current-scoring-algorithm.md).
3. Executable article source.
4. Browser-rendered explanation.

## Essential commands

```sh
python3 .agents/scripts/research_workflow.py validate
python3 .agents/scripts/research_workflow.py repositories
python3 .agents/scripts/research_workflow.py latest-article
git submodule update --init --recursive
```

Configured render, preview, test, and publication commands live in
[`.agents/research-workflow.json`](.agents/research-workflow.json). Resolve the
default branch from `origin/HEAD`; do not assume `main` or `master`.
