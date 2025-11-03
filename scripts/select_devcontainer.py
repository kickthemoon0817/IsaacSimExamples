#!/usr/bin/env python3
"""Select a devcontainer variant by merging it with the shared base config."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEVCONTAINER_DIR = REPO_ROOT / ".devcontainer"
BASE_CONFIG = DEVCONTAINER_DIR / "devcontainer.base.json"
VARIANTS_DIR = DEVCONTAINER_DIR / "variants"
OUTPUT_CONFIG = DEVCONTAINER_DIR / "devcontainer.json"


def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge two dictionaries, returning a new dictionary."""
    result = dict(base)
    for key, override_value in override.items():
        base_value = result.get(key)
        if isinstance(base_value, dict) and isinstance(override_value, dict):
            result[key] = deep_merge(base_value, override_value)
        else:
            result[key] = override_value
    return result


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing configuration: {path}") from exc


def list_variants() -> list[str]:
    if not VARIANTS_DIR.exists():
        return []
    return sorted(
        str(path.relative_to(VARIANTS_DIR))
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

    if not args.variant:
        print("Please specify a variant. Available options:")
        for item in available:
            print(f"  - {item}")
        return 1

    variant_path = (VARIANTS_DIR / args.variant / "devcontainer.json").resolve()

    if not variant_path.is_file():
        print(f"Unknown variant '{args.variant}'. Available options:", file=sys.stderr)
        for item in available:
            print(f"  - {item}", file=sys.stderr)
        return 1

    base_config = load_json(BASE_CONFIG)
    variant_config = load_json(variant_path)
    merged = deep_merge(base_config, variant_config)

    OUTPUT_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CONFIG.open("w", encoding="utf-8") as handle:
        json.dump(merged, handle, indent=2)
        handle.write("\n")

    print(f"Wrote {OUTPUT_CONFIG} using variant '{args.variant}'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
