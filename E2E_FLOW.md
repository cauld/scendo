# End-to-end flow (this study)

Generic loop: [`.seal/E2E_FLOW.md`](.seal/E2E_FLOW.md).  
This page is the **SCENDO instantiation** (units, datasets, Decide branches).

Chat shorthand: **Explore → Question → Kill → Protocol → Clarify → Analyze → Seal (OSF) → Unit → Run → Converge → Decide → Archive.**

**You are here:** see `STATUS.md`. Kill protocol **sealed**. Kill test **done**. **Decision: atlas-only.** Atlas protocol **SEALED**. Units 10–11 **done**. Gate D **pass**. **Next:** **Run** (Unit 12, Gate E tables). OSF prereg for the kill SHA may follow by a day.

Lost on order? **[SEAL flow diagrams](docs/SEAL-FLOW.md)** — what to say, which unit is current.

---

## Specify (confirm)

| File | Job |
|---|---|
| `QUESTION.md` | One sentence |
| `CLAIMS.md` | What we may / may not say |
| `KILL.md` | Gates A/B/C |

---

## Plan then lock

| File | Job |
|---|---|
| `PROTOCOL.md` | CONFIRMATORY gene list, dataset roles, stats |
| `PHASES.md` | Checklist |
| `units/` | Operator packets |

**Clarify (atlas):** **done 2026-08-24** — five defaults accepted in [`PROTOCOL-ATLAS.md`](PROTOCOL-ATLAS.md). Kill Clarify is done.  
**External review:** [`PLAN.md`](PLAN.md) (kill, frozen) · [`PLAN-ATLAS.md`](PLAN-ATLAS.md) (atlas; `PROTOCOL-ATLAS.md` wins).  
**Lock (atlas):** **done 2026-08-24**. SHA in `STATUS.md`. Kill SHA `3fbf310` stays.

---

## Kill-test units

| Unit | Gate | Must not |
|---|---|---|
| 00 Inventory | — | Peek ICI labels for model shopping |
| 01 Detection | C | — |
| 02 scRNA states | A | Open ICI outcomes |
| 03 Freeze markers | A | Change gene list except amendment |
| 04 TCGA confound | A | — |
| 05 Name primary non-B state | wall | Open ICI outcomes before naming |
| 06 IMvigor210 | B | New ECS genes; optimize cutoff on AUC |
| 07 Melanoma GEO | replication | Rescue Gate B by hunting here |
| 08 Converge + Decide | — | Rewrite protocol to match figures |

---

## Decide

| Kill result | Next |
|---|---|
| A and B pass | Full paper; ICI analysis stays frozen |
| A pass, B fail | Atlas-only; ICI reported negative |
| A fail (B-cell proxy) | Stop or descriptive only; no checkpoint claim |
| A and B fail | Stop |

No browser, large-model training, or GSE220635 on this kill protocol. Atlas protocol (`PROTOCOL-ATLAS.md`) does not name them. GSE220635 stays a full-paper positive control unless an amendment names it.

---

## Atlas units (after atlas Seal)

| Unit | Gate | Must not |
|---|---|---|
| 10 Reproduce core | D | Rename Stromal/other; add genes |
| 11 Expansion inventory | E | Add types after seeing data |
| 12 Expansion states | E | New confirmatory states |
| 13 Stromal figures | — | UMAP / browser / clustering |
| 14 Converge atlas | F | Refit ICI |

Gate D **pass**. Unit 11 **done**. **Run** is next (Unit 12). Atlas protocol is sealed.
