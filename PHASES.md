# PHASES

Generic loop: [`.seal/E2E_FLOW.md`](.seal/E2E_FLOW.md). Study instantiation: [`E2E_FLOW.md`](E2E_FLOW.md). This file is the checklist.

## Phase 0 — Spec (done)

| Step | Workflow | Output |
|---|---|---|
| 0.1 | Question | `QUESTION.md`, `CLAIMS.md` |
| 0.2 | Kill | `KILL.md` |
| 0.3 | Protocol | `PROTOCOL.md` |
| 0.4 | Clarify | **Done 2026-08-24**; **patched** same day after validation (see `PROTOCOL.md` amendments) |
| 0.5 | Analyze | **Pass 2026-08-24** — note in `STATUS.md` |
| 0.5b | Unit 00 inventory | Access + gene coverage; **no ICI peek**; run blocker for Units 01–08 |
| 0.6 | **Seal** (human) | **Done 2026-08-24** — git SHA in `STATUS.md` (OSF may follow) |

**Exit:** Kill protocol sealed. Agent will not edit CONFIRMATORY sections.

## Phase 1 — Kill test (~10 days, laptop)

Units in `units/` (Operator). Order is dependency order.

1. Census/TISCH2 detection (Gate C) — Unit 00 already ran before Seal  
2. scRNA ECS states (Gate A, no ICI)  
3. Freeze marker lists → commit  
4. TCGA B-cell/TLS confound  
5. **Stop if Gate A fail**  
6. Name primary non-B state (if any) **before** ICI outcomes  
7. IMvigor210 Gate B  
8. Melanoma replication (descriptive)  
9. Converge + Decide — **Done 2026-08-24.** Decision: **atlas-only**

**Exit:** **atlas-only** (A pass, B fail). ICI reported negative. Full paper closed.

## Phase 2a — Stop

Write a short kill note. Do not build a browser.

## Phase 2b — Atlas-only (complete)

Chosen 2026-08-24. Atlas lock **sealed**:

| Step | Workflow | Output |
|---|---|---|
| Protocol | **Sealed 2026-08-24** | `PROTOCOL-ATLAS.md`, `KILL-ATLAS.md`, `PLAN-ATLAS.md` |
| Clarify | **Done 2026-08-24** | Five defaults accepted (see `PROTOCOL-ATLAS.md` amendments) |
| Analyze | **Pass 2026-08-24** | Note in `STATUS.md` |
| Seal | **Done 2026-08-24** | Git SHA in `STATUS.md` (kill SHA `3fbf310` unchanged) |
| Units 10–14 | After Seal | Units 10–14 **done**; Gates D, E, F **pass** |
| Decide | **Done 2026-08-25** | Atlas paper as written (core + expansion; ICI negative chapter) |
| Scribe | **Done 2026-08-25** | [`RESULTS.md`](RESULTS.md) · [`docs/manuscript.md`](docs/manuscript.md); bound held |
| Archive | **Done 2026-08-25** | [`EXPLORE.md`](EXPLORE.md); confirmatory loop closed |

**Must not:** reopen Gate B; add confirmatory ECS genes; browser / scGPT / GSE220635 unless a later amendment names them.

**Exit:** **Taken 2026-08-25.** Atlas paper as written. Scribe complete. Archive complete. OSF prereg may still go up.

## Phase 2c — Full paper (if A and B pass)

Broader atlas, GSE220635 as reconciliation, manuscript. ICI confirmatory analysis stays as already run.

## Deferred (not this study)

Oncology DDI / FAERS / CYP. Wet-lab CB2. Prospective cannabis+ICI cohort.
