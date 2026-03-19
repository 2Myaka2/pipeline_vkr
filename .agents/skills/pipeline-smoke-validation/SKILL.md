---
name: pipeline-smoke-validation
description: Use after implementation to run a lightweight validation of the MD pipeline and verify CLI behavior, CSV schemas, and plot outputs without inventing results.
---

# Purpose
Confirm that the pipeline runs and that its outputs match the assignment at a smoke-test level.

# When to use
- After implementation.
- Before final reporting.
- When full validation is too heavy and only a reduced or partial run is feasible.

# What to do
1. Run the pipeline on available data or on a smaller representative subset if full validation is too heavy.
2. Verify that:
   - CLI arguments are accepted;
   - the output directory is created or used correctly;
   - required CSV files are generated;
   - required columns are present;
   - plots are generated in a plots/ directory;
   - errors are reported clearly if something fails.
3. Record exactly:
   - what was tested;
   - what data were used;
   - whether the run was full or partial;
   - what was not validated.

# Required checks
- rmsd.csv contains time_ps and region columns
- rmsf_<region>.csv contains resid and rmsf_nm
- rg_time.csv contains time_ps and region columns
- rg_residues_<region>.csv contains resid and rg_contribution_nm
- sasa_<region>.csv contains time_ps and sasa_nm2

# Output
Produce a short validation note with:
- executed command(s);
- generated files;
- schema checks passed;
- limitations of the validation.

# Rules
- If only partial validation is possible, state that explicitly.
- Never fabricate output values.
- Never claim full scientific validation without a real run on actual data.