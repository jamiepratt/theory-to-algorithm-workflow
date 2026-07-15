# Theory to Algorithm Workflow

A worked example of using coding agents, executable research, and precommitted
validation gates to turn established theory into versioned algorithms.

The repository is for researchers and engineers who need to make model changes
auditable: assumptions are named, candidates are replayable, negative results
remain visible, and publication cannot silently turn a failed experiment into a
promoted algorithm.

## The workflow

1. Define a measurable **estimand**.
2. State the relevant **theory** and assumptions.
3. Make an executable, versioned **baseline**.
4. Introduce one **candidate** that removes or tests one assumption.
5. Freeze a **validation gate** before examining held-out evidence.
6. Produce deterministic evidence from immutable inputs and explicit seeds.
7. Record **promotion or non-promotion** without rewriting history.
8. Publish the reasoning, code, evidence, and decision together.

See [the lifecycle](docs/workflow/README.md) and
[validation lanes](docs/workflow/validation-gates.md).

## Complete case study

The vocabulary-estimation example defines receptive knowledge of
lemma–surface-form pairs in a fixed pool.

- `stratified-beta-binomial-v1` became the implementation target.
- `continuous-pair-frequency-logistic-v2` tested whether continuous frequency
  could replace eight independent strata.
- V2 improved aggregate measures but failed precommitted worst-cell coverage,
  worst-cell error, and test-length checks. It was not promoted; v1 remains the
  target.

The [case-study index](docs/language-learning/vocabulary-estimation/README.md)
links the contract, executable articles, immutable evidence, and tests.

## Quick start

```sh
git clone --recurse-submodules \
  https://github.com/jamiepratt/theory-to-algorithm-workflow.git
cd theory-to-algorithm-workflow
python3 .agents/scripts/research_workflow.py validate
```

Preview the configured article repository:

```sh
cd clojurecivitas.github.io
clojure -M:clay
```

Use the repository-local skills for repeatable operations:

- `$preview-latest-research-article`
- `$publish-research-prs`
- `$review-research-prs`

## Adapt this workflow

Fork or copy the repository, replace the case-study documentation, then edit
[`.agents/research-workflow.json`](.agents/research-workflow.json). Configure
repository IDs and roles, submodule ownership, article mapping, commands, and
browser policy. The three skills contain no case-specific paths or logic; they
validate and consume that profile. See the
[adaptation guide](docs/workflow/adaptation.md).

## Limits

This is one worked case study, not proof that every research question fits one
model family or gate. Synthetic validation cannot replace representative human
data. Coding agents improve traceability and iteration speed but do not supply
scientific authority, choose an estimand, or justify a threshold by themselves.
Clojure, Clay, Quarto, Civitas, and Git submodules are example technologies,
not workflow requirements.

Root-owned material is MIT licensed. The Civitas submodule retains its own
license and history.
