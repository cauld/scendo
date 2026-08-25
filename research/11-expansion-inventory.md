# Unit 11 — Expansion inventory (Gate E)

**Run date:** 2026-08-24  
**Census version:** `2025-11-08`  
**Kill protocol SHA:** `3fbf310870c57247163edca35ed536ade3ea4301`  
**Atlas protocol SHA:** `2a74270a16685cbc4df5c45c293a7afb5b7665f5`  
**Rule:** Census only. Map each locked expansion type to Census `disease` strings (Unit 00 style). Count cells after the Unit 01 filter (`is_primary_data == True`; drop tissue_type in cell culture / organoid / cell line). Include if n ≥ 10,000; else skip (missing **or** n < 10,000). Do not substitute a type or a TISCH2 dataset. No ICI files.

## Sources

- CELLxGENE Census pin `2025-11-08`, human RNA, `is_primary_data == True`.
- Locked types: `PROTOCOL-ATLAS.md` (PAAD, OV, PRAD, KIRC, LIHC, STAD, ESCA, HNSC, GBM, UCEC, THCA, CESC).
- Disease mapping: a priori needles plus exact Census strings in `pipeline/inventory_11.py` (same substring style as Unit 00). First locked type wins on overlap.
- Cell filter: same as Unit 01 (`census_obs_filter` + culture/organoid/cell-line drop). Summary-table n is recorded but does **not** decide include/skip.
- Handoff: `research/11-expansion-inventory.json` (include list for Unit 12).

Types scored: **12** (no extras). Include: **6** (OV, PRAD, KIRC, STAD, HNSC, GBM). Skip: **6** (PAAD, LIHC, ESCA, UCEC, THCA, CESC).

## Inventory

| Type | Protocol name | Census disease strings | n cells | Decision | Reason |
|---|---|---|---:|---|---|
| PAAD | pancreatic adenocarcinoma | — | 0 | **skip** | missing in Census |
| OV | ovarian | malignant ovarian serous tumor; ovarian cancer | 984,988 | **include** | n ≥ 10,000 |
| PRAD | prostate | prostatic acinar adenocarcinoma | 68,322 | **include** | n ≥ 10,000 |
| KIRC | clear cell kidney | clear cell renal carcinoma | 187,792 | **include** | n ≥ 10,000 |
| LIHC | hepatocellular | hepatocellular carcinoma | 0 | **skip** | n < 10,000 |
| STAD | stomach | gastric cancer | 217,923 | **include** | n ≥ 10,000 |
| ESCA | esophageal | — | 0 | **skip** | missing in Census |
| HNSC | head and neck squamous | oral cavity squamous cell carcinoma; oropharynx squamous cell carcinoma; tongue cancer | 82,378 | **include** | n ≥ 10,000 |
| GBM | glioblastoma | glioblastoma | 1,363,983 | **include** | n ≥ 10,000 |
| UCEC | endometrial | — | 0 | **skip** | missing in Census |
| THCA | thyroid | — | 0 | **skip** | missing in Census |
| CESC | cervical | — | 0 | **skip** | missing in Census |

## Per-label n (after Unit 01 filter)

| Type | Disease | n cells |
|---|---|---:|
| PAAD | — | 0 |
| OV | malignant ovarian serous tumor | 927,205 |
| OV | ovarian cancer | 57,783 |
| PRAD | prostatic acinar adenocarcinoma | 68,322 |
| KIRC | clear cell renal carcinoma | 187,792 |
| LIHC | hepatocellular carcinoma | 0 |
| STAD | gastric cancer | 217,923 |
| ESCA | — | 0 |
| HNSC | oral cavity squamous cell carcinoma | 28,186 |
| HNSC | oropharynx squamous cell carcinoma | 51,200 |
| HNSC | tongue cancer | 2,992 |
| GBM | glioblastoma | 1,363,983 |
| UCEC | — | 0 |
| THCA | — | 0 |
| CESC | — | 0 |

## Needles (a priori)

Locked before seeing cell counts. Matching is case-insensitive substring on each `||`-delimited part of the Census `disease` field. Heme, normal/healthy, uveal, and the kill-test core five are excluded even if a needle hits.

| Type | Needles |
|---|---|
| PAAD | `pancreatic adenocarcinoma`, `pancreatic ductal adenocarcinoma`, `pancreatic cancer`, `pancreas adenocarcinoma`, `pancreas cancer` |
| OV | `ovarian cancer`, `ovarian carcinoma`, `ovarian adenocarcinoma`, `ovarian serous`, `high-grade serous ovarian`, `high grade serous ovarian`, `high grade ovarian serous`, `ovary adenocarcinoma`, `ovary carcinoma`, `ovary cancer`, `ovarian epithelial`, `epithelial ovarian` |
| PRAD | `prostate adenocarcinoma`, `prostate cancer`, `prostate carcinoma`, `prostatic adenocarcinoma`, `prostatic cancer`, `prostatic carcinoma` |
| KIRC | `clear cell renal cell carcinoma`, `clear cell renal carcinoma`, `kidney clear cell carcinoma`, `kidney renal clear cell`, `clear cell kidney`, `renal clear cell`, `clear-cell renal` |
| LIHC | `hepatocellular carcinoma`, `hepatocellular cancer`, `liver hepatocellular`, `hepatocellular` |
| STAD | `stomach adenocarcinoma`, `gastric adenocarcinoma`, `gastric cancer`, `stomach cancer`, `gastric carcinoma`, `stomach carcinoma` |
| ESCA | `esophageal adenocarcinoma`, `esophageal squamous`, `oesophageal`, `esophageal carcinoma`, `esophageal cancer`, `esophagus adenocarcinoma`, `esophagus squamous`, `esophagus carcinoma`, `esophagus cancer`, `oesophagus` |
| HNSC | `head and neck squamous`, `head and neck squamous cell carcinoma`, `oral squamous`, `oral cavity squamous`, `oropharyngeal squamous`, `laryngeal squamous`, `hypopharyngeal squamous`, `tongue squamous`, `tonsil squamous`, `floor of mouth squamous`, `buccal squamous`, `gingival squamous`, `lip squamous` |
| GBM | `glioblastoma` |
| UCEC | `endometrial carcinoma`, `endometrial cancer`, `endometrial adenocarcinoma`, `uterine corpus endometrial`, `endometrioid adenocarcinoma of the endometrium`, `endometrioid endometrial`, `endometrium carcinoma`, `endometrium cancer`, `endometrium adenocarcinoma` |
| THCA | `thyroid carcinoma`, `thyroid cancer`, `thyroid adenocarcinoma`, `papillary thyroid`, `follicular thyroid carcinoma`, `follicular thyroid cancer`, `thyroid gland carcinoma`, `thyroid gland cancer`, `thyroid gland adenocarcinoma` |
| CESC | `cervical cancer`, `cervical carcinoma`, `cervical squamous`, `cervical adenocarcinoma`, `cervix cancer`, `cervix carcinoma`, `cervix squamous`, `cervix adenocarcinoma`, `uterine cervix`, `squamous cell carcinoma of the cervix`, `adenocarcinoma of the cervix`, `cervix uteri` |

## Census exact strings (same locked type)

Recorded after inspecting Census `disease` labels. These are the locked type under a different MONDO string, not extra cancer types.

| Type | Exact Census string |
|---|---|
| PRAD | `prostatic acinar adenocarcinoma` |
| HNSC | `oropharynx squamous cell carcinoma` |
| HNSC | `tongue cancer` |

Inspected and **not** mapped (would be a substitute type or a broader parent): `malignant pancreatic neoplasm` (not adenocarcinoma-specific); `renal cell carcinoma`, `nonpapillary renal cell carcinoma`, `chromophobe renal cell carcinoma` (not specifically KIRC); `liver cancer` (not specifically LIHC); `intrahepatic cholangiocarcinoma` (not in the locked list).


## Near-miss labels (not used)

Malignant Census `disease` labels that mention a locked-type token but did **not** map to a locked type. Listed so skips are not silent and so no extra type is added. These rows are **not** included.

| Disease | Summary n (not Unit 01 n) |
|---|---:|
| chromophobe renal cell carcinoma | 2,576 |
| intrahepatic cholangiocarcinoma | 0 |
| kidney benign neoplasm | 57 |
| liver cancer | 6,661 |
| malignant pancreatic neoplasm | 2,148 |
| nonpapillary renal cell carcinoma | 287,368 |
| renal cell carcinoma | 238,027 |

## Include list (Unit 12)

`OV`, `PRAD`, `KIRC`, `STAD`, `HNSC`, `GBM`.

Skipped types (one-line reason):

- `PAAD`: missing in Census
- `LIHC`: n < 10,000
- `ESCA`: missing in Census
- `UCEC`: missing in Census
- `THCA`: missing in Census
- `CESC`: missing in Census

## Completeness draft (Gate E inventory half)

- Every locked type is include or skip: **True**
- Extra types added: **0**
- TISCH2 used: **False**
- ICI files opened: **False**

Gate E is completed by Unit 12 (type × lineage tables for included types). This unit only records Census strings, n, and include vs skip.

## What was not done

- No TISCH2 (or other) substitution for skipped types.
- No extra cancer type added.
- No ECS scores, lineage tables, or contamination calls (Unit 12).
- No ICI phenotype or outcome files opened.
- No UMAP / browser / clustering / DE. No gene added.
