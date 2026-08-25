#!/usr/bin/env python3
"""Unit 05 — name the primary non-B state. No ICI phenotype/outcome files. No Gate B."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from freeze_03 import UNIT02, _md_tables, _table_by_header, parse_unit02  # noqa: E402
from genes import CONTAM, ECS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "research" / "03-frozen-markers.json"
UNIT04 = ROOT / "research" / "04-tcga-confound.md"
RESEARCH = ROOT / "research" / "05-primary-state.md"
OUT_DIR = ROOT / "pipeline" / "output" / "05"
JSON_OUT = OUT_DIR / "05-primary-state.json"

PROTOCOL_SHA = "3fbf310870c57247163edca35ed536ade3ea4301"
FIVE_TYPES = ("BLCA", "BRCA", "CRC", "NSCLC", "melanoma")
PRIORITY = {
    "Myeloid": 0,
    "T/NK": 1,
    "Malignant/epithelial": 2,
    "Stromal/other": 3,
}
ASCII_NAME = {
    "Malignant/epithelial": "malignant/epithelial",
    "Myeloid": "myeloid",
    "Stromal/other": "stromal/other",
    "T/NK": "t/nk",
}
CASCADE = [
    ("1", "lowest max(|r_B|, |r_TLS|) on pooled raw Pearson", "max_abs_r_pooled", "min"),
    ("2", "present (ECS-state rule) in more of the five cancer types", "n_types", "max"),
    ("3", "myeloid > T/NK > malignant/epithelial > stromal/other", "priority", "min"),
    ("4", "higher mean core-ECS across types where the bucket has an ECS state", "mean_core_ecs", "max"),
    ("5", "larger total cell n in those types", "n_cells", "max"),
    ("6", "earlier ASCII bucket name", "ascii", "min"),
]


def _parse_optional_float(value: str) -> float | None:
    text = (value or "").strip()
    if text in {"", "—", "-", "na", "NA", "None"}:
        return None
    return float(text)


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"true", "yes"}


def _fmt_r(v) -> str:
    return "—" if v is None else f"{v:.4f}"


def _fmt_mean(v) -> str:
    return "—" if v is None else f"{v:.4f}"


def load_frozen() -> dict:
    if not FROZEN.exists():
        raise SystemExit(f"Missing Unit 03 freeze: {FROZEN}")
    frozen = json.loads(FROZEN.read_text())
    genes = frozen["marker_list"]["genes"]
    if genes != ECS:
        raise SystemExit(f"Frozen genes drifted from protocol: {genes}")
    return frozen


def parse_unit04(text: str) -> dict[str, dict]:
    tables = _md_tables(text)
    rows = _table_by_header(tables, "Candidate", "r_B_pooled")
    out: dict[str, dict] = {}
    for row in rows:
        name = row["Candidate"]
        out[name] = {
            "r_B_pooled": _parse_optional_float(row["r_B_pooled"]),
            "r_TLS_pooled": _parse_optional_float(row["r_TLS_pooled"]),
            "r_B_BLCA": _parse_optional_float(row["r_B_BLCA"]),
            "r_TLS_BLCA": _parse_optional_float(row["r_TLS_BLCA"]),
            "residual_ratio_pooled": _parse_optional_float(row["Residual ratio pooled"]),
            "residual_ratio_BLCA": _parse_optional_float(row["Residual ratio BLCA"]),
            "qualifies": _parse_bool(row["Qualifies"]),
        }
    if not out:
        raise SystemExit("Unit 04 per-candidate table is empty")
    return out


def _best_key(values: list, direction: str):
    return min(values) if direction == "min" else max(values)


def apply_cascade(records: list[dict]) -> tuple[dict | None, str, list[dict]]:
    if not records:
        return None, "no qualifying non-B candidate", []
    if len(records) == 1:
        winner = records[0]
        return winner, "single qualifier (cascade not required)", []

    remaining = list(records)
    walk: list[dict] = []
    for step_id, label, field, direction in CASCADE:
        keys = [c[field] for c in remaining]
        best = _best_key(keys, direction)
        kept = [c for c in remaining if c[field] == best]
        walk.append(
            {
                "step": step_id,
                "rule": label,
                "field": field,
                "direction": direction,
                "best": best,
                "n_before": len(remaining),
                "n_after": len(kept),
                "remaining": [c["bucket"] for c in kept],
            }
        )
        remaining = kept
        if len(remaining) == 1:
            return remaining[0], f"step {step_id}: {label}", walk
    remaining.sort(key=lambda c: c["ascii"])
    return remaining[0], "step 6: earlier ASCII bucket name", walk


def build_records(
    frozen: dict,
    lineage_rows: list[dict],
    confound: dict[str, dict],
) -> list[dict]:
    kept = {c["bucket"]: c["cancer_types"] for c in frozen["lineage_buckets_with_ecs_state"]}
    records = []
    for bucket, types in kept.items():
        if bucket == "B/plasma":
            continue
        if bucket not in confound:
            raise SystemExit(f"Unit 04 missing candidate {bucket}")
        row = confound[bucket]
        means = []
        n_cells = 0
        type_rows = []
        for r in lineage_rows:
            if r["bucket"] != bucket or not r["kept"]:
                continue
            if r["mean_ecs"] is None:
                raise SystemExit(f"Missing mean ECS for kept {bucket} in {r['cancer_type']}")
            means.append(r["mean_ecs"])
            n_cells += r["n_cells"]
            type_rows.append(
                {
                    "cancer_type": r["cancer_type"],
                    "n_cells": r["n_cells"],
                    "mean_ecs": r["mean_ecs"],
                }
            )
        derived_types = [t["cancer_type"] for t in type_rows]
        if sorted(derived_types) != sorted(types):
            raise SystemExit(f"{bucket} types {derived_types} != freeze {types}")
        r_b = row["r_B_pooled"]
        r_tls = row["r_TLS_pooled"]
        if r_b is None or r_tls is None:
            raise SystemExit(f"Missing pooled Pearson for {bucket}")
        records.append(
            {
                "bucket": bucket,
                "cancer_types": types,
                "n_types": len(types),
                "type_rows": type_rows,
                "mean_core_ecs": sum(means) / len(means) if means else None,
                "n_cells": n_cells,
                "priority": PRIORITY[bucket],
                "ascii": ASCII_NAME[bucket],
                "r_B_pooled": r_b,
                "r_TLS_pooled": r_tls,
                "r_B_BLCA": row["r_B_BLCA"],
                "r_TLS_BLCA": row["r_TLS_BLCA"],
                "max_abs_r_pooled": max(abs(r_b), abs(r_tls)),
                "residual_ratio_pooled": row["residual_ratio_pooled"],
                "residual_ratio_BLCA": row["residual_ratio_BLCA"],
                "qualifies": row["qualifies"],
            }
        )
    return records


def write_markdown(
    frozen: dict,
    records: list[dict],
    winner: dict | None,
    deciding_step: str,
    walk: list[dict],
    two_lineage: bool,
) -> str:
    qualifiers = [r for r in records if r["qualifies"]]
    gate_a_numbers = two_lineage and winner is not None
    genes = ", ".join(f"`{g}`" for g in ECS)
    contam = frozen["contamination"]
    lines = [
        "# Unit 05 — Primary non-B state (A→B wall)",
        "",
        f"**Run date:** {date.today().isoformat()}  ",
        f"**Protocol SHA:** `{PROTOCOL_SHA}`  ",
        "**Inputs:** `research/02-scrna-states.md`, `research/03-frozen-markers.json`, "
        "`research/04-tcga-confound.md`  ",
        "**Rule:** Name the primary after Gate A numbers exist and **before** any IMvigor210 "
        "or GEO phenotype/outcome file is opened. Gate A needs both (i) ≥2 lineage buckets "
        "with an ECS state and (ii) ≥1 non-B candidate that passed confound tests. If several "
        "non-B buckets qualify, apply the locked cascade (no judgment). Subtypes within a "
        "bucket are not separate states. Gate B always uses the raw nine-gene score.",
        "",
        "## Gate A both-parts (operator; human marks below)",
        "",
        f"- Lineage buckets with an ECS state: **{len(frozen['marker_list']['lineages'])}** "
        f"({', '.join(frozen['marker_list']['lineages'])})",
        f"- Two-lineage rule (≥2 buckets, including B/plasma): **{two_lineage}**",
        f"- Non-B candidates: **{', '.join(r['bucket'] for r in records) or 'none'}**",
        f"- Non-B candidates that qualify on confound tests: "
        f"**{', '.join(r['bucket'] for r in qualifiers) or 'none'}** "
        f"(n={len(qualifiers)})",
        f"- Residual escape used: **False** (both Pearson tests passed |r| < 0.6)",
        f"- Operator Gate A numbers hold: **{gate_a_numbers}**",
        "",
    ]
    if not two_lineage:
        lines += [
            "Gate A **fails** (fewer than two lineage buckets). Do not open ICI outcomes "
            "for a checkpoint test.",
            "",
        ]
    elif winner is None:
        lines += [
            "Gate A **fails** (no non-B candidate qualifies). Do not open ICI outcomes "
            "for a checkpoint test.",
            "",
        ]

    lines += [
        "## Cascade (qualifying non-B buckets only)",
        "",
        "1. Lowest `max(|r_B|, |r_TLS|)` using Pearson on **pooled raw** scores.",
        "2. Tie: present (ECS-state rule) in more of the five cancer types.",
        "3. Tie: myeloid > T/NK > malignant/epithelial > stromal/other.",
        "4. Tie: higher mean core-ECS (mean of that bucket’s lineage-mean core-ECS across "
        "types where it has an ECS state).",
        "5. Tie: larger total cell count *n* in those types for that bucket.",
        "6. Tie: earlier bucket name in ASCII sort of "
        "`{malignant/epithelial, myeloid, stromal/other, t/nk}`.",
        "",
        "Bulk TCGA scores the same nine-gene mean for every non-B candidate, so step 1 "
        "is a tie whenever more than one bucket qualifies. They still compete as separate "
        "lineage buckets.",
        "",
        "| Candidate | Qualifies | r_B_pooled | r_TLS_pooled | max\\|r\\| pooled | r_B_BLCA | r_TLS_BLCA | Residual pooled | Residual BLCA | n types | Types | Mean core-ECS | Cell n | Priority | ASCII |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---|",
    ]
    for r in records:
        lines.append(
            f"| {r['bucket']} | {r['qualifies']} | {_fmt_r(r['r_B_pooled'])} | "
            f"{_fmt_r(r['r_TLS_pooled'])} | {_fmt_r(r['max_abs_r_pooled'])} | "
            f"{_fmt_r(r['r_B_BLCA'])} | {_fmt_r(r['r_TLS_BLCA'])} | "
            f"{_fmt_r(r['residual_ratio_pooled'])} | {_fmt_r(r['residual_ratio_BLCA'])} | "
            f"{r['n_types']} | {', '.join(r['cancer_types'])} | {_fmt_mean(r['mean_core_ecs'])} | "
            f"{r['n_cells']} | {r['priority']} | `{r['ascii']}` |"
        )

    lines += ["", "### Per-type core-ECS (types where the bucket has an ECS state)", ""]
    for r in records:
        lines.append(f"**{r['bucket']}**")
        lines.append("")
        lines.append("| Type | n cells | Mean core-ECS |")
        lines.append("|---|---:|---:|")
        for t in r["type_rows"]:
            lines.append(f"| {t['cancer_type']} | {t['n_cells']} | {_fmt_mean(t['mean_ecs'])} |")
        lines.append("")

    if walk:
        lines += ["### Walk", ""]
        for step in walk:
            best = step["best"]
            if isinstance(best, float):
                best_s = f"{best:.4f}"
            else:
                best_s = str(best)
            lines.append(
                f"- Step {step['step']} ({step['rule']}): {step['n_before']} → "
                f"{step['n_after']} remaining ({', '.join(step['remaining'])}); "
                f"best {step['field']} = {best_s}."
            )
            if step["n_after"] == 1:
                lines.append(f"  **Stopped here.**")
                break
        lines.append("")

    lines += [
        f"**Deciding step:** {deciding_step}",
        "",
    ]

    if winner is None:
        lines += [
            "## Primary state",
            "",
            "**None.** Gate A fail. Do not run Gate B as a checkpoint test.",
            "",
        ]
    else:
        lines += [
            "## Primary state (frozen for Gate B)",
            "",
            f"- **Name:** {winner['bucket']}",
            f"- **Lineage bucket:** {winner['bucket']}",
            f"- **Nine genes:** {genes}",
            f"- **r_B_pooled:** {_fmt_r(winner['r_B_pooled'])}",
            f"- **r_TLS_pooled:** {_fmt_r(winner['r_TLS_pooled'])}",
            f"- **r_B_BLCA:** {_fmt_r(winner['r_B_BLCA'])}",
            f"- **r_TLS_BLCA:** {_fmt_r(winner['r_TLS_BLCA'])}",
            f"- **Residual SD/raw SD pooled:** {_fmt_r(winner['residual_ratio_pooled'])} (not used)",
            f"- **Residual SD/raw SD BLCA:** {_fmt_r(winner['residual_ratio_BLCA'])} (not used)",
            f"- **Cancer types with an ECS state:** {', '.join(winner['cancer_types'])} "
            f"({winner['n_types']} of {len(FIVE_TYPES)})",
            f"- **Mean core-ECS (across those types):** {_fmt_mean(winner['mean_core_ecs'])}",
            f"- **Total cell n (those types):** {winner['n_cells']}",
            f"- **Tie-breaker that decided the primary:** {deciding_step}",
            "",
            "Secondary non-B states may be scored later; they cannot pass Gate B.",
            "",
        ]

    rates = contam["rates"]
    lines += [
        "## Contamination",
        "",
        f"- Fallback order: {' → '.join(f'`{g}`' for g in CONTAM)}",
        f"- Threshold: {contam['threshold_pct']:.0f}% detection in a non-B lineage (that type)",
        f"- Gene used (Census): **{contam['gene_used_census']}**",
        f"- Gene used (BLCA / TISCH2): **{contam['gene_used_blca']}**",
        f"- Non-B lineages discarded: **{contam['non_b_lineages_discarded']}**",
        "",
        "| Type | Source | Bucket | n cells | Contam gene | Contam % | Discarded | Kept |",
        "|---|---|---|---:|---|---:|---|---|",
    ]
    for r in rates:
        pct = "—" if r["contam_pct"] is None else f"{r['contam_pct']:.2f}"
        lines.append(
            f"| {r['cancer_type']} | {r['source']} | {r['bucket']} | {r['n_cells']} | "
            f"{r['contam_gene'] or '—'} | {pct} | {r['discarded']} | {r['kept']} |"
        )

    lines += [
        "",
        "## Human Gate A",
        "",
        "- [ ] Pass (two lineages + at least one qualifying non-B state named above)",
        "- [ ] Fail — do not open ICI outcomes for a checkpoint test",
        "",
        "## What was not done",
        "",
        "- No IMvigor210 or GEO phenotype/outcome files opened.",
        "- No Gate B. No cutoff search. No DE / extra ECS genes.",
        "- Frozen Unit 03 marker object not edited.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    if not UNIT02.exists():
        raise SystemExit(f"Missing Unit 02 artifact: {UNIT02}")
    if not UNIT04.exists():
        raise SystemExit(f"Missing Unit 04 artifact: {UNIT04}")

    frozen = load_frozen()
    lineage_rows, _candidates, _sources = parse_unit02(UNIT02.read_text())
    confound = parse_unit04(UNIT04.read_text())
    records = build_records(frozen, lineage_rows, confound)
    two_lineage = len(frozen["marker_list"]["lineages"]) >= 2
    qualifiers = [r for r in records if r["qualifies"]]
    winner, deciding_step, walk = apply_cascade(qualifiers)
    if not two_lineage:
        winner = None
        deciding_step = "Gate A fail: fewer than two lineage buckets"
        walk = []

    RESEARCH.write_text(write_markdown(frozen, records, winner, deciding_step, walk, two_lineage))
    payload = {
        "unit": "05",
        "title": "Primary non-B state",
        "run_date": date.today().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "protocol_sha": PROTOCOL_SHA,
        "two_lineage_rule": two_lineage,
        "candidates": records,
        "qualifiers": [r["bucket"] for r in qualifiers],
        "cascade_walk": walk,
        "deciding_step": deciding_step,
        "primary": None
        if winner is None
        else {
            "name": winner["bucket"],
            "lineage_bucket": winner["bucket"],
            "genes": list(ECS),
            "r_B_pooled": winner["r_B_pooled"],
            "r_TLS_pooled": winner["r_TLS_pooled"],
            "r_B_BLCA": winner["r_B_BLCA"],
            "r_TLS_BLCA": winner["r_TLS_BLCA"],
            "residual_ratio_pooled": winner["residual_ratio_pooled"],
            "residual_ratio_BLCA": winner["residual_ratio_BLCA"],
            "cancer_types": winner["cancer_types"],
            "mean_core_ecs": winner["mean_core_ecs"],
            "n_cells": winner["n_cells"],
            "deciding_step": deciding_step,
        },
        "gate_a_numbers_hold": bool(two_lineage and winner is not None),
        "ici_files_opened": False,
        "gate_b_run": False,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {RESEARCH}", flush=True)
    print(json.dumps(payload["primary"], indent=2), flush=True)
    print(json.dumps({"deciding_step": deciding_step, "gate_a_numbers_hold": payload["gate_a_numbers_hold"]}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
