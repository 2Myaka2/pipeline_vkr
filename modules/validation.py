from __future__ import annotations

from typing import Iterable

from modules.config import Region


def validate_regions(universe, regions: Iterable[Region]) -> None:
    for region in regions:
        atoms = universe.select_atoms(region.selection)
        if atoms.n_atoms == 0:
            raise ValueError(
                f"Region '{region.name}' selection returned 0 atoms: {region.selection}"
            )


def validate_ca_presence(universe, regions: Iterable[Region]) -> None:
    for region in regions:
        ca = universe.select_atoms(f"({region.selection}) and name CA")
        if ca.n_atoms == 0:
            raise ValueError(
                f"Region '{region.name}' has no C-alpha atoms for RMSF: {region.selection}"
            )
