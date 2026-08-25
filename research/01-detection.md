# Unit 01 — Detection rates (Gate C)

**Run date:** 2026-08-24  
**Census version:** `2025-11-08`  
**Protocol SHA:** `3fbf310870c57247163edca35ed536ade3ea4301`  
**Rule:** % cells with raw count > 0. No ICI labels. No UMAP.

## Sources

- NSCLC, melanoma, CRC, BRCA: CELLxGENE Census, `is_primary_data == True`, raw RNA counts.
- BLCA: TISCH2 `BLCA_GSE130001` cell types + GEO `GSE130001` MTX counts (barcode-matched).
- Lineage buckets: locked substring map in `PROTOCOL.md` / `pipeline/lineage.py`.

Types available: **5** (BLCA, BRCA, CRC, NSCLC, melanoma). Minimum ≥2: **True**.

## Detection table

| Type | Source | Bucket | n | CNR2 % | MGLL % | FAAH % |
|---|---|---|---:|---:|---:|---:|
| CRC | Census | B/plasma | 40943 | 4.06 | 11.41 | 1.46 |
| CRC | Census | Myeloid | 50617 | 0.29 | 14.03 | 1.22 |
| CRC | Census | T/NK | 121657 | 0.48 | 18.00 | 7.73 |
| CRC | Census | Malignant/epithelial | 5105 | 0.65 | 35.24 | 7.64 |
| CRC | Census | Stromal/other | 147152 | 0.21 | 43.99 | 23.01 |
| BRCA | Census | B/plasma | 74842 | 5.89 | 6.07 | 1.07 |
| BRCA | Census | Myeloid | 163404 | 0.30 | 20.47 | 1.10 |
| BRCA | Census | T/NK | 1038935 | 0.37 | 12.81 | 7.23 |
| BRCA | Census | Malignant/epithelial | 105099 | 0.31 | 47.49 | 12.98 |
| BRCA | Census | Stromal/other | 252577 | 0.17 | 20.62 | 1.22 |
| NSCLC | Census | B/plasma | 123381 | 5.00 | 5.37 | 1.45 |
| NSCLC | Census | Myeloid | 311128 | 0.25 | 18.35 | 1.20 |
| NSCLC | Census | T/NK | 556875 | 0.30 | 5.42 | 1.48 |
| NSCLC | Census | Malignant/epithelial | 59167 | 0.11 | 34.04 | 8.17 |
| NSCLC | Census | Stromal/other | 110846 | 0.17 | 21.70 | 2.63 |
| melanoma | Census | B/plasma | 964 | 35.06 | 8.71 | 2.70 |
| melanoma | Census | Myeloid | 121 | 19.01 | 59.50 | 8.26 |
| melanoma | Census | T/NK | 22335 | 16.02 | 23.53 | 1.86 |
| melanoma | Census | Malignant/epithelial | 204 | 0.00 | 9.80 | 1.96 |
| melanoma | Census | Stromal/other | 295 | 5.42 | 44.75 | 4.07 |
| BLCA | TISCH2+GEO GSE130001 | B/plasma | 0 | — | — | — |
| BLCA | TISCH2+GEO GSE130001 | Myeloid | 0 | — | — | — |
| BLCA | TISCH2+GEO GSE130001 | T/NK | 0 | — | — | — |
| BLCA | TISCH2+GEO GSE130001 | Malignant/epithelial | 3772 | 0.16 | 1.80 | 19.51 |
| BLCA | TISCH2+GEO GSE130001 | Stromal/other | 357 | 0.28 | 23.25 | 1.40 |

## Gate C draft (human marks)

- **No raw-*CNR2*-UMAP atlas:** False  
  *(true iff CNR2 % < 1 in every non-B/plasma lineage with n>0 in every type)*
- MGLL < 5% in every non-B lineage in every type: **False**
- FAAH < 5% in every non-B lineage in every type: **False**
- Detection half of stop-kill (CNR2 dark **and** both enzymes dark): **False**

Gate C stop-kill also requires no non-B ECS state (Unit 02). If the detection half is false, stop-kill cannot fire.

## Human Gate C

- [ ] Pass / continue (do not stop the kill on detectability)
- [ ] No raw-*CNR2*-UMAP atlas (CNR2 < 1% rule)
- [ ] Fail (stop the kill) — only if detection half **and** Unit 02 finds no non-B ECS state

## What was not done

- No ICI phenotype or outcome files opened.
- No UMAP. No nine-gene ECS-state test (Unit 02).
- No TCGA or IMvigor210 scores.
