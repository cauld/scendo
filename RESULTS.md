# RESULTS

Confirmatory extract for the Scribe. Numbers below appear in `STATUS.md` as confirmatory, or are copied from sealed-protocol unit notes. Do not add exploratory items from `EXPLORE.md`. Manuscript: [`docs/manuscript.md`](docs/manuscript.md).

**Bound.** `CLAIMS.md` non-claims plus `PROTOCOL-ATLAS.md` frozen ICI negative. Kill SHA `3fbf310`. Atlas SHA `2a74270`. OSF: [osf.io/c8kpx](https://osf.io/c8kpx). Decide (2026-08-25): atlas paper as written (core + expansion; ICI negative chapter).

**May claim**

1. Human tumor ECS is visible as **lineage cell states** on the nine-gene list (`CNR1, CNR2, GPR55, TRPV1, FAAH, MGLL, DAGLA, DAGLB, NAPEPLD`).
2. At least one non-B state (**Stromal/other**) is distinguishable from B-cell / TLS abundance (Gate A).
3. The frozen Stromal/other score **does not** associate with IMvigor210 **response** after B + TLS + CD8 (Model 1 ECS OR 1.189, 95% CI 0.551–2.563). OS, unadjusted, Model 2, deconvolution, and melanoma GEO do not carry this claim.

**Must not claim:** cannabis/CBD therapy; CB2 **is** a checkpoint; patients should change cannabis during PD-1; GEO validates a biomarker; OS / unadjusted / deconvolution is a checkpoint association; myeloid / T/NK catalog rows are confirmatory named states; stromal subtypes are a new state.

## Gates

| Gate | Result | Source |
|---|---|---|
| C detectability | Pass / continue | `research/01-detection.md` |
| A states ≠ B cells | Pass. Primary **Stromal/other** | `research/04-tcga-confound.md`, `research/05-primary-state.md` |
| B ICI ≠ confound | Fail. Model 1 CI includes 1 | `research/06-imvigor210.md` |
| D core map | Pass. Same three buckets; 0 flips | `research/10-reproduce-core.md` |
| E expansion | Pass. 6 tabled, 6 skipped | `research/11-expansion-inventory.md`, `research/12-expansion-states.md` |
| F ICI frozen | Pass. Numbers = Units 06–07 | `research/14-atlas-converge.md` |

## Named states (core five types)

Nine core genes unchanged. Neighbors (`GPR18, GPR119, TRPV2, ABHD6, ABHD12`) not in the score. Census pin `2025-11-08`. BLCA: TISCH2 `BLCA_GSE130001` + GEO `GSE130001`. Contamination gene **MS4A1**; 0 non-B discards.

A lineage has an ECS state if ≥1 core gene is detected in ≥5% of that lineage’s cells **and** lineage mean core-ECS is highest or second-highest in that type, after contamination.

| Named state | Core types where kept | Role |
|---|---|---|
| B/plasma | melanoma | confirmatory named state |
| Malignant/epithelial | BLCA, BRCA, CRC, NSCLC | confirmatory named state |
| Stromal/other | BLCA, BRCA, CRC, NSCLC, melanoma | confirmatory named state; **primary** |

Myeloid and T/NK are scored in every table. They are not confirmatory named states on the core five.

Gate D: 0 kept↔dropped flips vs Unit 02; 0 numeric drift at published precision.

## Confound (Gate A)

Same nine-gene bulk score for every non-B candidate. Pearson on TOIL `tcga_RSEM_gene_tpm`. Residual escape not used.

| Cohort | n | r_B | r_TLS | \|r\| < 0.6 |
|---|---:|---:|---:|---|
| Pooled TCGA | 3664 | 0.417 | 0.383 | True |
| TCGA-BLCA | 426 | 0.361 | 0.263 | True |

Primary named **Stromal/other** by cascade step 2 (present in 5 of 5 core types vs 4 for Malignant/epithelial), **before** ICI outcome files were opened.

## Expansion (Gate E)

Locked list of 12. Census only. Include if n ≥ 10,000 after the Unit 01 filter; else skip. No substitute types. No TISCH2.

| Type | Decision | n cells | Reason |
|---|---|---:|---|
| OV | tabled | 984,988 | n ≥ 10,000 |
| PRAD | tabled | 68,322 | n ≥ 10,000 |
| KIRC | tabled | 187,792 | n ≥ 10,000 |
| STAD | tabled | 217,923 | n ≥ 10,000 |
| HNSC | tabled | 82,378 | n ≥ 10,000 |
| GBM | tabled | 1,363,983 | n ≥ 10,000 |
| PAAD | skip | 0 | missing in Census |
| LIHC | skip | 0 | n < 10,000 |
| ESCA | skip | 0 | missing in Census |
| UCEC | skip | 0 | missing in Census |
| THCA | skip | 0 | missing in Census |
| CESC | skip | 0 | missing in Census |

Expansion catalog calls (kill ECS-state rule; **not** new named states): Malignant/epithelial in HNSC, OV, PRAD, STAD; Stromal/other in GBM, HNSC, KIRC, PRAD, STAD; Myeloid in OV (catalog only); T/NK in GBM, KIRC (catalog only). Primary remains **Stromal/other**.

## Stromal/other composition (display only)

Existing Census `cell_type` / TISCH2 labels among cells already in Stromal/other. Not a new confirmatory state. Stromal n matches Units 10/12 on all 11 included types.

| Type | n stromal | Fibroblast % | Endothelial % | Pericyte/SM % | Unmatched % |
|---|---:|---:|---:|---:|---:|
| NSCLC | 110,846 | 17.04 | 34.54 | 5.15 | 43.28 |
| melanoma | 295 | 40.68 | 31.19 | 0.00 | 28.14 |
| CRC | 147,152 | 5.62 | 5.52 | 1.62 | 87.24 |
| BRCA | 252,577 | 46.17 | 31.90 | 8.17 | 13.76 |
| BLCA | 357 | 59.94 | 40.06 | 0.00 | 0.00 |
| OV | 205,482 | 85.83 | 9.96 | 0.00 | 4.21 |
| PRAD | 42,415 | 6.02 | 33.42 | 15.82 | 44.74 |
| KIRC | 61,569 | 0.00 | 15.53 | 4.40 | 80.07 |
| STAD | 141,769 | 0.97 | 1.52 | 1.68 | 95.83 |
| HNSC | 16,499 | 19.76 | 11.25 | 0.00 | 68.99 |
| GBM | 450,998 | 0.12 | 3.62 | 1.11 | 95.15 |

Figures (heatmaps of confirmatory tables): `docs/diagrams/13-mean-ecs.png`, `docs/diagrams/13-detection-stromal.png`, `docs/diagrams/13-stromal-composition.png`. No UMAP.

## Frozen ICI chapter (Gate B fail; Gate F pass)

Primary estimator: continuous **raw** nine-gene score. No cutoff search. States frozen before ICI phenotypes were opened.

### IMvigor210 Model 1 (confirmatory)

`response ~ ECS + B_cell + TLS + CD8`. CR/PR vs SD/PD. n = **298** (68 CR/PR, 230 SD/PD). 9/9 ECS genes present. VIF(ECS) = **1.360**.

| Term | OR | 95% CI | CI excludes 1 |
|---|---:|---|---|
| ECS | 1.189 | 0.551–2.563 | **False** |
| B cell | 0.961 | 0.495–1.863 | False |
| TLS | 0.517 | 0.258–1.035 | False |
| CD8 | 2.380 | 1.508–3.757 | True |

Gate B **fail**: ECS CI includes 1. CD8 is a sanity check that the model can see cytotoxicity; it does not pass Gate B for ECS.

### Secondary (cannot carry the claim)

| Analysis | n | ECS | Note |
|---|---:|---|---|
| Unadjusted logistic | 298 | OR 1.076 (0.568–2.038) | Neither necessary nor sufficient |
| Model 2 (+ TMB, PD-L1 IC, sex) | 234 | OR 1.093 (0.449–2.663) | Robustness, not a pass |
| Cox OS | 348 | HR 0.898 (0.623–1.294) | Secondary; not a pass |
| GSE78220 Model 1 | 26 | OR 0.469 (0.019–11.697) | Replication; cannot rescue |
| GSE91061 Model 1 | 49 | OR 0.603 (0.066–5.510) | Replication; cannot rescue |

Deconvolution was not run.

## Out of this paper

Public browser. scGPT. GSE220635. Neighbor genes in the confirmatory score. New clustering / NMF. New ICI cohorts. Renaming **Stromal/other**. Reopening Gate B.
