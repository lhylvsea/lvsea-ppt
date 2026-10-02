---
name: lvsea-ppt
description: "中文优先的 PPT 总调度 Skill：根据内容来源、受众、编辑性、交付格式和视觉风险，在原生可编辑 PPTX、SVG/HTML 到 PPTX、浏览器 HTML PPT、图片型 PPT、手绘技术页、Bento 单页、动画演示和配图资产路线之间选择合适的执行器；网页/URL 默认只作为来源材料，不自动路由 Bento；一页 PPT 未指定版式时先给出推荐风格与可选路线。Use when the user asks to 做PPT、制作演示文稿、生成可编辑PPTX、网页内容转PPT、图片转PPTX、HTML转PPTX、SVG转PPTX、先做HTML再导出PPTX、做图片版PPT、Bento单页、PPT配图、流程图、行程图、路线图、架构图、关系图、示意图或统一派发多个PPT Skill。"
metadata:
  author: "海洋哥 / lhylvsea"
  version: "0.1.3"
  archetype: "vertical-presentation-router"
---

# Lvsea PPT Boss

把本 Skill 当作 PPT 垂类的总调度层，而不是把所有上游项目源码复制成一个巨型渲染器。先锁定交付契约，再选择一个主路由，必要时增加一个协作路由，最后用统一质量门验收。

## 触发条件与调用方式

当用户提出做 PPT、制作演示文稿、生成可编辑 PPTX、图片/截图转 PPTX、HTML/SVG 转 PPTX、先做 HTML 再做视觉终版、网页 PPT、Bento 单页、PPT 配图或多 Skill 派发时调用 `$lvsea-ppt`。只有解释、翻译、只查看或明确不要创建/修改文件的请求不触发本 Skill。

## 1. 默认交付契约

信息已经足够时直接执行，不为了形式追问。默认约定如下；用户本次明确要求优先级更高：

- 中文、16:9 横版、高信息密度、目的明确的版式。
- 正式 PPTX 的常规可见文字不低于 12 pt；HTML 演示正文默认不低于 16 px。
- 标题、正文、数字、单位、图表标签、表格和流程关系尽量保持可编辑；复杂摄影、纹理、插画或高保真视觉允许作为图片组件，但必须记录编辑边界。
- 来源材料只读抽取事实、数字、日期、单位和结论；缺失内容标记待补充，不用模板文案或想象填空。
- 真实图片、截图、产品图、现场图和证据图优先复用原始文件；生成式图片只用于概念、氛围和缺失视觉资产，不伪造事实证据。
- 正式数据、图片和附件落在项目目录的真实文件中，不依赖 localStorage、浏览器缓存或临时生成目录。
- 交付时优先给主文件、可继续编辑源工程、派生预览和验证报告，并明确区分“已调用”“仅配置”“静态通过”和“视觉未核对”。

## 2. 先锁定任务形状

从请求中提取：

1. 目的：汇报、决策、培训、答辩、发布、销售、演讲、异步阅读、网页分享或视觉探索。
2. 来源：主题、Markdown、DOCX、PDF、XLSX、URL、旧 PPTX、PNG/JPG、HTML、SVG、代码库或混合资料。
3. 目标格式：可编辑 PPTX、HTML PPT、PDF、图片型 PPTX、SVG/PNG 图组、Bento 单页或多格式。
4. 编辑性：原生文本/图形可编辑、图片组件可替换、仅浏览器可改，还是只需视觉成品。
5. 受众与风险：制造运营、生产安全、党建党政、经营分析、研究、课程、发布会或创意展示。
6. 迭代方式：一次交付、先看提纲、先看风格预览、先在 HTML 中持续调整，还是按页面逐页确认。

仅在来源、格式或编辑边界改变路由时追问。图/流程图/行程图/路线图/架构图/关系图/示意图若未说明用途或表现方式，先进入 `clarification-required`，列出选项，不擅自猜风格。用户说“你来定”“直接做”“不用确认”时跳过闸门，按默认路线决策并列出关键假设。

## 3. 路由总表

先运行 `scripts/route_request.py` 做确定性初判，再按 `references/route-playbook.md` 做语义复核。路由名是本 Skill 的稳定接口，主执行器必须按当前机器实际发现结果选择。

| 路由 | 典型请求 | 首选执行器 | 主要交付 |
| --- | --- | --- | --- |
| `clarification-required` | 图/流程图/行程图等描述宽泛，未说明用途或表现方式 | 不选 provider，先向用户列出选项 | 语义问题、风格选项、推荐路线、继续执行提示 |
| `native-create` | 从材料或主题生成严肃、可编辑 PPTX | `$ppt-master`；高风险时 `$cyber-ppt` | PPTX、项目源、SVG/预览、QA |
| `native-template-fill` | 套用现有 PPTX/公司模板、保持排版只换内容 | `$ppt-master` Fill Native；`$GordenPPTSkill` | 新 PPTX、填充计划、回读与渲染 |
| `native-enhance` | 保留现有 PPTX 页面，增加备注、动画、旁白或局部增强 | `$ppt-master` Enhance Native | 新 PPTX、变更清单、回归预览 |
| `evidence-consulting` | SCR、战略、生产、安全、经营分析、数据密集 | `$cyber-ppt`；`$ppt-master` | 证据台账、故事线、可编辑 PPTX、严格 QA |
| `html-first-iterate` | 先做 HTML/React/网页 PPT，在浏览器里反复改 | `$open-slide` / `$PPT-as-code` / `$dashiai-ppt` | 可运行 HTML、预览、可选 PPTX 导出 |
| `html-presenter` | 演讲、发布会、杂志风、Swiss、WebGL、讲稿与演讲者视图 | `$guizang-ppt-skill` / `$PPT-as-code` | 单文件或静态 HTML、演讲备注、交互核查 |
| `clarification-required` | URL/文章做一页 PPT 但未指定构图路线 | 暂不选 provider | 生成前推荐风格、四项风格选择、恢复提示 |
| `bento-onepage` | 用户明确要求 Bento、信息卡片或卡片矩阵 | `$bentohttp-ppt` / `$qiaomu-bento-ppt` | 可编辑离线 Bento HTML、内容计划、QA |
| `image-first-visual` | 视觉冲击、图片版 PPT、手绘页、分享型图片 deck | `$baoyu-slide-deck` / `$ppt-image-first` / `$ian-handdrawn-ppt` | PNG 图组、图片型 PPTX/PDF、提示词与预览 |
| `image-to-editable` | 图片、截图、海报、图片 PPT 转可编辑 PPTX | `$GordenImage2PPTX` / `$bggg-creator-image2ppt` | 分层 manifest、可编辑 PPTX、逐页预览 |
| `structured-import` | HTML/SVG/网页设计稿转 PPTX，保留结构和文本编辑性 | `$ppt-master` SVG-first；`$bggg-creator-image2ppt` | SVG/manifest、PPTX、降级说明、QA |
| `hybrid-html-to-visual` | 先用 open-slide/PPT-as-code 迭代，再用 baoyu/图片路线做视觉终版 | HTML 路由主导，图片路线协作 | HTML 源、视觉终版、可选可编辑重建 |
| `visual-asset` | 只需要封面图、章节图、概念图、对比图或背景 | `$ppt-design-prompt` + `imagegen` | 设计规范、提示词、图片资产与版权记录 |
| `motion-html` | 动画 HTML、流程演示、录屏配套、动态 Web 视觉 | `$AI_Animation` / `$frontend-slides` | 可运行 HTML、静态降级、动效检查 |

优先级：用户明确格式/工具 > 输入形态 > 编辑性 > 受众与风险 > 迭代方式 > 默认偏好。不要同时调用所有执行器。

### URL 来源与一页版式闸门

- `http://`、`https://`、网页、公众号和文章链接首先只被视为来源材料，不再自动等同于 Bento。
- 用户明确说 `Bento`、`信息卡片`、`卡片矩阵` 或指定 `$bentohttp-ppt` / `$qiaomu-bento-ppt` 时，才进入 `bento-onepage`。
- 用户要求“做一页 PPT/可编辑 PPTX”但没有说明版式时，先返回 `status=needs-user-choice`，推荐“模板构图参考版”，并给出“模板构图参考版 / 图文叙事版 / 时间轴演进版 / Bento 信息卡片版”四项选择。
- “参考 PPT-Design/DesignPPT.md/公司模板”表示借鉴构图、色系和组件，不等于 `native-template-fill`；只有明确套用、填充、保留原版式或只改文字时才填充现有 PPTX。
- 生成前必须读取本机 `PPT-Design/DesignPPT.md`，再按内容关系选择逻辑图、时间轴、主视觉、流程或其他构图；不得因为输入是 URL 就固定使用仪表盘加卡片矩阵。

风格菜单的实际路由如下：

| 风格 | 适用内容 | 路线 |
| --- | --- | --- |
| `design-reference-native` 模板构图参考版（推荐） | 正式汇报、政策、制造、安全、经营和一般文章 | `native-create`；`ppt-master` / `qiaomu-ppt` |
| `editorial-photo` 图文叙事版 | 新闻、人物、现场和需要保留原文照片的材料 | `native-create`；原生图片与文字混排 |
| `timeline-policy` 时间轴演进版 | 年份、阶段、历程、政策演进和行动路径 | `native-create`；时间轴/阶段带为主骨架 |
| `bento-info` Bento 信息卡片版 | 明确要求 Bento、信息卡片或 HTML 单页 | `bento-onepage`；`bentohttp-ppt` / `qiaomu-bento-ppt` |

### 图形请求的歧义闸门

当请求只说“做一张流程图/行程图/关系图/示意图”，但没有说明图的用途、阅读对象、视觉风格、交付格式或编辑边界时，先发出选择题，不直接生成。机器路由器返回 `status=needs-user-choice`，并提供两个问题：

1. 语义范围：旅行/日程路线、工艺/业务流程、系统/技术架构、战略/项目路线或其他。
2. 表现路线：
   - `technical-native`：中文技术解释图，原生文字/形状/箭头，优先可编辑 PPTX；`ppt-master`、`cyber-ppt`、`qiaomu-ppt`。
   - `handdrawn`：手绘线稿、知识卡、草图感；`ian-handdrawn-ppt`、`ppt-image-first`。
   - `illustrated`：文字配图、插画、场景化信息图；`baoyu-slide-deck`、`ppt-image-first`。
   - `editable-vector`：原生可编辑矢量图或局部 SVG；`ppt-master`、`bggg-creator-image2ppt`、`qiaomu-ppt`。
   - `interactive-web`：HTML、动画、演讲者视图、浏览器交互；`open-slide`、`PPT-as-code`、`guizang-ppt-skill`。
   - `bento`：高密度一页信息图；`bentohttp-ppt`、`qiaomu-bento-ppt`。
   - `evidence-consulting`：SCR、战略、经营、安全或制造证据链图；`cyber-ppt`、`ppt-master`。

用户可回复“中文技术解释图 + 可编辑PPTX”或“手绘式 + 图片型PPT”。出现手绘、技术解释、文字配图、可编辑 PPTX、HTML/动画、Bento、SCR/证据链或明确 provider 后不再重复提问。默认推荐 `technical-native`，便于保留事实、关系和后续编辑能力。

## 4. 关键混合路线

### HTML 先行，再视觉终版

当用户明确要“先用 open-slide 持续改到满意，再用 baoyu-slide-deck 做视觉震撼版本”时：

1. 用 `$open-slide` 或 `$PPT-as-code` 建立内容、页序、导航、备注和可持续修改的 HTML 源。
2. 每次修改只改唯一源文件或 `deck_model`，不要直接改派生截图。
3. 锁定 `slide_plan`、内容事实、风格契约和每页 thesis 后，再由 `$baoyu-slide-deck` 或 `$ppt-image-first` 生成图片终版。
4. 图片终版与 HTML 是两种交付物，不声称像素级同源；若还要可编辑 PPTX，继续走 `$GordenImage2PPTX` 或 `$bggg-creator-image2ppt`，把文字提取为真文本，并明确复杂视觉仍是图片层。
5. 分别验收 HTML 交互、图片视觉和最终 PPTX 结构；图片生成失败时不能用 HTML 截图冒充真实生图证据。

### 图片或截图转可编辑 PPTX

优先建立逐页 `manifest`：画布、背景、框架、图标/装饰、文字、图表、图片、层级和编辑边界。普通文字尽量写成真文本框；复杂背景、插画、图表或无法可靠还原的结构才退化为图片组件。禁止把原图整页铺底后再叠一层重复文字。

### HTML/SVG 转 PPTX

先判断 HTML/SVG 是否有可解析的结构和语义分组。可识别的文本、矩形、路径、线条、图表、图片和分组优先转为 PPT 原生对象；无法安全转换的节点保留为局部 SVG/PNG 组件，不把整页截图当作“可编辑 PPTX”。运行 `$ppt-master` 的源 SVG、导出、PPTX 回读和渲染链；无该执行器时使用 `$bggg-creator-image2ppt` 并报告能力边界。

## 5. 统一质量门

按风险选择轻重，但正式交付至少完成：

1. 事实门：来源、数字、单位、日期、引用和页面主张可回溯。
2. 结构门：页序、页面角色、故事线、标题层级和内容容量合理，避免机械复用四宫格或卡片墙。
3. 编辑门：回读 PPTX，统计可编辑文本/图形/图片，确认复杂元素的降级边界。
4. 几何门：没有越界、遮挡、箭头穿框、孤字、裁切错误、无效大留白或底部导航冲突。
5. 渲染门：正式 PPTX 导出 PNG/PDF，逐页检查，不只看第一页；HTML 打开浏览器并检查缩放、翻页、刷新和必要交互。
6. 视觉门：检查字体、字号、色彩、密度、图片比例、信息焦点和相邻页面节奏；用户要求“调到满意/视觉精修”时必须扩大到逐页视觉复核。
7. 交付门：主文件、源文件、派生物、验证命令、实际运行状态、许可证和未验证项分开说明。

## 6. 路由失败与降级

- 首选 Skill 未发现：检查 `.codex/skills`、`.agents/skills`、环境变量指定的技能根；选择声明过的候选，不静默编造工具。
- 只有 HTML 运行时而用户要 PPTX：完成 HTML 预览后转可用 PPTX exporter；没有真实 exporter 就交付 HTML 并明确阻塞，不把截图改名为 PPTX。
- 只有图片生成能力而用户要可编辑 PPTX：交付图片型 PPTX并继续图片转可编辑路线；图片层与文字层的编辑性必须写入报告。
- 真实来源图片抓取失败：保留来源链接和失败原因，不能用生成图替代事实图片。
- 浏览器或 PowerPoint 无法打开：保留静态校验、文件和日志，标记 `visual_review: skipped`，不猜测通过。

## 7. 中文调用示例

- `用 $lvsea-ppt 把这个网页链接做成一页可编辑 PPTX，保留原文图片。` 首轮应先给出推荐的“模板构图参考版”和其他三项风格，不得直接路由 Bento。
- `用 $lvsea-ppt 把这篇文章做成一页 PPT，采用图文叙事版，参考 PPT-Design 下的模板构图但不要直接套模板。` 直接进入 `native-create`，并保留真实图片和原生文字。
- `用 $lvsea-ppt 把这篇文章做成一页 Bento 信息图。` 仅在明确选择 Bento 后进入 `bento-onepage`。
- `用 $lvsea-ppt 把这篇网页文章做成一页 PPT，你来定风格。` 跳过偏好闸门，采用推荐的“模板构图参考版”，并在假设中写明这一选择。
- `用 $lvsea-ppt 把生产运营月报做成高密度、可编辑 PPTX，按海洋哥偏好的稳重红白风格，保留数据和证据并逐页渲染检查。`
- `用 $lvsea-ppt 先用 open-slide 做 HTML 草稿，浏览器里持续改到满意，再用 baoyu-slide-deck 做视觉终版，最后给我 HTML、图片型 PPTX 和可编辑重建版。`
- `用 $lvsea-ppt 把这组 PPT 截图转成可编辑 PPTX，文字尽量是真文本，复杂背景作为图片组件，并输出逐页 QA。`
- `用 $lvsea-ppt 把这个 SVG/HTML 设计稿转成可编辑 PPTX，先判断哪些节点能转原生对象，不能转的局部保留为 SVG，不要整页截图。`
- `用 $lvsea-ppt 把这篇公众号文章做成一页高密度 Bento HTML，保留来源图片并检查 12 pt 级别可读性。`
- `用 $lvsea-ppt 做一张流程图。`
  - 首轮应先列出“中文技术解释图 / 手绘式 / 文字配图 / 原生可编辑矢量图 / HTML 动画 / Bento / 咨询证据链”等选项，不应直接猜风格。
- `用 $lvsea-ppt 做一张手绘式中文技术流程图，输出图片型 PPTX，后续再考虑可编辑重建。`

## 8. 注意事项、限制与能力边界

- URL、文章、公众号和网页不是版式名称；来源形态不会自动触发 Bento。
- `PPT-Design/DesignPPT.md` 是视觉上位准则，参考模板用于提取构图能力；模板参考、模板填充和 Bento 信息卡片是三种不同契约。
- 本 Skill 是路由与质量总线，不替代每个专业执行器，也不会凭空安装上游工具、创建 MCP 会话、生成外部凭据或保证图片模型可用。
- 上游 Skill 的许可证、模板授权、专有导出器、非商业限制和第三方素材要求继续有效；只抽取方法、路由和质量规则，不把上游源码、模板、图片、商标或私人资料打包进本仓库。
- “HTML 可编辑”不等于“PPTX 原生可编辑”；“PPTX 文件存在”不等于“能打开、可回读或视觉通过”。
- 复杂视觉越接近原图，通常越依赖图片组件；编辑性越高，通常越需要接受局部视觉差异。每次交付要把这个取舍写清楚。
- 静态触发评测、路由器、结构检查和本地报告不能证明所有 provider 已实跑；未调用的执行器必须标记为未调用。
