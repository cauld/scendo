"""Locked gene lists from PROTOCOL.md. Do not add neighbors here."""

ECS = [
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
B_CELL = ["MS4A1", "CD19", "CD79A", "CD79B", "MZB1"]
TLS = ["CXCL13", "CCL19", "CCL21", "CCR7"]
CD8 = ["CD8A", "CD8B", "GZMB", "PRF1", "IFNG"]
CONTAM = ["MS4A1", "CD19", "CD79A"]

ALL_SCORE_GENES = ECS + B_CELL + TLS + CD8

# Protocol aliases plus common HGNC / literature names. Unit 00 records what
# each matrix actually uses.
ALIASES = {
    "CNR1": ["CB1", "CB-R", "CNR", "CANN6"],
    "CNR2": ["CB2", "CX5", "CB-2"],
    "GPR55": ["LPIR1"],
    "TRPV1": ["VR1"],
    "FAAH": ["FAAH1"],
    "MGLL": ["MAGL", "MGL", "HUK5", "HU-K5"],
    "DAGLA": ["DAGLALPHA", "DAGL-ALPHA", "DGL-ALPHA", "C11ORF11", "NOC2", "NSDDR"],
    "DAGLB": ["DAGLBETA", "DAGL-BETA", "DGL-BETA", "KCCR13L"],
    "NAPEPLD": ["NAPE-PLD", "NAPEPLD", "FMP30", "C7ORF9"],
}


def lookup_names(symbol: str) -> list[str]:
    names = [symbol, *ALIASES.get(symbol, [])]
    out: list[str] = []
    seen: set[str] = set()
    for name in names:
        key = name.upper()
        if key not in seen:
            seen.add(key)
            out.append(name)
    return out
