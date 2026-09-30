# Creation Handoff

## Result

- Skill: `lvsea-ppt` `0.1.2`
- Owner: `海洋哥 / lhylvsea`
- Job: 统一派发 PPT、HTML、图片、SVG、Bento、动画和模板工作流，并以事实、编辑性、渲染和视觉质量门交付。
- Package root: repository root
- Publication target: `lhylvsea/lvsea-ppt`
- Public repository: `https://github.com/lhylvsea/lvsea-ppt`

## Method

This package was authored with the local `lvsea-zao-skill` governed Skill source as the package-authoring authority. The actual validation commands and their results are recorded at handoff time; no claim of provider-backed visual quality is made without a real provider run.

## Provider policy

The package routes to existing provider Skills when available. It does not vendor upstream source, templates, proprietary exporters, fonts, images, or private user material. Each provider keeps its own license and runtime boundary.

## Verification boundary

- Static package checks: route fixtures `PASS: 17/17`; diagram clarification cases `PASS: 3/3`; unit tests `PASS: 11`; Agent Skills quick validator `PASS`; Skill IR generated; context budget `PASS` with root `13,993` bytes.
- Trigger regression: `PASS: 19/19` across positive, negative, near-neighbor and adversarial cases.
- Route regression: deterministic local fixture.
- Provider-backed PPTX/HTML/image run: not part of package creation; mark `missing evidence` unless separately executed.
- Local install acceptance: `Test-SkillInstall.ps1` `PASS` for `lvsea-ppt`, including discoverability, Chinese discovery terms, trigger guidance, examples, usage guidance, boundary notes and route validation.
- Public discovery and clean install: release follow-up gate; record separately from local package checks.

## Tooling honesty

No callable `lvsea-zao-skill` runtime tool was exposed in this task. The local `lvsea-zao-skill` source package supplied the applicable IR export, context sizing and trigger evaluation scripts; its self-package validator/release checker was not used as a generic target validator because it requires the source package name `lvsea-zao-skill` and its own interface contract. The target package was instead checked with the Agent Skills quick validator, route/unit/trigger fixtures and the mandatory local install acceptance script.
