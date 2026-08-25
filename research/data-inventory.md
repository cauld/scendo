# Data inventory

**Unit:** 00  
**Run date:** 2026-08-24  
**Protocol SHA (STATUS):** `3fbf310870c57247163edca35ed536ade3ea4301`  
**Rule:** access + gene coverage only. No ICI outcome-vs-ECS plots or summaries. Phenotype recorded as column names only.

## Pass / fail

- Primary sources reachable: **True**
- IMvigor210 core ECS missing ≤ 2: **True** (0 missing)
- Census cancer types ≥ 2 of 5: **True** (['NSCLC', 'melanoma', 'CRC', 'BRCA'])
- scRNA contamination gene available (Census): **MS4A1**
- TCGA-BLCA phenotype rows present: **True**

## HGNC aliases (Unit 00 record)

Locked symbols stay as in `PROTOCOL.md`. Aliases below are for matrix matching only.

| Symbol | Ensembl | Entrez | HGNC aliases / previous |
|---|---|---|---|
| `CNR1` | `ENSG00000118432` | 1268 | CB1K5, CB-R, CB1, CANN6, CB1A, CNR |
| `CNR2` | `ENSG00000188822` | 1269 | CB2; protocol: CX5, CB-2 |
| `GPR55` | `ENSG00000135898` | 9290 | —protocol: LPIR1 |
| `TRPV1` | `ENSG00000196689` | 7442 | VR1 |
| `FAAH` | `ENSG00000117480` | 2166 | FAAH-1, FAAH1 |
| `MGLL` | `ENSG00000074416` | 11343 | HU-K5, MGL, MAGL; protocol: HUK5 |
| `DAGLA` | `ENSG00000134780` | 747 | KIAA0659, NSDDR, DAGLALPHA, C11orf11; protocol: DAGL-ALPHA, DGL-ALPHA, NOC2 |
| `DAGLB` | `ENSG00000164535` | 221955 | KCCR13L, DAGLBETA; protocol: DAGL-BETA, DGL-BETA |
| `NAPEPLD` | `ENSG00000161048` | 222236 | FMP30, C7orf18, NAPE-PLD; protocol: NAPEPLD, C7ORF9 |
| `MS4A1` | `ENSG00000156738` | 931 | B1, Bp35, FMC7, CD20 |
| `CD19` | `ENSG00000177455` | 930 | — |
| `CD79A` | `ENSG00000105369` | 973 | MB-1, Ig-alpha, MB1, IGAlpha, IGA |
| `CD79B` | `ENSG00000007312` | 974 | B29, Ig-beta, Igbeta, IGB |
| `MZB1` | `ENSG00000170476` | 51237 | PACAP, MGC29506, HSPC190, pERp1, MEDA-7 |
| `CXCL13` | `ENSG00000156234` | 10563 | BLC, BCA-1, BLR1L, ANGIE, ANGIE2, SCYB13 |
| `CCL19` | `ENSG00000172724` | 6363 | ELC, MIP-3b, exodus-3, CKb11, SCYA19 |
| `CCL21` | `ENSG00000137077` | 6366 | SLC, exodus-2, TCA4, CKb9, 6Ckine, ECL, SCYA21 |
| `CCR7` | `ENSG00000126353` | 1236 | BLR2, CDw197, CD197, CMKBR7, EBI1 |
| `CD8A` | `ENSG00000153563` | 925 | p32, CD8alpha, CD8 |
| `CD8B` | `ENSG00000172116` | 926 | Ly-3, LYT3, P37, CD8beta, CD8B1 |
| `GZMB` | `ENSG00000100453` | 3002 | CCPI, CGL-1, CSP-B, CGL1, CTSGL1, HLP, SECT, CTLA1, CSPB |
| `PRF1` | `ENSG00000180644` | 5551 | PFP, P1, HPLH2 |
| `IFNG` | `ENSG00000111537` | 3458 | — |

## 1. CELLxGENE Census (primary scRNA)

- **API:** `cellxgene-census` via `uv` group `census`
- **Pinned version:** `2025-11-08` (requested `stable`)
- **License:** Per-dataset on CELLxGENE Discover (typically CC BY 4.0); Census access terms apply
- **Gene IDs:** feature_name (HGNC symbol) + feature_id (Ensembl)
- **Features:** 61497
- **Local path:** remote SOMA (not downloaded as h5ad)
- **Cancer types present:** NSCLC, melanoma, CRC, BRCA

- NSCLC: lung adenocarcinoma (n=831387), non-small cell lung carcinoma (n=94157), squamous cell lung carcinoma (n=235853)
- melanoma: melanoma (n=13024), metastatic melanoma (n=230924), uveal melanoma (n=51712)
- CRC: colon adenocarcinoma (n=257251), colorectal cancer (n=146575), colorectal carcinoma || metastatic malignant neoplasm (n=31536)
- BRCA: HER2 positive breast carcinoma (n=16017), breast cancer (n=1286123), breast carcinoma (n=17357), estrogen-receptor positive breast cancer (n=87648), invasive ductal breast carcinoma (n=208638), invasive lobular breast carcinoma (n=25304), invasive tubular breast carcinoma || invasive lobular breast carcinoma (n=8512), luminal A breast carcinoma (n=10227), luminal B breast carcinoma (n=28628), metaplastic breast carcinoma (n=0), triple-negative breast carcinoma (n=215960)
- BLCA: **not found** in Census disease labels (TISCH2 fallback eligible)

**ECS** (9/9 present)

| Gene | In matrix |
|---|---|
| `CNR1` | CNR1 |
| `CNR2` | CNR2 |
| `GPR55` | GPR55 |
| `TRPV1` | TRPV1 |
| `FAAH` | FAAH |
| `MGLL` | MGLL |
| `DAGLA` | DAGLA |
| `DAGLB` | DAGLB |
| `NAPEPLD` | NAPEPLD |

**B cell** (5/5 present)

| Gene | In matrix |
|---|---|
| `MS4A1` | MS4A1 |
| `CD19` | CD19 |
| `CD79A` | CD79A |
| `CD79B` | CD79B |
| `MZB1` | MZB1 |

**TLS** (4/4 present)

| Gene | In matrix |
|---|---|
| `CXCL13` | CXCL13 |
| `CCL19` | CCL19 |
| `CCL21` | CCL21 |
| `CCR7` | CCR7 |

**CD8** (5/5 present)

| Gene | In matrix |
|---|---|
| `CD8A` | CD8A |
| `CD8B` | CD8B |
| `GZMB` | GZMB |
| `PRF1` | PRF1 |
| `IFNG` | IFNG |

**Contamination screen genes** (3/3 present)

| Gene | In matrix |
|---|---|
| `MS4A1` | MS4A1 |
| `CD19` | CD19 |
| `CD79A` | CD79A |

Contamination gene for Census (first present of MS4A1 → CD19 → CD79A): **MS4A1**

## 2. TISCH2 (fallback only)

- **URL:** https://tisch.compbio.cn/home/  
- **Reachable:** True (HTTP 200)
- **License:** Academic / cite Sun et al. NAR 2021 and Han et al. NAR 2023; processed matrices under TISCH terms
- **Gene IDs:** HGNC symbols (MAESTRO-processed)
- **Local path:** `data/raw/tisch2/BLCA_GSE130001_CellMetainfo_table.tsv` (BLCA fallback metadata only; no count matrix)

| Kill type | TISCH2 code | Datasets on home page |
|---|---|---|
| NSCLC | NSCLC | 17 |
| melanoma | SKCM | 10 |
| CRC | CRC | 11 |
| BRCA | BRCA | 12 |
| BLCA | BLCA | 3 |

All five kill-test types exist on TISCH2. **Census lacks BLCA**, so Unit 01 uses TISCH2 for that type only.

Pinned BLCA fallback: `BLCA_GSE130001` (untreated primary; 2 patients; 4,129 cells; major-lineage labels on the metadata file). Other BLCA sets on TISCH2 are ICI/chemo-treated (`GSE145281_aPDL1`, `GSE149652`) and are not needed unless GSE130001 fails to load.

TISCH2 gene-search index includes all nine ECS genes, B/TLS/CD8, and `MS4A1` / `CD19` / `CD79A`. Count matrix not downloaded in Unit 00.

## 3. TCGA (UCSC Xena TOIL)

- **Host:** https://toil.xenahubs.net
- **Pinned dataset:** `tcga_RSEM_gene_tpm` — log2(TPM + 0.001) (TOIL RSEM); not downloaded in Unit 00
- **Full matrix URL (not downloaded in Unit 00):** https://toil.xenahubs.net/download/tcga_RSEM_gene_tpm.gz
- **License:** TCGA / NIH Genomic Data Sharing; no attempt to re-identify
- **Gene IDs:** Ensembl gene ID (probe) mapped to HGNC via gencode.v23 probeMap
- **probeMap:** `data/raw/xena/gencode.v23.annotation.gene.probemap` SHA256 `6783ea58791ae876efb697889a042cc7be8e32e40fc01191c622ef25d9416931`
- **Phenotype file:** `data/raw/xena/TCGA_phenotype_denseDataOnlyDownload.tsv.gz` (cancer-type labels only; no ICI outcomes)

Sample rows mentioning each project (phenotype file; not an expression n):

| Project | Xena phenotype rows | GDC cases |
|---|---|---|
| LUAD | 705 | 585 |
| LUSC | 626 | 504 |
| SKCM | 480 | 470 |
| COAD | 548 | 461 |
| READ | 184 | 172 |
| BRCA | 1241 | 1098 |
| BLCA | 436 | 412 |

TCGA-BLCA available for Gate A: **True**

**ECS** (9/9 present)

| Gene | In matrix |
|---|---|
| `CNR1` | CNR1 |
| `CNR2` | CNR2 |
| `GPR55` | GPR55 |
| `TRPV1` | TRPV1 |
| `FAAH` | FAAH |
| `MGLL` | MGLL |
| `DAGLA` | DAGLA |
| `DAGLB` | DAGLB |
| `NAPEPLD` | NAPEPLD |

**B cell** (5/5 present)

| Gene | In matrix |
|---|---|
| `MS4A1` | MS4A1 |
| `CD19` | CD19 |
| `CD79A` | CD79A |
| `CD79B` | CD79B |
| `MZB1` | MZB1 |

**TLS** (4/4 present)

| Gene | In matrix |
|---|---|
| `CXCL13` | CXCL13 |
| `CCL19` | CCL19 |
| `CCL21` | CCL21 |
| `CCR7` | CCR7 |

**CD8** (5/5 present)

| Gene | In matrix |
|---|---|
| `CD8A` | CD8A |
| `CD8B` | CD8B |
| `GZMB` | GZMB |
| `PRF1` | PRF1 |
| `IFNG` | IFNG |


## 4. IMvigor210 (primary ICI) — pin only

- **Pin:** IMvigor210CoreBiologies_1.0.1.tar.gz
- **Local path:** `data/raw/imvigor210/IMvigor210CoreBiologies_1.0.1.tar.gz`
- **SHA256:** `890b80da68a837db6edbc1d348c53de4c7c8c7e9eddf3000bf26df5ef2b4668a`
- **Bytes:** 73683703
- **License:** Package LICENSE (PDF in tarball); published as CC BY 3.0 (Gene / medRxiv data statement)
- **Citation:** Mariathasan et al. Nature 2018; http://research-pub.gene.com/IMvigor210CoreBiologies/
- **Gene IDs:** HGNC symbols in cds ExpressionSet fData (symbol field)

**Must not (this unit):** open response/OS values for model shopping; plot response vs ECS / CNR2 / B-cell scores.

Phenotype / pData **column names only**:

- `ANONPT_ID`
- `Best Confirmed Overall Response`
- `binaryResponse`
- `IC Level`
- `os`
- `censOS`
- `Lund`
- `Lund2`
- `TCGA Subtype`
- `Enrollment IC`
- `Immune phenotype`
- `Sex`
- `Race`
- `Intravesical BCG administered`
- `Baseline ECOG Score`
- `Tobacco Use History`
- `Met Disease Status`
- `TC Level`
- `FMOne mutation burden per MB`
- `Sample age`
- `Tissue`
- `Received platinum`
- `Sample collected pre-platinum`

n phenotype rows (count only): None

**ECS** (9/9 present)

| Gene | In matrix |
|---|---|
| `CNR1` | CNR1 |
| `CNR2` | CNR2 |
| `GPR55` | GPR55 |
| `TRPV1` | TRPV1 |
| `FAAH` | FAAH |
| `MGLL` | MGLL |
| `DAGLA` | DAGLA |
| `DAGLB` | DAGLB |
| `NAPEPLD` | NAPEPLD |

**B cell** (5/5 present)

| Gene | In matrix |
|---|---|
| `MS4A1` | MS4A1 |
| `CD19` | CD19 |
| `CD79A` | CD79A |
| `CD79B` | CD79B |
| `MZB1` | MZB1 |

**TLS** (4/4 present)

| Gene | In matrix |
|---|---|
| `CXCL13` | CXCL13 |
| `CCL19` | CCL19 |
| `CCL21` | CCL21 |
| `CCR7` | CCR7 |

**CD8** (5/5 present)

| Gene | In matrix |
|---|---|
| `CD8A` | CD8A |
| `CD8B` | CD8B |
| `GZMB` | GZMB |
| `PRF1` | PRF1 |
| `IFNG` | IFNG |


## 5. Melanoma GEO (replication)

### GSE78220

- **Role:** replication ICI (descriptive; not Gate B rescue)
- **License:** NCBI GEO public; Hugo et al. Cell 2016; original paper license
- **Expression:** `data/raw/geo/GSE78220_PatientFPKM.xlsx` SHA256 `ae3b044f23a0a4cd2859da36726a220856c35216a169c17f93dfc3bd20b04de6`
- **Series matrix:** `data/raw/geo/GSE78220_series_matrix.txt.gz`
- **Gene IDs:** HGNC symbols (PatientFPKM.xlsx Gene column)
- **Matrix shape:** 25268 genes × 28 samples

Series-matrix characteristic **field names only** (no values):

- `age (yrs)`
- `anatomical location`
- `anti-pd-1 response`
- `biopsy time`
- `braf`
- `disease status`
- `gender`
- `nf1`
- `nras`
- `overall survival (days)`
- `patient id`
- `previous mapki`
- `stranded/unstranded rnaseq`
- `study site`
- `tissue`
- `treatment`
- `vital status`

**ECS** (9/9 present)

| Gene | In matrix |
|---|---|
| `CNR1` | CNR1 |
| `CNR2` | CNR2 |
| `GPR55` | GPR55 |
| `TRPV1` | TRPV1 |
| `FAAH` | FAAH |
| `MGLL` | MGLL |
| `DAGLA` | DAGLA |
| `DAGLB` | DAGLB |
| `NAPEPLD` | NAPEPLD |

**B cell** (5/5 present)

| Gene | In matrix |
|---|---|
| `MS4A1` | MS4A1 |
| `CD19` | CD19 |
| `CD79A` | CD79A |
| `CD79B` | CD79B |
| `MZB1` | MZB1 |

**TLS** (4/4 present)

| Gene | In matrix |
|---|---|
| `CXCL13` | CXCL13 |
| `CCL19` | CCL19 |
| `CCL21` | CCL21 |
| `CCR7` | CCR7 |

**CD8** (5/5 present)

| Gene | In matrix |
|---|---|
| `CD8A` | CD8A |
| `CD8B` | CD8B |
| `GZMB` | GZMB |
| `PRF1` | PRF1 |
| `IFNG` | IFNG |

### GSE91061

- **Role:** replication ICI (descriptive; not Gate B rescue)
- **License:** NCBI GEO public; Riaz et al. Cell 2017; original paper license
- **Expression:** `data/raw/geo/GSE91061_BMS038109Sample.hg19KnownGene.fpkm.csv.gz` SHA256 `987c7637e72ff5ad9c9630b0ee959064713cd8f57348d05003fb85a2f4cc43d5`
- **Series matrix:** `data/raw/geo/GSE91061_series_matrix.txt.gz`
- **Gene IDs:** NCBI Entrez gene IDs (column 0 of hg19KnownGene FPKM)
- **Matrix shape:** 22187 genes × 109 samples

Series-matrix characteristic **field names only** (no values):

- `response`
- `tissue`
- `visit (pre or on treatment)`

**ECS** (9/9 present)

| Gene | In matrix |
|---|---|
| `CNR1` | Entrez:1268 |
| `CNR2` | Entrez:1269 |
| `GPR55` | Entrez:9290 |
| `TRPV1` | Entrez:7442 |
| `FAAH` | Entrez:2166 |
| `MGLL` | Entrez:11343 |
| `DAGLA` | Entrez:747 |
| `DAGLB` | Entrez:221955 |
| `NAPEPLD` | Entrez:222236 |

**B cell** (5/5 present)

| Gene | In matrix |
|---|---|
| `MS4A1` | Entrez:931 |
| `CD19` | Entrez:930 |
| `CD79A` | Entrez:973 |
| `CD79B` | Entrez:974 |
| `MZB1` | Entrez:51237 |

**TLS** (4/4 present)

| Gene | In matrix |
|---|---|
| `CXCL13` | Entrez:10563 |
| `CCL19` | Entrez:6363 |
| `CCL21` | Entrez:6366 |
| `CCR7` | Entrez:1236 |

**CD8** (5/5 present)

| Gene | In matrix |
|---|---|
| `CD8A` | Entrez:925 |
| `CD8B` | Entrez:926 |
| `GZMB` | Entrez:3002 |
| `PRF1` | Entrez:5551 |
| `IFNG` | Entrez:3458 |


## Environment

- Python: 3.12.12
- uv lock present: True
- Packages: {'pandas': '3.0.5', 'pyarrow': '25.0.1', 'requests': '2.34.2', 'openpyxl': '3.1.5', 'rdata': '1.1.0', 'cellxgene-census': '1.18.0'}

## What was not done

- No ECS / CNR2 / B-cell scores computed.
- No response or OS value tabulation, plots, or models.
- IMvigor210 and GEO phenotype **values** were not written out.
- Full TCGA expression matrix not downloaded (Unit 04).
- Census counts not sliced to anndata (Unit 01).
