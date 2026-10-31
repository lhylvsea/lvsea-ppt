# Synthesis Ledger

## Keep

- Route by output contract rather than by brand name.
- Keep one primary provider and only necessary collaborators.
- Separate content/evidence planning from visual execution.
- Preserve a canonical source artifact and make HTML/SVG/PPTX/PNG derivatives explicit.
- Prefer native text, charts, tables and vectors when safe; use bounded image components for complex visuals.
- Use preview-first and confirmation gates for style-sensitive or expensive image workflows.
- Keep prompt files, manifests, slide plans, source cards and QA reports as reproducibility records.
- Render every formal page and distinguish static, browser, provider and human evidence.

## Adapt

- Adapt `ppt-master`'s route ownership and native/template/SVG boundaries into a provider-neutral router.
- Adapt `qiaomu-ppt`'s source manifest, source cards, visual asset plan and multi-format delivery into a cross-provider contract.
- Adapt `CyberPPT`'s evidence/SCR/strict QA for high-risk decks without forcing every lightweight deck through the heaviest gate.
- Adapt `open-slide`, `PPT-as-code`, `dashi`, `guizang`, `gaiduo` and `bento` as HTML routes, not as native PPTX substitutes.
- Adapt `baoyu`, `ppt-image-first`, `ian-handdrawn` and Gorden image workflows as image-first routes with explicit editability downgrade.
- Adapt `lvsea-zao-skill`'s governed package, trigger eval, IR, context budget and branch/PR/Release/clean-install gates.

### Oh My PPT adapter

- Keep: source-grounded reading, explicit page/layout budgets, deterministic chart inputs, declarative animation boundaries and multi-ratio format checks.
- Adapt: convert the upstream skill guidance into small, on-demand reference files and expose it as an advisory collaborator in the router.
- Reject: vendoring the Electron application, runtime dependencies, build output, templates, fonts, images or private assets; treating HTML preview or `data-anim` as proof of native PPTX editability.
- Invent: the local `integration.json` contract, `validate_oh_my_ppt_integration.py` check and the explicit `ppt-master` execution boundary.

### OpenPencil adapter

- Keep: PenNode/vector authoring, `design`/`design:refine` iteration, `.op` source retention and PNG/SVG preview.
- Adapt: expose `openpencil-design` only for explicit OpenPencil requests or high-density one-page vector composition; preserve `ppt-master` for verified native PPTX export or fallback.
- Reject: vendoring OpenPencil Electron, runtime dependencies, templates, fonts, images or private assets; treating `.op` or PNG preview as native PPTX editability.
- Invent: runtime exporter probing, OpenPencil-specific output boundary, route regression and a local capability-gap report.

## Reject

- Reject “copy every upstream repository into one super Skill”. It creates license, size, update and duplicate-source problems.
- Reject calling a screenshot, PDF or full-slide raster “fully editable PPTX”.
- Reject running unreviewed remote install hooks or third-party scripts merely to learn from them.
- Reject using AI-generated images for factual evidence, product screenshots, diagrams or process parameters without a human/source basis.
- Reject making every deck use the same four-grid, ring or card-wall structure.
- Reject publishing personal template assets, proprietary exporters, private attachments or absolute local paths.

## Invent

- A deterministic cross-provider route vocabulary (`native-create`, `structured-import`, `hybrid-html-to-visual`, etc.).
- Availability-aware provider selection that reports missing providers instead of inventing calls.
- One compact editable-boundary vocabulary: `native-text`, `native-shape`, `vector-component`, `image-component`, `full-slide-raster`.
- A single QA contract shared by native PPTX, HTML, SVG and image-first branches.
- A specific bridge for the user's preferred workflow: HTML iteration first, visual raster edition second, optional editable reconstruction third.
