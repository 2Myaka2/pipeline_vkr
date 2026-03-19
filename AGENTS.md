# AGENTS.md

## Project scope
Implement only the mandatory assignment items 1–6 for the MD analysis pipeline.
Do not work on optional extensions / section 9 unless explicitly requested.

## Source priority
Use sources in this order:
1. assignment file;
2. README.md;
3. repository structure, notebooks, and existing scripts.

If README.md conflicts with the assignment, follow the assignment and document the conflict.

## Working style
This is a research repository with many intermediate artifacts.
Prefer reconstructing working logic from notebooks and existing scripts instead of inventing a brand-new design.
Use README.md as an operational reference, not as a source that overrides the formal assignment.
Before major edits, first inspect the assignment, README.md, relevant notebooks, and existing scripts, then produce a short implementation plan.

## Data and Git rules
Do not commit heavy data, trajectories, generated plots, or bulky results.
A large `results` directory may exist outside the repository, in the same parent directory as the repo.
Support explicit paths and avoid hardcoded local absolute paths.

## Code rules
Keep changes minimally invasive.
Prefer modular, readable, reproducible code.
Do not restructure the whole repository unless it is necessary to satisfy assignment items 1–6.
Do not rewrite unrelated ML/topology/reporting parts of the project.
Preserve assignment-defined CLI, output filenames, and CSV column names unless the assignment explicitly allows otherwise.
Document scientific or methodological assumptions explicitly, especially for residue-wise contribution to Rg.
Do not silently mix units; document any unit conversions explicitly.

## Validation
Before finishing, run a smoke test or validation run on available data.
If full validation is too heavy, do a partial check and say exactly what was verified.
Never invent results.

## Final report
Before completion, report:
- what was implemented;
- which files were changed;
- how to run the pipeline;
- what was validated;
- what assumptions remain;
- what came from notebooks;
- what came from README.md;
- what was implemented independently.