---
id: 02
role: Operator
status: ready_after_seal
reads:
  - PROTOCOL.md
  - KILL.md
  - research/01-detection.md
must_not:
  - Open ICI phenotype or outcome files
  - Run NMF, new clustering, or DE
---

# Unit 02 — scRNA ECS states (Gate A, discovery)

**Goal.** Decide which lineage buckets have an ECS state. Apply the contamination filter (`MS4A1` → `CD19` → `CD79A`). No ICI labels.

**Inputs.** Same scRNA objects as Unit 01. Nine core genes in `PROTOCOL.md`.

**Procedure.**

1. Score each cell as the mean of the nine core genes (available-case if a gene is absent in that matrix; record drops).
2. For each type × lineage, test the “has an ECS state” rule (detection ≥5% for ≥1 core gene **and** lineage mean highest or second-highest in that dataset).
3. Per dataset, set contamination gene = first present of `MS4A1`, `CD19`, `CD79A`. Drop non-B lineages with that gene’s detection ≥ 10%. If none of the three genes is in the matrix, discard all non-B lineages from that dataset and record the reason.
4. List remaining buckets with an ECS state. Gate A already fails if fewer than two buckets remain (including B/plasma).

**Outputs.** `research/02-scrna-states.md` (per-type lineage means, contamination rates, candidate list).

**Pass criteria.** Candidates listed without ICI outcomes. Human does not yet name the primary state (Unit 05).

## Notes (after run)

-
