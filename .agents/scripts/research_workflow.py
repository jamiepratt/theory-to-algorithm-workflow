#!/usr/bin/env python3
"""Validate and query the repository-local research workflow profile."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

SUPPORTED_SCHEMA = 1


class ProfileError(Exception):
    pass


def fail(message: str) -> None:
    raise ProfileError(message)


def git(*args: str, cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, text=True, capture_output=True, check=False
    )
    if result.returncode:
        fail(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def discover_root(explicit: str | None) -> Path:
    if explicit:
        root = Path(explicit).resolve()
    else:
        root = Path(git("rev-parse", "--show-toplevel", cwd=Path.cwd())).resolve()
    if not (root / ".git").exists():
        fail(f"Git root not found: {root}")
    return root


def required(mapping: dict, key: str, where: str):
    if key not in mapping:
        fail(f"Missing required field: {where}.{key}")
    return mapping[key]


def safe_path(
    root: Path, relative: str, where: str, *, must_exist: bool = True
) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute():
        fail(f"Absolute path is not supported at {where}: {relative}")
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        fail(f"Path escapes Git root at {where}: {relative}")
    if must_exist and not resolved.exists():
        fail(f"Configured path does not exist at {where}: {relative}")
    return resolved


def load_and_validate(root: Path, profile_path: str | None) -> tuple[dict, Path]:
    path = Path(profile_path).resolve() if profile_path else root / ".agents/research-workflow.json"
    if not path.is_file():
        fail(f"Workflow profile not found: {path}")
    try:
        profile = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        fail(f"Cannot read workflow profile: {error}")

    version = required(profile, "schema_version", "profile")
    if version != SUPPORTED_SCHEMA:
        fail(f"Unsupported schema_version {version}; supported: {SUPPORTED_SCHEMA}")

    repositories = required(profile, "repositories", "profile")
    if not isinstance(repositories, list) or not repositories:
        fail("profile.repositories must be a non-empty array")
    ids: set[str] = set()
    orders: set[int] = set()
    resolved_repositories: dict[str, Path] = {}
    for index, repository in enumerate(repositories):
        where = f"profile.repositories[{index}]"
        for key in ("id", "github", "path", "role", "remote", "commit_order"):
            required(repository, key, where)
        repo_id = repository["id"]
        if repo_id in ids:
            fail(f"Duplicate repository id: {repo_id}")
        if repository["commit_order"] in orders:
            fail(f"Duplicate commit_order: {repository['commit_order']}")
        ids.add(repo_id)
        orders.add(repository["commit_order"])
        repo_path = safe_path(root, repository["path"], f"{where}.path")
        if not (repo_path / ".git").exists():
            fail(f"Configured repository is not a Git worktree: {repo_path}")
        git("remote", "get-url", repository["remote"], cwd=repo_path)
        resolved_repositories[repo_id] = repo_path

    for index, submodule in enumerate(required(profile, "submodules", "profile")):
        where = f"profile.submodules[{index}]"
        for key in ("path", "owner_repository", "source_repository", "url", "pointer_behavior"):
            required(submodule, key, where)
        safe_path(root, submodule["path"], f"{where}.path")
        for key in ("owner_repository", "source_repository"):
            if submodule[key] not in ids:
                fail(f"Unknown repository id at {where}.{key}: {submodule[key]}")

    articles = required(profile, "articles", "profile")
    for key in (
        "repository", "source_glob", "source_marker", "source_root", "qmd_root",
        "generated_root", "source_suffix", "qmd_suffix", "generated_suffix",
        "preview_base_url",
    ):
        required(articles, key, "profile.articles")
    if articles["repository"] not in ids:
        fail(f"Unknown article repository: {articles['repository']}")
    article_repo = resolved_repositories[articles["repository"]]
    for key in ("source_root", "qmd_root"):
        safe_path(article_repo, articles[key], f"profile.articles.{key}")
    safe_path(
        article_repo,
        articles["generated_root"],
        "profile.articles.generated_root",
        must_exist=False,
    )

    commands = required(profile, "commands", "profile")
    for key in (
        "targeted_render", "live_preview", "default_live_preview",
        "scoped_publication_gate", "full_publication_gate", "validation",
    ):
        required(commands, key, "profile.commands")
    browser = required(profile, "browser_policy", "profile")
    for key in ("browser", "protect_reading_tabs", "verification_tab", "checks"):
        required(browser, key, "profile.browser_policy")

    return profile, path


def repository_rows(root: Path, profile: dict) -> list[dict]:
    rows = []
    for repository in sorted(profile["repositories"], key=lambda item: item["commit_order"]):
        row = dict(repository)
        row["resolved_path"] = str((root / repository["path"]).resolve())
        rows.append(row)
    return rows


def article_candidates(repo: Path, articles: dict) -> list[Path]:
    candidates = []
    for path in repo.glob(articles["source_glob"]):
        if path.is_file() and articles["source_marker"] in path.read_text(errors="ignore"):
            candidates.append(path.resolve())
    if not candidates:
        fail(f"No configured article sources found in {repo}")
    return candidates


def changed_paths(repo: Path) -> set[Path]:
    output = git("status", "--porcelain=v1", "--untracked-files=all", cwd=repo)
    paths = set()
    for line in output.splitlines():
        value = line[3:]
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        paths.add((repo / value).resolve())
    return paths


def expand(command: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        command = command.replace("{" + key + "}", value)
    return command


def latest_article(root: Path, profile: dict) -> dict:
    repositories = {row["id"]: row for row in repository_rows(root, profile)}
    articles = profile["articles"]
    repo = Path(repositories[articles["repository"]]["resolved_path"])
    candidates = article_candidates(repo, articles)
    changed = changed_paths(repo)
    changed_candidates = [path for path in candidates if path in changed]
    preferred = changed_candidates or candidates
    source = max(preferred, key=lambda path: path.stat().st_mtime)
    source_root = (repo / articles["source_root"]).resolve()
    try:
        relative = source.relative_to(source_root)
    except ValueError:
        fail(f"Article source is outside configured source_root: {source}")
    if source.suffix != articles["source_suffix"]:
        fail(f"Article source suffix does not match profile: {source}")
    stem = relative.with_suffix("")
    qmd = repo / articles["qmd_root"] / stem.with_suffix(articles["qmd_suffix"])
    generated = repo / articles["generated_root"] / stem.with_suffix(articles["generated_suffix"])
    source_relative = str(relative)
    qmd_relative = str(qmd.relative_to(repo))
    generated_relative = str(generated.relative_to(repo))
    values = {
        "source_relative": source_relative,
        "qmd_relative": qmd_relative,
        "generated_relative": generated_relative,
    }
    stale = not generated.exists() or source.stat().st_mtime > generated.stat().st_mtime
    preview_path = "/" + quote(
        generated_relative.removeprefix(
            articles["generated_root"].rstrip("/") + "/"
        )
    )
    repository_head = git("rev-parse", "HEAD", cwd=repo)
    pinned_commit = None
    for submodule in profile["submodules"]:
        if submodule["source_repository"] == articles["repository"]:
            owner = Path(repositories[submodule["owner_repository"]]["resolved_path"])
            pinned_commit = git("rev-parse", f":{submodule['path']}", cwd=owner)
            break
    return {
        "repository": str(repo),
        "repository_head": repository_head,
        "pinned_commit": pinned_commit,
        "pin_matches_head": pinned_commit is None or pinned_commit == repository_head,
        "source": str(source),
        "selection_basis": (
            "changed-source-mtime" if changed_candidates else "source-mtime"
        ),
        "source_relative": source_relative,
        "qmd": str(qmd),
        "qmd_relative": qmd_relative,
        "generated": str(generated),
        "generated_relative": generated_relative,
        "preview_path": preview_path,
        "url": articles["preview_base_url"].rstrip("/") + preview_path,
        "stale": stale,
        "targeted_render": [expand(item, values) for item in profile["commands"]["targeted_render"]],
        "live_preview": expand(profile["commands"]["live_preview"], values),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("validate", "repositories", "latest-article"))
    parser.add_argument("--root")
    parser.add_argument("--profile")
    args = parser.parse_args()
    try:
        root = discover_root(args.root)
        profile, path = load_and_validate(root, args.profile)
        if args.command == "validate":
            output = {
                "ok": True,
                "schema_version": profile["schema_version"],
                "profile": str(path),
                "repositories": len(profile["repositories"]),
            }
        elif args.command == "repositories":
            output = repository_rows(root, profile)
        else:
            output = latest_article(root, profile)
        print(json.dumps(output, indent=2))
        return 0
    except ProfileError as error:
        print(f"profile error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
