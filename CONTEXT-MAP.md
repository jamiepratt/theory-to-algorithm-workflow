# Context map

Read [`CONTEXT.md`](CONTEXT.md) first. Then load only the row matching the task.

| Trigger | Read |
|---|---|
| Understand or adapt the general workflow | [`docs/workflow/README.md`](docs/workflow/README.md), [`docs/workflow/adaptation.md`](docs/workflow/adaptation.md) |
| Define or judge a model gate | [`docs/workflow/validation-gates.md`](docs/workflow/validation-gates.md), [model-experiment template](.github/ISSUE_TEMPLATE/model-experiment.yml) |
| Understand repository identity or ownership | [`docs/adr/0001-case-study-workflow-identity.md`](docs/adr/0001-case-study-workflow-identity.md), [`docs/adr/0002-publication-submodule.md`](docs/adr/0002-publication-submodule.md) |
| Change preview or vocabulary-test orchestration | [`docs/adr/0003-workflow-owned-publication-tooling.md`](docs/adr/0003-workflow-owned-publication-tooling.md), [workflow profile](.agents/research-workflow.json), [preview wrapper](.agents/scripts/vocabulary_preview.sh), [test wrapper](.agents/scripts/vocabulary_tests.sh) |
| Change the current vocabulary scorer | [`docs/language-learning/vocabulary-estimation/current-scoring-algorithm.md`](docs/language-learning/vocabulary-estimation/current-scoring-algorithm.md) |
| Review v1, failed v2, or evidence | [`docs/language-learning/vocabulary-estimation/README.md`](docs/language-learning/vocabulary-estimation/README.md) |
| Preview an article | [`.agents/skills/preview-latest-research-article/SKILL.md`](.agents/skills/preview-latest-research-article/SKILL.md) |
| Commit, push, or open PRs | [`.agents/skills/publish-research-prs/SKILL.md`](.agents/skills/publish-research-prs/SKILL.md) |
| Review, approve, or merge PRs | [`.agents/skills/review-research-prs/SKILL.md`](.agents/skills/review-research-prs/SKILL.md) |
| Change repository topology, commands, or mapping | [`.agents/research-workflow.json`](.agents/research-workflow.json), [profile helper](.agents/scripts/research_workflow.py) |
