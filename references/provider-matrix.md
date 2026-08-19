# Provider Matrix

研究日期：2026-08-19。下列版本是本次只读源码审阅的短 commit 快照，不代表未来版本不变。这里记录“吸收的方法”和“路由边界”，不复制上游代码、模板、图片或专有资产。

| Provider | 研究快照 | 吸收优势 | 适合路由 | 边界/注意事项 |
| --- | --- | --- | --- | --- |
| [ppt-master](https://cnb.cool/lvsea2008/ppt-master) | `4cdea1e` | SVG-first 原生 PPTX、模板/品牌/布局工作区、Fill Native、Enhance Native、逐页渲染与回读 | `native-create`, `native-template-fill`, `structured-import` | 本机实际 Skill 优先；不能把仓库存在写成每次 provider 已调用 |
| [CyberPPT](https://github.com/crazyykhllc-bit/CyberPPT) | `980e557` | MBB 证据表、SCR 故事线、视觉蓝图、可编辑信息层、strict QA | `evidence-consulting` | 高成本重型路线；材料不足时不能补造事实；MIT |
| [dashi-ppt-skill](https://github.com/chuspeeism/dashi-ppt-skill) | `7cb2334` | 多主题、浏览器编辑控制台、离线 HTML、可编辑 PPTX/PDF 导出 | `html-first-iterate` | AGPL-3.0；README 标明导出子包含专有组件；不复制或单独分发 |
| [dashiai-ppt-skill](https://github.com/chuspeeism/dashiai-ppt-skill) | redirect | 本机已发现的 Dashi 路线，模板化 HTML 与 PPTX/PDF 导出 | `html-first-iterate` | 本机版本与上游版本需现场核对 |
| [open-slide](https://github.com/1weiho/open-slide) | `7384649` | React 固定 1920x1080 画布、热更新、浏览器 Inspector 评论、presenter mode、静态 HTML/PDF | `html-first-iterate` | README 重点是 HTML/PDF；PPTX 不作为已确认能力，除非现场实跑；MIT |
| [PPT-as-code](https://github.com/Russell-cell/PPT-as-code) | `3f0cfce` | ingest/normalize/scenes、quick/basic/advanced、唯一源模型、可选 PPTX 导出、静态优先与降级 | `html-first-iterate`, `hybrid-html-to-visual` | exporter 仍需现场验证；MIT |
| [frontend-slides](https://github.com/zarazhangrui/frontend-slides) | `9906a34` | coding-agent HTML 设计、模板包、动画模式和参考驱动视觉探索 | `html-first-iterate`, `motion-html` | 不把网页视觉能力冒充 native PPTX；MIT |
| [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | `c91369c` | 电子杂志/Swiss 两套风格、WebGL、讲稿、演讲者视图、观众屏与低功耗降级 | `html-presenter` | 静态 HTML 优先；AGPL-3.0 |
| [html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) | `f3a8435` | 多主题、多布局、动画和 HTML presentation studio | `html-first-iterate` | 具体 exporter/运行时需现场验证；MIT |
| [qiaomu-ppt](https://github.com/joeseesun/qiaomu-ppt) | `b9b3c17` | 多源资料摄取、source cards、content contract、视觉资产清单、SVG-first、PPTX 回读和多格式 bundle | `native-create`, `structured-import` | AGPL-3.0；吸收方法，不镜像源码 |
| [qiaomu-bento-ppt](https://github.com/joeseesun/qiaomu-bento-ppt) | `55c63c8` | 自包含、可编辑、离线 Bento HTML 和语义布局 | `bento-onepage` | 不把一页 HTML 宣称为 native PPTX；MIT |
| [gaiduo-ppt](https://github.com/gaiduo/gaiduo-ppt) | `1df3703` | 内容 -> 视觉方向 -> 高清视觉稿 -> HTML 混合还原，逐阶段闸门 | `html-first-iterate`, `hybrid-html-to-visual` | 本次仓库未发现 LICENSE 文件，使用前需另行确认权利 |
| [baoyu-slide-deck](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-slide-deck) | `6b7a2e4` | outline -> prompt 文件 -> 批量生图 -> PNG/PDF/PPTX 合并、备份与可复现提示词 | `image-first-visual` | 图片型 PPTX 默认不是原生可编辑；MIT 仓库许可证仍不覆盖第三方模型/素材权利 |
| [ppt-image-first](https://github.com/NyxTides/ppt-image-first) | `87a300a` | 需求/风格/生成前确认、首页/目录/正文预览、image-first 和 review surface | `image-first-visual` | 目标是视觉稿与图片页面；Apache-2.0 |
| [ian-handdrawn-ppt](https://github.com/helloianneo/ian-handdrawn-ppt) | `b2cc5f3` | 中文手绘技术叙事、语义页面原型、风格 token 和逐页 PNG | `image-first-visual` | 明确是 raster page images，不是可编辑 PPTX；MIT |
| [GordenPPTSkill](https://github.com/GordenSun/GordenPPTSkill) | `7d4a61c` | 原生 PPTX 模板库、detail.json 容量、只换字、出框检测、模板回读 | `native-template-fill` | Skill 文档明确“个人学习和研究，严禁商业用途”；不复制模板资产 |
| [PPT-Design-Prompt](https://github.com/Russell-cell/PPT-Design-Prompt) | `a195f14` | PPT 配图的 thesis、安全区、16:9、4K、最小文字和品牌色规范 | `visual-asset` | 只做 slide image system，不是完整 deck/PPTX exporter；MIT |
| [AI_Animation](https://github.com/Unclecheng-li/AI_Animation) | `71f5427` | 动态 HTML、3D/动画/演示视觉灵感 | `motion-html` | 不是可编辑 PPTX 生产器；不要把动画网页截图替代 PPTX |
| [dashi-ppt-skill](https://github.com/chuspeeism/dashi-ppt-skill) | `7cb2334` | 用户给出的 `dashiai-ppt-skill` 已重定向到此仓库 | `html-first-iterate` | 避免重复 provider |
| `axi-front-design-skill` | 2026-08-19 | 无可核验优势 | 不进入路由 | 用户 URL 当前返回 404，保持“不可用”记录 |

## Local adapters

本机曾发现的可用入口包括 `ppt-master`、`dashiai-ppt`、`cyber-ppt`、`gaiduo-ppt`、`bentohttp-ppt`、`slide-maker`、`GordenPPTSkill`、`GordenImage2PPTX`、`GordenSuperPPTSkill`、`ian-handdrawn-ppt`、`PPT-as-code`、`ppt-design-prompt`、`guizang-ppt-skill` 和 `bggg-creator-image2ppt`。运行时必须重新探测，不能只凭这份快照宣称已安装。
