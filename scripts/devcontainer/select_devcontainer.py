#!/usr/bin/env python3
"""Select a devcontainer variant by copying it to the devcontainer.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEVCONTAINER_DIR = REPO_ROOT / ".devcontainer"
VARIANTS_DIR = DEVCONTAINER_DIR / "variants"
OUTPUT_CONFIG = DEVCONTAINER_DIR / "devcontainer.json"


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing configuration: {path}") from exc


def list_variants() -> list[str]:
    """List available variant names (just the folder names, not full paths)."""
    if not VARIANTS_DIR.exists():
        return []
    return sorted(
        path.parent.name
        for path in VARIANTS_DIR.glob("*/devcontainer.json")
        if path.is_file()
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy a devcontainer variant into .devcontainer/devcontainer.json",
    )
    parser.add_argument(
        "variant",
        nargs="?",
        help="Variant folder name under .devcontainer/variants",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    available = list_variants()
    if not available:
        print("No devcontainer variants were found.", file=sys.stderr)
        return 1

    # Determine the variant to use
    variant_name = None

    if not args.variant:
        # Show numbered list
        print("Please select a variant:")
        for idx, item in enumerate(available, 1):
            print(f"  {idx}. {item}")
        return 1

    # Check if user provided a number
    if args.variant.isdigit():
        variant_idx = int(args.variant) - 1
        if 0 <= variant_idx < len(available):
            variant_name = available[variant_idx]
        else:
            print(f"Invalid selection '{args.variant}'. Please choose 1-{len(available)}:", file=sys.stderr)
            for idx, item in enumerate(available, 1):
                print(f"  {idx}. {item}", file=sys.stderr)
            return 1
    else:
        # User provided a name directly
        if args.variant in available:
            variant_name = args.variant
        else:
            print(f"Unknown variant '{args.variant}'. Available options:", file=sys.stderr)
            for idx, item in enumerate(available, 1):
                print(f"  {idx}. {item}", file=sys.stderr)
            return 1

    variant_path = (VARIANTS_DIR / variant_name / "devcontainer.json").resolve()

    if not variant_path.is_file():
        print(f"Error: Configuration file not found at {variant_path}", file=sys.stderr)
        return 1

    # Load the variant configuration
    variant_config = load_json(variant_path)

    # Write the variant configuration directly to the output
    OUTPUT_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CONFIG.open("w", encoding="utf-8") as handle:
        json.dump(variant_config, handle, indent=2)
        handle.write("\n")

    print(f"✓ Wrote {OUTPUT_CONFIG} using variant '{variant_name}'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
