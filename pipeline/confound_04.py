#!/usr/bin/env python3
"""Unit 04 — TCGA confound (Gate A). No ICI phenotype/outcome files. Do not name the primary state."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from genes import B_CELL, ECS, TLS  # noqa: E402
from inventory_00 import TCGA_DISEASE  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "research" / "03-frozen-markers.json"
PHENO = ROOT / "data" / "raw" / "xena" / "TCGA_phenotype_denseDataOnlyDownload.tsv.gz"
PROBEMAP = ROOT / "data" / "raw" / "xena" / "gencode.v23.annotation.gene.probemap"
OUT_DIR = ROOT / "pipeline" / "output" / "04"
CACHE = OUT_DIR / "tcga_signature_genes.parquet"
META = OUT_DIR / "tcga_query_meta.json"
RESEARCH = ROOT / "research" / "04-tcga-confound.md"
JSON_OUT = OUT_DIR / "04-tcga-confound.json"

PROTOCOL_SHA = "3fbf310870c57247163edca35ed536ade3ea4301"
XENA_HOST = "https://toil.xenahubs.net"
XENA_DATASET = "tcga_RSEM_gene_tpm"
MIN_ECS, MIN_B, MIN_TLS = 7, 3, 3
R_PASS = 0.6
R_CEILING = 0.75
SD_RATIO_MIN = 0.5
SCORE_GENES = [*ECS, *B_CELL, *TLS]
PROJECT_TO_TYPE = {
    "LUAD": "NSCLC",
    "LUSC": "NSCLC",
    "SKCM": "melanoma",
    "COAD": "CRC",
    "READ": "CRC",
    "BRCA": "BRCA",
    "BLCA": "BLCA",
}


def _lisp_str_array(xs: list[str]) -> str:
    return "[" + " ".join(json.dumps(x) for x in xs) + "]"


def _pearson(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    x = x - x.mean()
    y = y - y.mean()
    denom = float(np.sqrt((x * x).sum() * (y * y).sum()))
    if denom == 0:
        return float("nan")
    return float((x * y).sum() / denom)


def _spearman(x: np.ndarray, y: np.ndarray) -> float:
    rx = pd.Series(x).rank(method="average").to_numpy(dtype=np.float64)
    ry = pd.Series(y).rank(method="average").to_numpy(dtype=np.float64)
    return _pearson(rx, ry)


def load_frozen() -> dict:
    if not FROZEN.exists():
        raise SystemExit(f"Missing Unit 03 freeze: {FROZEN}")
    frozen = json.loads(FROZEN.read_text())
    genes = frozen["marker_list"]["genes"]
    if genes != ECS:
        raise SystemExit(f"Frozen genes drifted from protocol: {genes}")
    lineages = frozen["marker_list"]["lineages"]
    non_b = [b for b in lineages if b != "B/plasma"]
    if not non_b:
        raise SystemExit("No non-B candidate lineages in the freeze")
    return frozen


def probe_ids(frozen: dict) -> dict[str, str]:
    pm = pd.read_csv(PROBEMAP, sep="\t")
    pm["ens_bare"] = pm["id"].astype(str).str.split(".").str[0]
    out: dict[str, str] = {}
    for gene in SCORE_GENES:
        ens = (frozen.get("hgnc_aliases") or {}).get(gene, {}).get("ensembl")
        if ens:
            hit = pm.loc[pm["ens_bare"] == ens]
        else:
            hit = pm.loc[pm["gene"].astype(str).str.upper() == gene]
        if hit.empty:
            raise SystemExit(f"No probeMap row for {gene} ({ens})")
        out[gene] = str(hit.iloc[0]["id"])
    return out


def load_phenotype() -> pd.DataFrame:
    ph = pd.read_csv(PHENO, sep="\t", compression="gzip")
    inv = {v: k for k, v in TCGA_DISEASE.items()}
    ph = ph.loc[ph["_primary_disease"].isin(TCGA_DISEASE.values())].copy()
    ph["project"] = ph["_primary_disease"].map(inv)
    ph["cancer_type"] = ph["project"].map(PROJECT_TO_TYPE)
    ph["sample"] = ph["sample"].astype(str)
    return ph.reset_index(drop=True)


def xena_fetch(probes: list[str], samples: list[str], chunk: int = 800) -> pd.DataFrame:
    rows = []
    for i in range(0, len(samples), chunk):
        batch = samples[i : i + chunk]
        query = (
            '(fetch [{:table '
            + json.dumps(XENA_DATASET)
            + " :columns "
            + _lisp_str_array(probes)
            + " :samples "
            + _lisp_str_array(batch)
            + "}])"
        )
        print(f"  Xena fetch samples {i + 1}–{i + len(batch)} / {len(samples)}", flush=True)
        r = requests.post(
            XENA_HOST + "/data/",
            data=query.encode(),
            headers={"Content-Type": "text/plain"},
            timeout=180,
        )
        r.raise_for_status()
        block = json.loads(r.text)
        if not isinstance(block, list) or len(block) != len(probes):
            raise SystemExit(f"Unexpected Xena shape: {type(block)} len={getattr(block, '__len__', None)}")
        part = pd.DataFrame({p: np.asarray(vals, dtype=np.float64) for p, vals in zip(probes, block)}, index=batch)
        rows.append(part)
    return pd.concat(rows)


def load_expression(probes: dict[str, str], samples: list[str]) -> tuple[pd.DataFrame, dict]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    probe_list = [probes[g] for g in SCORE_GENES]
    if CACHE.exists() and META.exists():
        meta = json.loads(META.read_text())
        if meta.get("probes") == probes and meta.get("n_samples_requested") == len(samples):
            print("Loading cached TCGA signature matrix", flush=True)
            expr = pd.read_parquet(CACHE)
            return expr, meta
    print(f"Querying Xena {XENA_DATASET} ({len(probe_list)} probes × {len(samples)} samples)", flush=True)
    raw = xena_fetch(probe_list, samples)
    expr = raw.rename(columns={probes[g]: g for g in SCORE_GENES})
    expr = expr.loc[:, SCORE_GENES]
    expr.to_parquet(CACHE)
    meta = {
        "host": XENA_HOST,
        "dataset": XENA_DATASET,
        "unit": "log2(TPM + 0.001) as shipped (TOIL RSEM)",
        "probes": probes,
        "n_samples_requested": len(samples),
        "n_samples_returned": int(len(expr)),
        "n_all_nan_rows": int(expr.isna().all(axis=1).sum()),
    }
    META.write_text(json.dumps(meta, indent=2))
    return expr, meta


def zscore_mean(mat: pd.DataFrame, genes: list[str], min_n: int) -> pd.Series:
    z = mat[genes].apply(lambda s: (s - s.mean()) / s.std(ddof=0), axis=0)
    z = z.replace([np.inf, -np.inf], np.nan)
    n_present = z.notna().sum(axis=1)
    score = z.mean(axis=1, skipna=True)
    score = score.where(n_present >= min_n)
    return score


def residualize(y: np.ndarray, b: np.ndarray, tls: np.ndarray) -> tuple[np.ndarray, float]:
    x = np.column_stack([np.ones(len(y)), b, tls])
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    resid = y - x @ beta
    sd_y = float(np.std(y, ddof=0))
    sd_r = float(np.std(resid, ddof=0))
    ratio = float("nan") if sd_y == 0 else sd_r / sd_y
    return resid, ratio


def cohort_test(scores: pd.DataFrame) -> dict:
    work = scores.dropna(subset=["ecs", "b_cell", "tls"]).copy()
    n = int(len(work))
    if n < 3:
        return {
            "n": n,
            "r_B": float("nan"),
            "r_TLS": float("nan"),
            "spearman_B": float("nan"),
            "spearman_TLS": float("nan"),
            "pearson_fail": True,
            "max_abs_r": float("nan"),
            "residual_sd_ratio": None,
            "escape": False,
            "escape_reason": "n < 3 complete cases",
            "pass": False,
        }
    y = work["ecs"].to_numpy(dtype=np.float64)
    b = work["b_cell"].to_numpy(dtype=np.float64)
    t = work["tls"].to_numpy(dtype=np.float64)
    r_b = _pearson(y, b)
    r_t = _pearson(y, t)
    s_b = _spearman(y, b)
    s_t = _spearman(y, t)
    abs_b, abs_t = abs(r_b), abs(r_t)
    pearson_fail = bool(abs_b >= R_PASS or abs_t >= R_PASS)
    ceiling_fail = bool(abs_b >= R_CEILING or abs_t >= R_CEILING)
    ratio = None
    escape = False
    reason = ""
    if not pearson_fail:
        passed = True
        reason = f"both |r| < {R_PASS}"
    elif ceiling_fail:
        passed = False
        reason = f"no residual escape (|r| ≥ {R_CEILING})"
    else:
        _, ratio = residualize(y, b, t)
        escape = bool(pd.notna(ratio) and ratio >= SD_RATIO_MIN)
        passed = escape
        reason = (
            f"residual SD/raw SD = {ratio:.4f} "
            f"{'≥' if escape else '<'} {SD_RATIO_MIN} (raw |r| in [{R_PASS}, {R_CEILING}))"
        )
    return {
        "n": n,
        "r_B": r_b,
        "r_TLS": r_t,
        "spearman_B": s_b,
        "spearman_TLS": s_t,
        "pearson_fail": pearson_fail,
        "max_abs_r": max(abs_b, abs_t),
        "residual_sd_ratio": ratio,
        "escape": escape,
        "escape_reason": reason,
        "pass": passed,
    }


def score_window(expr: pd.DataFrame, pheno: pd.DataFrame) -> pd.DataFrame:
    samples = pheno["sample"].tolist()
    mat = expr.reindex(samples)
    out = pheno.set_index("sample").copy()
    out["ecs"] = zscore_mean(mat, ECS, MIN_ECS)
    out["b_cell"] = zscore_mean(mat, B_CELL, MIN_B)
    out["tls"] = zscore_mean(mat, TLS, MIN_TLS)
    return out


def _fmt_r(v) -> str:
    return "—" if v is None or pd.isna(v) else f"{v:.4f}"


def _fmt_bool(v) -> str:
    if v is None:
        return "—"
    return "True" if v else "False"


def write_markdown(
    frozen: dict,
    expr_meta: dict,
    probes: dict[str, str],
    pheno: pd.DataFrame,
    n_requested: int,
    n_expr: int,
    confirmatory: dict[str, dict],
    per_project: dict[str, dict],
    candidates: list[str],
) -> str:
    types_n = pheno.groupby("cancer_type").size().to_dict()
    proj_n = pheno.groupby("project").size().to_dict()
    sample_types = (
        pheno.groupby(["project", "sample_type"]).size().unstack(fill_value=0).to_string()
    )
    pooled = confirmatory["pooled"]
    blca = confirmatory["BLCA"]
    any_qualify = bool(pooled["pass"] and blca["pass"])
    lines = [
        "# Unit 04 — TCGA confound (Gate A)",
        "",
        f"**Run date:** {date.today().isoformat()}  ",
        f"**Protocol SHA:** `{PROTOCOL_SHA}`  ",
        f"**Frozen markers:** `{FROZEN.relative_to(ROOT)}`  ",
        "**Rule:** For each non-B candidate, score the **raw** nine-gene mean of within-cohort "
        "z-scores. Pearson |r| vs B-cell and vs TLS must both be **< 0.6** in concatenated "
        "pooled TCGA **and** in TCGA-BLCA. If a Pearson test fails on a cohort, residualize "
        "`raw ~ B + TLS` on that same cohort. Rescue iff residual SD / raw SD ≥ 0.5 **and** "
        "|r_B| < 0.75 **and** |r_TLS| < 0.75. Spearman is descriptive. Gate B always uses the "
        "raw score. Do not name the primary state.",
        "",
        "## Bulk scoring note",
        "",
        "The sealed marker list is the nine core ECS genes (no DE). In bulk TCGA, every non-B "
        f"candidate ({', '.join(candidates)}) is therefore scored with the **same** nine-gene "
        "mean. Pearson values are identical across candidates; they still qualify or fail as "
        "separate lineage buckets for Unit 05.",
        "",
        "## Matrix",
        "",
        f"- **Host:** `{expr_meta['host']}`  ",
        f"- **Dataset:** `{expr_meta['dataset']}` — {expr_meta['unit']}  ",
        f"- **Phenotype:** `{PHENO.relative_to(ROOT)}` (`_primary_disease` labels from Unit 00; "
        "cancer-type only, no ICI outcomes)  ",
        f"- **Samples requested (disease-matched):** {n_requested}  ",
        f"- **Samples with expression (aligned):** {n_expr}  ",
        "",
        "Pooled window = concatenate LUAD, LUSC, SKCM, COAD, READ, BRCA, BLCA. "
        "NSCLC = LUAD+LUSC; CRC = COAD+READ. BLCA is its own z-score window. "
        "All `_primary_disease`-matched sample types are kept (including Solid Tissue Normal); "
        "counts below.",
        "",
        "### Sample type × project",
        "",
        "```",
        sample_types,
        "```",
        "",
        f"Kill-type n: {', '.join(f'{k}={v}' for k, v in sorted(types_n.items()))}. "
        f"Project n: {', '.join(f'{k}={v}' for k, v in proj_n.items())}.",
        "",
        "## Genes",
        "",
        "Available-case mean of gene-wise z-scores (ddof=0) within the analysis window. "
        f"Minimum genes: ECS {MIN_ECS}/9, B cell {MIN_B}/5, TLS {MIN_TLS}/4. Never zero-fill. "
        "Confirmatory correlations use complete cases with all three scores.",
        "",
        "| Symbol | Probe (gencode.v23) | Signature |",
        "|---|---|---|",
    ]
    for g in ECS:
        lines.append(f"| `{g}` | `{probes[g]}` | ECS |")
    for g in B_CELL:
        lines.append(f"| `{g}` | `{probes[g]}` | B cell |")
    for g in TLS:
        lines.append(f"| `{g}` | `{probes[g]}` | TLS |")

    lines += [
        "",
        "## Confirmatory Pearson (same nine-gene score for every non-B candidate)",
        "",
        "| Cohort | n | r_B | abs r_B | r_TLS | abs r_TLS | Spearman_B | Spearman_TLS | max abs r | Pearson fail | Residual SD/raw SD | Cohort pass |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|",
    ]
    for name, row in (("pooled TCGA", pooled), ("TCGA-BLCA", blca)):
        lines.append(
            f"| {name} | {row['n']} | {_fmt_r(row['r_B'])} | {_fmt_r(abs(row['r_B']) if pd.notna(row['r_B']) else np.nan)} | "
            f"{_fmt_r(row['r_TLS'])} | {_fmt_r(abs(row['r_TLS']) if pd.notna(row['r_TLS']) else np.nan)} | "
            f"{_fmt_r(row['spearman_B'])} | {_fmt_r(row['spearman_TLS'])} | {_fmt_r(row['max_abs_r'])} | "
            f"{_fmt_bool(row['pearson_fail'])} | {_fmt_r(row['residual_sd_ratio'])} | {_fmt_bool(row['pass'])} |"
        )

    lines += [
        "",
        f"- Pooled: {pooled['escape_reason']}",
        f"- BLCA: {blca['escape_reason']}",
        "",
        "## Per candidate (four Pearson values each)",
        "",
        "| Candidate | r_B_pooled | r_TLS_pooled | r_B_BLCA | r_TLS_BLCA | Residual ratio pooled | Residual ratio BLCA | Qualifies |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for cand in candidates:
        lines.append(
            f"| {cand} | {_fmt_r(pooled['r_B'])} | {_fmt_r(pooled['r_TLS'])} | "
            f"{_fmt_r(blca['r_B'])} | {_fmt_r(blca['r_TLS'])} | "
            f"{_fmt_r(pooled['residual_sd_ratio'])} | {_fmt_r(blca['residual_sd_ratio'])} | "
            f"{_fmt_bool(any_qualify)} |"
        )

    lines += [
        "",
        "## Per-project Pearson (descriptive; not the pass metric)",
        "",
        "Each project is its own z-score window.",
        "",
        "| Project | Kill type | n | r_B | r_TLS | Spearman_B | Spearman_TLS |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for proj in ["LUAD", "LUSC", "SKCM", "COAD", "READ", "BRCA", "BLCA"]:
        row = per_project[proj]
        lines.append(
            f"| {proj} | {PROJECT_TO_TYPE[proj]} | {row['n']} | {_fmt_r(row['r_B'])} | "
            f"{_fmt_r(row['r_TLS'])} | {_fmt_r(row['spearman_B'])} | {_fmt_r(row['spearman_TLS'])} |"
        )

    lines += [
        "",
        "## Qualification (operator; human marks Gate A in Unit 05)",
        "",
        f"- Non-B candidates from Unit 03: **{', '.join(candidates)}**",
        f"- Pooled confound pass: **{pooled['pass']}**",
        f"- BLCA confound pass: **{blca['pass']}**",
        f"- At least one non-B candidate qualifies (both cohorts): **{any_qualify}**",
        f"- Two-lineage rule (from Unit 02/03, including B/plasma): **True** "
        f"({', '.join(frozen['marker_list']['lineages'])})",
        "",
        "A candidate qualifies only if every failed Pearson test is rescued on that same cohort. "
        "Unit 05 applies the naming cascade and the human marks Gate A. This unit does not pick "
        "the primary state.",
        "",
        "## What was not done",
        "",
        "- No ICI phenotype or outcome files opened.",
        "- No DE / extra ECS genes.",
        "- Primary non-B state not named (Unit 05).",
        "- Gate B not run.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    frozen = load_frozen()
    candidates = [b for b in frozen["marker_list"]["lineages"] if b != "B/plasma"]
    probes = probe_ids(frozen)
    pheno = load_phenotype()
    n_requested = int(len(pheno))
    expr, expr_meta = load_expression(probes, pheno["sample"].tolist())
    keep = pheno["sample"].isin(expr.index) & ~expr.reindex(pheno["sample"]).isna().all(axis=1).to_numpy()
    pheno = pheno.loc[keep].copy()
    n_expr = int(len(pheno))
    print(f"Aligned samples: {n_expr}", flush=True)
    if int((pheno["project"] == "BLCA").sum()) == 0:
        raise SystemExit("TCGA-BLCA RNA missing after alignment; amend before Gate B")

    pooled_scores = score_window(expr, pheno)
    blca_ph = pheno.loc[pheno["project"] == "BLCA"].copy()
    blca_scores = score_window(expr, blca_ph)
    confirmatory = {
        "pooled": cohort_test(pooled_scores),
        "BLCA": cohort_test(blca_scores),
    }
    per_project = {}
    for proj in TCGA_DISEASE:
        sub = pheno.loc[pheno["project"] == proj].copy()
        per_project[proj] = cohort_test(score_window(expr, sub))

    RESEARCH.write_text(
        write_markdown(frozen, expr_meta, probes, pheno, n_requested, n_expr, confirmatory, per_project, candidates)
    )
    payload = {
        "run_date": date.today().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "protocol_sha": PROTOCOL_SHA,
        "candidates": candidates,
        "same_bulk_score_for_all_non_b": True,
        "confirmatory": confirmatory,
        "per_project": per_project,
        "n_aligned": n_expr,
        "at_least_one_non_b_qualifies": bool(confirmatory["pooled"]["pass"] and confirmatory["BLCA"]["pass"]),
        "ici_files_opened": False,
        "primary_state_named": False,
    }
    JSON_OUT.write_text(json.dumps(payload, indent=2, default=str))
    print(f"Wrote {RESEARCH}", flush=True)
    print(json.dumps({k: {kk: vv for kk, vv in row.items() if kk != "escape_reason"} | {"reason": row["escape_reason"]} for k, row in confirmatory.items()}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
