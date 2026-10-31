# Oh My PPT 数据动画适配

## 优先规则

- 先确定阅读顺序，再决定 `load`、`stagger`、`with`、`after` 或明确的 `click`。
- HTML 路线优先使用 `data-anim` 和 `data-anim-stagger`，动画对象应是完整模块、卡片或图表容器。
- 不使用逐字拆分、无限循环、高频闪烁或无法导出的复杂时间线作为默认交付。
- `PPT.animate` 仅作为 HTML 运行时的有限逃生口；不能把 `anime.js` 或自定义脚本运行成功写成 PPTX 动画已验证。

## PPTX 边界

原生可编辑 PPTX 的动画需由实际 exporter 逐页验证。没有验证时，默认交付静态内容，并把 HTML 预览动画与 PPTX 版本的差异写入报告。
