from __future__ import annotations

import numpy as np
from MDAnalysis.analysis import sas

from modules.config import Region


ANGSTROM2_TO_NM2 = 0.01


def compute_sasa_nm2(universe, regions: list[Region]) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    sr = sas.ShrakeRupley(universe.trajectory.universe.atoms, mode="atom")
    sr.run()

    atom_sasa = sr.results.sasa
    times_ps = np.asarray([float(ts.time) for ts in universe.trajectory], dtype=float)

    idx_by_region: dict[str, np.ndarray] = {}
    for region in regions:
        idx_by_region[region.name] = universe.select_atoms(region.selection).indices

    result: dict[str, np.ndarray] = {}
    for region in regions:
        idx = idx_by_region[region.name]
        sasa_a2 = np.sum(atom_sasa[:, idx], axis=1)
        result[region.name] = sasa_a2 * ANGSTROM2_TO_NM2

    return times_ps, result
