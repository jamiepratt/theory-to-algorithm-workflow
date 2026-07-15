# Current target scoring algorithm: stratified Beta–binomial v1

Status: **implementation target; not the scorer currently deployed by
Lexibench**

Algorithm ID: `stratified-beta-binomial-v1`

Decision date: 2026-07-12

Current-status review: 2026-07-15. V1 remains the implementation target after
`continuous-pair-frequency-logistic-v2` failed its precommitted promotion gate.
This status records the later decision without rewriting the v1 specification.

This document specifies the first scorer Jamie intends to implement while
learning and iteratively developing the model. It is detailed enough to build
equivalent Clojure and ClojureScript implementations. Every modelling choice
below is provisional and must remain versioned.

## Sources and authority

- Executable explanation:
  [`beta_binomial_first_pass.clj`](../../../clojurecivitas.github.io/src/language_learning/vocabulary_estimation/beta_binomial_first_pass.clj)
- Browser teaching interaction:
  [`beta_binomial_first_pass_interactive.cljs`](../../../clojurecivitas.github.io/src/language_learning/vocabulary_estimation/beta_binomial_first_pass_interactive.cljs)
- Preserved v2 experiment and decision:
  [`pair_frequency_logistic_v2_article.clj`](../../../clojurecivitas.github.io/src/language_learning/vocabulary_estimation/pair_frequency_logistic_v2_article.clj)
- Immutable v2 held-out evidence:
  [`pair_frequency_logistic_v2_held_out.edn`](../../../clojurecivitas.github.io/resources/language_learning/vocabulary_estimation/pair_frequency_logistic_v2_held_out.edn)

Review and annotate the generated article in Codex's internal browser. The
browser is the teaching and visual-review surface; this contract, tested code,
and executable assertions remain authoritative for implementation. The
worked-example posterior-predictive mean is `4,334`.

## 1. Construct and non-goals

The estimated quantity is:

> Receptive knowledge of lemma–surface-form pairs in a fixed, versioned pool.

A pair is identified by stable `lemma-id` and `surface-form-id`. The canonical
test item also has a context, intended translation, distractors, and language
pair. Those fields affect measurement but do not create additional countable
vocabulary units in v1.

The frequency data does not distinguish senses. Context selects an intended
meaning operationally, but v1 must not report sense-specific knowledge.

V1 does not:

- convert a CEFR level into a pair inventory;
- convert known pairs into known lemmas;
- infer guessing or slips;
- calibrate item difficulty;
- choose items adaptively;
- model multiple contexts or senses;
- claim that frequency rank is measured learner difficulty.

The caller must supply an already constructed pool. The article's 8,000-pair
pool is synthetic and must never be presented as a current Lexibench or CEFR
inventory size.

## 2. Versioned inputs

### Pool

A pool contains:

```clojure
{:pool-id "polish-example-pool"
 :pool-version "2026-07-12"
 :language-pair [:pl :en]
 :pairs [{:pair-id [lemma-id surface-form-id]
          :lemma-id lemma-id
          :surface-form-id surface-form-id
          :pair-frequency-rank rank
          :item-version-id item-version-id}
         ...]}
```

All pair IDs and item-version IDs must be unique in the pool. Pool contents are
immutable after publication; changes create a new `pool-version`.

### Scorer configuration

```clojure
{:algorithm-id :stratified-beta-binomial-v1
 :algorithm-version 1
 :strata-count 8
 :prior {:alpha 1.0 :beta 1.0}
 :credible-mass 0.95
 :minimum-items 32
 :round-size 8
 :target-half-width-ratio 0.10
 :soft-maximum-items 96
 :posterior-draws 50000
 :seed 20260712}
```

The seed and draw count are part of the scorer version. They make repeated
scoring of identical sufficient statistics deterministic. A verification build
may use 100,000 or more draws, but production outputs must not silently change
draw count or seed.

### Raw response event

Persist an append-only event before collapsing it for inference:

```clojure
{:attempt-id attempt-id
 :algorithm-id :stratified-beta-binomial-v1
 :algorithm-version 1
 :pool-id pool-id
 :pool-version pool-version
 :item-version-id item-version-id
 :pair-id [lemma-id surface-form-id]
 :stratum-index 0                 ; 0..7
 :round-index 0
 :position 0
 :response :correct              ; :correct | :wrong | :dont-know
 :response-ms 2400
 :presented-at instant
 :selection-probability probability}
```

`response-ms` and `selection-probability` may be absent only in early test
fixtures. Production collection should preserve them for later calibration and
sampling-bias analysis. Never rewrite `:wrong` as `:dont-know` in storage.

## 3. Pool stratification and item selection

1. Sort pool pairs by `(pair-frequency-rank, deterministic-pair-id)` ascending;
   lower rank means more frequent.
2. Partition the ordered vector into eight contiguous, near-equal-count strata.
   Sizes may differ by at most one. Tied frequency ranks may be split to retain
   equal counts; this is a documented v1 simplification.
3. At attempt creation, independently shuffle each stratum's item-version IDs
   with the attempt's selection seed and store the queues or enough state to
   reproduce them.
4. One round takes the next unseen item from every stratum, then shuffles the
   order of those eight selected items before presentation.
5. Never repeat an item version within an attempt.
6. Responses do not alter queues, strata, or round order. Only exhaustion or a
   stop decision ends selection.

For item `i` selected uniformly from `r` remaining eligible items in its
stratum, record selection probability `1/r`. If exposure controls later make
selection non-uniform, version the selector and record its actual probability.

## 4. Response likelihood and posterior

V1 preserves three raw outcomes but uses a Bernoulli likelihood:

```clojure
(defn known-outcome [response]
  (case response
    :correct 1
    :wrong 0
    :dont-know 0))
```

For stratum `s`:

- `N_s`: number of pairs in the stratum;
- `n_s`: valid responses observed in the stratum;
- `k_s`: correct responses in the stratum;
- `p_s`: unknown proportion of the stratum known by this learner.

Prior and likelihood:

```text
p_s ~ Beta(alpha_0, beta_0)
responses | p_s ~ Bernoulli(p_s)
alpha_0 = 1
beta_0 = 1
```

Posterior:

```text
alpha_s = 1 + k_s
beta_s  = 1 + n_s - k_s
p_s | data ~ Beta(alpha_s, beta_s)
```

`Beta(1,1)` is uniform on `[0,1]`; call it the simple v1 prior, not universally
uninformative.

Reject an unknown response value. Do not score duplicate item events, events
whose pair/item is absent from the stated pool version, or states where
`k_s > n_s`, `n_s > N_s`, or a stratum index is invalid.

## 5. Finite-pool posterior prediction

The observed correct pairs are known outcomes and must not be predicted again.
For each posterior draw `j` and stratum `s`:

```text
p_s[j] ~ Beta(alpha_s, beta_s)
U_s[j] ~ Binomial(N_s - n_s, p_s[j])
T_s[j] = k_s + U_s[j]
T[j]   = sum_s T_s[j]
```

Use the analytic posterior-predictive mean for the unrounded point estimate:

```text
mean_s = k_s + (N_s - n_s) * alpha_s / (alpha_s + beta_s)
mean_total = sum_s mean_s
```

Use deterministic posterior draws for the equal-tail credible interval:

1. generate `posterior-draws` totals using the configured seed;
2. sort totals ascending;
3. for probability `q`, select index `floor(q * (draw-count - 1))`;
4. with mass `0.95`, report quantiles `0.025` and `0.975`.

Keep raw calculation values. The UI may round the point and endpoints to the
nearest ten pairs, but persisted/API results must retain unrounded values and
the credible mass.

### Required reference example

For eight 1,000-pair strata, four responses per stratum, and correct counts:

```clojure
[4 4 3 3 2 1 1 0]
```

the implementation must reproduce:

```text
items tested:              32
correct:                   18
analytic total mean:       4,334
exact reference 95% ETI:   3,404–5,249
reader-facing result:      about 4,330 (roughly 3,400–5,250)
```

A seeded Monte Carlo interval may differ slightly. With 100,000 verification
draws, require mean error below 20 pairs and endpoint errors below 40 pairs.

## 6. Stopping behavior

Evaluate an automatic stop only at complete eight-item round boundaries.

```text
minimum reached = items_tested >= 32
round complete  = items_tested mod 8 = 0
half_width      = (upper - lower) / 2
target reached  = half_width <= 0.10 * pool_size
soft max reached = items_tested >= 96
```

Return:

```clojure
{:assess? (and minimum-reached? round-complete?)
 :recommended-stop? boolean
 :reason :voluntary | :precision-target | :soft-maximum | :continue}
```

Priority when more than one reason applies:

1. `:voluntary`
2. `:precision-target`
3. `:soft-maximum`
4. `:continue`

A learner may stop voluntarily at any time, including during a partial round.
Return an estimate using all valid responses, but label it voluntary and do not
claim the automatic precision target was assessed off-boundary.

If a stratum queue is exhausted before a stop condition, return a typed
`pool-exhausted` failure with the exhausted strata; do not repeat items.

## 7. Scorer output

Return a data-only value usable from CLJ and CLJS:

```clojure
{:algorithm {:id :stratified-beta-binomial-v1
             :version 1
             :seed 20260712
             :posterior-draws 50000}
 :pool {:id pool-id :version pool-version :size pool-size}
 :responses {:items-tested n :correct k :wrong w :dont-know d}
 :estimate {:unit :lemma-surface-form-pairs
            :mean mean-total
            :rounded-mean rounded-mean}
 :credible-interval {:mass 0.95
                     :kind :equal-tail
                     :lower lower
                     :upper upper
                     :half-width half-width}
 :strata [{:index 0
           :pool-size N_s
           :tested n_s
           :correct k_s
           :posterior {:alpha alpha_s :beta beta_s}
           :mean mean_s}
          ...]
 :stopping {:assess? boolean
            :recommended-stop? boolean
            :reason reason}}
```

No public label should say only “words known.” Prefer:

> Estimated receptive knowledge: about 4,330 lemma–surface-form pairs from pool
> `X`, version `Y` (95% credible interval: roughly 3,400–5,250).

## 8. Implementation boundaries

- Put pure validation, aggregation, posterior parameters, analytic means,
  quantiles, interval summaries, and stopping logic in a shared `.cljc` module.
- Pass an RNG/seed into posterior sampling. Do not read global randomness inside
  pure scoring functions.
- Keep database loading, event persistence, UI formatting, and async execution
  outside the scoring module.
- Run large CLJS simulations off the browser's UI thread or precompute on the
  backend. Client and backend must use the same algorithm/config version and
  pass parity fixtures.
- Persist enough version metadata to rescore an old attempt under both its
  original algorithm and later experimental models.
- Treat the Scittle article component as teaching UI, not reusable production
  scoring code.

## 9. Acceptance tests

Implement equivalent CLJ and CLJS tests for:

- response mapping preserves three raw values and maps only `:correct` to `1`;
- posterior parameter updates, including all-correct and all-not-known cases;
- analytic stratum and total means;
- the 8,000-pair reference fixture above;
- deterministic replay for identical versioned input and seed;
- credible-interval quantile indexing and Monte Carlo tolerance;
- unequal stratum sizes differing by at most one;
- no repeat selection and balanced one-per-stratum rounds;
- responses never changing the precomputed selection queues;
- minimum, round-boundary, precision, soft-maximum, and voluntary stopping;
- voluntary stopping during a partial round;
- rejection of unknown responses, duplicates, version mismatches, invalid
  counts, missing pairs/items, and invalid stratum IDs;
- typed failure when a stratum is exhausted;
- output bounds `0 <= lower <= upper <= pool-size`;
- CLJ/CLJS equality for deterministic fixtures and configured rounding.

Render the Civitas article after scoring changes and verify that its executable
assertions, worked values, Scittle interaction, browser console, and mobile
layout still pass.

## 10. V2 non-promotion and future work

The continuous-frequency v2 candidate tested the first proposed refinement. It
improved aggregate coverage and MAE under favourable synthetic scenarios, but
failed the all-checks promotion rule: held-out worst-cell coverage was 91.95%,
worst-cell MAE was 21.1% worse than v1, and median length was 64 items rather
than v1's 40. V2 therefore remains an experimental replayable checkpoint; it
did not replace this contract.

Future refinements require a new algorithm version, immutable inputs, explicit
seeds, a precommitted gate, parity fixtures, a replay/rollback story, and a
published promotion or non-promotion decision. Track them in GitHub:

- [#2 Define and version CEFR-to-pair pool construction](https://github.com/jamiepratt/theory-to-algorithm-workflow/issues/2)
- [#3 Model correlated form pairs through latent lemma knowledge](https://github.com/jamiepratt/theory-to-algorithm-workflow/issues/3)
- [#4 Model correct, wrong, and don't-know separately](https://github.com/jamiepratt/theory-to-algorithm-workflow/issues/4)
- [#5 Calibrate complete immutable item versions](https://github.com/jamiepratt/theory-to-algorithm-workflow/issues/5)
- [#6 Evaluate IRT and adaptive selection after calibration](https://github.com/jamiepratt/theory-to-algorithm-workflow/issues/6)
- [#7 Investigate context and sense models when identifiable](https://github.com/jamiepratt/theory-to-algorithm-workflow/issues/7)
