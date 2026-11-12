
import struct
import tempfile
import unittest

from pathlib import Path
from huc.adapters.java_bytecode import analyze_class_file


class JavaConstantPoolTests(unittest.TestCase):

    def create_class_file(self, path, constants):
        data = bytearray(
            struct.pack(">IHHH", 0xCAFEBABE, 0, 61, len(constants) + 1)
        )

        for tag, payload in constants:
            data.append(tag)
            data.extend(payload)

        path.write_bytes(data)

    def test_utf8_constant(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "Text.class"
            text = b"TestClass"
            constants = [
                (1, struct.pack(">H", len(text)) + text)
            ]

            self.create_class_file(path, constants)
            result = analyze_class_file(str(path))

            self.assertTrue(result["success"])
            self.assertEqual(result["constant_pool_tags"]["Utf8"], 1)

    def test_class_reference(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "Class.class"
            name = b"example/Test"
            constants = [
                (1, struct.pack(">H", len(name)) + name),
                (7, struct.pack(">H", 1))
            ]

            self.create_class_file(path, constants)
            result = analyze_class_file(str(path))

            self.assertTrue(result["success"])
            self.assertEqual(result["class_names"], ["example/Test"])
            self.assertEqual(result["constant_pool_tags"]["Class"], 1)

    def test_method_reference(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "Method.class"
            name = b"example/Test"
            method_name = b"run"
            descriptor = b"()V"

            constants = [
                (1, struct.pack(">H", len(name)) + name),
                (7, struct.pack(">H", 1)),
                (1, struct.pack(">H", len(method_name)) + method_name),
                (1, struct.pack(">H", len(descriptor)) + descriptor),
                (12, struct.pack(">HH", 3, 4)),
                (10, struct.pack(">HH", 2, 5))
            ]

            self.create_class_file(path, constants)
            result = analyze_class_file(str(path))

            self.assertTrue(result["success"])
            self.assertEqual(result["constant_pool_tags"]["Methodref"], 1)

    def test_incomplete_constant_pool(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "Incomplete.class"
            data = struct.pack(
                ">IHHHB", 0xCAFEBABE, 0, 61, 2, 1
            )

            path.write_bytes(data)
            result = analyze_class_file(str(path))

            self.assertFalse(result["success"])

    def test_unknown_constant_tag(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "Unknown.class"
            data = struct.pack(
                ">IHHHB", 0xCAFEBABE, 0, 61, 2, 99
            )

            path.write_bytes(data)
            result = analyze_class_file(str(path))

            self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
  
