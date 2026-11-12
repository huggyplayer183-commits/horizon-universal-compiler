
import json
import struct
from pathlib import Path


def analyze_model(model_path: str) -> dict:
    path = Path(model_path)

    if not path.is_file():
        return {
            "success": False,
            "message": "Model file not found."
        }

    extension = path.suffix.lower()

    try:
        if extension == ".gltf":
            return analyze_gltf(path)

        if extension == ".glb":
            return analyze_glb(path)

        if extension == ".bbmodel":
            return analyze_bbmodel(path)

        return {
            "success": False,
            "message": f"Unsupported model format: {extension}"
        }

    except (OSError, UnicodeDecodeError, json.JSONDecodeError,
            ValueError, struct.error) as error:
        return {
            "success": False,
            "message": f"Could not analyze model: {error}"
        }


def analyze_gltf(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    asset = data.get("asset", {})

    return {
        "success": True,
        "format": "gltf",
        "version": asset.get("version"),
        "generator": asset.get("generator"),
        "meshes": len(data.get("meshes", [])),
        "nodes": len(data.get("nodes", [])),
        "materials": len(data.get("materials", [])),
        "animations": len(data.get("animations", []))
    }


def analyze_glb(path: Path) -> dict:
    with path.open("rb") as file:
        header = file.read(12)

    if len(header) != 12:
        raise ValueError("Invalid GLB header.")

    magic, version, declared_length = struct.unpack("<4sII", header)

    if magic != b"glTF":
        raise ValueError("Invalid GLB magic signature.")

    if declared_length != path.stat().st_size:
        raise ValueError("GLB declared length does not match file size.")

    return {
        "success": True,
        "format": "glb",
        "version": version,
        "file_size": declared_length,
        "message": "GLB header validated."
    }


def analyze_bbmodel(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return {
        "success": True,
        "format": "blockbench_model",
        "name": data.get("name"),
        "model_format": data.get("meta", {}).get("model_format"),
        "elements": len(data.get("elements", [])),
        "outliner_groups": len(data.get("outliner", [])),
        "animations": len(data.get("animations", [])),
        "textures": len(data.get("textures", []))
  }
  
