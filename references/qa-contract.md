# Unified QA Contract

## Required evidence

Every formal run should leave a compact record of:

- source files and source hash or source locator;
- content/evidence ledger and unresolved gaps;
- route decision and provider availability;
- page count, canvas and target format;
- editable-object classification;
- render commands and output paths;
- visual review status and known limitations.

## Diagram route checks

- Broad requests such as “流程图/行程图/路线图/架构图/关系图” must pause at `clarification-required` when purpose or presentation style is missing.
- The response must expose a semantic question when “行程图/路线图” can mean travel, process, system or strategy, and must expose the seven style branches with their next route and provider candidates.
- Explicit style, format, provider or “你来定/直接做” instructions must not be blocked by a redundant clarification question.
- The selected diagram style and editability boundary must be copied into the later route decision and final QA record.

## Native PPTX checks

- Opens with `python-pptx`, PowerPoint, WPS or the provider's documented reader.
- Slide count and order match the approved plan.
- Text readback contains no placeholder copy, duplicate hidden text or stale default labels.
- Minimum visible font is normally 12 pt; smaller text requires an explicit exception.
- No shape or text box crosses the slide bounds; no footer/nav collision.
- Charts/tables are native only when the provider's contract and readback prove it; otherwise report fallback image/SVG.
- Render every slide to PNG/PDF and inspect all pages, not only page 1.

## HTML checks

- Open the actual local URL or file, not only source syntax.
- Confirm page navigation, refresh, scaling and any claimed inspector/comment, speaker or export control.
- Check 16:9 framing, overflow, title hierarchy, responsive crop and reduced-motion/static fallback when motion exists.
- If an HTML page is later used as PPTX source, record which nodes were parsed and which were rasterized.

## Image-first checks

- Prompt files and image-generation manifest exist before generation.
- Each page image is independently present, has the intended ratio, and is visually reviewed.
- Text baked into images is not silently patched with code; regenerate or use an editable text layer.
- Image-only PPTX is labeled `image-backed`, not `fully editable`.

## Stop conditions

Stop or downgrade the claim when:

- source facts cannot be read;
- provider is unavailable and no declared fallback matches the output contract;
- a requested editable output is only a full-slide screenshot;
- render preview was not possible;
- user-provided content would be overwritten without a backup;
- third-party license or asset rights are unclear.
