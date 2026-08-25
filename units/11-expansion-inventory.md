---
id: 11
role: Operator
status: done
reads:
  - PROTOCOL-ATLAS.md
  - research/data-inventory.md
must_not:
  - Add a cancer type because it looks interesting
  - Use TISCH2 for expansion types
  - Open ICI outcomes
---

# Unit 11 — Expansion inventory

**Goal.** For each locked expansion type, record Census disease strings, n cells after the Unit 01 filter, and include vs skip.

**Inputs.** Locked list in `PROTOCOL-ATLAS.md`. Census `2025-11-08`, `is_primary_data == True`.

**Procedure.**

1. Map each type (`PAAD`, `OV`, `PRAD`, `KIRC`, `LIHC`, `STAD`, `ESCA`, `HNSC`, `GBM`, `UCEC`, `THCA`, `CESC`) to Census `disease` labels (record the strings).
2. Count cells after the same primary-data filter as Unit 01.
3. Include if n ≥ 10,000; else skip with the reason (missing **or** n < 10,000). Do not substitute another type.

**Outputs.** `research/11-expansion-inventory.md`

**Pass criteria.** Every listed type is include or skip. No extras.

## Notes (after run)

- **2026-08-24 complete.** `research/11-expansion-inventory.md` (+ `research/11-expansion-inventory.json` for Unit 12). Runner: `uv run python pipeline/inventory_11.py`. Census `2025-11-08`, `is_primary_data == True`, same culture/organoid/cell-line drop as Unit 01. No TISCH2. No extra types. No ICI files.
- **Include (n ≥ 10,000):** `OV` 984,988; `PRAD` 68,322; `KIRC` 187,792; `STAD` 217,923; `HNSC` 82,378; `GBM` 1,363,983.
- **Skip:** `PAAD` missing in Census; `LIHC` n < 10,000 (HCC label present, 0 cells); `ESCA`, `UCEC`, `THCA`, `CESC` missing in Census. Did not substitute generic RCC, liver cancer, cholangiocarcinoma, or `malignant pancreatic neoplasm`.
- Every locked type is include or skip. **Next:** Unit 12 expansion states (Gate E tables).
