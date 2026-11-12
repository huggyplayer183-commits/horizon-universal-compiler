import json
import zipfile
from pathlib import Path


def analyze_bedrock_pack(pack_path: str) -> dict:
    path = Path(pack_path)

    if not path.is_file():
        return {
            "success": False,
            "message": "Bedrock pack not found."
        }

    try:
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path, "r") as archive:
                manifest_names = [
                    name for name in archive.namelist()
                    if Path(name).name == "manifest.json"
                ]

                if len(manifest_names) != 1:
                    return {
                        "success": False,
                        "message": "A unique manifest.json was not found."
                    }

                manifest = json.loads(
                    archive.read(manifest_names[0]).decode("utf-8")
                )

        else:
            return {
                "success": False,
                "message": "Unsupported Bedrock pack container."
            }

        header = manifest.get("header", {})
        modules = manifest.get("modules", [])

        return {
            "success": True,
            "format": "bedrock_pack",
            "name": header.get("name"),
            "description": header.get("description"),
            "uuid": header.get("uuid"),
            "version": header.get("version"),
            "module_count": len(modules),
            "modules": modules
        }

    except (
        OSError,
        zipfile.BadZipFile,
        UnicodeDecodeError,
        json.JSONDecodeError
    ) as error:
        return {
            "success": False,
            "message": f"Could not analyze Bedrock pack: {error}"
        }
      
