#!/usr/bin/env python3
"""Unit 10 — reproduce core five-type ECS-state catalog (Gate D). No ICI files."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from detection_01 import CENSUS_VERSION  # noqa: E402
from freeze_03 import UNIT02, parse_unit02  # noqa: E402
from genes import ECS  # noqa: E402
from states_02 import (  # noqa: E402
    BUCKETS,
    PROTOCOL_SHA as KILL_SHA,
    ROOT,
    _dataset_tables,
    _fmt_mean,
    _fmt_pct,
    _fmt_rank,
    run_census,
    run_tisch_blca,
    summarize,
)

OUT_DIR = ROOT / "pipeline" / "output" / "10"
RESEARCH = ROOT / "research" / "10-reproduce-core.md"
JSON_OUT = OUT_DIR / "10-reproduce-core.json"
UNIT02_JSON = ROOT / "pipeline" / "output" / "02" / "02-scrna-states.json"
FROZEN = ROOT / "research" / "03-frozen-markers.json"
UNIT05 = ROOT / "research" / "05-primary-state.md"
ATLAS_SHA = "2a74270a16685cbc4df5c45c293a7afb5b7665f5"
FROZEN_BUCKETS = ["B/plasma", "Malignant/epithelial", "Stromal/other"]
PRIMARY = "Stromal/other"
MEAN_DP = 4
PCT_DP = 2


def _round_or_none(v, ndigits: int):
    if v is None or (isinstance(v, float) and np.isnan(v)) or pd.isna(v):
        return None
    return round(float(v), ndigits)


def load_frozen() -> dict:
    if not FROZEN.exists():
        raise SystemExit(f"Missing Unit 03 freeze: {FROZEN}")
    frozen = json.loads(FROZEN.read_text())
    genes = frozen["marker_list"]["genes"]
    if genes != list(ECS):
        raise SystemExit(f"Frozen genes drifted from protocol: {genes}")
    lineages = frozen["marker_list"]["lineages"]
    if lineages != FROZEN_BUCKETS:
        raise SystemExit(f"Frozen lineages drifted: {lineages}")
    return frozen


def load_primary_name(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("- **Name:**"):
            return line.split("**Name:**", 1)[1].strip()
    raise SystemExit(f"Missing primary name in {UNIT05}")


def load_unit02_table() -> tuple[pd.DataFrame, dict, str]:
    if UNIT02_JSON.exists():
        payload = json.loads(UNIT02_JSON.read_text())
        table = pd.DataFrame(payload["table"])
        summary = payload["summary"]
        return table, summary, str(UNIT02_JSON.relative_to(ROOT))
    lineage, candidates, _sources = parse_unit02(UNIT02.read_text())
    table = pd.DataFrame(lineage)
    types_by_bucket = {c["bucket"]: c["cancer_types"] for c in candidates}
    summary = {
        "buckets_with_ecs_state": [c["bucket"] for c in candidates],
        "types_by_bucket": types_by_bucket,
    }
    return table, summary, str(UNIT02.relative_to(ROOT))


def _key_rows(table: pd.DataFrame) -> dict[tuple[str, str], pd.Series]:
    return {(str(r.cancer_type), str(r.bucket)): r for r in table.itertuples(index=False)}


def compare_tables(unit10: pd.DataFrame, unit02: pd.DataFrame) -> dict:
    keys10 = _key_rows(unit10)
    keys02 = _key_rows(unit02)
    all_keys = sorted(set(keys10) | set(keys02))
    rows = []
    flips = []
    missing = []
    extra = []
    n_cell_mismatches = 0
    rank_mismatches = 0
    max_mean_abs = 0.0
    max_contam_abs = 0.0
    for key in all_keys:
        ctype, bucket = key
        a = keys10.get(key)
        b = keys02.get(key)
        if a is None:
            missing.append({"cancer_type": ctype, "bucket": bucket, "side": "unit10_missing"})
            continue
        if b is None:
            extra.append({"cancer_type": ctype, "bucket": bucket, "side": "unit02_missing"})
            continue
        kept10 = bool(a.kept)
        kept02 = bool(b.kept)
        flip = kept10 != kept02
        if flip:
            flips.append(
                {
                    "cancer_type": ctype,
                    "bucket": bucket,
                    "unit02_kept": kept02,
                    "unit10_kept": kept10,
                }
            )
        n10 = int(a.n_cells)
        n02 = int(b.n_cells)
        if n10 != n02:
            n_cell_mismatches += 1
        mean10 = None if pd.isna(a.mean_ecs) else float(a.mean_ecs)
        mean02 = None if pd.isna(b.mean_ecs) else float(b.mean_ecs)
        mean_abs = 0.0
        if mean10 is not None and mean02 is not None:
            mean_abs = abs(mean10 - mean02)
            max_mean_abs = max(max_mean_abs, mean_abs)
        elif mean10 is not None or mean02 is not None:
            mean_abs = float("inf")
            max_mean_abs = float("inf")
        rank10 = None if pd.isna(a.rank) else int(a.rank)
        rank02 = None if pd.isna(getattr(b, "rank", np.nan)) else int(b.rank)
        if rank10 != rank02:
            rank_mismatches += 1
        contam10 = None if pd.isna(a.contam_pct) else float(a.contam_pct)
        contam02 = None if pd.isna(getattr(b, "contam_pct", np.nan)) else float(b.contam_pct)
        contam_abs = 0.0
        if contam10 is not None and contam02 is not None:
            contam_abs = abs(contam10 - contam02)
            max_contam_abs = max(max_contam_abs, contam_abs)
        elif contam10 is not None or contam02 is not None:
            # Unit 02 markdown uses — for B/plasma; treat both-missing as zero drift.
            if not (contam10 is None and contam02 is None):
                if {contam10, contam02} != {None}:
                    # one side missing, other present
                    if not (
                        (contam10 is None and (pd.isna(getattr(b, "contam_pct", np.nan)) or getattr(b, "contam_pct", None) is None))
                        or (contam02 is None and pd.isna(a.contam_pct))
                    ):
                        contam_abs = abs((contam10 or 0.0) - (contam02 or 0.0))
                        max_contam_abs = max(max_contam_abs, contam_abs)
        published_mean_drift = _round_or_none(mean10, MEAN_DP) != _round_or_none(mean02, MEAN_DP)
        published_contam_drift = _round_or_none(contam10, PCT_DP) != _round_or_none(contam02, PCT_DP)
        any_drift = bool(
            flip
            or n10 != n02
            or rank10 != rank02
            or published_mean_drift
            or published_contam_drift
        )
        rows.append(
            {
                "cancer_type": ctype,
                "bucket": bucket,
                "n_cells_10": n10,
                "n_cells_02": n02,
                "mean_ecs_10": mean10,
                "mean_ecs_02": mean02,
                "mean_abs_diff": None if mean_abs == float("inf") else mean_abs,
                "rank_10": rank10,
                "rank_02": rank02,
                "kept_10": kept10,
                "kept_02": kept02,
                "flip": flip,
                "any_published_drift": any_drift,
            }
        )
    return {
        "rows": rows,
        "flips": flips,
        "missing": missing,
        "extra": extra,
        "n_cell_mismatches": n_cell_mismatches,
        "rank_mismatches": rank_mismatches,
        "max_mean_abs_diff": max_mean_abs,
        "max_contam_abs_diff": max_contam_abs,
        "n_published_drift_rows": int(sum(1 for r in rows if r["any_published_drift"])),
    }


def gate_d(
    summary: dict,
    primary: str,
    genes_ok: bool,
    comparison: dict,
) -> dict:
    buckets = list(summary["buckets_with_ecs_state"])
    same_three = buckets == FROZEN_BUCKETS
    no_flip = comparison["flips"] == []
    no_missing = comparison["missing"] == [] and comparison["extra"] == []
    myeloid_or_tnk = [b for b in buckets if b in {"Myeloid", "T/NK"}]
    primary_ok = primary == PRIMARY
    operator_pass = bool(genes_ok and same_three and no_flip and no_missing and not myeloid_or_tnk and primary_ok)
    return {
        "genes_unchanged": genes_ok,
        "buckets_match_unit02": same_three,
        "buckets": buckets,
        "no_kept_dropped_flip": no_flip,
        "no_new_confirmatory_bucket": myeloid_or_tnk == [],
        "primary_still_stromal_other": primary_ok,
        "primary": primary,
        "operator_gate_d_holds": operator_pass,
        "note": (
            "Gate D is human-owned. Operator draft holds if the nine genes are unchanged, "
            "the kept ECS-state buckets are still B/plasma, Malignant/epithelial, and "
            "Stromal/other, no type×bucket kept↔dropped flip vs Unit 02, myeloid/T/NK "
            "are not confirmatory named states, and the primary remains Stromal/other."
        ),
    }


def write_markdown(
    table: pd.DataFrame,
    summary: dict,
    census_meta: dict,
    blca_meta: dict,
    comparison: dict,
    gates: dict,
    unit02_source: str,
    primary: str,
) -> str:
    types = sorted(table["cancer_type"].unique().tolist())
    lines = [
        "# Unit 10 — Reproduce core map (Gate D)",
        "",
        f"**Run date:** {date.today().isoformat()}  ",
        f"**Census version:** `{CENSUS_VERSION}`  ",
        f"**Kill protocol SHA:** `{KILL_SHA}`  ",
        f"**Atlas protocol SHA:** `{ATLAS_SHA}`  ",
        "**Rule:** Same cell filters and scoring as Units 01–02. A lineage has an ECS "
        "state in a cancer type if ≥1 core gene is detected (count > 0) in ≥5% of that "
        "lineage’s cells **and** the lineage mean core-ECS score is highest or "
        "second-highest among buckets with cells in that type. Non-B lineages with "
        "contamination-gene detection ≥ 10% are discarded in that type. "
        "No ICI labels. No NMF / clustering / DE. Primary name is not re-opened.",
        "",
        "## Sources",
        "",
        "- NSCLC, melanoma, CRC, BRCA: CELLxGENE Census pin `2025-11-08`, "
        "`is_primary_data == True`, raw RNA counts (Unit 02 cell-level cache; re-query "
        "if that cache is absent).",
        "- BLCA: TISCH2 `BLCA_GSE130001` cell types + GEO `GSE130001` MTX counts "
        "(barcode-matched).",
        "- Lineage buckets: locked substring map in kill `PROTOCOL.md` / `pipeline/lineage.py`.",
        "- Comparison baseline: Unit 02 catalog "
        f"(`{unit02_source}` and `research/02-scrna-states.md`).",
        "",
        f"Types available: **{len(types)}** ({', '.join(types)}).",
        "",
        "## Frozen objects (unchanged)",
        "",
        f"- Nine core genes: `{', '.join(ECS)}`. **Unchanged:** {gates['genes_unchanged']}.",
        f"- Named states: {', '.join(FROZEN_BUCKETS)}.",
        f"- Primary display name: **{primary}**. **Unchanged:** {gates['primary_still_stromal_other']}.",
        "",
        "## Scoring",
        "",
        "- Cell score = available-case mean of the nine core genes on **raw counts** "
        "(denominator = genes present in that matrix; min 7/9 or no score).",
        "- Lineage mean = mean of cell scores in that bucket. Rank uses competition ranking "
        "(highest mean = 1; ties share the minimum rank). Empty buckets are not ranked.",
        "",
        "## Genes present / dropped",
        "",
        f"- Census ECS dropped: **{census_meta.get('ecs_dropped') or 'none'}**. "
        f"Contamination gene: **{census_meta.get('contam_gene') or 'none'}**.",
        f"- BLCA ECS dropped: **{blca_meta.get('ecs_dropped') or 'none'}**. "
        f"Contamination gene: **{blca_meta.get('contam_gene') or 'none'}**.",
        "",
        f"Non-B lineages discarded for contamination (≥ 10%): "
        f"**{int(table['discarded'].sum())}**.",
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

    max_mean = comparison["max_mean_abs_diff"]
    max_contam = comparison["max_contam_abs_diff"]
    mean_txt = "—" if max_mean == float("inf") else f"{max_mean:.6g}"
    contam_txt = "—" if max_contam == float("inf") else f"{max_contam:.6g}"
    lines += [
        "",
        "## Comparison to Unit 02",
        "",
        f"- Kept↔dropped flips: **{len(comparison['flips'])}**.",
        f"- Rows missing from one table: **{len(comparison['missing']) + len(comparison['extra'])}**.",
        f"- n-cell mismatches: **{comparison['n_cell_mismatches']}**.",
        f"- Rank mismatches: **{comparison['rank_mismatches']}**.",
        f"- Max |Δ mean ECS|: **{mean_txt}**.",
        f"- Max |Δ contamination %|: **{contam_txt}**.",
        f"- Rows with drift at published precision (mean 4 d.p., % 2 d.p., or n/rank/kept): "
        f"**{comparison['n_published_drift_rows']}**.",
        "",
    ]
    if comparison["flips"]:
        lines += [
            "| Type | Bucket | Unit 02 kept | Unit 10 kept |",
            "|---|---|---|---|",
        ]
        for flip in comparison["flips"]:
            lines.append(
                f"| {flip['cancer_type']} | {flip['bucket']} | {flip['unit02_kept']} | {flip['unit10_kept']} |"
            )
        lines.append("")
    else:
        lines.append("No kept↔dropped flips.")
        lines.append("")

    drift_rows = [r for r in comparison["rows"] if r["any_published_drift"]]
    if drift_rows:
        lines += [
            "| Type | Bucket | n 02 | n 10 | Mean 02 | Mean 10 | Rank 02 | Rank 10 | Kept 02 | Kept 10 |",
            "|---|---|---:|---:|---:|---:|---:|---:|---|---|",
        ]
        for r in drift_rows:
            lines.append(
                f"| {r['cancer_type']} | {r['bucket']} | {r['n_cells_02']} | {r['n_cells_10']} | "
                f"{_fmt_mean(r['mean_ecs_02'])} | {_fmt_mean(r['mean_ecs_10'])} | "
                f"{_fmt_rank(r['rank_02'])} | {_fmt_rank(r['rank_10'])} | {r['kept_02']} | {r['kept_10']} |"
            )
        lines.append("")
    else:
        lines.append(
            "Numeric drift at published precision: **none**. Catalog matches Unit 02."
        )
        lines.append("")

    lines += [
        "## Gate D draft (human marks)",
        "",
        f"- Nine core genes unchanged: **{gates['genes_unchanged']}**",
        f"- Kept ECS-state buckets: **{', '.join(gates['buckets']) or 'none'}** "
        f"(match Unit 02 three: **{gates['buckets_match_unit02']}**)",
        f"- No type×bucket kept↔dropped flip: **{gates['no_kept_dropped_flip']}**",
        f"- No new confirmatory bucket (myeloid / T/NK not named): **{gates['no_new_confirmatory_bucket']}**",
        f"- Primary remains **Stromal/other**: **{gates['primary_still_stromal_other']}**",
        f"- Operator Gate D numbers hold: **{gates['operator_gate_d_holds']}**",
        "",
        gates["note"],
        "",
        "## Human Gate D",
        "",
        "- [ ] Pass (same three buckets; primary Stromal/other)",
        "- [ ] Fail (kept↔dropped flip / new confirmatory bucket / genes added / primary renamed)",
        "",
        "## What was not done",
        "",
        "- No ICI phenotype or outcome files opened.",
        "- No NMF, new clustering, or DE.",
        "- No gene added. Primary **Stromal/other** not renamed.",
        "- No expansion types (Unit 11). No stromal subtype table (Unit 13). No UMAP.",
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

    census_cells, census_meta = run_census()
    blca_cells, blca_meta = run_tisch_blca()
    census_tbl = _dataset_tables(census_cells, census_meta.get("contam_gene"), census_meta.get("ecs_dropped") or [])
    blca_tbl = _dataset_tables(blca_cells, blca_meta.get("contam_gene"), blca_meta.get("ecs_dropped") or [])
    table = pd.concat([census_tbl, blca_tbl], ignore_index=True)
    table.to_csv(OUT_DIR / "states.csv", index=False)
    summary = summarize(table)
    summary["note"] = (
        "Unit 10 reproduces the Unit 02 catalog. Named states stay the three frozen "
        "buckets. Myeloid and T/NK catalog rows are not confirmatory named states. "
        "Primary remains Stromal/other (Unit 05). Gate D is human-owned."
    )

    unit02_table, _unit02_summary, unit02_source = load_unit02_table()
    comparison = compare_tables(table, unit02_table)
    gates = gate_d(summary, primary, genes_ok, comparison)

    payload = {
        "run_date": date.today().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "census_version": CENSUS_VERSION,
        "kill_protocol_sha": KILL_SHA,
        "atlas_protocol_sha": ATLAS_SHA,
        "census_meta": census_meta,
        "blca_meta": blca_meta,
        "primary": primary,
        "summary": summary,
        "comparison": comparison,
        "gate_d": gates,
        "table": table.to_dict(orient="records"),
        "ici_files_opened": False,
    }
    JSON_OUT.write_text(json.dumps(payload, indent=2, default=str))
    RESEARCH.write_text(write_markdown(table, summary, census_meta, blca_meta, comparison, gates, unit02_source, primary))
    print(f"Wrote {RESEARCH}", flush=True)
    print(json.dumps({"summary": summary, "gate_d": gates, "comparison_counts": {
        "flips": len(comparison["flips"]),
        "n_cell_mismatches": comparison["n_cell_mismatches"],
        "n_published_drift_rows": comparison["n_published_drift_rows"],
        "max_mean_abs_diff": comparison["max_mean_abs_diff"],
    }}, indent=2, default=str), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
