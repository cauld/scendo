# Unit 05 — Primary non-B state (A→B wall)

**Run date:** 2026-08-24  
**Protocol SHA:** `3fbf310870c57247163edca35ed536ade3ea4301`  
**Inputs:** `research/02-scrna-states.md`, `research/03-frozen-markers.json`, `research/04-tcga-confound.md`  
**Rule:** Name the primary after Gate A numbers exist and **before** any IMvigor210 or GEO phenotype/outcome file is opened. Gate A needs both (i) ≥2 lineage buckets with an ECS state and (ii) ≥1 non-B candidate that passed confound tests. If several non-B buckets qualify, apply the locked cascade (no judgment). Subtypes within a bucket are not separate states. Gate B always uses the raw nine-gene score.

## Gate A both-parts (operator; human marks below)

- Lineage buckets with an ECS state: **3** (B/plasma, Malignant/epithelial, Stromal/other)
- Two-lineage rule (≥2 buckets, including B/plasma): **True**
- Non-B candidates: **Malignant/epithelial, Stromal/other**
- Non-B candidates that qualify on confound tests: **Malignant/epithelial, Stromal/other** (n=2)
- Residual escape used: **False** (both Pearson tests passed |r| < 0.6)
- Operator Gate A numbers hold: **True**

## Cascade (qualifying non-B buckets only)

1. Lowest `max(|r_B|, |r_TLS|)` using Pearson on **pooled raw** scores.
2. Tie: present (ECS-state rule) in more of the five cancer types.
3. Tie: myeloid > T/NK > malignant/epithelial > stromal/other.
4. Tie: higher mean core-ECS (mean of that bucket’s lineage-mean core-ECS across types where it has an ECS state).
5. Tie: larger total cell count *n* in those types for that bucket.
6. Tie: earlier bucket name in ASCII sort of `{malignant/epithelial, myeloid, stromal/other, t/nk}`.

Bulk TCGA scores the same nine-gene mean for every non-B candidate, so step 1 is a tie whenever more than one bucket qualifies. They still compete as separate lineage buckets.

| Candidate | Qualifies | r_B_pooled | r_TLS_pooled | max\|r\| pooled | r_B_BLCA | r_TLS_BLCA | Residual pooled | Residual BLCA | n types | Types | Mean core-ECS | Cell n | Priority | ASCII |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---|
| Malignant/epithelial | True | 0.4173 | 0.3835 | 0.4173 | 0.3605 | 0.2628 | — | — | 4 | BLCA, BRCA, CRC, NSCLC | 0.3973 | 173143 | 2 | `malignant/epithelial` |
| Stromal/other | True | 0.4173 | 0.3835 | 0.4173 | 0.3605 | 0.2628 | — | — | 5 | BLCA, BRCA, CRC, NSCLC, melanoma | 2.4239 | 511227 | 3 | `stromal/other` |

### Per-type core-ECS (types where the bucket has an ECS state)

**Malignant/epithelial**

| Type | n cells | Mean core-ECS |
|---|---:|---:|
| CRC | 5105 | 0.1788 |
| BRCA | 105099 | 0.1726 |
| NSCLC | 59167 | 1.1985 |
| BLCA | 3772 | 0.0395 |

**Stromal/other**

| Type | n cells | Mean core-ECS |
|---|---:|---:|
| CRC | 147152 | 0.2754 |
| BRCA | 252577 | 0.0739 |
| NSCLC | 110846 | 1.8128 |
| melanoma | 295 | 9.8983 |
| BLCA | 357 | 0.0591 |

### Walk

- Step 1 (lowest max(|r_B|, |r_TLS|) on pooled raw Pearson): 2 → 2 remaining (Malignant/epithelial, Stromal/other); best max_abs_r_pooled = 0.4173.
- Step 2 (present (ECS-state rule) in more of the five cancer types): 2 → 1 remaining (Stromal/other); best n_types = 5.
  **Stopped here.**

**Deciding step:** step 2: present (ECS-state rule) in more of the five cancer types

## Primary state (frozen for Gate B)

- **Name:** Stromal/other
- **Lineage bucket:** Stromal/other
- **Nine genes:** `CNR1`, `CNR2`, `GPR55`, `TRPV1`, `FAAH`, `MGLL`, `DAGLA`, `DAGLB`, `NAPEPLD`
- **r_B_pooled:** 0.4173
- **r_TLS_pooled:** 0.3835
- **r_B_BLCA:** 0.3605
- **r_TLS_BLCA:** 0.2628
- **Residual SD/raw SD pooled:** — (not used)
- **Residual SD/raw SD BLCA:** — (not used)
- **Cancer types with an ECS state:** BLCA, BRCA, CRC, NSCLC, melanoma (5 of 5)
- **Mean core-ECS (across those types):** 2.4239
- **Total cell n (those types):** 511227
- **Tie-breaker that decided the primary:** step 2: present (ECS-state rule) in more of the five cancer types

Secondary non-B states may be scored later; they cannot pass Gate B.

## Contamination

- Fallback order: `MS4A1` → `CD19` → `CD79A`
- Threshold: 10% detection in a non-B lineage (that type)
- Gene used (Census): **MS4A1**
- Gene used (BLCA / TISCH2): **MS4A1**
- Non-B lineages discarded: **0**

| Type | Source | Bucket | n cells | Contam gene | Contam % | Discarded | Kept |
|---|---|---|---:|---|---:|---|---|
| CRC | Census | B/plasma | 40943 | MS4A1 | — | False | False |
| CRC | Census | Myeloid | 50617 | MS4A1 | 1.15 | False | False |
| CRC | Census | T/NK | 121657 | MS4A1 | 1.36 | False | False |
| CRC | Census | Malignant/epithelial | 5105 | MS4A1 | 3.55 | False | True |
| CRC | Census | Stromal/other | 147152 | MS4A1 | 0.67 | False | True |
| BRCA | Census | B/plasma | 74842 | MS4A1 | — | False | False |
| BRCA | Census | Myeloid | 163404 | MS4A1 | 0.63 | False | False |
| BRCA | Census | T/NK | 1038935 | MS4A1 | 1.21 | False | False |
| BRCA | Census | Malignant/epithelial | 105099 | MS4A1 | 0.32 | False | True |
| BRCA | Census | Stromal/other | 252577 | MS4A1 | 0.68 | False | True |
| NSCLC | Census | B/plasma | 123381 | MS4A1 | — | False | False |
| NSCLC | Census | Myeloid | 311128 | MS4A1 | 0.89 | False | False |
| NSCLC | Census | T/NK | 556875 | MS4A1 | 1.96 | False | False |
| NSCLC | Census | Malignant/epithelial | 59167 | MS4A1 | 0.57 | False | True |
| NSCLC | Census | Stromal/other | 110846 | MS4A1 | 0.80 | False | True |
| melanoma | Census | B/plasma | 964 | MS4A1 | — | False | True |
| melanoma | Census | Myeloid | 121 | MS4A1 | 0.83 | False | False |
| melanoma | Census | T/NK | 22335 | MS4A1 | 1.36 | False | False |
| melanoma | Census | Malignant/epithelial | 204 | MS4A1 | 0.98 | False | False |
| melanoma | Census | Stromal/other | 295 | MS4A1 | 2.37 | False | True |
| BLCA | TISCH2+GEO GSE130001 | B/plasma | 0 | MS4A1 | — | False | False |
| BLCA | TISCH2+GEO GSE130001 | Myeloid | 0 | MS4A1 | — | False | False |
| BLCA | TISCH2+GEO GSE130001 | T/NK | 0 | MS4A1 | — | False | False |
| BLCA | TISCH2+GEO GSE130001 | Malignant/epithelial | 3772 | MS4A1 | 0.03 | False | True |
| BLCA | TISCH2+GEO GSE130001 | Stromal/other | 357 | MS4A1 | 0.00 | False | True |

## Human Gate A

- [X] Pass (two lineages + at least one qualifying non-B state named above) — marked 2026-08-24
- [ ] Fail — do not open ICI outcomes for a checkpoint test

## What was not done

- No IMvigor210 or GEO phenotype/outcome files opened.
- No Gate B. No cutoff search. No DE / extra ECS genes.
- Frozen Unit 03 marker object not edited.
