#!/usr/bin/env python3

import re
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


class DocumentationLinksTest(unittest.TestCase):
    def test_local_markdown_links_exist(self):
        missing = []
        documents = [
            path
            for path in ROOT.rglob("*.md")
            if "clojurecivitas.github.io" not in path.parts
            and ".git" not in path.parts
        ]
        for document in documents:
            for raw in LINK.findall(document.read_text(errors="ignore")):
                target = raw.split("#", 1)[0].strip().strip("<>")
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                resolved = (document.parent / unquote(target)).resolve()
                if not resolved.exists():
                    missing.append(f"{document.relative_to(ROOT)} -> {target}")
        self.assertEqual([], missing, "Missing local links:\n" + "\n".join(missing))


if __name__ == "__main__":
    unittest.main()
