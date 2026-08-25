# SEAL flow — what order, what to run

Look here when the sequence is unclear. **You are here** is always `STATUS.md`. Today: Units 00–02 done; **say `Run` for Unit 03**.

Generic kernel: [`.seal/E2E_FLOW.md`](../.seal/E2E_FLOW.md). This study: [`E2E_FLOW.md`](../E2E_FLOW.md). Chat cheat-sheet: [`.seal/workflows.md`](../.seal/workflows.md).

## The loop

Green = finished. Yellow = current. Grey = later.

![SEAL loop: lock, then run units, then Decide](diagrams/seal-loop.png)

## This study’s units

Do not open IMvigor210 or GEO **outcome** files until Unit 05 is committed.

![SCENDO units 00–08 with Unit 03 current](diagrams/scendo-units.png)

| Say in chat | When | What happens |
|---|---|---|
| **Run** | After Seal, one unit at a time | Agent executes the current unit in `STATUS.md` |
| **Unit** | Packet missing or wrong | Writes/updates `units/<id>.md` only |
| **Converge** | After Unit 08 outputs exist | Check results against the sealed protocol |
| **Decide** | After Converge | You pick stop / atlas-only / full paper |
| Explore / Question / Kill / Protocol / Clarify / Analyze / Seal | Already done | Do not re-open unless a dated amendment |

OSF prereg can go up any time after the git SHA. It is not a Unit 01 blocker. Spark is after Decide, full-paper path only.

## What to run right now

![What to run: STATUS, say Run for Unit 03](diagrams/what-to-run.png)

Stay on this laptop. No ICI phenotype/outcome files. Output: `research/03-frozen-markers.json` (nine core genes + candidate lineages from Unit 02).