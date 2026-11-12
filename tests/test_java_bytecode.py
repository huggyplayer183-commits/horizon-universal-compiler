
import struct
import tempfile
import unittest

from pathlib import Path
from huc.adapters.java_bytecode import analyze_class_file


class JavaBytecodeTests(unittest.TestCase):

    def create_class_file(self, path, major=61, minor=0):
        header = struct.pack(
            ">IHHH",
            0xCAFEBABE,
            minor,
            major,
            1
        )

        path.write_bytes(header)

    def test_valid_class_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "Test.class"
            self.create_class_file(path)

            result = analyze_class_file(str(path))

            self.assertTrue(result["success"])
            self.assertEqual(result["format"], "java_class")
            self.assertEqual(result["major_version"], 61)
            self.assertEqual(result["java_version"], "Java 17")

    def test_invalid_magic_number(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "Invalid.class"
            path.write_bytes(b"INVALID1234")

            result = analyze_class_file(str(path))

            self.assertFalse(result["success"])

    def test_file_too_small(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "Small.class"
            path.write_bytes(b"123")

            result = analyze_class_file(str(path))

            self.assertFalse(result["success"])

    def test_missing_file(self):
        result = analyze_class_file("missing.class")

        self.assertFalse(result["success"])

    def test_java_8_version(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "Java8.class"
            self.create_class_file(path, major=52)

            result = analyze_class_file(str(path))

            self.assertTrue(result["success"])
            self.assertEqual(result["java_version"], "Java 8")


if __name__ == "__main__":
    unittest.main()
      
