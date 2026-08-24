---
id: 06
role: Operator
status: ready_after_seal
reads:
  - PROTOCOL.md
  - KILL.md
  - research/05-primary-state.md
must_not:
  - Add ECS genes or search cutoffs
  - Treat OS, unadjusted, Model 2, or deconvolution as a Gate B pass
  - Peek outcomes before Unit 05 is committed
---

# Unit 06 — IMvigor210 confirmatory (Gate B)

**Goal.** Score the frozen primary state on IMvigor210. Fit Model 1. Report OS and Model 2 as secondary. Human marks Gate B.

**Inputs.** Pinned IMvigor210 extract from Unit 00. Frozen primary state from Unit 05. Outcome files may be opened **only after** Unit 05 is committed.

**Procedure.**

1. Score ECS, B, TLS, CD8 with available-case within-cohort z-score means. Drop samples below gene minima. Report n dropped.
2. Endpoint: CR/PR vs SD/PD; drop NE/NA.
3. Fit Model 1: `response ~ ECS_raw + B_cell + TLS + CD8` (logistic). Report OR and 95% CI.
4. Compute VIF for all four terms on the complete-case table. Do not drop terms.
5. Report unadjusted `response ~ ECS_raw`, Model 2 (+ TMB + PD-L1 IC if present), and Cox OS (secondary).
6. No median/Youden/AUC cutoff search.

**Outputs.** `research/06-imvigor210.md` (n, OR/CI, VIF, OS HR as secondary).

**Pass criteria (human):** Model 1 ECS CI excludes 1 **and** VIF(ECS) < 3. Otherwise Gate B fail. Secondary analyses cannot rescue.

## Notes (after run)

-
