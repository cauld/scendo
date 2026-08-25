#!/usr/bin/env python3
"""Unit 12 — expansion ECS-state tables (Gate E). Census only. No ICI files. No TISCH2."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from detection_01 import CENSUS_VERSION, census_obs_filter  # noqa: E402
from genes import ECS  # noqa: E402
from inventory_11 import CULTURE, EXPANSION_TYPES, PROTOCOL_NAMES  # noqa: E402
from lineage import assign_bucket  # noqa: E402
from reproduce_10 import (  # noqa: E402
    ATLAS_SHA,
    FROZEN_BUCKETS,
    PRIMARY,
    load_frozen,
    load_primary_name,
)
from states_02 import (  # noqa: E402
    BUCKETS,
    PROTOCOL_SHA as KILL_SHA,
    QUERY_GENES,
    ROOT,
    _dataset_tables,
    _fmt_mean,
    _fmt_pct,
    _fmt_rank,
    _pick_contam_gene,
)

OUT_DIR = ROOT / "pipeline" / "output" / "12"
RESEARCH = ROOT / "research" / "12-expansion-states.md"
JSON_OUT = OUT_DIR / "12-expansion-states.json"
HANDOFF = ROOT / "research" / "11-expansion-inventory.json"
UNIT05 = ROOT / "research" / "05-primary-state.md"
NAMED_STATES = list(FROZEN_BUCKETS)
CATALOG_ONLY = ["Myeloid", "T/NK"]


def load_handoff() -> dict:
    if not HANDOFF.exists():
        raise SystemExit(f"Missing Unit 11 handoff: {HANDOFF}")
    payload = json.loads(HANDOFF.read_text())
    types = payload.get("types") or []
    got = [t["cancer_type"] for t in types]
    if got != list(EXPANSION_TYPES):
        raise SystemExit(f"Unit 11 type list drifted from protocol: {got}")
    return payload


def run_census_type(ctype: str, diseases: list[str]) -> tuple[pd.DataFrame, dict]:
    import cellxgene_census
    import tiledbsoma as soma

    cache = OUT_DIR / f"{ctype}_cells.parquet"
    meta_path = OUT_DIR / f"{ctype}_query_meta.json"
    if cache.exists() and meta_path.exists():
        print(f"Loading cached {ctype} cells", flush=True)
        return pd.read_parquet(cache), json.loads(meta_path.read_text())

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    obs_filter = census_obs_filter(diseases)
    print(
        f"{ctype}: Census obs filter ({len(diseases)} disease labels, "
        f"{len(QUERY_GENES)} genes) …",
        flush=True,
    )

    with cellxgene_census.open_soma(census_version=CENSUS_VERSION) as census:
        hs = census["census_data"]["homo_sapiens"]
        query = hs.axis_query(
            measurement_name="RNA",
            obs_query=soma.AxisQuery(value_filter=obs_filter),
            var_query=soma.AxisQuery(value_filter=f"feature_name in {QUERY_GENES}"),
        )
        print(f"  {ctype}: reading obs …", flush=True)
        obs = query.obs(column_names=["soma_joinid", "cell_type", "disease", "tissue_type"]).concat().to_pandas()
        print(f"  {ctype}: obs n={len(obs):,}", flush=True)
        var = query.var(column_names=["soma_joinid", "feature_name"]).concat().to_pandas()
        genes_found = list(var["feature_name"].astype(str))
        print(f"  {ctype}: var {genes_found}", flush=True)
        gid_to_gene = dict(zip(var["soma_joinid"].astype(int), var["feature_name"].astype(str)))

        if "tissue_type" in obs.columns:
            tt = obs["tissue_type"].astype(str).str.lower()
            obs = obs.loc[~tt.isin(CULTURE)].copy()
        dise = obs["disease"].astype(str)
        obs = obs.loc[dise.isin(diseases)].copy()
        obs["cancer_type"] = ctype
        print(f"  {ctype}: after Unit 01 filter n={len(obs):,}", flush=True)

        obs = obs.sort_values("soma_joinid").reset_index(drop=True)
        join_ids = obs["soma_joinid"].astype(int).to_numpy()
        n = len(obs)
        gene_cols = {g: i for i, g in enumerate(QUERY_GENES) if g in set(genes_found)}
        counts = np.zeros((n, len(QUERY_GENES)), dtype=np.float32)
        nnz = 0
        print(f"  {ctype}: reading sparse X (ECS + contamination genes) …", flush=True)
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
        print(f"  {ctype}: nnz stored: {nnz:,}", flush=True)

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
    cells.to_parquet(cache, index=False)
    dropped = [g for g in ECS if g not in set(genes_found)]
    meta = {
        "cancer_type": ctype,
        "diseases": diseases,
        "genes_found": genes_found,
        "ecs_dropped": dropped,
        "contam_gene": _pick_contam_gene(genes_found),
        "n_cells": int(len(cells)),
        "n_obs_raw": int(n),
    }
    meta_path.write_text(json.dumps(meta, indent=2))
    return cells, meta


def catalog_summary(table: pd.DataFrame) -> dict:
    kept = table[table["kept"]]
    buckets = [b for b in BUCKETS if b in set(kept["bucket"].tolist())]
    types_by_bucket = {
        b: sorted(kept.loc[kept["bucket"] == b, "cancer_type"].unique().tolist()) for b in buckets
    }
    myeloid_tnk = [b for b in buckets if b in CATALOG_ONLY]
    named_catalog = [b for b in buckets if b in NAMED_STATES]
    return {
        "catalog_kept_buckets": buckets,
        "types_by_bucket": types_by_bucket,
        "named_state_catalog_calls": named_catalog,
        "myeloid_tnk_catalog_calls": myeloid_tnk,
        "confirmatory_named_states": list(NAMED_STATES),
        "note": (
            "Expansion ECS-state calls are catalog rows. Confirmatory named states "
            "stay B/plasma, Malignant/epithelial, and Stromal/other. Myeloid / T/NK "
            "true-calls are not new confirmatory named states."
        ),
    }


def gate_e(
    handoff: dict,
    table: pd.DataFrame,
    included: list[str],
    skipped: list[dict],
    summary: dict,
    primary: str,
    genes_ok: bool,
    n_extra: int,
    tisch2: bool,
    ici: bool,
) -> dict:
    locked = list(EXPANSION_TYPES)
    handoff_types = [t["cancer_type"] for t in handoff["types"]]
    table_types = sorted(table["cancer_type"].unique().tolist()) if len(table) else []
    expected_include = [t["cancer_type"] for t in handoff["types"] if t["decision"] == "include"]
    expected_skip = [t["cancer_type"] for t in handoff["types"] if t["decision"] == "skip"]
    every_locked = handoff_types == locked
    include_match = included == expected_include and set(table_types) == set(expected_include)
    skip_match = [s["cancer_type"] for s in skipped] == expected_skip
    skip_reasons = all(bool(s.get("reason")) for s in skipped)
    buckets_ok = True
    if len(table):
        for ctype in expected_include:
            got = table.loc[table["cancer_type"] == ctype, "bucket"].tolist()
            if got != list(BUCKETS):
                buckets_ok = False
                break
    named_ok = summary["confirmatory_named_states"] == NAMED_STATES
    # Promotion fail = putting myeloid/T/NK into confirmatory named states.
    not_promoted = named_ok and "Myeloid" not in summary["confirmatory_named_states"] and "T/NK" not in summary[
        "confirmatory_named_states"
    ]
    primary_ok = primary == PRIMARY
    sources = set(table["source"].tolist()) if len(table) else set()
    census_only = sources <= {"Census"}
    operator_pass = bool(
        genes_ok
        and every_locked
        and include_match
        and skip_match
        and skip_reasons
        and buckets_ok
        and n_extra == 0
        and not tisch2
        and not ici
        and named_ok
        and not_promoted
        and primary_ok
        and census_only
    )
    return {
        "every_type_tabled_or_skipped": bool(every_locked and include_match and skip_match and skip_reasons and buckets_ok),
        "no_extra_types": n_extra == 0,
        "no_tisch2": (not tisch2) and census_only,
        "no_ici_files": not ici,
        "genes_unchanged": genes_ok,
        "named_states_unchanged": named_ok,
        "named_states": list(summary["confirmatory_named_states"]),
        "myeloid_tnk_not_promoted": not_promoted,
        "myeloid_tnk_catalog_calls": list(summary["myeloid_tnk_catalog_calls"]),
        "primary_still_stromal_other": primary_ok,
        "primary": primary,
        "operator_gate_e_holds": operator_pass,
        "note": (
            "Gate E is human-owned. Operator draft holds if every locked expansion "
            "type has a complete type × lineage table or a documented skip (missing "
            "in Census or n < 10,000), no substitute types, no TISCH2, nine genes "
            "unchanged, confirmatory named states stay the three frozen buckets, "
            "myeloid / T/NK catalog rows are not promoted, and the primary remains "
            "Stromal/other."
        ),
    }


def write_markdown(
    table: pd.DataFrame,
    summary: dict,
    metas: dict[str, dict],
    n_vs_11: list[dict],
    handoff: dict,
    included: list[str],
    skipped: list[dict],
    gates: dict,
    primary: str,
) -> str:
    def fmt_n(n: int) -> str:
        return f"{n:,}"

    skip_txt = "; ".join(f"{s['cancer_type']} ({s['reason']})" for s in skipped) or "none"
    ecs_dropped = sorted({g for m in metas.values() for g in (m.get("ecs_dropped") or [])})
    contam_genes = sorted({m.get("contam_gene") or "none" for m in metas.values()})
    lines = [
        "# Unit 12 — Expansion ECS-state tables (Gate E)",
        "",
        f"**Run date:** {date.today().isoformat()}  ",
        f"**Census version:** `{CENSUS_VERSION}`  ",
        f"**Kill protocol SHA:** `{KILL_SHA}`  ",
        f"**Atlas protocol SHA:** `{ATLAS_SHA}`  ",
        "**Rule:** Same detection / mean / contamination / ECS-state table as Unit 10, "
        "for every **included** expansion type. A lineage has an ECS-state catalog "
        "call in a cancer type if ≥1 core gene is detected (count > 0) in ≥5% of "
        "that lineage’s cells **and** the lineage mean core-ECS score is highest or "
        "second-highest among buckets with cells in that type. Non-B lineages with "
        "contamination-gene detection ≥ 10% are discarded in that type. "
        "Confirmatory **named** states stay B/plasma, Malignant/epithelial, "
        "Stromal/other. Expansion calls are catalog rows. No ICI labels. No TISCH2. "
        "No NMF / clustering / DE. Primary name is not re-opened.",
        "",
        "## Sources",
        "",
        f"- CELLxGENE Census pin `{CENSUS_VERSION}`, `is_primary_data == True`, "
        "raw RNA counts. One query per included type (Unit 11 disease strings).",
        "- Cell filter: same as Unit 01 (`census_obs_filter` + culture/organoid/"
        "cell-line drop).",
        "- Lineage buckets: locked substring map in kill `PROTOCOL.md` / `pipeline/lineage.py`.",
        "- Include / skip list: `research/11-expansion-inventory.json`.",
        "",
        f"Included types tabled: **{len(included)}** ({', '.join(included) or 'none'}). "
        f"Skipped (one-line reason): **{len(skipped)}** ({skip_txt}).",
        "",
        "## Frozen objects (unchanged)",
        "",
        f"- Nine core genes: `{', '.join(ECS)}`. **Unchanged:** {gates['genes_unchanged']}.",
        f"- Named states: {', '.join(NAMED_STATES)}.",
        f"- Primary display name: **{primary}**. **Unchanged:** {gates['primary_still_stromal_other']}.",
        "",
        "## Scoring",
        "",
        "- Cell score = available-case mean of the nine core genes on **raw counts** "
        "(denominator = genes present in that matrix; min 7/9 or no score).",
        "- Lineage mean = mean of cell scores in that bucket. Rank uses competition ranking "
        "(highest mean = 1; ties share the minimum rank). Empty buckets are not ranked.",
        "- All five lineage buckets are scored. Myeloid / T/NK catalog calls are not "
        "confirmatory named states.",
        "",
        "## Include / skip (from Unit 11)",
        "",
        "| Type | Protocol name | Decision | Reason | Unit 11 n | Unit 12 n |",
        "|---|---|---|---|---:|---:|",
    ]
    n12 = {r["cancer_type"]: r["n_12"] for r in n_vs_11}
    for t in handoff["types"]:
        ctype = t["cancer_type"]
        n12_txt = fmt_n(n12[ctype]) if ctype in n12 else "—"
        lines.append(
            f"| {ctype} | {PROTOCOL_NAMES[ctype]} | **{t['decision']}** | {t['reason']} | "
            f"{fmt_n(int(t['n_cells']))} | {n12_txt} |"
        )

    lines += [
        "",
        "Skipped types (one-line reason):",
        "",
    ]
    for s in skipped:
        lines.append(f"- `{s['cancer_type']}`: {s['reason']}")
    lines += [
        "",
        "## Genes present / dropped",
        "",
        f"- Census ECS dropped: **{', '.join(ecs_dropped) if ecs_dropped else 'none'}**. "
        f"Contamination gene(s): **{', '.join(contam_genes)}**.",
        "",
        f"Non-B lineages discarded for contamination (≥ 10%): "
        f"**{int(table['discarded'].sum()) if len(table) else 0}**.",
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
        "## Catalog ECS-state calls (not new named states)",
        "",
        "A kept=True row is a catalog call under the kill ECS-state + contamination "
        "rule. Confirmatory **named** states are not expanded beyond the three frozen "
        "buckets.",
        "",
    ]
    if summary["catalog_kept_buckets"]:
        lines.append("| Bucket | Expansion types where kept | Role |")
        lines.append("|---|---|---|")
        for b in summary["catalog_kept_buckets"]:
            types_b = ", ".join(summary["types_by_bucket"][b])
            role = "frozen named state" if b in NAMED_STATES else "catalog row only"
            lines.append(f"| {b} | {types_b} | {role} |")
    else:
        lines.append("None.")
    lines.append("")
    if summary["myeloid_tnk_catalog_calls"]:
        calls = ", ".join(summary["myeloid_tnk_catalog_calls"])
        lines.append(
            f"Myeloid / T/NK catalog calls: **{calls}**. These rows stay catalog-only "
            "and are **not** confirmatory named states."
        )
        lines.append("")
    else:
        lines.append("No myeloid / T/NK catalog calls.")
        lines.append("")

    lines += [
        "## Gate E draft (human marks)",
        "",
        f"- Every locked type tabled or skipped with a reason: **{gates['every_type_tabled_or_skipped']}**",
        f"- Extra types added: **{0 if gates['no_extra_types'] else 'yes'}**",
        f"- TISCH2 used: **{not gates['no_tisch2']}**",
        f"- ICI files opened: **{not gates['no_ici_files']}**",
        f"- Nine core genes unchanged: **{gates['genes_unchanged']}**",
        f"- Named states unchanged ({', '.join(NAMED_STATES)}): **{gates['named_states_unchanged']}**",
        f"- Myeloid / T/NK not promoted to named states: **{gates['myeloid_tnk_not_promoted']}**",
        f"- Primary remains **Stromal/other**: **{gates['primary_still_stromal_other']}**",
        f"- Operator Gate E numbers hold: **{gates['operator_gate_e_holds']}**",
        "",
        gates["note"],
        "",
        "## Human Gate E",
        "",
        "- [ ] Pass (every type tabled or skipped; no substitutes; named states unchanged)",
        "- [ ] Fail (silent drop / extra type / TISCH2 / promoted named state)",
        "",
        "## What was not done",
        "",
        "- No TISCH2 (or other) substitution for skipped types.",
        "- No extra cancer type added.",
        "- No ICI phenotype or outcome files opened.",
        "- No NMF, new clustering, or DE. No UMAP / browser.",
        "- No gene added. Primary **Stromal/other** not renamed.",
        "- Myeloid / T/NK catalog rows not promoted to confirmatory named states.",
        "- No stromal subtype table (Unit 13).",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    frozen = load_frozen()
    if not UNIT05.exists():
        raise SystemExit(f"Missing Unit 05 artifact: {UNIT05}")
    primary = load_primary_name(UNIT05.read_text())
    genes_ok = list(ECS) == frozen["marker_list"]["genes"] == frozen["core_ecs_genes"]
    handoff = load_handoff()

    included = [t["cancer_type"] for t in handoff["types"] if t["decision"] == "include"]
    skipped = [
        {"cancer_type": t["cancer_type"], "reason": t["reason"]}
        for t in handoff["types"]
        if t["decision"] == "skip"
    ]

    tables = []
    metas: dict[str, dict] = {}
    n_vs_11 = []
    for t in handoff["types"]:
        ctype = t["cancer_type"]
        if t["decision"] != "include":
            n_vs_11.append({"cancer_type": ctype, "n_11": int(t["n_cells"]), "n_12": 0, "decision": "skip"})
            continue
        diseases = list(t["disease_strings"])
        cells, meta = run_census_type(ctype, diseases)
        metas[ctype] = meta
        tbl = _dataset_tables(cells, meta.get("contam_gene"), meta.get("ecs_dropped") or [])
        # Keep protocol bucket order per type.
        tbl["_bucket_i"] = tbl["bucket"].map({b: i for i, b in enumerate(BUCKETS)})
        tbl = tbl.sort_values("_bucket_i").drop(columns="_bucket_i")
        tables.append(tbl)
        n_vs_11.append(
            {
                "cancer_type": ctype,
                "n_11": int(t["n_cells"]),
                "n_12": int(meta["n_cells"]),
                "decision": "include",
                "n_match": int(meta["n_cells"]) == int(t["n_cells"]),
            }
        )
        print(
            f"{ctype}: Unit 11 n={t['n_cells']:,}; Unit 12 n={meta['n_cells']:,}; "
            f"contam={meta.get('contam_gene')}",
            flush=True,
        )

    table = pd.concat(tables, ignore_index=True) if tables else pd.DataFrame()
    if len(table):
        table.to_csv(OUT_DIR / "states.csv", index=False)
    summary = catalog_summary(table) if len(table) else catalog_summary(
        pd.DataFrame(columns=["kept", "bucket", "cancer_type"])
    )
    gates = gate_e(
        handoff,
        table,
        included,
        skipped,
        summary,
        primary,
        genes_ok,
        n_extra=0,
        tisch2=False,
        ici=False,
    )

    payload = {
        "run_date": date.today().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "census_version": CENSUS_VERSION,
        "kill_protocol_sha": KILL_SHA,
        "atlas_protocol_sha": ATLAS_SHA,
        "include": included,
        "skip": skipped,
        "n_vs_unit11": n_vs_11,
        "per_type_meta": metas,
        "primary": primary,
        "summary": summary,
        "gate_e": gates,
        "table": table.to_dict(orient="records") if len(table) else [],
        "ici_files_opened": False,
        "tisch2_used": False,
        "n_extra_types": 0,
    }
    JSON_OUT.write_text(json.dumps(payload, indent=2, default=str))
    RESEARCH.write_text(
        write_markdown(table, summary, metas, n_vs_11, handoff, included, skipped, gates, primary)
    )
    print(f"Wrote {RESEARCH}", flush=True)
    print(f"Wrote {JSON_OUT}", flush=True)
    print(
        json.dumps(
            {
                "include": included,
                "skip": skipped,
                "n_vs_unit11": n_vs_11,
                "summary": summary,
                "gate_e": gates,
            },
            indent=2,
            default=str,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
