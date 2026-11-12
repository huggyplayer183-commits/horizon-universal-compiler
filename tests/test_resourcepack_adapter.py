
import json
import tempfile
import unittest
import zipfile

from pathlib import Path
from huc.adapters.resourcepack import analyze_resource_pack


class ResourcePackTests(unittest.TestCase):

    def test_valid_resource_pack_zip(self):
        with tempfile.TemporaryDirectory() as temp:
            pack = Path(temp) / "test_pack.zip"

            manifest = {
                "pack": {
                    "pack_format": 15,
                    "description": "HUC Test Pack"
                }
            }

            with zipfile.ZipFile(pack, "w") as archive:
                archive.writestr(
                    "pack.mcmeta",
                    json.dumps(manifest)
                )
                archive.writestr(
                    "assets/minecraft/test.txt",
                    "HUC test"
                )

            result = analyze_resource_pack(str(pack))

            self.assertTrue(result["success"])
            self.assertEqual(result["pack_format"], 15)
            self.assertTrue(result["has_assets"])

    def test_missing_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            pack = Path(temp) / "empty.zip"

            with zipfile.ZipFile(pack, "w"):
                pass

            result = analyze_resource_pack(str(pack))

            self.assertFalse(result["success"])

    def test_missing_file(self):
        result = analyze_resource_pack("nonexistent_pack.zip")

        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
  
