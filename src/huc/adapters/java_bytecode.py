import struct
from collections import Counter
from pathlib import Path


JAVA_VERSIONS = {
    45: "Java 1.1", 46: "Java 1.2", 47: "Java 1.3",
    48: "Java 1.4", 49: "Java 5", 50: "Java 6",
    51: "Java 7", 52: "Java 8", 53: "Java 9",
    54: "Java 10", 55: "Java 11", 56: "Java 12",
    57: "Java 13", 58: "Java 14", 59: "Java 15",
    60: "Java 16", 61: "Java 17", 62: "Java 18",
    63: "Java 19", 64: "Java 20", 65: "Java 21",
    66: "Java 22", 67: "Java 23", 68: "Java 24",
    69: "Java 25",
}


CONSTANT_TAGS = {
    1: "Utf8", 3: "Integer", 4: "Float", 5: "Long",
    6: "Double", 7: "Class", 8: "String",
    9: "Fieldref", 10: "Methodref",
    11: "InterfaceMethodref", 12: "NameAndType",
    15: "MethodHandle", 16: "MethodType", 17: "Dynamic",
    18: "InvokeDynamic", 19: "Module", 20: "Package",
}


def _read_u2(data: bytes, offset: int) -> int:
    if offset + 2 > len(data):
        raise ValueError("Unexpected end of class file.")

    return struct.unpack_from(">H", data, offset)[0]


def _parse_constant_pool(data: bytes, offset: int, count: int):
    constants = [None] * count
    tag_counts = Counter()
    index = 1

    while index < count:
        if offset >= len(data):
            raise ValueError("Incomplete constant pool.")

        tag = data[offset]
        offset += 1

        if tag not in CONSTANT_TAGS:
            raise ValueError(f"Unknown constant pool tag: {tag}")

        tag_name = CONSTANT_TAGS[tag]
        tag_counts[tag_name] += 1

        if tag == 1:
            length = _read_u2(data, offset)
            offset += 2

            if offset + length > len(data):
                raise ValueError("Incomplete UTF-8 constant.")

            raw_text = data[offset:offset + length]
            offset += length

            constants[index] = {
                "tag": tag_name,
                "value": raw_text.decode("utf-8", errors="replace")
            }

        elif tag in (3, 4):
            if offset + 4 > len(data):
                raise ValueError("Incomplete numeric constant.")

            value = data[offset:offset + 4]
            offset += 4

            constants[index] = {
                "tag": tag_name,
                "value": value.hex()
            }

        elif tag in (5, 6):
            if offset + 8 > len(data):
                raise ValueError("Incomplete long or double constant.")

            value = data[offset:offset + 8]
            offset += 8

            constants[index] = {
                "tag": tag_name,
                "value": value.hex()
            }

            index += 1

        elif tag in (7, 8, 16, 19, 20):
            value = _read_u2(data, offset)
            offset += 2

            constants[index] = {
                "tag": tag_name,
                "value": value
            }

        elif tag in (9, 10, 11, 12, 17, 18):
            first = _read_u2(data, offset)
            second = _read_u2(data, offset + 2)
            offset += 4

            constants[index] = {
                "tag": tag_name,
                "value": [first, second]
            }

        elif tag == 15:
            if offset + 3 > len(data):
                raise ValueError("Incomplete method handle constant.")

            reference_kind = data[offset]
            reference_index = _read_u2(data, offset + 1)
            offset += 3

            constants[index] = {
                "tag": tag_name,
                "value": [reference_kind, reference_index]
            }

        index += 1

    class_names = []

    for constant in constants:
        if constant is None or constant["tag"] != "Class":
            continue

        name_index = constant["value"]

        if (
            name_index < count
            and constants[name_index] is not None
            and constants[name_index]["tag"] == "Utf8"
        ):
            class_names.append(constants[name_index]["value"])

    return {
        "constant_pool": constants,
        "tag_counts": dict(tag_counts),
        "class_names": class_names,
        "next_offset": offset
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

        constant_pool_count = _read_u2(data, 8)

        if constant_pool_count < 1:
            return {
                "success": False,
                "message": "Invalid constant pool count."
            }

        parsed = _parse_constant_pool(data, 10, constant_pool_count)

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
            "constant_pool_tags": parsed["tag_counts"],
            "class_names": parsed["class_names"],
            "file_size": len(data),
            "message": "Java class constant pool analyzed successfully."
        }

    except (OSError, struct.error, ValueError) as error:
        return {
            "success": False,
            "message": f"Could not analyze class file: {error}"
        }
        
