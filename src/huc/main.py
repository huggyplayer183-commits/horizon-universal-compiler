import argparse
import json

from huc.detector import detect_format
from huc.adapters.horizon import analyze_horizon_project


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

    if result["format"] == "project_folder":
        result = analyze_horizon_project(args.input)

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
