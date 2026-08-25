#!/usr/bin/env python3
"""Unit 13 — Stromal/other composition (display-only) and confirmatory heatmaps.

No clustering, DE, UMAP, browser, or ICI files. Subtypes are not named states.
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm

sys.path.insert(0, str(Path(__file__).resolve().parent))
from detection_01 import (  # noqa: E402
    CENSUS_VERSION,
    DISEASES,
    _disease_type,
    census_obs_filter,
)
from genes import ECS  # noqa: E402
from inventory_11 import CULTURE  # noqa: E402
from lineage import assign_bucket  # noqa: E402
from reproduce_10 import ATLAS_SHA, PRIMARY  # noqa: E402
from states_02 import BUCKETS, PROTOCOL_SHA as KILL_SHA, ROOT  # noqa: E402

OUT_DIR = ROOT / "pipeline" / "output" / "13"
DIAGRAMS = ROOT / "docs" / "diagrams"
RESEARCH = ROOT / "research" / "13-stromal-figures.md"
JSON_OUT = OUT_DIR / "13-stromal-figures.json"
HANDOFF11 = ROOT / "research" / "11-expansion-inventory.json"
UNIT10_CSV = ROOT / "pipeline" / "output" / "10" / "states.csv"
UNIT12_CSV = ROOT / "pipeline" / "output" / "12" / "states.csv"
TISCH_BLCA = ROOT / "data" / "raw" / "tisch2" / "BLCA_GSE130001_CellMetainfo_table.tsv"

CORE_TYPES = ["NSCLC", "melanoma", "CRC", "BRCA", "BLCA"]
SUBTYPES = ["fibroblast", "endothelial", "pericyte/smooth muscle", "unmatched"]
CORE_ROLE = "core"
EXPANSION_ROLE = "expansion"


def stromal_subtype(label: str) -> str:
    """Group existing labels already in Stromal/other. First substring wins."""
    text = str(label).strip().lower()
    if "fibroblast" in text:
        return "fibroblast"
    if "endothelial" in text:
        return "endothelial"
    if "pericyte" in text or "smooth muscle" in text:
        return "pericyte/smooth muscle"
    return "unmatched"


def load_include_list() -> tuple[list[str], list[dict], dict[str, list[str]]]:
    payload = json.loads(HANDOFF11.read_text())
    included = [t["cancer_type"] for t in payload["types"] if t["decision"] == "include"]
    skipped = [
        {"cancer_type": t["cancer_type"], "reason": t["reason"]}
        for t in payload["types"]
        if t["decision"] == "skip"
    ]
    diseases = {
        t["cancer_type"]: list(t["disease_strings"])
        for t in payload["types"]
        if t["decision"] == "include"
    }
    return included, skipped, diseases


def load_states() -> pd.DataFrame:
    frames = []
    if not UNIT10_CSV.exists():
        raise SystemExit(f"Missing Unit 10 table: {UNIT10_CSV}")
    core = pd.read_csv(UNIT10_CSV)
    core["role"] = CORE_ROLE
    frames.append(core)
    if not UNIT12_CSV.exists():
        raise SystemExit(f"Missing Unit 12 table: {UNIT12_CSV}")
    exp = pd.read_csv(UNIT12_CSV)
    exp["role"] = EXPANSION_ROLE
    frames.append(exp)
    return pd.concat(frames, ignore_index=True)


def census_obs(diseases: list[str], mapper, drop_uveal: bool) -> pd.DataFrame:
    import cellxgene_census

    if not diseases:
        return pd.DataFrame(columns=["cell_type", "disease", "tissue_type", "cancer_type", "label"])
    obs_filter = census_obs_filter(diseases)
    print(f"Census get_obs ({len(diseases)} disease labels) …", flush=True)
    with cellxgene_census.open_soma(census_version=CENSUS_VERSION) as census:
        obs = cellxgene_census.get_obs(
            census,
            "homo_sapiens",
            value_filter=obs_filter,
            column_names=["soma_joinid", "cell_type", "disease", "tissue_type"],
        )
    print(f"  obs n={len(obs):,}", flush=True)
    if "tissue_type" in obs.columns:
        tt = obs["tissue_type"].astype(str).str.lower()
        obs = obs.loc[~tt.isin(CULTURE)].copy()
    dise = obs["disease"].astype(str)
    if drop_uveal:
        obs = obs.loc[~dise.str.lower().str.contains("uveal")].copy()
        dise = obs["disease"].astype(str)
    obs = obs.loc[dise.isin(diseases)].copy()
    obs["cancer_type"] = dise.map(mapper)
    obs = obs.loc[obs["cancer_type"].notna()].copy()
    obs["label"] = obs["cell_type"].astype(str)
    obs["source"] = "Census"
    print(obs["cancer_type"].value_counts().to_string(), flush=True)
    return obs[["cancer_type", "source", "label"]]


def blca_obs() -> pd.DataFrame:
    meta = pd.read_csv(TISCH_BLCA, sep="\t")
    col = "Celltype (major-lineage)" if "Celltype (major-lineage)" in meta.columns else meta.columns[4]
    return pd.DataFrame(
        {
            "cancer_type": "BLCA",
            "source": "TISCH2+GEO GSE130001",
            "label": meta[col].astype(str).to_numpy(),
        }
    )


def composition_tables(obs: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    work = obs.copy()
    work["bucket"] = work["label"].map(assign_bucket)
    stromal = work.loc[work["bucket"] == "Stromal/other"].copy()
    stromal["subtype"] = stromal["label"].map(stromal_subtype)
    rows = []
    unmatched_rows = []
    for (ctype, source), sub in stromal.groupby(["cancer_type", "source"], sort=False):
        n = int(len(sub))
        vc = sub["subtype"].value_counts()
        for st in SUBTYPES:
            k = int(vc.get(st, 0))
            rows.append(
                {
                    "cancer_type": ctype,
                    "source": source,
                    "subtype": st,
                    "n": k,
                    "n_stromal": n,
                    "pct": (100.0 * k / n) if n else np.nan,
                }
            )
        um = sub.loc[sub["subtype"] == "unmatched", "label"].value_counts()
        for lab, k in um.items():
            unmatched_rows.append(
                {
                    "cancer_type": ctype,
                    "source": source,
                    "label": str(lab),
                    "n": int(k),
                    "n_stromal": n,
                    "pct_of_stromal": (100.0 * int(k) / n) if n else np.nan,
                }
            )
    comp = pd.DataFrame(rows)
    unmatched = pd.DataFrame(unmatched_rows)
    return stromal, comp, unmatched


def type_order(included_exp: list[str]) -> list[str]:
    return [*CORE_TYPES, *included_exp]


def _fmt_pct(v) -> str:
    return "—" if v is None or pd.isna(v) else f"{v:.2f}"


def _fmt_n(n: int) -> str:
    return f"{n:,}"


def _fmt_mean(v) -> str:
    return "—" if v is None or pd.isna(v) else f"{v:.4f}"


def heatmap_mean_ecs(states: pd.DataFrame, order: list[str], path: Path) -> None:
    sub = states.copy()
    sub["cancer_type"] = pd.Categorical(sub["cancer_type"], categories=order, ordered=True)
    sub["bucket"] = pd.Categorical(sub["bucket"], categories=BUCKETS, ordered=True)
    mat = sub.pivot_table(index="cancer_type", columns="bucket", values="mean_ecs", aggfunc="first")
    mat = mat.reindex(index=order, columns=BUCKETS)
    nmat = sub.pivot_table(index="cancer_type", columns="bucket", values="n_cells", aggfunc="first")
    nmat = nmat.reindex(index=order, columns=BUCKETS)
    plot_mat = mat.mask(nmat.fillna(0) == 0)
    color = plot_mat.to_numpy(dtype=float)
    finite = color[np.isfinite(color)]
    vmin = float(np.nanmin(finite)) if len(finite) else 1e-4
    vmax = float(np.nanmax(finite)) if len(finite) else 1.0
    vmin = max(vmin, 1e-4)
    fig, ax = plt.subplots(figsize=(10.5, 8.5))
    cmap = plt.get_cmap("YlOrRd").copy()
    cmap.set_bad("#EEEEEE")
    im = ax.imshow(color, aspect="auto", cmap=cmap, norm=LogNorm(vmin=vmin, vmax=vmax))
    ax.set_xticks(range(len(BUCKETS)))
    ax.set_xticklabels(BUCKETS, rotation=30, ha="right")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order)
    ax.set_title("Mean core-ECS (type × bucket)")
    for i, ctype in enumerate(order):
        for j, bucket in enumerate(BUCKETS):
            val = plot_mat.iloc[i, j]
            if pd.isna(val):
                ax.text(j, i, "—", ha="center", va="center", fontsize=8, color="#666666")
            else:
                ax.text(j, i, f"{val:.3f}", ha="center", va="center", fontsize=7.5, color="black")
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("mean core-ECS (log color)")
    fig.tight_layout()
    fig.savefig(path, dpi=300, facecolor="white")
    plt.close(fig)


def heatmap_detection(states: pd.DataFrame, order: list[str], bucket: str, path: Path, title: str) -> None:
    sub = states.loc[states["bucket"] == bucket].copy()
    sub = sub.set_index("cancer_type").reindex(order)
    cols = [f"pct_{g}" for g in ECS]
    mat = sub[cols].apply(pd.to_numeric, errors="coerce")
    n = pd.to_numeric(sub["n_cells"], errors="coerce")
    mat = mat.mask(n.fillna(0) == 0, np.nan)
    color = mat.to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    cmap = plt.get_cmap("YlGnBu").copy()
    cmap.set_bad("#EEEEEE")
    im = ax.imshow(color, aspect="auto", cmap=cmap, vmin=0, vmax=50)
    ax.set_xticks(range(len(ECS)))
    ax.set_xticklabels(ECS, rotation=30, ha="right")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order)
    ax.set_title(title)
    for i in range(len(order)):
        for j in range(len(ECS)):
            val = color[i, j]
            if not np.isfinite(val):
                ax.text(j, i, "—", ha="center", va="center", fontsize=8, color="#666666")
            else:
                ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=7.5, color="black")
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("% cells with count > 0 (color clipped at 50)")
    fig.tight_layout()
    fig.savefig(path, dpi=300, facecolor="white")
    plt.close(fig)


def heatmap_composition(comp: pd.DataFrame, order: list[str], path: Path) -> None:
    sub = comp.copy()
    mat = sub.pivot_table(index="cancer_type", columns="subtype", values="pct", aggfunc="first")
    mat = mat.reindex(index=order, columns=SUBTYPES)
    n = sub.drop_duplicates("cancer_type").set_index("cancer_type")["n_stromal"].reindex(order)
    mat = mat.mask(n.fillna(0) == 0, np.nan)
    color = mat.to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(9.5, 8.5))
    cmap = plt.get_cmap("PuRd").copy()
    cmap.set_bad("#EEEEEE")
    im = ax.imshow(color, aspect="auto", cmap=cmap, vmin=0, vmax=100)
    ax.set_xticks(range(len(SUBTYPES)))
    ax.set_xticklabels(SUBTYPES, rotation=25, ha="right")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order)
    ax.set_title("Stromal/other composition (% of stromal cells)")
    for i in range(len(order)):
        for j in range(len(SUBTYPES)):
            val = color[i, j]
            if not np.isfinite(val):
                ax.text(j, i, "—", ha="center", va="center", fontsize=8, color="#666666")
            else:
                ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=8, color="black")
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("% of Stromal/other")
    fig.tight_layout()
    fig.savefig(path, dpi=300, facecolor="white")
    plt.close(fig)


def n_check(comp: pd.DataFrame, states: pd.DataFrame, order: list[str]) -> list[dict]:
    stromal_n = (
        states.loc[states["bucket"] == "Stromal/other", ["cancer_type", "n_cells"]]
        .drop_duplicates("cancer_type")
        .set_index("cancer_type")["n_cells"]
        .to_dict()
    )
    rows = []
    for ctype in order:
        sub = comp.loc[comp["cancer_type"] == ctype]
        n13 = 0 if sub.empty else int(sub["n_stromal"].iloc[0])
        n_ref = int(stromal_n.get(ctype, -1))
        rows.append(
            {
                "cancer_type": ctype,
                "n_stromal_13": n13,
                "n_stromal_ref": n_ref,
                "match": n13 == n_ref,
            }
        )
    return rows


def write_markdown(
    order: list[str],
    included_exp: list[str],
    skipped: list[dict],
    comp: pd.DataFrame,
    unmatched: pd.DataFrame,
    ncheck: list[dict],
    fig_rel: dict[str, str],
) -> str:
    skip_txt = "; ".join(f"`{s['cancer_type']}` ({s['reason']})" for s in skipped) or "none"
    n_mismatch = sum(1 for r in ncheck if not r["match"])
    lines = [
        "# Unit 13 — Stromal composition and figure pack",
        "",
        f"**Run date:** {date.today().isoformat()}  ",
        f"**Census version:** `{CENSUS_VERSION}`  ",
        f"**Kill protocol SHA:** `{KILL_SHA}`  ",
        f"**Atlas protocol SHA:** `{ATLAS_SHA}`  ",
        "**Rule:** Display-only. Among cells already in **Stromal/other**, tabulate "
        "existing Census `cell_type` / TISCH2 labels as fibroblast, endothelial, "
        "pericyte/smooth muscle, or unmatched. Do not cluster. Do not declare a "
        "new confirmatory state. Heatmaps are of Units 10 and 12 confirmatory "
        "tables. No UMAP. No ICI plots. Primary remains **Stromal/other**.",
        "",
        "## Sources",
        "",
        "- Core Census types (NSCLC, melanoma, CRC, BRCA): same disease strings and "
        "Unit 01 filter as Units 01–02 / 10. Obs-only (no expression re-read).",
        "- BLCA: TISCH2 `BLCA_GSE130001` `Celltype (major-lineage)` (already pinned).",
        "- Expansion included types: Unit 11 disease strings, same filter as Unit 12.",
        "- Heatmap values: `pipeline/output/10/states.csv` and "
        "`pipeline/output/12/states.csv`.",
        "",
        f"Types in composition tables: **{len(order)}** ({', '.join(order)}). "
        f"Expansion skips (not tabled here): {skip_txt}.",
        "",
        "## Display-only (not a new state)",
        "",
        f"Primary confirmatory name stays **{PRIMARY}**. Fibroblast / endothelial / "
        "pericyte-smooth-muscle / unmatched are **sublabels of that bucket**. They "
        "cannot rename it and are not Gate A / Gate B / Gate D tests.",
        "",
        "## Stromal n vs Units 10 / 12",
        "",
        f"Mismatches: **{n_mismatch}**.",
        "",
        "| Type | Unit 13 stromal n | Unit 10/12 stromal n | Match |",
        "|---|---:|---:|---|",
    ]
    for r in ncheck:
        lines.append(
            f"| {r['cancer_type']} | {_fmt_n(r['n_stromal_13'])} | "
            f"{_fmt_n(r['n_stromal_ref'])} | {r['match']} |"
        )

    lines += [
        "",
        "## Stromal/other composition",
        "",
        "Denominator = cells already assigned to Stromal/other. Percent is of that "
        "denominator. `myofibroblast` is counted as fibroblast (substring).",
        "",
        "| Type | Source | n stromal | Fibroblast n (%) | Endothelial n (%) | Pericyte/SM n (%) | Unmatched n (%) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for ctype in order:
        sub = comp.loc[comp["cancer_type"] == ctype]
        if sub.empty:
            continue
        source = str(sub["source"].iloc[0])
        n = int(sub["n_stromal"].iloc[0])
        by = sub.set_index("subtype")

        def cell(st: str) -> str:
            if st not in by.index:
                return "0 (—)" if n == 0 else "0 (0.00)"
            k = int(by.loc[st, "n"])
            return f"{k:,} ({_fmt_pct(by.loc[st, 'pct'])})"

        lines.append(
            f"| {ctype} | {source} | {n:,} | {cell('fibroblast')} | "
            f"{cell('endothelial')} | {cell('pericyte/smooth muscle')} | "
            f"{cell('unmatched')} |"
        )

    lines += [
        "",
        "### Per type",
        "",
    ]
    for ctype in order:
        sub = comp.loc[comp["cancer_type"] == ctype]
        if sub.empty:
            continue
        n = int(sub["n_stromal"].iloc[0])
        lines += [
            f"#### {ctype}",
            "",
            f"n Stromal/other = **{n:,}**. Sublabels are display-only.",
            "",
            "| Subtype | n | % of stromal |",
            "|---|---:|---:|",
        ]
        for row in sub.itertuples(index=False):
            lines.append(f"| {row.subtype} | {row.n:,} | {_fmt_pct(row.pct)} |")
        lines.append("")

    lines += [
        "## Unmatched labels (existing names only)",
        "",
        "Labels already in Stromal/other that did not match fibroblast / endothelial "
        "/ pericyte / smooth muscle. Listed so unmatched is not silent. Not a new "
        "confirmatory state. Rows with ≥ 1% of stromal, else top 5 per type.",
        "",
    ]
    if unmatched.empty:
        lines.append("None.")
        lines.append("")
    else:
        lines += [
            "| Type | Existing label | n | % of stromal |",
            "|---|---|---:|---:|",
        ]
        for ctype in order:
            u = unmatched.loc[unmatched["cancer_type"] == ctype]
            if u.empty:
                continue
            keep = u.loc[u["pct_of_stromal"] >= 1.0]
            if keep.empty:
                keep = u.nlargest(5, "n")
            else:
                keep = keep.sort_values("n", ascending=False)
            for row in keep.itertuples(index=False):
                lines.append(
                    f"| {ctype} | {row.label} | {row.n:,} | {_fmt_pct(row.pct_of_stromal)} |"
                )
        lines.append("")

    lines += [
        "## Figures",
        "",
        "Heatmaps of confirmatory tables (Units 10 and 12) plus the composition table. "
        "Grey = empty bucket (n = 0). Mean ECS color is log-scaled so melanoma does "
        "not wash out other types; printed numbers are raw means.",
        "",
        f"![Mean core-ECS by type and lineage bucket]({fig_rel['mean_ecs']})",
        "",
        f"![Nine-gene detection in Stromal/other]({fig_rel['detection']})",
        "",
        f"![Stromal/other subtype composition]({fig_rel['composition']})",
        "",
        "## What was not done",
        "",
        "- No clustering, NMF, or DE. No new confirmatory state from a subtype.",
        "- No UMAP, Harmony/scVI, or browser.",
        "- No ICI phenotype or outcome files opened. No ICI plots.",
        "- Primary **Stromal/other** not renamed. No gene added.",
        "- Myeloid / T/NK catalog rows from Unit 12 not promoted.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DIAGRAMS.mkdir(parents=True, exist_ok=True)
    included_exp, skipped, exp_diseases = load_include_list()
    order = type_order(included_exp)
    states = load_states()

    cache = OUT_DIR / "stromal_obs.parquet"
    if cache.exists():
        print("Loading cached stromal obs", flush=True)
        obs = pd.read_parquet(cache)
    else:
        core_diseases = list(dict.fromkeys(d for ds in DISEASES.values() for d in ds))
        core_obs = census_obs(core_diseases, _disease_type, drop_uveal=True)
        exp_list = list(dict.fromkeys(d for ds in exp_diseases.values() for d in ds))
        type_from_exact = {d: ctype for ctype, ds in exp_diseases.items() for d in ds}

        def exp_mapper(disease: str):
            return type_from_exact.get(str(disease))

        exp_obs = census_obs(exp_list, exp_mapper, drop_uveal=False)
        blca = blca_obs()
        obs = pd.concat([core_obs, blca, exp_obs], ignore_index=True)
        obs.to_parquet(cache, index=False)

    _stromal, comp, unmatched = composition_tables(obs)
    comp.to_csv(OUT_DIR / "composition.csv", index=False)
    if len(unmatched):
        unmatched.to_csv(OUT_DIR / "unmatched_labels.csv", index=False)
    ncheck = n_check(comp, states, order)

    mean_path = DIAGRAMS / "13-mean-ecs.png"
    det_path = DIAGRAMS / "13-detection-stromal.png"
    comp_path = DIAGRAMS / "13-stromal-composition.png"
    heatmap_mean_ecs(states, order, mean_path)
    heatmap_detection(
        states,
        order,
        "Stromal/other",
        det_path,
        "Nine-gene detection in Stromal/other (% cells count > 0)",
    )
    heatmap_composition(comp, order, comp_path)
    for src in (mean_path, det_path, comp_path):
        dst = OUT_DIR / src.name
        dst.write_bytes(src.read_bytes())
        print(f"Wrote {src}", flush=True)

    fig_rel = {
        "mean_ecs": "../docs/diagrams/13-mean-ecs.png",
        "detection": "../docs/diagrams/13-detection-stromal.png",
        "composition": "../docs/diagrams/13-stromal-composition.png",
    }
    RESEARCH.write_text(
        write_markdown(order, included_exp, skipped, comp, unmatched, ncheck, fig_rel)
    )
    payload = {
        "run_date": date.today().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "census_version": CENSUS_VERSION,
        "kill_protocol_sha": KILL_SHA,
        "atlas_protocol_sha": ATLAS_SHA,
        "types": order,
        "include_expansion": included_exp,
        "skip": skipped,
        "n_check": ncheck,
        "composition": comp.to_dict(orient="records"),
        "unmatched_n_labels": int(unmatched["label"].nunique()) if len(unmatched) else 0,
        "figures": [str(p.relative_to(ROOT)) for p in (mean_path, det_path, comp_path)],
        "ici_files_opened": False,
        "umap": False,
        "clustered": False,
        "primary": PRIMARY,
        "subtypes_are_display_only": True,
    }
    JSON_OUT.write_text(json.dumps(payload, indent=2, default=str))
    print(f"Wrote {RESEARCH}", flush=True)
    print(f"Wrote {JSON_OUT}", flush=True)
    print(json.dumps({"n_check": ncheck, "n_types": len(order)}, indent=2), flush=True)
    if any(not r["match"] for r in ncheck):
        print("WARNING: stromal n mismatch vs Units 10/12", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
