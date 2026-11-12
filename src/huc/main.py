import argparse
import json

from detector import detect_format


def main():
    parser = argparse.ArgumentParser(
        description="Horizon Universal Compiler"
    )

    parser.add_argument(
        "input",
        help="Path to the Minecraft project or file"
    )

    args = parser.parse_args()

    result = detect_format(args.input)

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
