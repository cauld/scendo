# Unit 07 — Melanoma GEO replication (descriptive)

**Run date:** 2026-08-24  
**Protocol SHA:** `3fbf310870c57247163edca35ed536ade3ea4301`  
**Primary state:** Stromal/other (same nine-gene raw score as Gate B)  
**Rule:** Pre-treatment anti-PD-1 melanoma. Same available-case scoring as Unit 06. Fit Model 1 covariates if available. **Cannot pass or rescue Gate B.** No cutoff search.

## Gate B (already marked; this unit cannot change it)

- Human Gate B: **fail** (IMvigor210 Model 1 ECS CI includes 1).
- These GEO sets are underpowered replication. They are reported only.

## GSE78220

- **Citation:** Hugo et al. Cell 2016; pembrolizumab melanoma
- Transform: `log2(FPKM + 1)`, then within-cohort z-score (pre-treatment window), available-case mean
- Expression columns: 28
- Pre-treatment samples: 27; patients in model window: 26
- Model n (CR/PR vs SD/PD, complete scores): **26** (CR/PR=14, SD/PD=12)
- Model 1 covariates available: B cell, TLS, CD8, sex, age, OS
- TMB / PD-L1 IC: **False**

- Dropped on-treatment columns: Pt16.OnTx

### Model 1 (descriptive)

`response ~ ecs + b_cell + tls + cd8`. Cannot pass or rescue Gate B.

- n = **26**. Converged: **True**. Error: none

| Term | OR | 95% CI | p | CI excludes 1 |
|---|---:|---|---:|---|
| ecs | 0.469 | 0.019–11.697 | 0.6443 | False |
| b_cell | 1.118 | 0.157–7.945 | 0.9111 | False |
| tls | 2.296 | 0.226–23.287 | 0.4819 | False |
| cd8 | 0.511 | 0.136–1.926 | 0.3213 | False |

### Unadjusted (descriptive)

`response ~ ecs`. n = **26**. OR 1.108 (0.084–14.613). Converged: **True**.

### Cox OS (descriptive)

Time = overall survival (days). Event = dead. n = **25**, events = 11.

| Term | HR | 95% CI | p |
|---|---:|---|---:|
| ecs | 1.353 | 0.066–27.886 | 0.8446 |
| b_cell | 1.213 | 0.277–5.315 | 0.7976 |
| tls | 0.546 | 0.067–4.415 | 0.5703 |
| cd8 | 1.445 | 0.520–4.011 | 0.4803 |

## GSE91061

- **Citation:** Riaz et al. Cell 2017; nivolumab melanoma
- Transform: `log2(FPKM + 1)`, then within-cohort z-score (pre-treatment window), available-case mean
- Expression columns: 109
- Pre-treatment samples: 51; patients in model window: 51
- Model n (CR/PR vs SD/PD, complete scores): **49** (CR/PR=10, SD/PD=39)
- Model 1 covariates available: B cell, TLS, CD8
- TMB / PD-L1 IC: **False**

- Dropped UNK/NA response: 2

### Model 1 (descriptive)

`response ~ ecs + b_cell + tls + cd8`. Cannot pass or rescue Gate B.

- n = **49**. Converged: **True**. Error: none

| Term | OR | 95% CI | p | CI excludes 1 |
|---|---:|---|---:|---|
| ecs | 0.603 | 0.066–5.510 | 0.6537 | False |
| b_cell | 1.520 | 0.345–6.699 | 0.5797 | False |
| tls | 1.349 | 0.266–6.839 | 0.718 | False |
| cd8 | 1.064 | 0.351–3.229 | 0.9122 | False |

### Unadjusted (descriptive)

`response ~ ecs`. n = **49**. OR 1.091 (0.163–7.310). Converged: **True**.

## What was not done

- No cutoff / Youden / AUC search. No new ECS genes. Primary name not changed.
- Results here do not flip Gate B.
