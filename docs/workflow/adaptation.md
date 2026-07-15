# Adaptation guide

1. Replace the worked case-study material while preserving its historical
   traceability pattern.
2. Edit [`.agents/research-workflow.json`](../../.agents/research-workflow.json):
   repository IDs, relative paths, roles, remotes, commit order, submodule
   ownership, article mapping, commands, and browser policy.
3. Keep paths relative to the discovered Git root. Use no workstation-specific
   paths. Keep the supported schema version at `1` unless helper and skills are
   upgraded together.
4. Run `python3 .agents/scripts/research_workflow.py validate` and exercise the
   missing-field, invalid-path, and unsupported-version failures.
5. Adjust durable domain vocabulary and authority order in `CONTEXT.md`; add
   read triggers to `CONTEXT-MAP.md`.
6. Use the model-experiment issue template for new candidates and the PR
   template to report model, software, and publication checks separately.
7. Forward-test the three skills in fresh contexts. Exercise publish/review
   mutation only against disposable fixture repositories.

The profile is the supported customization surface. Do not put domain names,
absolute paths, or default-branch assumptions into generic skill instructions.
