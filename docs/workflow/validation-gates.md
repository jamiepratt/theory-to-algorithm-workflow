# Three validation lanes

## Model validation

Answers: “Does this candidate earn promotion for the declared estimand?” Freeze
inputs, scenarios, metrics, thresholds, seeds, and the all/any decision rule
before held-out evidence. Report every check and preserve failures.

## Software validation

Answers: “Does the implementation behave as specified?” Use unit, parity,
property, replay, and fixture-integrity checks. Green tests do not rescue a
candidate that failed its model gate.

## Publication validation

Answers: “Can readers inspect the argument and evidence correctly?” Use focused
rendering during iteration. Immediately before publishing, run the configured
scoped gate for every marked article source in each configured or newly
introduced comparable authored namespace; exclude generated helper, evidence,
and gate pages without article metadata, and never treat the current article
list as fixed. Substitute the full-site gate only when shared configuration,
themes, templates, navigation, build tooling, listing metadata, or another
changed input may affect pages outside those namespaces. Verify links,
interactive controls, console, mobile layout, accessible labels, and light/dark
contrast.

## Decision record

A decision must name algorithm and evidence versions, gate definition, results,
promotion/non-promotion, and consequences. Threshold changes after seeing
held-out results define a new candidate and new gate—not a correction to the
old result.
