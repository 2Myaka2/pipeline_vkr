---
name: deps-and-readme-finish
description: Use at the end of implementation to finalize requirements.txt and README.md so the delivered pipeline is runnable in WSL/Linux and aligned with the assignment.
---

# Purpose
Make the finished pipeline understandable, installable, and runnable by another developer.

# When to use
- After implementation.
- After smoke validation.
- When the existing README is broader than the actual delivered scope.
- When old documentation needs to be narrowed to assignment items 1–6.

# What to do
1. Reduce requirements to what is actually needed for mandatory assignment items 1–6.
2. Ensure README explains:
   - installation in WSL/Linux;
   - required inputs;
   - regions.yaml format;
   - exact pipeline run command;
   - expected output files;
   - output directory structure;
   - external results directory convention if relevant;
   - assumptions and limitations.
3. Make README consistent with the assignment.
4. If README currently covers broader workflows, keep them secondary and make the assignment-specific quick-start path explicit.
5. Include at least one exact example command that matches the implemented CLI.

# Output
Produce a cleaned and focused requirements.txt and a README.md that supports reproducible local execution.

# Rules
- The assignment has priority over README.
- Keep instructions concrete and executable.
- Do not let unrelated ML, topology, or reporting workflows dominate the main quick-start path.
- Do not document functionality that was not actually implemented.