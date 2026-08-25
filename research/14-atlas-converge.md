# Unit 14 — Converge atlas + frozen ICI (Gate F)

**Run date:** 2026-08-25  
**Kill protocol SHA:** `3fbf310870c57247163edca35ed536ade3ea4301`  
**Atlas protocol SHA:** `2a74270a16685cbc4df5c45c293a7afb5b7665f5`  
**Rule:** Compare Units 10–13 to sealed `PROTOCOL-ATLAS.md`. Confirm the ICI chapter is Units 06–07 unchanged. Draft Gate F. Do not rewrite kill or atlas confirmatory fields. Do not refit ICI. Do not promote OS / GEO / deconvolution / expansion catalog rows to a checkpoint claim. Human marked Gate F **pass** (2026-08-25). **Decide: atlas paper as written** (2026-08-25).

## Protocol lock

- Atlas seal commit: `2a74270` (2026-08-24). `PROTOCOL-ATLAS.md` and `KILL-ATLAS.md` have **no** commits after that SHA.
- Kill seal commit: `3fbf310` (2026-08-24). `PROTOCOL.md` and `KILL.md` have **no** commits after that SHA. `CLAIMS.md` last commit is `2a19cb0` (before kill seal); **no** commits after `3fbf310`.
- ICI outcomes last written in `c1a47f9` (Units 06–07). Atlas-phase commits `c898e66` and `3be1149` add Units 10–13 only. `pipeline/imvigor_06.py` and `pipeline/geo_07.py` were **not** re-run.

## Locked lists and map

| Check | Result |
|---|---|
| Nine core ECS genes | Unchanged: `CNR1, CNR2, GPR55, TRPV1, FAAH, MGLL, DAGLA, DAGLB, NAPEPLD` (Units 10, 12, `pipeline/genes.py`, `research/03-frozen-markers.json`) |
| Neighbors (`GPR18, GPR119, TRPV2, ABHD6, ABHD12`) | Not added. Still in `EXPLORE.md` |
| Named states | Still **B/plasma**, **Malignant/epithelial**, **Stromal/other** |
| Primary display name | **Stromal/other** (Unit 05). Not renamed in Units 10–13 |
| Census pin | `2025-11-08`. BLCA pin: TISCH2 `BLCA_GSE130001` + GEO `GSE130001` (kill fallback only) |
| UMAP / browser / Harmony / scVI | Not run |
| scGPT / GSE220635 | Not run. Stay in `EXPLORE.md` |

scRNA scoring (Units 10, 12) used available-case means of **raw counts** inside locked lineage buckets. No NMF, clustering, or DE. Stromal sublabels (Unit 13) are existing Census / TISCH2 labels, display-only.

## Gate drafts vs `KILL-ATLAS.md`

### Gate D — core map reproduces (Unit 10; human already marked)

- Nine core genes unchanged: **True**
- Kept ECS-state buckets: **B/plasma**, **Malignant/epithelial**, **Stromal/other** (same three as Unit 02)
- Kept↔dropped flips vs Unit 02: **0**. Numeric drift at published precision: **none**
- No new confirmatory bucket (myeloid / T/NK not named)
- Primary remains **Stromal/other**
- Operator Gate D numbers hold: **True**
- Human Gate D: **pass** (2026-08-24)

### Gate E — expansion is pre-specified (Units 11–12; human already marked)

Locked list (12): `PAAD`, `OV`, `PRAD`, `KIRC`, `LIHC`, `STAD`, `ESCA`, `HNSC`, `GBM`, `UCEC`, `THCA`, `CESC`. Extra types added: **0**.

| Type | Decision | Reason |
|---|---|---|
| OV, PRAD, KIRC, STAD, HNSC, GBM | tabled | n ≥ 10,000 (Unit 11 n = Unit 12 n) |
| PAAD, ESCA, UCEC, THCA, CESC | skip | missing in Census |
| LIHC | skip | n < 10,000 |

- TISCH2 used for expansion: **False** (BLCA TISCH2 is the kill pin, not expansion shopping)
- Named states unchanged. Myeloid (OV) and T/NK (GBM, KIRC) stay **catalog-only**
- Primary remains **Stromal/other**
- Operator Gate E numbers hold: **True**
- Human Gate E: **pass** (2026-08-25)

Unit 13 is not a gate. Composition tables cover the 11 included types (core five + six expansion). Stromal n matches Units 10/12 (**0** mismatches). Sublabels did not rename **Stromal/other**. No UMAP.

### Gate F — ICI stays frozen (this unit)

Paper-packet ICI numbers vs Units 06–07:

| Source | IMvigor210 Model 1 | Match |
|---|---|---|
| `research/06-imvigor210.md` (source) | n=298; ECS OR 1.189 (0.551–2.563); CI includes 1; VIF(ECS)=1.360 | — |
| `PROTOCOL-ATLAS.md` confirmatory ICI chapter | n=298; ECS OR 1.189 (0.551–2.563); CI includes 1; VIF(ECS)=1.360 | **True** |
| `PLAN-ATLAS.md` | ECS OR 1.189, 0.551–2.563 | **True** |
| `STATUS.md` Scribe bound | ECS OR 1.189, 95% CI 0.551–2.563 | **True** |

| Source | GEO (replication; cannot rescue) | Match |
|---|---|---|
| `research/07-melanoma-geo.md` (source) | GSE78220 n=26 ECS OR 0.469 (0.019–11.697); GSE91061 n=49 ECS OR 0.603 (0.066–5.510); both CIs include 1 | — |
| `PROTOCOL-ATLAS.md` | Cites Units 06–07; no new GEO model | **True** |
| `STATUS.md` ledger | Same two accessions and n; display rounding 0.47 (0.02–11.7) / 0.60 (0.07–5.51) as Unit 08 | **True** (citation, not a refit) |

- New ICI model / cutoff / gene / cohort: **False**
- ICI matrices re-read in Units 10–13: **False** (citation only; no bit-for-bit re-fit required)
- Gate B remains **fail**. No path in `KILL-ATLAS.md` to a Gate B pass
- Operator Gate F numbers hold: **True**

Gate F is human-owned. **Pass** marked 2026-08-25: manuscript ICI numbers match Units 06–07; no new ICI analysis.

## Scribe bound

`CLAIMS.md` item 3 remains the sealed either/or from the kill. This unit does **not** edit it.

Atlas paper claim (`PROTOCOL-ATLAS.md` / `STATUS.md` Scribe bound):

1. Human tumor ECS is visible as **lineage cell states** (nine core genes).
2. At least one non-B state (**Stromal/other**) is distinguishable from B-cell / TLS abundance (Gate A, passed).
3. The **frozen** Stromal/other score **does not** associate with IMvigor210 **response** after B + TLS + CD8 (Model 1 ECS OR 1.189, 95% CI 0.551–2.563). OS, unadjusted, Model 2, deconvolution, and melanoma GEO do not carry this claim.

Must not say: cannabis/CBD treats cancer; CB2 **is** a clinical checkpoint; patients should change cannabis during PD-1; melanoma GEO validates a biomarker; an OS-only or unadjusted signal is a checkpoint association; myeloid / T/NK catalog rows are confirmatory named states; stromal subtypes are a new state.

## Decide map (`KILL-ATLAS.md`)

| Atlas result | Decision |
|---|---|
| **D pass, E pass, F pass** | **Atlas paper as written** (core + expansion; ICI negative chapter) — mapped path |
| D pass, E fail (skips or amend) | Narrower atlas (core five, maybe partial expansion); still ICI negative — not this case (E passed; skips were pre-specified) |
| D fail | Stop or amend; do not invent new states — not this case |
| F fail | Do not ship; revert ICI chapter to Units 06–07 — not this case |

There is no path here to a full-paper Gate B pass. Human may still choose **stop** (no atlas paper). That is a product choice, not a gate.

## Human Gate F

- [X] Pass (ICI numbers = Units 06–07; no new ICI analysis) — marked 2026-08-25
- [ ] Fail (any ICI fishing)

## Human Decide (atlas)

- [X] Atlas paper as written (core + expansion; ICI negative chapter) — mapped path (D/E/F pass) — marked 2026-08-25
- [ ] Stop (no atlas paper)
- [ ] Narrower atlas — **closed** (Gate E passed; skips were locked)
- [ ] Full paper — **closed** unless a dated kill-protocol amendment reopens Gate B

Scribe ≤ `CLAIMS.md` non-claims + `PROTOCOL-ATLAS.md` frozen negative. Do not claim CB2 is a checkpoint. **Scribe (2026-08-25):** [`RESULTS.md`](../RESULTS.md) · [`docs/manuscript.md`](../docs/manuscript.md). **Archive (2026-08-25):** [`EXPLORE.md`](../EXPLORE.md).

## Disclosed operational choices (not amendments)

These were recorded in unit notes. They do not change confirmatory fields.

- ICI work in this phase is citation. Matrices were not re-opened; protocol allows a bit-for-bit reproduction only, which was not needed.
- `STATUS.md` GEO ORs keep Unit 08 display rounding; `research/07-melanoma-geo.md` is the source.
- Expansion skips include LIHC (HCC label present, 0 cells after the Unit 01 filter) and five types missing in Census. Near-miss labels (generic RCC, liver cancer, `malignant pancreatic neoplasm`) were **not** substituted.
- Myeloid (OV) and T/NK (GBM, KIRC) are catalog rows under the kill ECS-state rule. They were not promoted.
- Stromal unmatched is heavy in STAD, GBM, CRC, and KIRC. That is existing-label composition, not a new confirmatory state.

No dated amendment. **Archive (2026-08-25):** leftovers and closed paths recorded in `EXPLORE.md` (not promoted to claims).

## What was not done

- No edit to `PROTOCOL-ATLAS.md` / `KILL-ATLAS.md` / `PROTOCOL.md` / `KILL.md` / `CLAIMS.md`.
- No ICI refit, cutoff search, new ECS gene, or new ICI cohort.
- No UMAP / browser / scGPT / GSE220635. No TISCH2 shopping. No extra cancer type.
- OS, Model 2, unadjusted, deconvolution, GEO, and expansion catalog rows were not used to flip Gate B.
- Human Gate F: **pass** (2026-08-25). **Human Decide: atlas paper as written** (2026-08-25).
