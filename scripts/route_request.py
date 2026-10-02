#!/usr/bin/env python3
"""Deterministic, availability-aware router for lvsea-ppt."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any


PROVIDERS: dict[str, dict[str, Any]] = {
    "ppt-master": {"skills": ["ppt-master"], "role": "native editable PPTX, SVG-first, template fill"},
    "cyber-ppt": {"skills": ["cyber-ppt", "CyberPPT"], "role": "evidence/SCR/strict QA"},
    "dashiai-ppt": {"skills": ["dashiai-ppt", "dashi-ppt", "dashi-ppt-skill"], "role": "browser-editable HTML and export"},
    "open-slide": {"skills": ["open-slide"], "role": "React HTML slide runtime and inspector"},
    "PPT-as-code": {"skills": ["PPT-as-code", "ppt-as-code"], "role": "staged HTML deck and optional export"},
    "guizang-ppt-skill": {"skills": ["guizang-ppt-skill"], "role": "magazine/Swiss presenter HTML"},
    "html-ppt-skill": {"skills": ["html-ppt-skill"], "role": "theme/layout HTML studio"},
    "gaiduo-ppt": {"skills": ["gaiduo-ppt"], "role": "visual exploration to hybrid HTML"},
    "bentohttp-ppt": {"skills": ["bentohttp-ppt"], "role": "article to dense Bento HTML"},
    "qiaomu-bento-ppt": {"skills": ["qiaomu-bento-ppt"], "role": "offline editable Bento HTML"},
    "qiaomu-ppt": {"skills": ["qiaomu-ppt"], "role": "source-aware editable PPTX"},
    "baoyu-slide-deck": {"skills": ["baoyu-slide-deck"], "role": "prompted raster slide deck"},
    "ppt-image-first": {"skills": ["ppt-image-first"], "role": "preview-first image deck"},
    "ian-handdrawn-ppt": {"skills": ["ian-handdrawn-ppt"], "role": "handdrawn raster pages"},
    "GordenPPTSkill": {"skills": ["GordenPPTSkill", "gorden-ppt-skill"], "role": "native template text fill"},
    "GordenImage2PPTX": {"skills": ["GordenImage2PPTX"], "role": "image to editable PPTX"},
    "bggg-creator-image2ppt": {"skills": ["bggg-creator-image2ppt"], "role": "image/HTML/SVG to editable PPTX"},
    "ppt-design-prompt": {"skills": ["ppt-design-prompt"], "role": "presentation image prompt system"},
    "AI_Animation": {"skills": ["AI_Animation"], "role": "animated HTML and visual motion"},
    "frontend-slides": {"skills": ["frontend-slides"], "role": "frontend coded slides and motion"},
}


STYLE_REFERENCE_POLICY = (
    "生成前先读取本机 PPT-Design/DesignPPT.md，并按内容需要抽样逻辑图*.pptx 或公司PPT模板.pptx；"
    "参考模板只借鉴构图、色系、层级和组件，不等于直接套用原生模板。只有用户明确要求套用/填充/保留原版式时，"
    "才进入 native-template-fill。"
)


STYLE_PROFILES: dict[str, dict[str, Any]] = {
    "design-reference-native": {
        "label": "模板构图参考版（推荐）",
        "description": "按 DesignPPT.md 与参考模板提取构图和色系，重新组织主视觉、逻辑链、时间线或重点区块；交付原生可编辑 PPTX，不机械复制卡片矩阵。",
        "route": "native-create",
        "providers": ["ppt-master", "qiaomu-ppt", "cyber-ppt"],
        "recommendation": "适合正式汇报、政策文章、制造/安全/经营材料，能兼顾来源图片、事实结构和后续编辑。",
    },
    "editorial-photo": {
        "label": "图文叙事版",
        "description": "以原文真实照片或现场图作为主视觉，配合标题、引语和少量主题段落，形成新闻编辑式单页；图片服务事实表达，不用装饰图凑数。",
        "route": "native-create",
        "providers": ["ppt-master", "qiaomu-ppt", "ppt-image-first"],
        "recommendation": "适合人物、现场、新闻稿或需要保留原文图片的文章。",
    },
    "timeline-policy": {
        "label": "时间轴演进版",
        "description": "把年份、阶段、政策演进或行动路径作为页面主骨架，用时间轴/阶段带承载事实，辅以关键结论和证据图片。",
        "route": "native-create",
        "providers": ["ppt-master", "qiaomu-ppt", "cyber-ppt"],
        "recommendation": "适合带有明显年份、历程、阶段和演进关系的政策或专题文章。",
    },
    "bento-info": {
        "label": "Bento 信息卡片版",
        "description": "采用高密度信息卡片、指标块或卡片矩阵，优先交付离线可编辑 Bento HTML；它只在用户明确选择 Bento/信息卡片时启用。",
        "route": "bento-onepage",
        "providers": ["bentohttp-ppt", "qiaomu-bento-ppt", "dashiai-ppt"],
        "recommendation": "适合明确要信息卡片、Bento 或 HTML 单页，而不是一般的 URL 到 PPTX。",
    },
}


def _skill_roots(extra: list[str] | None = None) -> list[Path]:
    roots: list[Path] = []
    raw = os.environ.get("LVSEA_SKILLS_ROOTS", "")
    if raw:
        roots.extend(Path(item) for item in raw.split(os.pathsep) if item)
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    userprofile = Path(os.environ.get("USERPROFILE", Path.home()))
    roots.extend([codex_home / "skills", userprofile / ".codex" / "skills", userprofile / ".agents" / "skills"])
    if extra:
        roots.extend(Path(item) for item in extra)
    unique: list[Path] = []
    for root in roots:
        root = root.expanduser()
        if root not in unique:
            unique.append(root)
    return unique


def _find_provider(provider: str, roots: list[Path]) -> dict[str, Any]:
    meta = PROVIDERS[provider]
    hits: list[str] = []
    for root in roots:
        for name in meta["skills"]:
            candidate = root / name
            if (candidate / "SKILL.md").is_file():
                hits.append(str(candidate))
    return {"provider": provider, "available": bool(hits), "paths": hits, "role": meta["role"]}


def _first_available(candidates: list[str], availability: dict[str, dict[str, Any]]) -> str | None:
    for candidate in candidates:
        if availability.get(candidate, {}).get("available"):
            return candidate
    return candidates[0] if candidates else None


def _has(text: str, *terms: str) -> bool:
    return any(term in text for term in terms)


def _explicit_provider(text: str) -> str | None:
    pairs = [
        ("GordenImage2PPTX", ["gordenimage2pptx", "gordenimage2ppt"]),
        ("GordenPPTSkill", ["gordenpptskill"]),
        ("cyber-ppt", ["cyberppt", "cyber-ppt"]),
        ("ppt-master", ["ppt-master"]),
        ("open-slide", ["open-slide"]),
        ("PPT-as-code", ["ppt-as-code"]),
        ("baoyu-slide-deck", ["baoyu-slide-deck"]),
        ("ppt-image-first", ["ppt-image-first"]),
        ("guizang-ppt-skill", ["guizang-ppt-skill"]),
        ("qiaomu-ppt", ["qiaomu-ppt"]),
        ("bentohttp-ppt", ["bentohttp-ppt"]),
        ("qiaomu-bento-ppt", ["qiaomu-bento-ppt"]),
        ("gaiduo-ppt", ["gaiduo-ppt"]),
        ("ian-handdrawn-ppt", ["ian-handdrawn-ppt", "handdrawn"]),
    ]
    for provider, terms in pairs:
        if _has(text, *terms):
            return provider
    return None


def _explicit_slide_style(text: str) -> str | None:
    """Return a one-page visual style only when the user actually names one."""
    choices = [
        (
            "design-reference-native",
            [
                "design-reference-native",
                "模板构图参考",
                "参考模板构图",
                "参考模板版式",
                "红白逻辑",
                "结构化汇报",
                "逻辑汇报",
                "中文技术解释",
            ],
        ),
        (
            "editorial-photo",
            [
                "editorial-photo",
                "图文叙事",
                "图文叙事版",
                "新闻编辑版",
                "照片主视觉",
                "照片叙事",
                "图文编辑版",
            ],
        ),
        (
            "timeline-policy",
            [
                "timeline-policy",
                "政策时间轴",
                "时间轴演进",
                "时间线版",
                "演进路径",
                "历程版",
            ],
        ),
        (
            "bento-info",
            [
                "bento-info",
                "bento",
                "bento单页",
                "bento 信息图",
                "信息卡片",
                "卡片矩阵",
                "卡片化信息图",
                "仪表盘卡片",
                "html bento",
            ],
        ),
    ]
    for style, terms in choices:
        if _has(text, *terms):
            return style
    return None


def _style_options() -> list[dict[str, Any]]:
    return [
        {
            "id": style_id,
            "label": profile["label"],
            "description": profile["description"],
            "route": profile["route"],
            "providers": profile["providers"],
        }
        for style_id, profile in STYLE_PROFILES.items()
    ]


def _recommended_slide_style(text: str) -> str:
    if _has(text, "时间轴", "时间线", "历程", "演进", "沿革", "阶段", "年份"):
        return "timeline-policy"
    if _has(text, "新闻", "采访", "人物故事", "现场报道", "专题报道"):
        return "editorial-photo"
    return "design-reference-native"


def _onepage_style_clarification(
    text: str,
    *,
    is_onepage_visual: bool,
    selected_style: str | None,
    selected_diagram_choice: str | None,
    explicit_provider: str | None,
    template_apply: bool,
    bypass: bool,
) -> dict[str, Any] | None:
    """Pause ambiguous one-page visual requests before choosing a provider.

    A URL or article is an input shape, not a visual style. The gate keeps
    Bento opt-in and exposes a small, actionable style menu for one-page work.
    """
    if (
        not is_onepage_visual
        or selected_style
        or selected_diagram_choice
        or explicit_provider
        or template_apply
        or bypass
    ):
        return None

    recommended = _recommended_slide_style(text)
    profile = STYLE_PROFILES[recommended]
    return {
        "route": "clarification-required",
        "status": "needs-user-choice",
        "reason": "网页/文章/URL 只是来源材料，不能单独决定一页 PPT 的版式；Bento 仅在明确选择时启用。",
        "recommended_style": {"id": recommended, **profile},
        "style_options": _style_options(),
        "clarification": {
            "kind": "onepage-style",
            "questions": [
                {
                    "id": "slide_style",
                    "question": "这份来源材料的一页 PPT，希望采用哪种构图路线？",
                    "choices": _style_options(),
                }
            ],
            "recommended_choice": recommended,
            "recommended_reason": profile["recommendation"],
            "reference_policy": STYLE_REFERENCE_POLICY,
            "resume_prompt": "可直接回复：`模板构图参考版`、`图文叙事版`、`时间轴演进版` 或 `Bento 信息卡片版`；回复“你来定”则采用推荐路线。",
        },
    }


def _explicit_diagram_choice(text: str) -> str | None:
    choices = [
        ("technical-native", ["technical-native", "中文技术解释图", "技术解释图"]),
        ("handdrawn", ["handdrawn", "手绘式", "手绘流程图"]),
        ("illustrated", ["illustrated", "文字配图", "插画式", "插图式"]),
        ("editable-vector", ["editable-vector", "原生可编辑矢量图", "可编辑矢量"]),
        ("interactive-web", ["interactive-web", "html动画交互图", "html交互图"]),
        ("bento", ["bento", "一页bento", "一页 bento"]),
        ("evidence-consulting", ["evidence-consulting", "咨询/证据链图", "证据链图"]),
    ]
    for choice, terms in choices:
        if _has(text, *terms):
            return choice
    return None


DIAGRAM_TERMS = (
    "流程图",
    "行程图",
    "路线图",
    "架构图",
    "关系图",
    "组织图",
    "示意图",
    "逻辑图",
    "信息图",
    "技术图",
    "工艺图",
    "系统图",
    "拓扑图",
    "结构图",
    "路径图",
    "旅程图",
    "图解",
    "图示",
)


def _diagram_clarification(
    text: str,
    *,
    has_diagram: bool,
    has_style_signal: bool,
    has_purpose_signal: bool,
    bypass: bool,
) -> dict[str, Any] | None:
    """Return a user-choice gate for broad diagram requests.

    The router must not silently choose between native technical diagrams,
    raster illustration, hand-drawn pages, and interactive HTML when the user
    only says "make a diagram". Explicit style/format signals or a direct
    "you decide" instruction can bypass the gate.
    """
    semantic_ambiguous = _has(text, "行程图", "路线图", "旅程图") and not has_purpose_signal
    if not has_diagram or bypass or (has_style_signal and not semantic_ambiguous):
        return None

    questions: list[dict[str, Any]] = []
    if semantic_ambiguous:
        questions.append(
            {
                "id": "diagram_purpose",
                "question": "你说的“行程图/路线图”具体是哪一类？",
                "choices": [
                    {"id": "travel-itinerary", "label": "旅行/日程路线", "description": "景点、时间、交通、酒店或任务安排。"},
                    {"id": "process-flow", "label": "工艺/业务流程", "description": "步骤、责任、输入输出、制度或操作路径。"},
                    {"id": "system-architecture", "label": "系统/技术架构", "description": "模块、设备、数据、接口或系统关系。"},
                    {"id": "strategy-roadmap", "label": "战略/项目路线", "description": "阶段、目标、里程碑、策略或行动计划。"},
                    {"id": "other", "label": "其他", "description": "请补充一句图的用途和阅读对象。"},
                ],
            }
        )

    if not has_style_signal:
        questions.append(
            {
                "id": "diagram_style",
                "question": "希望采用哪种表现路线？",
                "choices": [
                    {
                        "id": "technical-native",
                        "label": "中文技术解释图",
                        "description": "原生文字、形状、箭头和分层关系，适合工艺、设备、系统和培训说明；优先可编辑 PPTX。",
                        "route": "native-create",
                        "providers": ["ppt-master", "cyber-ppt", "qiaomu-ppt"],
                    },
                    {
                        "id": "handdrawn",
                        "label": "手绘式",
                        "description": "手绘线稿、知识卡或草图感；优先视觉成品，必要时再做可编辑重建。",
                        "route": "image-first-visual",
                        "providers": ["ian-handdrawn-ppt", "ppt-image-first"],
                    },
                    {
                        "id": "illustrated",
                        "label": "文字配图/插画式",
                        "description": "文字与场景图、插画或概念图结合；视觉冲击优先，复杂画面通常是图片层。",
                        "route": "image-first-visual",
                        "providers": ["baoyu-slide-deck", "ppt-image-first"],
                    },
                    {
                        "id": "editable-vector",
                        "label": "原生可编辑矢量图",
                        "description": "文本、矩形、路径、箭头和分组尽量成为 PPT 原生对象或局部 SVG。",
                        "route": "structured-import",
                        "providers": ["ppt-master", "bggg-creator-image2ppt", "qiaomu-ppt"],
                    },
                    {
                        "id": "interactive-web",
                        "label": "HTML/动画交互图",
                        "description": "浏览器预览、动画、演讲者视图、缩放或录屏优先。",
                        "route": "html-first-iterate",
                        "providers": ["open-slide", "PPT-as-code", "guizang-ppt-skill"],
                    },
                    {
                        "id": "bento",
                        "label": "一页 Bento 信息图",
                        "description": "高密度、一页式、适合文章、URL、公众号或管理摘要。",
                        "route": "bento-onepage",
                        "providers": ["bentohttp-ppt", "qiaomu-bento-ppt"],
                    },
                    {
                        "id": "evidence-consulting",
                        "label": "咨询/证据链图",
                        "description": "SCR、战略、经营、安全或制造分析，先建立证据台账和逻辑关系。",
                        "route": "evidence-consulting",
                        "providers": ["cyber-ppt", "ppt-master"],
                    },
                ],
            }
        )
    return {
        "route": "clarification-required",
        "status": "needs-user-choice",
        "reason": "“图/流程图/行程图/路线图”覆盖多种输出契约；在用途、表现方式或编辑边界未明确前，不直接替用户选择。",
        "clarification": {
            "questions": questions,
            "recommended_choice": "technical-native",
            "recommended_reason": "在制造、工艺、设备、安全和管理场景中，它最容易保留事实、中文说明和后续编辑能力。",
            "resume_prompt": "可直接回复：`中文技术解释图 + 可编辑PPTX`，或 `手绘式 + 图片型PPT`。若你说“你来定/直接做”，将采用推荐路线。",
        },
    }


def choose_route(request: str, extra_roots: list[str] | None = None) -> dict[str, Any]:
    original = request.strip()
    text = re.sub(r"\s+", " ", original.lower())
    roots = _skill_roots(extra_roots)
    availability = {name: _find_provider(name, roots) for name in PROVIDERS}

    explicit = _explicit_provider(text)
    selected_choice = _explicit_diagram_choice(text)
    selected_style = _explicit_slide_style(text)
    if selected_style is None and selected_choice == "bento":
        selected_style = "bento-info"
    has_editable = _has(text, "可编辑", "编辑", "pptx", "powerpoint", "真文本", "native")
    has_image = _has(text, "图片", "截图", "海报", "image", "png", "jpg", "视觉稿")
    has_html = _has(text, "html", "浏览器", "react", "webgl", "网页ppt", "网页演示", "网页幻灯片")
    has_svg = _has(text, "svg")
    template_apply = _has(
        text,
        "模板填充",
        "模板套用",
        "套用模板",
        "套公司模板",
        "填入模板",
        "填充模板",
        "保留排版",
        "保留原版式",
        "只改文字",
        "替换模板内容",
        "沿用模板",
        "按模板制作",
        "现有pptx",
        "旧ppt",
    )
    template_reference = _has(
        text,
        "参考模板",
        "参考ppt-design",
        "参考 ppt-design",
        "designppt",
        "ppt-design",
        "借鉴模板",
        "模板构图",
        "参考版式",
        "模板风格",
    )
    has_evidence = _has(text, "scr", "证据链", "战略", "经营分析", "生产运营", "安全生产", "制造", "数据密集", "咨询风")
    has_image_first = _has(text, "图片版", "图片型", "视觉冲击", "手绘", "image-first", "生图幻灯片", "图片ppt")
    has_bento = _has(
        text,
        "bento",
        "信息卡片",
        "卡片矩阵",
        "卡片化信息图",
        "仪表盘卡片",
        "html bento",
        "bentohttp-ppt",
        "qiaomu-bento-ppt",
    )
    has_visual_asset = _has(text, "配图", "封面图", "章节图", "概念图", "背景图", "图片提示词", "安全区")
    has_motion = _has(text, "动画html", "动画网页", "录屏", "动态流程", "motion", "动画演示")
    has_presenter = _has(text, "演讲者视图", "讲稿备注", "杂志风", "swiss", "发布会", "演讲")
    wants_hybrid = _has(text, "先用 open-slide", "先用open-slide", "再用 baoyu", "再用baoyu", "html再", "html ->", "html到图片")
    has_diagram = _has(text, *DIAGRAM_TERMS)
    has_url_or_article = bool(re.search(r"https?://\S+", text)) or _has(
        text,
        "url",
        "网址",
        "网页链接",
        "文章链接",
        "网页内容",
        "网页文章",
        "在线文章",
        "公众号",
        "原文",
        "文章",
        "报告",
    )
    has_onepage = _has(text, "一页", "单页", "一页式", "单页式", "one-page", "onepage", "单页可视化", "一页可视化")
    has_presentation_output = _has(text, "ppt", "pptx", "powerpoint", "演示文稿", "幻灯片", "汇报页", "演示页", "presentation")
    is_onepage_visual = has_onepage and (
        has_presentation_output or has_url_or_article or _has(text, "可视化", "信息图", "信息页")
    )
    has_style_signal = _has(
        text,
        "手绘",
        "handdrawn",
        "草图",
        "技术解释",
        "中文技术",
        "工艺",
        "设备",
        "系统架构",
        "架构",
        "文字配图",
        "图文",
        "插画",
        "插图",
        "配图式",
        "图片型",
        "图片版",
        "视觉冲击",
        "image-first",
        "可编辑",
        "pptx",
        "powerpoint",
        "svg",
        "html",
        "react",
        "浏览器",
        "动画",
        "交互",
        "bento",
        "一页",
        "scr",
        "证据链",
        "咨询风",
        "战略",
    )
    has_purpose_signal = _has(
        text,
        "旅行",
        "旅游",
        "景点",
        "酒店",
        "日程",
        "交通",
        "工艺",
        "设备",
        "系统",
        "业务",
        "生产",
        "安全",
        "技术",
        "战略",
        "项目",
        "经营",
        "制造",
        "培训",
    )
    bypass_diagram_gate = _has(text, "你来定", "直接做", "直接生成", "不用确认", "无需确认", "按默认")

    clarification = _diagram_clarification(
        text,
        has_diagram=has_diagram,
        has_style_signal=has_style_signal or explicit is not None or selected_choice is not None,
        has_purpose_signal=has_purpose_signal,
        bypass=bypass_diagram_gate,
    )
    if clarification:
        return {
            "request": original,
            "route": clarification["route"],
            "reason": clarification["reason"],
            "primary_candidates": [],
            "primary_provider": None,
            "collaborator_candidates": [],
            "collaborators": [],
            "provider_status": {},
            "clarification": clarification["clarification"],
            "assumptions": {
                "language": "zh-CN",
                "canvas": "16:9",
                "editable_default": True,
                "minimum_body_size": "12pt for PPTX, 16px for HTML",
                "diagram_gate": "paused-before-provider-selection",
            },
            "status": clarification["status"],
        }

    style_clarification = _onepage_style_clarification(
        text,
        is_onepage_visual=is_onepage_visual,
        selected_style=selected_style,
        selected_diagram_choice=selected_choice,
        explicit_provider=explicit,
        template_apply=template_apply,
        bypass=bypass_diagram_gate,
    )
    if style_clarification:
        return {
            "request": original,
            "route": style_clarification["route"],
            "reason": style_clarification["reason"],
            "primary_candidates": [],
            "primary_provider": None,
            "collaborator_candidates": [],
            "collaborators": [],
            "provider_status": {},
            "clarification": style_clarification["clarification"],
            "recommended_style": style_clarification["recommended_style"],
            "style_options": style_clarification["style_options"],
            "assumptions": {
                "language": "zh-CN",
                "canvas": "16:9",
                "editable_default": True,
                "minimum_body_size": "12pt for PPTX, 16px for HTML",
                "source_url_is_not_visual_style": True,
                "bento_requires_explicit_choice": True,
                "design_reference_policy": STYLE_REFERENCE_POLICY,
            },
            "status": style_clarification["status"],
        }

    if selected_style in STYLE_PROFILES:
        style_profile = STYLE_PROFILES[selected_style]
        route = style_profile["route"]
        candidates = style_profile["providers"]
        collaborators = []
        reason = f"用户已选择“{style_profile['label']}”，按该构图契约执行；URL/文章仅作为来源材料。"
    elif selected_choice == "technical-native":
        route = "native-create"
        candidates = ["ppt-master", "cyber-ppt", "qiaomu-ppt"]
        collaborators = []
        reason = "用户已选择中文技术解释图，优先使用原生文字、形状、箭头和分层关系。"
    elif selected_choice == "handdrawn":
        route = "image-first-visual"
        candidates = ["ian-handdrawn-ppt", "ppt-image-first", "baoyu-slide-deck"]
        collaborators = ["GordenImage2PPTX", "bggg-creator-image2ppt"] if has_editable else []
        reason = "用户已选择手绘式表达，先保证手绘视觉叙事，再按需重建可编辑对象。"
    elif selected_choice == "illustrated":
        route = "image-first-visual"
        candidates = ["baoyu-slide-deck", "ppt-image-first", "ian-handdrawn-ppt"]
        collaborators = ["GordenImage2PPTX", "bggg-creator-image2ppt"] if has_editable else []
        reason = "用户已选择文字配图/插画式表达，视觉构图优先，复杂画面保留为图片组件。"
    elif selected_choice == "editable-vector":
        route = "structured-import"
        candidates = ["ppt-master", "bggg-creator-image2ppt", "qiaomu-ppt"]
        collaborators = []
        reason = "用户已选择原生可编辑矢量图，优先将文字、路径、箭头和分组映射为可编辑对象。"
    elif selected_choice == "interactive-web":
        route = "html-first-iterate"
        candidates = ["open-slide", "PPT-as-code", "guizang-ppt-skill", "dashiai-ppt"]
        collaborators = []
        reason = "用户已选择 HTML/动画交互图，优先交付浏览器可运行源和交互预览。"
    elif selected_choice == "bento":
        route = "bento-onepage"
        candidates = ["bentohttp-ppt", "qiaomu-bento-ppt", "dashiai-ppt"]
        collaborators = []
        reason = "用户已选择一页 Bento 信息图，优先高密度布局和离线可编辑 HTML。"
    elif selected_choice == "evidence-consulting":
        route = "evidence-consulting"
        candidates = ["cyber-ppt", "ppt-master", "qiaomu-ppt"]
        collaborators = []
        reason = "用户已选择咨询/证据链图，先建立事实台账、故事线和严格质量门。"
    elif explicit in {"open-slide", "PPT-as-code", "dashiai-ppt", "html-ppt-skill", "gaiduo-ppt"} and not wants_hybrid:
        route = "html-first-iterate"
        candidates = [explicit, "open-slide", "PPT-as-code", "dashiai-ppt"]
        collaborators = []
        reason = f"用户明确指定 `{explicit}`，按其 HTML/浏览器迭代能力执行。"
    elif explicit == "guizang-ppt-skill":
        route = "html-presenter"
        candidates = ["guizang-ppt-skill", "PPT-as-code", "open-slide"]
        collaborators = []
        reason = "用户明确指定 Guizang 网页演示路线，优先保留演讲者视图和演示交互。"
    elif explicit in {"baoyu-slide-deck", "ppt-image-first", "ian-handdrawn-ppt"}:
        route = "image-first-visual"
        candidates = [explicit, "baoyu-slide-deck", "ppt-image-first", "ian-handdrawn-ppt"]
        collaborators = ["GordenImage2PPTX", "bggg-creator-image2ppt"] if has_editable else []
        reason = f"用户明确指定 `{explicit}`，按图片优先路线执行，并单独记录可编辑性边界。"
    elif explicit == "qiaomu-bento-ppt":
        route = "bento-onepage"
        candidates = ["qiaomu-bento-ppt", "bentohttp-ppt", "dashiai-ppt"]
        collaborators = []
        reason = "用户明确指定 Qiaomu Bento 路线，优先输出离线高密度 HTML 信息图。"
    elif explicit == "qiaomu-ppt":
        route = "native-create"
        candidates = ["qiaomu-ppt", "ppt-master", "cyber-ppt"]
        collaborators = []
        reason = "用户明确指定 Qiaomu PPT 路线，优先保留来源台账和可编辑结构。"
    elif explicit == "GordenImage2PPTX" or (has_image and has_editable and _has(text, "转", "还原", "逆向", "图片ppt")):
        route = "image-to-editable"
        candidates = ["GordenImage2PPTX", "bggg-creator-image2ppt", "ppt-master"]
        collaborators = ["ppt-master"]
        reason = "输入是图片/截图/图片PPT且要求继续编辑，先拆分文字与视觉组件。"
    elif (has_html or has_svg) and has_editable and _has(text, "转", "导出", "生成", "转换"):
        route = "structured-import"
        candidates = ["ppt-master", "bggg-creator-image2ppt"]
        collaborators = ["cyber-ppt"] if has_evidence else []
        reason = "HTML/SVG 与可编辑 PPTX 同时出现，优先走结构解析和局部降级，不把整页截图冒充编辑对象。"
    elif wants_hybrid:
        route = "hybrid-html-to-visual"
        candidates = ["open-slide", "PPT-as-code", "dashiai-ppt", "gaiduo-ppt"]
        collaborators = ["baoyu-slide-deck", "ppt-image-first", "ian-handdrawn-ppt"]
        reason = "请求明确要求浏览器 HTML 迭代后再生成视觉图片终版。"
    elif template_apply or explicit in {"GordenPPTSkill"}:
        route = "native-template-fill"
        candidates = ["ppt-master", "GordenPPTSkill"]
        collaborators = ["cyber-ppt"] if has_evidence else []
        reason = "已有模板/旧 PPTX/保排版要求，优先直接填充原生 PPTX。"
    elif has_motion:
        route = "motion-html"
        candidates = ["AI_Animation", "frontend-slides", "PPT-as-code"]
        collaborators = ["ppt-master"] if has_editable else []
        reason = "目标是动画网页或录屏配套，先走网页动效，不把它误判为静态 PPTX。"
    elif has_bento:
        route = "bento-onepage"
        candidates = ["bentohttp-ppt", "qiaomu-bento-ppt", "dashiai-ppt"]
        collaborators = []
        reason = "用户明确指定 Bento/信息卡片路线，优先高密度布局和离线可编辑 HTML；普通 URL 不触发此分支。"
    elif has_diagram and _has(text, "文字配图", "图文", "配图式", "插画式", "插图式"):
        route = "image-first-visual"
        candidates = ["baoyu-slide-deck", "ppt-image-first", "ian-handdrawn-ppt"]
        collaborators = ["GordenImage2PPTX", "bggg-creator-image2ppt"] if has_editable else []
        reason = "已明确采用文字配图/插画式表达，视觉构图优先，复杂画面保留为图片组件。"
    elif has_visual_asset and not _has(text, "做一份ppt", "做ppt", "制作ppt", "生成pptx"):
        route = "visual-asset"
        candidates = ["ppt-design-prompt"]
        collaborators = []
        reason = "请求只需要服务 PPT 页面的视觉资产或提示词，不需要完整 deck。"
    elif has_image_first:
        route = "image-first-visual"
        candidates = ["baoyu-slide-deck", "ppt-image-first", "ian-handdrawn-ppt"]
        collaborators = ["GordenImage2PPTX", "bggg-creator-image2ppt"] if has_editable else []
        reason = "请求强调视觉成品或手绘/图片型页面，图片生成优先，编辑性作为后续路线。"
    elif has_presenter:
        route = "html-presenter"
        candidates = ["guizang-ppt-skill", "PPT-as-code", "open-slide", "dashiai-ppt"]
        collaborators = []
        reason = "请求强调演讲、讲稿、演讲者视图或杂志/Swiss 网页表现。"
    elif has_evidence:
        route = "evidence-consulting"
        candidates = ["cyber-ppt", "ppt-master", "qiaomu-ppt"]
        collaborators = []
        reason = "制造/安全/经营/战略/数据密集内容需要证据链和严格质量门。"
    elif has_html:
        route = "html-first-iterate"
        candidates = ["open-slide", "PPT-as-code", "dashiai-ppt", "gaiduo-ppt", "html-ppt-skill"]
        collaborators = []
        reason = "请求以 HTML/React/浏览器迭代为中心，先交付可运行网页源。"
    else:
        route = "native-create"
        candidates = ["ppt-master", "cyber-ppt", "qiaomu-ppt"]
        collaborators = []
        reason = "没有更强的格式信号，按海洋哥偏好默认走原生可编辑 PPTX；URL/文章只作为来源材料。"

    chosen = _first_available(candidates, availability)
    collab_status = [_find_provider(name, roots) for name in collaborators]
    result = {
        "request": original,
        "route": route,
        "reason": reason,
        "primary_candidates": candidates,
        "primary_provider": chosen,
        "collaborator_candidates": collaborators,
        "collaborators": collab_status,
        "provider_status": {name: availability[name] for name in sorted(set(candidates + collaborators))},
        "assumptions": {
            "language": "zh-CN",
            "canvas": "16:9",
            "editable_default": True,
            "minimum_body_size": "12pt for PPTX, 16px for HTML"
        },
        "status": "available" if chosen and availability.get(chosen, {}).get("available") else "fallback-or-unavailable",
    }
    if selected_style in STYLE_PROFILES:
        result["style"] = {"id": selected_style, **STYLE_PROFILES[selected_style]}
    elif is_onepage_visual and (bypass_diagram_gate or explicit):
        recommended = _recommended_slide_style(text)
        result["style"] = {"id": recommended, **STYLE_PROFILES[recommended]}
        result["design_reference_policy"] = STYLE_REFERENCE_POLICY
    elif template_reference:
        result["design_reference_policy"] = STYLE_REFERENCE_POLICY
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Route a presentation request for lvsea-ppt.")
    parser.add_argument("--text", required=True, help="Natural-language presentation request")
    parser.add_argument("--skills-root", action="append", default=[], help="Additional skill root; repeatable")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()
    result = choose_route(args.text, args.skills_root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"route={result['route']}")
        print(f"primary={result['primary_provider']}")
        print(f"status={result['status']}")
        print(f"reason={result['reason']}")
        if result.get("status") == "needs-user-choice":
            clarification = result.get("clarification", {})
            for question in clarification.get("questions", []):
                print(f"{question['id']}: {question['question']}")
                for choice in question.get("choices", []):
                    route = f" -> {choice['route']}" if choice.get("route") else ""
                    print(f"  {choice['id']}: {choice['label']}{route} | {choice['description']}")
            print(f"recommended={clarification.get('recommended_choice')}")
            print(f"resume={clarification.get('resume_prompt')}")


if __name__ == "__main__":
    main()
