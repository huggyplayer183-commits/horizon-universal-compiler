import io
import json
import tempfile
import unittest
import zipfile

from pathlib import Path
from huc.adapters.bedrock import analyze_bedrock_pack


class BedrockAdapterTests(unittest.TestCase):

    def create_manifest(self):
        return {
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

    def test_valid_bedrock_pack(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bedrock.mcpack"

            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(
                    "manifest.json",
                    json.dumps(self.create_manifest())
                )

            result = analyze_bedrock_pack(str(path))

            self.assertTrue(result["success"])
            self.assertEqual(result["name"], "HUC Test")
            self.assertEqual(result["module_count"], 1)

    def test_valid_mcaddon(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bedrock.mcaddon"

            nested_buffer = io.BytesIO()

            with zipfile.ZipFile(nested_buffer, "w") as nested:
                nested.writestr(
                    "manifest.json",
                    json.dumps(self.create_manifest())
                )

            with zipfile.ZipFile(path, "w") as addon:
                addon.writestr(
                    "resource_pack.mcpack",
                    nested_buffer.getvalue()
                )

            result = analyze_bedrock_pack(str(path))

            self.assertTrue(result["success"])
            self.assertEqual(result["format"], "bedrock_addon")
            self.assertEqual(result["pack_count"], 1)
            self.assertEqual(result["packs"][0]["name"], "HUC Test")

    def test_mcaddon_without_packs(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "empty.mcaddon"

            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("example.txt", "HUC")

            result = analyze_bedrock_pack(str(path))

            self.assertFalse(result["success"])

    def test_missing_file(self):
        result = analyze_bedrock_pack("missing.mcpack")

        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
    
