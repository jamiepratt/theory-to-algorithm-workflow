#!/usr/bin/env python3

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / ".agents/scripts/research_workflow.py"


def run(cwd: Path, *arguments: str) -> str:
    result = subprocess.run(
        list(arguments), cwd=cwd, text=True, capture_output=True, check=False
    )
    if result.returncode:
        raise AssertionError(
            f"Command failed in {cwd}: {' '.join(arguments)}\n{result.stdout}{result.stderr}"
        )
    return result.stdout.strip()


def configure(repository: Path) -> None:
    run(repository, "git", "config", "user.name", "Fixture Agent")
    run(repository, "git", "config", "user.email", "fixture@example.invalid")


class RepositoryMutationFixtureTest(unittest.TestCase):
    def test_publish_order_and_review_merge_use_disposable_repositories(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            publication_remote = base / "publication.git"
            workflow_remote = base / "workflow.git"
            run(base, "git", "init", "--bare", str(publication_remote))
            run(base, "git", "init", "--bare", str(workflow_remote))

            seed = base / "publication-seed"
            run(base, "git", "init", "-b", "main", str(seed))
            configure(seed)
            (seed / "src").mkdir()
            (seed / "site").mkdir()
            (seed / "src/article.clj").write_text("^{:clay {:title \"Fixture\"}}\n")
            (seed / "site/.keep").write_text("")
            run(seed, "git", "add", "src/article.clj", "site/.keep")
            run(seed, "git", "commit", "-m", "seed publication")
            run(seed, "git", "remote", "add", "origin", str(publication_remote))
            run(seed, "git", "push", "-u", "origin", "main")
            run(publication_remote, "git", "symbolic-ref", "HEAD", "refs/heads/main")

            workflow = base / "workflow"
            run(base, "git", "init", "-b", "master", str(workflow))
            configure(workflow)
            (workflow / "workflow.txt").write_text("fixture\n")
            run(workflow, "git", "add", "workflow.txt")
            run(workflow, "git", "commit", "-m", "seed workflow")
            run(workflow, "git", "remote", "add", "origin", str(workflow_remote))
            run(workflow, "git", "push", "-u", "origin", "master")
            run(workflow_remote, "git", "symbolic-ref", "HEAD", "refs/heads/master")
            run(
                workflow,
                "git", "-c", "protocol.file.allow=always", "submodule", "add",
                str(publication_remote), "publication",
            )
            run(workflow, "git", "commit", "-am", "add publication pointer")
            run(workflow, "git", "push", "origin", "master")

            profile = {
                "schema_version": 1,
                "repositories": [
                    {"id": "publication", "github": "fixture/publication", "path": "publication", "role": "publication", "remote": "origin", "commit_order": 1},
                    {"id": "workflow", "github": "fixture/workflow", "path": ".", "role": "workflow", "remote": "origin", "commit_order": 2},
                ],
                "submodules": [
                    {"path": "publication", "owner_repository": "workflow", "source_repository": "publication", "url": str(publication_remote), "pointer_behavior": "commit-and-publish-source-before-owner-pointer"}
                ],
                "articles": {"repository": "publication", "source_glob": "src/**/*.clj", "source_marker": ":clay", "source_root": "src", "qmd_root": "site", "generated_root": "site/_site", "source_suffix": ".clj", "qmd_suffix": ".qmd", "generated_suffix": ".html", "preview_base_url": "http://127.0.0.1:1971"},
                "commands": {"targeted_render": ["render {source_relative}"], "live_preview": "preview {source_relative}", "default_live_preview": "preview", "full_publication_gate": "publish-gate", "validation": ["test"]},
                "browser_policy": {"browser": "codex-internal-browser", "protect_reading_tabs": True, "verification_tab": "separate", "checks": ["console-errors"]},
            }
            profile_path = workflow / "profile.json"
            profile_path.write_text(json.dumps(profile))
            ordered = json.loads(
                run(
                    workflow,
                    "python3", str(HELPER), "repositories", "--root", str(workflow),
                    "--profile", str(profile_path),
                )
            )
            self.assertEqual(["publication", "workflow"], [row["id"] for row in ordered])

            publication = workflow / "publication"
            configure(publication)
            (publication / "src/article.clj").write_text(
                "^{:clay {:title \"Published fixture\"}}\n"
            )
            run(publication, "git", "add", "src/article.clj")
            run(publication, "git", "commit", "-m", "publish fixture evidence")
            publication_commit = run(publication, "git", "rev-parse", "HEAD")
            run(publication, "git", "push", "origin", "HEAD:main")

            run(workflow, "git", "add", "publication")
            run(workflow, "git", "commit", "-m", "record publication pointer")
            workflow_commit = run(workflow, "git", "rev-parse", "HEAD")
            run(workflow, "git", "push", "origin", "master")
            tree = run(workflow, "git", "ls-tree", workflow_commit, "publication")
            self.assertIn(publication_commit, tree)
            self.assertEqual(
                publication_commit,
                run(publication_remote, "git", "rev-parse", "refs/heads/main"),
            )

            run(workflow, "git", "switch", "-c", "codex/review-fixture")
            (workflow / "reviewed.txt").write_text("review me\n")
            run(workflow, "git", "add", "reviewed.txt")
            run(workflow, "git", "commit", "-m", "add review fixture")
            run(workflow, "git", "push", "origin", "codex/review-fixture")
            self.assertIn(
                "reviewed.txt",
                run(workflow, "git", "diff", "--name-only", "master...codex/review-fixture"),
            )
            run(workflow, "git", "switch", "master")
            run(workflow, "git", "merge", "--no-ff", "codex/review-fixture", "-m", "merge reviewed fixture")
            run(workflow, "git", "push", "origin", "master")
            self.assertEqual(
                run(workflow, "git", "rev-parse", "master"),
                run(workflow_remote, "git", "rev-parse", "refs/heads/master"),
            )


if __name__ == "__main__":
    unittest.main()
