---
id: 07
role: Operator
status: ready_after_seal
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

-
