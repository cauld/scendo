# End-to-end flow (this study)

Generic loop: [`.seal/E2E_FLOW.md`](.seal/E2E_FLOW.md).  
This page is the **SCENDO instantiation** (units, datasets, Decide branches).

Chat shorthand: **Explore → Question → Kill → Protocol → Clarify → Analyze → Seal (OSF) → Unit → Run → Converge → Decide → Archive.**

**You are here:** see `STATUS.md`. Protocol **sealed**. Units 00–07 **done**. Primary **Stromal/other**. Gate A **pass**. Gate B **fail**. GEO replication reported (cannot rescue). **Next:** Unit 08 Converge, then human Decide. OSF prereg may follow the git SHA by a day.

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

**Clarify:** lock the **rule** for naming the primary non-B state (Unit 05, after Gate A, **before** IMvigor210 outcomes). The name itself is not known at seal.  
**External review:** [`PLAN.md`](PLAN.md) (this is a readable copy of the protocol; `PROTOCOL.md` wins if they disagree).  
**Lock:** commit those files; SHA in `STATUS.md`; OSF secondary-data prereg. No ICI outcome-vs-ECS analysis until then.

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

No browser, large-model training, or GSE220635 until Decide (GSE220635 is post-Decide positive control).
