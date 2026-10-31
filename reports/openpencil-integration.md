# OpenPencil Integration Evidence

Date: 2026-10-31
Package: `lvsea-ppt` 0.3.0
Integration mode: semantic adaptation; no upstream source vendored.

## Evidence collected

1. Reviewed the public [OpenPencil repository](https://github.com/ZSeven-W/openpencil) and [openpencil-skill repository](https://github.com/ZSeven-W/openpencil-skill).
2. The local `openpencil-design` Skill is discoverable under the configured Codex Skill roots.
3. The local `op` runtime reported version `0.8.4`.
4. A local headless run successfully created/updated an `.op` design, executed design refinement, embedded a local source image, and exported a PNG preview.
5. The same headless server returned `unknown tool` for `export-deck` and `templates`. Native PPTX export is therefore not claimed as a stable OpenPencil capability in this integration.

## Adopted contract

- `openpencil-design` is a primary authoring provider for explicit OpenPencil requests and high-density one-page `design-reference-native` work.
- `.op` is retained as the canonical PenNode/vector source.
- PNG/SVG are visual derivatives and must be inspected as such.
- PPTX requests keep `ppt-master` as a declared native exporter/fallback; the actual exporter and the final PPTX must be tested in the task run.

## Not adopted

- No OpenPencil Electron source, `node_modules`, templates, fonts, private assets or upstream application bundle was copied into `lvsea-ppt`.
- No claim is made that a PNG preview, an `.op` file or a full-slide raster is a fully editable native PPTX.
- No remote or unreviewed third-party code is executed by the router.

## Remaining evidence gaps

- No independent blind visual review is attached to this Skill package; this report proves local provider capability and routing boundaries, not universal design quality.
- The current headless OpenPencil exporter gap must be rechecked after runtime upgrades.
- A real PPTX delivery still requires separate structural readback, PowerPoint/WPS opening or an equivalent reader, full-slide render, and visual QA.

## Rollback boundary

The integration is isolated to the `lvsea-ppt` provider metadata, route branch, references, tests and reports. Rollback means removing the `openpencil-design` provider branch and restoring the previous package version; the upstream OpenPencil Skill and runtime remain untouched.
