# SCENDO kill-test plan (external review)

**Study:** SCENDO — Single-Cell ENDOcannabinoidome (host tissues and tumor microenvironment).  
**Stage:** Protocol **DRAFT**, not sealed. No ICI outcome-vs-ECS analysis has been run.  
**Audience:** Independent reviewer (stats / computational oncology / immunology).  
**Ask:** Can this protocol be frozen as a secondary-data preregistration, or must it change first?

**Source of truth:** `PROTOCOL.md` and `KILL.md`. This brief restates them. If anything here disagrees with those files, **those files win**. Related: `QUESTION.md`, `CLAIMS.md`.

**What we are not asking you to bless:** atlas browser, scGPT, GSE220635 CBD×PD-1, FAERS/DDI, wet lab, or a clinical guideline.

---

## 1. Question and claims

**Question.** Where does the human endocannabinoid system sit at single-cell resolution, and do those cell states associate with PD-1/PD-L1 **response** after accounting for B cells (and TLS / CD8)?

**If gates pass, we may say:**

1. The ECS is a small set of **cell states** (receptors + enzymes) in public scRNA, not only “CB1 brain / CB2 immune.”
2. At least one of those states is distinguishable from **B-cell / TLS abundance**.
3. A **frozen** state score, defined with no ICI labels, either **does** or **does not** associate with IMvigor210 **response** after B-cell + TLS + CD8 adjustment.

**We will not say:** cannabis treats cancer; CB2 is a clinical checkpoint; patients should start or stop cannabis on pembrolizumab; melanoma n≈28 “validates a biomarker”; an OS-only, unadjusted-only, or deconvolution-only result is the confirmatory association.

A clean **negative** on (3) is still a complete v1 paper if (1)–(2) hold (atlas-only path).

**Named confound.** Tumor *CNR2* / ECS scores are often a **B-cell / TLS** proxy. B cells already predict better ICI in several cancers. That is the alternative explanation this kill test is built to kill or confirm.

---

## 2. Design in one picture

```
scRNA (Census; TISCH2 fallback)  →  define lineage ECS states   [no ICI labels]
        ↓
TCGA bulk                       →  Gate A: not just B/TLS
        ↓
Name ONE primary non-B state    →  freeze in git              [still no ICI labels]
        ↓
IMvigor210 response             →  Gate B: Model 1 logistic
        ↓
GSE78220 / GSE91061             →  report only
        ↓
Human Decide                    →  stop / atlas-only / full paper
```

Train/test wall: states and the primary-state **name** are locked before any IMvigor210 or GEO **phenotype/outcome** file is opened.

---

## 3. Frozen objects (before any ICI outcome)

**ECS genes (confirmatory, n = 9):**  
`CNR1, CNR2, GPR55, TRPV1, FAAH, MGLL, DAGLA, DAGLB, NAPEPLD`

Neighbors (`GPR18, GPR119, TRPV2, ABHD6, ABHD12`) are exploratory and stay out of the kill.

**Adjustment signatures:**

| Signature | Genes |
|---|---|
| B cell | `MS4A1, CD19, CD79A, CD79B, MZB1` |
| TLS | `CXCL13, CCL19, CCL21, CCR7` |
| CD8 / cytotoxicity | `CD8A, CD8B, GZMB, PRF1, IFNG` |

**Scoring.** scRNA: mean of the nine genes inside an existing lineage bucket (no NMF, no new clustering, no DE). Bulk: **available-case mean** of gene-wise z-scores, z-scored **within the cohort used for that model**. Denominator = genes present for that sample, never the full list with zeros. Sample scored only if ≥7/9 ECS genes (B ≥3/5, TLS ≥3/4, CD8 ≥3/5). Continuous score is the test statistic. Median split is display-only. No AUC/Youden/tertile search on outcomes.

**Lineage buckets (substring map, first match):** B/plasma; myeloid; T/NK; malignant/epithelial; stromal/other. Census is the primary scRNA source; TISCH2 is used only if Census lacks that cancer type. One source per type.

**B-contamination (per scRNA dataset):** drop a non-B lineage if detection ≥ 10% for the first present of `MS4A1`, then `CD19`, then `CD79A`. If all three genes are absent in that dataset, discard all non-B lineages from that dataset. B/plasma is not filtered. One confirmatory state per lineage bucket (myeloid subtypes are pooled).

---

## 4. Gates (human pass/fail)

### Gate C — detectability (Unit 01)

Report % cells with count > 0 for *CNR2*, *MGLL*, *FAAH* by lineage and cancer type.

- No raw-*CNR2* UMAP atlas if *CNR2* < 1% in every non-B lineage in every type.
- **Stop the kill** if that is true **and** *MGLL* and *FAAH* are both < 5% in every non-B lineage in every type **and** no non-B ECS state exists.

### Gate A — not only B cells (Units 02–04)

**Pass only if both:**

1. At least **two** lineage buckets have an ECS state (a lone myeloid or T/NK state is not a pass).
2. At least one **non-B** state (after the contamination filter) has Pearson |r| < 0.6 vs B-cell **and** vs TLS in **concatenated** TCGA (available types among NSCLC, SKCM, CRC, BRCA, BLCA) **and** in **TCGA-BLCA**. Spearman is reported, not the pass metric.

**Residual escape (Gate A only), now capped:** if a Pearson test fails, `raw_score ~ B + TLS` on **that same cohort** may still qualify the state iff **both** residual SD / raw SD ≥ 0.5 **and** `|r_B| < 0.75` and `|r_TLS| < 0.75`. If either |r| ≥ 0.75, no escape (closes the |r|≈0.87 / VIF≈4 leak). **Gate B always uses the raw score.** Residual does not become the ICI predictor.

If Gate A fails, **do not run Gate B** as a checkpoint test. Optional honest “CB2-high B cell” atlas is a different, later protocol.

### Gate B — ICI association is not the confound (Unit 06)

**Cohort:** IMvigor210 (atezolizumab, urothelial; ~300 with RNA).  
**Kill endpoint:** response, CR/PR vs SD/PD. Drop NE/NA.  
**OS:** pre-specified secondary; **cannot** pass or rescue Gate B.

**Model 1 (the only kill model):**

`response ~ ECS_raw + B_cell + TLS + CD8` (logistic). Report OR and 95% CI.

**Pass:** Model 1 ECS CI excludes 1 **and** VIF(`ECS_raw`) **< 3.0** (report VIF for all four terms; no term dropping).  
**Cannot pass or rescue:** unadjusted model, Model 2 (+ TMB + PD-L1 IC), OS, deconvolution, secondary states, melanoma GEO. VIF(ECS) ≥ 3 is a Gate B **fail** (not interpretable as independent of the confound), even if the CI excludes 1.

**Replication (Units 07, underpowered):** GSE78220, GSE91061. Same frozen objects. Report only.

---

## 5. How the primary state is named (Unit 05)

Named **after** Gate A numbers exist and **before** outcome files are opened.

Among qualifying non-B **buckets** (not subtypes): lowest `max(|r_B|, |r_TLS|)` on pooled **raw** Pearson. Tie: present in more of the five cancer types. Tie: myeloid > T/NK > malignant > stromal. Tie: higher mean core-ECS score across types where present. Tie: larger cell *n*. Tie: ASCII bucket name.

Commit: name, lineage, nine genes, four Pearson r values (B/TLS × pooled/BLCA), residual ratios if used, contamination gene per dataset, contamination rates, tie-breaker step.

---

## 6. Execution sequence

| Step | When | What | Must not |
|---|---|---|---|
| Analyze | Now | Read-only consistency across artifacts | Change confirmatory fields to taste after seeing data (there are no outcome analyses yet) |
| Unit 00 | **Before Seal** | Access, licenses, file pins, gene coverage | Peek ICI labels; plot outcome vs ECS |
| Seal | Human | git SHA + OSF secondary-data prereg | Edit confirmatory fields afterward except dated amendment |
| Unit 01 | After Seal | Gate C detection table | — |
| Unit 02 | After 01 | Lineage ECS states | Open ICI outcomes |
| Unit 03 | After 02 | Freeze nine genes + lineage in git | Add genes |
| Unit 04 | After 03 | TCGA r and residual tests | — |
| Unit 05 | After 04 | Name primary state | Open ICI outcomes first |
| Unit 06 | After 05 + Seal | IMvigor210 Model 1 | New ECS genes; cutoff search; treat OS as the kill |
| Unit 07 | After 06 | Melanoma GEO | Rescue Gate B here |
| Unit 08 | After 06–07 | Converge; human Decide | Rewrite the protocol to match figures |

Compute: laptop, Python (`pipeline/`). R only to export IMvigor210 if needed.

**Decide:**

| Result | Next |
|---|---|
| A and B pass | Full paper path; ICI analysis stays frozen |
| A pass, B fail | Atlas-only; ICI reported negative |
| A fail | Stop or B-cell/ECS descriptive; no checkpoint claim |
| A and B fail | Stop |

---

## 7. Leniencies we already accepted (please challenge if you disagree)

These are deliberate, not accidents:

1. **Residual hatch is capped.** Residual SD ratio ≥ 0.5 is not enough; raw Pearson |r| vs B and vs TLS must also be **< 0.75**. That keeps pairwise VIF from a single confounder ≲ 2.3. Gate B still uses the **raw** score plus a VIF(ECS) < 3 pass rule.
2. **“Highest or second-highest” lineage mean** plus ubiquitous *MGLL*/*FAAH* makes “an ECS state exists” easy. The real Gate A knife is the TCGA r / contamination tests.
3. **No multiplicity correction** on a single primary state × one kill endpoint (response). Secondary states use Holm–Bonferroni and cannot pass Gate B.
4. **Pooled TCGA is concatenated samples** (BRCA can dominate n). BLCA-alone is required because IMvigor210 is urothelial.
5. **Missing ≤2 / 9** core genes on IMvigor210 is allowed. Score = mean of **available** gene-wise z-scores (denominator = genes present). Missing two genes → mean of seven z-scores, not mean of nine with zeros. Missing >2 core genes on IMvigor210 blocks Seal / Gate B.

---

## 8. Reviewer checklist

External review (2026-08-24) marked **ok** on all items except residual hatch and missing-gene math; those two are now locked as in §7.1 and §7.5 / `PROTOCOL.md`. Remaining checklist is historical.

- [x] Question and non-claims  
- [x] Named confound (B-cell/TLS proxy)  
- [x] Train/test wall  
- [x] Nine-gene list and adjustment sets  
- [x] Gate A: two-lineage + |r| < 0.6 + BLCA + contamination  
- [x] Residual hatch — **changed:** |r| < 0.75 ceiling + VIF(ECS) < 3 at Gate B  
- [x] Gate B: response-only Model 1; OS secondary  
- [x] Continuous score; no cutoff optimization  
- [x] Deconvolution and melanoma GEO cannot rescue Gate B  
- [x] Unit 00 before Seal  
- [x] Decide table  
- [x] Missing-gene math — **changed:** available-case mean, min 7/9, never zero-fill  

**Out of scope for this review:** code quality, cluster compute, paper figures, browser UX.

---

## 9. What happens after you reply

If you request changes, we amend `PROTOCOL.md` / `KILL.md` **before Seal** and record them in `STATUS.md`.  
If you sign off, a human seals: git SHA + OSF [secondary data preregistration](https://osf.io/registries/osf/drafts/new?form=secondary-data-preregistration), disclosing prior knowledge of these public datasets and that confirmatory outcome-vs-predictor plots were **not** used to choose the model.

Then Units 01–08 run as written. New ideas go to `EXPLORE.md` or a dated amendment — they do not silently rewrite Gate B.
