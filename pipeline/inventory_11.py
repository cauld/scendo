#!/usr/bin/env python3
"""Unit 11 — expansion inventory (Gate E). Census only. No ICI files. No TISCH2."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from detection_01 import CENSUS_VERSION, census_obs_filter  # noqa: E402

KILL_SHA = "3fbf310870c57247163edca35ed536ade3ea4301"
ATLAS_SHA = "2a74270a16685cbc4df5c45c293a7afb5b7665f5"

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "pipeline" / "output" / "11"
RESEARCH = ROOT / "research" / "11-expansion-inventory.md"
RESEARCH_JSON = ROOT / "research" / "11-expansion-inventory.json"
JSON_OUT = OUT_DIR / "11-expansion-inventory.json"

N_MIN = 10_000
CULTURE = {"cell culture", "organoid", "cell line"}

# Locked list and order from PROTOCOL-ATLAS.md. Do not add, drop, or reorder types
# after seeing cell counts. First type wins if two needles hit the same label.
EXPANSION_TYPES = [
    "PAAD",
    "OV",
    "PRAD",
    "KIRC",
    "LIHC",
    "STAD",
    "ESCA",
    "HNSC",
    "GBM",
    "UCEC",
    "THCA",
    "CESC",
]

PROTOCOL_NAMES = {
    "PAAD": "pancreatic adenocarcinoma",
    "OV": "ovarian",
    "PRAD": "prostate",
    "KIRC": "clear cell kidney",
    "LIHC": "hepatocellular",
    "STAD": "stomach",
    "ESCA": "esophageal",
    "HNSC": "head and neck squamous",
    "GBM": "glioblastoma",
    "UCEC": "endometrial",
    "THCA": "thyroid",
    "CESC": "cervical",
}

# A priori needles (Unit 00 style: needle in disease.lower()). Parent / synonym
# strings from the protocol parentheticals plus standard TCGA names for that
# same type — not extra cancer types.
DISEASE_NEEDLES: dict[str, list[str]] = {
    "PAAD": [
        "pancreatic adenocarcinoma",
        "pancreatic ductal adenocarcinoma",
        "pancreatic cancer",
        "pancreas adenocarcinoma",
        "pancreas cancer",
    ],
    "OV": [
        "ovarian cancer",
        "ovarian carcinoma",
        "ovarian adenocarcinoma",
        "ovarian serous",
        "high-grade serous ovarian",
        "high grade serous ovarian",
        "high grade ovarian serous",
        "ovary adenocarcinoma",
        "ovary carcinoma",
        "ovary cancer",
        "ovarian epithelial",
        "epithelial ovarian",
    ],
    "PRAD": [
        "prostate adenocarcinoma",
        "prostate cancer",
        "prostate carcinoma",
        "prostatic adenocarcinoma",
        "prostatic cancer",
        "prostatic carcinoma",
    ],
    "KIRC": [
        "clear cell renal cell carcinoma",
        "clear cell renal carcinoma",
        "kidney clear cell carcinoma",
        "kidney renal clear cell",
        "clear cell kidney",
        "renal clear cell",
        "clear-cell renal",
    ],
    "LIHC": [
        "hepatocellular carcinoma",
        "hepatocellular cancer",
        "liver hepatocellular",
        "hepatocellular",
    ],
    "STAD": [
        "stomach adenocarcinoma",
        "gastric adenocarcinoma",
        "gastric cancer",
        "stomach cancer",
        "gastric carcinoma",
        "stomach carcinoma",
    ],
    "ESCA": [
        "esophageal adenocarcinoma",
        "esophageal squamous",
        "oesophageal",
        "esophageal carcinoma",
        "esophageal cancer",
        "esophagus adenocarcinoma",
        "esophagus squamous",
        "esophagus carcinoma",
        "esophagus cancer",
        "oesophagus",
    ],
    "HNSC": [
        "head and neck squamous",
        "head and neck squamous cell carcinoma",
        "oral squamous",
        "oral cavity squamous",
        "oropharyngeal squamous",
        "laryngeal squamous",
        "hypopharyngeal squamous",
        "tongue squamous",
        "tonsil squamous",
        "floor of mouth squamous",
        "buccal squamous",
        "gingival squamous",
        "lip squamous",
    ],
    "GBM": [
        "glioblastoma",
    ],
    "UCEC": [
        "endometrial carcinoma",
        "endometrial cancer",
        "endometrial adenocarcinoma",
        "uterine corpus endometrial",
        "endometrioid adenocarcinoma of the endometrium",
        "endometrioid endometrial",
        "endometrium carcinoma",
        "endometrium cancer",
        "endometrium adenocarcinoma",
    ],
    "THCA": [
        "thyroid carcinoma",
        "thyroid cancer",
        "thyroid adenocarcinoma",
        "papillary thyroid",
        "follicular thyroid carcinoma",
        "follicular thyroid cancer",
        "thyroid gland carcinoma",
        "thyroid gland cancer",
        "thyroid gland adenocarcinoma",
    ],
    "CESC": [
        "cervical cancer",
        "cervical carcinoma",
        "cervical squamous",
        "cervical adenocarcinoma",
        "cervix cancer",
        "cervix carcinoma",
        "cervix squamous",
        "cervix adenocarcinoma",
        "uterine cervix",
        "squamous cell carcinoma of the cervix",
        "adenocarcinoma of the cervix",
        "cervix uteri",
    ],
}

# Exact Census `disease` strings that are the locked type under a different
# MONDO label (catalog inspect, Unit 11 step 1). Not extra cancer types.
# Inspected and *not* added: malignant pancreatic neoplasm (parent, not
# adenocarcinoma); renal cell carcinoma / nonpapillary RCC / chromophobe
# (not specifically KIRC); liver cancer (not specifically LIHC);
# intrahepatic cholangiocarcinoma (not in the locked list).
CENSUS_EXACT: dict[str, list[str]] = {
    "PAAD": [],
    "OV": [],
    "PRAD": ["prostatic acinar adenocarcinoma"],
    "KIRC": [],
    "LIHC": [],
    "STAD": [],
    "ESCA": [],
    "HNSC": [
        "oropharynx squamous cell carcinoma",
        "tongue cancer",
    ],
    "GBM": [],
    "UCEC": [],
    "THCA": [],
    "CESC": [],
}

# Labels that match a needle are still dropped if they are not a tumor, or heme.
MALIGNANT_TOKENS = (
    "cancer",
    "carcinoma",
    "adenocarcinoma",
    "neoplasm",
    "tumor",
    "tumour",
    "glioblastoma",
    "sarcoma",
    "blastoma",
    "malignant",
    "malignancy",
    "cystadenocarcinoma",
)
EXCLUDE_TOKENS = (
    "normal",
    "healthy",
    "leukemia",
    "leukaemia",
    "lymphoma",
    "myeloma",
    "myelodysplastic",
    "uveal",
)
CORE_EXCLUDE_TOKENS = (
    "breast",
    "lung adenocarcinoma",
    "lung squamous",
    "non-small cell lung",
    "colorectal",
    "colon adenocarcinoma",
    "rectal adenocarcinoma",
    "melanoma",
    "bladder",
    "urothelial",
)


def _parts(disease: str) -> list[str]:
    return [p.strip().lower() for p in str(disease).split("||") if p.strip()]


def _is_malignant(text: str) -> bool:
    t = text.lower()
    return any(tok in t for tok in MALIGNANT_TOKENS)


def _excluded(text: str) -> bool:
    t = text.lower()
    if any(tok in t for tok in EXCLUDE_TOKENS):
        return True
    if any(tok in t for tok in CORE_EXCLUDE_TOKENS):
        return True
    return False


def disease_type(disease: str) -> str | None:
    """Map a Census disease string to one locked expansion type (or None)."""
    parts = _parts(disease)
    if not parts:
        return None
    joined = " || ".join(parts)
    if _excluded(joined) or not _is_malignant(joined):
        return None
    low_full = str(disease).strip().lower()
    for ctype in EXPANSION_TYPES:
        for exact in CENSUS_EXACT.get(ctype, []):
            if low_full == exact.lower():
                return ctype
        for part in parts:
            if _excluded(part):
                continue
            for needle in DISEASE_NEEDLES[ctype]:
                n = needle.lower()
                if "||" in n:
                    continue
                if n in part:
                    return ctype
    return None


def census_disease_labels(census) -> tuple[list[str], dict[str, int]]:
    summary = census["census_info"]["summary_cell_counts"].read().concat().to_pandas()
    if "organism" in summary.columns:
        summary = summary[summary["organism"].astype(str).str.contains("Homo", case=False, na=False)]
    if "category" not in summary.columns or "label" not in summary.columns:
        raise SystemExit("census_info.summary_cell_counts missing category/label")
    dis = summary[summary["category"].astype(str) == "disease"]
    ncol = "effective_unique_cell_count" if "effective_unique_cell_count" in dis.columns else None
    if ncol is None:
        for c in ("unique_cell_count", "cell_count", "count"):
            if c in dis.columns:
                ncol = c
                break
    counts: dict[str, int] = {}
    labels: set[str] = set()
    for _, row in dis.iterrows():
        if pd.isna(row["label"]):
            continue
        lab = str(row["label"])
        labels.add(lab)
        if ncol:
            counts[lab] = int(row[ncol])
    return sorted(labels), counts


def map_labels(labels: list[str], summary_counts: dict[str, int]) -> dict:
    mapped: dict[str, list[dict]] = {t: [] for t in EXPANSION_TYPES}
    unmatched_malignant: list[dict] = []
    for lab in labels:
        ctype = disease_type(lab)
        rec = {"disease": lab, "summary_cells": summary_counts.get(lab)}
        if ctype:
            mapped[ctype].append(rec)
        elif _is_malignant(lab) and not _excluded(lab):
            # Keep a short near-miss list for locked-type tokens only.
            low = lab.lower()
            watch = (
                "pancrea",
                "ovarian",
                "ovary",
                "prostate",
                "prostatic",
                "kidney",
                "renal",
                "hepat",
                "liver",
                "stomach",
                "gastric",
                "esophag",
                "oesophag",
                "head and neck",
                "oral",
                "oropharynx",
                "pharyn",
                "laryngeal",
                "tongue",
                "glioma",
                "glioblastoma",
                "endometr",
                "uterine",
                "thyroid",
                "cervi",
            )
            if any(w in low for w in watch):
                unmatched_malignant.append(rec)
    return {"mapped": mapped, "near_miss": unmatched_malignant}


def count_primary_cells(census, diseases: list[str]) -> pd.DataFrame:
    import cellxgene_census

    if not diseases:
        return pd.DataFrame(columns=["soma_joinid", "disease", "tissue_type", "cancer_type"])
    obs_filter = census_obs_filter(diseases)
    print(f"Census obs filter ({len(diseases)} disease labels) …", flush=True)
    obs = cellxgene_census.get_obs(
        census,
        "homo_sapiens",
        value_filter=obs_filter,
        column_names=["soma_joinid", "disease", "tissue_type"],
    )
    print(f"  obs n={len(obs):,} (is_primary_data == True)", flush=True)
    if "tissue_type" in obs.columns:
        tt = obs["tissue_type"].astype(str).str.lower()
        obs = obs.loc[~tt.isin(CULTURE)].copy()
        print(f"  after dropping culture/organoid/cell line: n={len(obs):,}", flush=True)
    obs["cancer_type"] = obs["disease"].astype(str).map(disease_type)
    obs = obs.loc[obs["cancer_type"].notna()].copy()
    print(obs["cancer_type"].value_counts().reindex(EXPANSION_TYPES).fillna(0).astype(int).to_string(), flush=True)
    return obs


def decide_rows(mapped: dict[str, list[dict]], n_by_type: dict[str, int], n_by_disease: dict[tuple[str, str], int]) -> list[dict]:
    rows = []
    for ctype in EXPANSION_TYPES:
        labels = mapped.get(ctype) or []
        strings = [h["disease"] for h in labels]
        n = int(n_by_type.get(ctype, 0))
        per_label = []
        for lab in strings:
            per_label.append({"disease": lab, "n_cells": int(n_by_disease.get((ctype, lab), 0))})
        if not strings:
            decision = "skip"
            reason = "missing in Census"
        elif n >= N_MIN:
            decision = "include"
            reason = f"n ≥ {N_MIN:,}"
        else:
            decision = "skip"
            reason = f"n < {N_MIN:,}"
        rows.append(
            {
                "cancer_type": ctype,
                "protocol_name": PROTOCOL_NAMES[ctype],
                "disease_strings": strings,
                "n_cells": n,
                "decision": decision,
                "reason": reason,
                "per_label": per_label,
            }
        )
    return rows


def write_markdown(payload: dict) -> str:
    rows = payload["types"]
    n_include = sum(1 for r in rows if r["decision"] == "include")
    n_skip = sum(1 for r in rows if r["decision"] == "skip")
    included = [r["cancer_type"] for r in rows if r["decision"] == "include"]
    skipped = [r["cancer_type"] for r in rows if r["decision"] == "skip"]

    def fmt_n(n: int) -> str:
        return f"{n:,}"

    def fmt_strings(strings: list[str]) -> str:
        if not strings:
            return "—"
        return "; ".join(strings)

    lines = [
        "# Unit 11 — Expansion inventory (Gate E)",
        "",
        f"**Run date:** {payload['run_date']}  ",
        f"**Census version:** `{payload['census_version']}`  ",
        f"**Kill protocol SHA:** `{payload['kill_sha']}`  ",
        f"**Atlas protocol SHA:** `{payload['atlas_sha']}`  ",
        "**Rule:** Census only. Map each locked expansion type to Census `disease` "
        "strings (Unit 00 style). Count cells after the Unit 01 filter "
        f"(`is_primary_data == True`; drop tissue_type in cell culture / organoid / "
        f"cell line). Include if n ≥ {N_MIN:,}; else skip (missing **or** n < "
        f"{N_MIN:,}). Do not substitute a type or a TISCH2 dataset. No ICI files.",
        "",
        "## Sources",
        "",
        f"- CELLxGENE Census pin `{payload['census_version']}`, human RNA, "
        "`is_primary_data == True`.",
        "- Locked types: `PROTOCOL-ATLAS.md` (PAAD, OV, PRAD, KIRC, LIHC, STAD, "
        "ESCA, HNSC, GBM, UCEC, THCA, CESC).",
        "- Disease mapping: a priori needles plus exact Census strings in "
        "`pipeline/inventory_11.py` (same substring style as Unit 00). "
        "First locked type wins on overlap.",
        "- Cell filter: same as Unit 01 (`census_obs_filter` + culture/organoid/"
        "cell-line drop). Summary-table n is recorded but does **not** decide include/skip.",
        "- Handoff: `research/11-expansion-inventory.json` (include list for Unit 12).",
        "",
        f"Types scored: **{len(rows)}** (no extras). Include: **{n_include}** "
        f"({', '.join(included) or 'none'}). Skip: **{n_skip}** "
        f"({', '.join(skipped) or 'none'}).",
        "",
        "## Inventory",
        "",
        "| Type | Protocol name | Census disease strings | n cells | Decision | Reason |",
        "|---|---|---|---:|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['cancer_type']} | {r['protocol_name']} | {fmt_strings(r['disease_strings'])} | "
            f"{fmt_n(r['n_cells'])} | **{r['decision']}** | {r['reason']} |"
        )

    lines += [
        "",
        "## Per-label n (after Unit 01 filter)",
        "",
        "| Type | Disease | n cells |",
        "|---|---|---:|",
    ]
    for r in rows:
        if not r["per_label"]:
            lines.append(f"| {r['cancer_type']} | — | 0 |")
            continue
        for lab in r["per_label"]:
            lines.append(f"| {r['cancer_type']} | {lab['disease']} | {fmt_n(lab['n_cells'])} |")

    lines += [
        "",
        "## Needles (a priori)",
        "",
        "Locked before seeing cell counts. Matching is case-insensitive substring "
        "on each `||`-delimited part of the Census `disease` field. Heme, normal/"
        "healthy, uveal, and the kill-test core five are excluded even if a needle hits.",
        "",
        "| Type | Needles |",
        "|---|---|",
    ]
    for ctype in EXPANSION_TYPES:
        needles = ", ".join(f"`{n}`" for n in DISEASE_NEEDLES[ctype])
        lines.append(f"| {ctype} | {needles} |")

    lines += [
        "",
        "## Census exact strings (same locked type)",
        "",
        "Recorded after inspecting Census `disease` labels. These are the locked "
        "type under a different MONDO string, not extra cancer types.",
        "",
        "| Type | Exact Census string |",
        "|---|---|",
    ]
    any_exact = False
    for ctype in EXPANSION_TYPES:
        for lab in CENSUS_EXACT.get(ctype, []):
            any_exact = True
            lines.append(f"| {ctype} | `{lab}` |")
    if not any_exact:
        lines.append("| — | none |")

    lines += [
        "",
        "Inspected and **not** mapped (would be a substitute type or a broader parent): "
        "`malignant pancreatic neoplasm` (not adenocarcinoma-specific); "
        "`renal cell carcinoma`, `nonpapillary renal cell carcinoma`, "
        "`chromophobe renal cell carcinoma` (not specifically KIRC); "
        "`liver cancer` (not specifically LIHC); "
        "`intrahepatic cholangiocarcinoma` (not in the locked list).",
        "",
    ]

    near = payload.get("near_miss") or []
    lines += [
        "",
        "## Near-miss labels (not used)",
        "",
        "Malignant Census `disease` labels that mention a locked-type token but did "
        "**not** map to a locked type. Listed so skips are not silent and so no extra "
        "type is added. These rows are **not** included.",
        "",
    ]
    if near:
        lines += [
            "| Disease | Summary n (not Unit 01 n) |",
            "|---|---:|",
        ]
        for rec in near:
            n = rec.get("summary_cells")
            ntxt = "—" if n is None else f"{int(n):,}"
            lines.append(f"| {rec['disease']} | {ntxt} |")
        lines.append("")
    else:
        lines.append("None.")
        lines.append("")

    lines += [
        "## Include list (Unit 12)",
        "",
    ]
    if included:
        lines.append(", ".join(f"`{t}`" for t in included) + ".")
        lines.append("")
        lines.append("Skipped types (one-line reason):")
        lines.append("")
        for r in rows:
            if r["decision"] == "skip":
                lines.append(f"- `{r['cancer_type']}`: {r['reason']}")
        lines.append("")
    else:
        lines.append("None. Every listed type is a documented skip.")
        lines.append("")

    extra = payload.get("n_extra_types", 0)
    lines += [
        "## Completeness draft (Gate E inventory half)",
        "",
        f"- Every locked type is include or skip: **{payload['complete']}**",
        f"- Extra types added: **{extra}**",
        f"- TISCH2 used: **False**",
        f"- ICI files opened: **False**",
        "",
        "Gate E is completed by Unit 12 (type × lineage tables for included types). "
        "This unit only records Census strings, n, and include vs skip.",
        "",
        "## What was not done",
        "",
        "- No TISCH2 (or other) substitution for skipped types.",
        "- No extra cancer type added.",
        "- No ECS scores, lineage tables, or contamination calls (Unit 12).",
        "- No ICI phenotype or outcome files opened.",
        "- No UMAP / browser / clustering / DE. No gene added.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    import cellxgene_census

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Census {CENSUS_VERSION} …", flush=True)
    with cellxgene_census.open_soma(census_version=CENSUS_VERSION) as census:
        labels, summary_counts = census_disease_labels(census)
        print(f"  disease labels: {len(labels)}", flush=True)
        mapped_pack = map_labels(labels, summary_counts)
        mapped = mapped_pack["mapped"]
        for ctype in EXPANSION_TYPES:
            hits = mapped[ctype]
            print(f"  {ctype}: {len(hits)} label(s)", flush=True)
            for h in hits:
                print(f"    - {h['disease']} (summary n={h['summary_cells']})", flush=True)

        all_diseases = []
        for hits in mapped.values():
            all_diseases.extend(h["disease"] for h in hits)
        all_diseases = list(dict.fromkeys(all_diseases))
        obs = count_primary_cells(census, all_diseases)

    n_by_type = obs.groupby("cancer_type").size().to_dict() if len(obs) else {}
    n_by_disease: dict[tuple[str, str], int] = {}
    if len(obs):
        g = obs.groupby(["cancer_type", "disease"]).size()
        n_by_disease = {(str(a), str(b)): int(c) for (a, b), c in g.items()}

    types = decide_rows(mapped, n_by_type, n_by_disease)
    payload = {
        "run_date": date.today().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "census_version": CENSUS_VERSION,
        "kill_sha": KILL_SHA,
        "atlas_sha": ATLAS_SHA,
        "n_min": N_MIN,
        "needles": DISEASE_NEEDLES,
        "census_exact": CENSUS_EXACT,
        "types": types,
        "include": [r["cancer_type"] for r in types if r["decision"] == "include"],
        "skip": [
            {"cancer_type": r["cancer_type"], "reason": r["reason"]}
            for r in types
            if r["decision"] == "skip"
        ],
        "near_miss": mapped_pack["near_miss"],
        "complete": len(types) == len(EXPANSION_TYPES)
        and {r["cancer_type"] for r in types} == set(EXPANSION_TYPES)
        and all(r["decision"] in {"include", "skip"} for r in types),
        "n_extra_types": 0,
        "n_obs_primary_mapped": int(len(obs)),
    }
    JSON_OUT.write_text(json.dumps(payload, indent=2, default=str))
    handoff = {
        "run_date": payload["run_date"],
        "census_version": payload["census_version"],
        "n_min": N_MIN,
        "include": payload["include"],
        "skip": payload["skip"],
        "types": [
            {
                "cancer_type": r["cancer_type"],
                "protocol_name": r["protocol_name"],
                "disease_strings": r["disease_strings"],
                "n_cells": r["n_cells"],
                "decision": r["decision"],
                "reason": r["reason"],
            }
            for r in types
        ],
    }
    RESEARCH_JSON.write_text(json.dumps(handoff, indent=2) + "\n")
    RESEARCH.write_text(write_markdown(payload))
    print(f"Wrote {RESEARCH}", flush=True)
    print(f"Wrote {RESEARCH_JSON}", flush=True)
    print(f"Wrote {JSON_OUT}", flush=True)
    print("Decisions:", flush=True)
    for r in types:
        print(f"  {r['cancer_type']}: {r['decision']} ({r['reason']}; n={r['n_cells']:,})", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
