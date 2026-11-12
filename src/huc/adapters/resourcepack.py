import json
import zipfile
from pathlib import Path


def analyze_resource_pack(pack_path: str) -> dict:
    path = Path(pack_path)

    if not path.exists():
        return {
            "success": False,
            "message": "Resource pack not found."
        }

    if path.is_dir():
        return analyze_folder(path)

    if not zipfile.is_zipfile(path):
        return {
            "success": False,
            "message": "Invalid resource pack archive."
        }

    try:
        with zipfile.ZipFile(path, "r") as archive:
            files = archive.namelist()

            if "pack.mcmeta" not in files:
                return {
                    "success": False,
                    "message": "pack.mcmeta not found."
                }

            manifest = json.loads(
                archive.read("pack.mcmeta").decode("utf-8")
            )

            return create_result(manifest, files)

    except (OSError, zipfile.BadZipFile, UnicodeDecodeError,
            json.JSONDecodeError) as error:
        return {
            "success": False,
            "message": f"Could not analyze resource pack: {error}"
        }


def analyze_folder(path: Path) -> dict:
    manifest_path = path / "pack.mcmeta"

    if not manifest_path.is_file():
        return {
            "success": False,
            "message": "pack.mcmeta not found."
        }

    try:
        with manifest_path.open("r", encoding="utf-8") as file:
            manifest = json.load(file)

        files = [
            str(item.relative_to(path))
            for item in path.rglob("*")
            if item.is_file()
        ]

        return create_result(manifest, files)

    except (OSError, json.JSONDecodeError) as error:
        return {
            "success": False,
            "message": f"Could not analyze resource pack: {error}"
        }


def create_result(manifest: dict, files: list) -> dict:
    pack = manifest.get("pack", {})

    return {
        "success": True,
        "format": "minecraft_resource_pack",
        "pack_format": pack.get("pack_format"),
        "description": pack.get("description"),
        "has_assets": any(
            item.startswith("assets/")
            for item in files
        ),
        "file_count": len(files)
    }
  
