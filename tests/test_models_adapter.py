
import json
import struct
import tempfile
import unittest

from pathlib import Path
from huc.adapters.models import analyze_model


class ModelAdapterTests(unittest.TestCase):

    def test_gltf_model(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "test.gltf"

            data = {
                "asset": {"version": "2.0"},
                "meshes": [{}],
                "nodes": [{}, {}],
                "materials": [{}],
                "animations": [{}]
            }

            path.write_text(json.dumps(data), encoding="utf-8")

            result = analyze_model(str(path))

            self.assertTrue(result["success"])
            self.assertEqual(result["meshes"], 1)
            self.assertEqual(result["animations"], 1)

    def test_glb_model(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "test.glb"

            header = struct.pack("<4sII", b"glTF", 2, 12)
            path.write_bytes(header)

            result = analyze_model(str(path))

            self.assertTrue(result["success"])
            self.assertEqual(result["version"], 2)

    def test_bbmodel(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "test.bbmodel"

            data = {
                "name": "HUC Test",
                "meta": {"model_format": "free"},
                "elements": [{}, {}],
                "outliner": [{}],
                "animations": [],
                "textures": [{}]
            }

            path.write_text(json.dumps(data), encoding="utf-8")

            result = analyze_model(str(path))

            self.assertTrue(result["success"])
            self.assertEqual(result["elements"], 2)
            self.assertEqual(result["textures"], 1)

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "invalid.gltf"
            path.write_text("{invalid", encoding="utf-8")

            result = analyze_model(str(path))

            self.assertFalse(result["success"])

    def test_missing_file(self):
        result = analyze_model("missing_model.gltf")

        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
          
