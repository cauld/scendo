#!/usr/bin/env python3
"""Unit 00 — data access inventory.

Access + gene coverage only. Do not plot or summarize ICI outcomes vs ECS.
Phenotype files: record column / characteristic *names* only.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from genes import ALL_SCORE_GENES, ALIASES, B_CELL, CD8, CONTAM, ECS, TLS, lookup_names

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
OUT = ROOT / "research" / "data-inventory.md"
JSON_OUT = ROOT / "pipeline" / "output" / "00-inventory.json"

CANCER_TYPES = ["NSCLC", "melanoma", "CRC", "BRCA", "BLCA"]
TCGA_PROJECTS = ["LUAD", "LUSC", "SKCM", "COAD", "READ", "BRCA", "BLCA"]

CENSUS_DISEASE_MAP = {
    "NSCLC": [
        "lung adenocarcinoma",
        "lung squamous cell carcinoma",
        "non-small cell lung carcinoma",
        "squamous cell lung carcinoma",
        "non-small cell lung cancer",
    ],
    "melanoma": ["melanoma", "cutaneous melanoma"],
    "CRC": [
        "colorectal cancer",
        "colon adenocarcinoma",
        "rectal adenocarcinoma",
        "colorectal carcinoma",
        "colon cancer",
    ],
    "BRCA": [
        "breast cancer",
        "breast carcinoma",
        "invasive breast carcinoma",
        "breast invasive carcinoma",
    ],
    "BLCA": [
        "bladder carcinoma",
        "bladder cancer",
        "bladder urothelial carcinoma",
        "transitional cell carcinoma",
    ],
}

TISCH2_COUNTS_HOME = {
    "NSCLC": 17,
    "melanoma": 10,  # SKCM
    "CRC": 11,
    "BRCA": 12,
    "BLCA": 3,
}

HGNC_REST = "https://rest.genenames.org/fetch/symbol/{symbol}"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def match_symbol(index: set[str], symbol: str) -> tuple[bool, str | None]:
    """Return (present, matched_name) against an uppercase name set."""
    upper = {n.upper() for n in index}
    for name in lookup_names(symbol):
        if name.upper() in upper:
            return True, name
    # Ensembl-style suffix strip already done by caller for symbols.
    return False, None


def present_map(index: set[str], genes: list[str]) -> dict[str, str]:
    out = {}
    for g in genes:
        ok, matched = match_symbol(index, g)
        out[g] = matched if ok else "MISSING"
    return out


def coverage_line(mapping: dict[str, str]) -> str:
    missing = [g for g, v in mapping.items() if v == "MISSING"]
    n = len(mapping) - len(missing)
    extra = f"; missing: {', '.join(missing)}" if missing else ""
    return f"{n}/{len(mapping)} present{extra}"


def fetch_hgnc() -> dict[str, dict]:
    recs = {}
    headers = {"Accept": "application/json"}
    for symbol in ALL_SCORE_GENES:
        r = requests.get(HGNC_REST.format(symbol=symbol), headers=headers, timeout=30)
        r.raise_for_status()
        docs = r.json()["response"]["docs"]
        if not docs:
            recs[symbol] = {"status": "not found"}
            continue
        d = docs[0]
        recs[symbol] = {
            "hgnc_id": d.get("hgnc_id"),
            "ensembl_gene_id": d.get("ensembl_gene_id"),
            "entrez_id": d.get("entrez_id"),
            "alias_symbol": d.get("alias_symbol", []),
            "prev_symbol": d.get("prev_symbol", []),
        }
    return recs


def inventory_census() -> dict:
    import cellxgene_census

    pinned = cellxgene_census.get_census_version_description("stable")
    version = pinned.get("release_build") or pinned.get("census_version") or "stable"
    result = {
        "source": "CELLxGENE Census",
        "role": "primary scRNA (define states)",
        "api": "cellxgene-census Python",
        "package": "cellxgene-census",
        "license": "Per-dataset on CELLxGENE Discover (typically CC BY 4.0); Census access terms apply",
        "url": "https://chanzuckerberg.github.io/cellxgene-census/",
        "identifier": "feature_name (HGNC symbol) + feature_id (Ensembl)",
        "census_version_requested": "stable",
        "census_version": version,
        "release": {k: pinned[k] for k in pinned if k in {"release_date", "release_build", "lts"} or isinstance(pinned[k], (str, int, bool, type(None)))},
    }

    with cellxgene_census.open_soma(census_version="stable") as census:
        var = (
            census["census_data"]["homo_sapiens"]
            .ms["RNA"]
            .var.read(column_names=["feature_id", "feature_name"])
            .concat()
            .to_pandas()
        )
        names = set(var["feature_name"].astype(str))
        result["n_features"] = int(len(var))
        result["ecs"] = present_map(names, ECS)
        result["b_cell"] = present_map(names, B_CELL)
        result["tls"] = present_map(names, TLS)
        result["cd8"] = present_map(names, CD8)
        result["contam"] = present_map(names, CONTAM)
        result["contam_gene_used"] = next(
            (g for g in CONTAM if result["contam"][g] != "MISSING"),
            "NONE — discard all non-B lineages from Census datasets",
        )

        summary = (
            census["census_info"]["summary_cell_counts"]
            .read()
            .concat()
            .to_pandas()
        )
        # Human only; disease axis.
        if "organism" in summary.columns:
            summary = summary[summary["organism"].astype(str).str.contains("Homo", case=False, na=False)]
        diseases = []
        if "category" in summary.columns and "label" in summary.columns:
            dis = summary[summary["category"].astype(str) == "disease"]
            diseases = sorted({str(x) for x in dis["label"].dropna()})
            counts_by_label = {}
            ncol = "effective_unique_cell_count" if "effective_unique_cell_count" in dis.columns else None
            if ncol is None:
                for c in ("unique_cell_count", "cell_count", "count"):
                    if c in dis.columns:
                        ncol = c
                        break
            if ncol:
                counts_by_label = {
                    str(row["label"]): int(row[ncol])
                    for _, row in dis.iterrows()
                    if pd.notna(row["label"])
                }
        else:
            counts_by_label = {}
            if "disease" in summary.columns:
                diseases = sorted({str(x) for x in summary["disease"].dropna()})

        result["disease_labels_matching"] = {}
        types_present = []
        for ctype, needles in CENSUS_DISEASE_MAP.items():
            hits = []
            for d in diseases:
                dl = d.lower()
                if any(n in dl for n in needles):
                    n = counts_by_label.get(d)
                    hits.append({"disease": d, "cells": n})
            result["disease_labels_matching"][ctype] = hits
            if hits:
                types_present.append(ctype)
        result["cancer_types_present"] = types_present
        result["n_types"] = len(types_present)
        result["meets_two_type_minimum"] = len(types_present) >= 2

    return result


def inventory_tisch2() -> dict:
    # Home page (2026-08-24 fetch): BLCA 3, BRCA 12, CRC 11, NSCLC 17, SKCM 10.
    # Re-fetch to confirm reachability.
    url = "https://tisch.compbio.cn/home/"
    reachable = False
    status = None
    try:
        r = requests.get(url, timeout=40, headers={"User-Agent": "scendo-unit00/0.1"})
        status = r.status_code
        reachable = r.ok
    except requests.RequestException as e:
        status = str(e)
    return {
        "source": "TISCH2",
        "role": "fallback scRNA only if Census lacks a cancer type",
        "url": url,
        "gallery": "https://tisch.compbio.cn/gallery/",
        "license": "Academic / cite Sun et al. NAR 2021 and Han et al. NAR 2023; processed matrices under TISCH terms",
        "identifier": "HGNC symbols (MAESTRO-processed)",
        "reachable": reachable,
        "http_status": status,
        "cancer_types_present": {
            "NSCLC": {"tisch_code": "NSCLC", "n_datasets_home": TISCH2_COUNTS_HOME["NSCLC"]},
            "melanoma": {"tisch_code": "SKCM", "n_datasets_home": TISCH2_COUNTS_HOME["melanoma"]},
            "CRC": {"tisch_code": "CRC", "n_datasets_home": TISCH2_COUNTS_HOME["CRC"]},
            "BRCA": {"tisch_code": "BRCA", "n_datasets_home": TISCH2_COUNTS_HOME["BRCA"]},
            "BLCA": {"tisch_code": "BLCA", "n_datasets_home": TISCH2_COUNTS_HOME["BLCA"]},
        },
        "note": "All five kill-test types exist on TISCH2. Used only for a type Census lacks. Gene coverage of a TISCH2 matrix is recorded if/when a type falls back.",
        "ecs_matrix_checked": False,
        "contam_matrix_checked": False,
    }


TCGA_DISEASE = {
    "LUAD": "lung adenocarcinoma",
    "LUSC": "lung squamous cell carcinoma",
    "SKCM": "skin cutaneous melanoma",
    "COAD": "colon adenocarcinoma",
    "READ": "rectum adenocarcinoma",
    "BRCA": "breast invasive carcinoma",
    "BLCA": "bladder urothelial carcinoma",
}

GDC_CASE_COUNTS = {
    "LUAD": 585,
    "LUSC": 504,
    "SKCM": 470,
    "COAD": 461,
    "READ": 172,
    "BRCA": 1098,
    "BLCA": 412,
}


def inventory_tcga() -> dict:
    probe = DATA / "xena" / "gencode.v23.annotation.gene.probemap"
    pheno = DATA / "xena" / "TCGA_phenotype_denseDataOnlyDownload.tsv.gz"
    result = {
        "source": "TCGA via UCSC Xena TOIL + GDC project registry",
        "role": "bulk confound (Gate A)",
        "host": "https://toil.xenahubs.net",
        "dataset": "tcga_RSEM_gene_tpm",
        "dataset_url": "https://toil.xenahubs.net/download/tcga_RSEM_gene_tpm.gz",
        "unit": "log2(TPM + 0.001) (TOIL RSEM); not downloaded in Unit 00",
        "identifier": "Ensembl gene ID (probe) mapped to HGNC via gencode.v23 probeMap",
        "license": "TCGA / NIH Genomic Data Sharing; no attempt to re-identify",
        "probe_map": str(probe.relative_to(ROOT)) if probe.exists() else None,
        "phenotype": str(pheno.relative_to(ROOT)) if pheno.exists() else None,
        "phenotype_source": "https://pancanatlas.xenahubs.net/download/TCGA_phenotype_denseDataOnlyDownload.tsv.gz",
        "projects": TCGA_PROJECTS,
        "gdc_case_counts": GDC_CASE_COUNTS,
    }
    if not probe.exists():
        result["error"] = "probeMap missing"
        return result
    result["probe_map_sha256"] = sha256_file(probe)
    pm = pd.read_csv(probe, sep="\t")
    gene_col = "gene" if "gene" in pm.columns else pm.columns[1]
    id_col = "id" if "id" in pm.columns else pm.columns[0]
    symbols = set(pm[gene_col].astype(str))
    result["n_probe_rows"] = int(len(pm))
    result["ecs"] = present_map(symbols, ECS)
    result["b_cell"] = present_map(symbols, B_CELL)
    result["tls"] = present_map(symbols, TLS)
    result["cd8"] = present_map(symbols, CD8)
    result["ensembl"] = {}
    for g in ALL_SCORE_GENES:
        rows = pm[pm[gene_col].astype(str).str.upper() == g.upper()]
        result["ensembl"][g] = rows[id_col].astype(str).tolist() if len(rows) else []

    if pheno.exists():
        result["phenotype_sha256"] = sha256_file(pheno)
        ph = pd.read_csv(pheno, sep="\t", compression="gzip")
        result["phenotype_columns"] = list(ph.columns)
        project_counts = {}
        for proj, disease in TCGA_DISEASE.items():
            project_counts[proj] = int((ph["_primary_disease"] == disease).sum())
        result["n_samples_by_primary_disease"] = project_counts
        result["blca_available"] = project_counts.get("BLCA", 0) > 0
    return result


def _series_characteristic_keys(path: Path) -> list[str]:
    """Parse GEO series matrix for characteristic field names only (not values)."""
    keys: Counter[str] = Counter()
    opener = gzip.open if path.suffix == ".gz" or path.name.endswith(".gz") else open
    with opener(path, "rt", errors="replace") as f:
        for line in f:
            if line.startswith("!Sample_characteristics_ch"):
                # Values look like "response: R" — keep the key before the first colon.
                fields = line.rstrip("\n").split("\t")[1:]
                for field in fields:
                    field = field.strip().strip('"')
                    if ":" in field:
                        keys[field.split(":", 1)[0].strip().lower()] += 1
                    elif field:
                        keys[field.lower()] += 1
            if line.startswith("!series_matrix_table_begin"):
                break
    return sorted(keys)


def _gene_index_from_first_col(values, *, entrez: bool) -> set[str]:
    out = set()
    for g in values:
        g = str(g).strip()
        if "|" in g:
            g = g.split("|", 1)[0]
        if g.startswith("ENSG"):
            g = g.split(".")[0]
        out.add(g)
        if entrez:
            out.add(g.split(".")[0])
    return out


def _present_with_hgnc(index: set[str], genes: list[str], hgnc: dict) -> dict[str, str]:
    mapping = present_map(index, genes)
    for g, v in list(mapping.items()):
        if v != "MISSING":
            continue
        eid = str((hgnc.get(g) or {}).get("entrez_id") or "")
        if eid and eid in index:
            mapping[g] = f"Entrez:{eid}"
    return mapping


def inventory_geo(hgnc: dict) -> dict:
    gse78220_xlsx = DATA / "geo" / "GSE78220_PatientFPKM.xlsx"
    gse78220_series = DATA / "geo" / "GSE78220_series_matrix.txt.gz"
    gse91061_fpkm = DATA / "geo" / "GSE91061_BMS038109Sample.hg19KnownGene.fpkm.csv.gz"
    gse91061_series = DATA / "geo" / "GSE91061_series_matrix.txt.gz"

    def one(name, expr_path, series_path, id_system, license_note, entrez=False):
        rec = {
            "source": name,
            "role": "replication ICI (descriptive; not Gate B rescue)",
            "license": license_note,
            "expression_file": str(expr_path.relative_to(ROOT)) if expr_path.exists() else None,
            "series_matrix": str(series_path.relative_to(ROOT)) if series_path.exists() else None,
            "identifier": id_system,
        }
        if expr_path.exists():
            rec["expression_sha256"] = sha256_file(expr_path)
            rec["expression_bytes"] = expr_path.stat().st_size
            if expr_path.suffix == ".xlsx":
                df = pd.read_excel(expr_path, engine="openpyxl")
            else:
                df = pd.read_csv(expr_path, compression="gzip")
            index = _gene_index_from_first_col(df.iloc[:, 0], entrez=entrez)
            rec["n_rows"] = int(len(df))
            rec["n_sample_columns"] = int(df.shape[1] - 1)
            rec["first_column"] = str(df.columns[0])
            rec["ecs"] = _present_with_hgnc(index, ECS, hgnc)
            rec["b_cell"] = _present_with_hgnc(index, B_CELL, hgnc)
            rec["tls"] = _present_with_hgnc(index, TLS, hgnc)
            rec["cd8"] = _present_with_hgnc(index, CD8, hgnc)
        if series_path.exists():
            rec["series_sha256"] = sha256_file(series_path)
            rec["characteristic_field_names_only"] = _series_characteristic_keys(series_path)
        return rec

    return {
        "GSE78220": one(
            "GSE78220",
            gse78220_xlsx,
            gse78220_series,
            "HGNC symbols (PatientFPKM.xlsx Gene column)",
            "NCBI GEO public; Hugo et al. Cell 2016; original paper license",
        ),
        "GSE91061": one(
            "GSE91061",
            gse91061_fpkm,
            gse91061_series,
            "NCBI Entrez gene IDs (column 0 of hg19KnownGene FPKM)",
            "NCBI GEO public; Riaz et al. Cell 2017; original paper license",
            entrez=True,
        ),
    }


# From IMvigor210CoreBiologies R/data.R (package docs). Names only — values not opened.
IMVIGOR_PDATA_COLUMNS = [
    "ANONPT_ID",
    "Best Confirmed Overall Response",
    "binaryResponse",
    "IC Level",
    "os",
    "censOS",
    "Lund",
    "Lund2",
    "TCGA Subtype",
    "Enrollment IC",
    "Immune phenotype",
    "Sex",
    "Race",
    "Intravesical BCG administered",
    "Baseline ECOG Score",
    "Tobacco Use History",
    "Met Disease Status",
    "TC Level",
    "FMOne mutation burden per MB",
    "Sample age",
    "Tissue",
    "Received platinum",
    "Sample collected pre-platinum",
]


def _symbols_in_xz_rdata(path: Path, genes: list[str]) -> dict[str, str]:
    """Confirm HGNC symbols exist in an XZ-compressed RData feature table.

    Does not deserialize pData. Presence = ASCII symbol in the decompressed blob.
    """
    import lzma

    blob = lzma.decompress(path.read_bytes())
    out = {}
    for g in genes:
        out[g] = g if blob.find(g.encode("ascii")) >= 0 else "MISSING"
    return out


def inventory_imvigor() -> dict:
    tarball = DATA / "imvigor210" / "IMvigor210CoreBiologies_1.0.1.tar.gz"
    cds = DATA / "imvigor210" / "cds" / "cds.RData"
    rec = {
        "source": "IMvigor210CoreBiologies (Gene research-pub tarball)",
        "role": "primary ICI confirmatory (Gate B) — expression pin only in Unit 00",
        "license": "Package LICENSE (PDF in tarball); published as CC BY 3.0 (Gene / medRxiv data statement)",
        "citation": "Mariathasan et al. Nature 2018; http://research-pub.gene.com/IMvigor210CoreBiologies/",
        "identifier": "HGNC symbols in cds ExpressionSet fData (symbol field)",
        "pin": "IMvigor210CoreBiologies_1.0.1.tar.gz (Gene research-pub, not a GitHub mirror)",
        "url": "http://research-pub.gene.com/IMvigor210CoreBiologies/packageVersions/IMvigor210CoreBiologies_1.0.1.tar.gz",
        "package_version": "1.0.1",
        "outcome_rule": "Column names from R/data.R only. No response/OS values. No outcome-vs-ECS plots.",
        "phenotype_columns": IMVIGOR_PDATA_COLUMNS,
        "phenotype_columns_source": "IMvigor210CoreBiologies/R/data.R (docs for cds)",
    }
    if not tarball.exists() or tarball.stat().st_size < 1000:
        rec["error"] = "tarball missing"
        return rec
    rec["local_path"] = str(tarball.relative_to(ROOT))
    rec["bytes"] = tarball.stat().st_size
    rec["sha256"] = sha256_file(tarball)
    rec["package_file"] = tarball.name
    if cds.exists():
        rec["cds_path"] = str(cds.relative_to(ROOT))
        rec["cds_sha256"] = sha256_file(cds)
        rec["ecs"] = _symbols_in_xz_rdata(cds, ECS)
        rec["b_cell"] = _symbols_in_xz_rdata(cds, B_CELL)
        rec["tls"] = _symbols_in_xz_rdata(cds, TLS)
        rec["cd8"] = _symbols_in_xz_rdata(cds, CD8)
    else:
        rec["error"] = "cds.RData not extracted"
    return rec


def write_markdown(payload: dict) -> str:
    hgnc = payload["hgnc"]
    census = payload["census"]
    tisch = payload["tisch2"]
    tcga = payload["tcga"]
    geo = payload["geo"]
    imv = payload["imvigor"]

    def gene_table(mapping: dict[str, str]) -> str:
        rows = ["| Gene | In matrix |", "|---|---|"]
        for g, v in mapping.items():
            rows.append(f"| `{g}` | {v} |")
        return "\n".join(rows)

    def block(title: str, mapping: dict[str, str] | None) -> str:
        if not mapping:
            return f"**{title}:** not checked (file missing or unreadable).\n"
        return f"**{title}** ({coverage_line(mapping)})\n\n{gene_table(mapping)}\n"

    lines = [
        "# Data inventory",
        "",
        f"**Unit:** 00  ",
        f"**Run date:** {payload['run_date']}  ",
        f"**Protocol SHA (STATUS):** `{payload['protocol_sha']}`  ",
        "**Rule:** access + gene coverage only. No ICI outcome-vs-ECS plots or summaries. Phenotype recorded as column names only.",
        "",
        "## Pass / fail",
        "",
        f"- Primary sources reachable: **{payload['pass']['sources_reachable']}**",
        f"- IMvigor210 core ECS missing ≤ 2: **{payload['pass']['imvigor_ecs_ok']}** ({payload['pass']['imvigor_ecs_missing']} missing)",
        f"- Census cancer types ≥ 2 of 5: **{payload['pass']['census_types_ok']}** ({payload['pass']['census_types']})",
        f"- scRNA contamination gene available (Census): **{payload['pass']['census_contam']}**",
        f"- TCGA-BLCA phenotype rows present: **{payload['pass']['tcga_blca']}**",
        "",
        "## HGNC aliases (Unit 00 record)",
        "",
        "Locked symbols stay as in `PROTOCOL.md`. Aliases below are for matrix matching only.",
        "",
        "| Symbol | Ensembl | Entrez | HGNC aliases / previous |",
        "|---|---|---|---|",
    ]
    for g in ECS + B_CELL + TLS + CD8:
        rec = hgnc.get(g, {})
        aliases = rec.get("alias_symbol") or []
        prev = rec.get("prev_symbol") or []
        extra = ", ".join([*aliases, *prev]) if (aliases or prev) else "—"
        # also protocol aliases if HGNC omitted them
        proto = [a for a in ALIASES.get(g, []) if a.upper() not in {x.upper() for x in [*aliases, *prev]}]
        if proto:
            extra = extra + ("; protocol: " + ", ".join(proto) if extra != "—" else "protocol: " + ", ".join(proto))
        lines.append(
            f"| `{g}` | `{rec.get('ensembl_gene_id', '')}` | {rec.get('entrez_id', '')} | {extra} |"
        )

    lines += [
        "",
        "## 1. CELLxGENE Census (primary scRNA)",
        "",
        f"- **API:** `{census.get('package')}` via `uv` group `census`",
        f"- **Pinned version:** `{census.get('census_version')}` (requested `stable`)",
        f"- **License:** {census.get('license')}",
        f"- **Gene IDs:** {census.get('identifier')}",
        f"- **Features:** {census.get('n_features')}",
        f"- **Local path:** remote SOMA (not downloaded as h5ad)",
        f"- **Cancer types present:** {', '.join(census.get('cancer_types_present', [])) or 'none'}",
        "",
    ]
    for ctype, hits in (census.get("disease_labels_matching") or {}).items():
        if hits:
            bits = ", ".join(f"{h['disease']} (n={h['cells']})" for h in hits)
            lines.append(f"- {ctype}: {bits}")
        else:
            lines.append(f"- {ctype}: **not found** in Census disease labels (TISCH2 fallback eligible)")
    lines += [
        "",
        block("ECS", census.get("ecs")),
        block("B cell", census.get("b_cell")),
        block("TLS", census.get("tls")),
        block("CD8", census.get("cd8")),
        block("Contamination screen genes", census.get("contam")),
        f"Contamination gene for Census (first present of MS4A1 → CD19 → CD79A): **{census.get('contam_gene_used')}**",
        "",
        "## 2. TISCH2 (fallback only)",
        "",
        f"- **URL:** {tisch.get('url')}  ",
        f"- **Reachable:** {tisch.get('reachable')} (HTTP {tisch.get('http_status')})",
        f"- **License:** {tisch.get('license')}",
        f"- **Gene IDs:** {tisch.get('identifier')}",
        f"- **Local path:** none (catalog check only; no matrix downloaded)",
        "",
        "| Kill type | TISCH2 code | Datasets on home page |",
        "|---|---|---|",
    ]
    for ctype, rec in tisch.get("cancer_types_present", {}).items():
        lines.append(f"| {ctype} | {rec['tisch_code']} | {rec['n_datasets_home']} |")
    lines += [
        "",
        tisch.get("note", ""),
        "",
        "## 3. TCGA (UCSC Xena TOIL)",
        "",
        f"- **Host:** {tcga.get('host')}",
        f"- **Pinned dataset:** `{tcga.get('dataset')}` — {tcga.get('unit')}",
        f"- **Full matrix URL (not downloaded in Unit 00):** {tcga.get('dataset_url')}",
        f"- **License:** {tcga.get('license')}",
        f"- **Gene IDs:** {tcga.get('identifier')}",
        f"- **probeMap:** `{tcga.get('probe_map')}` SHA256 `{tcga.get('probe_map_sha256', '')}`",
        f"- **Phenotype file:** `{tcga.get('phenotype')}` (cancer-type labels only; no ICI outcomes)",
        "",
        "Sample rows mentioning each project (phenotype file; not an expression n):",
        "",
        "| Project | Xena phenotype rows | GDC cases |",
        "|---|---|---|",
    ]
    for proj, n in (tcga.get("n_samples_by_primary_disease") or {}).items():
        gdc = (tcga.get("gdc_case_counts") or {}).get(proj, "")
        lines.append(f"| {proj} | {n} | {gdc} |")
    lines += [
        "",
        f"TCGA-BLCA available for Gate A: **{tcga.get('blca_available')}**",
        "",
        block("ECS", tcga.get("ecs")),
        block("B cell", tcga.get("b_cell")),
        block("TLS", tcga.get("tls")),
        block("CD8", tcga.get("cd8")),
        "",
        "## 4. IMvigor210 (primary ICI) — pin only",
        "",
        f"- **Pin:** {imv.get('package_file') or imv.get('pin')}",
        f"- **Local path:** `{imv.get('local_path')}`",
        f"- **SHA256:** `{imv.get('sha256', '')}`",
        f"- **Bytes:** {imv.get('bytes')}",
        f"- **License:** {imv.get('license')}",
        f"- **Citation:** {imv.get('citation')}",
        f"- **Gene IDs:** {imv.get('identifier')}",
        "",
        "**Must not (this unit):** open response/OS values for model shopping; plot response vs ECS / CNR2 / B-cell scores.",
        "",
    ]
    if imv.get("error"):
        lines.append(f"- **Error:** {imv['error']}")
    if imv.get("phenotype_columns"):
        lines.append("Phenotype / pData **column names only**:")
        lines.append("")
        for c in imv["phenotype_columns"]:
            lines.append(f"- `{c}`")
        lines.append("")
        lines.append(f"n phenotype rows (count only): {imv.get('n_phenotype_rows')}")
        lines.append("")
    else:
        lines.append("Phenotype column names: not extracted (see tarball pin; export after Unit 05).")
        lines.append("")
    lines += [
        block("ECS", imv.get("ecs")),
        block("B cell", imv.get("b_cell")),
        block("TLS", imv.get("tls")),
        block("CD8", imv.get("cd8")),
        "",
        "## 5. Melanoma GEO (replication)",
        "",
    ]
    for acc, rec in geo.items():
        lines += [
            f"### {acc}",
            "",
            f"- **Role:** {rec.get('role')}",
            f"- **License:** {rec.get('license')}",
            f"- **Expression:** `{rec.get('expression_file')}` SHA256 `{rec.get('expression_sha256', '')}`",
            f"- **Series matrix:** `{rec.get('series_matrix')}`",
            f"- **Gene IDs:** {rec.get('identifier')}",
            f"- **Matrix shape:** {rec.get('n_rows')} genes × {rec.get('n_sample_columns')} samples",
            "",
        ]
        if rec.get("characteristic_field_names_only"):
            lines.append("Series-matrix characteristic **field names only** (no values):")
            lines.append("")
            for k in rec["characteristic_field_names_only"]:
                lines.append(f"- `{k}`")
            lines.append("")
        lines += [
            block("ECS", rec.get("ecs")),
            block("B cell", rec.get("b_cell")),
            block("TLS", rec.get("tls")),
            block("CD8", rec.get("cd8")),
        ]

    lines += [
        "",
        "## Environment",
        "",
        f"- Python: {payload['python']}",
        f"- uv lock present: {payload['uv_lock']}",
        f"- Packages: {payload['packages']}",
        "",
        "## What was not done",
        "",
        "- No ECS / CNR2 / B-cell scores computed.",
        "- No response or OS value tabulation, plots, or models.",
        "- IMvigor210 and GEO phenotype **values** were not written out.",
        "- Full TCGA expression matrix not downloaded (Unit 04).",
        "- Census counts not sliced to anndata (Unit 01).",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    sys.path.insert(0, str(Path(__file__).parent))
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)

    protocol_sha = "3fbf310870c57247163edca35ed536ade3ea4301"
    payload: dict = {
        "run_date": date.today().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "protocol_sha": protocol_sha,
        "python": sys.version.split()[0],
        "uv_lock": (ROOT / "uv.lock").exists(),
        "packages": {},
    }
    try:
        import importlib.metadata as md

        for pkg in ["pandas", "pyarrow", "requests", "openpyxl", "rdata", "cellxgene-census"]:
            try:
                payload["packages"][pkg] = md.version(pkg)
            except md.PackageNotFoundError:
                payload["packages"][pkg] = None
    except Exception:
        pass

    errors = []
    print("HGNC …", flush=True)
    try:
        payload["hgnc"] = fetch_hgnc()
    except Exception as e:
        errors.append(f"HGNC: {e}")
        payload["hgnc"] = {}

    print("Census …", flush=True)
    try:
        payload["census"] = inventory_census()
    except Exception as e:
        errors.append(f"Census: {e}")
        payload["census"] = {"error": str(e)}

    print("TISCH2 …", flush=True)
    try:
        payload["tisch2"] = inventory_tisch2()
    except Exception as e:
        errors.append(f"TISCH2: {e}")
        payload["tisch2"] = {"error": str(e)}

    print("TCGA / Xena …", flush=True)
    try:
        payload["tcga"] = inventory_tcga()
    except Exception as e:
        errors.append(f"TCGA: {e}")
        payload["tcga"] = {"error": str(e)}

    print("GEO …", flush=True)
    try:
        payload["geo"] = inventory_geo(payload.get("hgnc") or {})
    except Exception as e:
        errors.append(f"GEO: {e}")
        payload["geo"] = {"error": str(e)}

    print("IMvigor210 …", flush=True)
    try:
        payload["imvigor"] = inventory_imvigor()
    except Exception as e:
        errors.append(f"IMvigor: {e}")
        payload["imvigor"] = {"error": str(e)}

    def missing_count(mapping):
        if not mapping:
            return None
        return sum(1 for v in mapping.values() if v == "MISSING")

    imv_miss = missing_count(payload.get("imvigor", {}).get("ecs"))
    census_types = payload.get("census", {}).get("cancer_types_present", [])
    payload["pass"] = {
        "sources_reachable": all(
            [
                "error" not in payload.get("census", {}) or "census_version" in payload.get("census", {}),
                payload.get("tisch2", {}).get("reachable"),
                payload.get("tcga", {}).get("ecs"),
                payload.get("imvigor", {}).get("sha256"),
                payload.get("geo", {}).get("GSE78220", {}).get("ecs")
                or payload.get("geo", {}).get("GSE78220", {}).get("expression_file"),
                payload.get("geo", {}).get("GSE91061", {}).get("expression_file"),
            ]
        ),
        "imvigor_ecs_missing": imv_miss,
        "imvigor_ecs_ok": imv_miss is not None and imv_miss <= 2,
        "census_types": census_types,
        "census_types_ok": len(census_types) >= 2,
        "census_contam": payload.get("census", {}).get("contam_gene_used"),
        "tcga_blca": payload.get("tcga", {}).get("blca_available"),
    }
    payload["errors"] = errors

    JSON_OUT.write_text(json.dumps(payload, indent=2, default=str))
    OUT.write_text(write_markdown(payload))
    print(f"Wrote {OUT}", flush=True)
    print(f"Wrote {JSON_OUT}", flush=True)
    if errors:
        print("Errors:", *errors, sep="\n- ", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
