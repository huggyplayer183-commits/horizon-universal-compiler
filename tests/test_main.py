import contextlib
import io
import sys
import tempfile
import unittest

from pathlib import Path
from unittest.mock import patch

from huc.main import main


class MainTests(unittest.TestCase):

    def run_main(self, path):
        output = io.StringIO()

        with patch.object(sys, "argv", ["huc", str(path)]):
            with contextlib.redirect_stdout(output):
                main()

        return output.getvalue()

    def test_model_dispatch(self):
        with tempfile.TemporaryDirectory() as temp:
            model = Path(temp) / "test.gltf"
            model.write_text("{}", encoding="utf-8")

            expected = {
                "success": True,
                "format": "gltf",
                "meshes": 1
            }

            with patch(
                "huc.main.analyze_model",
                return_value=expected
            ) as analyzer:
                output = self.run_main(model)

            analyzer.assert_called_once_with(str(model))
            self.assertIn('"format": "gltf"', output)

    def test_archive_dispatch(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "test.zip"
            archive.write_bytes(b"test")

            expected = {
                "success": True,
                "format": "archive",
                "detected_types": []
            }

            with patch(
                "huc.main.analyze_archive",
                return_value=expected
            ) as analyzer:
                output = self.run_main(archive)

            analyzer.assert_called_once_with(str(archive))
            self.assertIn('"format": "archive"', output)

    def test_bedrock_dispatch(self):
        with tempfile.TemporaryDirectory() as temp:
            pack = Path(temp) / "test.mcpack"
            pack.write_bytes(b"test")

            expected = {
                "success": True,
                "format": "bedrock_pack",
                "name": "HUC Test"
            }

            with patch(
                "huc.main.analyze_bedrock_pack",
                return_value=expected
            ) as analyzer:
                output = self.run_main(pack)

            analyzer.assert_called_once_with(str(pack))
            self.assertIn('"format": "bedrock_pack"', output)


if __name__ == "__main__":
    unittest.main()
    
