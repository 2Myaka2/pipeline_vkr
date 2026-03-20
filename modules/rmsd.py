from __future__ import annotations

import numpy as np
from MDAnalysis.analysis import align

from modules.config import Region


ANGSTROM_TO_NM = 0.1


def align_trajectory_global_ca(universe) -> None:
    reference = universe.copy()
    align.AlignTraj(
        universe,
        reference,
        select="protein and name CA",
        in_memory=True,
    ).run()


def compute_rmsd_nm(universe, regions: list[Region]) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    universe.trajectory[0]
    reference_by_region = {
        region.name: universe.select_atoms(region.selection).positions.copy()
        for region in regions
    }

    times_ps: list[float] = []
    values: dict[str, list[float]] = {region.name: [] for region in regions}

    for ts in universe.trajectory:
        times_ps.append(float(ts.time))
        for region in regions:
            ag = universe.select_atoms(region.selection)
            ref = reference_by_region[region.name]
            if ag.n_atoms != ref.shape[0]:
                raise ValueError(f"Atom count drift for region '{region.name}'.")
            diff = ag.positions - ref
            rmsd_a = float(np.sqrt(np.mean(np.sum(diff * diff, axis=1))))
            values[region.name].append(rmsd_a * ANGSTROM_TO_NM)

    return np.asarray(times_ps), {k: np.asarray(v) for k, v in values.items()}
