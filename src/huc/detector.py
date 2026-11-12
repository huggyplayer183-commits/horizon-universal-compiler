from pathlib import Path

SUPPORTED_FORMATS = {
    ".jar": "java_mod",
    ".zip": "archive",
    ".hmod": "horizon_mod",
    ".hnmod": "horizon_native_mod",
    ".mcpack": "bedrock_pack",
    ".mcaddon": "bedrock_addon",
    ".mrpack": "modrinth_modpack",
    ".bbmodel": "blockbench_model",
    ".gltf": "gltf_model",
    ".glb": "gltf_binary_model",
}


def detect_format(path: str) -> dict:
    file_path = Path(path)

    if not file_path.exists():
        return {
            "success": False,
            "format": None,
            "message": "File or directory not found.",
        }

    if file_path.is_dir():
        return {
            "success": True,
            "format": "project_folder",
            "message": "Project folder detected.",
        }

    extension = file_path.suffix.lower()
    detected = SUPPORTED_FORMATS.get(extension)

    if detected is None:
        return {
            "success": False,
            "format": None,
            "message": f"Unsupported format: {extension or 'no extension'}",
        }

    return {
        "success": True,
        "format": detected,
        "message": f"Detected format: {detected}",
  }
