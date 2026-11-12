import struct
import tempfile
import unittest

from pathlib import Path
from huc.adapters.java_bytecode import analyze_class_file


class JavaClassStructureTests(unittest.TestCase):

    def create_class_file(self, path):
        constants = [
            (1, b"TestClass"),
            (7, struct.pack(">H", 1)),
            (1, b"java/lang/Object"),
            (7, struct.pack(">H", 3)),
            (1, b"java/io/Serializable"),
            (7, struct.pack(">H", 5)),
            (1, b"health"),
            (1, b"I"),
            (1, b"run"),
            (1, b"()V"),
        ]

        data = bytearray(
            struct.pack(">IHHH", 0xCAFEBABE, 0, 61, 11)
        )

        for tag, payload in constants:
            data.append(tag)
            data.extend(payload)

        data.extend(struct.pack(">HHH", 0x0021, 2, 4))
        data.extend(struct.pack(">HH", 1, 6))
        data.extend(struct.pack(">H", 1))
        data.extend(struct.pack(">HHHH", 0x0001, 7, 8, 0))
        data.extend(struct.pack(">H", 1))
        data.extend(struct.pack(">HHHH", 0x0001, 9, 10, 0))
        data.extend(struct.pack(">H", 0))
        path.write_bytes(data)

    def test_class_structure(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "TestClass.class"
            self.create_class_file(path)
            result = analyze_class_file(str(path))
            self.assertTrue(result["success"])
            self.assertTrue(result["structure_available"])
            structure = result["class_structure"]
            self.assertEqual(structure["class_name"], "TestClass")
            self.assertEqual(structure["superclass"], "java/lang/Object")
            self.assertEqual(structure["interfaces"], ["java/io/Serializable"])
            self.assertEqual(structure["fields"][0]["name"], "health")
            self.assertEqual(structure["fields"][0]["descriptor"], "I")
            self.assertEqual(structure["methods"][0]["name"], "run")
            self.assertEqual(structure["methods"][0]["descriptor"], "()V")

    def test_invalid_class_structure_reference(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "Invalid.class"
            data = bytearray(struct.pack(">IHHH", 0xCAFEBABE, 0, 61, 1))
            data.extend(struct.pack(">HHHH", 0x0021, 1, 0, 0))
            data.extend(struct.pack(">HHHH", 0, 0, 0, 0))
            data.extend(struct.pack(">H", 0))
            path.write_bytes(data)
            result = analyze_class_file(str(path))
            self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
          
