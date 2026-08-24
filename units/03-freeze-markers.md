---
id: 03
role: Operator
status: ready_after_seal
reads:
  - PROTOCOL.md
  - research/02-scrna-states.md
must_not:
  - Add or drop ECS genes
  - Open ICI phenotype or outcome files
---

# Unit 03 — Freeze markers

**Goal.** Commit the confirmatory marker object: nine core ECS genes + lineage bucket labels. No DE.

**Inputs.** Unit 02 candidate lineages. Gene list from `PROTOCOL.md`.

**Procedure.**

1. Write a frozen object (JSON or TSV) with: core nine genes, HGNC aliases used, lineage buckets that have an ECS state, contamination rates, cancer types used, scRNA source per type.
2. Commit that file. Do not change it except by protocol amendment.

**Outputs.** `research/03-frozen-markers.json` (or `.tsv`) + git commit of that file after Seal (or include in the next post-Seal commit).

**Pass criteria.** Marker list is exactly the nine core genes plus lineage names. No extra DE genes.

## Notes (after run)

-
