---
id: 06
role: Operator
status: done
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

- **2026-08-24 complete.** `research/06-imvigor210.md`. Runner: `uv run python pipeline/imvigor_06.py`. Primary **Stromal/other**. Freeze commit `21be9bd` before outcomes opened.
- Model 1 n=298 (68 CR/PR, 230 SD/PD). ECS OR 1.189 (0.551–2.563), CI includes 1. VIF(ECS)=1.360 (<3). Operator Gate B numbers **do not hold**. CD8 OR 2.380 (1.508–3.757) as expected; cannot pass Gate B.
- Unadjusted ECS OR 1.076 (0.568–2.038). Model 2 n=234 ECS OR 1.093 (0.449–2.663). Cox OS n=348 ECS HR 0.898 (0.623–1.294). No cutoff search. **2026-08-24 human Gate B: Fail.** **Next:** Unit 07 melanoma GEO (report only; cannot rescue).
