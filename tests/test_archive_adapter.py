import tempfile
import unittest
import zipfile

from pathlib import Path
from huc.adapters.archive import analyze_archive


class ArchiveAdapterTests(unittest.TestCase):

    def test_fabric_mod(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "fabric_mod.zip"

            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("fabric.mod.json", "{}")

            result = analyze_archive(str(path))

            self.assertTrue(result["success"])
            self.assertIn("fabric_mod", result["detected_types"])

    def test_resource_pack(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "resource_pack.zip"

            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("pack.mcmeta", "{}")

            result = analyze_archive(str(path))

            self.assertTrue(result["success"])
            self.assertIn("resource_pack", result["detected_types"])

    def test_nested_resource_pack(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "nested_resource_pack.zip"

            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(
                    "assets/resourcepack/pack.mcmeta",
                    "{}"
                )

            result = analyze_archive(str(path))

            self.assertTrue(result["success"])
            self.assertIn("resource_pack", result["detected_types"])

    def test_nested_fabric_mod(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "nested_fabric.zip"

            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(
                    "mods/example/fabric.mod.json",
                    "{}"
                )

            result = analyze_archive(str(path))

            self.assertTrue(result["success"])
            self.assertIn("fabric_mod", result["detected_types"])

    def test_unknown_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "unknown.zip"

            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("example.txt", "HUC")

            result = analyze_archive(str(path))

            self.assertTrue(result["success"])
            self.assertEqual(result["detected_types"], [])

    def test_invalid_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "invalid.zip"
            path.write_text("This is not a ZIP file")

            result = analyze_archive(str(path))

            self.assertFalse(result["success"])

    def test_missing_file(self):
        result = analyze_archive("arquivo_inexistente.zip")

        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
            
