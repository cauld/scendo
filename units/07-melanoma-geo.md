---
id: 07
role: Operator
status: done
reads:
  - PROTOCOL.md
  - research/05-primary-state.md
  - research/06-imvigor210.md
must_not:
  - Rescue a failed Gate B by hunting cutoffs here
  - Change frozen genes or the primary-state name
---

# Unit 07 — Melanoma GEO replication (descriptive)

**Goal.** Score the same frozen objects on GSE78220 and GSE91061 (pre-treatment anti-PD-1). Report only. Underpowered; not the kill.

**Inputs.** Frozen primary state. GEO matrices pinned in Unit 00.

**Procedure.**

1. Same available-case scoring as Gate B.
2. Fit Model 1 covariates if available; otherwise report unadjusted association and available covariates.
3. Do not optimize cutoffs. Do not declare Gate B pass/fail from these sets.

**Outputs.** `research/07-melanoma-geo.md`

**Pass criteria.** Both datasets reported, or missingness recorded. No protocol change.

## Notes (after run)

- **2026-08-24 complete.** `research/07-melanoma-geo.md`. Runner: `uv run python pipeline/geo_07.py`. Same nine-gene **Stromal/other** score. No cutoff search. Does not rescue Gate B.
- GSE78220: dropped `Pt16.OnTx`; averaged Pt27A/B; n=26 (14 CR/PR, 12 PD). Model 1 ECS OR 0.469 (0.019–11.697). Unadjusted 1.108 (0.084–14.613).
- GSE91061: pre-treatment only; dropped 2 UNK; n=49 (10 PRCR, 39 SD/PD). Model 1 ECS OR 0.603 (0.066–5.510). Unadjusted 1.091 (0.163–7.310).
- **Next:** Unit 08 Converge + human Decide.
