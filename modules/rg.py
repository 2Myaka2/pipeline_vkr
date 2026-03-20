from __future__ import annotations

import numpy as np

from modules.config import Region


ANGSTROM_TO_NM = 0.1


def compute_rg_time_nm(universe, regions: list[Region]) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    times_ps: list[float] = []
    rg_by_region: dict[str, list[float]] = {region.name: [] for region in regions}

    for ts in universe.trajectory:
        times_ps.append(float(ts.time))
        for region in regions:
            ag = universe.select_atoms(region.selection)
            rg_by_region[region.name].append(float(ag.radius_of_gyration()) * ANGSTROM_TO_NM)

    return np.asarray(times_ps), {k: np.asarray(v) for k, v in rg_by_region.items()}


def compute_residue_rg_contrib_nm(universe, region: Region) -> tuple[np.ndarray, np.ndarray]:
    """
    Approximation used when notebooks do not provide a strict formula:
    per residue we compute sqrt(mean_t[(m_i/M) * ||r_i - r_com||^2]).

    This has length units (nm) and is consistent with a mass-weighted decomposition
    of Rg^2. Values are not additive in linear space; squared terms are additive.
    """
    ag = universe.select_atoms(region.selection)
    residues = ag.residues

    residue_ids = np.asarray([res.resid for res in residues], dtype=int)
    accum = np.zeros(len(residues), dtype=float)
    frames = 0

    for _ in universe.trajectory:
        total_mass = float(np.sum(ag.masses))
        com = ag.center_of_mass()

        for idx, residue in enumerate(residues):
            atom_masses = residue.atoms.masses
            residue_mass = float(np.sum(atom_masses))
            if residue_mass == 0.0 or total_mass == 0.0:
                continue
            r_i = residue.atoms.center_of_mass()
            squared_distance = float(np.sum((r_i - com) ** 2))
            accum[idx] += (residue_mass / total_mass) * squared_distance

        frames += 1

    if frames == 0:
        raise ValueError("Trajectory has zero frames.")

    mean_contrib_a = np.sqrt(accum / frames)
    return residue_ids, mean_contrib_a * ANGSTROM_TO_NM
