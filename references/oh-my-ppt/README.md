# Oh My PPT 集成适配层

本目录把 [arcsin1/oh-my-ppt](https://github.com/arcsin1/oh-my-ppt) 的可复用方法整合到 `lvsea-ppt` 的路由与质量边界中。它是语义适配层，不是上游 Electron 应用的源码镜像。

## 已吸收

- 来源阅读：只使用主机明确提供的文件或检索片段；逐步定位标题、事实、数字、日期和术语；缺失事实不猜测。
- 页面布局：先锁定 3 秒主旨、页面角色、阅读路径、内容形状和密度，再选择布局模式并计算画布预算。
- 图表：先判断图表是否真的能表达关系；为图表保留明确高度；标签、单位和数据必须与来源一致。
- 动画：HTML 路线优先使用声明式 `data-anim`；需要原生可编辑 PPTX 时，把动画降级为静态结构或由 `ppt-master` 单独验证。
- 画布：按 16:9、4:3、1:1、3:4、9:16 选择对应布局规则，不把一种画布的尺寸假设带到另一种画布。

## 调用方式

- `用 $lvsea-ppt + oh-my-ppt 先核对来源，再做一页 16:9 可编辑 PPTX。`
- `用 $lvsea-ppt 采用 Oh My PPT 的布局预算，生成 HTML 预览后再导出 PPTX。`
- `用 $lvsea-ppt 按 oh-my-ppt 的 Chart.js 规则做一页数据图，并说明原生编辑边界。`
- `用 $lvsea-ppt 为 HTML 页面加 data-anim 动画，并检查导出后的降级结果。`

上述调用仍由 `lvsea-ppt` 选择实际执行器；需要原生 PPTX 时默认优先 `ppt-master`，不能把 Oh My PPT 的 HTML 工作台能力直接写成 PPTX 实跑证据。

## 依赖与限制

- 上游项目为 Apache-2.0；本适配只保留方法摘要、路由元数据和来源链接，未复制 Electron 源码、`node_modules`、构建产物、模板、字体、图片或模型。
- 上游应用运行需要其自己的 Node/pnpm/Electron 环境；本适配不自动安装、启动或执行第三方脚本。
- `oh-my-ppt` provider 是指导型协作者，不替代 `ppt-master`、HTML 运行时或图像型 PPTX provider。
- Provider 发现、实际调用、导出成功、视觉验收和人工质量评价分别记录；静态适配文件不能替代运行证据。
