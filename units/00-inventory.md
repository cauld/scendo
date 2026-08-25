---
id: 00
role: Operator
status: done
reads:
  - PROTOCOL.md
must_not:
  - Download-and-peek IMvigor210 response labels for model selection
  - Plot or model any ICI outcome vs ECS / CNR2 / B-cell scores
---

# Unit 00 — Data access inventory

**Goal.** Prove every kill-test source opens, pin exact files, and record gene coverage. No biology conclusions. **Run blocker for Units 01–08** (protocol text is already sealed).

**Inputs.**

- CELLxGENE Census Python API (primary scRNA)
- TISCH2 (fallback only; record whether each cancer type exists)
- TCGA via Xena or GDC (RNA + cancer type for LUAD, LUSC, SKCM, COAD, READ, BRCA, BLCA)
- Bioconductor `IMvigor210CoreBiologies` (or one Gene tarball / GitHub mirror with matching file hash — pin **one**)
- GEO: GSE78220, GSE91061

**Procedure.**

1. For each source: locate, license, local path, gene identifier system (symbol vs Ensembl).
2. Confirm the nine core ECS genes, the B/TLS/CD8 lists, and scRNA contamination genes (`MS4A1`, `CD19`, `CD79A`) exist in Census (or TISCH2 fallback), TCGA, IMvigor210, and both GEO matrices. Record which contamination gene is available on each scRNA matrix.
3. Pin the exact IMvigor210 extract (package version or file hash). Export to CSV/Parquet with R if needed. Do **not** open or summarize response/OS columns beyond confirming they exist (column names only).
4. Do **not** plot response vs *CNR2* or any ECS score.
5. Write `research/data-inventory.md`.

**Outputs.** `research/data-inventory.md`

**Pass criteria.** All primary sources reachable. IMvigor210 missing **>2** core ECS genes → do not run Gate B (amend or stop). Missing gene on another matrix → record; score with available-case mean per `PROTOCOL.md`. scRNA matrix missing `MS4A1`, `CD19`, and `CD79A` → that dataset cannot contribute non-B states.

## Notes (after run)

- **2026-08-24 pass.** Inventory in `research/data-inventory.md`. Runner: `uv run python pipeline/inventory_00.py`.
- All primary sources reachable. IMvigor210 pin: Gene tarball `IMvigor210CoreBiologies_1.0.1.tar.gz` (SHA256 in inventory). ECS **0** missing (Gate B not blocked). Phenotype **column names** from package `R/data.R` only; values not opened; no outcome-vs-ECS plots.
- Census LTS `2025-11-08`: NSCLC, melanoma, CRC, BRCA present. **BLCA absent** → TISCH2 fallback. Contamination gene: `MS4A1`.
- TISCH2: all five types exist. BLCA fallback dataset: `BLCA_GSE130001` (untreated primary; 4,129 cells; metadata at `data/raw/tisch2/`). Catalog gene index includes the nine ECS genes, B/TLS/CD8, and `MS4A1`/`CD19`/`CD79A`. Expression matrix not downloaded (Unit 01).
- TCGA-BLCA present on Xena phenotype (436 rows). GEO GSE78220 (symbols) and GSE91061 (Entrez) both 9/9 ECS.
