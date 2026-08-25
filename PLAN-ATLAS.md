# SCENDO atlas plan (external review)

**Study:** SCENDO — atlas-only paper after kill.  
**Stage:** Protocol **SEALED 2026-08-24**. Clarify and Analyze done. Kill test is done and frozen (SHA `3fbf310`). Units 10–11 **done**. Gate D **pass**. Next: **Run** Unit 12.  
**Audience:** Independent reviewer (computational oncology / immunology).  
**Ask:** Does this frozen atlas protocol match `PROTOCOL-ATLAS.md` / `KILL-ATLAS.md`?

**Source of truth:** `PROTOCOL-ATLAS.md`. Pass/fail bars: `KILL-ATLAS.md`. This brief restates them. If this file disagrees with `PROTOCOL-ATLAS.md`, **that file wins**. Kill science stays in `PROTOCOL.md` / `KILL.md` / `CLAIMS.md` (SHA `3fbf310`).

**What we are not asking you to bless:** public browser, scGPT, GSE220635, FAERS/DDI, a new ICI-positive claim, or renaming **Stromal/other**.

---

## 1. Why a new protocol

Kill result: Gate A **pass**, Gate B **fail**. Decide: **atlas-only; ICI reported negative**.

The map is the paper. The ICI chapter is the frozen negative (IMvigor210 Model 1 ECS OR 1.189, 0.551–2.563). This protocol expands the **map**. It does not hunt a Gate B pass.

## 2. Design in one picture

```
Frozen kill objects (nine genes, three states, Stromal/other primary)
        ↓
Reproduce five-type catalog          →  Gate D
        ↓
Census expansion (locked type list)  →  Gate E
        ↓
Cite Units 06–07 ICI numbers         →  Gate F (no refit)
        ↓
Human Seal → Run 10–14 → Converge
```

## 3. Frozen objects

Same nine genes, lineage map, contamination rule, and scoring math as the kill. Neighbors stay out. No DE / NMF / new clustering.

Expansion types (Census, skip if missing or n < 10k): PAAD, OV, PRAD, KIRC, LIHC, STAD, ESCA, HNSC, GBM, UCEC, THCA, CESC. No new TISCH2. Heme and normal tissue out. No UMAP.

## 4. Gates

| Gate | Pass |
|---|---|
| D | Core five types still yield the same three ECS-state buckets; primary stays Stromal/other |
| E | Every expansion type tabled or skipped with a reason; no substitute types; myeloid/T/NK catalog rows are not new named states |
| F | ICI numbers are Units 06–07; no new ICI analysis |

## 5. Execution

Units 10–14 in `units/`. Laptop, Python, `pipeline/`. Clarify **done**. Analyze **pass**. Seal **done** (2026-08-24). Units 10–11 **done**. Gate D **pass**. Next: **Run** Unit 12.

## 6. Frozen design (this lock)

- [x] Nine-gene list and primary name stay frozen
- [x] Expansion list is pre-specified (no type shopping)
- [x] No ICI refit / no new ICI cohorts
- [x] No browser / scGPT / GSE220635 in this lock
- [x] Stromal subtypes are display, not new confirmatory states
- [x] Scribe ≤ `CLAIMS.md` non-claims + frozen ICI negative
