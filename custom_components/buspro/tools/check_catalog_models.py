"""Compare Buspro catalog models against maintained official HDL model list.

Usage:
    python3 custom_components/buspro/tools/check_catalog_models.py
    python3 custom_components/buspro/tools/check_catalog_models.py --strict
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
BUSPRO_PATH = REPO_ROOT / "custom_components" / "buspro"
OFFICIAL_LIST_PATH = BUSPRO_PATH / "catalog" / "official_models.json"

VIRTUAL_MODELS = {
    "HDL panel",
    "HDL Buspro AC Controller",
    "HDL Buspro Curtain Controller",
    "HDL Buspro Variable-speed Fan Output",
    "HDL Buspro On/Off Fan Output",
    "HDL Buspro Universal Switch",
}


def load_catalog_models() -> set[str]:
    """Load DEVICE_CATALOG keys without importing Home Assistant runtime."""
    package_name = "_buspro_catalog_check"
    package = types.ModuleType(package_name)
    package.__path__ = [str(BUSPRO_PATH)]
    sys.modules.setdefault(package_name, package)

    spec = importlib.util.spec_from_file_location(
        f"{package_name}.device_catalog",
        BUSPRO_PATH / "device_catalog.py",
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load device_catalog.py")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return set(module.DEVICE_CATALOG.keys())


def load_official_models(path: Path) -> set[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    models = payload.get("models", [])
    if not isinstance(models, list):
        raise ValueError("official_models.json: 'models' must be a list")
    return {str(model) for model in models}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Diff Buspro DEVICE_CATALOG against maintained official HDL model list"
        )
    )
    parser.add_argument(
        "--official-list",
        type=Path,
        default=OFFICIAL_LIST_PATH,
        help="Path to official model JSON list",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero if there are missing official models",
    )
    args = parser.parse_args()

    official_models = load_official_models(args.official_list)
    catalog_models = load_catalog_models()
    physical_catalog_models = catalog_models - VIRTUAL_MODELS

    missing_in_catalog = sorted(official_models - physical_catalog_models)
    catalog_only = sorted(physical_catalog_models - official_models)
    virtual_models = sorted(catalog_models & VIRTUAL_MODELS)

    print("Buspro catalog model diff")
    print(f"- official models: {len(official_models)}")
    print(f"- catalog models: {len(catalog_models)}")
    print(f"- virtual models: {len(virtual_models)}")
    print(f"- physical catalog models: {len(physical_catalog_models)}")
    print()

    print(f"Missing in catalog ({len(missing_in_catalog)}):")
    for model in missing_in_catalog:
        print(f"  - {model}")
    if not missing_in_catalog:
        print("  - none")
    print()

    print(f"Catalog-only (not in official list) ({len(catalog_only)}):")
    for model in catalog_only:
        print(f"  - {model}")
    if not catalog_only:
        print("  - none")
    print()

    print(f"Virtual models ({len(virtual_models)}):")
    for model in virtual_models:
        print(f"  - {model}")

    if args.strict and missing_in_catalog:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
