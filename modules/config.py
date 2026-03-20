from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml


@dataclass(frozen=True)
class Region:
    name: str
    selection: str


def load_regions_config(config_path: str | Path) -> List[Region]:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    regions = data.get("regions")
    if not isinstance(regions, list) or not regions:
        raise ValueError("Config must contain non-empty top-level 'regions' list.")

    parsed: list[Region] = []
    seen_names: set[str] = set()
    for idx, item in enumerate(regions):
        if not isinstance(item, dict):
            raise ValueError(f"Region entry #{idx} must be a mapping.")

        name = str(item.get("name", "")).strip()
        selection = str(item.get("selection", "")).strip()
        if not name:
            raise ValueError(f"Region entry #{idx} has empty 'name'.")
        if not selection:
            raise ValueError(f"Region '{name}' has empty 'selection'.")
        if name in seen_names:
            raise ValueError(f"Duplicate region name in config: '{name}'.")

        seen_names.add(name)
        parsed.append(Region(name=name, selection=selection))

    return parsed
