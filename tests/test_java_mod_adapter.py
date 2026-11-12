import json
import tempfile
import unittest
import zipfile

from pathlib import Path
from huc.adapters.java_mod import analyze_java_mod


class JavaModAdapterTests(unittest.TestCase):

    def test_fabric_mod(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "fabric.jar"

            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(
                    "fabric.mod.json",
                    json.dumps({
                        "id": "testmod",
                        "version": "1.0.0"
                    })
                )
                archive.writestr("com/example/Test.class", b"test")

            result = analyze_java_mod(str(path))

            self.assertTrue(result["success"])
            self.assertIn("fabric", result["detected_loaders"])
            self.assertEqual(result["class_count"], 1)

    def test_legacy_forge_mod(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "legacy.jar"

            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("mcmod.info", "[]")
                archive.writestr("example/Main.class", b"test")

            result = analyze_java_mod(str(path))

            self.assertTrue(result["success"])
            self.assertIn("legacy_forge", result["detected_loaders"])

    def test_invalid_fabric_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "invalid.jar"

            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("fabric.mod.json", "{invalid}")

            result = analyze_java_mod(str(path))

            self.assertFalse(result["success"])

    def test_invalid_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "invalid.jar"
            path.write_text("not a jar")

            result = analyze_java_mod(str(path))

            self.assertFalse(result["success"])

    def test_missing_file(self):
        result = analyze_java_mod("missing.jar")

        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
  
