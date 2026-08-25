"""Locked lineage buckets from PROTOCOL.md. First substring match wins."""

from __future__ import annotations

BUCKET_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("B/plasma", ("b cell", "b-cell", "plasma", "plasmablast", "plasmacyte")),
    (
        "Myeloid",
        (
            "monocyte",
            "macrophage",
            "myeloid",
            "dendritic",
            "neutrophil",
            "mast",
            "granulocyte",
            "kupffer",
        ),
    ),
    (
        "T/NK",
        (
            "t cell",
            "t-cell",
            "cd4",
            "cd8",
            "treg",
            "nk cell",
            "natural killer",
            "ilc",
            "nkt",
            "gamma-delta",
            "gd t",
            "thymocyte",
        ),
    ),
    (
        "Malignant/epithelial",
        (
            "malignant",
            "tumor cell",
            "cancer cell",
            "epithelial",
            "keratinocyte",
            "pneumocyte",
            "enterocyte",
            "hepatocyte",
            "urothelial",
        ),
    ),
    (
        "Stromal/other",
        (
            "fibroblast",
            "endothelial",
            "pericyte",
            "smooth muscle",
            "myofibroblast",
            "stroma",
        ),
    ),
]

# Protocol example: TISCH2 Tprolif → T/NK when the parent lineage is in the label.
_SPECIAL = (
    ("T/NK", ("tprolif", "t-prolif", "t prolif")),
    ("B/plasma", ("bprolif", "b-prolif")),
    ("Myeloid", ("myeloid prolif", "mprolif")),
)


def assign_bucket(label: str) -> str:
    text = str(label).strip().lower()
    if not text or text in {"nan", "none", "na"}:
        return "Stromal/other"
    for bucket, needles in BUCKET_RULES:
        for needle in needles:
            if needle in text:
                return bucket
    for bucket, needles in _SPECIAL:
        for needle in needles:
            if needle in text:
                return bucket
    return "Stromal/other"
