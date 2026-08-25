#!/usr/bin/env python3
"""Unit 07 — melanoma GEO replication. Descriptive only. Cannot rescue Gate B."""

from __future__ import annotations

import gzip
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.duration.hazard_regression import PHReg

sys.path.insert(0, str(Path(__file__).resolve().parent))
from genes import B_CELL, CD8, ECS, TLS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
GEO = ROOT / "data" / "raw" / "geo"
RESEARCH = ROOT / "research" / "07-melanoma-geo.md"
OUT_DIR = ROOT / "pipeline" / "output" / "07"
JSON_OUT = OUT_DIR / "07-melanoma-geo.json"
GATE_B = ROOT / "research" / "06-imvigor210.md"

PROTOCOL_SHA = "3fbf310870c57247163edca35ed536ade3ea4301"
PRIMARY_NAME = "Stromal/other"
MIN_ECS, MIN_B, MIN_TLS, MIN_CD8 = 7, 3, 3, 3
SCORE_GENES = [*ECS, *B_CELL, *TLS, *CD8]

# Unit 00 inventory Entrez IDs (GSE91061).
ENTREZ = {
    "CNR1": "1268",
    "CNR2": "1269",
    "GPR55": "9290",
    "TRPV1": "7442",
    "FAAH": "2166",
    "MGLL": "11343",
    "DAGLA": "747",
    "DAGLB": "221955",
    "NAPEPLD": "222236",
    "MS4A1": "931",
    "CD19": "930",
    "CD79A": "973",
    "CD79B": "974",
    "MZB1": "51237",
    "CXCL13": "10563",
    "CCL19": "6363",
    "CCL21": "6366",
    "CCR7": "1236",
    "CD8A": "925",
    "CD8B": "926",
    "GZMB": "3002",
    "PRF1": "5551",
    "IFNG": "3458",
}


def parse_series(path: Path) -> pd.DataFrame:
    acc = titles = None
    char_rows: list[list[str]] = []
    with gzip.open(path, "rt") as fh:
        for line in fh:
            if line.startswith("!Sample_geo_accession"):
                acc = [x.strip().strip('"') for x in line.rstrip("\n").split("\t")[1:]]
            elif line.startswith("!Sample_title"):
                titles = [x.strip().strip('"') for x in line.rstrip("\n").split("\t")[1:]]
            elif line.startswith("!Sample_characteristics_ch1"):
                char_rows.append([x.strip().strip('"') for x in line.rstrip("\n").split("\t")[1:]])
            elif line.startswith("!series_matrix_table_begin"):
                break
    if not acc or not titles:
        raise SystemExit(f"Missing accession/title in {path}")
    recs = []
    for i, geo in enumerate(acc):
        chars: dict[str, str] = {}
        for row in char_rows:
            if i >= len(row):
                continue
            cell = row[i]
            if not cell or ":" not in cell:
                continue
            key, val = cell.split(":", 1)
            chars[key.strip().lower()] = val.strip()
        recs.append({"geo": geo, "title": titles[i], **chars})
    return pd.DataFrame(recs).set_index("title")


def zscore_mean(mat: pd.DataFrame, genes: list[str], min_n: int) -> tuple[pd.Series, pd.Series]:
    use = [g for g in genes if g in mat.columns]
    z = mat[use].apply(lambda s: (s - s.mean()) / s.std(ddof=0), axis=0)
    z = z.replace([np.inf, -np.inf], np.nan)
    n_present = z.notna().sum(axis=1)
    score = z.mean(axis=1, skipna=True)
    return score.where(n_present >= min_n), n_present


def logit_or(model) -> dict:
    ci = model.conf_int()
    out = {}
    for name in model.params.index:
        if name == "Intercept":
            continue
        coef = float(model.params[name])
        lo, hi = float(ci.loc[name, 0]), float(ci.loc[name, 1])
        out[name] = {
            "coef": coef,
            "or": float(np.exp(coef)),
            "or_lo": float(np.exp(lo)),
            "or_hi": float(np.exp(hi)),
            "p": float(model.pvalues[name]),
            "ci_excludes_1": bool(lo > 0 or hi < 0),
        }
    return out


def fit_logit(formula: str, data: pd.DataFrame) -> dict:
    try:
        model = smf.logit(formula, data=data).fit(disp=0, maxiter=200)
        return {
            "ok": True,
            "n": int(model.nobs),
            "converged": bool(model.mle_retvals.get("converged", True)),
            "terms": logit_or(model),
            "error": None,
        }
    except Exception as exc:
        return {"ok": False, "n": int(len(data)), "converged": False, "terms": {}, "error": str(exc)}


def cox_terms(tbl: pd.DataFrame, cols: list[str]) -> dict:
    work = tbl[["os", "event", *cols]].dropna()
    if len(work) < 8 or int(work["event"].sum()) < 3:
        return {"ok": False, "n": int(len(work)), "events": int(work["event"].sum()) if len(work) else 0, "terms": {}, "error": "too few events"}
    try:
        res = PHReg(work["os"], work[cols], status=work["event"]).fit()
        params = res.params
        ci = res.conf_int()
        pvals = res.pvalues
        names = list(params.index) if hasattr(params, "index") else cols
        terms = {}
        for i, name in enumerate(names):
            coef = float(params.iloc[i] if hasattr(params, "iloc") else params[i])
            if hasattr(ci, "iloc"):
                lo, hi = float(ci.iloc[i, 0]), float(ci.iloc[i, 1])
            else:
                lo, hi = float(ci[i, 0]), float(ci[i, 1])
            p = float(pvals.iloc[i] if hasattr(pvals, "iloc") else pvals[i])
            key = str(name)
            terms[key] = {
                "coef": coef,
                "hr": float(np.exp(coef)),
                "hr_lo": float(np.exp(lo)),
                "hr_hi": float(np.exp(hi)),
                "p": p,
            }
        mapped = {}
        for want in cols:
            hit = next((terms[k] for k in terms if want == k or want in k), None)
            if hit:
                mapped[want] = hit
        if set(mapped) != set(cols):
            extras = [v for k, v in terms.items() if "const" not in k.lower()]
            if len(extras) == len(cols):
                mapped = dict(zip(cols, extras, strict=True))
        return {
            "ok": True,
            "n": int(len(work)),
            "events": int((work["event"] == 1).sum()),
            "terms": mapped,
            "error": None,
        }
    except Exception as exc:
        return {"ok": False, "n": int(len(work)), "events": int(work["event"].sum()), "terms": {}, "error": str(exc)}


def pick_symbol_matrix(df: pd.DataFrame, gene_col: str) -> pd.DataFrame:
    work = df.copy()
    work[gene_col] = work[gene_col].astype(str).str.upper()
    # Mean duplicate symbols.
    num = work.drop(columns=[gene_col]).apply(pd.to_numeric, errors="coerce")
    num[gene_col] = work[gene_col]
    collapsed = num.groupby(gene_col, sort=False).mean(numeric_only=True)
    missing = [g for g in SCORE_GENES if g not in collapsed.index]
    if missing:
        raise SystemExit(f"GSE78220 missing genes: {missing}")
    return collapsed.loc[SCORE_GENES].T


def pick_entrez_matrix(df: pd.DataFrame) -> pd.DataFrame:
    genes = df.iloc[:, 0].astype(str).str.replace(r"\.0$", "", regex=True)
    mat = df.drop(columns=df.columns[0]).apply(pd.to_numeric, errors="coerce")
    mat.index = genes.to_numpy()
    out = {}
    missing = []
    for g in SCORE_GENES:
        eid = ENTREZ[g]
        if eid not in mat.index:
            missing.append(f"{g}:{eid}")
            continue
        row = mat.loc[eid]
        if isinstance(row, pd.DataFrame):
            row = row.mean(axis=0)
        out[g] = row
    if missing:
        raise SystemExit(f"GSE91061 missing genes: {missing}")
    return pd.DataFrame(out)


def score_cohort(expr: pd.DataFrame) -> pd.DataFrame:
    logmat = np.log2(expr.clip(lower=0) + 1.0)
    ecs, n_ecs = zscore_mean(logmat, ECS, MIN_ECS)
    b, n_b = zscore_mean(logmat, B_CELL, MIN_B)
    tls, n_tls = zscore_mean(logmat, TLS, MIN_TLS)
    cd8, n_cd8 = zscore_mean(logmat, CD8, MIN_CD8)
    return pd.DataFrame(
        {
            "ecs": ecs,
            "b_cell": b,
            "tls": tls,
            "cd8": cd8,
            "n_ecs": n_ecs,
            "n_b": n_b,
            "n_tls": n_tls,
            "n_cd8": n_cd8,
        },
        index=expr.index,
    )


def analyze_gse78220() -> dict:
    expr_raw = pd.read_excel(GEO / "GSE78220_PatientFPKM.xlsx", engine="openpyxl")
    series = parse_series(GEO / "GSE78220_series_matrix.txt.gz")
    gene_mat = pick_symbol_matrix(expr_raw, "Gene")  # samples × genes
    # Map expression columns to series titles.
    col_map = {}
    for col in gene_mat.index:
        m = re.match(r"^(Pt\d+[AB]?)\.(baseline|OnTx)$", str(col), flags=re.I)
        if not m:
            continue
        col_map[col] = {"title": m.group(1), "on_tx": m.group(2).lower() == "ontx"}
    keep_cols = [c for c, meta in col_map.items() if not meta["on_tx"] and meta["title"] in series.index]
    dropped_on = [c for c, meta in col_map.items() if meta["on_tx"]]
    pre = gene_mat.loc[keep_cols].copy()
    pre["title"] = [col_map[c]["title"] for c in pre.index]
    pre["patient"] = series.loc[pre["title"], "patient id"].to_numpy()
    # Average multiple pre biopsies from the same patient (Pt27A/B).
    gene_cols = list(SCORE_GENES)
    patient_expr = pre.groupby("patient", sort=False)[gene_cols].mean()
    scores = score_cohort(patient_expr)
    ph = series.reset_index().drop_duplicates("patient id").set_index("patient id")
    scores = scores.join(ph[["anti-pd-1 response", "gender", "age (yrs)", "overall survival (days)", "vital status"]], how="left")
    resp = scores["anti-pd-1 response"].map(
        {
            "Complete Response": 1,
            "Partial Response": 1,
            "Progressive Disease": 0,
            "Stable Disease": 0,
        }
    )
    scores["y"] = resp
    tbl = scores.dropna(subset=["ecs", "b_cell", "tls", "cd8", "y"])
    m1 = fit_logit("y ~ ecs + b_cell + tls + cd8", tbl)
    un = fit_logit("y ~ ecs", tbl)
    scores["os"] = pd.to_numeric(scores["overall survival (days)"], errors="coerce")
    scores["event"] = scores["vital status"].map({"Dead": 1, "Alive": 0})
    cox = cox_terms(scores, ["ecs", "b_cell", "tls", "cd8"])
    return {
        "accession": "GSE78220",
        "citation": "Hugo et al. Cell 2016; pembrolizumab melanoma",
        "n_expr_columns": int(gene_mat.shape[0]),
        "dropped_on_treatment": dropped_on,
        "n_pre_samples": int(len(keep_cols)),
        "n_patients": int(len(patient_expr)),
        "n_model": int(len(tbl)),
        "n_crpr": int((tbl["y"] == 1).sum()),
        "n_sdpd": int((tbl["y"] == 0).sum()),
        "response_raw": scores["anti-pd-1 response"].value_counts(dropna=False).to_dict(),
        "model1": m1,
        "unadjusted": un,
        "cox": cox,
        "covariates_available": ["B cell", "TLS", "CD8", "sex", "age", "OS"],
        "tmb_pdl1": False,
    }


def analyze_gse91061() -> dict:
    expr_raw = pd.read_csv(GEO / "GSE91061_BMS038109Sample.hg19KnownGene.fpkm.csv.gz")
    series = parse_series(GEO / "GSE91061_series_matrix.txt.gz")
    gene_mat = pick_entrez_matrix(expr_raw)  # samples × genes; index = titles
    series = series.reindex(gene_mat.index)
    pre_mask = series["visit (pre or on treatment)"].astype(str).str.lower().eq("pre")
    pre_expr = gene_mat.loc[pre_mask]
    scores = score_cohort(pre_expr)
    ph = series.loc[pre_mask]
    scores["response_raw"] = ph["response"].to_numpy()
    scores["visit"] = ph["visit (pre or on treatment)"].to_numpy()
    resp = scores["response_raw"].map({"PRCR": 1, "CR": 1, "PR": 1, "PD": 0, "SD": 0})
    scores["y"] = resp
    tbl = scores.dropna(subset=["ecs", "b_cell", "tls", "cd8", "y"])
    m1 = fit_logit("y ~ ecs + b_cell + tls + cd8", tbl)
    un = fit_logit("y ~ ecs", tbl)
    return {
        "accession": "GSE91061",
        "citation": "Riaz et al. Cell 2017; nivolumab melanoma",
        "n_expr_columns": int(gene_mat.shape[0]),
        "n_pre_samples": int(pre_mask.sum()),
        "n_patients": int(pre_mask.sum()),
        "n_dropped_unk": int((scores["y"].isna()).sum()),
        "n_model": int(len(tbl)),
        "n_crpr": int((tbl["y"] == 1).sum()),
        "n_sdpd": int((tbl["y"] == 0).sum()),
        "response_raw": scores["response_raw"].value_counts(dropna=False).to_dict(),
        "model1": m1,
        "unadjusted": un,
        "cox": None,
        "covariates_available": ["B cell", "TLS", "CD8"],
        "tmb_pdl1": False,
    }


def fmt_or(block: dict, term: str = "ecs") -> str:
    if not block or not block.get("ok"):
        err = (block or {}).get("error") or "model failed"
        return f"— ({err})"
    row = block["terms"].get(term)
    if not row:
        return "—"
    return f"{row['or']:.3f} ({row['or_lo']:.3f}–{row['or_hi']:.3f})"


def fmt_hr(block: dict, term: str = "ecs") -> str:
    if not block or not block.get("ok"):
        return "—"
    row = block["terms"].get(term)
    if not row:
        return "—"
    return f"{row['hr']:.3f} ({row['hr_lo']:.3f}–{row['hr_hi']:.3f})"


def cohort_section(name: str, rec: dict) -> list[str]:
    m1 = rec["model1"]
    un = rec["unadjusted"]
    lines = [
        f"## {name}",
        "",
        f"- **Citation:** {rec['citation']}",
        f"- Transform: `log2(FPKM + 1)`, then within-cohort z-score (pre-treatment window), available-case mean",
        f"- Expression columns: {rec['n_expr_columns']}",
        f"- Pre-treatment samples: {rec['n_pre_samples']}; patients in model window: {rec['n_patients']}",
        f"- Model n (CR/PR vs SD/PD, complete scores): **{rec['n_model']}** (CR/PR={rec['n_crpr']}, SD/PD={rec['n_sdpd']})",
        f"- Model 1 covariates available: {', '.join(rec['covariates_available'])}",
        f"- TMB / PD-L1 IC: **{rec['tmb_pdl1']}**",
        "",
    ]
    if rec.get("dropped_on_treatment"):
        lines.append(f"- Dropped on-treatment columns: {', '.join(rec['dropped_on_treatment'])}")
        lines.append("")
    if rec.get("n_dropped_unk") is not None:
        lines.append(f"- Dropped UNK/NA response: {rec['n_dropped_unk']}")
        lines.append("")
    lines += [
        "### Model 1 (descriptive)",
        "",
        "`response ~ ecs + b_cell + tls + cd8`. Cannot pass or rescue Gate B.",
        "",
        f"- n = **{m1['n']}**. Converged: **{m1.get('converged')}**. Error: {m1.get('error') or 'none'}",
        "",
    ]
    if m1.get("ok") and m1["terms"]:
        lines += [
            "| Term | OR | 95% CI | p | CI excludes 1 |",
            "|---|---:|---|---:|---|",
        ]
        for term, row in m1["terms"].items():
            lines.append(
                f"| {term} | {row['or']:.3f} | {row['or_lo']:.3f}–{row['or_hi']:.3f} | "
                f"{row['p']:.4g} | {row['ci_excludes_1']} |"
            )
        lines.append("")
    lines += [
        "### Unadjusted (descriptive)",
        "",
        f"`response ~ ecs`. n = **{un['n']}**. OR {fmt_or(un)}. "
        f"Converged: **{un.get('converged')}**.",
        "",
    ]
    cox = rec.get("cox")
    if cox:
        lines += [
            "### Cox OS (descriptive)",
            "",
            f"Time = overall survival (days). Event = dead. n = **{cox['n']}**, events = {cox.get('events')}.",
            "",
        ]
        if cox.get("ok") and cox["terms"]:
            lines += [
                "| Term | HR | 95% CI | p |",
                "|---|---:|---|---:|",
            ]
            for term in ["ecs", "b_cell", "tls", "cd8"]:
                row = cox["terms"].get(term)
                if not row:
                    continue
                lines.append(
                    f"| {term} | {row['hr']:.3f} | {row['hr_lo']:.3f}–{row['hr_hi']:.3f} | {row['p']:.4g} |"
                )
            lines.append("")
        else:
            lines.append(f"Not fit: {cox.get('error')}")
            lines.append("")
    return lines


def write_markdown(g78: dict, g91: dict) -> str:
    lines = [
        "# Unit 07 — Melanoma GEO replication (descriptive)",
        "",
        f"**Run date:** {date.today().isoformat()}  ",
        f"**Protocol SHA:** `{PROTOCOL_SHA}`  ",
        f"**Primary state:** {PRIMARY_NAME} (same nine-gene raw score as Gate B)  ",
        "**Rule:** Pre-treatment anti-PD-1 melanoma. Same available-case scoring as Unit 06. "
        "Fit Model 1 covariates if available. **Cannot pass or rescue Gate B.** No cutoff search.",
        "",
        "## Gate B (already marked; this unit cannot change it)",
        "",
        "- Human Gate B: **fail** (IMvigor210 Model 1 ECS CI includes 1).",
        "- These GEO sets are underpowered replication. They are reported only.",
        "",
    ]
    lines += cohort_section("GSE78220", g78)
    lines += cohort_section("GSE91061", g91)
    lines += [
        "## What was not done",
        "",
        "- No cutoff / Youden / AUC search. No new ECS genes. Primary name not changed.",
        "- Results here do not flip Gate B.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = GATE_B.read_text()
    if "[X] Fail" not in text:
        raise SystemExit("Gate B fail is not marked; Unit 07 is report-only after that mark")
    print("GSE78220 …", flush=True)
    g78 = analyze_gse78220()
    print("GSE91061 …", flush=True)
    g91 = analyze_gse91061()
    RESEARCH.write_text(write_markdown(g78, g91))
    payload = {
        "unit": "07",
        "run_date": date.today().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "protocol_sha": PROTOCOL_SHA,
        "primary_state": PRIMARY_NAME,
        "cannot_rescue_gate_b": True,
        "GSE78220": g78,
        "GSE91061": g91,
        "cutoff_search": False,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    print(f"Wrote {RESEARCH}", flush=True)
    print(
        json.dumps(
            {
                "GSE78220": {"n": g78["n_model"], "m1_ecs": fmt_or(g78["model1"]), "un_ecs": fmt_or(g78["unadjusted"])},
                "GSE91061": {"n": g91["n_model"], "m1_ecs": fmt_or(g91["model1"]), "un_ecs": fmt_or(g91["unadjusted"])},
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
