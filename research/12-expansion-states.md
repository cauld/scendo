# Unit 12 — Expansion ECS-state tables (Gate E)

**Run date:** 2026-08-24  
**Census version:** `2025-11-08`  
**Kill protocol SHA:** `3fbf310870c57247163edca35ed536ade3ea4301`  
**Atlas protocol SHA:** `2a74270a16685cbc4df5c45c293a7afb5b7665f5`  
**Rule:** Same detection / mean / contamination / ECS-state table as Unit 10, for every **included** expansion type. A lineage has an ECS-state catalog call in a cancer type if ≥1 core gene is detected (count > 0) in ≥5% of that lineage’s cells **and** the lineage mean core-ECS score is highest or second-highest among buckets with cells in that type. Non-B lineages with contamination-gene detection ≥ 10% are discarded in that type. Confirmatory **named** states stay B/plasma, Malignant/epithelial, Stromal/other. Expansion calls are catalog rows. No ICI labels. No TISCH2. No NMF / clustering / DE. Primary name is not re-opened.

## Sources

- CELLxGENE Census pin `2025-11-08`, `is_primary_data == True`, raw RNA counts. One query per included type (Unit 11 disease strings).
- Cell filter: same as Unit 01 (`census_obs_filter` + culture/organoid/cell-line drop).
- Lineage buckets: locked substring map in kill `PROTOCOL.md` / `pipeline/lineage.py`.
- Include / skip list: `research/11-expansion-inventory.json`.

Included types tabled: **6** (OV, PRAD, KIRC, STAD, HNSC, GBM). Skipped (one-line reason): **6** (PAAD (missing in Census); LIHC (n < 10,000); ESCA (missing in Census); UCEC (missing in Census); THCA (missing in Census); CESC (missing in Census)).

## Frozen objects (unchanged)

- Nine core genes: `CNR1, CNR2, GPR55, TRPV1, FAAH, MGLL, DAGLA, DAGLB, NAPEPLD`. **Unchanged:** True.
- Named states: B/plasma, Malignant/epithelial, Stromal/other.
- Primary display name: **Stromal/other**. **Unchanged:** True.

## Scoring

- Cell score = available-case mean of the nine core genes on **raw counts** (denominator = genes present in that matrix; min 7/9 or no score).
- Lineage mean = mean of cell scores in that bucket. Rank uses competition ranking (highest mean = 1; ties share the minimum rank). Empty buckets are not ranked.
- All five lineage buckets are scored. Myeloid / T/NK catalog calls are not confirmatory named states.

## Include / skip (from Unit 11)

| Type | Protocol name | Decision | Reason | Unit 11 n | Unit 12 n |
|---|---|---|---|---:|---:|
| PAAD | pancreatic adenocarcinoma | **skip** | missing in Census | 0 | 0 |
| OV | ovarian | **include** | n ≥ 10,000 | 984,988 | 984,988 |
| PRAD | prostate | **include** | n ≥ 10,000 | 68,322 | 68,322 |
| KIRC | clear cell kidney | **include** | n ≥ 10,000 | 187,792 | 187,792 |
| LIHC | hepatocellular | **skip** | n < 10,000 | 0 | 0 |
| STAD | stomach | **include** | n ≥ 10,000 | 217,923 | 217,923 |
| ESCA | esophageal | **skip** | missing in Census | 0 | 0 |
| HNSC | head and neck squamous | **include** | n ≥ 10,000 | 82,378 | 82,378 |
| GBM | glioblastoma | **include** | n ≥ 10,000 | 1,363,983 | 1,363,983 |
| UCEC | endometrial | **skip** | missing in Census | 0 | 0 |
| THCA | thyroid | **skip** | missing in Census | 0 | 0 |
| CESC | cervical | **skip** | missing in Census | 0 | 0 |

Skipped types (one-line reason):

- `PAAD`: missing in Census
- `LIHC`: n < 10,000
- `ESCA`: missing in Census
- `UCEC`: missing in Census
- `THCA`: missing in Census
- `CESC`: missing in Census

## Genes present / dropped

- Census ECS dropped: **none**. Contamination gene(s): **MS4A1**.

Non-B lineages discarded for contamination (≥ 10%): **0**.

## Lineage means, ranks, contamination

| Type | Source | Bucket | n | Mean ECS | Rank | ≥5% gene | Contam gene | Contam % | Rule | Discarded | Kept |
|---|---|---|---:|---:|---:|---|---|---:|---|---|---|
| OV | Census | B/plasma | 42127 | 0.0468 | 3 | MGLL 14.39% | MS4A1 | — | False | no | False |
| OV | Census | Myeloid | 207417 | 0.0974 | 2 | MGLL 24.53% | MS4A1 | 0.48 | True | no | True |
| OV | Census | T/NK | 274230 | 0.0131 | 5 | NAPEPLD 4.60% | MS4A1 | 2.44 | False | no | False |
| OV | Census | Malignant/epithelial | 255732 | 0.1045 | 1 | NAPEPLD 21.82% | MS4A1 | 0.06 | True | no | True |
| OV | Census | Stromal/other | 205482 | 0.0435 | 4 | MGLL 11.03% | MS4A1 | 0.21 | False | no | False |
| PRAD | Census | B/plasma | 828 | 0.0353 | 4 | CNR2 8.21% | MS4A1 | — | False | no | False |
| PRAD | Census | Myeloid | 2794 | 0.0460 | 3 | DAGLB 16.00% | MS4A1 | 0.50 | False | no | False |
| PRAD | Census | T/NK | 19075 | 0.0098 | 5 | DAGLB 3.18% | MS4A1 | 1.93 | False | no | False |
| PRAD | Census | Malignant/epithelial | 3210 | 0.1092 | 1 | FAAH 35.55% | MS4A1 | 0.16 | True | no | True |
| PRAD | Census | Stromal/other | 42415 | 0.1085 | 2 | MGLL 21.08% | MS4A1 | 0.17 | True | no | True |
| KIRC | Census | B/plasma | 2907 | 0.0318 | 4 | CNR2 14.52% | MS4A1 | — | False | no | False |
| KIRC | Census | Myeloid | 25168 | 0.0491 | 3 | DAGLB 14.48% | MS4A1 | 0.39 | False | no | False |
| KIRC | Census | T/NK | 98148 | 0.0533 | 2 | MGLL 7.48% | MS4A1 | 2.42 | True | no | True |
| KIRC | Census | Malignant/epithelial | 0 | — | — | — | MS4A1 | — | False | no | False |
| KIRC | Census | Stromal/other | 61569 | 0.1488 | 1 | MGLL 30.34% | MS4A1 | 0.69 | True | no | True |
| STAD | Census | B/plasma | 38138 | 0.0083 | 4 | MGLL 3.06% | MS4A1 | — | False | no | False |
| STAD | Census | Myeloid | 8294 | 0.0164 | 3 | MGLL 6.26% | MS4A1 | 0.65 | False | no | False |
| STAD | Census | T/NK | 19286 | 0.0068 | 5 | MGLL 1.72% | MS4A1 | 1.32 | False | no | False |
| STAD | Census | Malignant/epithelial | 10436 | 0.1189 | 1 | MGLL 27.16% | MS4A1 | 0.53 | True | no | True |
| STAD | Census | Stromal/other | 141769 | 0.0663 | 2 | MGLL 17.73% | MS4A1 | 3.97 | True | no | True |
| HNSC | Census | B/plasma | 10616 | 0.0310 | 4 | MGLL 7.12% | MS4A1 | — | False | no | False |
| HNSC | Census | Myeloid | 11339 | 0.0587 | 3 | MGLL 14.37% | MS4A1 | 0.77 | False | no | False |
| HNSC | Census | T/NK | 25862 | 0.0107 | 5 | DAGLB 2.78% | MS4A1 | 2.57 | False | no | False |
| HNSC | Census | Malignant/epithelial | 18062 | 0.1245 | 1 | MGLL 13.77% | MS4A1 | 0.59 | True | no | True |
| HNSC | Census | Stromal/other | 16499 | 0.1036 | 2 | MGLL 22.24% | MS4A1 | 0.61 | True | no | True |
| GBM | Census | B/plasma | 5465 | 0.0538 | 4 | CNR2 14.53% | MS4A1 | — | False | no | False |
| GBM | Census | Myeloid | 407923 | 0.1668 | 3 | DAGLB 27.09% | MS4A1 | 0.44 | False | no | False |
| GBM | Census | T/NK | 499597 | 0.3377 | 2 | MGLL 20.81% | MS4A1 | 0.76 | True | no | True |
| GBM | Census | Malignant/epithelial | 0 | — | — | — | MS4A1 | — | False | no | False |
| GBM | Census | Stromal/other | 450998 | 0.3455 | 1 | MGLL 29.41% | MS4A1 | 0.25 | True | no | True |

## Per-gene detection (% cells with count > 0)

| Type | Bucket | n | CNR1 % | CNR2 % | GPR55 % | TRPV1 % | FAAH % | MGLL % | DAGLA % | DAGLB % | NAPEPLD % |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| OV | B/plasma | 42127 | 1.42 | 7.12 | 0.56 | 0.94 | 1.08 | 14.39 | 0.08 | 2.58 | 5.02 |
| OV | Myeloid | 207417 | 0.08 | 0.29 | 0.43 | 2.14 | 1.64 | 24.53 | 2.31 | 22.70 | 6.21 |
| OV | T/NK | 274230 | 0.02 | 0.64 | 0.54 | 0.65 | 0.36 | 1.85 | 0.06 | 1.92 | 4.60 |
| OV | Malignant/epithelial | 255732 | 0.09 | 0.06 | 0.20 | 2.95 | 10.12 | 18.97 | 1.59 | 5.64 | 21.82 |
| OV | Stromal/other | 205482 | 0.37 | 0.04 | 0.02 | 1.29 | 0.83 | 11.03 | 0.92 | 4.16 | 9.38 |
| PRAD | B/plasma | 828 | 4.47 | 8.21 | 0.60 | 0.48 | 3.14 | 3.26 | 0.00 | 3.14 | 2.05 |
| PRAD | Myeloid | 2794 | 0.14 | 0.25 | 0.72 | 1.15 | 4.12 | 7.98 | 0.97 | 16.00 | 2.25 |
| PRAD | T/NK | 19075 | 0.04 | 0.31 | 0.59 | 0.47 | 1.28 | 1.09 | 0.04 | 3.18 | 1.52 |
| PRAD | Malignant/epithelial | 3210 | 0.06 | 0.44 | 0.00 | 2.37 | 35.55 | 2.77 | 1.96 | 4.89 | 17.91 |
| PRAD | Stromal/other | 42415 | 3.03 | 0.31 | 0.01 | 3.06 | 17.32 | 21.08 | 1.55 | 5.56 | 9.36 |
| KIRC | B/plasma | 2907 | 2.27 | 14.52 | 0.48 | 0.00 | 0.17 | 1.17 | 0.00 | 2.48 | 4.61 |
| KIRC | Myeloid | 25168 | 0.04 | 0.18 | 0.36 | 0.08 | 2.53 | 11.48 | 1.16 | 14.48 | 2.46 |
| KIRC | T/NK | 98148 | 0.10 | 0.30 | 0.48 | 0.00 | 1.17 | 7.48 | 0.18 | 2.22 | 4.32 |
| KIRC | Malignant/epithelial | 0 | — | — | — | — | — | — | — | — | — |
| KIRC | Stromal/other | 61569 | 0.44 | 0.06 | 0.36 | 0.26 | 3.47 | 30.34 | 1.31 | 12.20 | 6.23 |
| STAD | B/plasma | 38138 | 0.64 | 1.38 | 0.21 | 0.16 | 0.31 | 3.06 | 0.01 | 0.57 | 0.77 |
| STAD | Myeloid | 8294 | 0.00 | 0.06 | 0.25 | 0.13 | 0.37 | 6.26 | 0.47 | 2.36 | 0.63 |
| STAD | T/NK | 19286 | 0.01 | 0.12 | 0.61 | 0.10 | 0.36 | 1.72 | 0.02 | 1.12 | 1.06 |
| STAD | Malignant/epithelial | 10436 | 0.02 | 0.06 | 0.04 | 0.93 | 14.32 | 27.16 | 1.33 | 6.54 | 11.64 |
| STAD | Stromal/other | 141769 | 0.52 | 0.21 | 0.43 | 0.88 | 4.32 | 17.73 | 0.78 | 4.59 | 4.78 |
| HNSC | B/plasma | 10616 | 3.04 | 6.12 | 0.79 | 0.65 | 0.71 | 7.12 | 0.02 | 2.51 | 2.62 |
| HNSC | Myeloid | 11339 | 0.06 | 0.66 | 0.72 | 0.75 | 0.96 | 14.37 | 1.81 | 7.64 | 2.03 |
| HNSC | T/NK | 25862 | 0.03 | 0.51 | 1.48 | 0.42 | 0.22 | 0.98 | 0.02 | 2.78 | 2.32 |
| HNSC | Malignant/epithelial | 18062 | 0.20 | 0.09 | 1.00 | 1.71 | 9.97 | 13.77 | 1.43 | 13.18 | 12.95 |
| HNSC | Stromal/other | 16499 | 1.74 | 0.14 | 0.10 | 2.29 | 2.22 | 22.24 | 1.25 | 4.98 | 10.16 |
| GBM | B/plasma | 5465 | 4.41 | 14.53 | 0.55 | 0.70 | 0.68 | 6.42 | 0.07 | 3.42 | 3.51 |
| GBM | Myeloid | 407923 | 0.92 | 0.22 | 0.23 | 1.49 | 1.00 | 15.74 | 1.53 | 27.09 | 2.71 |
| GBM | T/NK | 499597 | 15.00 | 0.30 | 0.31 | 2.30 | 2.04 | 20.81 | 3.23 | 8.50 | 16.76 |
| GBM | Malignant/epithelial | 0 | — | — | — | — | — | — | — | — | — |
| GBM | Stromal/other | 450998 | 9.06 | 0.24 | 0.30 | 3.81 | 8.19 | 29.41 | 4.55 | 24.32 | 9.85 |

## Catalog ECS-state calls (not new named states)

A kept=True row is a catalog call under the kill ECS-state + contamination rule. Confirmatory **named** states are not expanded beyond the three frozen buckets.

| Bucket | Expansion types where kept | Role |
|---|---|---|
| Myeloid | OV | catalog row only |
| T/NK | GBM, KIRC | catalog row only |
| Malignant/epithelial | HNSC, OV, PRAD, STAD | frozen named state |
| Stromal/other | GBM, HNSC, KIRC, PRAD, STAD | frozen named state |

Myeloid / T/NK catalog calls: **Myeloid, T/NK**. These rows stay catalog-only and are **not** confirmatory named states.

## Gate E draft (human marks)

- Every locked type tabled or skipped with a reason: **True**
- Extra types added: **0**
- TISCH2 used: **False**
- ICI files opened: **False**
- Nine core genes unchanged: **True**
- Named states unchanged (B/plasma, Malignant/epithelial, Stromal/other): **True**
- Myeloid / T/NK not promoted to named states: **True**
- Primary remains **Stromal/other**: **True**
- Operator Gate E numbers hold: **True**

Gate E is human-owned. Operator draft holds if every locked expansion type has a complete type × lineage table or a documented skip (missing in Census or n < 10,000), no substitute types, no TISCH2, nine genes unchanged, confirmatory named states stay the three frozen buckets, myeloid / T/NK catalog rows are not promoted, and the primary remains Stromal/other.

## Human Gate E

- [X] Pass (every type tabled or skipped; no substitutes; named states unchanged) — marked 2026-08-25
- [ ] Fail (silent drop / extra type / TISCH2 / promoted named state)

## What was not done

- No TISCH2 (or other) substitution for skipped types.
- No extra cancer type added.
- No ICI phenotype or outcome files opened.
- No NMF, new clustering, or DE. No UMAP / browser.
- No gene added. Primary **Stromal/other** not renamed.
- Myeloid / T/NK catalog rows not promoted to confirmatory named states.
- No stromal subtype table (Unit 13).
