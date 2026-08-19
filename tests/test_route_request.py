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

    def test_template_fill(self):
        self.assertEqual(choose_route("套用公司PPT模板并保留排版")["route"], "native-template-fill")

    def test_image_to_editable(self):
        self.assertEqual(choose_route("把PPT截图转成可编辑PPTX")["route"], "image-to-editable")

    def test_hybrid(self):
        self.assertEqual(choose_route("先用 open-slide 做 HTML，再用 baoyu 做视觉终版")["route"], "hybrid-html-to-visual")

    def test_fixture_shape(self):
        cases = json.loads((ROOT / "evals" / "trigger_cases.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases["should_trigger"]), 8)
        self.assertGreaterEqual(len(cases["should_not_trigger"]), 3)


if __name__ == "__main__":
    unittest.main()
