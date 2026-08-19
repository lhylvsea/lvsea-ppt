# Prior-Art Research

研究日期：2026-08-19。研究方式：打开用户给出的公开页面、浅克隆公开仓库、只读审阅入口说明/README/许可证/关键脚本；没有运行未经审查的第三方安装器或生成命令。

## Inputs reviewed

已读取或核对：

- `dashi-ppt-skill` / `dashiai-ppt-skill`
- `ian-handdrawn-ppt`
- `frontend-slides`
- `PPT-Design-Prompt`
- `CyberPPT`
- `GordenPPTSkill`
- `open-slide`
- `ppt-image-first`
- `guizang-ppt-skill`
- `html-ppt-skill`
- `PPT-as-code`
- `AI_Animation`
- `qiaomu-ppt`
- `qiaomu-bento-ppt`
- `gaiduo-ppt`
- `baoyu-slide-deck` in `baoyu-skills`
- `ppt-master` CNB checkout
- 本机既有 `ppt-master`、`dashiai-ppt`、`cyber-ppt`、`gaiduo-ppt`、`bentohttp-ppt`、`GordenImage2PPTX`、`GordenSuperPPTSkill`、`slide-maker` 等入口

## Main findings

1. Native PPTX and HTML deck are different artifact lifecycles. A browser-editable HTML deck is excellent for iteration, but it should not be called fully editable PPTX without an actual exporter/readback.
2. Image-first workflows produce stronger visual coherence and page-level polish, but they naturally trade away object-level editability. A second image-to-editable pass is a separate route, not a free property.
3. Evidence-heavy decks need a content/evidence gate before visual styling. SCR and MBB-style planning are useful for production, safety, strategy and operating reviews.
4. The best general architecture is an orchestrator: `ppt-master`/`CyberPPT` for native and evidence paths, HTML providers for iterative visual work, image providers for raster editions, and one unified QA contract.
5. The user's preference for 16:9, 12 pt minimum, dense but clear layouts, real source images, editable artifacts and actual rendering checks is compatible with the router's defaults.

## Unavailable or redirected inputs

- `https://github.com/bbostaice/axi-front-design-skill` returned 404 on the review date. It is not registered as an available provider.
- `https://github.com/chuspeeism/dashiai-ppt-skill` redirects to `dashi-ppt-skill`; the matrix keeps one provider entry and one local adapter name.
- `https://cnb.cool/lvsea2008/ppt-master` was readable through a shallow Git checkout even though direct web fetch was not available; it is treated as the user's preferred local provider, not bundled into this package.

## Evidence classification

- `validated by source review`: route/feature is stated in the reviewed source.
- `available locally`: a local Skill entry was found during this run.
- `provider run`: requires a real task invocation; this package did not call every provider.
- `missing evidence`: no provider-backed visual run or human blind comparison was performed for the synthesis itself.
