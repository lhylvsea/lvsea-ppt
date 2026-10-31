# Changelog

## 0.3.0 - 2026-10-31

- Added `openpencil-design` as an explicit and high-density one-page vector-authoring provider.
- Kept `.op` as the OpenPencil design source and routed native PPTX delivery through a verified exporter or declared `ppt-master` fallback.
- Added OpenPencil provider metadata, source/output and QA boundaries, trigger coverage, interface metadata, and local integration evidence.
- Did not vendor OpenPencil Electron source, dependencies, templates, or private assets.

## 0.2.0 - 2026-10-25

- Integrated Oh My PPT as a semantic advisory layer for source reading, layout budgeting, charts, declarative animation boundaries and multi-ratio page checks.
- Kept `ppt-master` and other discovered providers responsible for native PPTX generation and export; no upstream Electron source or runtime dependencies were vendored.
- Added router discovery, trigger coverage, integration metadata, license attribution and a local integration validator.

## 0.1.3 - 2026-10-02

- Changed URL/article routing so a web link is treated as source material, not an implicit Bento style.
- Added an explicit Bento opt-in rule and separated template reference from native template filling.
- Added a pre-generation one-page style gate with `design-reference-native`, `editorial-photo`, `timeline-policy` and `bento-info` choices.
- Added route regression coverage for URL, one-page, style-choice and template-reference cases.

## 0.1.2 - 2026-09-30

- Added a clarification gate for broad diagram requests such as 流程图、行程图、路线图、架构图 and 关系图.
- Added semantic-purpose and visual-style menus, including technical-native, hand-drawn, illustrated, editable-vector, interactive-web, Bento and evidence-consulting branches.
- Added explicit-choice, named-provider and "你来定/直接做" bypass rules, with route/unit/evaluation coverage.

## 0.1.1 - 2026-08-19

- Refreshed the generated Skill IR, trigger evaluation and context-budget evidence after the final discovery-contract update.
- Corrected the documented root context measurement to `11,547` bytes; no routing behavior was changed.

## 0.1.0 - 2026-08-19

- Added `lvsea-ppt`, a Chinese-first presentation routing and governance Skill.
- Added routes for native editable PPTX, template filling, evidence-led consulting decks, HTML-first iteration, presenter HTML, Bento one-pagers, image-first visual decks, image-to-editable reconstruction, structured HTML/SVG import, hybrid HTML-to-visual workflows, visual assets and motion HTML.
- Added provider discovery with local availability probing and explicit fallback reporting.
- Added source-to-output contracts, license boundaries, trigger cases, route regression tests, context budget, Skill IR and output evidence reports.
