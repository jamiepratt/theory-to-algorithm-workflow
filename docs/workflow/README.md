# Theory-to-algorithm lifecycle

The unit of progress is one versioned, explainable refinement—not an indefinite
rewrite.

1. **Estimand:** state the population, unit, conditions, and wording of the
   reported quantity. Name what is excluded.
2. **Theory:** identify established relationships and the assumptions required
   to turn them into a measurement model.
3. **Executable baseline:** encode the simplest defensible model with fixtures,
   assertions, and deterministic replay.
4. **Versioned candidate:** remove or test one important assumption. Keep the
   baseline runnable.
5. **Precommitted gate:** freeze scenarios, metrics, thresholds, seeds, and the
   Boolean promotion rule before held-out evaluation.
6. **Deterministic evidence:** record immutable input IDs/hashes, code version,
   seeds, numerical approximations, and result artifacts.
7. **Decision:** promote only if the declared rule passes. Otherwise retain the
   baseline and publish non-promotion.
8. **Publication:** connect theory, executable examples, evidence, software
   tests, and the decision without changing historical claims.

Every promoted version needs a replay and rollback story. Every non-promoted
candidate remains useful evidence: it identifies which assumption, scenario,
or measurement property failed.

The vocabulary case study shows the full loop. V1 is the executable baseline;
continuous-frequency v2 is a preserved candidate whose aggregate improvements
did not satisfy its cellwise and length gate.
