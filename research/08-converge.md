# Unit 08 — Converge

**Run date:** 2026-08-24  
**Protocol SHA:** `3fbf310870c57247163edca35ed536ade3ea4301`  
**Rule:** Compare Units 01–07 to the sealed protocol. Draft gate scores. Map to Decide. Do not rewrite confirmatory fields. Do not promote OS / GEO / deconvolution to the confirmatory claim. Human Decide is separate.

## Protocol lock

- Seal commit: `3fbf310` (2026-08-24). `PROTOCOL.md`, `KILL.md`, `CLAIMS.md`, `QUESTION.md` have **no** commits after that SHA.
- Frozen objects: `research/03-frozen-markers.json` and `research/05-primary-state.md` in `21be9bd` (Units 03–05, Gate A pass, primary **Stromal/other**).
- ICI outcomes first appear in `c1a47f9` (Units 06–07). That commit is **after** `21be9bd`. Outcome wall holds.

## Locked lists and scoring

| Check | Result |
|---|---|
| Nine core ECS genes | Unchanged: `CNR1, CNR2, GPR55, TRPV1, FAAH, MGLL, DAGLA, DAGLB, NAPEPLD` |
| Neighbors (`GPR18, GPR119, TRPV2, ABHD6, ABHD12`) | Not added. Still in `EXPLORE.md` |
| B / TLS / CD8 lists | Identical to `PROTOCOL.md` / `pipeline/genes.py` |
| Contamination gene | First present of `MS4A1` → `CD19` → `CD79A`. Census and BLCA used **MS4A1**. 0 non-B discards |
| Missing-gene math | Available-case mean of within-cohort gene-wise z-scores (ddof=0). Denominator = genes present. Min 7/9 ECS, 3/5 B, 3/4 TLS, 3/5 CD8. Never zero-fill |
| IMvigor210 gene coverage | 9/9 ECS; 0 samples dropped for gene minima |
| Primary estimator | Continuous **raw** nine-gene score. No median / Youden / ROC / AUC cutoff search |
| Deconvolution | Not run. Cannot rescue Gate B |

scRNA states (Units 01–02) used available-case means of **raw counts** inside locked lineage buckets. No NMF, clustering, or DE. Bulk windows (Units 04, 06, 07) used within-cohort z-score means, as sealed.

## Outcome wall

Units 00–05 notes and research files record **no** IMvigor210 or GEO phenotype/outcome values. Unit 05 named **Stromal/other** and was committed (`21be9bd`) before Unit 06 opened `cds` phenotypes. Unit 07 used the same frozen name and gene list.

## Gate drafts (human already marked)

### Gate C — detectability (Unit 01)

- CNR2 < 1% in every non-B lineage in every type: **False** (melanoma myeloid 19.01%, T/NK 16.02%, stromal 5.42%). No-UMAP-atlas rule does **not** fire.
- MGLL < 5% in every non-B lineage in every type: **False**
- FAAH < 5% in every non-B lineage in every type: **False**
- Detection half of stop-kill: **False** → stop-kill cannot fire on detectability.
- Human Gate C: **pass / continue** (2026-08-24)

### Gate A — states are not only B cells (Units 02–05)

- Lineage buckets with an ECS state: **3** (B/plasma, Malignant/epithelial, Stromal/other)
- Two-lineage rule: **True**
- Non-B candidates that qualify: both (pooled n=3664 r_B=0.417 r_TLS=0.383; BLCA n=426 r_B=0.361 r_TLS=0.263; both \|r\| < 0.6)
- Residual escape: **not used**
- Cascade: step 1 tied (same nine-gene bulk score); step 2 named **Stromal/other** (present in 5 types vs 4)
- Human Gate A: **pass** (2026-08-24)

### Gate B — ICI association is not the confound (Unit 06)

- Model 1 n=298. ECS OR **1.189 (0.551–2.563)**. CI **includes 1**.
- VIF(ECS)=**1.360** (< 3). VIF(B)=5.330 and VIF(TLS)=4.686 are reported; they are not the kill metric.
- Operator numbers hold: **False**
- Unadjusted OR 1.076 (0.568–2.038); Model 2 n=234 ECS OR 1.093 (0.449–2.663); Cox OS n=348 ECS HR 0.898 (0.623–1.294). None of these can pass or rescue.
- Human Gate B: **fail** (2026-08-24)

### Replication (Unit 07; cannot rescue)

- GSE78220 n=26 ECS OR 0.47 (0.02–11.7). CI includes 1.
- GSE91061 n=49 ECS OR 0.60 (0.07–5.51). CI includes 1.

## Decide map (`KILL.md`)

| Kill result | Decision |
|---|---|
| A and B pass | Full paper path — **closed** |
| **A pass, B fail** | **Atlas-only; ICI reported negative** — mapped path |
| A fail | Stop or B-cell/ECS descriptive; no checkpoint claim — not this case |
| A and B fail | Stop — not this case |

Full paper is closed unless a dated protocol amendment reopens Gate B. The Scribe, after Decide, stays inside `CLAIMS.md`: the map may still be claimed; the frozen IMvigor210 test **does not** associate with response after B/TLS/CD8 adjustment. Do not claim CB2 is a checkpoint, that cannabis treats cancer, or that melanoma GEO validates a biomarker.

Human may still choose **stop** (no atlas paper). That is a product choice, not a gate.

## Human Decide

- [X] Atlas-only (mapped path; ICI chapter reported negative) — marked 2026-08-24
- [ ] Stop (no atlas paper)
- [ ] Full paper — **closed** unless a dated protocol amendment reopens Gate B

Scribe ≤ `CLAIMS.md`: map may be claimed; frozen IMvigor210 Model 1 **does not** associate with response. Do not claim CB2 is a checkpoint. Phase 2b next: new atlas protocol + new lock. No ICI fishing.

## Disclosed operational choices (not amendments)

These were recorded in unit notes. They do not change confirmatory fields.

- IMvigor210 used DESeq size-factor normalized counts, then `log2(norm + 1)`, then within-cohort z-scores. Protocol allows the shipped matrix or `log2(TPM+1)`.
- TCGA pooled window kept all `_primary_disease`-matched sample types, including Solid Tissue Normal.
- Both non-B buckets share the same nine-gene bulk score (no DE). Cascade step 1 is then a tie by construction; step 2 broke it.
- BLCA scRNA (`GSE130001`) has epithelial + stromal only under the locked map (no B/myeloid/T). Census lacked BLCA, so TISCH2 fallback was used as sealed.
- Melanoma Census primary-data n is small relative to the other Census types.

No dated amendment. Nothing moved to `EXPLORE.md` from this unit.

## What was not done

- No edit to `PROTOCOL.md` / `KILL.md` / `CLAIMS.md`.
- No cutoff search. No new ECS genes. No deconvolution. No GSE220635 / browser / scGPT.
- OS, Model 2, unadjusted, secondary states, and GEO were not used to flip Gate B.
- Human Decide is recorded: **atlas-only** (2026-08-24). No atlas protocol drafted in this unit.
