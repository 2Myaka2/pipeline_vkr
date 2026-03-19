---
name: notebook-to-module-md
description: Use after repository audit to extract MD analysis logic from notebooks and existing scripts and convert it into small reusable modules with minimal redesign.
---

# Purpose
Convert existing notebook-based MD analysis logic into reusable Python modules without rewriting the whole project.

# When to use
- Relevant RMSD, RMSF, Rg, SASA, plotting, or trajectory-loading logic already exists in notebooks or scripts.
- The assignment requires a clean pipeline entrypoint and modular structure.
- Minimal invasive changes are preferred over a full redesign.

# What to do
1. Identify the exact notebook cells or script sections that implement:
   - RMSD
   - RMSF
   - radius of gyration
   - SASA
   - trajectory loading
   - plotting
2. Separate reusable computational logic from notebook-only code such as:
   - display and plotting glue;
   - exploratory cells;
   - debug prints;
   - Colab-specific code;
   - hardcoded local paths.
3. Move the reusable logic into small functions with clear inputs and outputs.
4. Preserve assignment-required public behavior:
   - required CLI interface;
   - required output file names;
   - required CSV column names;
   - YAML-driven regions;
   - reproducible command-line execution.
5. Keep implementation aligned with the assignment first, then README, then existing repo behavior.
6. Document scientific or methodological assumptions when notebook logic is ambiguous or incomplete.

# Special caution
For residue-wise contribution to Rg:
- prefer an existing notebook formula if one is present;
- if no explicit formula exists, implement a clearly documented approximation;
- explain the chosen definition in code comments and README.

# Output
Produce modular functions that can be called from the main pipeline entrypoint and plotting workflow.

# Rules
- Minimal redesign.
- No unnecessary abstractions.
- No silent unit conversions.
- Document Å/nm handling explicitly.
- Do not rewrite unrelated ML, topology, or reporting parts of the project.