---
id: 01
role: Operator
status: done
reads:
  - PROTOCOL.md
  - KILL.md
  - research/data-inventory.md
must_not:
  - Open ICI phenotype or outcome files
  - Edit confirmatory protocol fields
---

# Unit 01 — Detection rates (Gate C)

**Goal.** Report *CNR2*, *MGLL*, and *FAAH* detection by lineage bucket and cancer type. Score Gate C. No ICI labels.

**Inputs.** Census (primary) and TISCH2 fallback only where Unit 00 recorded Census missing a type. Lineage map in `PROTOCOL.md`.

**Procedure.**

1. Load scRNA for available types among NSCLC, melanoma, CRC, BRCA, BLCA (≥2 types or stop and amend).
2. Assign lineage buckets with the locked substring map.
3. For each type × bucket, compute % cells with count > 0 for `CNR2`, `MGLL`, `FAAH`.
4. Apply Gate C rules in `KILL.md` / `PROTOCOL.md`. Do not build a raw-*CNR2* UMAP atlas if *CNR2* < 1% in every non-B lineage in every type.

**Outputs.** `research/01-detection.md` (table + Gate C call for the human).

**Pass criteria.** Table complete. Human marks Gate C. If Gate C **fail (stop the kill)**, do not continue Units 02–08 as a checkpoint path.

## Notes (after run)

- **2026-08-24 table complete.** `research/01-detection.md`. Runner: `uv run python pipeline/detection_01.py`. Census `2025-11-08`, 5 types. BLCA barcodes 4129/4129 matched to GEO MTX.
- Operator Gate C **draft** (human must mark): no-UMAP-atlas rule **false** (melanoma non-B CNR2 is not < 1% in every lineage). MGLL and FAAH are not both < 5% in every non-B lineage. Stop-kill detection half **false** → Gate C cannot stop the kill on detectability alone.
- BLCA `GSE130001` has no B/myeloid/T cells under the locked map (epithelial + stromal only). Melanoma Census n is small (~24k primary-data cells after dropping uveal).
- No ICI files opened. No UMAP.
- **2026-08-24 human Gate C:** Pass / continue (do not stop the kill on detectability). `research/01-detection.md`.
