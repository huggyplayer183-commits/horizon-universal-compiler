import json
from pathlib import Path


def analyze_horizon_project(project_path: str) -> dict:
    root = Path(project_path)

    if not root.exists() or not root.is_dir():
        return {
            "success": False,
            "message": "Invalid project directory."
        }

    manifest_path = root / "horizon-native.json"

    if not manifest_path.is_file():
        return {
            "success": False,
            "message": "horizon-native.json not found."
        }

    try:
        with manifest_path.open("r", encoding="utf-8") as file:
            manifest = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        return {
            "success": False,
            "message": f"Could not read manifest: {error}"
        }

    return {
        "success": True,
        "format": "horizon_native_project",
        "id": manifest.get("id"),
        "version": manifest.get("version"),
        "game": manifest.get("game"),
        "schema": manifest.get("schema"),
        "manifest": manifest
    }
