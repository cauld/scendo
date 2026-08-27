# OSF secondary-data preregistration (paste packet)

**Status:** **Public.** https://osf.io/c8kpx · DOI [10.17605/OSF.IO/C8KPX](https://doi.org/10.17605/OSF.IO/C8KPX) (registered 2026-08-24). Not a substitute for the sealed protocol. Paste packet below is historical.  
**Confirmatory SHA (the freeze):** `3fbf310870c57247163edca35ed536ade3ea4301` (2026-08-24)  
**Repo:** https://github.com/cauld/scendo  
**Files that win if anything conflicts:** `PROTOCOL.md`, `KILL.md`, `CLAIMS.md` at that SHA.

This environment cannot log into OSF. A human submits.

## You are submitting AFTER Decide

Confirmatory analyses **have already been run** (Units 06–07 on 2026-08-24; atlas Units 10–14 and Scribe on 2026-08-24/25). Git SHA `3fbf310` is still the protocol freeze: it was committed **before** ICI outcome-vs-ECS models (`21be9bd` named **Stromal/other**; `c1a47f9` is Units 06–07).

OSF now is a **public timestamp of that already-sealed plan**, not a claim that tests remain unrun. Do **not** paste the old “analyses have not been run” integrity sentence as if it were still true on the click date.

**Before click:** your name + ORCID in Authors. In *Knowledge of data*, say the plan was frozen at `3fbf310` before ICI models, and that confirmatory results now exist in the repo (`research/06-imvigor210.md`, `RESULTS.md`).

**Do not create an OSF Project.** [Projects are being retired](https://help.osf.io/article/727-osf-projects-transition). **Add new → Registration** from scratch. Template: **Secondary Data Preregistration**.

Permalink to the freeze: `https://github.com/cauld/scendo/tree/3fbf310870c57247163edca35ed536ade3ea4301`

Done: URL is in `STATUS.md` (https://osf.io/c8kpx). Do not edit CONFIRMATORY protocol fields.

---

The sections below are the **plan as sealed** (still what to paste for research questions, variables, and models). Skip or replace any sentence that says ICI analyses have not been run.

**Confirmatory SHA:** `3fbf310870c57247163edca35ed536ade3ea4301`  
**Files that win if anything conflicts:** `PROTOCOL.md`, `KILL.md`, `CLAIMS.md` at that SHA.

---

## Submit checklist

**Do not create an OSF Project.** [Projects are being retired](https://help.osf.io/article/727-osf-projects-transition) (no new projects after 16 Nov 2026; read-only after 19 Feb 2027). **Registrations and preregistrations are unaffected.** File a registration **from scratch**.

1. Log in at [osf.io](https://osf.io). Use **Add new → Registration** (or [this draft link](https://osf.io/registries/osf/drafts/new?form=secondary-data-preregistration)).
2. When asked “Do you have content in an existing OSF project?” choose **No**.
3. Template: **Secondary Data Preregistration** (or **Preregistration of Secondary Data Analysis**).
4. Attach or paste a GitHub permalink to `cauld/scendo` at commit `3fbf310` (`https://github.com/cauld/scendo/tree/3fbf310870c57247163edca35ed536ade3ea4301`). Files live on GitHub; OSF is only the timestamped plan.
5. Paste the **plan** sections below (questions, variables, models). For Knowledge of data and Statement of integrity, use the **after Decide** wording at the top of this file, not any leftover “analyses have not been run” sentence.
6. Disclose prior knowledge (section *Knowledge of data*).
7. Submit. Paste the public registration URL into `STATUS.md` (STATUS only; do not edit CONFIRMATORY protocol fields).

---

## Study information

### Title

SCENDO: single-cell endocannabinoidome states and immune-checkpoint response after B-cell/TLS adjustment

### Description (OSF landing page)

Secondary-data preregistration for SCENDO (Single-Cell ENDOcannabinoidome). This is a computational study of existing public data only. No new patients.

The study asks where a locked nine-gene endocannabinoid-system (ECS) program sits in human tumor single-cell RNA, whether any non-B-cell lineage state can be distinguished from B-cell and tertiary-lymphoid-structure (TLS) abundance in TCGA, and whether a frozen score of that state associates with atezolizumab response in IMvigor210 after adjustment for B-cell, TLS, and CD8 signatures. Direction of the IMvigor210 association is not pre-specified.

Named confound: tumor CNR2 / ECS scores are often a B-cell/TLS proxy. Gate A (state existence and confound tests) must pass before Gate B (IMvigor210 Model 1) is run as a confirmatory checkpoint test. Overall survival, unadjusted models, deconvolution, secondary states, and melanoma GEO cohorts cannot pass or rescue Gate B. This is not a test of cannabis as cancer therapy.

Protocol files (QUESTION, CLAIMS, KILL, PROTOCOL) are sealed on GitHub at commit 3fbf310870c57247163edca35ed536ade3ea4301. That commit is the freeze. Confirmatory ICI analyses were run after it, as specified; Gate B failed. This OSF record timestamps the sealed plan.

### Authors

Chad Auld — [https://orcid.org/0009-0000-8449-5810]. Correspondence: chadauld@gmail.com.

### Research questions

RQ1. At single-cell resolution in public human tumor scRNA, which lineage buckets carry a nine-gene endocannabinoid-system (ECS) program?

RQ2. Can at least one non-B ECS lineage state be distinguished from B-cell and tertiary-lymphoid-structure (TLS) abundance in TCGA bulk RNA?

RQ3. Does a frozen score of that primary non-B state, defined with no ICI labels, associate with atezolizumab **response** in IMvigor210 after adjustment for B-cell, TLS, and CD8 signatures?

### Hypotheses (NHST, two-sided unless noted)

Framework: frequentist NHST. Kill/pass rules are in `KILL.md` at SHA `3fbf310` (qualitative kill bars, not a clinical AUC target).

**H-A (Gate A).** There exist at least two lineage buckets with an ECS state, and at least one non-B candidate whose Pearson |r| vs the locked B-cell signature and vs the locked TLS signature is < 0.6 in concatenated TCGA **and** in TCGA-BLCA (residual escape only if residual SD/raw SD ≥ 0.5 **and** |r| < 0.75 vs B and vs TLS on that same cohort). Else Gate A fails; Gate B is not run as a checkpoint test.

**H-B (Gate B, confirmatory).** In IMvigor210, logistic Model 1  
`response ~ ECS_raw + B_cell + TLS + CD8`  
has ECS 95% CI excluding OR = 1 **and** VIF(ECS) < 3.0. Failure if the CI includes 1 **or** VIF(ECS) ≥ 3. OS, unadjusted ECS, Model 2, deconvolution, secondary states, and melanoma GEO **cannot** pass or rescue Gate B.

**H-C (Gate C).** Detection of *CNR2*, *MGLL*, *FAAH* by lineage is reported. A raw-*CNR2* UMAP atlas is not claimed if *CNR2* detection is < 1% in every non-B lineage in every type. The kill stops if that is true **and** *MGLL* and *FAAH* are both < 5% in every non-B lineage in every type **and** no non-B ECS state exists.

Direction of the ICI association is **not** pre-specified (two-sided). A clean negative on H-B after Gate A pass is a complete confirmatory result (atlas-only path).

---

## Data description

### Dataset

All data are **existing public** resources. No new patients.

| Role | Source | Use |
|---|---|---|
| Define states | CELLxGENE Census tumor scRNA (TISCH2 only if Census lacks a type). Types: NSCLC, melanoma, CRC, BRCA, BLCA. Need ≥2 types. | Lineage ECS states. **No ICI labels.** |
| Confound | TCGA RNA: LUAD+LUSC, SKCM, COAD+READ, BRCA, BLCA | Pearson/residual vs B and TLS |
| Primary ICI | IMvigor210 (Bioconductor `IMvigor210CoreBiologies` or the extract pinned in Unit 00) | Frozen-score confirmatory test |
| Replication ICI | GEO GSE78220, GSE91061 (pre-treatment melanoma anti-PD-1) | Same frozen objects; report only; not a Gate B rescue |
| Not primary | GSE93157 nCounter | Core ECS genes not on panel |

Cross-sectional tumor transcriptomes (scRNA and bulk). IMvigor210 is a clinical ICI cohort with RNA and response/OS.

### Openness of data

Open/public with standard licenses (Census, TCGA, GEO, Bioconductor). No exclusive access.

### Access to data

- Census: CELLxGENE Census Python API  
- TISCH2: https://tisch.comp-genomics.org/  
- TCGA: Xena or GDC  
- IMvigor210: Bioconductor `IMvigor210CoreBiologies`  
- GEO: GSE78220, GSE91061  

Exact files and gene-coverage pins: Unit 00 → `research/data-inventory.md` (filled 2026-08-24). Protocol SHA: `3fbf310`.

### Date(s) data were accessed

**At seal (2026-08-24):** ICI matrices had not been used for outcome-vs-ECS models. Unit 00 recorded access and gene coverage without response-vs-ECS plots.

**When submitting OSF after Decide:** Census, TCGA, IMvigor210, and GEO files were accessed for the sealed units on 2026-08-24. Primary state was named (`21be9bd`) before ICI models (`c1a47f9`). Disclose that in Knowledge of data.

### Data collection

Original collection by the source consortia (TCGA, Mariathasan et al. IMvigor210, Hugo/Riaz melanoma GEO, CELLxGENE Census contributors). This study does not re-collect samples.

### Data codebook

Codebooks: Census schema; TISCH2 annotation tables; TCGA gene maps; IMvigor210 package vignette; GEO Series Matrix / SOFT. Locked gene lists and models: `PROTOCOL.md` at `3fbf310`.

---

## Variables

### Manipulated variable(s)

Not applicable (observational secondary analysis).

### Measured variable(s)

**ECS core (confirmatory, n = 9):** `CNR1, CNR2, GPR55, TRPV1, FAAH, MGLL, DAGLA, DAGLB, NAPEPLD`  
Neighbors (`GPR18, GPR119, TRPV2, ABHD6, ABHD12`) are exploratory only.

**scRNA state:** mean of the nine genes inside one locked lineage bucket (B/plasma, myeloid, T/NK, malignant/epithelial, stromal/other). One state per bucket.

**Bulk scores:** available-case mean of within-cohort gene-wise z-scores. Denominator = genes present for that sample, never 9 with zeros. Sample scored only if ≥7/9 ECS genes (B ≥3/5, TLS ≥3/4, CD8 ≥3/5).

**Adjustment signatures:**  
- B cell: `MS4A1, CD19, CD79A, CD79B, MZB1`  
- TLS: `CXCL13, CCL19, CCL21, CCR7`  
- CD8 / cytotoxicity: `CD8A, CD8B, GZMB, PRF1, IFNG`

**scRNA contamination gene (per dataset):** first present of `MS4A1`, `CD19`, `CD79A`. Non-B lineage dropped if that gene’s detection ≥ 10%. If all three absent, all non-B lineages from that dataset are discarded.

**IMvigor210 outcome (kill):** binary response CR/PR vs SD/PD; drop NE/NA.  
**Secondary:** Cox OS. Not a Gate B pass.

**Primary predictor at Gate B:** continuous **raw** frozen ECS score of the Unit 05 primary non-B state. Median split is display-only.

### Inclusion and exclusion

- scRNA: tumor datasets for the five types; ≥2 types or amend.  
- TCGA: listed types; BLCA required for Gate A.  
- IMvigor210: samples with RNA and coded response for Model 1; complete cases for VIF/Model 1.  
- Expected n: IMvigor210 on the order of ~300 with RNA (exact n after Unit 00). Melanoma GEO small n, descriptive.

### Missing data

Gene missingness: drop gene cohort-wide if absent for all samples; available-case mean otherwise; never zero-fill. If >2 core ECS genes missing from IMvigor210, do not run Gate B. Samples below gene minima are dropped; report n. Residualization is Gate A only.

### Outliers

No outcome-based outlier deletion. No AUC/Youden/tertile search. Continuous scores as specified.

### Sampling weights

None.

---

## Knowledge of data

### Previous work

No prior SCENDO paper or conference analysis existed at seal. The registrant knows the public literature that *CNR2* is often B-cell-associated, that B cells/TLS predict ICI in several cancers, and that IMvigor210/TCGA/Census/GEO exist as public resources.

**After Decide (paste this on OSF):** Confirmatory results are now in this repository (`research/06-imvigor210.md`, `research/07-melanoma-geo.md`, `RESULTS.md`, `docs/manuscript.md`). Gate B **failed** (Model 1 ECS CI includes 1). The atlas paper reports that negative. This OSF record does not re-open Gate B.

**Fill in if true:** any other lab paper that already used IMvigor210, TCGA, or Census for other genes.

### Prior knowledge

**At seal:** published biology and cohort descriptions; the sealed protocol; no ICI outcome-vs-ECS models for this study. Primary non-B state named in Unit 05 **before** those files were opened (git `21be9bd` before `c1a47f9`).

**At OSF click after Decide:** those models have been run as specified. Disclose that. The freeze SHA remains `3fbf310`.

---

## Analyses

### Statistical model

**Gate C:** detection % (count > 0) for `CNR2`, `MGLL`, `FAAH` by lineage × type.

**Gate A:** lineage ECS means; Pearson (pass) and Spearman (report) of non-B raw scores vs B and TLS in pooled TCGA and TCGA-BLCA; optional residual `raw ~ B + TLS` with locked escape rules; contamination filter as above. Primary state named by the locked cascade in `PROTOCOL.md` § primary state rule.

**Gate B (only if Gate A passed and Unit 05 committed):**  
Model 1 (kill): logistic `response ~ ECS_raw + B_cell + TLS + CD8`. Report OR and 95% CI. VIF for all four terms; no term dropping.  
Model 2 (robustness only): + TMB + PD-L1 IC if present.  
Unadjusted `response ~ ECS_raw` reported, neither necessary nor sufficient.  
Cox OS secondary.

**Replication:** GSE78220, GSE91061 with frozen objects; report only.

### Effect size

No clinical minimum effect. Kill bar is CI excluding 1 (and VIF < 3), not a target OR/AUC.

### Power

IMvigor210 n is fixed (~300 with RNA). No prospective sample-size calculation. Underpowered melanoma GEO will not rescue Gate B. Exact n after Unit 00.

### Inference criteria

- Gate A/C: rules in `KILL.md` at `3fbf310` (human marks pass/fail).  
- Gate B pass: Model 1 ECS 95% CI excludes OR = 1 **and** VIF(ECS) < 3.0. Two-sided logistic/Cox.  
- Secondary states: Holm–Bonferroni; cannot rescue Gate B.  
- No multiple-testing correction on the single primary state × single kill endpoint (response).

### Assumptions

If logistic/Cox fails to fit (separation, non-convergence): report the failure, do not switch to cutoff search or new ECS genes; amend in `STATUS.md` if a different pre-specified estimator is required. Collinearity is handled by the VIF rule, not by dropping B/TLS/CD8.

### Sensitivity

Pre-specified robustness: Model 2 (TMB + PD-L1 IC). Deconvolution is exploratory and cannot flip Gate B. No unplanned cutoff optimization.

### Exploratory

Neighbor ECS genes; NMF programs; CIBERSORTx/BayesPrism ECS-in-fraction; GSE220635 after Decide; DDI/FAERS; browser/scGPT. Label exploratory in the paper. See `EXPLORE.md`.

---

## Statement of integrity (use this version after Decide)

The registrant states that the confirmatory protocol was sealed at git SHA `3fbf310870c57247163edca35ed536ade3ea4301` on 2026-08-24, that genes, models, and the Unit 05 primary name were frozen before ICI outcome-vs-ECS analysis, and that those analyses were then run as specified. This OSF record deposits that sealed plan for public timestamping. It does not claim that confirmatory tests remain unrun as of the OSF submission date. No other preregistration exists for the same confirmatory hypotheses at that SHA.

---

## After OSF returns a URL

**Done 2026-08-27.** Public URL in `STATUS.md`: https://osf.io/c8kpx (DOI 10.17605/OSF.IO/C8KPX). Do not edit `PROTOCOL.md` confirmatory sections.
