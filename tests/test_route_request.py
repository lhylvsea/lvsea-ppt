import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from route_request import choose_route  # noqa: E402


class RouteRequestTests(unittest.TestCase):
    def test_native_default(self):
        self.assertEqual(choose_route("把这份月报做成可编辑PPTX")["route"], "native-create")

    def test_url_is_source_material_not_bento(self):
        result = choose_route("把这个网页链接内容做成PPT")
        self.assertEqual(result["route"], "native-create")
        self.assertNotEqual(result["route"], "bento-onepage")

    def test_onepage_url_requires_style_choice(self):
        result = choose_route("把这个网页链接内容制作成一页可编辑PPTX，保留原文图片")
        self.assertEqual(result["route"], "clarification-required")
        self.assertEqual(result["status"], "needs-user-choice")
        self.assertEqual(result["clarification"]["kind"], "onepage-style")
        self.assertEqual(result["recommended_style"]["id"], "design-reference-native")
        self.assertEqual(
            [choice["id"] for choice in result["style_options"]],
            ["design-reference-native", "editorial-photo", "timeline-policy", "bento-info"],
        )

    def test_explicit_bento_is_opt_in(self):
        result = choose_route("把这篇文章做成一页 Bento 信息图")
        self.assertEqual(result["route"], "bento-onepage")
        self.assertEqual(result["style"]["id"], "bento-info")

    def test_template_reference_is_not_template_fill(self):
        result = choose_route("把网页文章做成一页PPT，参考 PPT-Design 和公司模板")
        self.assertEqual(result["route"], "clarification-required")
        self.assertEqual(result["clarification"]["kind"], "onepage-style")

    def test_direct_default_uses_recommended_onepage_style(self):
        result = choose_route("把这篇网页文章做成一页PPT，你来定风格")
        self.assertEqual(result["route"], "native-create")
        self.assertEqual(result["style"]["id"], "design-reference-native")

    def test_explicit_onepage_style_is_actionable(self):
        result = choose_route("把这篇网页文章做成一页PPT，采用图文叙事版")
        self.assertEqual(result["route"], "native-create")
        self.assertEqual(result["style"]["id"], "editorial-photo")

    def test_template_fill(self):
        self.assertEqual(choose_route("套用公司PPT模板并保留排版")["route"], "native-template-fill")

    def test_image_to_editable(self):
        self.assertEqual(choose_route("把PPT截图转成可编辑PPTX")["route"], "image-to-editable")

    def test_hybrid(self):
        self.assertEqual(choose_route("先用 open-slide 做 HTML，再用 baoyu 做视觉终版")["route"], "hybrid-html-to-visual")

    def test_ambiguous_diagram_requires_choice(self):
        result = choose_route("帮我做一张流程图")
        self.assertEqual(result["route"], "clarification-required")
        self.assertEqual(result["status"], "needs-user-choice")
        self.assertEqual(result["clarification"]["recommended_choice"], "technical-native")
        self.assertGreaterEqual(len(result["clarification"]["questions"]), 1)

    def test_itinerary_requires_semantic_choice(self):
        result = choose_route("帮我做一个行程图")
        self.assertEqual(result["route"], "clarification-required")
        question_ids = [question["id"] for question in result["clarification"]["questions"]]
        self.assertIn("diagram_purpose", question_ids)
        self.assertIn("diagram_style", question_ids)

    def test_explicit_diagram_styles_bypass_gate(self):
        self.assertEqual(choose_route("做一个手绘式流程图")["route"], "image-first-visual")
        self.assertEqual(choose_route("做一个中文技术解释图")["route"], "native-create")
        self.assertEqual(choose_route("做一个文字配图式流程图")["route"], "image-first-visual")

    def test_direct_default_bypasses_gate(self):
        result = choose_route("做一个流程图，你来定")
        self.assertEqual(result["route"], "native-create")

    def test_menu_choice_is_actionable(self):
        self.assertEqual(choose_route("handdrawn")["route"], "image-first-visual")
        self.assertEqual(choose_route("editable-vector")["route"], "structured-import")
        self.assertEqual(choose_route("interactive-web")["route"], "html-first-iterate")

    def test_named_provider_is_respected_for_diagram(self):
        self.assertEqual(choose_route("用 open-slide 做一张流程图")["route"], "html-first-iterate")
        self.assertEqual(choose_route("用 ian-handdrawn-ppt 做一张流程图")["route"], "image-first-visual")

    def test_fixture_shape(self):
        cases = json.loads((ROOT / "evals" / "trigger_cases.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases["should_trigger"]), 8)
        self.assertGreaterEqual(len(cases["should_not_trigger"]), 3)
        self.assertGreaterEqual(len(cases["should_clarify"]), 3)


if __name__ == "__main__":
    unittest.main()
