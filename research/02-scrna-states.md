# Unit 02 — scRNA ECS states (Gate A, discovery)

**Run date:** 2026-08-24  
**Census version:** `2025-11-08`  
**Protocol SHA:** `3fbf310870c57247163edca35ed536ade3ea4301`  
**Rule:** A lineage has an ECS state in a cancer type if ≥1 core gene is detected (count > 0) in ≥5% of that lineage’s cells **and** the lineage mean core-ECS score is highest or second-highest among buckets with cells in that type. Non-B lineages with contamination-gene detection ≥ 10% are discarded in that type. No ICI labels. No NMF / clustering / DE.

## Sources

- NSCLC, melanoma, CRC, BRCA: CELLxGENE Census, `is_primary_data == True`, raw RNA counts.
- BLCA: TISCH2 `BLCA_GSE130001` cell types + GEO `GSE130001` MTX counts (barcode-matched).
- Lineage buckets: locked substring map in `PROTOCOL.md` / `pipeline/lineage.py`.

Types available: **5** (BLCA, BRCA, CRC, NSCLC, melanoma). Minimum ≥2: **True**.

## Scoring

- Cell score = available-case mean of the nine core genes on **raw counts** (denominator = genes present in that matrix; min 7/9 or no score).
- Lineage mean = mean of cell scores in that bucket. Rank uses competition ranking (highest mean = 1; ties share the minimum rank). Empty buckets are not ranked.
- Z-score windows are for bulk (Units 04–07), not this unit.

## Genes present / dropped

- Census ECS dropped: **none**. Contamination gene: **MS4A1**.
- BLCA ECS dropped: **none**. Contamination gene: **MS4A1**.

Non-B lineages discarded for contamination (≥ 10%): **0**. Myeloid and T/NK meet the ≥5% detection bar in every type where they have cells, but their mean core-ECS is not highest or second-highest in any type.

## Lineage means, ranks, contamination

| Type | Source | Bucket | n | Mean ECS | Rank | ≥5% gene | Contam gene | Contam % | Rule | Discarded | Kept |
|---|---|---|---:|---:|---:|---|---|---:|---|---|---|
| CRC | Census | B/plasma | 40943 | 0.0344 | 5 | MGLL 11.41% | MS4A1 | — | False | no | False |
| CRC | Census | Myeloid | 50617 | 0.0504 | 4 | MGLL 14.03% | MS4A1 | 1.15 | False | no | False |
| CRC | Census | T/NK | 121657 | 0.1096 | 3 | MGLL 18.00% | MS4A1 | 1.36 | False | no | False |
| CRC | Census | Malignant/epithelial | 5105 | 0.1788 | 2 | MGLL 35.24% | MS4A1 | 3.55 | True | no | True |
| CRC | Census | Stromal/other | 147152 | 0.2754 | 1 | MGLL 43.99% | MS4A1 | 0.67 | True | no | True |
| BRCA | Census | B/plasma | 74842 | 0.0252 | 5 | MGLL 6.07% | MS4A1 | — | False | no | False |
| BRCA | Census | Myeloid | 163404 | 0.0632 | 3 | MGLL 20.47% | MS4A1 | 0.63 | False | no | False |
| BRCA | Census | T/NK | 1038935 | 0.0522 | 4 | MGLL 12.81% | MS4A1 | 1.21 | False | no | False |
| BRCA | Census | Malignant/epithelial | 105099 | 0.1726 | 1 | MGLL 47.49% | MS4A1 | 0.32 | True | no | True |
| BRCA | Census | Stromal/other | 252577 | 0.0739 | 2 | MGLL 20.62% | MS4A1 | 0.68 | True | no | True |
| NSCLC | Census | B/plasma | 123381 | 0.2239 | 5 | MGLL 5.37% | MS4A1 | — | False | no | False |
| NSCLC | Census | Myeloid | 311128 | 0.3763 | 4 | MGLL 18.35% | MS4A1 | 0.89 | False | no | False |
| NSCLC | Census | T/NK | 556875 | 0.5005 | 3 | MGLL 5.42% | MS4A1 | 1.96 | False | no | False |
| NSCLC | Census | Malignant/epithelial | 59167 | 1.1985 | 2 | MGLL 34.04% | MS4A1 | 0.57 | True | no | True |
| NSCLC | Census | Stromal/other | 110846 | 1.8128 | 1 | MGLL 21.70% | MS4A1 | 0.80 | True | no | True |
| melanoma | Census | B/plasma | 964 | 9.5105 | 2 | TRPV1 82.68% | MS4A1 | — | True | no | True |
| melanoma | Census | Myeloid | 121 | 9.2874 | 3 | MGLL 59.50% | MS4A1 | 0.83 | False | no | False |
| melanoma | Census | T/NK | 22335 | 0.9703 | 5 | MGLL 23.53% | MS4A1 | 1.36 | False | no | False |
| melanoma | Census | Malignant/epithelial | 204 | 5.6836 | 4 | TRPV1 74.51% | MS4A1 | 0.98 | False | no | False |
| melanoma | Census | Stromal/other | 295 | 9.8983 | 1 | TRPV1 73.22% | MS4A1 | 2.37 | True | no | True |
| BLCA | TISCH2+GEO GSE130001 | B/plasma | 0 | — | — | — | MS4A1 | — | False | no | False |
| BLCA | TISCH2+GEO GSE130001 | Myeloid | 0 | — | — | — | MS4A1 | — | False | no | False |
| BLCA | TISCH2+GEO GSE130001 | T/NK | 0 | — | — | — | MS4A1 | — | False | no | False |
| BLCA | TISCH2+GEO GSE130001 | Malignant/epithelial | 3772 | 0.0395 | 2 | FAAH 19.51% | MS4A1 | 0.03 | True | no | True |
| BLCA | TISCH2+GEO GSE130001 | Stromal/other | 357 | 0.0591 | 1 | MGLL 23.25% | MS4A1 | 0.00 | True | no | True |

## Per-gene detection (% cells with count > 0)

| Type | Bucket | n | CNR1 % | CNR2 % | GPR55 % | TRPV1 % | FAAH % | MGLL % | DAGLA % | DAGLB % | NAPEPLD % |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CRC | B/plasma | 40943 | 1.28 | 4.06 | 0.94 | 0.99 | 1.46 | 11.41 | 0.13 | 2.10 | 3.60 |
| CRC | Myeloid | 50617 | 0.10 | 0.29 | 0.50 | 0.74 | 1.22 | 14.03 | 1.53 | 8.69 | 2.80 |
| CRC | T/NK | 121657 | 0.12 | 0.48 | 1.10 | 1.36 | 7.73 | 18.00 | 2.73 | 4.82 | 10.20 |
| CRC | Malignant/epithelial | 5105 | 0.29 | 0.65 | 0.39 | 1.37 | 7.64 | 35.24 | 1.57 | 4.62 | 9.95 |
| CRC | Stromal/other | 147152 | 0.29 | 0.21 | 0.67 | 2.67 | 23.01 | 43.99 | 6.49 | 10.81 | 21.94 |
| BRCA | B/plasma | 74842 | 1.56 | 5.89 | 0.41 | 0.67 | 1.07 | 6.07 | 0.12 | 1.81 | 1.72 |
| BRCA | Myeloid | 163404 | 0.06 | 0.30 | 0.29 | 0.74 | 1.10 | 20.47 | 1.46 | 9.66 | 2.25 |
| BRCA | T/NK | 1038935 | 0.46 | 0.37 | 0.25 | 2.16 | 7.23 | 12.81 | 1.24 | 5.07 | 7.84 |
| BRCA | Malignant/epithelial | 105099 | 0.07 | 0.31 | 0.18 | 11.53 | 12.98 | 47.49 | 1.06 | 7.02 | 35.61 |
| BRCA | Stromal/other | 252577 | 1.28 | 0.17 | 0.07 | 1.22 | 1.22 | 20.62 | 1.24 | 5.18 | 5.39 |
| NSCLC | B/plasma | 123381 | 1.49 | 5.00 | 0.53 | 0.76 | 1.45 | 5.37 | 0.14 | 2.14 | 2.41 |
| NSCLC | Myeloid | 311128 | 0.06 | 0.25 | 0.21 | 0.76 | 1.20 | 18.35 | 2.01 | 7.20 | 1.76 |
| NSCLC | T/NK | 556875 | 0.13 | 0.30 | 0.37 | 0.60 | 1.48 | 5.42 | 0.30 | 2.56 | 2.42 |
| NSCLC | Malignant/epithelial | 59167 | 1.28 | 0.11 | 0.02 | 1.60 | 8.17 | 34.04 | 1.51 | 6.22 | 5.20 |
| NSCLC | Stromal/other | 110846 | 1.16 | 0.17 | 0.05 | 0.79 | 2.63 | 21.70 | 0.56 | 3.80 | 3.02 |
| melanoma | B/plasma | 964 | 8.30 | 35.06 | 1.76 | 82.68 | 2.70 | 8.71 | 1.04 | 13.49 | 28.84 |
| melanoma | Myeloid | 121 | 0.00 | 19.01 | 0.00 | 19.83 | 8.26 | 59.50 | 12.40 | 37.19 | 0.83 |
| melanoma | T/NK | 22335 | 1.76 | 16.02 | 0.72 | 22.31 | 1.86 | 23.53 | 8.03 | 22.20 | 4.33 |
| melanoma | Malignant/epithelial | 204 | 3.43 | 0.00 | 3.92 | 74.51 | 1.96 | 9.80 | 2.45 | 5.88 | 29.90 |
| melanoma | Stromal/other | 295 | 1.02 | 5.42 | 2.03 | 73.22 | 4.07 | 44.75 | 5.76 | 29.49 | 30.85 |
| BLCA | B/plasma | 0 | — | — | — | — | — | — | — | — | — |
| BLCA | Myeloid | 0 | — | — | — | — | — | — | — | — | — |
| BLCA | T/NK | 0 | — | — | — | — | — | — | — | — | — |
| BLCA | Malignant/epithelial | 3772 | 0.24 | 0.16 | 0.03 | 0.00 | 19.51 | 1.80 | 0.08 | 4.64 | 4.90 |
| BLCA | Stromal/other | 357 | 0.84 | 0.28 | 0.00 | 0.00 | 1.40 | 23.25 | 1.40 | 7.00 | 3.92 |

## Candidates (ECS state after contamination filter)

| Bucket | Cancer types where kept |
|---|---|
| B/plasma | melanoma |
| Malignant/epithelial | BLCA, BRCA, CRC, NSCLC |
| Stromal/other | BLCA, BRCA, CRC, NSCLC, melanoma |

## Gate A draft from this unit (not the full gate)

- Lineage buckets with an ECS state: **3** (B/plasma, Malignant/epithelial, Stromal/other)
- Of those, non-B: **2**
- Two-lineage rule (≥2 buckets including B/plasma): **True**
- At least one non-B candidate listed: **True**
- Gate A already fails (fewer than two buckets): **False**

Unit 02 lists candidates only. Gate A still requires TCGA confound tests (Unit 04) and naming (Unit 05). Gate A already fails if fewer than two buckets remain.

Human does not name the primary state here (Unit 05, after Unit 04 confound tests).

## What was not done

- No ICI phenotype or outcome files opened.
- No NMF, new clustering, or DE.
- No TCGA correlation (Unit 04). No frozen marker commit (Unit 03).
- No UMAP.
