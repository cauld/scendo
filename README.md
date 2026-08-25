# SCENDO

**SCENDO** = **S**ingle-**C**ell **ENDO**cannabinoidome.

Public-data computational study. No wet lab. Atlas paper: named ECS **lineage cell states** plus a **frozen negative** IMvigor210 response test after B-cell / TLS / CD8 adjustment.

| Read first | What it is |
|---|---|
| [`docs/manuscript.md`](docs/manuscript.md) | Paper draft |
| [`RESULTS.md`](RESULTS.md) | Confirmatory numbers |
| [`CLAIMS.md`](CLAIMS.md) | What we may / may not say |
| [`STATUS.md`](STATUS.md) | You are here; freeze SHAs |
| [`EXPLORE.md`](EXPLORE.md) | Not confirmatory (archived leftovers) |
| [`research/osf-secondary-prereg.md`](research/osf-secondary-prereg.md) | OSF paste packet |

Kill protocol freeze: git `3fbf310` (2026-08-24). Atlas protocol freeze: git `2a74270`. ICI chapter is Gate B **fail** (Model 1 n=298, ECS OR 1.189, 95% CI 0.551–2.563).

Study text is [CC BY 4.0](LICENSE). Third-party datasets stay under their original licenses.

## Reproduce

Python **3.12**, [uv](https://docs.astral.sh/uv/):

```bash
uv sync
uv run python pipeline/inventory_00.py
```

Unit runners are `pipeline/*.py`. Pins and checksums: [`research/data-inventory.md`](research/data-inventory.md). Raw matrices live under `data/` (gitignored).

Process kernel: [`.seal/E2E_FLOW.md`](.seal/E2E_FLOW.md). This folder is the study instance.
