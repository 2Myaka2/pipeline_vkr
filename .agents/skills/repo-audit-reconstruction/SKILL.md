---
name: repo-audit-reconstruction
description: Use at the start of work in a messy research repository to identify source-of-truth notebooks, relevant scripts, conflicts between assignment and README, and the minimal implementation path for mandatory items 1–6.
---

# Purpose
Run this skill before major edits in order to avoid blind refactoring.

# When to use
- The repository is messy or research-oriented.
- The assignment scope is narrower than the repository scope.
- Notebooks likely contain the real working logic.
- You need to decide what to reuse instead of rewriting everything.

# What to do
1. Read the assignment and extract non-negotiable requirements.
2. Read README.md as an operational reference.
3. Scan the repository for notebooks, MD analysis scripts, plotting code, configs, and dependency files.
4. Search for RMSD, RMSF, radius of gyration, SASA, MDAnalysis, ShrakeRupley, YAML config parsing, argparse, pandas, and matplotlib.
5. Produce a short audit summary:
   - relevant files;
   - likely source-of-truth notebooks;
   - conflicts between assignment and README;
   - minimal implementation path.

# Output
Produce a short audit note that can directly drive the implementation plan.

# Rules
- Focus only on mandatory items 1–6.
- Prefer reusing notebooks and working fragments over inventing a new architecture.
- Do not start major code edits before the audit summary exists.