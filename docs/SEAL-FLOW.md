# SEAL flow — what order, what to run

Look here when the sequence is unclear. **You are here** is always `STATUS.md`. Today: **Decide is atlas-only.** Kill test done. Gate A **pass**, Gate B **fail**. **Next:** new atlas protocol (Phase 2b). No ICI fishing.

Generic kernel: [`.seal/E2E_FLOW.md`](../.seal/E2E_FLOW.md). This study: [`E2E_FLOW.md`](../E2E_FLOW.md). Chat cheat-sheet: [`.seal/workflows.md`](../.seal/workflows.md).

## The loop

Green = finished. Yellow = current. Grey = later.

![SEAL loop: Decide is atlas-only; next is a new protocol](diagrams/seal-loop.png)

## This study’s units

Kill-test units 00–08 are done. Decision: atlas-only; ICI reported negative.

![SCENDO units 00–08 done; Decide atlas-only](diagrams/scendo-units.png)

| Say in chat | When | What happens |
|---|---|---|
| **Run** | After Seal, one unit at a time | Done through Unit 08 |
| **Unit** | Packet missing or wrong | Writes/updates `units/<id>.md` only |
| **Converge** | After Unit 08 outputs exist | **Done** — `research/08-converge.md` |
| **Decide** | After Converge | **Done** — atlas-only (2026-08-24) |
| **Protocol** | After this Decide | New atlas protocol + new lock (Phase 2b) |
| Explore / Question / Kill / Clarify / Analyze / Seal | Kill phase done | Do not re-open the kill protocol unless a dated amendment |

OSF prereg can go up any time after the git SHA. Spark / browser / GSE220635 are not this branch unless the atlas protocol names them.

## What to run right now

![What to run: atlas protocol next](diagrams/what-to-run.png)

Stay on this laptop. **Decision: atlas-only.** Say **Protocol** for the census-scale map. Do not reopen ICI outcomes to hunt a Gate B pass.
