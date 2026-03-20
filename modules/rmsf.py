from __future__ import annotations

import numpy as np
from MDAnalysis.analysis import rms

from modules.config import Region


ANGSTROM_TO_NM = 0.1


def compute_rmsf_nm_by_region(universe, regions: list[Region]) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    results: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for region in regions:
        ca = universe.select_atoms(f"({region.selection}) and name CA")
        if ca.n_atoms == 0:
            raise ValueError(f"No CA atoms found for region '{region.name}'.")

        analyzer = rms.RMSF(ca).run()
        resid = np.asarray(ca.resids, dtype=int)
        rmsf_nm = np.asarray(analyzer.results.rmsf, dtype=float) * ANGSTROM_TO_NM
        results[region.name] = (resid, rmsf_nm)

    return results
