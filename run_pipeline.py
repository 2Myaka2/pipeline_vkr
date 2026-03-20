from __future__ import annotations

import argparse
import csv
from pathlib import Path


def _sanitize(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in name)


def write_timeseries_csv(path: Path, times_ps, values_by_region: dict[str, list[float] | object], regions_order: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["time_ps", *regions_order])
        for i, t in enumerate(times_ps):
            writer.writerow([float(t), *[float(values_by_region[r][i]) for r in regions_order]])


def run_pipeline(tpr: str, xtc: str, config: str, output: str) -> None:
    # Lazy imports keep CLI --help usable even when MD stack is not installed.
    from modules.config import load_regions_config
    from modules.loader import load_universe
    from modules.rg import compute_residue_rg_contrib_nm, compute_rg_time_nm
    from modules.rmsd import align_trajectory_global_ca, compute_rmsd_nm
    from modules.rmsf import compute_rmsf_nm_by_region
    from modules.sasa import compute_sasa_nm2
    from modules.validation import validate_ca_presence, validate_regions
    from plot import plot_rg_residue_contrib, plot_rmsf_by_region, plot_timeseries

    regions = load_regions_config(config)
    region_names = [r.name for r in regions]

    out_dir = Path(output)
    plots_dir = out_dir / "plots"
    out_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    universe = load_universe(tpr, xtc)
    validate_regions(universe, regions)
    validate_ca_presence(universe, regions)

    align_trajectory_global_ca(universe)

    rmsd_t, rmsd_vals = compute_rmsd_nm(universe, regions)
    write_timeseries_csv(out_dir / "rmsd.csv", rmsd_t, rmsd_vals, region_names)

    rmsf_data = compute_rmsf_nm_by_region(universe, regions)
    for region_name, (resid, rmsf_nm) in rmsf_data.items():
        path = out_dir / f"rmsf_{_sanitize(region_name)}.csv"
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["resid", "rmsf_nm"])
            for r, v in zip(resid, rmsf_nm):
                writer.writerow([int(r), float(v)])

    rg_t, rg_vals = compute_rg_time_nm(universe, regions)
    write_timeseries_csv(out_dir / "rg_time.csv", rg_t, rg_vals, region_names)

    for region in regions:
        resid, contrib_nm = compute_residue_rg_contrib_nm(universe, region)
        path = out_dir / f"rg_residues_{_sanitize(region.name)}.csv"
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["resid", "rg_contribution_nm"])
            for r, v in zip(resid, contrib_nm):
                writer.writerow([int(r), float(v)])
        plot_rg_residue_contrib(region.name, resid, contrib_nm, plots_dir)

    sasa_t, sasa_vals = compute_sasa_nm2(universe, regions)
    for region_name, series in sasa_vals.items():
        path = out_dir / f"sasa_{_sanitize(region_name)}.csv"
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["time_ps", "sasa_nm2"])
            for t, v in zip(sasa_t, series):
                writer.writerow([float(t), float(v)])

    plot_timeseries(rmsd_t, rmsd_vals, "rmsd_nm", "RMSD (aligned on protein CA)", plots_dir / "rmsd.png")
    plot_rmsf_by_region(rmsf_data, plots_dir)
    plot_timeseries(rg_t, rg_vals, "rg_nm", "Radius of gyration", plots_dir / "rg_time.png")
    plot_timeseries(sasa_t, sasa_vals, "sasa_nm2", "SASA by region", plots_dir / "sasa.png")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run MD analysis pipeline (mandatory items 1–6).")
    parser.add_argument("--tpr", required=True, help="Path to input .tpr")
    parser.add_argument("--xtc", required=True, help="Path to input .xtc")
    parser.add_argument("--config", required=True, help="Path to YAML regions config")
    parser.add_argument("--output", required=True, help="Output directory")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_pipeline(args.tpr, args.xtc, args.config, args.output)


if __name__ == "__main__":
    main()
