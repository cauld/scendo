# KILL (atlas phase)

**Purpose.** Stop or shrink the atlas paper before a browser or a second ICI analysis. Human-owned pass/fail.

**Named confound (unchanged).** ECS scores can be a B-cell / TLS proxy. Gate A already passed. This phase does **not** re-test that confound and does **not** reopen Gate B.

The kill-test gates in [`KILL.md`](KILL.md) stay as marked: C pass / continue, A pass, B fail. Decide is **atlas-only**.

## Gate D — core map reproduces

**Data:** Same five types and pins as Units 01–02 (Census `2025-11-08`; BLCA TISCH2+GEO `GSE130001`).

**Pass if all hold:**

- Nine core genes unchanged.
- After the locked ECS-state + contamination rules, the buckets with an ECS state are still **B/plasma**, **Malignant/epithelial**, and **Stromal/other** (same three; no new confirmatory bucket; none of the three dropped).
- Primary name remains **Stromal/other**.

**Fail:** A kept bucket flips to dropped, a fourth bucket becomes a confirmatory state, genes are added, or the primary is renamed.

**If fail:** Stop the atlas paper or amend. Do not “fix” the catalog by changing the gene list after seeing expansion types.

## Gate E — expansion is pre-specified

**Data:** Locked expansion types in `PROTOCOL-ATLAS.md`, Census only.

**Pass if:** Every listed type has a complete type × lineage table **or** a documented skip (Census missing **or** n < 10,000 after the Unit 01 filter). No substitute types. No new TISCH2 shopping.

**Fail:** Types dropped without a reason, or a type added because it looked good. Promoting an expansion catalog row (including myeloid / T/NK) to a new confirmatory named state is also a fail.

**If fail:** Amend the list before claiming a “census-scale” map. The core five-type map may still be written if Gate D passed (narrower paper).

## Gate F — ICI stays frozen

**Pass if:** The manuscript ICI numbers match Units 06–07. No new ICI model, cutoff, gene, or cohort.

**Fail:** Any ICI fishing. That is a protocol violation, not a scientific rescue.

## Decide (atlas)

| Result | Decision |
|---|---|
| D pass, E pass, F pass | Atlas paper as written (core + expansion; ICI negative chapter) |
| D pass, E fail (skips or amend) | Narrower atlas (core five, maybe partial expansion); still ICI negative |
| D fail | Stop or amend; do not invent new states to save the paper |
| F fail | Do not ship; revert ICI chapter to Units 06–07 |

There is no path here to a full-paper Gate B pass.

## Explicitly not in this kill

Browser, scGPT, GSE220635, FAERS/DDI, wet lab, neighbor genes in the confirmatory score, new clustering.
