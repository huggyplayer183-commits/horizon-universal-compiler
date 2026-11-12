
import json
import zipfile

from pathlib import Path


def analyze_java_mod(mod_path: str) -> dict:
    path = Path(mod_path)

    if not path.is_file():
        return {
            "success": False,
            "message": "Java mod not found."
        }

    if not zipfile.is_zipfile(path):
        return {
            "success": False,
            "message": "Invalid Java mod archive."
        }

    try:
        with zipfile.ZipFile(path, "r") as archive:
            files = [
                name for name in archive.namelist()
                if not name.endswith("/")
            ]

            if len(files) > 100000:
                return {
                    "success": False,
                    "message": "Mod contains too many entries."
                }

            file_set = set(files)

            class_files = [
                name for name in files
                if name.endswith(".class")
            ]

            java_sources = [
                name for name in files
                if name.endswith(".java")
            ]

            metadata = {
                "fabric": "fabric.mod.json" in file_set,
                "forge": "META-INF/mods.toml" in file_set,
                "neoforge": "META-INF/neoforge.mods.toml" in file_set,
                "legacy_forge": "mcmod.info" in file_set
            }

            fabric_info = None

            if metadata["fabric"]:
                try:
                    fabric_info = json.loads(
                        archive.read("fabric.mod.json").decode("utf-8")
                    )
                except (UnicodeDecodeError, json.JSONDecodeError):
                    return {
                        "success": False,
                        "message": "Invalid Fabric metadata."
                    }

            detected_loaders = [
                loader for loader, found in metadata.items()
                if found
            ]

            return {
                "success": True,
                "format": "java_mod",
                "detected_loaders": detected_loaders,
                "class_count": len(class_files),
                "source_count": len(java_sources),
                "has_fabric_metadata": metadata["fabric"],
                "has_forge_metadata": metadata["forge"],
                "has_neoforge_metadata": metadata["neoforge"],
                "has_legacy_forge_metadata": metadata["legacy_forge"],
                "fabric_info": fabric_info,
                "file_count": len(files),
                "message": "Java mod analyzed successfully."
            }

    except (OSError, zipfile.BadZipFile) as error:
        return {
            "success": False,
            "message": f"Could not analyze Java mod: {error}"
        }
      
