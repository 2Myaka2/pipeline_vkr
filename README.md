# NAPI2B MD Analysis Pipeline (Mandatory items 1–6)

This repository now includes a minimal, assignment-aligned MD analysis CLI pipeline focused only on mandatory MD metrics (RMSD, RMSF, Rg, residue-wise Rg contribution, SASA) using MDAnalysis.

> Scope note: this pipeline intentionally does **not** implement optional extensions, section 9, or broader ML/topology workflows.

## WSL/Linux setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Inputs

Required inputs are explicit file paths:
- `--tpr`: topology file (`.tpr`)
- `--xtc`: trajectory file (`.xtc`)
- `--config`: YAML with top-level `regions` list; each region has:
  - `name`
  - `selection` (MDAnalysis selection syntax)
- `--output`: output directory

Example `regions.yaml` (see `regions.example.yaml`):

```yaml
regions:
  - name: full_protein
    selection: "protein"
  - name: extracellular_domain
    selection: "protein and resid 233-360"
  - name: epitope_323_337
    selection: "protein and resid 323-337"
```

## Run command (assignment contract)

```bash
python run_pipeline.py --tpr <file.tpr> --xtc <file.xtc> --config <regions.yaml> --output <dir>
```

Concrete example:

```bash
python run_pipeline.py \
  --tpr ../results/md_trajectories/normal/prod.tpr \
  --xtc ../results/md_trajectories/normal/prod.xtc \
  --config regions.example.yaml \
  --output out_md
```

## Outputs

The pipeline writes:

- `rmsd.csv` with columns: `time_ps`, one column per region
- `rmsf_<region>.csv` with columns: `resid,rmsf_nm`
- `rg_time.csv` with columns: `time_ps`, one column per region
- `rg_residues_<region>.csv` with columns: `resid,rg_contribution_nm`
- `sasa_<region>.csv` with columns: `time_ps,sasa_nm2`
- `plots/*.png`

## Metric definitions and units

- **RMSD**: computed after global trajectory alignment on `protein and name CA`; output in **nm**.
- **RMSF**: computed on **C-alpha atoms** only; output in **nm**.
- **Rg time series**: standard radius of gyration per region; output in **nm**.
- **Residue-wise Rg contribution**: approximation
  \(\sqrt{\langle (m_i/M) \|r_i-r_{COM}\|^2 \rangle_t}\), output in **nm**.
  This is documented explicitly because notebooks do not define a strict canonical residue-wise formula.
- **SASA**: computed with mdakit-sasa by running a separate selected analysis for each configured region; region SASA is not derived from full-structure atomwise aggregation; output in **nm²**.

The code converts from MDAnalysis default Å / Å² to nm / nm² explicitly.


## Validation status

- CLI parser smoke check (`python run_pipeline.py --help`) is implemented to work without importing MDAnalysis before argument parsing.
- If runtime dependencies or trajectory files are unavailable in the execution environment, full end-to-end validation on real `.tpr/.xtc` inputs remains **pending** and must be run in a properly provisioned environment.

## External results directory handling

In this research repository, large trajectory/results data can exist outside Git in a sibling folder (for example `../results`).
Use explicit `--tpr` and `--xtc` paths; do not hardcode absolute local paths in scripts.

## Legacy project materials

The repository also contains notebooks and historical outputs for ML/topology/reporting experiments. They are retained as reference artifacts and are not required to run this mandatory MD pipeline.
