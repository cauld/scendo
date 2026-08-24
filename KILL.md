# KILL

**Purpose.** Stop or shrink the project before an atlas, browser, or Spark training. Human-owned pass/fail.

**Named confound.** *CNR2* / ECS scores are a proxy for B cells and tertiary lymphoid structures.

## Gate A — states are not only B cells

**Data:** Tumor scRNA (CELLxGENE Census; TISCH2 fallback), then TCGA bulk for correlation.

**Pass if all hold:**

- At least **two** ECS-defined states in **different** lineage buckets (B/plasma, myeloid, T/NK, malignant/epithelial, stromal/other). A single non-B lineage is not a pass.
- At least one **non-B** candidate survives the **contamination filter** and the confound tests. Contamination is per scRNA dataset: detection < 10% of the contamination gene in that lineage. Contamination gene = first present of `MS4A1`, `CD19`, `CD79A`. If all three are absent in that dataset, all non-B lineages from that dataset are discarded (untestable). Pearson |r| vs the B-cell signature (*MS4A1, CD19, CD79A, CD79B, MZB1*) and vs the TLS signature (*CXCL13, CCL19, CCL21, CCR7*) is **< 0.6** in concatenated pooled TCGA **and** in TCGA-BLCA. If a Pearson test fails, residual escape on **that same cohort** requires **both** residual SD / raw SD ≥ 0.5 **and** `|r_B| < 0.75` and `|r_TLS| < 0.75` (raw Pearson). If either |r| ≥ 0.75, no escape. The **raw** score still goes to Gate B. Spearman is reported, not the pass metric.
- Marker list is the nine core ECS genes (no DE). Immunoglobulin / B-lineage identity is the contamination filter above (`MS4A1` → `CD19` → `CD79A`), not a top-marker table.

**Fail:** Fewer than two lineage states, every non-B state is B-contaminated, or no non-B candidate passes the confound tests.

**If fail:** ICI “checkpoint” pitch dies. Optional atlas-only path only if cell-type structure is still clean (honest CB2-high B-cell state allowed as a named state, not as a new checkpoint). **Do not run Gate B** as a checkpoint test.

## Gate B — ICI association is not the confound

**Discovery:** ECS states from scRNA **only**. No ICI outcomes. Freeze the nine-gene + lineage objects in git (Unit 05) before opening outcome files.

**Primary confirmatory set:** IMvigor210 (atezolizumab, urothelial; ~300 with RNA). States never trained on these labels.

**Kill endpoint:** binary **response** (CR/PR vs SD/PD). OS is secondary and cannot pass or rescue Gate B.

**Model 1 (kill):** `response ~ ECS_state + B_cell + TLS + CD8` (continuous **raw** frozen score). TMB + PD-L1 IC is robustness only.

**Pass:** Model 1 ECS 95% CI excludes the null (OR ≠ 1) **and** VIF(`ECS_state`) **< 3.0** (VIF computed on the Model 1 complete-case table; report VIF for ECS, B, TLS, CD8). Unadjusted ECS is reported; it is neither necessary nor sufficient. Deconvolution, Model 2, OS, secondary states, and melanoma GEO do not rescue a fail.

**Fail:** Model 1 CI includes 1, **or** VIF(`ECS_state`) ≥ 3 (coefficient not interpretable as independent of the confound).

**Replication (underpowered, not the kill):** GSE78220, GSE91061. Report; do not rescue a failed Gate B by hunting cutoffs here.

## Gate C — detectability

Census (TISCH2 fallback): *CNR2*, *MGLL*, *FAAH* detection (% cells with count > 0) by lineage bucket.

**No raw-*CNR2*-UMAP atlas:** *CNR2* detection **< 1%** in every non-B/plasma lineage in every available cancer type.

**Gate C fail (stop the kill):** that CNR2 condition **and** *MGLL* and *FAAH* both **< 5%** in every non-B lineage in every type **and** no non-B ECS state. Then stop, or move programs/deconvolution to a new protocol.

**Not a kill:** Low *CNR2* in T cells if ISH literature still supports a rare CB2+ T/NK state — but then you may not sell scRNA *CNR2* as the T-cell checkpoint readout.

## Decide (after gates)

| Result | Decision |
|---|---|
| A and B pass | Full SCENDO paper path |
| A pass, B fail | Atlas-only; ICI as negative |
| A fail (do not run B as checkpoint) | Stop or reframe as B-cell/ECS descriptive; **do not** claim a new checkpoint |
| A and B fail | Stop |

The “A fail, B pass” row is counterfactual. If Gate A failed, Gate B was not a confirmatory checkpoint test.

## Explicitly not in the kill

DDI/FAERS/CYP (idea 3). GSE220635 CBD×PD-1 (positive-control, after Decide). Fine-tuning scGPT. A public browser.
