from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def _sanitize(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in name)


def plot_timeseries(times_ps: np.ndarray, values: dict[str, np.ndarray], ylabel: str, title: str, output_path: Path) -> None:
    plt.figure(figsize=(10, 5))
    for key, series in values.items():
        plt.plot(times_ps, series, label=key)
    plt.xlabel("time_ps")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_rmsf_by_region(rmsf_data: dict[str, tuple[np.ndarray, np.ndarray]], plots_dir: Path) -> None:
    for region, (resid, rmsf_nm) in rmsf_data.items():
        plt.figure(figsize=(10, 4))
        plt.plot(resid, rmsf_nm)
        plt.xlabel("resid")
        plt.ylabel("rmsf_nm")
        plt.title(f"RMSF C-alpha: {region}")
        plt.tight_layout()
        plt.savefig(plots_dir / f"rmsf_{_sanitize(region)}.png", dpi=150)
        plt.close()


def plot_rg_residue_contrib(region: str, resid: np.ndarray, contrib_nm: np.ndarray, plots_dir: Path) -> None:
    plt.figure(figsize=(10, 4))
    plt.plot(resid, contrib_nm)
    plt.xlabel("resid")
    plt.ylabel("rg_contribution_nm")
    plt.title(f"Residue-wise Rg contribution: {region}")
    plt.tight_layout()
    plt.savefig(plots_dir / f"rg_residues_{_sanitize(region)}.png", dpi=150)
    plt.close()
