# PROTOCOL (atlas phase)

**Seal status:** SEALED 2026-08-24. Git SHA in `STATUS.md`. After seal, do not edit sections marked CONFIRMATORY without a dated amendment in `STATUS.md`.

Clarify (2026-08-24) accepted five defaults: expansion list + 10k bar; Census-only expansion; no UMAP / no browser; neighbors stay exploratory; stromal sublabels display-only.

This protocol is **only the atlas-only paper** after Decide (2026-08-24): Gate A **pass**, Gate B **fail**. It does **not** replace the sealed kill protocol.

**Kill protocol (frozen):** [`PROTOCOL.md`](PROTOCOL.md), git SHA `3fbf310`. If this file and the kill protocol disagree about Gates A–C or IMvigor210 Model 1, **the kill protocol wins**. This file may not reopen Gate B.

Human-readable brief: [`PLAN-ATLAS.md`](PLAN-ATLAS.md). If PLAN-ATLAS and this file disagree, **this file wins**.

Claims ceiling: [`CLAIMS.md`](CLAIMS.md) **non-claims** plus the ICI sentence in this file (frozen **negative**). Kill gates: [`KILL.md`](KILL.md). Atlas stops: [`KILL-ATLAS.md`](KILL-ATLAS.md). `CLAIMS.md` item 3 remains the sealed either/or from the kill; this phase does not reopen it.

## CONFIRMATORY — inherited freeze (do not reopen)

Carry forward from the kill, unchanged:

- Nine core genes: `CNR1, CNR2, GPR55, TRPV1, FAAH, MGLL, DAGLA, DAGLB, NAPEPLD`
- Neighbors **out:** `GPR18, GPR119, TRPV2, ABHD6, ABHD12` (stay in `EXPLORE.md`)
- Lineage buckets and substring map: kill `PROTOCOL.md`
- Contamination gene fallback: `MS4A1` → `CD19` → `CD79A`; ≥10% drops a non-B lineage in that dataset; all three absent → drop all non-B from that dataset
- ECS-state rule: ≥1 core gene detected in ≥5% of that lineage’s cells **and** lineage mean core-ECS is highest or second-highest in that dataset
- Scoring: scRNA = available-case mean of raw counts (min 7/9); bulk = available-case mean of within-cohort gene-wise z-scores (same minima as kill)
- Named states from Unit 05: **B/plasma**, **Malignant/epithelial**, **Stromal/other**. Primary display name: **Stromal/other**
- Census pin: `2025-11-08`. BLCA pin: TISCH2 `BLCA_GSE130001` + GEO `GSE130001` (already used)
- ICI: IMvigor210 Model 1 and GSE78220 / GSE91061 **as already run** in Units 06–07. Numbers are frozen. Do not refit, do not add covariates, do not search cutoffs, do not add genes, do not add ICI cohorts.

No NMF, no new clustering, no DE. One confirmatory state per lineage bucket. Subtypes inside a bucket are **display only**.

## CONFIRMATORY — paper claim (atlas-only)

The paper is a **named-state map** plus a **frozen negative ICI chapter**.

May claim (inside `CLAIMS.md`):

1. Human tumor ECS is visible as lineage cell states on the nine-gene list.
2. At least one non-B state (**Stromal/other**) is distinguishable from B-cell / TLS abundance (Gate A, already passed).
3. The frozen Stromal/other score **does not** associate with IMvigor210 response after B + TLS + CD8 (Gate B, already failed).

Must not claim: cannabis/CBD therapy; CB2 **is** a checkpoint; GEO validates a biomarker; OS / unadjusted / deconvolution is a checkpoint association; a new ICI-positive finding from this phase.

## CONFIRMATORY — dataset roles

| Role | Dataset | Allowed |
|---|---|---|
| Core map (must reproduce) | Kill five: NSCLC, melanoma, CRC, BRCA (Census); BLCA (TISCH2+GEO, already pinned) | Detection, ECS-state calls, contamination. **No ICI labels.** |
| Expansion map | Locked list below, Census only, `is_primary_data == True` | Same tables. Skip a type if Census lacks it or n cells < 10,000 after the Unit 01 filter. **Do not** substitute a different type or a new TISCH2 dataset. |
| Confound (already done) | TCGA pooled + TCGA-BLCA from Unit 04 | Cite Unit 04. Do not recompute to rename the primary state. |
| Frozen ICI chapter | IMvigor210, GSE78220, GSE91061 as in Units 06–07 | Copy numbers into the paper. **No new analysis.** |
| Out | New ICI cohorts; GSE220635; FAERS/DDI; Tabula Sapiens / normal-tissue Census; heme cancers | Not this protocol |

**Expansion types** (Census disease labels grouped; one source per type):

`PAAD` (pancreatic adenocarcinoma), `OV` (ovarian), `PRAD` (prostate), `KIRC` (clear cell kidney), `LIHC` (hepatocellular), `STAD` (stomach), `ESCA` (esophageal), `HNSC` (head and neck squamous), `GBM` (glioblastoma), `UCEC` (endometrial), `THCA` (thyroid), `CESC` (cervical).

Unit 11 records the exact Census `disease` strings used for each group (same style as Unit 00). If several disease strings map to one type, concatenate cells (one type, one annotation source). Melanoma stays in the core five even if n < 10,000.

Heme / lymphoid malignancies are **out**. Healthy tissue is **out**.

## CONFIRMATORY — scoring and tables

For every included type × lineage bucket, report:

- n cells
- Detection % (count > 0) for all nine core genes
- Mean core-ECS (available-case raw-count mean)
- Rank of that mean among non-empty buckets (competition rank)
- Contamination gene used and % in non-B buckets
- ECS-state call (true/false) after contamination

All **five** kill lineage buckets are scored in every table (B/plasma, myeloid, T/NK, malignant/epithelial, stromal/other). A type may emit an ECS-state **catalog call** only under the kill rule. Expansion types **do not** rename the primary state and **do not** add confirmatory **named** states beyond the three frozen buckets (**B/plasma**, **Malignant/epithelial**, **Stromal/other**). Myeloid and T/NK may appear as catalog rows; they are not confirmatory named states.

**Stromal/other composition (display):** among cells already in Stromal/other, tabulate existing Census `cell_type` (or TISCH2 label) frequencies: fibroblast, endothelial, pericyte/smooth muscle, unmatched. Do not cluster. Do not declare a new confirmatory state from a subtype.

**UMAP / integration:** **not** in this protocol. No full-Census embedding, no Harmony/scVI, no raw-*CNR2*-only atlas. The map is tables (and heatmaps of those tables).

**Bulk:** do not rerun Gate A. Optional TCGA project-level detection or mean z-score plots are **exploratory** (`EXPLORE.md`); they cannot change Unit 05 or enter confirmatory tables.

## CONFIRMATORY — ICI chapter (frozen)

The atlas manuscript reports Unit 06 Model 1 as the confirmatory ICI result:

- n = 298; ECS OR 1.189 (0.551–2.563); CI includes 1; VIF(ECS) = 1.360
- Unadjusted, Model 2, Cox OS, and GEO are secondary / replication as already labeled in Units 06–07

Operator work in this phase is **citation**, not computation: paste from `research/06-imvigor210.md` and `research/07-melanoma-geo.md`. Opening ICI matrices again is allowed only to reproduce those files bit-for-bit. Any other ICI model is a protocol violation.

## CONFIRMATORY — statistics (atlas)

No new confirmatory hypothesis test on ICI outcomes.

Atlas pass metrics are **completeness and reproduction**, not p-values:

- Core five types: ECS-state catalog matches Unit 02 on Census `2025-11-08` / pinned BLCA (same three buckets kept). Small numeric drift from library versions is recorded; a bucket flipping kept↔dropped is a Gate D fail.
- Expansion: every listed type is either tabled or skipped with a reason (missing in Census **or** n < 10,000). No silent drops.
- No gene added. No ICI refit.

Spearman, extra plots, neighbor genes, deconvolution, NMF: exploratory (`EXPLORE.md`), not confirmatory.

## CONFIRMATORY — pass/fail

See [`KILL-ATLAS.md`](KILL-ATLAS.md). Bar is Gate D (reproduce core map) and Gate E (expansion table or documented skip). Gate F = ICI chapter untouched.

## How (operational)

- Code: **Python**, `pipeline/`. Laptop. No Spark, no scGPT, no browser.
- One cancer type per query, same Census access pattern as Units 01–02.
- Figures: heatmaps/tables from the atlas outputs only. Embed PNGs in markdown; Mermaid for flow diagrams per `AGENTS.md`.
- Scribe ≤ `CLAIMS.md`.

## Out of this protocol

Public browser. scGPT. GSE220635. New ICI cohorts. Neighbor genes in the confirmatory list. New clustering / NMF. Renaming **Stromal/other**. Reopening Gate B.

## Amendments

| Date | Change |
|---|---|
| 2026-08-24 | Clarify: keep 12-type expansion + n ≥ 10,000 include bar; Census-only expansion (skip, no new TISCH2); no UMAP / no browser; neighbors stay in `EXPLORE.md` (no confirmatory supplement); Stromal/other composition table stays as display-only output |
| 2026-08-24 | Analyze nits: confirmatory named states = the three frozen buckets (not “five”); optional TCGA bulk plots → `EXPLORE.md`; Scribe ICI sentence is this file’s frozen negative |

## Clarify (closed 2026-08-24)

Accepted (conservative; fewer researcher degrees of freedom).

1. **Expansion list + 10k bar — kept.** Types: `PAAD`, `OV`, `PRAD`, `KIRC`, `LIHC`, `STAD`, `ESCA`, `HNSC`, `GBM`, `UCEC`, `THCA`, `CESC`. Include if Census has the type and n ≥ 10,000 after the Unit 01 filter; else skip with that reason. Do not shorten, add, or substitute types. Do not change the bar after seeing cell counts.
2. **Census-only expansion — kept.** If Census lacks a listed type, skip. Do not add a TISCH2 (or other) dataset for expansion.
3. **No UMAP / no browser — kept.** The map is tables and heatmaps of those tables. No embedding, even as display-only.
4. **Neighbors stay exploratory — kept.** `GPR18, GPR119, TRPV2, ABHD6, ABHD12` stay in `EXPLORE.md`. No labeled neighbor supplement in confirmatory outputs. They cannot enter the nine-gene score.
5. **Stromal sublabels display-only — kept, table in.** Among cells already in Stromal/other, tabulate existing labels (fibroblast / endothelial / pericyte-smooth-muscle / unmatched). That table is a confirmatory *output*. It is not a new confirmatory state and cannot rename **Stromal/other**.
