
import struct
from pathlib import Path


JAVA_VERSIONS = {
    45: "Java 1.1",
    46: "Java 1.2",
    47: "Java 1.3",
    48: "Java 1.4",
    49: "Java 5",
    50: "Java 6",
    51: "Java 7",
    52: "Java 8",
    53: "Java 9",
    54: "Java 10",
    55: "Java 11",
    56: "Java 12",
    57: "Java 13",
    58: "Java 14",
    59: "Java 15",
    60: "Java 16",
    61: "Java 17",
    62: "Java 18",
    63: "Java 19",
    64: "Java 20",
    65: "Java 21",
    66: "Java 22",
    67: "Java 23",
    68: "Java 24",
    69: "Java 25",
}


def analyze_class_file(class_path: str) -> dict:
    path = Path(class_path)

    if not path.is_file():
        return {
            "success": False,
            "message": "Java class file not found."
        }

    try:
        data = path.read_bytes()

        if len(data) < 10:
            return {
                "success": False,
                "message": "Class file is too small."
            }

        magic, minor, major = struct.unpack_from(">IHH", data, 0)

        if magic != 0xCAFEBABE:
            return {
                "success": False,
                "message": "Invalid Java class file magic number."
            }

        constant_pool_count = struct.unpack_from(">H", data, 8)[0]

        if constant_pool_count < 1:
            return {
                "success": False,
                "message": "Invalid constant pool count."
            }

        return {
            "success": True,
            "format": "java_class",
            "minor_version": minor,
            "major_version": major,
            "java_version": JAVA_VERSIONS.get(
                major,
                "Unknown Java version"
            ),
            "constant_pool_count": constant_pool_count,
            "file_size": len(data),
            "message": "Java class header analyzed successfully."
        }

    except (OSError, struct.error) as error:
        return {
            "success": False,
            "message": f"Could not analyze class file: {error}"
        }
      
