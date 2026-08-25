---
id: 05
role: Operator
status: done
reads:
  - PROTOCOL.md
  - KILL.md
  - research/02-scrna-states.md
  - research/04-tcga-confound.md
must_not:
  - Open any IMvigor210 or GEO phenotype/outcome file
  - Run Gate B
---

# Unit 05 — Name primary non-B state (A→B wall)

**Goal.** Apply the locked naming rule. Commit the primary state **before** ICI outcomes are opened. Human marks Gate A.

**Inputs.** Units 02–04 outputs only.

**Procedure.**

1. Confirm Gate A both-parts: ≥2 lineage buckets with an ECS state **and** ≥1 non-B candidate that passed confound tests (including residual cap if used).
2. If several non-B **buckets** qualify, apply the locked cascade (no judgment): lowest `max(|r_B|, |r_TLS|)` on pooled **raw** Pearson; then more of the five cancer types; then myeloid > T/NK > malignant/epithelial > stromal/other; then higher mean core-ECS; then larger cell *n*; then ASCII bucket name. Subtypes within a bucket are not separate states.
3. Commit name, lineage, nine genes, four Pearson values, residual ratios if used, contamination gene per dataset, contamination rates, and which cascade step broke a tie.
4. If no non-B candidate qualifies: Gate A fails. **Do not** open ICI outcomes for a checkpoint test.

**Outputs.** `research/05-primary-state.md` + git commit of that file.

**Pass criteria.** Primary name is in git **or** Gate A fail is recorded. No ICI files have been opened.

## Notes (after run)

- **2026-08-24 complete.** `research/05-primary-state.md`. Runner: `uv run python pipeline/name_05.py`. Primary **Stromal/other**. Cascade step 1 tied (same pooled |r|); step 2 broke it (5 types vs 4). No ICI files. No Gate B.
- Gate A operator numbers hold: 3 buckets (B/plasma + two non-B); both non-B qualify (pooled r_B=0.4173 r_TLS=0.3835; BLCA r_B=0.3605 r_TLS=0.2628; residual not used). Contamination gene **MS4A1** on Census and BLCA; 0 non-B discards.
- **2026-08-24 human Gate A:** Pass. `research/05-primary-state.md`. **Next:** commit that file, then Unit 06 IMvigor210.
