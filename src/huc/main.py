import argparse
import json

from huc.detector import detect_format
from huc.adapters.horizon import analyze_horizon_project
from huc.adapters.resourcepack import analyze_resource_pack
from huc.adapters.models import analyze_model


def main():
    parser = argparse.ArgumentParser(
        description="Horizon Universal Compiler"
    )

    parser.add_argument(
        "input",
        help="Path to a Minecraft project or file"
    )

    args = parser.parse_args()

    result = detect_format(args.input)

    if not result["success"]:
        print(json.dumps(result, indent=4))
        return

    input_format = result["format"]

    if input_format in ("project_folder", "horizon_project"):
        result = analyze_horizon_project(args.input)

    elif input_format == "resource_pack":
        result = analyze_resource_pack(args.input)

    elif input_format == "archive":
        result = analyze_resource_pack(args.input)

    elif input_format in (
        "blockbench_model",
        "gltf_model",
        "gltf_binary_model"
    ):
        result = analyze_model(args.input)

    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
    
