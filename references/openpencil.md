# OpenPencil 适配边界

## 目的

`openpencil-design` 是 `lvsea-ppt` 的可选矢量构图 provider，适合高密度 16:9 单页、逻辑图和需要保留 PenNode 设计源的页面。它不是默认替换所有 PPTX 生成器的通用 exporter。

## Keep / Adapt / Reject / Invent

| 分类 | 处理 |
| --- | --- |
| Keep | PenNode/矢量节点构图、`design` 与 `design:refine` 迭代、`.op` 源文件、PNG/SVG 预览。 |
| Adapt | 由 `lvsea-ppt` 先锁定来源事实、16:9 画布和编辑边界；PPTX 仅在实际 exporter 可用时直出，否则交给 `ppt-master` 或其他已声明的原生 fallback。 |
| Reject | 不复制 OpenPencil Electron、`node_modules`、模板、字体、图片或私有资产；不把 PNG、截图或 `.op` 预览直接称为原生可编辑 PPTX。 |
| Invent | 增加 provider 发现、显式触发词、PPTX fallback、统一 QA 记录和本地能力缺口报告。 |

## 调用契约

推荐使用：

```text
用 $lvsea-ppt 调用 OpenPencil，把材料做成高密度 16:9 单页，保留 .op 源文件并输出可编辑 PPTX。
```

执行时应按当前 OpenPencil Skill 的实际说明准备 `op` CLI/无头会话，至少完成：

1. `op --version` 与运行状态探测。
2. 创建或打开 `.op` 源文件。
3. 执行设计和必要的 `design:refine` 迭代。
4. 导出 PNG/SVG 预览并检查画布、文字、图片比例和越界。
5. 单独探测 PPTX exporter；只有返回成功且能被 PowerPoint/WPS 或结构读取器打开时，才报告 OpenPencil 直接导出 PPTX。

## 当前能力边界

本机验证过 `op 0.8.4` 的设计、细化和 PNG 预览路径；当前无头服务对 `export-deck` 和 `templates` 返回过 `unknown tool`。因此路由器把 OpenPencil 视为 authoring-first provider，默认保留 `ppt-master` 作为 PPTX 协作/降级出口。每次任务仍需重新探测，不用这份快照替代实际运行证据。

## 来源与许可证

- [OpenPencil](https://github.com/ZSeven-W/openpencil)：上游编辑器项目。
- [openpencil-skill](https://github.com/ZSeven-W/openpencil-skill)：面向 Agent 的 Skill 与 `op` 调用说明。

只采用公开项目的方法和调用边界；上游许可证、运行依赖、第三方图片/字体和平台限制继续由实际执行器负责。
