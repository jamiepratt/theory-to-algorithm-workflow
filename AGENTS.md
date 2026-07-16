# Theory-to-algorithm workflow agent notes

This repository is a reusable workflow plus one completed vocabulary-estimation
case study. Read [`CONTEXT.md`](CONTEXT.md), then use
[`CONTEXT-MAP.md`](CONTEXT-MAP.md) to load only task-relevant detail.

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
