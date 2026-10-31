# Creation Handoff

## Result

- Skill: `lvsea-ppt` `0.3.0`
- Owner: `海洋哥 / lhylvsea`
- Job: 统一派发 PPT、HTML、图片、SVG、Bento、动画、模板和 OpenPencil 矢量构图工作流，并以事实、编辑性、渲染和视觉质量门交付。
- Package root: repository root
- Publication target: `lhylvsea/lvsea-ppt`
- Public repository: `https://github.com/lhylvsea/lvsea-ppt`

## Method

This package was authored with the local `lvsea-zao-skill` governed Skill source as the package-authoring authority. The actual validation commands and their results are recorded at handoff time; no claim of provider-backed visual quality is made without a real provider run.

## Provider policy

The package routes to existing provider Skills when available. It does not vendor upstream source, templates, proprietary exporters, fonts, images, or private user material. Each provider keeps its own license and runtime boundary.

## Verification boundary

- Static package checks: route fixtures `PASS: 22/22`; unit tests `PASS: 22`; Skill IR generated; context budget `WARN` with root `19,693` bytes, below the 20,000-byte block threshold but above the 14,000-byte production recommendation.
- Trigger regression: `PASS: 22/22` across positive, negative, near-neighbor and adversarial cases, including the Oh My PPT and OpenPencil cases.
- Route regression: deterministic local fixture.
- Provider-backed PPTX/HTML/image run: not part of package creation; mark `missing evidence` unless separately executed.
- Local install acceptance: the earlier `0.2.0` install record passed; `Test-SkillInstall.ps1` was not rerun for this local-only `0.3.0` integration, so that historical result is not counted as current package acceptance.
- Public discovery and clean install: release follow-up gate; record separately from local package checks.

## Oh My PPT integration handoff

- Upstream: `https://github.com/arcsin1/oh-my-ppt`, reviewed at `b937ae5`, Apache-2.0.
- Integration mode: semantic adapter under `references/oh-my-ppt/`; no upstream application source or runtime dependencies are vendored.
- Adopted modules: source reading, layout, charts, data animation and multi-ratio format guidance.
- Execution boundary: advisory collaborator only; use a separately discovered provider, with `ppt-master` as the preferred native PPTX executor.
- Local acceptance: `scripts/validate_oh_my_ppt_integration.py`, route fixture and unit test coverage must pass before publication.

## OpenPencil integration handoff

- Upstream: `https://github.com/ZSeven-W/openpencil` and `https://github.com/ZSeven-W/openpencil-skill`.
- Integration mode: semantic adapter under `references/openpencil.md`; no upstream application source or runtime dependencies are vendored.
- Adopted boundary: `openpencil-design` is authoring-first for explicit/high-density one-page work; `.op` is retained as the canonical design source.
- Native export boundary: the local `op 0.8.4` headless run produced `.op`/PNG design output, while `export-deck` and `templates` returned `unknown tool`; PPTX remains a separately probed `ppt-master` fallback.
- Local acceptance: OpenPencil route fixture, unit tests, provider discovery and `reports/openpencil-integration.md` pass; no universal PPTX exporter claim is made.

## Tooling honesty

No callable `lvsea-zao-skill` runtime tool was exposed in this task. The local `lvsea-zao-skill` source package supplied the applicable IR export, context sizing and trigger evaluation scripts. Its self-package validator/release checker was also inspected against the target and correctly reported that it expects the source package name `lvsea-zao-skill` and `agents/interface.yaml`; that result is not counted as target acceptance. The target package was checked with the custom integration validator, route/unit/trigger fixtures and the mandatory local install acceptance script.
