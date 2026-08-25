# Units

A **unit** is BMAD’s story file without Agile: everything the Operator needs in one place. One unit, one run, one note.

Protocol is **locked**. Units 00–08 **done**. **Decision: atlas-only** (ICI negative). Next: Phase 2b atlas protocol (new lock). Diagrams: [`docs/SEAL-FLOW.md`](../docs/SEAL-FLOW.md).

| ID | Title | Gate | Depends on |
|---|---|---|---|
| 00 | Data access inventory | — | After Seal; before 01–08 |
| 01 | Detection rates (Census; TISCH2 fallback) | C | 00, Seal |
| 02 | scRNA ECS states | A | 01 |
| 03 | Freeze markers (nine genes + lineage) | A | 02 |
| 04 | TCGA confound | A | 03 |
| 05 | Name primary non-B state | A→B wall | 04, **before ICI outcomes** |
| 06 | IMvigor210 confirmatory | B | 05 |
| 07 | Melanoma replication | B (weak) | 06 |
| 08 | Converge + Decide | — | 06–07 |

Templates: study `_template.md` or [`.seal/templates/unit.md`](../.seal/templates/unit.md). After a run, fill **Notes**. Operator does not edit `PROTOCOL.md`.
