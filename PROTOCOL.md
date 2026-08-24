# PROTOCOL (kill phase)

**Seal status:** DRAFT. After seal, do not edit sections marked CONFIRMATORY without a dated amendment in `STATUS.md`.

This protocol is **only the kill test**. Atlas-scale integration, browser, and paper figures beyond Gates A–C require a new sealed protocol.

Human-readable brief for external review: [`PLAN.md`](PLAN.md). If PLAN and this file ever disagree, **this file wins**.

## CONFIRMATORY — ECS gene list (freeze at seal)

Core (must score; confirmatory list is **only** these nine):

`CNR1, CNR2, GPR55, TRPV1, FAAH, MGLL, DAGLA, DAGLB, NAPEPLD`

**Neighbors not in the kill.** `GPR18, GPR119, TRPV2, ABHD6, ABHD12` stay in `EXPLORE.md`. Do not add them after seeing ICI results.

Do not add genes because they predict IMvigor210.

**Missing genes (math is confirmatory).** Map to HGNC symbols (record aliases in Unit 00).

- **Cohort-level:** if a gene is absent from the matrix (or NA for every sample), drop it from that cohort’s signature for **all** samples and record the drop. If **more than two** core ECS genes are missing from IMvigor210, do not Seal (if still draft) and do not run Gate B (if already sealed); amend or stop.
- **Score:** available-case mean of **within-cohort gene-wise z-scores**. For sample *i*, let *G_i* be the signature genes with non-missing values for that sample.  
  `score_i = mean({z_ig : g ∈ G_i})`.  
  The denominator is `|G_i|`, **not** the full list length. Do **not** impute missing as 0, as the gene-wise mean, or as any other fill. Z-score each gene using samples that have that gene in the same cohort.
- **Same rule** for B-cell, TLS, and CD8 signatures.
- **Minimum genes to emit a score:** ECS `|G_i| ≥ 7`; B cell `≥ 3` of 5; TLS `≥ 3` of 4; CD8 `≥ 3` of 5. Samples below a minimum are dropped from models that use that score; report n dropped.
- **Worked example (reviewer question):** IMvigor210 sample missing exactly two core ECS genes (cohort-wide or sample-wise) → score = mean of the **seven** remaining gene-wise z-scores. Denominator = 7, not 9.

## CONFIRMATORY — dataset roles

| Role | Dataset | Allowed |
|---|---|---|
| Define states | Human tumor scRNA. **Primary source:** CELLxGENE Census. **Fallback:** TISCH2 only for a cancer type Census lacks. One source per cancer type; do not mix annotations within a type. Types: NSCLC, melanoma, CRC, BRCA, BLCA. | Cell types, ECS programs. **No ICI labels.** Need **≥2** of the five types or amend before Unit 02. |
| Confound in bulk | TCGA (LUAD+LUSC, SKCM, COAD+READ, BRCA, BLCA) | Correlation / residual vs B-cell and TLS signatures |
| **Primary ICI** | IMvigor210 (Bioconductor `IMvigor210CoreBiologies`, or the exact extract pinned in Unit 00) | Score **frozen** states; fit **no** new ECS genes |
| Replication ICI | GSE78220, GSE91061 (pre-treatment melanoma anti-PD-1) | Same frozen objects. Small n. Descriptive; not a Gate B rescue |
| Do not use as primary | GSE93157 nCounter | Core ECS genes not on that panel |

## CONFIRMATORY — signatures for adjustment

Locked lists (no substitution after seal):

- B cell: `MS4A1, CD19, CD79A, CD79B, MZB1`
- TLS: `CXCL13, CCL19, CCL21, CCR7`
- CD8 / cytotoxicity: `CD8A, CD8B, GZMB, PRF1, IFNG`

Optional deconvolution (CIBERSORTx or BayesPrism) is **exploratory**. It does **not** flip Gate B from fail to pass.

## CONFIRMATORY — lineage buckets

Assign each cell to one bucket from existing labels (Census `cell_type` or TISCH2 major/minor). Case-insensitive substring match, first match in this order:

| Bucket | Label contains (examples) |
|---|---|
| B/plasma | `b cell`, `b-cell`, `plasma`, `plasmablast`, `plasmacyte` |
| Myeloid | `monocyte`, `macrophage`, `myeloid`, `dendritic`, `neutrophil`, `mast`, `granulocyte`, `kupffer` |
| T/NK | `t cell`, `t-cell`, `cd4`, `cd8`, `treg`, `nk cell`, `natural killer`, `ilc`, `nkt`, `gamma-delta`, `gd t`, `thymocyte` |
| Malignant/epithelial | `malignant`, `tumor cell`, `cancer cell`, `epithelial`, `keratinocyte`, `pneumocyte`, `enterocyte`, `hepatocyte`, `urothelial` |
| Stromal/other | `fibroblast`, `endothelial`, `pericyte`, `smooth muscle`, `myofibroblast`, `stroma`; **and any unmatched label** |

Cycling/proliferating cells follow the parent lineage if labeled (e.g. TISCH2 `Tprolif` → T/NK); otherwise Stromal/other. In tumor datasets, epithelial → Malignant/epithelial.

## CONFIRMATORY — scoring (freeze at seal)

- **scRNA states:** existing annotations only. No NMF, no new clustering. A **state** is the mean of the nine core genes inside one lineage bucket. Those nine genes **are** the marker list (Unit 03 commits lineage + the nine genes; no DE).
- **A lineage has an ECS state** if, in ≥1 cancer type, at least one core gene is detected (count > 0) in ≥5% of that lineage’s cells **and** the lineage mean core-ECS score is elevated vs other lineages in that dataset (highest or second-highest). A lineage is **present** in a cancer type when this rule holds in that type.
- **B-contamination (replaces a DE “top markers” check):** a non-B lineage is discarded (does not count toward Gate A) if `MS4A1` detection (count > 0) in that lineage is **≥ 10%** in the same dataset. B/plasma is not subjected to this filter.
- **Bulk scores:** z-score **within the cohort used for that analysis** (TCGA pooled, TCGA-BLCA, IMvigor210, and each GEO set are separate z-score windows). Use the cohort’s shipped matrix, or log2(TPM+1). Sample score = mean of gene-wise z-scores. Same rule for ECS states and for B/TLS/CD8 signatures.
- **TCGA pooled:** concatenate samples from the available types among the five (BRCA may dominate n; that is why BLCA is also required). Report per-type Pearson r as descriptive. **Pooled Pearson** = Pearson on the concatenated matrix, not the average of per-type r.
- **Primary estimator:** the **continuous raw** score. Median split is display-only. No tertiles, Youden, ROC, or AUC-chosen cutoffs on ICI outcomes.

## CONFIRMATORY — Gate C (detection)

Unit 01 reports % cells with count > 0 for `CNR2`, `MGLL`, `FAAH` by lineage bucket and cancer type.

- **No raw-CNR2-UMAP atlas** if `CNR2` detection is **< 1%** in every non-B/plasma lineage in every available cancer type.
- **Gate C fail (stop the kill):** that CNR2 condition **and** `MGLL` and `FAAH` both **< 5%** in every non-B/plasma lineage in every type **and** no non-B lineage has an ECS state. Then stop or leave programs/deconvolution to a new protocol.
- Low *CNR2* in T/NK is not by itself a kill.

## CONFIRMATORY — primary state rule (name after Gate A, before ICI outcomes)

Do **not** name the primary state at seal. Name it in Unit 05 after Units 02–04, **before** any IMvigor210 or GEO phenotype/outcome file is opened.

**Gate A requires both:** (i) at least **two** lineage buckets have an ECS state; (ii) at least **one non-B** candidate qualifies on the confound tests below. A single non-B lineage, even with r < 0.6, is **not** a Gate A pass.

Procedure:

1. List lineage buckets that have an ECS state and pass the `MS4A1` contamination filter.
2. Gate A fails if fewer than two buckets remain (including B/plasma).
3. Non-B candidates = remaining buckets except B/plasma.
4. In TCGA, score each non-B candidate with the **raw** nine-gene mean z-score. **Pearson** |r| vs B-cell and vs TLS must both be **< 0.6** in (a) pooled TCGA and (b) **TCGA-BLCA**. Spearman is reported, not the pass metric. If BLCA RNA is unavailable, amend before Gate B.
5. **Residual is a Gate A qualification test only, with a hard |r| ceiling.** If Pearson |r| ≥ 0.6 vs B or vs TLS in pooled, residualize `raw_score ~ B_cell + TLS` on **pooled** samples. That cohort is rescued iff **both** (i) residual SD / raw SD **≥ 0.5** and (ii) Pearson `|r_B| < 0.75` **and** `|r_TLS| < 0.75` on that same cohort (raw score). If Pearson fails in BLCA, repeat on **BLCA only** with the same two conditions. If either |r| is **≥ 0.75**, there is **no** residual escape for that cohort. A candidate qualifies only if every failed Pearson test is rescued on that same cohort. **Gate B always uses the raw continuous score**, never the residual. Model 1 does the adjustment.
6. If several non-B candidates qualify, primary = lowest `max(|r_B|, |r_TLS|)` using Pearson on **pooled raw** scores. Tie: present (ECS-state rule) in more of the five cancer types. Tie: myeloid > T/NK > malignant/epithelial > stromal/other.
7. Commit in Unit 05: name, lineage bucket, the nine genes, the **four** Pearson values (`r_B_pooled`, `r_TLS_pooled`, `r_B_BLCA`, `r_TLS_BLCA`), residual SD ratios if used, and contamination rates.
8. If no non-B candidate qualifies, **Gate A fails**. Do not run Gate B as a checkpoint test.

Secondary non-B states may be scored later; they cannot pass Gate B.

## CONFIRMATORY — statistics (primary)

**Kill endpoint (Gate B):** IMvigor210 **response**, CR/PR vs SD/PD as coded in the extract. Drop NE/NA from the logistic model.

**Secondary (not a Gate B pass):** Cox OS (time + censor as shipped). PFS only if the extract includes it; also secondary.

**Gate B models** (primary state, **raw** continuous score):

- **Model 1 (kill):** `response ~ ECS_state + B_cell + TLS + CD8` (logistic)
- **Model 2 (robustness):** Model 1 + TMB + PD-L1 IC when those columns exist. Complete cases; report n. Sex/age if present and complete for the same n.
- Report unadjusted `response ~ ECS_state`. It is **neither necessary nor sufficient** to pass.

Logistic: OR and 95% CI. Cox: HR and 95% CI (secondary).

**Collinearity (confirmatory).** Before interpreting Model 1, compute VIF for `ECS_state`, `B_cell`, `TLS`, and `CD8` on the Model 1 complete-case table. Report all four. Model 1 is always fit as specified (no term dropping).

**Gate B pass:** Model 1 ECS term 95% CI excludes the null (**OR ≠ 1**) **and** VIF(`ECS_state`) **< 3.0**. If VIF(`ECS_state`) ≥ 3, Gate B **fails** (coefficient not interpretable as independent of the confound), even if the CI excludes 1. OS, Model 2, unadjusted, secondary states, deconvolution, and melanoma GEO **cannot** rescue a failed Model 1.

**Secondary states:** Holm–Bonferroni across those states × {response, OS}. Cannot rescue Gate B.

**Replication.** Same frozen objects and Model 1 covariates if available. Report only.

## CONFIRMATORY — pass/fail

See `KILL.md`. Kill bar is Gate A (two lineages + confound tests, residual escape only if |r| < 0.75) and Gate B (Model 1 response CI **and** VIF(ECS) < 3), not a clinical AUC target.

## How (operational, not outcome-fitted)

- Code: **Python**, one folder `pipeline/`. Unit 00 may use R only to export Bioconductor `IMvigor210CoreBiologies` to CSV/Parquet, then Python thereafter.
- Compute: laptop. No Spark, no scGPT, no browser.
- Gene aliases (non-exhaustive): *CNR2*/*CB2*, *MGLL*/*MAGL*, *DAGLA*/*DAGLα*, *DAGLB*/*DAGLβ*.
- **Unit 00 (no outcome peek) is a Seal blocker:** pin exact files; confirm the nine core genes on Census/TISCH2, TCGA, IMvigor210, and both GEO matrices.

## Positive control (after Decide, not kill)

GSE220635 (CBD, macrophage polarization, PD-1). Do not use to redefine the sealed gene list.

## Amendments

| Date | Change |
|---|---|
| 2026-08-24 | Clarify: core-nine only; continuous primary score; Unit 05 naming rule; locked signatures/covariates; cluster-mean + mean z-score; deconvolution not a Gate B rescue |
| 2026-08-24 | Patch after validation: Gate B = Model 1 **response** only; unadjusted not required; residual = Gate A only; two lineages required; no DE (nine-gene mean + MS4A1 contamination); Census primary / TISCH2 fallback; within-cohort z-score; pooled = concatenated samples; Gate C numeric; Unit 00 before Seal |
| 2026-08-24 | Analyze nits: unify fallback name to TISCH2; pin IMvigor210 extract as Bioconductor `IMvigor210CoreBiologies` |
| 2026-08-24 | External review: residual escape also requires |r| < 0.75 vs B and vs TLS; Gate B pass also requires VIF(ECS) < 3; missing-gene score = available-case mean (denominator = genes present; min 7/9 ECS); never zero-fill |
