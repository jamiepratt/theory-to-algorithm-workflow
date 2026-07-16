#!/usr/bin/env python3

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PUBLICATION = ROOT / "clojurecivitas.github.io"
PROFILE = json.loads((ROOT / ".agents/research-workflow.json").read_text())


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

        publication_deps = (PUBLICATION / "deps.edn").read_text()
        publication_db = (PUBLICATION / "src/civitas/db.clj").read_text()
        self.assertIn('"scicloj.clay.v2.main"', publication_deps)
        self.assertNotIn('"civitas.clay-main"', publication_deps)
        self.assertFalse((PUBLICATION / "src/civitas/clay_main.clj").exists())
        self.assertNotIn("restore-replaced-quarto-config", publication_db)

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

        publication_deps = (PUBLICATION / "deps.edn").read_text()
        self.assertNotIn(":test-clj", publication_deps)
        self.assertNotIn(":test-cljs", publication_deps)


if __name__ == "__main__":
    unittest.main()
