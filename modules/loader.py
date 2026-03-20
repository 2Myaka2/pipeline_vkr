from __future__ import annotations

from pathlib import Path

import MDAnalysis as mda


def load_universe(tpr_path: str | Path, xtc_path: str | Path) -> mda.Universe:
    tpr = Path(tpr_path)
    xtc = Path(xtc_path)
    if not tpr.exists():
        raise FileNotFoundError(f"TPR file not found: {tpr}")
    if not xtc.exists():
        raise FileNotFoundError(f"XTC file not found: {xtc}")

    return mda.Universe(str(tpr), str(xtc))
