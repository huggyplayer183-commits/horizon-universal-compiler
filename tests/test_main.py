import contextlib
import io
import sys
import tempfile
import unittest

from pathlib import Path
from unittest.mock import patch

from huc.main import main


class MainTests(unittest.TestCase):

    def test_model_dispatch(self):
        with tempfile.TemporaryDirectory() as temp:
            model = Path(temp) / "test.gltf"
            model.write_text("{}", encoding="utf-8")

            expected = {
                "success": True,
                "format": "gltf",
                "meshes": 1
            }

            output = io.StringIO()

            with patch.object(sys, "argv", ["huc", str(model)]):
                with patch(
                    "huc.main.analyze_model",
                    return_value=expected
                ) as analyzer:
                    with contextlib.redirect_stdout(output):
                        main()

            analyzer.assert_called_once_with(str(model))
            self.assertIn('"format": "gltf"', output.getvalue())

    def test_archive_dispatch(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "test.zip"
            archive.write_bytes(b"test")

            expected = {
                "success": True,
                "format": "archive",
                "detected_types": []
            }

            output = io.StringIO()

            with patch.object(sys, "argv", ["huc", str(archive)]):
                with patch(
                    "huc.main.analyze_archive",
                    return_value=expected
                ) as analyzer:
                    with contextlib.redirect_stdout(output):
                        main()

            analyzer.assert_called_once_with(str(archive))
            self.assertIn('"format": "archive"', output.getvalue())


if __name__ == "__main__":
    unittest.main()
    
