# SCENDO

**SCENDO** = **S**ingle-**C**ell **ENDO**cannabinoidome (host tissues and tumor microenvironment).

Computational study. Public data only. No wet lab in v1.  
Reusable flow: [`.seal/E2E_FLOW.md`](.seal/E2E_FLOW.md). This folder is the study instance.

Read: [`PLAN.md`](PLAN.md) (external review brief) → [`docs/SEAL-FLOW.md`](docs/SEAL-FLOW.md) (order + what to run) → [`E2E_FLOW.md`](E2E_FLOW.md) → `STATUS.md` → `QUESTION.md` → `CLAIMS.md` → `KILL.md` → `PROTOCOL.md` → `PHASES.md` → `units/`.

Study text in this repository is [CC BY 4.0](LICENSE). Third-party datasets stay under their original licenses. Pipeline code, when added, can take MIT without changing this.

## Setup

Python env and deps are managed with [uv](https://docs.astral.sh/uv/). Python **3.12** (Census wheels; 3.14 is too new).

```bash
uv sync
uv run python pipeline/inventory_00.py
```

`.venv/` is local and gitignored. `uv.lock` is the pinned resolver output.
