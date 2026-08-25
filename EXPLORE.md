# EXPLORE

Ledger of work that is **not** confirmatory. The Scribe does not put these in the main claims.

**Archive (2026-08-25).** Kill Decide: atlas-only. Atlas Decide: paper as written. Scribe is done (`RESULTS.md`, `docs/manuscript.md`). Items below stay out of the manuscript claims. They need a **new protocol + new lock** (or a dated amendment) before they can become confirmatory.

Paper: named-state map + frozen ICI **negative**. Do not reopen Gate B from this list.

## Closed on this Decide

| Item | Status | Notes |
|---|---|---|
| Full-paper Gate B pass | **Closed** | A pass, B fail. No path in `KILL-ATLAS.md` to a Gate B pass |
| Reopening ICI (new model, cutoff, gene, cohort) | **Closed** | Gate F pass = Units 06–07 only |
| Narrower atlas (core five only) | **Closed** | Gate E passed; skips were locked, not a fail |
| Promoting myeloid / T/NK catalog rows | **Closed** | OV myeloid; GBM / KIRC T/NK. Catalog only |
| Clustering stromal unmatched into a new state | **Closed** | Unit 13 is display-only. Unmatched-heavy STAD / GBM / CRC / KIRC stay labels, not a fourth named state |
| Filling expansion skips with TISCH2 | **Closed** | PAAD, ESCA, UCEC, THCA, CESC missing; LIHC n < 10,000. Census-only |

## Out of this paper (not named in the atlas lock)

| Item | Status | Notes |
|---|---|---|
| Public ECS browser | Archived | Not in `PROTOCOL-ATLAS.md` |
| scGPT / large-model training | Archived | Not in `PROTOCOL-ATLAS.md` |
| GSE220635 CBD×PD-1 reanalysis | Archived | Full-paper positive control; do not reopen Gate B |
| UMAP / Harmony / scVI / raw-*CNR2* embedding | Archived | Map is tables and heatmaps of those tables |
| Tabula Sapiens / normal-tissue Census | Archived | Healthy tissue out |
| Heme / lymphoid malignancies | Archived | Out of expansion list |
| EGA/dbGaP extra ICI cohorts | Archived | Optional; not required; would be a new ICI cohort |

## Exploratory methods (parked)

| Item | Status | Notes |
|---|---|---|
| ECS neighbor genes (`GPR18, GPR119, TRPV2, ABHD6, ABHD12`) | Exploratory | Out of the nine-gene score; no labeled neighbor supplement |
| NMF ECS programs | Exploratory | Lineage means only in this lock |
| CIBERSORTx / BayesPrism ECS-in-fraction | Exploratory | Cannot flip Gate B |
| TCGA project-level ECS detection / mean z-score plots | Exploratory | Same TOIL matrix as Unit 04; cannot change Unit 05 or confirmatory tables |
| Spearman on TCGA confound | Exploratory | Pearson is the Gate A metric |
| Median / Youden / ROC / AUC cutoffs on ICI | Exploratory | Primary estimator is continuous raw score |

## Census near-misses (not substituted)

Inspected in Unit 11 and **not** added. Would be a substitute type or a broader parent. Detail: `research/11-expansion-inventory.md`.

- `malignant pancreatic neoplasm` (not adenocarcinoma-specific)
- `renal cell carcinoma`, `nonpapillary renal cell carcinoma`, `chromophobe renal cell carcinoma` (not specifically KIRC)
- `liver cancer` (not specifically LIHC)
- `intrahepatic cholangiocarcinoma` (not in the locked list)

## Operational choices (not amendments)

Recorded in unit notes. They do not change confirmatory fields.

- IMvigor210: DESeq size-factor normalized counts, then `log2(norm + 1)`, then within-cohort z-scores. Protocol allows the shipped matrix or `log2(TPM+1)`.
- TCGA pooled window kept all `_primary_disease`-matched sample types, including Solid Tissue Normal.
- Both non-B buckets share the same nine-gene bulk score, so cascade step 1 is a tie by construction; step 2 named **Stromal/other**.
- BLCA used the pinned TISCH2+GEO fallback because Census lacked BLCA (kill rule, not expansion shopping).
- Atlas-phase ICI work was citation; matrices were not re-opened.

## Follow-up studies (not this repo’s confirmatory loop)

| Item | Status | Notes |
|---|---|---|
| DDI / FAERS / CYP oncology atlas | Deferred | Separate study |
| Wet-lab CB2 | Deferred | Not this computational paper |
| Prospective cannabis + ICI cohort | Deferred | Not a practice guideline from this map |
| Copy `.seal/` into the next study | Optional | Constitution: extract after one completed Decide |

## Still open (not a leftover idea)

OSF secondary-data prereg URL is **not yet** posted. That is the public lock for kill SHA `3fbf310`. It may follow the git SHA by a day. It is not an exploratory analysis.
