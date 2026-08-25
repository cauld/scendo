# STATUS

**Study:** SCENDO  
**Flow:** [`.seal/E2E_FLOW.md`](.seal/E2E_FLOW.md) (generic) · [`E2E_FLOW.md`](E2E_FLOW.md) (this study)  
**Protocol seal:** **SEALED 2026-08-24**  
**Confirmatory git SHA:** `3fbf310870c57247163edca35ed536ade3ea4301` (`3fbf310`)  
**OSF URL:** not yet (public lock may follow this SHA by a day)  
**Current stage:** Kill test **complete**. Primary **Stromal/other**. Gate C **pass / continue**. Gate A **pass**. Gate B **fail**. **Decision: atlas-only; ICI reported negative.** Full paper closed. **Next:** new atlas protocol + new lock (Phase 2b). No ICI fishing.  
**Order / what to run:** [`docs/SEAL-FLOW.md`](docs/SEAL-FLOW.md)  
**Decision:** **atlas-only** (2026-08-24). ICI chapter stays negative. Scribe ≤ `CLAIMS.md`.

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
| 2026-08-24 | Unit 03 freeze markers: nine core ECS genes + 3 lineage buckets in `research/03-frozen-markers.json`; no DE; no ICI files |
| 2026-08-24 | Unit 04 TCGA confound: pooled n=3664 r_B=0.417 r_TLS=0.383; BLCA n=426 r_B=0.361 r_TLS=0.263; both |r| < 0.6; both non-B candidates qualify; no residual; no ICI files |
| 2026-08-24 | Unit 05 primary named **Stromal/other** (cascade step 2: 5 types vs 4). Gate A numbers hold; human marks Gate A. No ICI files |
| 2026-08-24 | Human Gate A: **pass**. Primary **Stromal/other** frozen. Unit 06 IMvigor210 next |
| 2026-08-24 | Unit 06 IMvigor210: Model 1 n=298 ECS OR 1.189 (0.551–2.563) CI includes 1; VIF(ECS)=1.36. Operator Gate B numbers fail. Human marks Gate B |
| 2026-08-24 | Human Gate B: **fail**. Unit 07 melanoma GEO next (report only) |
| 2026-08-24 | Unit 07 GSE78220 n=26 ECS OR 0.47 (0.02–11.7); GSE91061 n=49 ECS OR 0.60 (0.07–5.51); both CIs include 1. Does not rescue Gate B |
| 2026-08-24 | Unit 08 Converge: protocol lock and outcome wall hold. Mapped Decide: **atlas-only; ICI negative**. Human Decide next |
| 2026-08-24 | **Decide: atlas-only.** ICI reported negative. Full paper closed. Next: Phase 2b atlas protocol (new lock; no ICI fishing) |

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
- [x] Unit 02 scRNA ECS states complete: `research/02-scrna-states.md`. Candidates: B/plasma, Malignant/epithelial, Stromal/other. Two-lineage rule holds. No ICI files.
- [x] Unit 03 freeze markers complete: `research/03-frozen-markers.json`. Marker list = nine core genes + B/plasma, Malignant/epithelial, Stromal/other. No DE.
- [x] Unit 04 TCGA confound complete: `research/04-tcga-confound.md`. Both non-B candidates qualify (pooled and BLCA |r| < 0.6). Residual not used.
- [x] Unit 05 primary named: `research/05-primary-state.md`. **Stromal/other**. Cascade step 2 (present in more of the five types). Human Gate A: **pass**. Frozen in git before Unit 06.
- [x] Unit 06 IMvigor210 complete: `research/06-imvigor210.md`. Model 1 n=298 ECS OR 1.189 (0.551–2.563) CI includes 1; VIF(ECS)=1.360. Human Gate B: **fail**.
- [x] Unit 07 melanoma GEO complete: `research/07-melanoma-geo.md`. GSE78220 n=26; GSE91061 n=49. ECS CIs include 1. Cannot rescue Gate B.
- [x] Unit 08 Converge complete: `research/08-converge.md`. Protocol lock and outcome wall hold. Mapped Decide: **atlas-only; ICI reported negative**.
- [x] Human Decide: **atlas-only** (2026-08-24). ICI chapter reported negative. Full paper closed unless a dated amendment reopens Gate B.

## Converge (2026-08-24)

Operator audit vs sealed `KILL.md` / `PROTOCOL.md`. Detail: [`research/08-converge.md`](research/08-converge.md).

| Gate | Operator draft | Human mark |
|---|---|---|
| C detectability | Stop-kill detection half false; no-UMAP-atlas rule false | **Pass / continue** |
| A states ≠ B cells | 3 buckets; both non-B qualify; primary Stromal/other | **Pass** |
| B ICI ≠ confound | Model 1 ECS CI includes 1; VIF(ECS)=1.360 | **Fail** |

GEO, OS, unadjusted, Model 2, and deconvolution cannot rescue Gate B. Confirmatory files were not edited to match figures.

**Mapped Decide (`KILL.md`):** A pass, B fail → **atlas-only; ICI as negative**. Full paper path is closed unless a dated amendment. Scribe ≤ `CLAIMS.md`.

## Human Decide

- [X] Atlas-only (mapped path; ICI chapter reported negative) — marked 2026-08-24
- [ ] Stop (no atlas paper)
- [ ] Full paper — **closed** unless a dated protocol amendment reopens Gate B

## Scribe bound (after Decide)

May say, inside `CLAIMS.md`:

1. Human tumor ECS is visible as **lineage cell states** (nine core genes), not only CB1-brain / CB2-immune slogans.
2. At least one non-B state (**Stromal/other**) is distinguishable from B-cell / TLS abundance on the Gate A tests.
3. The **frozen** Stromal/other score **does not** associate with IMvigor210 **response** after B-cell / TLS / CD8 adjustment (Model 1 ECS OR 1.189, 95% CI 0.551–2.563). OS, unadjusted, Model 2, deconvolution, and melanoma GEO do not carry this claim.

Must not say: cannabis/CBD treats cancer; CB2 **is** a clinical checkpoint; patients should change cannabis during PD-1; melanoma GEO validates a biomarker; an OS-only or unadjusted signal is a checkpoint association.

**Next (Phase 2b):** new protocol + new lock for a census-scale map. Do not reopen ICI outcomes to hunt a pass. GSE220635 / browser / scGPT stay out until that protocol names them.
