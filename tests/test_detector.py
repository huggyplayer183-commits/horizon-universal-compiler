import tempfile
import unittest

from pathlib import Path
from huc.detector import detect_format


class DetectorTests(unittest.TestCase):

    def test_gltf_detection(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "model.gltf"
            path.write_text("{}", encoding="utf-8")

            result = detect_format(str(path))

            self.assertTrue(result["success"])
            self.assertEqual(result["format"], "gltf_model")

    def test_bbmodel_detection(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "model.bbmodel"
            path.write_text("{}", encoding="utf-8")

            result = detect_format(str(path))

            self.assertEqual(result["format"], "blockbench_model")

    def test_zip_detection(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "archive.zip"
            path.write_bytes(b"test")

            result = detect_format(str(path))

            self.assertEqual(result["format"], "archive")

    def test_unknown_format(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "file.unknown"
            path.write_text("test", encoding="utf-8")

            result = detect_format(str(path))

            self.assertFalse(result["success"])

    def test_missing_file(self):
        result = detect_format("missing_file.gltf")

        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
  
