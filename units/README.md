# Units

A **unit** is BMAD’s story file without Agile: everything the Operator needs in one place. One unit, one run, one note.

Kill protocol is **locked**. Units 00–08 **done**. **Decision: atlas-only**. Atlas protocol is **locked** (`PROTOCOL-ATLAS.md`). Units 10–13 **done**. Gates D and E **pass**. Next: **Run** Unit 14. Diagrams: [`docs/SEAL-FLOW.md`](../docs/SEAL-FLOW.md).

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
| 10 | Reproduce core map | D | Atlas seal |
| 11 | Expansion inventory | E | 10 |
| 12 | Expansion ECS-state tables | E | 11 |
| 13 | Stromal composition + figures | — | 10, 12 |
| 14 | Converge atlas + frozen ICI | F | 12–13 |

Templates: study `_template.md` or [`.seal/templates/unit.md`](../.seal/templates/unit.md). After a run, fill **Notes**. Operator does not edit sealed `PROTOCOL.md` or, after atlas seal, `PROTOCOL-ATLAS.md` confirmatory fields.
