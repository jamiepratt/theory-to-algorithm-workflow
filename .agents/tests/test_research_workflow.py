#!/usr/bin/env python3

import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / ".agents/scripts/research_workflow.py"
PROFILE = json.loads((ROOT / ".agents/research-workflow.json").read_text())


def run_helper(*arguments: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(HELPER), *arguments, "--root", str(ROOT)],
        text=True,
        capture_output=True,
        check=False,
    )


class ResearchWorkflowProfileTest(unittest.TestCase):
    def profile_result(self, profile: dict) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            path.write_text(json.dumps(profile))
            return run_helper("validate", "--profile", str(path))

    def test_current_profile_and_latest_article(self):
        validated = run_helper("validate")
        self.assertEqual(0, validated.returncode, validated.stderr)
        self.assertTrue(json.loads(validated.stdout)["ok"])

        latest = run_helper("latest-article")
        self.assertEqual(0, latest.returncode, latest.stderr)
        article = json.loads(latest.stdout)
        self.assertTrue(article["source"].endswith(".clj"))
        self.assertTrue(article["generated"].endswith(".html"))
        self.assertTrue(article["preview_path"].endswith(".html"))
        self.assertEqual(
            article["pinned_commit"] == article["repository_head"],
            article["pin_matches_head"],
        )
        self.assertEqual(2, len(article["targeted_render"]))

    def test_missing_field_fails(self):
        profile = copy.deepcopy(PROFILE)
        del profile["articles"]["source_glob"]
        result = self.profile_result(profile)
        self.assertEqual(2, result.returncode)
        self.assertIn("Missing required field", result.stderr)

    def test_missing_scoped_publication_gate_fails(self):
        profile = copy.deepcopy(PROFILE)
        del profile["commands"]["scoped_publication_gate"]
        result = self.profile_result(profile)
        self.assertEqual(2, result.returncode)
        self.assertIn("Missing required field", result.stderr)

    def test_authored_namespace_escape_fails(self):
        profile = copy.deepcopy(PROFILE)
        profile["articles"]["authored_namespaces"] = ["../other-contributor"]
        result = self.profile_result(profile)
        self.assertEqual(2, result.returncode)
        self.assertIn("escapes Git root", result.stderr)

    def test_authored_namespace_cannot_cover_repository_root(self):
        profile = copy.deepcopy(PROFILE)
        profile["articles"]["authored_namespaces"] = ["."]
        result = self.profile_result(profile)
        self.assertEqual(2, result.returncode)
        self.assertIn("must not resolve", result.stderr)

    def test_invalid_path_fails(self):
        profile = copy.deepcopy(PROFILE)
        profile["repositories"][0]["path"] = "missing-publication-repository"
        result = self.profile_result(profile)
        self.assertEqual(2, result.returncode)
        self.assertIn("does not exist", result.stderr)

    def test_unsupported_version_fails(self):
        profile = copy.deepcopy(PROFILE)
        profile["schema_version"] = 2
        result = self.profile_result(profile)
        self.assertEqual(2, result.returncode)
        self.assertIn("Unsupported schema_version", result.stderr)


if __name__ == "__main__":
    unittest.main()
