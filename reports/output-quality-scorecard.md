# Output Quality Scorecard

This report is intentionally evidence-bound. Package-level checks prove the router and documentation contract; they do not prove that every upstream provider can render a beautiful deck on every host.

| Dimension | Gate | Evidence | Status |
| --- | --- | --- | --- |
| Source fidelity | provider run or source review | `references/provider-matrix.md`, source ledgers | `source-reviewed; provider-run missing` |
| Trigger boundary | positive, negative, near-neighbor and adversarial fixtures | `reports/trigger-eval.json` | `PASS: 19/19` |
| Route correctness | deterministic cases | `scripts/route_request.py`, `evals/trigger_cases.json` | `PASS: 14/14` |
| Package structure | Agent Skills quick validator | `quick_validate.py`, `reports/skill-ir.json` | `PASS` |
| Context budget | measured bytes | `reports/context-budget.json` | `PASS: root 11,547 bytes` |
| PPTX editability | native readback | provider-specific evidence | `missing evidence` |
| HTML interaction | browser run | provider-specific evidence | `missing evidence` |
| Raster visual quality | rendered pages + human review | provider-specific evidence | `missing evidence` |
| License boundary | source/asset audit | `references/license-boundaries.md` | `source-reviewed` |
