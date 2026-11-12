import json
import tempfile
import unittest
import zipfile

from pathlib import Path
from huc.adapters.bedrock import analyze_bedrock_pack


class BedrockAdapterTests(unittest.TestCase):

    def test_valid_bedrock_pack(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bedrock.mcpack"

            manifest = {
                "header": {
                    "name": "HUC Test",
                    "description": "Test Pack",
                    "uuid": "12345678-test",
                    "version": [1, 0, 0]
                },
                "modules": [
                    {"type": "resources"}
                ]
            }

            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(
                    "manifest.json",
                    json.dumps(manifest)
                )

            result = analyze_bedrock_pack(str(path))

            self.assertTrue(result["success"])
            self.assertEqual(result["name"], "HUC Test")
            self.assertEqual(result["module_count"], 1)

    def test_missing_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "empty.mcpack"

            with zipfile.ZipFile(path, "w"):
                pass

            result = analyze_bedrock_pack(str(path))

            self.assertFalse(result["success"])

    def test_missing_file(self):
        result = analyze_bedrock_pack("missing.mcpack")

        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
  
