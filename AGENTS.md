# Theory-to-algorithm workflow agent notes

This repository is a reusable workflow plus one completed vocabulary-estimation
case study. Read [`CONTEXT.md`](CONTEXT.md), then use
[`CONTEXT-MAP.md`](CONTEXT-MAP.md) to load only task-relevant detail.

## Article-series purpose

The vocabulary-estimation articles are a Jamie-first curriculum that must also
stand alone for any educated lay reader; assume no prior statistics or
psychometrics. Introduce theory gradually, in service of concrete design
decisions across the complete measurement chain:

1. construct and version the target pool of lemma–surface-form pairs, then
   select administered items efficiently;
2. design each multiple-choice item's context, intended meaning, translation,
   and distractors, then version, pilot, calibrate, diagnose, and revise the
   complete item;
3. infer receptive pair knowledge and calibrated uncertainty from responses.

Pair knowledge is an intermediate, countable research target. The eventual
learner-facing quantity remains estimated receptive Polish lemmas; do not imply
that a pair count already solves the lemma-inference problem.

The opening sequence is durable:

1. **Managing Brilliant but Uneven Minds** — how the research is organised;
2. **Why Estimate Vocabulary?** — learner purpose and the measurement chain;
3. **Bayes’ Theorem: From Uncertainty to Decision** — necessary foundations;
4. **Proposal 1: Estimating Known Pairs** — the current research target;
5. **Proposal 2: Does Pair Frequency Predict Responses?** — a preserved,
   non-promoted experimental checkpoint.

Use an approachable title, a precise subtitle, one concrete reader question at
a time, and define technical language when it becomes necessary. Keep reader
labels beside exact algorithm IDs, distinguish teaching simulations from model
validation and representative learner evidence, and state explicitly whenever
an article does not describe the scorer deployed at LexiBench.

The direction of travel is the shortest test that satisfies defined, broad
measurement-quality standards: construct validity, low bias and error,
calibrated uncertainty, and robustness across relevant learner and item groups.
Optimize length only among candidates that pass those standards. “Most
accurate possible” is an aspiration, not a global-optimality claim: compare
versioned candidates with baselines, distinguish simulations from
representative learner evidence, and claim only what the evidence supports.

## Hot path

- Load and validate [`.agents/research-workflow.json`](.agents/research-workflow.json)
  before repository, article-preview, publication, or PR work.
- Discover the root with `git rev-parse --show-toplevel`; never assume a local
  path or default branch. Resolve the default branch from `origin/HEAD`.
- `clojurecivitas.github.io/` is a Git submodule and owns executable articles,
  evidence, tests, and generated publication inputs. Commit and publish it
  before committing the parent submodule pointer.
- Prefer tested implementation, then the current model contract, then
  executable articles, then rendered pages when sources disagree.
- Keep model-validation, software-test, and publication gates distinct. Passing
  software checks never promotes a model whose precommitted gate failed.
- Preserve historical checkpoints and immutable evidence. A rejected candidate
  remains reproducible; a later change receives a new version.
- Track future work in GitHub issues via `gh-axi`, not repository TODO or plan
  files.

## Change rules

- Stage explicit paths. Preserve unrelated changes. Never rewrite history
  unless explicitly requested.
- Commit every completed, validated workflow-repository change immediately on
  the current branch. Keep each commit scoped; do not include the Civitas
  submodule pointer or publication-repository work unless that repository's
  workflow calls for it. Do not push unless explicitly requested.
- After Clojure edits, run `clj-paren-repair <changed-files>` before tests.
- During article iteration, run only the configured targeted render. Immediately
  before publication push, run the scoped publication gate for marked article
  sources in all configured or newly introduced comparable authored
  namespaces. Do not count generated helper/evidence pages as articles. Run the
  full-site gate instead only when the diff may affect rendering outside those
  namespaces.
- Before committing or pushing the Civitas repository, audit staged paths and
  outgoing commit paths against configured `articles.authored_namespaces`. Warn
  with exact outside/shared paths and likely contributor impact. Unless the user
  explicitly authorized those named effects, ask for confirmation before
  commit or push; broad “commit all” or “push everything” wording is not enough.
  A focused non-default branch pushed solely to create or update a PR is exempt
  from the confirmation pause, but still requires the audit and disclosure.
  Direct/shared-branch pushes, force pushes, approval, and merge are not exempt.
- Use Codex's internal browser. Protect the user's reading tab; verify in a
  separate tab, including console, mobile layout, labels, and light/dark
  contrast.
- Keep scorer math pure and deterministic. Version inputs, algorithms, seeds,
  and outputs; preserve original response events.
