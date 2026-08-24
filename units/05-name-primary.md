---
id: 05
role: Operator
status: ready_after_seal
reads:
  - PROTOCOL.md
  - KILL.md
  - research/02-scrna-states.md
  - research/04-tcga-confound.md
must_not:
  - Open any IMvigor210 or GEO phenotype/outcome file
  - Run Gate B
---

# Unit 05 — Name primary non-B state (A→B wall)

**Goal.** Apply the locked naming rule. Commit the primary state **before** ICI outcomes are opened. Human marks Gate A.

**Inputs.** Units 02–04 outputs only.

**Procedure.**

1. Confirm Gate A both-parts: ≥2 lineage buckets with an ECS state **and** ≥1 non-B candidate that passed confound tests (including residual cap if used).
2. If several non-B candidates qualify: primary = lowest `max(|r_B|, |r_TLS|)` on pooled **raw** Pearson. Tie: present in more of the five cancer types. Tie: myeloid > T/NK > malignant/epithelial > stromal/other.
3. Commit name, lineage, nine genes, four Pearson values, residual ratios if used, contamination rates.
4. If no non-B candidate qualifies: Gate A fails. **Do not** open ICI outcomes for a checkpoint test.

**Outputs.** `research/05-primary-state.md` + git commit of that file.

**Pass criteria.** Primary name is in git **or** Gate A fail is recorded. No ICI files have been opened.

## Notes (after run)

-
