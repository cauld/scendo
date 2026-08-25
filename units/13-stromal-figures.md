---
id: 13
role: Operator
status: ready
reads:
  - PROTOCOL-ATLAS.md
  - research/02-scrna-states.md
  - research/10-reproduce-core.md
  - research/12-expansion-states.md
must_not:
  - Cluster or DE a new stromal state
  - Treat subtype counts as Gate A or Gate B
  - Build a UMAP or browser
---

# Unit 13 — Stromal composition and figure pack

**Goal.** Display-only composition of **Stromal/other** from existing labels, plus heatmaps of the confirmatory tables.

**Inputs.** Units 10 and 12 cell-level lineage assignments (or the same queries). Existing Census `cell_type` / TISCH2 labels.

**Procedure.**

1. Within Stromal/other, count existing labels grouped as fibroblast / endothelial / pericyte-smooth-muscle / unmatched.
2. One table per included type (core + expansion).
3. Render heatmaps of nine-gene detection and of mean core-ECS (type × bucket). PNG at 3× if Mermaid is used for flow; scientific heatmaps may be matplotlib PNGs under `docs/diagrams/` or `pipeline/output/13/`.
4. No embedding. No ICI plots.

**Outputs.** `research/13-stromal-figures.md` + figure PNGs

**Pass criteria.** Tables and figures exist. Subtypes not claimed as new confirmatory states.

## Notes (after run)

-
