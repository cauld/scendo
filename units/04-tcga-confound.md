---
id: 04
role: Operator
status: done
reads:
  - PROTOCOL.md
  - KILL.md
  - research/03-frozen-markers.json
must_not:
  - Open ICI phenotype or outcome files
  - Choose the primary state (that is Unit 05)
---

# Unit 04 — TCGA confound (Gate A)

**Goal.** Score non-B ECS states in TCGA. Compute Pearson (and Spearman) vs B-cell and TLS signatures in pooled TCGA and in TCGA-BLCA. Apply residual-escape rules if needed.

**Inputs.** Frozen markers from Unit 03. TCGA RNA for LUAD, LUSC, SKCM, COAD, READ, BRCA, BLCA.

**Procedure.**

1. Within-cohort z-score (pooled TCGA is its own window; BLCA is a separate window). Available-case mean per `PROTOCOL.md`.
2. For each non-B candidate: Pearson |r| vs B and vs TLS in pooled **and** in BLCA.
3. If a Pearson test fails (|r| ≥ 0.6): residualize `raw ~ B + TLS` on **that same cohort**. Rescue only if residual SD / raw SD ≥ 0.5 **and** |r_B| < 0.75 **and** |r_TLS| < 0.75. If either |r| ≥ 0.75, no escape for that cohort.
4. Report Spearman as descriptive. Do not name the primary state here.

**Outputs.** `research/04-tcga-confound.md` (four Pearson r values per candidate, residual ratios if used).

**Pass criteria.** Numbers exist for Unit 05. If BLCA RNA is missing, stop and amend before Gate B.

## Notes (after run)

- **2026-08-24 complete.** `research/04-tcga-confound.md`. Runner: `uv run python pipeline/confound_04.py`. TOIL `tcga_RSEM_gene_tpm`, n=3664 pooled / 426 BLCA (complete cases). No ICI files. Primary state not named.
- Non-B candidates: Malignant/epithelial, Stromal/other. Same nine-gene bulk score (no DE). Pooled Pearson r_B=0.417, r_TLS=0.383; BLCA r_B=0.361, r_TLS=0.263. Both |r| < 0.6; residual escape not used. Both candidates qualify.
- Two-lineage rule still holds (B/plasma + two non-B). Human marks Gate A in Unit 05. **Next:** Unit 05 name primary (still no ICI outcomes).
