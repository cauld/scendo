---
id: 14
role: Operator
status: done
reads:
  - PROTOCOL-ATLAS.md
  - KILL-ATLAS.md
  - CLAIMS.md
  - research/06-imvigor210.md
  - research/07-melanoma-geo.md
  - research/10-reproduce-core.md
  - research/12-expansion-states.md
must_not:
  - Refit ICI models or add ICI cohorts
  - Rewrite kill confirmatory fields
  - Promote OS / GEO / deconvolution / expansion states to a checkpoint claim
---

# Unit 14 — Converge atlas + frozen ICI chapter (Gate F)

**Goal.** Check the atlas outputs against `PROTOCOL-ATLAS.md`. Confirm the ICI chapter is Units 06–07 unchanged.

**Procedure.**

1. Gate D/E drafts vs `KILL-ATLAS.md`.
2. Confirm nine genes, primary name, no UMAP/browser, no TISCH2 shopping, no extra types.
3. Gate F: ICI numbers in the paper packet equal `research/06-imvigor210.md` and `research/07-melanoma-geo.md`. If matrices were re-read, the reproduction must match; any other model is a fail.
4. Scribe bound: `CLAIMS.md` non-claims plus `PROTOCOL-ATLAS.md` paper claim (ICI chapter is the frozen **negative**). Do not upgrade CLAIMS item 3’s either/or into a new ICI-positive finding.

**Outputs.** `research/14-atlas-converge.md` and `STATUS.md` gate drafts.

**Pass criteria (human):** Gates D/E/F marked. Then human Decide whether to write the atlas manuscript (Scribe).

## Human Gate F (after Converge)

- [X] Pass (ICI numbers = Units 06–07; no new ICI analysis) — marked 2026-08-25
- [ ] Fail (any ICI fishing)

## Human Decide (atlas)

- [X] Atlas paper as written (core + expansion; ICI negative chapter) — mapped path (D/E/F pass) — marked 2026-08-25
- [ ] Stop (no atlas paper)
- [ ] Narrower atlas — **closed** (Gate E passed)
- [ ] Full paper — **closed** unless a dated kill-protocol amendment reopens Gate B

## Notes (after run)

- **2026-08-25 Converge complete.** `research/14-atlas-converge.md`. No pipeline runner. Atlas SHA `2a74270` and kill SHA `3fbf310` unchanged after seal. ICI last written in `c1a47f9` (Units 06–07); atlas commits add Units 10–13 only.
- Nine genes, primary **Stromal/other**, no UMAP/browser, no TISCH2 shopping, no extra types. Myeloid / T/NK stay catalog-only. Stromal subtypes stay display-only.
- Gate drafts: **D pass** (human 2026-08-24), **E pass** (human 2026-08-25), **F pass** (human 2026-08-25). IMvigor210 n=298 ECS OR 1.189 (0.551–2.563) VIF=1.360; GEO citation only; no refit. **2026-08-25 human Decide: atlas paper as written** (core + expansion; ICI negative chapter). **Scribe complete:** `RESULTS.md` · `docs/manuscript.md`.
