#!/usr/bin/env python3
"""Validate the local, semantic Oh My PPT integration boundary."""

from __future__ import annotations

import json
import sys
from pathlib import Path


SCRIPT_INTERFACE = "internal-module"
ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "references" / "oh-my-ppt"
REQUIRED_FILES = (
    "README.md",
    "integration.json",
    "source-reading.md",
    "layout.md",
    "chart.md",
    "data-animation.md",
    "format-catalog.md",
    "LICENSE",
    "NOTICE",
)


def main() -> int:
    checks: list[str] = []

    missing = [name for name in REQUIRED_FILES if not (REFERENCE / name).is_file()]
    if missing:
        print(json.dumps({"status": "FAIL", "missing": missing}, ensure_ascii=False))
        return 1
    checks.append("required files")

    metadata = json.loads((REFERENCE / "integration.json").read_text(encoding="utf-8"))
    if metadata.get("provider") != "oh-my-ppt":
        raise ValueError("integration provider must be oh-my-ppt")
    if metadata.get("upstream", {}).get("repository") != "https://github.com/arcsin1/oh-my-ppt":
        raise ValueError("upstream repository is not pinned")
    if metadata.get("upstream", {}).get("reviewed_commit") != "b937ae5":
        raise ValueError("reviewed upstream commit is not pinned")
    if metadata.get("upstream", {}).get("license") != "Apache-2.0":
        raise ValueError("upstream license is not recorded as Apache-2.0")
    if metadata.get("execution_provider") != "ppt-master":
        raise ValueError("native execution provider must remain ppt-master")
    checks.append("metadata and execution boundary")

    adopted = metadata.get("adopted_modules", [])
    adapters = {
        entry.get("upstream_skill", ""): entry.get("adapter")
        for entry in adopted
        if isinstance(entry, dict)
    }
    for module in ("oh-my-ppt-source-reading", "oh-my-ppt-layout", "oh-my-ppt-chart", "oh-my-ppt-data-anim", "format-layout-skills"):
        adapter = adapters.get(module)
        if not adapter or not (ROOT / adapter).is_file():
            raise ValueError(f"missing adapter for {module}")
    rejected = " ".join(metadata.get("rejected", []))
    if "vendoring" not in rejected.lower():
        raise ValueError("vendoring boundary is not recorded")
    checks.append("adopted and rejected module ledger")

    nested_skills = sorted(str(path.relative_to(REFERENCE)) for path in REFERENCE.rglob("SKILL.md"))
    if nested_skills:
        raise ValueError(f"unexpected nested SKILL.md files: {nested_skills}")
    checks.append("single root Skill boundary")

    sys.path.insert(0, str(ROOT))
    from scripts.route_request import PROVIDERS

    provider = PROVIDERS.get("oh-my-ppt")
    if not provider or provider.get("integrated_reference") != "references/oh-my-ppt":
        raise ValueError("router does not expose the integrated provider")
    checks.append("router discovery metadata")

    print(json.dumps({"status": "PASS", "checks": checks}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
