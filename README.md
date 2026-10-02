# lvsea-ppt

中文优先的 PPT 垂类总调度 Skill。它不把几十个 PPT 项目粗暴拼成一个巨型生成器，而是根据输入来源、交付格式、编辑性、受众和视觉风险，选择最合适的专业路线，再统一做事实、结构、渲染和视觉验收。

## 解决什么问题

同一句“帮我做 PPT”，可能实际需要完全不同的技术路线：

- 经营分析、安全生产、制造运营：需要证据链、SCR、数据和真正可编辑的 PPTX。
- 公司模板填充：需要保留原生版式，只替换文本、表格或图表数据。
- HTML/React 先行：需要在浏览器中快速修改、预览、评论和演示。
- 图片或截图转 PPTX：需要分离文字、背景、框架和装饰，而不是整页铺图。
- 视觉冲击型图片 PPT：需要提示词、逐页生图、PNG/PDF/图片型 PPTX，未必需要原生编辑。
- SVG/HTML 设计稿转 PPTX：需要判断哪些节点能转为原生对象，哪些只能保留为局部图片。

`lvsea-ppt` 负责做这个判断，并在交付前把“源文件、派生物、编辑边界、实际验证状态”说清楚。

## 安装

### Agent Skills 安装

```bash
npx skills add lhylvsea/lvsea-ppt --skill lvsea-ppt
```

安装后重启 Agent，再用：

```text
用 $lvsea-ppt 选择最合适的 PPT 路线，保留可编辑源文件并完成验证。
```

Windows 本机也可以把仓库目录安装到：

```text
C:\Users\<用户名>\.codex\skills\lvsea-ppt
```

具体执行器仍需单独安装或在本机已经存在；总调度器不会把所有上游依赖偷偷打包进来。

## 路由总览

| 用户目标 | 主路线 | 常见执行器 | 交付重点 |
| --- | --- | --- | --- |
| 图/流程图描述不清 | `clarification-required` | 暂不选 provider | 先确认语义范围、表现风格和编辑边界 |
| URL/文章做一页 PPT 但未指定版式 | `clarification-required` | 暂不选 provider | 推荐版式、四项风格选择、可恢复提示 |
| 新建可编辑 PPTX | `native-create` | `ppt-master` / `cyber-ppt` | 内容证据、SVG/PPTX、逐页 QA |
| 套公司模板 | `native-template-fill` | `ppt-master` Fill Native / `GordenPPTSkill` | 保留版式、填充计划、回读 |
| 严肃经营/安全/战略汇报 | `evidence-consulting` | `cyber-ppt` | SCR、证据表、严格检查 |
| HTML 先行持续修改 | `html-first-iterate` | `open-slide` / `PPT-as-code` / `dashiai-ppt` | HTML 源、浏览器迭代、可选导出 |
| 演讲者视图/杂志/Swiss | `html-presenter` | `guizang-ppt-skill` / `PPT-as-code` | 讲稿、导航、演示交互 |
| 明确要求 Bento/信息卡片一页 | `bento-onepage` | `bentohttp-ppt` / `qiaomu-bento-ppt` | 1280x720、密度、来源图片 |
| 图片/截图转可编辑 | `image-to-editable` | `GordenImage2PPTX` / `bggg-creator-image2ppt` | 文字真编辑、组件层、manifest |
| HTML/SVG 转 PPTX | `structured-import` | `ppt-master` SVG-first | 原生对象优先、局部 SVG 降级 |
| 图片型视觉终版 | `image-first-visual` | `baoyu-slide-deck` / `ppt-image-first` / `ian-handdrawn-ppt` | 逐页 PNG、提示词、图片型 PPTX |
| HTML -> 视觉终版 | `hybrid-html-to-visual` | `open-slide` + `baoyu-slide-deck` | 双源交付、再决定是否重建可编辑版 |

完整路由规则见 [`references/route-playbook.md`](references/route-playbook.md)，执行器能力与许可证见 [`references/provider-matrix.md`](references/provider-matrix.md)。

## URL 来源不会自动变成 Bento

URL、网页、公众号和文章链接首先是内容来源，不是版式信号。请求“把网页做成一页 PPT/可编辑 PPTX”时，路由器会在生成前暂停，推荐 `design-reference-native`“模板构图参考版”，并提供四项可选路线：

1. `design-reference-native` 模板构图参考版（推荐）：读取 `PPT-Design/DesignPPT.md`，按内容关系借鉴逻辑图和模板的构图、色系与组件，重新生成原生可编辑 PPTX。
2. `editorial-photo` 图文叙事版：用原文真实照片、现场图或人物图做主视觉，配合引语与主题段落。
3. `timeline-policy` 时间轴演进版：以年份、阶段、政策演进或行动路径为主骨架。
4. `bento-info` Bento 信息卡片版：只有用户明确选择 Bento、信息卡片或卡片矩阵时才启用。

“参考模板”与“套用模板”是两种不同请求：前者走 `native-create`，后者只有在明确“套用/填充/保留原版式/只改文字”时才走 `native-template-fill`。用户回复“你来定/直接做”时，路由器采用推荐风格并记录假设。

## 图形请求如何选择

“流程图”“行程图”“路线图”“架构图”“关系图”“示意图”不是单一产物。没有明确风格时，路由器会暂停 provider 选择，并让用户从以下分支中选择：

| 选择 | 适合什么 | 典型路线 |
| --- | --- | --- |
| 中文技术解释图 | 工艺、设备、系统、培训、业务流程 | 原生可编辑 PPTX，`ppt-master` / `cyber-ppt` |
| 手绘式 | 草图、知识卡、轻量技术叙事 | `ian-handdrawn-ppt` / `ppt-image-first` |
| 文字配图/插画式 | 场景化说明、视觉传播、概念图 | `baoyu-slide-deck` / `ppt-image-first` |
| 原生可编辑矢量图 | 文字、路径、箭头、分组需要继续修改 | `ppt-master` / `bggg-creator-image2ppt` |
| HTML/动画交互图 | 浏览器演示、动画、录屏、演讲者视图 | `open-slide` / `PPT-as-code` / `guizang-ppt-skill` |
| 一页 Bento 信息图 | 文章、URL、公众号或管理摘要 | `bentohttp-ppt` / `qiaomu-bento-ppt` |
| 咨询/证据链图 | SCR、战略、经营、安全、制造分析 | `cyber-ppt` / `ppt-master` |

如果用户明确说“你来定/直接做”，默认采用“中文技术解释图 + 原生可编辑 PPTX”，并在交付中记录这一假设。

## 四个真实应用场景

### 1. 制造运营月度汇报

输入会议纪要、产销数据、库存安排、异常清单和旧模板。路由到 `evidence-consulting` 或 `native-template-fill`，先建立事实和指标口径，再生成可编辑 PPTX，渲染全部页面并回读数字、单位和最小字号。

### 2. 安全生产专题培训

输入制度、事故复盘、风险点、操作规程和现场图片。优先 `native-create`/`evidence-consulting`；现场图作为真实证据图片，流程和责任边界用原生对象表达，不用生成图伪造设备、事故或工艺参数。

### 3. HTML 先迭代，图片终版再交付

先用 `open-slide` 或 `PPT-as-code` 做内容结构、页序、讲稿和浏览器预览；用户满意后，用 `baoyu-slide-deck` 或 `ppt-image-first` 生成视觉终版。HTML、PNG/PDF、图片型 PPTX 是不同产物；用户仍要求可编辑时，再接 `GordenImage2PPTX`/`bggg-creator-image2ppt`，并记录图片层与文本层边界。

### 4. 图片/HTML/SVG 设计稿还原为可编辑 PPTX

先生成逐页 manifest，判断文字、图形、路径、图片和复杂背景。能安全转换的节点进入原生 PPTX，无法转换的局部作为 SVG/PNG 组件，最后验证 PPTX 可打开、文本可回读、图片比例正确且没有重复文字。

## 统一验收

正式交付至少检查：

1. 来源事实、数字、日期、单位与引用位置。
2. 页序、页面角色、标题层级和信息密度。
3. PPTX 可打开、文本可回读、编辑对象数量和降级边界。
4. 全部页面渲染图的越界、遮挡、裁切、字体、颜色、空白和底部安全区。
5. HTML 的翻页、缩放、刷新、演讲者视图、评论或导出功能（只检查实际存在的功能）。

## 研究与边界

本次研究了用户提供的公开项目，并将方法归纳为 `keep / adapt / reject / invent` 台账。没有把上游源码、模板、图片、商标或专有导出器复制进本仓库。`dashi-ppt-skill` 含 AGPL-3.0 与专有导出组件；`qiaomu-ppt`、`guizang-ppt-skill` 采用 AGPL；`GordenPPTSkill` 的 Skill 文档明确提示个人/研究用途；因此本仓库只做路由和方法抽取，使用上游执行器时仍需遵守其许可。

`axi-front-design-skill` 在本次核查日期（2026-08-19）返回 404，未作为可用 provider；其名称只保留在研究报告中，不在运行时路由中冒充已安装工具。

## 本地验证

```powershell
python scripts/route_request.py --text "把这组 PPT 截图转成可编辑 PPTX" --json
python scripts/validate_route.py --cases evals/trigger_cases.json
python -m unittest discover -s tests -p "test*.py"
```

Skill 包级验证、IR、上下文预算和发布门禁由 `lvsea-zao-skill` 的工具执行。详见 [`reports/creation-handoff.md`](reports/creation-handoff.md)。

## 许可证

本仓库新增的总调度与文档代码采用 MIT，详见 [`LICENSE`](LICENSE)。上游 provider 的许可证、模板限制、专有组件和第三方素材权利不因本仓库的路由而改变。
