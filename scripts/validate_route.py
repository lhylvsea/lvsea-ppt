#!/usr/bin/env python3
"""Run the local route fixtures without requiring provider installations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from route_request import choose_route  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate lvsea-ppt route fixtures.")
    parser.add_argument("--cases", default=str(Path(__file__).resolve().parents[1] / "evals" / "trigger_cases.json"))
    args = parser.parse_args()
    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))
    expected = {
        "native_create": "native-create",
        "native_template_fill": "native-template-fill",
        "image_to_editable": "image-to-editable",
        "structured_import": "structured-import",
        "hybrid_html_visual": "hybrid-html-to-visual",
        "bento_onepage": "bento-onepage",
        "evidence_consulting": "evidence-consulting",
        "html_presenter": "html-presenter",
        "visual_asset": "visual-asset",
        "motion_html": "motion-html",
    }
    failures: list[str] = []
    checked = 0
    for case in cases.get("should_trigger", []):
        checked += 1
        got = choose_route(case["text"])["route"]
        want = expected[case["family"]]
        if got != want:
            failures.append(f"trigger: {case['text']} -> {got}, expected {want}")
    for case in cases.get("should_not_trigger", []):
        checked += 1
        result = choose_route(case["text"])
        if result["route"] != "native-create":
            failures.append(f"negative: {case['text']} -> {result['route']}")
    if failures:
        print(json.dumps({"status": "FAIL", "checked": checked, "failures": failures}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"status": "PASS", "checked": checked, "failures": []}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
