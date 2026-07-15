# Vocabulary-estimation workspace agent notes

These instructions apply to this top-level vocabulary-estimation workspace.

## Purpose

This workspace records Jamie Pratt's iterative learning and development of the
Lexibench scoring model. Work in small, explainable increments. Each published
post should remove or test one important assumption without rewriting history.

`clojurecivitas.github.io/` is a separate Git repository Jamie cloned into this
workspace. It is where he will publish his series of articles on incrementally
learning the relevant theory and developing an algorithm for estimating
vocabulary size. The top-level repository ignores that directory except for
`src/language_learning/vocabulary_estimation/`, which is deliberately tracked
in both repositories. Run publication-repository Git operations inside the
nested repository; when this shared source subtree changes, record the intended
change in both repositories.

The current article describes the first-pass target scorer. It is not a
description of the scorer currently deployed at <https://lexibench.com/>.

## Read first

1. [`docs/language-learning/vocabulary-estimation/current-scoring-algorithm.md`](docs/language-learning/vocabulary-estimation/current-scoring-algorithm.md)
   — implementation contract and current roadmap.
2. [`beta_binomial_first_pass.clj`](clojurecivitas.github.io/src/language_learning/vocabulary_estimation/beta_binomial_first_pass.clj)
   — executable article and mathematical examples in the Civitas repository.
3. [`beta_binomial_first_pass_interactive.cljs`](clojurecivitas.github.io/src/language_learning/vocabulary_estimation/beta_binomial_first_pass_interactive.cljs)
   — educational browser interaction, not the production scorer.

If these disagree, prefer tested production code, then the scoring contract,
then the executable article. Use the generated article in Codex's internal
browser for visual review and annotation; rendered browser output is not
implementation authority.

## Stable vocabulary and invariants

- The v1 estimand is receptive knowledge of **lemma–surface-form pairs** in a
  fixed, versioned pool.
- Pair-frequency data distinguishes lemmas but not senses. Context and answer
  choices select an intended meaning; do not claim sense-specific frequency or
  knowledge.
- Preserve raw responses as `:correct`, `:wrong`, or `:dont-know`. V1 collapses
  the last two only for inference.
- V1 item selection is non-adaptive: one unseen item from each of eight strata
  per round. Responses update inference, not the selection schedule.
- `Beta(1,1)`, eight equal-count strata, the frequency proxy, and the stopping
  thresholds are provisional model choices, not discovered facts.
- Report the pool ID/version, algorithm version, estimate, and credible
  interval together. Never report an unqualified count of "words known."
- Frequency is a proxy, not calibrated item difficulty.
- Preserve immutable item versions and original event data so later models can
  be replayed without data migration or reinterpretation.

## Learning and development path

Develop and document one vertical refinement at a time:

1. Replace equal-difficulty strata with a continuous pair-frequency difficulty
   model; validate whether frequency predicts learner responses.
2. Define/version how self-reported CEFR chooses a lemma–form-pair pool.
3. Aggregate correlated pair probabilities into latent lemma knowledge.
4. Model correct, wrong, and don't-know outcomes separately, including
   guessing and slips.
5. Calibrate complete item versions, then evaluate IRT and adaptive selection.
6. Investigate multiple contexts and explicit sense modelling only when the
   data has stable sense identifiers and sufficient repeated observations.

Do not implement a later stage merely because the article mentions it. Record
new model decisions and their rejected alternatives before changing the scorer.

## Repository boundaries and source data

On Jamie's workstation:

- Civitas publishing repository:
  `/Users/jamiep/Documents/vocab size estimation/clojurecivitas.github.io`
- Lexibench app: `/Users/jamiep/Documents/clj/vocab_test_client_side`
- Lexicon source: `/Users/jamiep/Documents/subtlex`
- Pair-frequency table:
  `/Users/jamiep/Documents/subtlex/data/database-import/surface_form_lemma_pair_frequency_ranks.tsv`

The pair-frequency table is unique by `(surface_form_id, lemma_id)` and has no
sense ID. FreeDict sense tables are separate and do not provide sense-specific
pair frequencies.

## Local article preview

- Use Clay Live Reload as the default iteration loop for Civitas articles.
  From `clojurecivitas.github.io/`, start `clojure -M:clay`, keep that process
  running, and open the URL it serves in Codex's internal browser. A one-shot
  Clay/Quarto render is not a live-reload session.
- With no arguments, `clojure -M:clay` should preview the first Civitas article
  and watch all article sources. Keep Clay configured not to launch an external
  browser; open and leave the requested preview in Codex's internal browser.
- Treat the local Clay URL as a preview of the Civitas blog, not as a plain Clay
  document. The current article and pages reached through its relative links
  must retain the Civitas navbar, theme, styles, title, and complete article
  metadata. Keep navigation on the same local Clay origin. The preview plumbing
  lives in `clay.edn` and `src/civitas/clay_main.clj`.
- Verify this workflow in a separate internal-browser tab: observe an automatic
  reload after a source edit, follow at least one article link, confirm the
  linked page still looks like Civitas, and check the browser console.
- Use Clay's live preview while editing `.clj` article content and sibling
  Scittle `.cljs` interactions. Do not introduce Shadow merely to serve the
  preview; evaluate Shadow separately only if compiled-CLJS hot code reload is
  deliberately required.
- Do not use or start Lavish for Civitas article preview or review unless Jamie
  explicitly requests it. Use the internal browser directly.
- Clay's `temp` preview is the fast iteration surface, not final publication
  proof. Render only the affected Quarto post for publication-layout checks,
  then run the full-site gate only immediately before pushing.

## Change discipline

- Keep scoring math pure and portable to `.cljc`; isolate storage, UI, clocks,
  and randomness at boundaries.
- Require deterministic replay from versioned inputs and an explicit seed.
- Add CLJ and CLJS parity tests for every scoring change.
- Update the scoring contract, executable article, worked examples, and tests
  in the same change when behavior changes.
- Preserve previous posts as historical checkpoints; publish a follow-up rather
  than silently making an old learning milestone claim a later model.
- After editing Clojure files, run `clj-paren-repair <changed-files>` before
  tests.
- During iteration, render only the affected post:

  ```sh
  cd clojurecivitas.github.io
  clojure -M:clay -A:markdown \
    language_learning/vocabulary_estimation/beta_binomial_first_pass.clj
  quarto render \
    site/language_learning/vocabulary_estimation/beta_binomial_first_pass.qmd
  ```

- Immediately before pushing Civitas changes, run the full-site gate with
  `quarto render site`. Do not run that 229-page build after every edit.

- Verify Scittle controls, browser console, mobile layout, accessible labels,
  and the generated article before publishing.
- When the user is reading or commenting on an article in Codex's internal
  browser, perform reloads and verification in a separate browser tab. Never
  claim, reload, navigate, resize, or otherwise disturb the user's reading tab;
  close only the separate verification tab when checks finish.
- For every UI control, callout, explanation, chart label, and interactive
  state, verify foreground/background contrast in both light and dark modes.
  Derive paired foreground and background colours from the active theme; do
  not combine a fixed light background with inherited dark-mode text, or the
  reverse.
