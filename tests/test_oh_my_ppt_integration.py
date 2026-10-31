import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "references" / "oh-my-ppt"


class OhMyPptIntegrationTests(unittest.TestCase):
    def test_metadata_and_adapters_are_complete(self):
        metadata = json.loads((REFERENCE / "integration.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["provider"], "oh-my-ppt")
        self.assertEqual(metadata["upstream"]["reviewed_commit"], "b937ae5")
        self.assertEqual(metadata["upstream"]["license"], "Apache-2.0")
        self.assertEqual(metadata["execution_provider"], "ppt-master")
        adapters = {
            entry["upstream_skill"]: entry["adapter"]
            for entry in metadata["adopted_modules"]
        }
        for module in ("oh-my-ppt-source-reading", "oh-my-ppt-layout", "oh-my-ppt-chart", "oh-my-ppt-data-anim", "format-layout-skills"):
            adapter = adapters[module]
            self.assertTrue((ROOT / adapter).is_file(), adapter)

    def test_integration_does_not_create_a_nested_skill(self):
        self.assertEqual(list(REFERENCE.rglob("SKILL.md")), [])


if __name__ == "__main__":
    unittest.main()
