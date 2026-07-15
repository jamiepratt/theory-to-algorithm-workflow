# Vocabulary-estimation case study

## Current decision

`stratified-beta-binomial-v1` remains the implementation target.
`continuous-pair-frequency-logistic-v2` is an experimental, replayable
checkpoint that failed its precommitted promotion gate. It improved aggregate
coverage and MAE, but its held-out worst-cell coverage was 91.95%, its worst
cell MAE was 21.1% worse than v1, and its median test length was 64 rather than
40. The declared rule required all checks, so the result was non-promotion.

## Read the evidence chain

1. [Current v1 contract](current-scoring-algorithm.md)
2. [Probability foundation](../../../clojurecivitas.github.io/src/language_learning/vocabulary_estimation/bayes_theorem_simulations.clj)
3. [Executable v1 article](../../../clojurecivitas.github.io/src/language_learning/vocabulary_estimation/beta_binomial_first_pass.clj)
4. [Executable v2 experiment and decision](../../../clojurecivitas.github.io/src/language_learning/vocabulary_estimation/pair_frequency_logistic_v2_article.clj)
5. [V2 candidate implementation](../../../clojurecivitas.github.io/src/language_learning/vocabulary_estimation/pair_frequency_logistic_v2.cljc)
6. [Deterministic gate runner](../../../clojurecivitas.github.io/src/language_learning/vocabulary_estimation/pair_frequency_logistic_v2_gate.clj)
7. Immutable evidence: [tuning](../../../clojurecivitas.github.io/resources/language_learning/vocabulary_estimation/pair_frequency_logistic_v2_tuning.edn), [held out](../../../clojurecivitas.github.io/resources/language_learning/vocabulary_estimation/pair_frequency_logistic_v2_held_out.edn), [stress](../../../clojurecivitas.github.io/resources/language_learning/vocabulary_estimation/pair_frequency_logistic_v2_stress.edn), and [grid check](../../../clojurecivitas.github.io/resources/language_learning/vocabulary_estimation/pair_frequency_logistic_v2_grid_check.edn)
8. [CLJ/CLJS parity tests](../../../clojurecivitas.github.io/test/language_learning/vocabulary_estimation/pair_frequency_logistic_v2_test.cljc)

Neither scorer is claimed to be the model currently deployed by Lexibench.
