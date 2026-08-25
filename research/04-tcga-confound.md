# Unit 04 — TCGA confound (Gate A)

**Run date:** 2026-08-24  
**Protocol SHA:** `3fbf310870c57247163edca35ed536ade3ea4301`  
**Frozen markers:** `research/03-frozen-markers.json`  
**Rule:** For each non-B candidate, score the **raw** nine-gene mean of within-cohort z-scores. Pearson |r| vs B-cell and vs TLS must both be **< 0.6** in concatenated pooled TCGA **and** in TCGA-BLCA. If a Pearson test fails on a cohort, residualize `raw ~ B + TLS` on that same cohort. Rescue iff residual SD / raw SD ≥ 0.5 **and** |r_B| < 0.75 **and** |r_TLS| < 0.75. Spearman is descriptive. Gate B always uses the raw score. Do not name the primary state.

## Bulk scoring note

The sealed marker list is the nine core ECS genes (no DE). In bulk TCGA, every non-B candidate (Malignant/epithelial, Stromal/other) is therefore scored with the **same** nine-gene mean. Pearson values are identical across candidates; they still qualify or fail as separate lineage buckets for Unit 05.

## Matrix

- **Host:** `https://toil.xenahubs.net`  
- **Dataset:** `tcga_RSEM_gene_tpm` — log2(TPM + 0.001) as shipped (TOIL RSEM)  
- **Phenotype:** `data/raw/xena/TCGA_phenotype_denseDataOnlyDownload.tsv.gz` (`_primary_disease` labels from Unit 00; cancer-type only, no ICI outcomes)  
- **Samples requested (disease-matched):** 4220  
- **Samples with expression (aligned):** 3664  

Pooled window = concatenate LUAD, LUSC, SKCM, COAD, READ, BRCA, BLCA. NSCLC = LUAD+LUSC; CRC = COAD+READ. BLCA is its own z-score window. All `_primary_disease`-matched sample types are kept (including Solid Tissue Normal); counts below.

### Sample type × project

```
sample_type  Additional Metastatic  Metastatic  Primary Tumor  Recurrent Tumor  Solid Tissue Normal
project                                                                                            
BLCA                             0           0            407                0                   19
BRCA                             0           7           1092                0                  113
COAD                             0           1            288                1                   41
LUAD                             0           0            513                2                   59
LUSC                             0           0            498                0                   50
READ                             0           0             92                1                   10
SKCM                             1         366            102                0                    1
```

Kill-type n: BLCA=426, BRCA=1212, CRC=434, NSCLC=1122, melanoma=470. Project n: BLCA=426, BRCA=1212, COAD=331, LUAD=574, LUSC=548, READ=103, SKCM=470.

## Genes

Available-case mean of gene-wise z-scores (ddof=0) within the analysis window. Minimum genes: ECS 7/9, B cell 3/5, TLS 3/4. Never zero-fill. Confirmatory correlations use complete cases with all three scores.

| Symbol | Probe (gencode.v23) | Signature |
|---|---|---|
| `CNR1` | `ENSG00000118432.12` | ECS |
| `CNR2` | `ENSG00000188822.7` | ECS |
| `GPR55` | `ENSG00000135898.9` | ECS |
| `TRPV1` | `ENSG00000196689.10` | ECS |
| `FAAH` | `ENSG00000117480.15` | ECS |
| `MGLL` | `ENSG00000074416.13` | ECS |
| `DAGLA` | `ENSG00000134780.9` | ECS |
| `DAGLB` | `ENSG00000164535.14` | ECS |
| `NAPEPLD` | `ENSG00000161048.11` | ECS |
| `MS4A1` | `ENSG00000156738.17` | B cell |
| `CD19` | `ENSG00000177455.11` | B cell |
| `CD79A` | `ENSG00000105369.9` | B cell |
| `CD79B` | `ENSG00000007312.12` | B cell |
| `MZB1` | `ENSG00000170476.15` | B cell |
| `CXCL13` | `ENSG00000156234.7` | TLS |
| `CCL19` | `ENSG00000172724.11` | TLS |
| `CCL21` | `ENSG00000137077.7` | TLS |
| `CCR7` | `ENSG00000126353.3` | TLS |

## Confirmatory Pearson (same nine-gene score for every non-B candidate)

| Cohort | n | r_B | abs r_B | r_TLS | abs r_TLS | Spearman_B | Spearman_TLS | max abs r | Pearson fail | Residual SD/raw SD | Cohort pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| pooled TCGA | 3664 | 0.4173 | 0.4173 | 0.3835 | 0.3835 | 0.3936 | 0.3732 | 0.4173 | False | — | True |
| TCGA-BLCA | 426 | 0.3605 | 0.3605 | 0.2628 | 0.2628 | 0.3427 | 0.2564 | 0.3605 | False | — | True |

- Pooled: both |r| < 0.6
- BLCA: both |r| < 0.6

## Per candidate (four Pearson values each)

| Candidate | r_B_pooled | r_TLS_pooled | r_B_BLCA | r_TLS_BLCA | Residual ratio pooled | Residual ratio BLCA | Qualifies |
|---|---:|---:|---:|---:|---:|---:|---|
| Malignant/epithelial | 0.4173 | 0.3835 | 0.3605 | 0.2628 | — | — | True |
| Stromal/other | 0.4173 | 0.3835 | 0.3605 | 0.2628 | — | — | True |

## Per-project Pearson (descriptive; not the pass metric)

Each project is its own z-score window.

| Project | Kill type | n | r_B | r_TLS | Spearman_B | Spearman_TLS |
|---|---|---:|---:|---:|---:|---:|
| LUAD | NSCLC | 574 | 0.2492 | 0.2996 | 0.2449 | 0.3152 |
| LUSC | NSCLC | 548 | 0.3357 | 0.3669 | 0.3019 | 0.3499 |
| SKCM | melanoma | 470 | 0.3423 | 0.3505 | 0.3113 | 0.3374 |
| COAD | CRC | 331 | 0.5546 | 0.4053 | 0.5729 | 0.4626 |
| READ | CRC | 103 | 0.3954 | 0.3946 | 0.3780 | 0.3608 |
| BRCA | BRCA | 1212 | 0.4160 | 0.4454 | 0.4117 | 0.4257 |
| BLCA | BLCA | 426 | 0.3605 | 0.2628 | 0.3427 | 0.2564 |

## Qualification (operator; human marks Gate A in Unit 05)

- Non-B candidates from Unit 03: **Malignant/epithelial, Stromal/other**
- Pooled confound pass: **True**
- BLCA confound pass: **True**
- At least one non-B candidate qualifies (both cohorts): **True**
- Two-lineage rule (from Unit 02/03, including B/plasma): **True** (B/plasma, Malignant/epithelial, Stromal/other)

A candidate qualifies only if every failed Pearson test is rescued on that same cohort. Unit 05 applies the naming cascade and the human marks Gate A. This unit does not pick the primary state.

## What was not done

- No ICI phenotype or outcome files opened.
- No DE / extra ECS genes.
- Primary non-B state not named (Unit 05).
- Gate B not run.
