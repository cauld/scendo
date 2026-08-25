# Unit 13 — Stromal composition and figure pack

**Run date:** 2026-08-25  
**Census version:** `2025-11-08`  
**Kill protocol SHA:** `3fbf310870c57247163edca35ed536ade3ea4301`  
**Atlas protocol SHA:** `2a74270a16685cbc4df5c45c293a7afb5b7665f5`  
**Rule:** Display-only. Among cells already in **Stromal/other**, tabulate existing Census `cell_type` / TISCH2 labels as fibroblast, endothelial, pericyte/smooth muscle, or unmatched. Do not cluster. Do not declare a new confirmatory state. Heatmaps are of Units 10 and 12 confirmatory tables. No UMAP. No ICI plots. Primary remains **Stromal/other**.

## Sources

- Core Census types (NSCLC, melanoma, CRC, BRCA): same disease strings and Unit 01 filter as Units 01–02 / 10. Obs-only (no expression re-read).
- BLCA: TISCH2 `BLCA_GSE130001` `Celltype (major-lineage)` (already pinned).
- Expansion included types: Unit 11 disease strings, same filter as Unit 12.
- Heatmap values: `pipeline/output/10/states.csv` and `pipeline/output/12/states.csv`.

Types in composition tables: **11** (NSCLC, melanoma, CRC, BRCA, BLCA, OV, PRAD, KIRC, STAD, HNSC, GBM). Expansion skips (not tabled here): `PAAD` (missing in Census); `LIHC` (n < 10,000); `ESCA` (missing in Census); `UCEC` (missing in Census); `THCA` (missing in Census); `CESC` (missing in Census).

## Display-only (not a new state)

Primary confirmatory name stays **Stromal/other**. Fibroblast / endothelial / pericyte-smooth-muscle / unmatched are **sublabels of that bucket**. They cannot rename it and are not Gate A / Gate B / Gate D tests.

## Stromal n vs Units 10 / 12

Mismatches: **0**.

| Type | Unit 13 stromal n | Unit 10/12 stromal n | Match |
|---|---:|---:|---|
| NSCLC | 110,846 | 110,846 | True |
| melanoma | 295 | 295 | True |
| CRC | 147,152 | 147,152 | True |
| BRCA | 252,577 | 252,577 | True |
| BLCA | 357 | 357 | True |
| OV | 205,482 | 205,482 | True |
| PRAD | 42,415 | 42,415 | True |
| KIRC | 61,569 | 61,569 | True |
| STAD | 141,769 | 141,769 | True |
| HNSC | 16,499 | 16,499 | True |
| GBM | 450,998 | 450,998 | True |

## Stromal/other composition

Denominator = cells already assigned to Stromal/other. Percent is of that denominator. `myofibroblast` is counted as fibroblast (substring).

| Type | Source | n stromal | Fibroblast n (%) | Endothelial n (%) | Pericyte/SM n (%) | Unmatched n (%) |
|---|---|---:|---:|---:|---:|---:|
| NSCLC | Census | 110,846 | 18,887 (17.04) | 38,282 (34.54) | 5,706 (5.15) | 47,971 (43.28) |
| melanoma | Census | 295 | 120 (40.68) | 92 (31.19) | 0 (0.00) | 83 (28.14) |
| CRC | Census | 147,152 | 8,274 (5.62) | 8,120 (5.52) | 2,387 (1.62) | 128,371 (87.24) |
| BRCA | Census | 252,577 | 116,603 (46.17) | 80,571 (31.90) | 20,645 (8.17) | 34,758 (13.76) |
| BLCA | TISCH2+GEO GSE130001 | 357 | 214 (59.94) | 143 (40.06) | 0 (0.00) | 0 (0.00) |
| OV | Census | 205,482 | 176,361 (85.83) | 20,468 (9.96) | 0 (0.00) | 8,653 (4.21) |
| PRAD | Census | 42,415 | 2,552 (6.02) | 14,177 (33.42) | 6,709 (15.82) | 18,977 (44.74) |
| KIRC | Census | 61,569 | 0 (0.00) | 9,561 (15.53) | 2,708 (4.40) | 49,300 (80.07) |
| STAD | Census | 141,769 | 1,375 (0.97) | 2,157 (1.52) | 2,379 (1.68) | 135,858 (95.83) |
| HNSC | Census | 16,499 | 3,261 (19.76) | 1,856 (11.25) | 0 (0.00) | 11,382 (68.99) |
| GBM | Census | 450,998 | 560 (0.12) | 16,317 (3.62) | 4,999 (1.11) | 429,122 (95.15) |

### Per type

#### NSCLC

n Stromal/other = **110,846**. Sublabels are display-only.

| Subtype | n | % of stromal |
|---|---:|---:|
| fibroblast | 18,887 | 17.04 |
| endothelial | 38,282 | 34.54 |
| pericyte/smooth muscle | 5,706 | 5.15 |
| unmatched | 47,971 | 43.28 |

#### melanoma

n Stromal/other = **295**. Sublabels are display-only.

| Subtype | n | % of stromal |
|---|---:|---:|
| fibroblast | 120 | 40.68 |
| endothelial | 92 | 31.19 |
| pericyte/smooth muscle | 0 | 0.00 |
| unmatched | 83 | 28.14 |

#### CRC

n Stromal/other = **147,152**. Sublabels are display-only.

| Subtype | n | % of stromal |
|---|---:|---:|
| fibroblast | 8,274 | 5.62 |
| endothelial | 8,120 | 5.52 |
| pericyte/smooth muscle | 2,387 | 1.62 |
| unmatched | 128,371 | 87.24 |

#### BRCA

n Stromal/other = **252,577**. Sublabels are display-only.

| Subtype | n | % of stromal |
|---|---:|---:|
| fibroblast | 116,603 | 46.17 |
| endothelial | 80,571 | 31.90 |
| pericyte/smooth muscle | 20,645 | 8.17 |
| unmatched | 34,758 | 13.76 |

#### BLCA

n Stromal/other = **357**. Sublabels are display-only.

| Subtype | n | % of stromal |
|---|---:|---:|
| fibroblast | 214 | 59.94 |
| endothelial | 143 | 40.06 |
| pericyte/smooth muscle | 0 | 0.00 |
| unmatched | 0 | 0.00 |

#### OV

n Stromal/other = **205,482**. Sublabels are display-only.

| Subtype | n | % of stromal |
|---|---:|---:|
| fibroblast | 176,361 | 85.83 |
| endothelial | 20,468 | 9.96 |
| pericyte/smooth muscle | 0 | 0.00 |
| unmatched | 8,653 | 4.21 |

#### PRAD

n Stromal/other = **42,415**. Sublabels are display-only.

| Subtype | n | % of stromal |
|---|---:|---:|
| fibroblast | 2,552 | 6.02 |
| endothelial | 14,177 | 33.42 |
| pericyte/smooth muscle | 6,709 | 15.82 |
| unmatched | 18,977 | 44.74 |

#### KIRC

n Stromal/other = **61,569**. Sublabels are display-only.

| Subtype | n | % of stromal |
|---|---:|---:|
| fibroblast | 0 | 0.00 |
| endothelial | 9,561 | 15.53 |
| pericyte/smooth muscle | 2,708 | 4.40 |
| unmatched | 49,300 | 80.07 |

#### STAD

n Stromal/other = **141,769**. Sublabels are display-only.

| Subtype | n | % of stromal |
|---|---:|---:|
| fibroblast | 1,375 | 0.97 |
| endothelial | 2,157 | 1.52 |
| pericyte/smooth muscle | 2,379 | 1.68 |
| unmatched | 135,858 | 95.83 |

#### HNSC

n Stromal/other = **16,499**. Sublabels are display-only.

| Subtype | n | % of stromal |
|---|---:|---:|
| fibroblast | 3,261 | 19.76 |
| endothelial | 1,856 | 11.25 |
| pericyte/smooth muscle | 0 | 0.00 |
| unmatched | 11,382 | 68.99 |

#### GBM

n Stromal/other = **450,998**. Sublabels are display-only.

| Subtype | n | % of stromal |
|---|---:|---:|
| fibroblast | 560 | 0.12 |
| endothelial | 16,317 | 3.62 |
| pericyte/smooth muscle | 4,999 | 1.11 |
| unmatched | 429,122 | 95.15 |

## Unmatched labels (existing names only)

Labels already in Stromal/other that did not match fibroblast / endothelial / pericyte / smooth muscle. Listed so unmatched is not silent. Not a new confirmatory state. Rows with ≥ 1% of stromal, else top 5 per type.

| Type | Existing label | n | % of stromal |
|---|---|---:|---:|
| NSCLC | unknown | 21,250 | 19.17 |
| NSCLC | pulmonary alveolar type 2 cell | 17,379 | 15.68 |
| NSCLC | pulmonary alveolar type 1 cell | 4,094 | 3.69 |
| NSCLC | natural T-regulatory cell | 3,531 | 3.19 |
| melanoma | mononuclear phagocyte | 46 | 15.59 |
| melanoma | microglial cell | 37 | 12.54 |
| CRC | stem cell | 97,900 | 66.53 |
| CRC | colonocyte | 10,922 | 7.42 |
| CRC | mononuclear phagocyte | 6,081 | 4.13 |
| CRC | T-helper 17 cell | 3,182 | 2.16 |
| CRC | transit amplifying cell | 2,395 | 1.63 |
| CRC | gut absorptive cell | 1,575 | 1.07 |
| BRCA | T follicular helper cell | 10,490 | 4.15 |
| BRCA | mesothelial cell | 6,431 | 2.55 |
| BRCA | mononuclear phagocyte | 4,951 | 1.96 |
| BRCA | hepatic stellate cell | 2,899 | 1.15 |
| OV | mononuclear phagocyte | 8,646 | 4.21 |
| PRAD | basal cell of prostate epithelium | 8,220 | 19.38 |
| PRAD | club-like cell of the urethral epithelium | 4,966 | 11.71 |
| PRAD | luminal cell of prostate epithelium | 4,582 | 10.80 |
| PRAD | glial cell | 1,064 | 2.51 |
| KIRC | abnormal cell | 38,198 | 62.04 |
| KIRC | unknown | 10,985 | 17.84 |
| STAD | unknown | 118,175 | 83.36 |
| STAD | mucous neck cell of gastric gland | 6,136 | 4.33 |
| STAD | foveolar cell of stomach | 5,121 | 3.61 |
| STAD | T-helper 17 cell | 2,141 | 1.51 |
| STAD | T follicular helper cell | 1,713 | 1.21 |
| HNSC | oral mucosa squamous cell | 7,386 | 44.77 |
| HNSC | oligodendrocyte | 1,382 | 8.38 |
| HNSC | mural cell | 1,010 | 6.12 |
| HNSC | cerebral cortex neuron | 521 | 3.16 |
| HNSC | L4 intratelencephalic projecting glutamatergic neuron | 209 | 1.27 |
| HNSC | L2/3 intratelencephalic projecting glutamatergic neuron | 204 | 1.24 |
| HNSC | astrocyte | 204 | 1.24 |
| GBM | microglial cell | 245,015 | 54.33 |
| GBM | oligodendrocyte | 70,092 | 15.54 |
| GBM | neoplastic cell | 59,418 | 13.17 |
| GBM | oligodendrocyte precursor cell | 24,327 | 5.39 |
| GBM | astrocyte | 12,746 | 2.83 |
| GBM | mural cell | 5,909 | 1.31 |

## Figures

Heatmaps of confirmatory tables (Units 10 and 12) plus the composition table. Grey = empty bucket (n = 0). Mean ECS color is log-scaled so melanoma does not wash out other types; printed numbers are raw means.

![Mean core-ECS by type and lineage bucket](../docs/diagrams/13-mean-ecs.png)

![Nine-gene detection in Stromal/other](../docs/diagrams/13-detection-stromal.png)

![Stromal/other subtype composition](../docs/diagrams/13-stromal-composition.png)

## What was not done

- No clustering, NMF, or DE. No new confirmatory state from a subtype.
- No UMAP, Harmony/scVI, or browser.
- No ICI phenotype or outcome files opened. No ICI plots.
- Primary **Stromal/other** not renamed. No gene added.
- Myeloid / T/NK catalog rows from Unit 12 not promoted.
