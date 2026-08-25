---
id: 10
role: Operator
status: ready
reads:
  - PROTOCOL-ATLAS.md
  - KILL-ATLAS.md
  - research/01-detection.md
  - research/02-scrna-states.md
  - research/05-primary-state.md
must_not:
  - Add ECS genes or rename Stromal/other
  - Open ICI matrices (citation of Units 06–07 is Unit 14)
  - Run NMF, new clustering, or DE
  - Promote myeloid or T/NK catalog rows to confirmatory named states
---

# Unit 10 — Reproduce core map (Gate D)

**Goal.** Re-run the five-type ECS-state catalog on the kill pins. Confirm the same three buckets and primary **Stromal/other**.

**Inputs.** Census `2025-11-08`; BLCA TISCH2+GEO `GSE130001`. Frozen markers in `research/03-frozen-markers.json`. Lineage map in `pipeline/lineage.py`.

**Procedure.**

1. Same cell filters and scoring as Units 01–02.
2. Write type × lineage table (n, nine-gene detection, mean core-ECS, rank, contamination, ECS-state call).
3. Compare kept buckets to Unit 02. Record numeric drift. A kept↔dropped flip is a Gate D fail.

**Outputs.** `research/10-reproduce-core.md`

**Pass criteria (human):** Gate D in `KILL-ATLAS.md`.

## Notes (after run)

-
