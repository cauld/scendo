---
id: 08
role: Operator
status: done
reads:
  - PROTOCOL.md
  - KILL.md
  - CLAIMS.md
  - research/01-detection.md
  - research/04-tcga-confound.md
  - research/05-primary-state.md
  - research/06-imvigor210.md
  - research/07-melanoma-geo.md
must_not:
  - Rewrite confirmatory protocol fields to match figures
  - Promote OS / GEO / deconvolution to the confirmatory claim
---

# Unit 08 — Converge + Decide

**Goal.** Compare outputs to the sealed protocol. Draft gate scores. Human Decide.

**Procedure.**

1. Check that Units 01–07 followed locked gene lists, scoring math, and the outcome wall.
2. Draft Gate A/B/C calls against `KILL.md` (human marks pass/fail).
3. Map to Decide: A+B pass → full paper path; A pass B fail → atlas-only, ICI negative; A fail → stop or B-cell/ECS descriptive, no checkpoint claim.
4. Record deviations as exploratory in `EXPLORE.md` or a dated amendment. Do not silently edit `PROTOCOL.md`.

**Outputs.** Update `STATUS.md` with gate drafts and the human Decide.

**Pass criteria.** Human Decision recorded. Scribe stays inside `CLAIMS.md`.

## Human Decide (after Converge)

- [X] Atlas-only (mapped path; ICI chapter reported negative) — marked 2026-08-24
- [ ] Stop (no atlas paper)
- [ ] Full paper — **closed** unless a dated protocol amendment reopens Gate B

## Notes (after run)

- **2026-08-24 Converge complete.** `research/08-converge.md`. No pipeline runner. Protocol SHA `3fbf310` unchanged after seal. Outcome wall: `21be9bd` (Units 03–05 freeze) before `c1a47f9` (Units 06–07 ICI).
- Locked nine-gene list, B/TLS/CD8, available-case z-score math, and raw-score primary estimator held. No cutoff search. Neighbors not added. GEO / OS / Model 2 / deconvolution not used to rescue Gate B.
- Gate drafts match human marks: **C pass / continue**, **A pass**, **B fail**. Mapped Decide: **atlas-only; ICI reported negative**. Full paper closed unless a dated amendment.
- **2026-08-24 human Decide: atlas-only.** ICI chapter reported negative. Scribe ≤ `CLAIMS.md`. **Next:** Phase 2b atlas protocol (new lock; no ICI fishing).
