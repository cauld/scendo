# SEAL flow — what order, what to run

Look here when the sequence is unclear. **You are here** is always `STATUS.md`. Today: atlas protocol **SEALED**. Kill done (A pass, B fail, Decide atlas-only). Gates D and E **pass**. Units 10–13 **done**. **Say `Run`.** That is Unit 14 (converge + frozen ICI).

Generic kernel: [`.seal/E2E_FLOW.md`](../.seal/E2E_FLOW.md). This study: [`E2E_FLOW.md`](../E2E_FLOW.md). Chat cheat-sheet: [`.seal/workflows.md`](../.seal/workflows.md).

## The loop

Green = finished. Yellow = current. Grey = later.

![SEAL loop: Unit 13 done; Run Unit 14](diagrams/seal-loop.png)

## This study’s units

Kill units 00–08 done. Atlas Units 10–13 done (Gates D and E pass). Unit 14 is next.

![SCENDO Unit 13 done; Unit 14 next](diagrams/scendo-units.png)

| Say in chat | When | What happens |
|---|---|---|
| **Run** | After Unit 13 | **Say this now.** Unit 14 only |
| **Unit** | Packet missing or wrong | Writes/updates `units/<id>.md` only |
| **Clarify** | After Protocol draft | **Done** |
| **Analyze** | After Clarify | **Done** |
| **Seal** | After Analyze | **Done** — atlas SHA in `STATUS.md` |
| **Protocol** | Atlas lock | **Done** — `PROTOCOL-ATLAS.md` (kill `PROTOCOL.md` untouched) |
| Explore / Question / Kill / Decide | Kill phase done | Do not re-open Gate B |

OSF prereg can go up any time after the kill git SHA. Browser / scGPT / GSE220635 are not in this lock.

## What to run right now

![What to run: say Run](diagrams/what-to-run.png)

Stay on this laptop. **Say `Run`.** Unit 14 only. Do not reopen ICI outcomes. Do not promote myeloid / T/NK catalog rows. Stromal subtypes stay display-only.
