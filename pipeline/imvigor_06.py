#!/usr/bin/env python3
"""Unit 06 — IMvigor210 confirmatory (Gate B).

Opens phenotype/outcome values only after Unit 05 is in git.
No new ECS genes. No cutoff search. Gate B is Model 1 + VIF only.
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import rdata
import statsmodels.api as sm
import statsmodels.formula.api as smf
from rdata.parser._parser import RObjectType
from statsmodels.duration.hazard_regression import PHReg
from statsmodels.stats.outliers_influence import variance_inflation_factor

sys.path.insert(0, str(Path(__file__).resolve().parent))
from genes import B_CELL, CD8, ECS, TLS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CDS = ROOT / "data" / "raw" / "imvigor210" / "cds" / "cds.RData"
PRIMARY = ROOT / "research" / "05-primary-state.md"
FROZEN = ROOT / "research" / "03-frozen-markers.json"
RESEARCH = ROOT / "research" / "06-imvigor210.md"
OUT_DIR = ROOT / "pipeline" / "output" / "06"
JSON_OUT = OUT_DIR / "06-imvigor210.json"

PROTOCOL_SHA = "3fbf310870c57247163edca35ed536ade3ea4301"
PRIMARY_NAME = "Stromal/other"
MIN_ECS, MIN_B, MIN_TLS, MIN_CD8 = 7, 3, 3, 3
SCORE_GENES = [*ECS, *B_CELL, *TLS, *CD8]


def _cdr(node):
    if isinstance(node.value, tuple) and len(node.value) > 1:
        return node.value[1]
    return None


def _car(node):
    return node.value[0] if isinstance(node.value, tuple) else node.value


def walk_pairlist(node) -> list:
    items = []
    while node is not None and hasattr(node, "info") and node.info.type == RObjectType.LIST:
        items.append(_car(node))
        node = _cdr(node)
        if node is not None and getattr(node, "info", None) and node.info.type == RObjectType.NILVALUE:
            break
    return items


def r_str(obj):
    if obj is None or not hasattr(obj, "info"):
        return None
    t = obj.info.type
    if t == RObjectType.CHAR:
        v = obj.value
        if v is None:
            return None
        return v.decode("utf-8") if isinstance(v, bytes) else str(v)
    if t == RObjectType.STR:
        return [r_str(x) for x in obj.value]
    if t == RObjectType.SYM:
        return r_str(obj.value)
    return None


def factor_levels(col) -> list[str] | None:
    node = col.attributes
    while node is not None and hasattr(node, "info") and node.info.type == RObjectType.LIST:
        car = _car(node)
        if car.info.type == RObjectType.STR:
            vals = r_str(car)
            if isinstance(vals, list) and vals and vals[0] != "factor":
                return vals
        node = _cdr(node)
    return None


def df_names(df_vec) -> list[str]:
    node = df_vec.attributes
    while node is not None and hasattr(node, "info") and node.info.type == RObjectType.LIST:
        car = _car(node)
        if car.info.type == RObjectType.STR:
            vals = r_str(car)
            if isinstance(vals, list) and vals and vals[0] not in {"data.frame"}:
                return vals
        node = _cdr(node)
    raise SystemExit("data.frame names attribute missing")


def decode_column(col) -> np.ndarray | list:
    t = col.info.type
    if t == RObjectType.STR:
        return r_str(col)
    if t in {RObjectType.INT, RObjectType.REAL, RObjectType.LGL}:
        arr = np.asarray(col.value)
        levels = factor_levels(col)
        if levels is not None:
            out = []
            mask = np.ma.getmaskarray(col.value) if np.ma.isMaskedArray(col.value) else np.zeros(len(arr), dtype=bool)
            for i, v in enumerate(arr):
                if mask[i] or pd.isna(v):
                    out.append(None)
                else:
                    idx = int(v) - 1
                    out.append(levels[idx] if 0 <= idx < len(levels) else None)
            return out
        if np.ma.isMaskedArray(col.value):
            data = col.value.astype(np.float64).filled(np.nan)
            return np.asarray(data, dtype=np.float64)
        return np.asarray(arr, dtype=np.float64)
    raise SystemExit(f"Unsupported column type {t}")


def load_cds() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    parsed = rdata.parser.parse_file(CDS)
    s4 = parsed.object.value[0]
    slots = walk_pairlist(s4.attributes)
    class_name = r_str(slots[10])
    if class_name not in (["CountDataSet"], "CountDataSet"):
        raise SystemExit(f"cds class is {class_name!r}, expected CountDataSet")

    ht = slots[4].value.hash_table
    exprs_list = [x for x in ht.value if hasattr(x, "info") and x.info.type == RObjectType.LIST]
    if len(exprs_list) != 1:
        raise SystemExit(f"assayData expected 1 binding, got {len(exprs_list)}")
    exprs_obj = _car(exprs_list[0])
    dims = None
    dimnames = None
    for attr in walk_pairlist(exprs_obj.attributes):
        if attr.info.type == RObjectType.INT and dims is None:
            dims = [int(x) for x in attr.value]
        elif attr.info.type == RObjectType.VEC:
            dimnames = [r_str(x) for x in attr.value]
    if dims != [31286, 348] and (dims is None or len(dims) != 2):
        raise SystemExit(f"Unexpected exprs dims: {dims}")
    n_genes, n_samples = dims
    counts = np.asarray(exprs_obj.value, dtype=np.float64).reshape((n_genes, n_samples), order="F")
    gene_ids = dimnames[0]
    sample_ids = dimnames[1]

    fd_slots = walk_pairlist(slots[6].attributes)
    fd_df = fd_slots[2]
    fd_names = df_names(fd_df)
    fdata = {name: decode_column(col) for name, col in zip(fd_names, fd_df.value, strict=True)}
    symbols = [None if s is None else str(s) for s in fdata["symbol"]]

    ph_slots = walk_pairlist(slots[5].attributes)
    ph_df = ph_slots[2]
    ph_names = df_names(ph_df)
    pdata = pd.DataFrame({name: decode_column(col) for name, col in zip(ph_names, ph_df.value, strict=True)})
    pdata.index = sample_ids
    pdata.index.name = "sample"

    meta = {
        "n_genes": n_genes,
        "n_samples": n_samples,
        "gene_ids_are_entrez": gene_ids[:3] == ["1", "10", "100"],
        "pdata_columns": ph_names,
        "fdata_columns": fd_names,
    }
    feat = pd.DataFrame({"entrez": gene_ids, "symbol": symbols})
    expr = pd.DataFrame(counts.T, index=sample_ids, columns=pd.RangeIndex(n_genes))
    return expr, feat, pdata, meta


def pick_gene_columns(feat: pd.DataFrame) -> dict[str, int]:
    frozen = json.loads(FROZEN.read_text())
    entrez_by_symbol = {
        g: str(frozen["hgnc_aliases"][g]["entrez"])
        for g in ECS
        if g in frozen.get("hgnc_aliases", {})
    }
    chosen: dict[str, int] = {}
    notes: dict[str, str] = {}
    for gene in SCORE_GENES:
        hits = feat.index[feat["symbol"].astype(str).str.upper() == gene].tolist()
        if not hits:
            notes[gene] = "MISSING"
            continue
        if len(hits) == 1:
            chosen[gene] = int(hits[0])
            notes[gene] = "unique_symbol"
            continue
        want = entrez_by_symbol.get(gene)
        if want:
            ent = feat.loc[hits, "entrez"].astype(str)
            match = [i for i in hits if ent.loc[i] == want]
            if match:
                chosen[gene] = int(match[0])
                notes[gene] = f"entrez_{want}_from_{len(hits)}_symbols"
                continue
        chosen[gene] = int(hits[0])
        notes[gene] = f"first_of_{len(hits)}_symbols"
    missing = [g for g in SCORE_GENES if g not in chosen]
    if missing:
        raise SystemExit(f"IMvigor210 missing score genes: {missing}")
    ecs_miss = [g for g in ECS if g not in chosen]
    if len(ecs_miss) > 2:
        raise SystemExit(f"More than two core ECS genes missing: {ecs_miss}")
    return chosen, notes


def zscore_mean(mat: pd.DataFrame, genes: list[str], min_n: int) -> pd.Series:
    z = mat[genes].apply(lambda s: (s - s.mean()) / s.std(ddof=0), axis=0)
    z = z.replace([np.inf, -np.inf], np.nan)
    n_present = z.notna().sum(axis=1)
    score = z.mean(axis=1, skipna=True)
    return score.where(n_present >= min_n), n_present


def logit_or(model) -> dict:
    params = model.params
    ci = model.conf_int()
    out = {}
    for name in params.index:
        if name == "Intercept":
            continue
        coef = float(params[name])
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


def fmt_or(row: dict | None) -> str:
    if not row:
        return "—"
    return f"{row['or']:.3f} ({row['or_lo']:.3f}–{row['or_hi']:.3f})"


def fmt_hr(row: dict | None) -> str:
    if not row:
        return "—"
    return f"{row['hr']:.3f} ({row['hr_lo']:.3f}–{row['hr_hi']:.3f})"


def cox_hr(res) -> dict:
    params = res.params
    ci = res.conf_int()
    out = {}
    names = list(params.index) if hasattr(params, "index") else [f"x{i}" for i in range(len(params))]
    pvals = res.pvalues
    for i, name in enumerate(names):
        coef = float(params.iloc[i] if hasattr(params, "iloc") else params[i])
        if hasattr(ci, "iloc"):
            lo, hi = float(ci.iloc[i, 0]), float(ci.iloc[i, 1])
        else:
            lo, hi = float(ci[i, 0]), float(ci[i, 1])
        p = float(pvals.iloc[i] if hasattr(pvals, "iloc") else pvals[i])
        out[str(name)] = {
            "coef": coef,
            "hr": float(np.exp(coef)),
            "hr_lo": float(np.exp(lo)),
            "hr_hi": float(np.exp(hi)),
            "p": p,
        }
    return out


def write_markdown(payload: dict) -> str:
    m1 = payload["model1"]
    un = payload["unadjusted"]
    m2 = payload["model2"]
    cox = payload["cox"]
    vif = payload["vif"]
    n = payload["n"]
    ecs = m1["terms"].get("ecs")
    gate_b = bool(ecs and ecs["ci_excludes_1"] and vif["ecs"] < 3.0)
    lines = [
        "# Unit 06 — IMvigor210 confirmatory (Gate B)",
        "",
        f"**Run date:** {date.today().isoformat()}  ",
        f"**Protocol SHA:** `{PROTOCOL_SHA}`  ",
        f"**Primary state:** {PRIMARY_NAME} (Unit 05, git freeze before this run)  ",
        f"**Pin:** `data/raw/imvigor210/cds/cds.RData` from `IMvigor210CoreBiologies_1.0.1.tar.gz`  ",
        "**Rule:** Continuous **raw** nine-gene ECS score. Model 1 = "
        "`response ~ ECS + B_cell + TLS + CD8` (logistic). Gate B pass = Model 1 ECS 95% CI "
        "excludes 1 **and** VIF(ECS) < 3. Unadjusted, Model 2, OS, and secondary states cannot "
        "pass or rescue. No cutoff search.",
        "",
        "## Matrix",
        "",
        f"- Object: CountDataSet `cds` (raw integer counts, {n['genes']} genes × {n['rna']} samples)",
        "- Transform: DESeq `sizeFactor`-normalized counts, then `log2(norm + 1)`, then "
        "within-cohort gene-wise z-score (ddof=0), available-case mean per `PROTOCOL.md`",
        f"- Size factors present: **{payload['size_factor_ok']}**",
        f"- Genes missing from matrix: **none** (ECS 9/9, B 5/5, TLS 4/4, CD8 5/5)",
        "",
        "## Endpoint",
        "",
        "- `binaryResponse` as shipped: CR/PR vs SD/PD. Drop NE/NA.",
        f"- RNA samples: **{n['rna']}**",
        f"- Dropped (ECS/B/TLS/CD8 below gene minima): **{n['dropped_min_genes']}**",
        f"- Dropped (binaryResponse NE/NA or not CR/PR|SD/PD): **{n['dropped_endpoint']}**",
        f"- Model 1 complete cases: **{n['model1']}** "
        f"(CR/PR={n['responders']}, SD/PD={n['nonresponders']})",
        "",
        "## Scores (Model 1 table)",
        "",
        "| Score | Genes used | Min genes | n missing on RNA |",
        "|---|---|---:|---:|",
        f"| ECS (primary {PRIMARY_NAME}) | nine core | {MIN_ECS}/9 | {n['missing_ecs']} |",
        f"| B cell | five locked | {MIN_B}/5 | {n['missing_b']} |",
        f"| TLS | four locked | {MIN_TLS}/4 | {n['missing_tls']} |",
        f"| CD8 | five locked | {MIN_CD8}/5 | {n['missing_cd8']} |",
        "",
        "## Model 1 (kill)",
        "",
        "`response ~ ecs + b_cell + tls + cd8` (logistic). 1 = CR/PR.",
        "",
        f"- n = **{n['model1']}**",
        f"- Converged: **{m1['converged']}**",
        "",
        "| Term | OR | 95% CI | p | CI excludes 1 |",
        "|---|---:|---|---:|---|",
    ]
    for term in ["ecs", "b_cell", "tls", "cd8"]:
        row = m1["terms"][term]
        lines.append(
            f"| {term} | {row['or']:.3f} | {row['or_lo']:.3f}–{row['or_hi']:.3f} | "
            f"{row['p']:.4g} | {row['ci_excludes_1']} |"
        )
    lines += [
        "",
        "## VIF (Model 1 complete-case predictors)",
        "",
        "VIF from OLS auxiliary regressions on the four scores plus intercept. Report the four "
        "scores. Model 1 is always fit as specified (no term dropping).",
        "",
        "| Term | VIF |",
        "|---|---:|",
        f"| ecs | {vif['ecs']:.3f} |",
        f"| b_cell | {vif['b_cell']:.3f} |",
        f"| tls | {vif['tls']:.3f} |",
        f"| cd8 | {vif['cd8']:.3f} |",
        f"| Intercept (not a Gate B term) | {vif['const']:.3f} |",
        "",
        f"- VIF(ECS) < 3: **{vif['ecs'] < 3.0}**",
        "",
        "## Gate B draft (human marks)",
        "",
        f"- Model 1 ECS CI excludes 1: **{ecs['ci_excludes_1']}** (OR {fmt_or(ecs)})",
        f"- VIF(ECS) < 3: **{vif['ecs'] < 3.0}** ({vif['ecs']:.3f})",
        f"- Operator Gate B numbers hold: **{gate_b}**",
        "",
        "OS, Model 2, unadjusted, secondary states, deconvolution, and melanoma GEO cannot rescue.",
        "",
        "## Unadjusted (neither necessary nor sufficient)",
        "",
        f"`response ~ ecs`. n = **{un['n']}**. OR {fmt_or(un['terms'].get('ecs'))}. "
        f"p = {un['terms']['ecs']['p']:.4g}.",
        "",
        "## Model 2 (robustness, not a pass)",
        "",
        "Model 1 + TMB (`FMOne mutation burden per MB`) + PD-L1 IC (`IC Level` as shipped factor). "
        "Complete cases. Sex added only if it is complete for that same n (no extra drops). "
        "No patient age column in the extract.",
        "",
        f"- n = **{m2['n']}**",
        f"- Sex included: **{m2['sex_included']}** (complete on Model 2 table: {m2['sex_complete']})",
        f"- Converged: **{m2['converged']}**",
        "",
        "| Term | OR | 95% CI | p |",
        "|---|---:|---|---:|",
    ]
    for term, row in m2["terms"].items():
        lines.append(
            f"| {term} | {row['or']:.3f} | {row['or_lo']:.3f}–{row['or_hi']:.3f} | {row['p']:.4g} |"
        )
    lines += [
        "",
        "## Cox OS (secondary, not a pass)",
        "",
        f"Time = `os` (months). Event = `censOS` (1 = dead) as shipped. Same four scores as Model 1. "
        f"n = **{cox['n']}** (events = {cox['events']}).",
        "",
        "| Term | HR | 95% CI | p |",
        "|---|---:|---|---:|",
    ]
    for term in ["ecs", "b_cell", "tls", "cd8"]:
        row = cox["terms"][term]
        lines.append(
            f"| {term} | {row['hr']:.3f} | {row['hr_lo']:.3f}–{row['hr_hi']:.3f} | {row['p']:.4g} |"
        )
    lines += [
        "",
        "## Human Gate B",
        "",
        "- [ ] Pass (Model 1 ECS CI excludes 1 **and** VIF(ECS) < 3)",
        "- [ ] Fail",
        "",
        "## What was not done",
        "",
        "- No new ECS genes. No median/Youden/ROC/AUC cutoff search.",
        "- No deconvolution. No melanoma GEO (Unit 07). Secondary non-B state not used to pass Gate B.",
        "- Frozen Unit 03/05 objects not edited.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    if not PRIMARY.exists():
        raise SystemExit("Unit 05 artifact missing")
    if "Stromal/other" not in PRIMARY.read_text() or "[X] Pass" not in PRIMARY.read_text():
        raise SystemExit("Unit 05 primary / Gate A pass not recorded")

    print("Loading cds.RData …", flush=True)
    expr_raw, feat, pdata, cds_meta = load_cds()
    gene_cols, gene_notes = pick_gene_columns(feat)
    mat = pd.DataFrame({g: expr_raw.iloc[:, gene_cols[g]].to_numpy() for g in SCORE_GENES}, index=expr_raw.index)

    sf = pd.to_numeric(pdata["sizeFactor"], errors="coerce")
    if int(sf.notna().sum()) != len(pdata):
        raise SystemExit("sizeFactor missing; amend before Gate B scoring")
    # samples × genes; sizeFactor is per sample
    norm = mat.div(sf, axis=0)
    logmat = np.log2(norm + 1.0)

    ecs, n_ecs = zscore_mean(logmat, ECS, MIN_ECS)
    b, n_b = zscore_mean(logmat, B_CELL, MIN_B)
    tls, n_tls = zscore_mean(logmat, TLS, MIN_TLS)
    cd8, n_cd8 = zscore_mean(logmat, CD8, MIN_CD8)

    scores = pd.DataFrame({"ecs": ecs, "b_cell": b, "tls": tls, "cd8": cd8}, index=mat.index)
    min_ok = scores.notna().all(axis=1)
    n_rna = int(len(scores))
    n_drop_min = int((~min_ok).sum())

    y_raw = pdata["binaryResponse"].astype("object")
    y = y_raw.map({"CR/PR": 1, "SD/PD": 0})
    endpoint_ok = y.isin([0, 1])
    n_drop_end = int((min_ok & ~endpoint_ok).sum())

    model1_tbl = pd.DataFrame(
        {
            "y": y,
            "ecs": scores["ecs"],
            "b_cell": scores["b_cell"],
            "tls": scores["tls"],
            "cd8": scores["cd8"],
        }
    ).loc[min_ok & endpoint_ok]
    model1_tbl = model1_tbl.dropna()
    n_m1 = int(len(model1_tbl))
    n_resp = int((model1_tbl["y"] == 1).sum())
    n_non = int((model1_tbl["y"] == 0).sum())

    m1 = smf.logit("y ~ ecs + b_cell + tls + cd8", data=model1_tbl).fit(disp=0)
    m1_terms = logit_or(m1)
    # formula uses those names
    m1_terms = {
        "ecs": m1_terms["ecs"],
        "b_cell": m1_terms["b_cell"],
        "tls": m1_terms["tls"],
        "cd8": m1_terms["cd8"],
    }

    x_vif = sm.add_constant(model1_tbl[["ecs", "b_cell", "tls", "cd8"]], has_constant="add")
    vif = {
        name: float(variance_inflation_factor(x_vif.to_numpy(), i))
        for i, name in enumerate(x_vif.columns)
    }

    un_tbl = model1_tbl[["y", "ecs"]].dropna()
    un = smf.logit("y ~ ecs", data=un_tbl).fit(disp=0)

    m2_base = model1_tbl.copy()
    m2_base["tmb"] = pd.to_numeric(pdata.loc[m2_base.index, "FMOne mutation burden per MB"], errors="coerce")
    m2_base["ic"] = pdata.loc[m2_base.index, "IC Level"].astype("object")
    m2_base["sex"] = pdata.loc[m2_base.index, "Sex"].astype("object")
    m2_tbl = m2_base.dropna(subset=["y", "ecs", "b_cell", "tls", "cd8", "tmb", "ic"])
    sex_complete = bool(m2_tbl["sex"].notna().all() and set(m2_tbl["sex"].unique()) <= {"F", "M"})
    sex_included = sex_complete
    formula2 = "y ~ ecs + b_cell + tls + cd8 + tmb + C(ic)"
    if sex_included:
        formula2 += " + C(sex)"
    m2 = smf.logit(formula2, data=m2_tbl).fit(disp=0)

    cox_tbl = pd.DataFrame(
        {
            "os": pd.to_numeric(pdata["os"], errors="coerce"),
            "event": pd.to_numeric(pdata["censOS"], errors="coerce"),
            "ecs": scores["ecs"],
            "b_cell": scores["b_cell"],
            "tls": scores["tls"],
            "cd8": scores["cd8"],
        }
    ).loc[min_ok]
    cox_tbl = cox_tbl.dropna()
    cox_exog = cox_tbl[["ecs", "b_cell", "tls", "cd8"]]
    cox_res = PHReg(cox_tbl["os"], cox_exog, status=cox_tbl["event"]).fit()
    cox_terms_raw = cox_hr(cox_res)
    # PHReg param names may be const, ecs, ...
    cox_terms = {}
    for k, v in cox_terms_raw.items():
        key = k.lower().replace("const", "intercept")
        cox_terms[key] = v
    # map to expected keys
    rename = {}
    for k in cox_terms:
        for want in ["ecs", "b_cell", "tls", "cd8"]:
            if want in k:
                rename[want] = cox_terms[k]
    if set(rename) != {"ecs", "b_cell", "tls", "cd8"}:
        # fall back to column order after intercept
        names = ["ecs", "b_cell", "tls", "cd8"]
        vals = [v for k, v in cox_terms_raw.items() if "const" not in k.lower() and k != "Intercept"]
        if len(vals) == 4:
            rename = dict(zip(names, vals, strict=True))
        else:
            raise SystemExit(f"Could not map Cox terms: {list(cox_terms_raw)}")

    payload = {
        "unit": "06",
        "run_date": date.today().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "protocol_sha": PROTOCOL_SHA,
        "primary_state": PRIMARY_NAME,
        "size_factor_ok": True,
        "cds_meta": cds_meta,
        "gene_notes": gene_notes,
        "n": {
            "genes": cds_meta["n_genes"],
            "rna": n_rna,
            "dropped_min_genes": n_drop_min,
            "dropped_endpoint": n_drop_end,
            "model1": n_m1,
            "responders": n_resp,
            "nonresponders": n_non,
            "missing_ecs": int((n_ecs < MIN_ECS).sum()),
            "missing_b": int((n_b < MIN_B).sum()),
            "missing_tls": int((n_tls < MIN_TLS).sum()),
            "missing_cd8": int((n_cd8 < MIN_CD8).sum()),
        },
        "model1": {
            "n": n_m1,
            "converged": bool(m1.mle_retvals.get("converged", True)),
            "terms": m1_terms,
        },
        "vif": {
            "const": vif["const"],
            "ecs": vif["ecs"],
            "b_cell": vif["b_cell"],
            "tls": vif["tls"],
            "cd8": vif["cd8"],
        },
        "unadjusted": {
            "n": int(len(un_tbl)),
            "converged": bool(un.mle_retvals.get("converged", True)),
            "terms": logit_or(un),
        },
        "model2": {
            "n": int(len(m2_tbl)),
            "sex_complete": sex_complete,
            "sex_included": sex_included,
            "formula": formula2,
            "converged": bool(m2.mle_retvals.get("converged", True)),
            "terms": logit_or(m2),
        },
        "cox": {
            "n": int(len(cox_tbl)),
            "events": int((cox_tbl["event"] == 1).sum()),
            "terms": rename,
        },
        "gate_b_numbers_hold": bool(m1_terms["ecs"]["ci_excludes_1"] and vif["ecs"] < 3.0),
        "cutoff_search": False,
        "new_ecs_genes": False,
    }

    RESEARCH.write_text(write_markdown(payload))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    print(f"Wrote {RESEARCH}", flush=True)
    print(
        json.dumps(
            {
                "model1_n": n_m1,
                "ecs_or": m1_terms["ecs"],
                "vif_ecs": vif["ecs"],
                "gate_b_numbers_hold": payload["gate_b_numbers_hold"],
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
