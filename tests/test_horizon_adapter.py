import json
import tempfile
import unittest

from pathlib import Path
from huc.adapters.horizon import analyze_horizon_project


class HorizonAdapterTests(unittest.TestCase):

    def test_valid_project(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)

            manifest = {
                "id": "test_mod",
                "version": "1.0.0",
                "game": "26.3",
                "schema": 1
            }

            manifest_path = project / "horizon-native.json"

            manifest_path.write_text(
                json.dumps(manifest),
                encoding="utf-8"
            )

            result = analyze_horizon_project(str(project))

            self.assertTrue(result["success"])
            self.assertEqual(result["id"], "test_mod")
            self.assertEqual(result["game"], "26.3")

    def test_missing_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            result = analyze_horizon_project(temp)

            self.assertFalse(result["success"])

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as temp:
            manifest_path = Path(temp) / "horizon-native.json"
            manifest_path.write_text("{invalid json", encoding="utf-8")

            result = analyze_horizon_project(temp)

            self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
