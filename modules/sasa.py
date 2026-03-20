from __future__ import annotations

import numpy as np
from mdakit_sasa.analysis.sasaanalysis import SASAAnalysis

from modules.config import Region

ANGSTROM2_TO_NM2 = 0.01


def compute_sasa_nm2(universe, regions: list[Region]) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """
    Compute SASA in nm^2 for each configured region.

    Methodological note:
    `mdakit-sasa` exposes trajectory-wise total SASA for a selected group, but
    does not expose the atomwise SASA array used by the old Shrake-Rupley path.
    Region SASA is therefore computed by a separate SASAAnalysis run for each
    region selection, not by computing full-structure SASA and aggregating
    atom-level contributions afterward.
    """
    times_ps: np.ndarray | None = None
    result: dict[str, np.ndarray] = {}

    for region in regions:
        analysis = SASAAnalysis(universe, select=region.selection)
        analysis.run()

        region_times = np.asarray(analysis.times, dtype=float)
        region_sasa_nm2 = (
            np.asarray(analysis.results.total_area, dtype=float) * ANGSTROM2_TO_NM2
        )

        if times_ps is None:
            times_ps = region_times
        elif not np.allclose(times_ps, region_times):
            raise ValueError(
                f"SASA time grid mismatch for region '{region.name}'."
            )

        result[region.name] = region_sasa_nm2

    if times_ps is None:
        return np.asarray([], dtype=float), {}

    return times_ps, result
