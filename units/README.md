# Units

A **unit** is BMAD’s story file without Agile: everything the Operator needs in one place. One unit, one run, one note.

Do not start Units 01–08 until the protocol is **locked** (see `E2E_FLOW.md` stage 3). **Unit 00** runs **before** Seal (access + gene coverage only; no ICI outcome peek).

| ID | Title | Gate | Depends on |
|---|---|---|---|
| 00 | Data access inventory | — | Before Seal |
| 01 | Detection rates (Census; TISCH2 fallback) | C | 00, Seal |
| 02 | scRNA ECS states | A | 01 |
| 03 | Freeze markers (nine genes + lineage) | A | 02 |
| 04 | TCGA confound | A | 03 |
| 05 | Name primary non-B state | A→B wall | 04, **before ICI outcomes** |
| 06 | IMvigor210 confirmatory | B | 05 |
| 07 | Melanoma replication | B (weak) | 06 |
| 08 | Converge + Decide | — | 06–07 |

Templates: study `_template.md` or [`.seal/templates/unit.md`](../.seal/templates/unit.md). After a run, fill **Notes**. Operator does not edit `PROTOCOL.md`.
