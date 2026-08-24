---
id: 01
role: Operator
status: ready_after_seal
reads:
  - PROTOCOL.md
  - KILL.md
  - research/data-inventory.md
must_not:
  - Open ICI phenotype or outcome files
  - Edit confirmatory protocol fields
---

# Unit 01 — Detection rates (Gate C)

**Goal.** Report *CNR2*, *MGLL*, and *FAAH* detection by lineage bucket and cancer type. Score Gate C. No ICI labels.

**Inputs.** Census (primary) and TISCH2 fallback only where Unit 00 recorded Census missing a type. Lineage map in `PROTOCOL.md`.

**Procedure.**

1. Load scRNA for available types among NSCLC, melanoma, CRC, BRCA, BLCA (≥2 types or stop and amend).
2. Assign lineage buckets with the locked substring map.
3. For each type × bucket, compute % cells with count > 0 for `CNR2`, `MGLL`, `FAAH`.
4. Apply Gate C rules in `KILL.md` / `PROTOCOL.md`. Do not build a raw-*CNR2* UMAP atlas if *CNR2* < 1% in every non-B lineage in every type.

**Outputs.** `research/01-detection.md` (table + Gate C call for the human).

**Pass criteria.** Table complete. Human marks Gate C. If Gate C **fail (stop the kill)**, do not continue Units 02–08 as a checkpoint path.

## Notes (after run)

-
