# Route Playbook

## 1. Precedence

Use the first decisive signal in this order:

1. Explicit output format or named provider.
2. Input shape: existing PPTX, image, SVG/HTML, URL/article, source document, or free topic.
   A URL/article is an input source, not a visual style; it must not imply Bento by itself.
3. Editability requirement: native editable, partially editable, browser-editable, or image-only.
4. Diagram ambiguity gate: if the request only names a broad diagram, pause and ask for semantic scope and presentation style.
5. Risk and audience: evidence-heavy/official/production/safety versus creative/demo.
6. Iteration mode: one-shot, preview-first, browser loop, or page-by-page approval.
7. Default local preference: `ppt-master` for editable PPTX and `CyberPPT` for evidence-heavy work.

Do not ask the user to choose a route when the signals already resolve it. Ask only when two routes have materially different output contracts and the request does not reveal which one is wanted. “你来定/直接做/不用确认” explicitly bypasses the diagram gate and uses the recommended default.

## 2. Deterministic route rules

| Signals | Route | Primary candidate | Collaborator / fallback |
| --- | --- | --- | --- |
| broad `图/流程图/行程图/路线图/架构图/关系图/示意图` without purpose/style | `clarification-required` | none before user choice | return semantic question + style menu |
| `图片/截图/海报/PPT图片` + `可编辑/PPTX` | `image-to-editable` | `GordenImage2PPTX`, `bggg-creator-image2ppt` | `ppt-master` QA |
| `HTML/SVG` + `PPTX/PowerPoint/可编辑` | `structured-import` | `ppt-master` | `bggg-creator-image2ppt` |
| `现有PPTX/模板/套用/保留排版/只改文字` | `native-template-fill` | `ppt-master`, `GordenPPTSkill` | `CyberPPT` only for evidence review |
| `备注/旁白/转场/动画` + existing PPTX | `native-enhance` | `ppt-master` | provider-specific post-process |
| `SCR/证据链/战略/经营/生产/安全/数据密集` | `evidence-consulting` | `cyber-ppt` | `ppt-master` |
| `open-slide/React/HTML先行/浏览器持续改` | `html-first-iterate` | `open-slide`, `PPT-as-code` | `dashiai-ppt` |
| `杂志/Swiss/WebGL/演讲者视图/发布会` | `html-presenter` | `guizang-ppt-skill`, `PPT-as-code` | `open-slide` |
| explicit `Bento`/`信息卡片`/`卡片矩阵` | `bento-onepage` | `bentohttp-ppt`, `qiaomu-bento-ppt` | `ppt-master` for multi-page PPTX |
| `图片版/视觉震撼/手绘/baoyu/图片PPT` | `image-first-visual` | `baoyu-slide-deck`, `ppt-image-first`, `ian-handdrawn-ppt` | `GordenImage2PPTX` if editable |
| `先HTML再图片终版/open-slide + baoyu` | `hybrid-html-to-visual` | HTML provider | image provider, then optional reconstruction |
| `封面图/章节图/概念图/PPT配图` without deck | `visual-asset` | `ppt-design-prompt` | `imagegen` |
| `动画HTML/录屏/动态流程` | `motion-html` | `AI_Animation`, `frontend-slides` | static HTML fallback |
| no decisive signal, PPT requested | `native-create` | `ppt-master` | `cyber-ppt` when source risk is high |

## 2.1 Diagram ambiguity gate

The gate applies to creation requests containing broad diagram nouns such as `流程图`, `行程图`, `路线图`, `架构图`, `关系图`, `示意图`, `逻辑图`, `信息图`, `工艺图` or `图解`.

Return `route=clarification-required` and `status=needs-user-choice` when the user has not supplied a style, format, editability, named provider or a direct default instruction. The machine-readable response must include:

- `clarification.questions`: one semantic question for ambiguous `行程图/路线图`, plus one style question when style is missing;
- `clarification.recommended_choice`: `technical-native`;
- `clarification.resume_prompt`: a short example that lets the user answer in one line;
- `choices[].route` and `choices[].providers`: the next route and the original Skill branches behind it.

The style menu is intentionally explicit:

| Choice | Meaning | Route / source branches |
| --- | --- | --- |
| `technical-native` | 中文技术解释图，原生文本、形状和箭头 | `native-create`: `ppt-master`, `cyber-ppt`, `qiaomu-ppt` |
| `handdrawn` | 手绘线稿、知识卡、草图感 | `image-first-visual`: `ian-handdrawn-ppt`, `ppt-image-first` |
| `illustrated` | 文字配图、插画、场景化信息图 | `image-first-visual`: `baoyu-slide-deck`, `ppt-image-first` |
| `editable-vector` | 原生可编辑矢量或局部 SVG | `structured-import`: `ppt-master`, `bggg-creator-image2ppt`, `qiaomu-ppt` |
| `interactive-web` | HTML、动画、演讲者视图、浏览器交互 | `html-first-iterate`: `open-slide`, `PPT-as-code`, `guizang-ppt-skill` |
| `bento` | 高密度一页信息图 | `bento-onepage`: `bentohttp-ppt`, `qiaomu-bento-ppt` |
| `evidence-consulting` | SCR、战略、经营、安全、制造证据链 | `evidence-consulting`: `cyber-ppt`, `ppt-master` |

Explicit signals such as “手绘式”“中文技术解释”“文字配图”“可编辑 PPTX”“HTML 动画”“Bento”“SCR/证据链” count as a choice and must not trigger a redundant clarification. An explicit provider name also bypasses the gate.

### 2.2 URL/article one-page style gate

When a request combines a URL/article/公众号 source with “一页 PPT”, “单页 PPTX”,
“一页可视化” or equivalent language but does not name a visual style, return
`route=clarification-required` and `status=needs-user-choice` before provider
selection. The response must include `clarification.kind=onepage-style`, a
`recommended_style`, and these four actionable choices:

| Choice | Composition contract | Route |
| --- | --- | --- |
| `design-reference-native` | Read `PPT-Design/DesignPPT.md`, sample the local logic/template decks, then rebuild a native editable page around one dominant visual and the content relationship. | `native-create` |
| `editorial-photo` | Use relevant original photos/scene images as the visual narrative, with title, quote and a few thematic blocks. | `native-create` |
| `timeline-policy` | Make dates, phases, evolution or action path the main spine; use images as evidence, not decoration. | `native-create` |
| `bento-info` | Use an information-card or card-matrix composition and the Bento HTML route. | `bento-onepage` |

The default recommendation is `design-reference-native` for formal, policy,
manufacturing, safety, management and general source articles. It may be
overridden by visible time/phase signals or explicit news/people/story signals.
“参考模板” means borrowing composition and tokens; only “套用/填充/保留原
版式/只改文字” selects `native-template-fill`. A direct instruction such as
“你来定/直接做” bypasses the preference gate and records the recommended style
in the route result.

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
