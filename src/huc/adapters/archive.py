import zipfile
from pathlib import Path


def analyze_archive(archive_path: str) -> dict:
    path = Path(archive_path)

    if not path.is_file():
        return {
            "success": False,
            "message": "Archive not found."
        }

    if not zipfile.is_zipfile(path):
        return {
            "success": False,
            "message": "Invalid ZIP archive."
        }

    try:
        with zipfile.ZipFile(path, "r") as archive:
            files = archive.namelist()

            if len(files) > 100000:
                return {
                    "success": False,
                    "message": "Archive contains too many entries."
                }

            file_set = set(files)

            detected_types = []

            if "pack.mcmeta" in file_set:
                detected_types.append("resource_pack")

            if "modrinth.index.json" in file_set:
                detected_types.append("modrinth_modpack")

            if "fabric.mod.json" in file_set:
                detected_types.append("fabric_mod")

            if "META-INF/mods.toml" in file_set:
                detected_types.append("forge_mod")

            if "META-INF/neoforge.mods.toml" in file_set:
                detected_types.append("neoforge_mod")

            if "manifest.json" in file_set:
                detected_types.append("bedrock_pack_or_addon")

            return {
                "success": True,
                "format": "archive",
                "detected_types": detected_types,
                "file_count": len(files),
                "message": "Archive analyzed successfully."
            }

    except (OSError, zipfile.BadZipFile) as error:
        return {
            "success": False,
            "message": f"Could not analyze archive: {error}"
              }
      
