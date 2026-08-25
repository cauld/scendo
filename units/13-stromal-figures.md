---
id: 13
role: Operator
status: done
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

- **2026-08-25 complete.** `research/13-stromal-figures.md` + `docs/diagrams/13-mean-ecs.png`, `13-detection-stromal.png`, `13-stromal-composition.png`. Runner: `uv run python pipeline/figures_13.py`. Stromal n matches Units 10/12 on all 11 types (0 mismatches). No UMAP. No clustering / DE. No ICI files.
- Composition is display-only. Primary remains **Stromal/other**. Fibroblast-rich: OV 86%, BLCA 60%, BRCA 46%. Unmatched-heavy (existing labels, not a new state): STAD 96% (`unknown`), GBM 95% (microglia / oligodendrocyte / neoplastic), CRC 87% (stem cell), KIRC 80% (`abnormal cell` / `unknown`).
- Heatmaps: type × bucket mean core-ECS (Units 10+12); nine-gene detection in Stromal/other; subtype % of stromal. **Next:** Unit 14 converge + frozen ICI (Gate F).
