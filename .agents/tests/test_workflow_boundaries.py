#!/usr/bin/env python3

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROFILE = json.loads((ROOT / ".agents/research-workflow.json").read_text())
PREVIEW_SKILL = ROOT / ".agents/skills/preview-latest-research-article/SKILL.md"
PUBLISH_SKILL = ROOT / ".agents/skills/publish-research-prs/SKILL.md"
TOOLING_ADR = ROOT / "docs/adr/0003-workflow-owned-publication-tooling.md"
PREVIEW_SOURCE = ROOT / ".agents/vocabulary-preview/src/vocabulary_estimation/preview.clj"
PREVIEW_TESTS = ROOT / ".agents/scripts/vocabulary_preview_tests.sh"
AGENT_INSTRUCTIONS = ROOT / "AGENTS.md"


class WorkflowBoundaryTest(unittest.TestCase):
    def test_specialized_preview_is_workflow_owned(self):
        self.assertEqual(
            "../.agents/scripts/vocabulary_preview.sh {source_relative}",
            PROFILE["commands"]["live_preview"],
        )
        self.assertEqual(
            "../.agents/scripts/vocabulary_preview.sh",
            PROFILE["commands"]["default_live_preview"],
        )
        self.assertTrue((ROOT / ".agents/scripts/vocabulary_preview.sh").is_file())

    def test_local_preview_preserves_origin_and_theme_preference(self):
        self.assertEqual(
            "http://localhost:1971",
            PROFILE["articles"]["preview_base_url"],
        )
        preview_source = PREVIEW_SOURCE.read_text()
        self.assertIn("preview-html", preview_source)
        self.assertIn("install-origin-preserving-wrapper!", preview_source)
        result = subprocess.run(
            [str(PREVIEW_TESTS)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_workflow_changes_are_committed_after_validation(self):
        instructions = " ".join(AGENT_INSTRUCTIONS.read_text().split())
        self.assertIn(
            "Commit every completed, validated workflow-repository change immediately",
            instructions,
        )

    def test_vocabulary_test_invocation_is_workflow_owned(self):
        self.assertEqual(
            [
                "../.agents/scripts/vocabulary_tests.sh clj",
                "../.agents/scripts/vocabulary_tests.sh cljs",
            ],
            PROFILE["commands"]["validation"],
        )

        workflow_aliases = (ROOT / ".agents/vocabulary-tests.edn").read_text()
        self.assertIn(":workflow-vocab-test-clj", workflow_aliases)
        self.assertIn(":workflow-vocab-test-cljs", workflow_aliases)
        self.assertTrue((ROOT / ".agents/scripts/vocabulary_tests.sh").is_file())

    def test_workflow_tools_do_not_require_shared_civitas_cleanup(self):
        adr = TOOLING_ADR.read_text()
        self.assertIn(
            "does not require changes to Civitas's shared configuration",
            adr,
        )

    def test_local_preview_discloses_pin_mismatch_without_blocking(self):
        skill = " ".join(PREVIEW_SKILL.read_text().split())
        self.assertIn(
            "Local iteration may continue when `pin_matches_head` is false",
            skill,
        )
        self.assertIn("Publication verification requires `pin_matches_head`", skill)

    def test_publish_skill_requires_article_preview_artifacts(self):
        skill = " ".join(PUBLISH_SKILL.read_text().split())
        self.assertIn("required publication artifact", skill)
        self.assertIn("real rendered simulation", skill)
        self.assertIn("1200×630 PNG", skill)
        self.assertIn("`:image` and descriptive `:image-alt` metadata", skill)
        self.assertIn("desktop and mobile listing card", skill)
        self.assertIn("requires the configured full publication gate", skill)


if __name__ == "__main__":
    unittest.main()
