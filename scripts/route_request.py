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
        ("qiaomu-bento-ppt", ["qiaomu-bento-ppt"]),
        ("gaiduo-ppt", ["gaiduo-ppt"]),
    ]
    for provider, terms in pairs:
        if _has(text, *terms):
            return provider
    return None


def choose_route(request: str, extra_roots: list[str] | None = None) -> dict[str, Any]:
    original = request.strip()
    text = re.sub(r"\s+", " ", original.lower())
    roots = _skill_roots(extra_roots)
    availability = {name: _find_provider(name, roots) for name in PROVIDERS}

    explicit = _explicit_provider(text)
    has_editable = _has(text, "可编辑", "编辑", "pptx", "powerpoint", "真文本", "native")
    has_image = _has(text, "图片", "截图", "海报", "image", "png", "jpg", "视觉稿")
    has_html = _has(text, "html", "网页", "浏览器", "react", "webgl", "网页ppt")
    has_svg = _has(text, "svg")
    has_template = _has(text, "模板", "套用", "保留排版", "只改文字", "原版式", "旧ppt")
    has_evidence = _has(text, "scr", "证据链", "战略", "经营分析", "生产运营", "安全生产", "制造", "数据密集", "咨询风")
    has_image_first = _has(text, "图片版", "图片型", "视觉冲击", "手绘", "image-first", "生图幻灯片", "图片ppt")
    has_bento = _has(text, "bento", "一页", "公众号", "文章链接", "网页文章")
    has_visual_asset = _has(text, "配图", "封面图", "章节图", "概念图", "背景图", "图片提示词", "安全区")
    has_motion = _has(text, "动画html", "动画网页", "录屏", "动态流程", "motion", "动画演示")
    has_presenter = _has(text, "演讲者视图", "讲稿备注", "杂志风", "swiss", "发布会", "演讲")
    wants_hybrid = _has(text, "先用 open-slide", "先用open-slide", "再用 baoyu", "再用baoyu", "html再", "html ->", "html到图片")

    if explicit == "GordenImage2PPTX" or (has_image and has_editable and _has(text, "转", "还原", "逆向", "图片ppt")):
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
    elif has_template or explicit in {"GordenPPTSkill"}:
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
        reason = "内容是一页高密度文章/URL/Bento 信息页。"
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
        reason = "没有更强的格式信号，按海洋哥偏好默认走原生可编辑 PPTX。"

    chosen = _first_available(candidates, availability)
    collab_status = [_find_provider(name, roots) for name in collaborators]
    return {
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


if __name__ == "__main__":
    main()
