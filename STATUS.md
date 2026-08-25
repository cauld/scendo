# STATUS

**Study:** SCENDO  
**Flow:** [`.seal/E2E_FLOW.md`](.seal/E2E_FLOW.md) (generic) · [`E2E_FLOW.md`](E2E_FLOW.md) (this study)  
**Protocol seal:** **SEALED 2026-08-24**  
**Confirmatory git SHA:** `3fbf310870c57247163edca35ed536ade3ea4301` (`3fbf310`)  
**OSF URL:** not yet (public lock may follow this SHA by a day)  
**Current stage:** Units 00–02 done. Human marked Gate C **pass / continue**. **Next:** Unit 03 (freeze markers).  
**Order / what to run:** [`docs/SEAL-FLOW.md`](docs/SEAL-FLOW.md)  
**Decision:** none yet (full paper vs atlas-only vs stop)

**External review brief:** [`PLAN.md`](PLAN.md)

## Ledger

| Date | Event |
|---|---|
| 2026-08-24 | SCENDO study files opened |
| 2026-08-24 | Reusable flow kernel in `.seal/`; this STATUS opened |
| 2026-08-24 | Clarify: five confirmatory gaps closed in `PROTOCOL.md` |
| 2026-08-24 | Validation found contradictions; protocol patched (see `PROTOCOL.md` amendments) |
| 2026-08-24 | External review: residual hatch capped at \|r\| < 0.75; Gate B also requires VIF(ECS) < 3; missing-gene score frozen as available-case mean |
| 2026-08-24 | Analyze pass: confirmatory artifacts consistent (note below) |
| 2026-08-24 | Analyze nits applied; Units 01–08 packets written |
| 2026-08-24 | Human confirmed CLAIMS / KILL / PROTOCOL; seal patches (MS4A1 fallback; Unit 05 tie cascade) |
| 2026-08-24 | **Protocol sealed** at git SHA `3fbf310870c57247163edca35ed536ade3ea4301` |
| 2026-08-24 | Unit 00 inventory: sources reachable; IMvigor 9/9 ECS; Census 4/5 types (BLCA → TISCH2); no outcome peek |
| 2026-08-24 | Unit 01 detection table: 5 types; stop-kill detection half **false**; human marks Gate C |
| 2026-08-24 | Human Gate C: **pass / continue**. Unit 02 scRNA states: 3 candidate buckets (B/plasma, malignant/epithelial, stromal/other); two-lineage rule holds; no contamination drops |

## Analyze (2026-08-24)

Read-only check of `QUESTION.md`, `CLAIMS.md`, `KILL.md`, `PROTOCOL.md`, `PLAN.md`, `EXPLORE.md`, `PHASES.md`, `E2E_FLOW.md`, `units/`.

**Verdict: pass.** No confirmatory contradiction. Protocol is freeze-ready after Unit 00 and human Seal.

**Aligned (locked science):**

- Question / claims / non-claims: map + frozen IMvigor210 **response** test; OS, unadjusted, deconvolution, melanoma GEO cannot carry the claim.
- Named confound: ECS as B-cell/TLS proxy; Model 1 adjusts B + TLS + CD8.
- Train/test wall: name primary state in Unit 05 before any ICI phenotype/outcome file.
- Nine ECS genes, neighbor genes out, B/TLS/CD8 lists identical across PROTOCOL / KILL / PLAN.
- Gate A: two lineages; non-B r < 0.6 in pooled TCGA and TCGA-BLCA; residual escape only if SD ratio ≥ 0.5 **and** |r| < 0.75; raw score to Gate B; contamination gene `MS4A1` → `CD19` → `CD79A` (≥ 10% drops a non-B lineage; all three missing ⇒ drop non-B from that dataset).
- Gate B: logistic response Model 1; pass = CI excludes 1 **and** VIF(ECS) < 3; no cutoff search.
- Gate C: CNR2 < 1% (no UMAP atlas) vs stop-kill if enzymes also dark and no non-B state.
- Missing-gene math: available-case mean; denominator = genes present; min 7/9 ECS; never zero-fill.
- Decide table and “do not run Gate B if A fails” match across KILL / PROTOCOL / PLAN / PHASES.
- Deferred work (browser, scGPT, GSE220635, DDI) is in EXPLORE, not in the kill.

**Nits (applied 2026-08-24, do not re-open confirmatory science):**

- Fallback name unified to **TISCH2**.
- IMvigor210 extract pinned as Bioconductor `IMvigor210CoreBiologies` in PROTOCOL / Unit 00.
- QUESTION one-sentence verb is **associate**, matching CLAIMS/PROTOCOL.
- Repo-root `.seal/` links and `units/_template.md` paths corrected.
- Operator packets Units 01–08 written under `units/`.

**Not checked (by design):** data access, gene coverage on IMvigor210, code. That is Unit 00.

## Confirmatory vs exploratory

Until seal: everything is exploratory planning.  
After seal: Operator runs units; new ideas → `EXPLORE.md` or a dated protocol amendment. **Do not edit CONFIRMATORY fields** in `PROTOCOL.md` / `KILL.md` / `CLAIMS.md` except by dated amendment.

## Blockers before Seal

- [x] Analyze pass (consistency) recorded below
- [x] Human reads `CLAIMS.md`, `KILL.md`, `PROTOCOL.md` and agrees
- [x] Seal date + git SHA + “do not edit confirmatory fields” (`3fbf310870c57247163edca35ed536ade3ea4301`)
- [ ] OSF secondary-data prereg URL (public lock; may follow git SHA by a day)

## After seal (execution)

- [x] Unit 00 inventory complete: sources reachable; nine core genes present on IMvigor210 (0 missing); extract pinned (`IMvigor210CoreBiologies_1.0.1.tar.gz`); Census contamination gene `MS4A1`; **no** outcome-vs-ECS plots. See `research/data-inventory.md`.
- [x] Unit 01 Gate C marked by human (`research/01-detection.md`): **pass / continue** (do not stop the kill on detectability). Table complete; stop-kill detection half was false.
- [x] Unit 02 scRNA ECS states complete: `research/02-scrna-states.md`. Candidates: B/plasma, Malignant/epithelial, Stromal/other. Two-lineage rule holds. No ICI files. **Next:** Unit 03 freeze markers.
