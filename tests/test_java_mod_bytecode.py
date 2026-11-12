import json
import struct
import tempfile
import unittest
import zipfile

from pathlib import Path

from huc.adapters.java_mod import analyze_java_mod


class JavaModBytecodeTests(unittest.TestCase):

    def create_class_file(self):
        constants = [
            (1, b"\x00\x04Test"),
            (7, struct.pack(">H", 1)),
            (1, b"\x00\x10java/lang/Object"),
            (7, struct.pack(">H", 3)),
        ]

        data = bytearray(
            struct.pack(">IHHH", 0xCAFEBABE, 0, 61, 5)
        )

        for tag, payload in constants:
            data.append(tag)
            data.extend(payload)

        data.extend(struct.pack(">HHH", 0x0021, 2, 4))
        data.extend(struct.pack(">HH", 0, 0))
        data.extend(struct.pack(">HH", 0, 0))
        data.extend(struct.pack(">H", 0))

        return bytes(data)

    def test_analyzes_classes_inside_jar(self):
        with tempfile.TemporaryDirectory() as temp:
            jar_path = Path(temp) / "test_mod.jar"

            with zipfile.ZipFile(jar_path, "w") as archive:
                archive.writestr(
                    "fabric.mod.json",
                    json.dumps({"id": "test_mod"})
                )
                archive.writestr(
                    "Test.class",
                    self.create_class_file()
                )

            result = analyze_java_mod(str(jar_path))

            self.assertTrue(result["success"])
            self.assertEqual(result["class_count"], 1)
            self.assertEqual(result["analyzed_class_count"], 1)
            self.assertEqual(result["failed_class_count"], 0)
            self.assertEqual(
                result["analyzed_classes"][0]["class_name"],
                "Test"
            )

    def test_records_invalid_class(self):
        with tempfile.TemporaryDirectory() as temp:
            jar_path = Path(temp) / "invalid_mod.jar"

            with zipfile.ZipFile(jar_path, "w") as archive:
                archive.writestr("Invalid.class", b"INVALID")

            result = analyze_java_mod(str(jar_path))

            self.assertTrue(result["success"])
            self.assertEqual(result["class_count"], 1)
            self.assertEqual(result["analyzed_class_count"], 0)
            self.assertEqual(result["failed_class_count"], 1)
            self.assertEqual(
                result["failed_classes"],
                ["Invalid.class"]
            )


if __name__ == "__main__":
    unittest.main()
  
