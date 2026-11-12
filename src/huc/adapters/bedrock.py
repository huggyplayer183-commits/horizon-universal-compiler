import io
import json
import zipfile
from pathlib import Path


def read_manifest(archive):
    manifests = [
        name for name in archive.namelist()
        if Path(name).name == "manifest.json"
    ]

    if len(manifests) != 1:
        raise ValueError("A unique manifest.json was not found.")

    return json.loads(
        archive.read(manifests[0]).decode("utf-8")
    )


def analyze_bedrock_pack(pack_path: str) -> dict:
    path = Path(pack_path)

    if not path.is_file():
        return {
            "success": False,
            "message": "Bedrock pack not found."
        }

    try:
        if not zipfile.is_zipfile(path):
            return {
                "success": False,
                "message": "Invalid Bedrock archive."
            }

        with zipfile.ZipFile(path, "r") as archive:
            if path.suffix.lower() == ".mcaddon":
                packs = []

                nested_packs = [
                    name for name in archive.namelist()
                    if name.lower().endswith(".mcpack")
                ]

                for pack_name in nested_packs:
                    content = archive.read(pack_name)

                    with zipfile.ZipFile(
                        io.BytesIO(content), "r"
                    ) as nested_archive:
                        manifest = read_manifest(nested_archive)

                    packs.append({
                        "name": manifest.get("header", {}).get("name"),
                        "description": manifest.get("header", {}).get("description"),
                        "uuid": manifest.get("header", {}).get("uuid"),
                        "modules": manifest.get("modules", [])
                    })

                if not packs:
                    return {
                        "success": False,
                        "message": "No MCpack files found inside MCAddon."
                    }

                return {
                    "success": True,
                    "format": "bedrock_addon",
                    "pack_count": len(packs),
                    "packs": packs
                }

            manifest = read_manifest(archive)

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
        json.JSONDecodeError,
        ValueError
    ) as error:
        return {
            "success": False,
            "message": f"Could not analyze Bedrock pack: {error}"
        }
        
