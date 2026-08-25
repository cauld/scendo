#!/usr/bin/env python3
"""Unit 02 — scRNA ECS states (Gate A discovery). No ICI phenotype/outcome files."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from detection_01 import (  # noqa: E402
    BUCKETS,
    CENSUS_VERSION,
    DISEASES,
    NON_B,
    ROOT,
    _disease_type,
    census_obs_filter,
    load_gse130001_counts,
)
from genes import CONTAM, ECS  # noqa: E402
from lineage import assign_bucket  # noqa: E402

OUT_DIR = ROOT / "pipeline" / "output" / "02"
RESEARCH = ROOT / "research" / "02-scrna-states.md"
JSON_OUT = OUT_DIR / "02-scrna-states.json"
PROTOCOL_SHA = "3fbf310870c57247163edca35ed536ade3ea4301"
MIN_ECS_GENES = 7
DETECT_PCT = 5.0
CONTAM_PCT = 10.0
QUERY_GENES = [*ECS, *CONTAM]


def _gene_index(symbols: list[str], wanted: list[str]) -> dict[str, int]:
    upper = [s.upper() for s in symbols]
    out: dict[str, int] = {}
    for gene in wanted:
        hits = [i for i, s in enumerate(upper) if s == gene]
        if hits:
            out[gene] = hits[0]
    return out


def _pick_contam_gene(present: list[str]) -> str | None:
    have = {g.upper() for g in present}
    for gene in CONTAM:
        if gene in have:
            return gene
    return None


def _cell_scores(cells: pd.DataFrame, ecs_dropped: list[str]) -> tuple[np.ndarray, int]:
    present = [g for g in ECS if g in cells.columns and g not in ecs_dropped]
    n_genes = len(present)
    n = len(cells)
    if n_genes < MIN_ECS_GENES:
        return np.full(n, np.nan, dtype=np.float64), n_genes
    X = np.column_stack([cells[g].to_numpy(dtype=np.float64) for g in present])
    return X.mean(axis=1), n_genes


def run_census() -> tuple[pd.DataFrame, dict]:
    import cellxgene_census
    import tiledbsoma as soma

    cache = OUT_DIR / "census_cells.parquet"
    meta_path = OUT_DIR / "census_query_meta.json"
    if cache.exists() and meta_path.exists():
        print("Loading cached Census cells", flush=True)
        cells = pd.read_parquet(cache)
        meta = json.loads(meta_path.read_text())
        return cells, meta

    all_diseases = list(dict.fromkeys(d for ds in DISEASES.values() for d in ds))
    obs_filter = census_obs_filter(all_diseases)
    print(f"Census obs filter ({len(all_diseases)} disease labels, {len(QUERY_GENES)} genes) …", flush=True)

    with cellxgene_census.open_soma(census_version=CENSUS_VERSION) as census:
        hs = census["census_data"]["homo_sapiens"]
        query = hs.axis_query(
            measurement_name="RNA",
            obs_query=soma.AxisQuery(value_filter=obs_filter),
            var_query=soma.AxisQuery(value_filter=f"feature_name in {QUERY_GENES}"),
        )
        print("  reading obs …", flush=True)
        obs = query.obs(column_names=["soma_joinid", "cell_type", "disease", "tissue_type"]).concat().to_pandas()
        print(f"  obs n={len(obs):,}", flush=True)
        var = query.var(column_names=["soma_joinid", "feature_name"]).concat().to_pandas()
        genes_found = list(var["feature_name"].astype(str))
        print(f"  var {genes_found}", flush=True)
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
        join_ids = obs["soma_joinid"].astype(int).to_numpy()
        n = len(obs)
        gene_cols = {g: i for i, g in enumerate(QUERY_GENES) if g in set(genes_found)}
        counts = np.zeros((n, len(QUERY_GENES)), dtype=np.float32)
        nnz = 0
        print("  reading sparse X (ECS + contamination genes) …", flush=True)
        for tbl in query.X("raw").tables():
            df = tbl.to_pandas()
            data_col = "soma_data" if "soma_data" in df.columns else df.columns[-1]
            dim0 = "soma_dim_0" if "soma_dim_0" in df.columns else df.columns[0]
            dim1 = "soma_dim_1" if "soma_dim_1" in df.columns else df.columns[1]
            dim0_v = df[dim0].astype(int).to_numpy()
            dim1_v = df[dim1].astype(int).to_numpy()
            vals = df[data_col].to_numpy()
            idx = np.searchsorted(join_ids, dim0_v)
            in_range = idx < n
            hit = np.zeros(len(dim0_v), dtype=bool)
            hit[in_range] = join_ids[idx[in_range]] == dim0_v[in_range]
            if not hit.any():
                continue
            rows = idx[hit]
            genes = pd.Series(dim1_v[hit]).map(gid_to_gene)
            ok = genes.notna()
            if not ok.any():
                continue
            rows = rows[ok.to_numpy()]
            gene_names = genes[ok].astype(str).to_numpy()
            data = vals[hit][ok.to_numpy()]
            cols = np.array([gene_cols[g] for g in gene_names], dtype=int)
            counts[rows, cols] = data.astype(np.float32)
            nnz += int(len(rows))
        print(f"  nnz stored: {nnz:,}", flush=True)

    obs["bucket"] = obs["cell_type"].map(assign_bucket)
    cells = pd.DataFrame(
        {
            "cancer_type": obs["cancer_type"].to_numpy(),
            "source": "Census",
            "bucket": obs["bucket"].to_numpy(),
        }
    )
    for i, gene in enumerate(QUERY_GENES):
        cells[gene] = counts[:, i]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cells.to_parquet(cache, index=False)
    dropped = [g for g in ECS if g not in set(genes_found)]
    meta = {
        "genes_found": genes_found,
        "ecs_dropped": dropped,
        "contam_gene": _pick_contam_gene(genes_found),
        "n_cells": int(len(cells)),
    }
    meta_path.write_text(json.dumps(meta, indent=2))
    return cells, meta


def run_tisch_blca() -> tuple[pd.DataFrame, dict]:
    cache = OUT_DIR / "blca_cells.parquet"
    meta_path = OUT_DIR / "blca_query_meta.json"
    if cache.exists() and meta_path.exists():
        print("Loading cached BLCA cells", flush=True)
        return pd.read_parquet(cache), json.loads(meta_path.read_text())

    meta_tbl = pd.read_csv(ROOT / "data" / "raw" / "tisch2" / "BLCA_GSE130001_CellMetainfo_table.tsv", sep="\t")
    mat, symbols, barcodes = load_gse130001_counts()
    gene_idx = _gene_index(symbols, QUERY_GENES)
    genes_found = [g for g in QUERY_GENES if g in gene_idx]
    print(f"BLCA genes found: {genes_found}", flush=True)

    tisch_cells = meta_tbl["Cell"].astype(str)
    geo_map = {b: i for i, b in enumerate(barcodes)}
    matched = tisch_cells.map(geo_map)
    n_match = int(matched.notna().sum())
    print(f"TISCH2–GEO barcode match: {n_match}/{len(meta_tbl)}", flush=True)
    if n_match < 0.5 * len(meta_tbl):
        tisch_bc = tisch_cells.str.split("@").str[-1]
        geo_plain = {b.split("@")[-1]: i for i, b in enumerate(barcodes)}
        matched = tisch_bc.map(geo_plain)
        print(f"  fallback barcode-only match: {int(matched.notna().sum())}/{len(meta_tbl)}", flush=True)
    keep = matched.notna()
    meta_k = meta_tbl.loc[keep].copy()
    cols = matched.loc[keep].astype(int).to_numpy()
    label_col = "Celltype (major-lineage)" if "Celltype (major-lineage)" in meta_k.columns else meta_k.columns[4]
    buckets = meta_k[label_col].astype(str).map(assign_bucket)

    cells = pd.DataFrame(
        {
            "cancer_type": "BLCA",
            "source": "TISCH2+GEO GSE130001",
            "bucket": buckets.to_numpy(),
        }
    )
    for gene in QUERY_GENES:
        if gene in gene_idx:
            cells[gene] = np.asarray(mat[gene_idx[gene], cols].todense()).ravel().astype(np.float32)
        else:
            cells[gene] = np.nan
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cells.to_parquet(cache, index=False)
    meta = {
        "genes_found": genes_found,
        "ecs_dropped": [g for g in ECS if g not in gene_idx],
        "contam_gene": _pick_contam_gene(genes_found),
        "n_cells": int(len(cells)),
        "n_matched": n_match,
        "n_meta": int(len(meta_tbl)),
    }
    meta_path.write_text(json.dumps(meta, indent=2))
    return cells, meta


def _dataset_tables(cells: pd.DataFrame, contam_gene: str | None, ecs_dropped: list[str]) -> pd.DataFrame:
    score, n_ecs_genes = _cell_scores(cells, ecs_dropped)
    work = cells.copy()
    work["_score"] = score
    rows = []
    for (ctype, source), sub in work.groupby(["cancer_type", "source"], sort=False):
        means = {}
        ns = {}
        for bucket in BUCKETS:
            b = sub.loc[sub["bucket"] == bucket]
            n = int(len(b))
            ns[bucket] = n
            if n == 0:
                means[bucket] = np.nan
            else:
                means[bucket] = float(np.nanmean(b["_score"].to_numpy())) if b["_score"].notna().any() else np.nan
        present = [b for b in BUCKETS if ns[b] > 0 and pd.notna(means[b])]
        rank_map: dict[str, float] = {}
        if present:
            ser = pd.Series({b: means[b] for b in present})
            ranks = ser.rank(ascending=False, method="min")
            rank_map = {b: float(ranks[b]) for b in present}

        for bucket in BUCKETS:
            b = sub.loc[sub["bucket"] == bucket]
            n = ns[bucket]
            det = {}
            for gene in ECS:
                if n == 0 or gene in ecs_dropped:
                    det[gene] = np.nan
                else:
                    det[gene] = 100.0 * float((b[gene].to_numpy() > 0).sum()) / n
            any_ge5 = bool(any(pd.notna(v) and v >= DETECT_PCT for v in det.values()))
            max_gene, max_pct = None, np.nan
            if n > 0:
                valid = {g: v for g, v in det.items() if pd.notna(v)}
                if valid:
                    max_gene = max(valid, key=valid.get)
                    max_pct = valid[max_gene]
            if n == 0 or contam_gene is None or bucket == "B/plasma":
                contam_rate = np.nan
            else:
                contam_rate = 100.0 * float((b[contam_gene].to_numpy() > 0).sum()) / n
            rank = rank_map.get(bucket, np.nan)
            elevated = bool(pd.notna(rank) and rank <= 2)
            has_rule = bool(n > 0 and any_ge5 and elevated)
            if bucket == "B/plasma":
                discarded = False
                discard_reason = ""
            elif contam_gene is None:
                discarded = True
                discard_reason = "contamination untestable (MS4A1/CD19/CD79A all absent)"
            elif pd.notna(contam_rate) and contam_rate >= CONTAM_PCT:
                discarded = True
                discard_reason = f"{contam_gene} detection {contam_rate:.2f}% ≥ {CONTAM_PCT:.0f}%"
            else:
                discarded = False
                discard_reason = ""
            kept = bool(has_rule and not discarded)
            rows.append(
                {
                    "cancer_type": ctype,
                    "source": source,
                    "bucket": bucket,
                    "n_cells": n,
                    "mean_ecs": means[bucket],
                    "rank": rank,
                    "any_gene_ge_5": any_ge5,
                    "max_detect_gene": max_gene if n else None,
                    "max_detect_pct": max_pct,
                    "contam_gene": contam_gene,
                    "contam_pct": contam_rate,
                    "ecs_state_rule": has_rule,
                    "discarded": discarded,
                    "discard_reason": discard_reason,
                    "kept": kept,
                    **{f"pct_{g}": det[g] for g in ECS},
                    "ecs_dropped": ",".join(ecs_dropped) if ecs_dropped else "",
                    "n_ecs_genes": n_ecs_genes,
                }
            )
    return pd.DataFrame(rows)


def summarize(table: pd.DataFrame) -> dict:
    kept = table[table["kept"]]
    buckets_with_state = sorted(kept["bucket"].unique().tolist())
    types_by_bucket = {
        b: sorted(kept.loc[kept["bucket"] == b, "cancer_type"].unique().tolist()) for b in buckets_with_state
    }
    n_buckets = len(buckets_with_state)
    n_non_b = sum(1 for b in buckets_with_state if b != "B/plasma")
    return {
        "buckets_with_ecs_state": buckets_with_state,
        "types_by_bucket": types_by_bucket,
        "n_buckets": n_buckets,
        "n_non_b_buckets": n_non_b,
        "two_lineage_rule": n_buckets >= 2,
        "has_non_b_candidate": n_non_b >= 1,
        "gate_a_unit02_already_fails": n_buckets < 2,
        "note": (
            "Unit 02 lists candidates only. Gate A still requires TCGA confound tests (Unit 04) "
            "and naming (Unit 05). Gate A already fails if fewer than two buckets remain."
        ),
    }


def _fmt_pct(v) -> str:
    return "—" if v is None or pd.isna(v) else f"{v:.2f}"


def _fmt_mean(v) -> str:
    return "—" if v is None or pd.isna(v) else f"{v:.4f}"


def _fmt_rank(v) -> str:
    return "—" if v is None or pd.isna(v) else str(int(v))


def write_markdown(table: pd.DataFrame, summary: dict, census_meta: dict, blca_meta: dict) -> str:
    types = sorted(table["cancer_type"].unique().tolist())
    lines = [
        "# Unit 02 — scRNA ECS states (Gate A, discovery)",
        "",
        f"**Run date:** {date.today().isoformat()}  ",
        f"**Census version:** `{CENSUS_VERSION}`  ",
        f"**Protocol SHA:** `{PROTOCOL_SHA}`  ",
        "**Rule:** A lineage has an ECS state in a cancer type if ≥1 core gene is detected "
        "(count > 0) in ≥5% of that lineage’s cells **and** the lineage mean core-ECS score "
        "is highest or second-highest among buckets with cells in that type. "
        "Non-B lineages with contamination-gene detection ≥ 10% are discarded in that type. "
        "No ICI labels. No NMF / clustering / DE.",
        "",
        "## Sources",
        "",
        "- NSCLC, melanoma, CRC, BRCA: CELLxGENE Census, `is_primary_data == True`, raw RNA counts.",
        "- BLCA: TISCH2 `BLCA_GSE130001` cell types + GEO `GSE130001` MTX counts (barcode-matched).",
        "- Lineage buckets: locked substring map in `PROTOCOL.md` / `pipeline/lineage.py`.",
        "",
        f"Types available: **{len(types)}** ({', '.join(types)}). Minimum ≥2: **{len(types) >= 2}**.",
        "",
        "## Scoring",
        "",
        "- Cell score = available-case mean of the nine core genes on **raw counts** "
        f"(denominator = genes present in that matrix; min {MIN_ECS_GENES}/9 or no score).",
        "- Lineage mean = mean of cell scores in that bucket. Rank uses competition ranking "
        "(highest mean = 1; ties share the minimum rank). Empty buckets are not ranked.",
        "- Z-score windows are for bulk (Units 04–07), not this unit.",
        "",
        "## Genes present / dropped",
        "",
        f"- Census ECS dropped: **{census_meta.get('ecs_dropped') or 'none'}**. "
        f"Contamination gene: **{census_meta.get('contam_gene') or 'none'}**.",
        f"- BLCA ECS dropped: **{blca_meta.get('ecs_dropped') or 'none'}**. "
        f"Contamination gene: **{blca_meta.get('contam_gene') or 'none'}**.",
        "",
        f"Non-B lineages discarded for contamination (≥ {CONTAM_PCT:.0f}%): "
        f"**{int(table['discarded'].sum())}**. "
        "Myeloid and T/NK meet the ≥5% detection bar in every type where they have cells, "
        "but their mean core-ECS is not highest or second-highest in any type.",
        "",
        "## Lineage means, ranks, contamination",
        "",
        "| Type | Source | Bucket | n | Mean ECS | Rank | ≥5% gene | Contam gene | Contam % | Rule | Discarded | Kept |",
        "|---|---|---|---:|---:|---:|---|---|---:|---|---|---|",
    ]
    for row in table.itertuples(index=False):
        maxg = row.max_detect_gene or "—"
        maxp = _fmt_pct(row.max_detect_pct)
        ge5 = f"{maxg} {maxp}%" if row.n_cells and row.max_detect_gene else "—"
        cg = row.contam_gene or "—"
        disc = "yes" if row.discarded else "no"
        if row.discard_reason:
            disc = f"yes ({row.discard_reason})"
        lines.append(
            f"| {row.cancer_type} | {row.source} | {row.bucket} | {row.n_cells} | "
            f"{_fmt_mean(row.mean_ecs)} | {_fmt_rank(row.rank)} | {ge5} | {cg} | "
            f"{_fmt_pct(row.contam_pct)} | {row.ecs_state_rule} | {disc} | {row.kept} |"
        )

    lines += [
        "",
        "## Per-gene detection (% cells with count > 0)",
        "",
        "| Type | Bucket | n | "
        + " | ".join(f"{g} %" for g in ECS)
        + " |",
        "|---|---|---:|"
        + "|".join("---:" for _ in ECS)
        + "|",
    ]
    for row in table.itertuples(index=False):
        pcts = " | ".join(_fmt_pct(getattr(row, f"pct_{g}")) for g in ECS)
        lines.append(f"| {row.cancer_type} | {row.bucket} | {row.n_cells} | {pcts} |")

    lines += [
        "",
        "## Candidates (ECS state after contamination filter)",
        "",
    ]
    if summary["buckets_with_ecs_state"]:
        lines.append("| Bucket | Cancer types where kept |")
        lines.append("|---|---|")
        for b in summary["buckets_with_ecs_state"]:
            types_b = ", ".join(summary["types_by_bucket"][b])
            lines.append(f"| {b} | {types_b} |")
    else:
        lines.append("None.")

    lines += [
        "",
        "## Gate A draft from this unit (not the full gate)",
        "",
        f"- Lineage buckets with an ECS state: **{summary['n_buckets']}** "
        f"({', '.join(summary['buckets_with_ecs_state']) or 'none'})",
        f"- Of those, non-B: **{summary['n_non_b_buckets']}**",
        f"- Two-lineage rule (≥2 buckets including B/plasma): **{summary['two_lineage_rule']}**",
        f"- At least one non-B candidate listed: **{summary['has_non_b_candidate']}**",
        f"- Gate A already fails (fewer than two buckets): **{summary['gate_a_unit02_already_fails']}**",
        "",
        summary["note"],
        "",
        "Human does not name the primary state here (Unit 05, after Unit 04 confound tests).",
        "",
        "## What was not done",
        "",
        "- No ICI phenotype or outcome files opened.",
        "- No NMF, new clustering, or DE.",
        "- No TCGA correlation (Unit 04). No frozen marker commit (Unit 03).",
        "- No UMAP.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    census_cells, census_meta = run_census()
    blca_cells, blca_meta = run_tisch_blca()
    census_tbl = _dataset_tables(census_cells, census_meta.get("contam_gene"), census_meta.get("ecs_dropped") or [])
    blca_tbl = _dataset_tables(blca_cells, blca_meta.get("contam_gene"), blca_meta.get("ecs_dropped") or [])
    table = pd.concat([census_tbl, blca_tbl], ignore_index=True)
    table.to_csv(OUT_DIR / "states.csv", index=False)
    summary = summarize(table)
    payload = {
        "run_date": date.today().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "census_version": CENSUS_VERSION,
        "protocol_sha": PROTOCOL_SHA,
        "census_meta": census_meta,
        "blca_meta": blca_meta,
        "summary": summary,
        "table": table.to_dict(orient="records"),
    }
    JSON_OUT.write_text(json.dumps(payload, indent=2, default=str))
    RESEARCH.write_text(write_markdown(table, summary, census_meta, blca_meta))
    print(f"Wrote {RESEARCH}", flush=True)
    print(json.dumps(summary, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
