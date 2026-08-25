#!/usr/bin/env python3
"""Unit 03 — freeze confirmatory markers. No DE. No ICI phenotype/outcome files."""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from detection_01 import CENSUS_VERSION  # noqa: E402
from genes import ALIASES, CONTAM, ECS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research" / "03-frozen-markers.json"
UNIT02 = ROOT / "research" / "02-scrna-states.md"
INVENTORY = ROOT / "research" / "data-inventory.md"
OUT_DIR = ROOT / "pipeline" / "output" / "03"

PROTOCOL_SHA = "3fbf310870c57247163edca35ed536ade3ea4301"
PROTOCOL_ECS = [
    "CNR1",
    "CNR2",
    "GPR55",
    "TRPV1",
    "FAAH",
    "MGLL",
    "DAGLA",
    "DAGLB",
    "NAPEPLD",
]
NEIGHBORS_NOT_IN_KILL = ["GPR18", "GPR119", "TRPV2", "ABHD6", "ABHD12"]
CONTAM_THRESHOLD_PCT = 10.0


def _md_tables(text: str) -> list[list[list[str]]]:
    tables: list[list[list[str]]] = []
    current: list[list[str]] | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            if current:
                tables.append(current)
                current = None
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and set(cells[0]) <= {"-", ":"}:
            continue
        if current is None:
            current = [cells]
        else:
            current.append(cells)
    if current:
        tables.append(current)
    return tables


def _table_by_header(tables: list[list[list[str]]], first: str, second: str) -> list[dict[str, str]]:
    for table in tables:
        header = table[0]
        if len(header) >= 2 and header[0] == first and header[1] == second:
            return [dict(zip(header, row, strict=False)) for row in table[1:]]
    raise SystemExit(f"Missing markdown table with headers {first!r}, {second!r}")


def _parse_pct(value: str) -> float | None:
    if not value or value in {"—", "-", "na", "NA"}:
        return None
    return float(value)


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"true", "yes"}


def _split_aliases(cell: str) -> tuple[list[str], list[str]]:
    text = cell.strip()
    if text in {"—", "-", ""}:
        return [], []
    proto: list[str] = []
    hgnc_part = text
    match = re.search(r";?\s*protocol:\s*", text, flags=re.I)
    if match:
        hgnc_part = text[: match.start()]
        proto = [a.strip() for a in text[match.end() :].split(",") if a.strip()]
    hgnc_part = hgnc_part.strip().lstrip("—–-").strip()
    hgnc = [a.strip() for a in hgnc_part.split(",") if a.strip() and a.strip() != "—"]
    return hgnc, proto


def parse_hgnc(inventory: str) -> dict[str, dict]:
    tables = _md_tables(inventory)
    rows = _table_by_header(tables, "Symbol", "Ensembl")
    out: dict[str, dict] = {}
    for row in rows:
        symbol = row["Symbol"].strip("`")
        if symbol not in ECS:
            continue
        hgnc_aliases, proto_from_cell = _split_aliases(row["HGNC aliases / previous"])
        protocol_aliases = list(dict.fromkeys([*ALIASES.get(symbol, []), *proto_from_cell]))
        used = [symbol, *hgnc_aliases, *protocol_aliases]
        seen: set[str] = set()
        aliases_used: list[str] = []
        for name in used:
            key = name.upper()
            if key not in seen:
                seen.add(key)
                aliases_used.append(name)
        out[symbol] = {
            "symbol": symbol,
            "ensembl": row["Ensembl"].strip("`"),
            "entrez": str(row["Entrez"]).strip(),
            "hgnc_aliases": hgnc_aliases,
            "protocol_aliases": protocol_aliases,
            "aliases_used": aliases_used,
            "matrix_symbol": symbol,
        }
    missing = [g for g in ECS if g not in out]
    if missing:
        raise SystemExit(f"Unit 00 HGNC table missing core genes: {missing}")
    return out


def parse_unit02(text: str) -> tuple[list[dict], list[dict], dict[str, str]]:
    tables = _md_tables(text)
    lineage_rows = _table_by_header(tables, "Type", "Source")
    candidate_rows = _table_by_header(tables, "Bucket", "Cancer types where kept")
    sources: dict[str, str] = {}
    lineage: list[dict] = []
    for row in lineage_rows:
        ctype = row["Type"]
        source = row["Source"]
        sources[ctype] = source
        discarded = _parse_bool(row["Discarded"].split("(")[0])
        lineage.append(
            {
                "cancer_type": ctype,
                "source": source,
                "bucket": row["Bucket"],
                "n_cells": int(row["n"]),
                "mean_ecs": None if row["Mean ECS"] in {"—", "-"} else float(row["Mean ECS"]),
                "rank": None if row["Rank"] in {"—", "-"} else int(row["Rank"]),
                "contam_gene": None if row["Contam gene"] in {"—", "-"} else row["Contam gene"],
                "contam_pct": _parse_pct(row["Contam %"]),
                "ecs_state_rule": _parse_bool(row["Rule"]),
                "discarded": discarded,
                "kept": _parse_bool(row["Kept"]),
            }
        )
    candidates = []
    for row in candidate_rows:
        types = [t.strip() for t in row["Cancer types where kept"].split(",") if t.strip()]
        candidates.append({"bucket": row["Bucket"], "cancer_types": types})
    return lineage, candidates, sources


def build() -> dict:
    if ECS != PROTOCOL_ECS:
        raise SystemExit(f"genes.ECS drifted from sealed protocol list: {ECS}")
    if not UNIT02.exists():
        raise SystemExit(f"Missing Unit 02 artifact: {UNIT02}")
    if not INVENTORY.exists():
        raise SystemExit(f"Missing Unit 00 artifact: {INVENTORY}")

    hgnc = parse_hgnc(INVENTORY.read_text())
    lineage, candidates, sources = parse_unit02(UNIT02.read_text())
    kept_buckets = [c["bucket"] for c in candidates]
    derived_kept = sorted({r["bucket"] for r in lineage if r["kept"]})
    listed_kept = sorted(kept_buckets)
    if derived_kept != listed_kept:
        raise SystemExit(f"Unit 02 kept buckets {derived_kept} != candidate list {listed_kept}")
    if len(ECS) != 9:
        raise SystemExit("marker gene list must be exactly the nine core genes")
    extra_de = []
    n_non_b = sum(1 for b in kept_buckets if b != "B/plasma")
    n_discarded = sum(1 for r in lineage if r["discarded"])
    census_contam = {r["contam_gene"] for r in lineage if r["source"] == "Census" and r["contam_gene"]}
    blca_contam = {
        r["contam_gene"] for r in lineage if "TISCH2" in r["source"] and r["contam_gene"]
    }
    cancer_types = []
    for ctype, source in sources.items():
        entry = {
            "cancer_type": ctype,
            "scrna_source": source,
            "census_version": CENSUS_VERSION if source == "Census" else None,
        }
        cancer_types.append(entry)

    payload = {
        "unit": "03",
        "title": "Frozen markers",
        "run_date": date.today().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "protocol_sha": PROTOCOL_SHA,
        "rule": (
            "Confirmatory marker object is the nine core ECS genes plus lineage "
            "buckets that have an ECS state after the Unit 02 contamination filter. "
            "No DE. Do not add or drop genes except by dated protocol amendment."
        ),
        "marker_list": {
            "genes": list(ECS),
            "lineages": kept_buckets,
        },
        "core_ecs_genes": list(ECS),
        "hgnc_aliases": hgnc,
        "lineage_buckets_with_ecs_state": candidates,
        "cancer_types": cancer_types,
        "contamination": {
            "fallback_order": list(CONTAM),
            "threshold_pct": CONTAM_THRESHOLD_PCT,
            "non_b_lineages_discarded": n_discarded,
            "gene_used_census": next(iter(census_contam), None),
            "gene_used_blca": next(iter(blca_contam), None),
            "rates": [
                {
                    "cancer_type": r["cancer_type"],
                    "source": r["source"],
                    "bucket": r["bucket"],
                    "n_cells": r["n_cells"],
                    "contam_gene": r["contam_gene"],
                    "contam_pct": r["contam_pct"],
                    "discarded": r["discarded"],
                    "kept": r["kept"],
                }
                for r in lineage
            ],
        },
        "gate_a_from_unit02": {
            "n_buckets_with_ecs_state": len(kept_buckets),
            "n_non_b": n_non_b,
            "two_lineage_rule": len(kept_buckets) >= 2,
            "has_non_b_candidate": n_non_b >= 1,
            "note": (
                "Unit 03 freezes markers only. Gate A still requires TCGA confound "
                "tests (Unit 04) and naming (Unit 05)."
            ),
        },
        "not_included": {
            "de_genes": extra_de,
            "neighbors_not_in_kill": NEIGHBORS_NOT_IN_KILL,
            "b_tls_cd8_signatures": "locked in PROTOCOL.md; not part of this marker object",
            "primary_state_named": False,
            "ici_files_opened": False,
        },
    }
    if payload["marker_list"]["genes"] != PROTOCOL_ECS:
        raise SystemExit("frozen gene list is not the sealed nine")
    if extra_de:
        raise SystemExit("DE genes are not allowed in the freeze")
    return payload


def main() -> int:
    payload = build()
    text = json.dumps(payload, indent=2) + "\n"
    RESEARCH.write_text(text)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "03-frozen-markers.json").write_text(text)
    print(f"Wrote {RESEARCH}", flush=True)
    print(json.dumps(payload["marker_list"], indent=2), flush=True)
    print(json.dumps(payload["gate_a_from_unit02"], indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
