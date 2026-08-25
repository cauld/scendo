---
id: 12
role: Operator
status: ready
reads:
  - PROTOCOL-ATLAS.md
  - KILL-ATLAS.md
  - research/11-expansion-inventory.md
must_not:
  - Promote an expansion lineage to a new confirmatory state
  - Rename the primary
  - Open ICI outcomes
---

# Unit 12 — Expansion ECS-state tables (Gate E)

**Goal.** Same detection / mean / contamination / ECS-state table as Unit 10, for every **included** expansion type.

**Inputs.** Unit 11 include list. Nine core genes. Locked lineage and contamination rules.

**Procedure.**

1. For each included type, assign lineage buckets and score as in Unit 02.
2. Write the full type × lineage table.
3. Skipped types: one-line reason only (from Unit 11).
4. Do not change which buckets are confirmatory **named** states (still B/plasma, Malignant/epithelial, Stromal/other). Score all five lineage buckets. Expansion ECS-state calls are catalog rows; myeloid / T/NK true-calls do not become confirmatory named states.

**Outputs.** `research/12-expansion-states.md`

**Pass criteria (human):** Gate E in `KILL-ATLAS.md`.

## Notes (after run)

-
