# Unit 06 — IMvigor210 confirmatory (Gate B)

**Run date:** 2026-08-24  
**Protocol SHA:** `3fbf310870c57247163edca35ed536ade3ea4301`  
**Primary state:** Stromal/other (Unit 05, git freeze before this run)  
**Pin:** `data/raw/imvigor210/cds/cds.RData` from `IMvigor210CoreBiologies_1.0.1.tar.gz`  
**Rule:** Continuous **raw** nine-gene ECS score. Model 1 = `response ~ ECS + B_cell + TLS + CD8` (logistic). Gate B pass = Model 1 ECS 95% CI excludes 1 **and** VIF(ECS) < 3. Unadjusted, Model 2, OS, and secondary states cannot pass or rescue. No cutoff search.

## Matrix

- Object: CountDataSet `cds` (raw integer counts, 31286 genes × 348 samples)
- Transform: DESeq `sizeFactor`-normalized counts, then `log2(norm + 1)`, then within-cohort gene-wise z-score (ddof=0), available-case mean per `PROTOCOL.md`
- Size factors present: **True**
- Genes missing from matrix: **none** (ECS 9/9, B 5/5, TLS 4/4, CD8 5/5)

## Endpoint

- `binaryResponse` as shipped: CR/PR vs SD/PD. Drop NE/NA.
- RNA samples: **348**
- Dropped (ECS/B/TLS/CD8 below gene minima): **0**
- Dropped (binaryResponse NE/NA or not CR/PR|SD/PD): **50**
- Model 1 complete cases: **298** (CR/PR=68, SD/PD=230)

## Scores (Model 1 table)

| Score | Genes used | Min genes | n missing on RNA |
|---|---|---:|---:|
| ECS (primary Stromal/other) | nine core | 7/9 | 0 |
| B cell | five locked | 3/5 | 0 |
| TLS | four locked | 3/4 | 0 |
| CD8 | five locked | 3/5 | 0 |

## Model 1 (kill)

`response ~ ecs + b_cell + tls + cd8` (logistic). 1 = CR/PR.

- n = **298**
- Converged: **True**

| Term | OR | 95% CI | p | CI excludes 1 |
|---|---:|---|---:|---|
| ecs | 1.189 | 0.551–2.563 | 0.6593 | False |
| b_cell | 0.961 | 0.495–1.863 | 0.9057 | False |
| tls | 0.517 | 0.258–1.035 | 0.06233 | False |
| cd8 | 2.380 | 1.508–3.757 | 0.000195 | True |

## VIF (Model 1 complete-case predictors)

VIF from OLS auxiliary regressions on the four scores plus intercept. Report the four scores. Model 1 is always fit as specified (no term dropping).

| Term | VIF |
|---|---:|
| ecs | 1.360 |
| b_cell | 5.330 |
| tls | 4.686 |
| cd8 | 2.157 |
| Intercept (not a Gate B term) | 1.002 |

- VIF(ECS) < 3: **True**

## Gate B draft (human marks)

- Model 1 ECS CI excludes 1: **False** (OR 1.189 (0.551–2.563))
- VIF(ECS) < 3: **True** (1.360)
- Operator Gate B numbers hold: **False**

OS, Model 2, unadjusted, secondary states, deconvolution, and melanoma GEO cannot rescue.

## Unadjusted (neither necessary nor sufficient)

`response ~ ecs`. n = **298**. OR 1.076 (0.568–2.038). p = 0.8224.

## Model 2 (robustness, not a pass)

Model 1 + TMB (`FMOne mutation burden per MB`) + PD-L1 IC (`IC Level` as shipped factor). Complete cases. Sex added only if it is complete for that same n (no extra drops). No patient age column in the extract.

- n = **234**
- Sex included: **True** (complete on Model 2 table: True)
- Converged: **True**

| Term | OR | 95% CI | p |
|---|---:|---|---:|
| C(ic)[T.IC1] | 0.847 | 0.315–2.275 | 0.7419 |
| C(ic)[T.IC2+] | 1.477 | 0.500–4.362 | 0.4799 |
| C(sex)[T.M] | 1.056 | 0.459–2.427 | 0.8981 |
| ecs | 1.093 | 0.449–2.663 | 0.8443 |
| b_cell | 1.272 | 0.554–2.922 | 0.5709 |
| tls | 0.511 | 0.214–1.219 | 0.1301 |
| cd8 | 1.462 | 0.806–2.654 | 0.2116 |
| tmb | 1.097 | 1.052–1.143 | 1.246e-05 |

## Cox OS (secondary, not a pass)

Time = `os` (months). Event = `censOS` (1 = dead) as shipped. Same four scores as Model 1. n = **348** (events = 232).

| Term | HR | 95% CI | p |
|---|---:|---|---:|
| ecs | 0.898 | 0.623–1.294 | 0.5628 |
| b_cell | 1.029 | 0.747–1.418 | 0.8607 |
| tls | 1.031 | 0.742–1.431 | 0.8576 |
| cd8 | 0.800 | 0.644–0.994 | 0.04393 |

## Human Gate B

- [ ] Pass (Model 1 ECS CI excludes 1 **and** VIF(ECS) < 3)
- [X] Fail — marked 2026-08-24 (Model 1 ECS CI includes 1)

## What was not done

- No new ECS genes. No median/Youden/ROC/AUC cutoff search.
- No deconvolution. No melanoma GEO (Unit 07). Secondary non-B state not used to pass Gate B.
- Frozen Unit 03/05 objects not edited.
