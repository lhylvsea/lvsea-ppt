# Route Playbook

## 1. Precedence

Use the first decisive signal in this order:

1. Explicit output format or named provider.
2. Input shape: existing PPTX, image, SVG/HTML, URL/article, source document, or free topic.
3. Editability requirement: native editable, partially editable, browser-editable, or image-only.
4. Risk and audience: evidence-heavy/official/production/safety versus creative/demo.
5. Iteration mode: one-shot, preview-first, browser loop, or page-by-page approval.
6. Default local preference: `ppt-master` for editable PPTX and `CyberPPT` for evidence-heavy work.

Do not ask the user to choose a route when the signals already resolve it. Ask only when two routes have materially different output contracts and the request does not reveal which one is wanted.

## 2. Deterministic route rules

| Signals | Route | Primary candidate | Collaborator / fallback |
| --- | --- | --- | --- |
| `图片/截图/海报/PPT图片` + `可编辑/PPTX` | `image-to-editable` | `GordenImage2PPTX`, `bggg-creator-image2ppt` | `ppt-master` QA |
| `HTML/SVG` + `PPTX/PowerPoint/可编辑` | `structured-import` | `ppt-master` | `bggg-creator-image2ppt` |
| `现有PPTX/模板/套用/保留排版/只改文字` | `native-template-fill` | `ppt-master`, `GordenPPTSkill` | `CyberPPT` only for evidence review |
| `备注/旁白/转场/动画` + existing PPTX | `native-enhance` | `ppt-master` | provider-specific post-process |
| `SCR/证据链/战略/经营/生产/安全/数据密集` | `evidence-consulting` | `cyber-ppt` | `ppt-master` |
| `open-slide/React/HTML先行/浏览器持续改` | `html-first-iterate` | `open-slide`, `PPT-as-code` | `dashiai-ppt` |
| `杂志/Swiss/WebGL/演讲者视图/发布会` | `html-presenter` | `guizang-ppt-skill`, `PPT-as-code` | `open-slide` |
| `公众号/URL/文章/一页/Bento` | `bento-onepage` | `bentohttp-ppt`, `qiaomu-bento-ppt` | `ppt-master` for multi-page PPTX |
| `图片版/视觉震撼/手绘/baoyu/图片PPT` | `image-first-visual` | `baoyu-slide-deck`, `ppt-image-first`, `ian-handdrawn-ppt` | `GordenImage2PPTX` if editable |
| `先HTML再图片终版/open-slide + baoyu` | `hybrid-html-to-visual` | HTML provider | image provider, then optional reconstruction |
| `封面图/章节图/概念图/PPT配图` without deck | `visual-asset` | `ppt-design-prompt` | `imagegen` |
| `动画HTML/录屏/动态流程` | `motion-html` | `AI_Animation`, `frontend-slides` | static HTML fallback |
| no decisive signal, PPT requested | `native-create` | `ppt-master` | `cyber-ppt` when source risk is high |

## 3. Provider selection

For each route, select the first provider whose skill directory or explicitly documented command is actually discoverable. The router reports unavailable candidates rather than claiming they ran. An unavailable preferred provider may be replaced only by a declared fallback with the same output contract.

Provider availability roots are discovered in this order:

1. `LVSEA_SKILLS_ROOTS` (path-separated list).
2. `$CODEX_HOME/skills`.
3. `$USERPROFILE/.codex/skills`.
4. `$USERPROFILE/.agents/skills`.

The public package does not assume a fixed username or copy local skill folders into itself.

## 4. Hybrid workflow rules

### HTML -> visual final

The HTML deck is the canonical source during iteration. Freeze `deck_model`, `slide_plan`, content facts, and the design contract before dispatching raster generation. The generated images are a derived visual edition, not a hidden replacement of the HTML source.

### Visual final -> editable PPTX

Use image-to-editable reconstruction only after the image edition is approved. Keep text as native text whenever reliable; keep complex visuals as bounded image/SVG components. Report the percentage or count of native editable objects when the provider can measure it.

### SVG/HTML -> editable PPTX

Parse semantic DOM/SVG groups first. Prefer text, paths, rectangles, lines, charts and media as native or vector objects. If a whole page cannot be safely mapped, split the page into local components; do not call a full-page screenshot editable.

## 5. Checkpoint policy

- `evidence-consulting`, `image-first-visual`, `html-first-iterate` and `gaiduo`-style staged workflows preserve their own confirmation gates.
- A direct request such as “直接生成” or “你来定” can waive preference checkpoints for that run, but never waives factual, editability, render or security gates.
- A user request to “调到满意” upgrades visual QA to all-page review and requires a repair loop.
