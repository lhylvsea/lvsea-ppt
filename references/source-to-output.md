# Source to Output Contract

## Input matrix

| Source | User intent | Preferred output | Primary route |
| --- | --- | --- | --- |
| Topic / notes / DOCX / PDF / XLSX | serious editable deck | PPTX + project + QA | `native-create` or `evidence-consulting` |
| Existing PPTX template | reuse visual shell | new PPTX, original untouched | `native-template-fill` |
| PNG/JPG/PPT screenshots | edit text and move components | layered editable PPTX | `image-to-editable` |
| HTML/React deck | browser iteration | HTML first, optional PPTX | `html-first-iterate` |
| SVG design | preserve vector/semantic groups | SVG source + PPTX | `structured-import` |
| Article / URL / WeChat | one-page summary without a named style | style-choice gate first, then native PPTX or explicit Bento HTML | `clarification-required` -> `native-create` / `bento-onepage` |
| Article / URL / WeChat | explicit Bento / information cards | offline editable Bento HTML | `bento-onepage` |
| Article / URL / WeChat | ordinary PPT/PPTX or multi-page deck | native editable PPTX + source + QA | `native-create` |
| abstract visual idea | visual storytelling | PNG assets or image deck | `visual-asset` / `image-first-visual` |

## URL/article style boundary

An article, URL or WeChat page identifies the source material only. For a one-page
PPT request without a named style, pause before provider selection and recommend
`design-reference-native` after reading the local `PPT-Design/DesignPPT.md`.
Use `editorial-photo`, `timeline-policy` or `bento-info` only when selected or
when a direct “you decide” instruction accepts the recorded recommendation.

## Editable boundary

Classify every visible object as one of:

- `native-text`: editable text box or run.
- `native-shape`: editable PowerPoint shape/path/chart/table.
- `vector-component`: SVG or vector object that remains replaceable but may not be individually editable in PowerPoint.
- `image-component`: bounded photo, texture, illustration, screenshot or complex visual.
- `full-slide-raster`: one image for the whole page; only use when the user explicitly accepts image-only output.

The delivery report must count or list these categories when the chosen provider can measure them. Never use `full-slide-raster` and call the result fully editable.

## Export ladder

1. Canonical source: content/evidence/slide plan + HTML/SVG/manifest/project.
2. Editable derivative: PPTX with text and safe native objects.
3. Visual derivative: PNG/JPG contact sheet or PDF.
4. Share derivative: static HTML or offline Bento.

Always keep the canonical source and editable derivative together. A screenshot or PDF is never the only backup for a requested editable deliverable.
