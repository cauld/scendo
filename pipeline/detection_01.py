#!/usr/bin/env python3
"""Unit 01 — Gate C detection rates. No ICI phenotype/outcome files."""

from __future__ import annotations

import json
import sys
import tarfile
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lineage import assign_bucket

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "pipeline" / "output" / "01"
RESEARCH = ROOT / "research" / "01-detection.md"
JSON_OUT = OUT_DIR / "01-detection.json"
CENSUS_VERSION = "2025-11-08"
GENES = ["CNR2", "MGLL", "FAAH"]
NON_B = ["Myeloid", "T/NK", "Malignant/epithelial", "Stromal/other"]
BUCKETS = ["B/plasma", *NON_B]

# Exact Census disease labels from Unit 00 + close variants. Substring used
# after fetch for ||-delimited fields. Uveal melanoma is excluded.
DISEASES = {
    "NSCLC": [
        "lung adenocarcinoma",
        "lung squamous cell carcinoma",
        "non-small cell lung carcinoma",
        "squamous cell lung carcinoma",
        "non-small cell lung cancer",
    ],
    "melanoma": [
        "melanoma",
        "metastatic melanoma",
        "cutaneous melanoma",
        "skin melanoma",
    ],
    "CRC": [
        "colon adenocarcinoma",
        "colorectal cancer",
        "colorectal carcinoma",
        "rectal adenocarcinoma",
        "colon cancer",
        "colorectal carcinoma || metastatic malignant neoplasm",
    ],
    "BRCA": [
        "breast cancer",
        "breast carcinoma",
        "invasive breast carcinoma",
        "breast invasive carcinoma",
        "HER2 positive breast carcinoma",
        "estrogen-receptor positive breast cancer",
        "invasive ductal breast carcinoma",
        "invasive lobular breast carcinoma",
        "luminal A breast carcinoma",
        "luminal B breast carcinoma",
        "triple-negative breast carcinoma",
        "metaplastic breast carcinoma",
        "invasive tubular breast carcinoma || invasive lobular breast carcinoma",
    ],
}


def _disease_type(disease: str) -> str | None:
    parts = [p.strip().lower() for p in str(disease).split("||")]
    # First match in type priority (NSCLC / melanoma / CRC / BRCA).
    for ctype, needles in DISEASES.items():
        for part in parts:
            if ctype == "melanoma" and "uveal" in part:
                continue
            for needle in needles:
                n = needle.lower()
                if "||" in n:
                    continue
                if n in part:
                    return ctype
    return None


def _detection_from_cells(cell_buckets: pd.Series, detected: dict[str, np.ndarray], cancer_type: str, source: str) -> pd.DataFrame:
    rows = []
    n_total = len(cell_buckets)
    for gene in GENES:
        flag = detected[gene]
        for bucket in BUCKETS:
            mask = cell_buckets.to_numpy() == bucket
            n = int(mask.sum())
            if n == 0:
                n_pos, pct = 0, np.nan
            else:
                n_pos = int(flag[mask].sum())
                pct = 100.0 * n_pos / n
            rows.append(
                {
                    "cancer_type": cancer_type,
                    "source": source,
                    "bucket": bucket,
                    "gene": gene,
                    "n_cells": n,
                    "n_detected": n_pos,
                    "pct_detected": pct,
                    "n_type": n_total,
                }
            )
    return pd.DataFrame(rows)


def _detection_from_adata(adata, cancer_type: str, source: str, label_col: str) -> pd.DataFrame:
    labels = adata.obs[label_col].astype(str)
    buckets = labels.map(assign_bucket)
    X = adata.X
    if sparse.issparse(X):
        X = X.tocsr()
        det = (X > 0).toarray()
    else:
        det = np.asarray(X) > 0
    if det.shape[1] != len(GENES):
        raise ValueError(f"expected {len(GENES)} gene columns, got {det.shape}")
    detected = {gene: det[:, i] for i, gene in enumerate(GENES)}
    return _detection_from_cells(buckets, detected, cancer_type, source)


def census_obs_filter(diseases: list[str]) -> str:
    quoted = ", ".join(repr(d) for d in diseases)
    return f"is_primary_data == True and disease in [{quoted}]"


def run_census() -> pd.DataFrame:
    import cellxgene_census
    import tiledbsoma as soma

    all_diseases = []
    for ds in DISEASES.values():
        all_diseases.extend(ds)
    all_diseases = list(dict.fromkeys(all_diseases))
    obs_filter = census_obs_filter(all_diseases)
    print(f"Census obs filter ({len(all_diseases)} disease labels) …", flush=True)

    with cellxgene_census.open_soma(census_version=CENSUS_VERSION) as census:
        hs = census["census_data"]["homo_sapiens"]
        query = hs.axis_query(
            measurement_name="RNA",
            obs_query=soma.AxisQuery(value_filter=obs_filter),
            var_query=soma.AxisQuery(value_filter=f"feature_name in {GENES}"),
        )
        print("  reading obs …", flush=True)
        obs = query.obs(column_names=["soma_joinid", "cell_type", "disease", "tissue_type"]).concat().to_pandas()
        print(f"  obs n={len(obs):,}", flush=True)
        var = query.var(column_names=["soma_joinid", "feature_name"]).concat().to_pandas()
        print(f"  var {list(var['feature_name'])}", flush=True)
        gid_to_gene = dict(zip(var["soma_joinid"].astype(int), var["feature_name"].astype(str)))

        if "tissue_type" in obs.columns:
            tt = obs["tissue_type"].astype(str).str.lower()
            obs = obs.loc[~tt.isin(["cell culture", "organoid", "cell line"])].copy()
        dise = obs["disease"].astype(str)
        obs = obs.loc[~dise.str.lower().str.contains("uveal")].copy()
        obs["cancer_type"] = dise.map(_disease_type)
        obs = obs.loc[obs["cancer_type"].notna()].copy()
        print(obs["cancer_type"].value_counts().to_string(), flush=True)

        obs = obs.sort_values("soma_joinid").reset_index(drop=True)
        join_to_row = {int(j): i for i, j in enumerate(obs["soma_joinid"].astype(int))}
        n = len(obs)
        detected = {g: np.zeros(n, dtype=bool) for g in GENES}
        nnz = 0
        print("  reading sparse X (3 genes) …", flush=True)
        for tbl in query.X("raw").tables():
            df = tbl.to_pandas()
            data_col = "soma_data" if "soma_data" in df.columns else df.columns[-1]
            dim0 = "soma_dim_0" if "soma_dim_0" in df.columns else df.columns[0]
            dim1 = "soma_dim_1" if "soma_dim_1" in df.columns else df.columns[1]
            hit = df.loc[df[data_col] > 0]
            nnz += int(len(hit))
            if hit.empty:
                continue
            rows = hit[dim0].astype(int).map(join_to_row)
            genes = hit[dim1].astype(int).map(gid_to_gene)
            ok = rows.notna() & genes.notna()
            tmp = pd.DataFrame({"row": rows[ok].astype(int), "gene": genes[ok]})
            for gene, sub in tmp.groupby("gene", sort=False):
                detected[str(gene)][sub["row"].to_numpy()] = True
        print(f"  nnz counts > 0: {nnz:,}", flush=True)

    obs["bucket"] = obs["cell_type"].map(assign_bucket)
    frames = []
    for ctype, sub in obs.groupby("cancer_type", sort=False):
        idx = sub.index.to_numpy()
        det = {g: detected[g][idx] for g in GENES}
        frames.append(_detection_from_cells(sub["bucket"], det, ctype, "Census"))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def load_gse130001_counts() -> tuple[sparse.spmatrix, list[str], list[str]]:
    """Genes x cells CSC from GEO 10x MTX; barcodes as sampleN@barcode to match TISCH2."""
    raw = ROOT / "data" / "raw" / "geo" / "GSE130001"
    tar_path = raw / "GSE130001_RAW.tar"
    extract = raw / "extract"
    extract.mkdir(parents=True, exist_ok=True)
    if not (extract / "GSM3729178_sample1_matrix.mtx.gz").exists():
        with tarfile.open(tar_path) as tf:
            tf.extractall(extract)
    from scipy.io import mmread

    parts_x = []
    parts_bc = []
    symbols = None
    for sample in ("sample1", "sample2"):
        gsm = "GSM3729178" if sample == "sample1" else "GSM3729179"
        mtx = extract / f"{gsm}_{sample}_matrix.mtx.gz"
        genes_file = extract / f"{gsm}_{sample}_genes.tsv.gz"
        bc_file = extract / f"{gsm}_{sample}_barcodes.tsv.gz"
        mat = mmread(mtx).tocsc()
        genes = pd.read_csv(genes_file, sep="\t", header=None)
        bcs = pd.read_csv(bc_file, sep="\t", header=None)[0].astype(str).tolist()
        if genes.shape[1] >= 2:
            sym = genes.iloc[:, 1].astype(str).tolist()
        else:
            sym = genes.iloc[:, 0].astype(str).tolist()
        if mat.shape[0] != len(sym) and mat.shape[1] == len(sym):
            mat = mat.T.tocsc()
        if symbols is None:
            symbols = sym
        elif symbols != sym:
            raise ValueError(f"{sample} gene list differs from sample1")
        parts_x.append(mat)
        parts_bc.extend([f"{sample}@{b}" for b in bcs])
    mat = sparse.hstack(parts_x).tocsc()
    return mat, symbols, parts_bc


def run_tisch_blca() -> pd.DataFrame:
    meta_path = ROOT / "data" / "raw" / "tisch2" / "BLCA_GSE130001_CellMetainfo_table.tsv"
    meta = pd.read_csv(meta_path, sep="\t")
    mat, symbols, barcodes = load_gse130001_counts()
    sym_u = [s.upper() for s in symbols]
    gene_idx = {}
    for g in GENES:
        if g in {s.upper() for s in symbols}:
            gene_idx[g] = [i for i, s in enumerate(sym_u) if s == g][0]
        else:
            raise KeyError(f"{g} missing from GSE130001")

    # Match TISCH2 cell ids to GEO barcodes.
    # TISCH: sample1@AACTCCCCAAACGCGA-1
    tisch_cells = meta["Cell"].astype(str)
    geo_map = {b: i for i, b in enumerate(barcodes)}
    matched = tisch_cells.map(geo_map)
    n_match = int(matched.notna().sum())
    print(f"TISCH2–GEO barcode match: {n_match}/{len(meta)}", flush=True)
    if n_match < 0.5 * len(meta):
        tisch_bc = tisch_cells.str.split("@").str[-1]
        geo_plain = {b.split("@")[-1]: i for i, b in enumerate(barcodes)}
        matched = tisch_bc.map(geo_plain)
        print(f"  fallback barcode-only match: {int(matched.notna().sum())}/{len(meta)}", flush=True)
    keep = matched.notna()
    meta_k = meta.loc[keep].copy()
    cols = matched.loc[keep].astype(int).to_numpy()
    label_col = "Celltype (major-lineage)" if "Celltype (major-lineage)" in meta.columns else meta.columns[4]
    # Build a fake AnnData-like for detection
    X = np.vstack([np.asarray(mat[gene_idx[g], cols].todense()).ravel() for g in GENES]).T
    class _A:
        pass

    a = _A()
    a.obs = pd.DataFrame({label_col: meta_k[label_col].astype(str).values})
    a.X = X
    return _detection_from_adata(a, "BLCA", "TISCH2+GEO GSE130001", label_col)


def gate_c(table: pd.DataFrame) -> dict:
    # Present buckets: n_cells > 0 for CNR2 row (same n for all genes).
    sub = table[table["gene"] == "CNR2"].copy()
    present = sub[sub["n_cells"] > 0]
    non_b = present[present["bucket"].isin(NON_B)]

    def all_below(df: pd.DataFrame, gene: str, thresh: float) -> bool:
        g = df[df["gene"] == gene]
        g = g[g["n_cells"] > 0]
        g = g[g["bucket"].isin(NON_B)]
        if g.empty:
            return True
        return bool((g["pct_detected"] < thresh).all())

    cnr2_dark = all_below(table, "CNR2", 1.0)
    mgll_dark = all_below(table, "MGLL", 5.0)
    faah_dark = all_below(table, "FAAH", 5.0)
    return {
        "types": sorted(table["cancer_type"].unique().tolist()),
        "n_types": table["cancer_type"].nunique(),
        "non_b_bucket_rows": int(len(non_b)),
        "no_raw_cnr2_umap_atlas": cnr2_dark,
        "mgll_all_nonb_lt_5": mgll_dark,
        "faah_all_nonb_lt_5": faah_dark,
        "stop_kill_detection_half": cnr2_dark and mgll_dark and faah_dark,
        "stop_kill_needs_unit_02_ecs_state": True,
        "note": (
            "Gate C stop-kill also requires no non-B ECS state (Unit 02). "
            "If the detection half is false, stop-kill cannot fire."
        ),
    }


def write_markdown(table: pd.DataFrame, gates: dict) -> str:
    lines = [
        "# Unit 01 — Detection rates (Gate C)",
        "",
        f"**Run date:** {date.today().isoformat()}  ",
        f"**Census version:** `{CENSUS_VERSION}`  ",
        f"**Protocol SHA:** `3fbf310870c57247163edca35ed536ade3ea4301`  ",
        "**Rule:** % cells with raw count > 0. No ICI labels. No UMAP.",
        "",
        "## Sources",
        "",
        "- NSCLC, melanoma, CRC, BRCA: CELLxGENE Census, `is_primary_data == True`, raw RNA counts.",
        "- BLCA: TISCH2 `BLCA_GSE130001` cell types + GEO `GSE130001` MTX counts (barcode-matched).",
        "- Lineage buckets: locked substring map in `PROTOCOL.md` / `pipeline/lineage.py`.",
        "",
        f"Types available: **{gates['n_types']}** ({', '.join(gates['types'])}). Minimum ≥2: **{gates['n_types'] >= 2}**.",
        "",
        "## Detection table",
        "",
        "| Type | Source | Bucket | n | CNR2 % | MGLL % | FAAH % |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    # Pivot for display
    for (ctype, source, bucket), g in table.groupby(["cancer_type", "source", "bucket"], sort=False):
        n = int(g["n_cells"].iloc[0])
        pct = {row.gene: row.pct_detected for row in g.itertuples()}
        def fmt(p):
            return "—" if pd.isna(p) else f"{p:.2f}"
        lines.append(
            f"| {ctype} | {source} | {bucket} | {n} | {fmt(pct.get('CNR2'))} | {fmt(pct.get('MGLL'))} | {fmt(pct.get('FAAH'))} |"
        )
    lines += [
        "",
        "## Gate C draft (human marks)",
        "",
        f"- **No raw-*CNR2*-UMAP atlas:** {gates['no_raw_cnr2_umap_atlas']}  ",
        "  *(true iff CNR2 % < 1 in every non-B/plasma lineage with n>0 in every type)*",
        f"- MGLL < 5% in every non-B lineage in every type: **{gates['mgll_all_nonb_lt_5']}**",
        f"- FAAH < 5% in every non-B lineage in every type: **{gates['faah_all_nonb_lt_5']}**",
        f"- Detection half of stop-kill (CNR2 dark **and** both enzymes dark): **{gates['stop_kill_detection_half']}**",
        "",
        gates["note"],
        "",
        "## Human Gate C",
        "",
        "- [ ] Pass / continue (do not stop the kill on detectability)",
        "- [ ] No raw-*CNR2*-UMAP atlas (CNR2 < 1% rule)",
        "- [ ] Fail (stop the kill) — only if detection half **and** Unit 02 finds no non-B ECS state",
        "",
        "## What was not done",
        "",
        "- No ICI phenotype or outcome files opened.",
        "- No UMAP. No nine-gene ECS-state test (Unit 02).",
        "- No TCGA or IMvigor210 scores.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    census_path = OUT_DIR / "census_detection.parquet"
    tisch_path = OUT_DIR / "blca_detection.parquet"
    if census_path.exists():
        print("Loading cached Census table", flush=True)
        census = pd.read_parquet(census_path)
    else:
        census = run_census()
        census.to_parquet(census_path, index=False)
    if tisch_path.exists():
        print("Loading cached BLCA table", flush=True)
        blca = pd.read_parquet(tisch_path)
    else:
        print("BLCA TISCH2+GEO …", flush=True)
        blca = run_tisch_blca()
        blca.to_parquet(tisch_path, index=False)
    table = pd.concat([census, blca], ignore_index=True)
    table.to_csv(OUT_DIR / "detection.csv", index=False)
    gates = gate_c(table)
    payload = {
        "run_date": date.today().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "census_version": CENSUS_VERSION,
        "gates": gates,
        "table": table.to_dict(orient="records"),
    }
    JSON_OUT.write_text(json.dumps(payload, indent=2, default=str))
    RESEARCH.write_text(write_markdown(table, gates))
    print(f"Wrote {RESEARCH}", flush=True)
    print(json.dumps(gates, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
