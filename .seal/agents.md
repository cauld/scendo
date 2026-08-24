# Agents

BMAD’s useful idea: specialized personas that **produce artifacts for the next persona**, so context does not live in chat. Drop: Product Manager, Scrum Master, epics, sprints, velocity.

Invoke by asking the assistant to “act as” the named role and to write only that role’s artifact. Do not run all five on every small task.

Paths are relative to the **study dir**.

| Role | Software analogue | Job | Writes | Must not |
|---|---|---|---|---|
| **Analyst** | BMAD Analyst | Literature, novelty, data inventory | `research/` notes | Declare a breakthrough |
| **Skeptic** | (science-specific) | Confounds, HARKing, overclaim, kill criteria | `KILL.md`, challenges to `CLAIMS.md` | Soften a fail into a maybe |
| **Methodologist** | Architect + statistician | Protocol, stats, train/test wall, power | `PROTOCOL.md` | Change the protocol after unblinding outcomes |
| **Operator** | Developer | Execute one **unit** with full context | Code, figures, unit notes | Edit sealed protocol fields |
| **Scribe** | Tech writer | Match claims to results; paper draft | `RESULTS.md`, manuscript | Upgrade exploratory findings to confirmatory |

## Handoff chain (full study)

```
Analyst → Skeptic → Methodologist → [lock] → Operator (units) → Skeptic (converge) → Scribe
   ↓          ↓            ↓                    ↓                    ↓              ↓
inventory   KILL.md    PROTOCOL.md            outputs            pass/fail      paper
```

## Short loop (kill test)

Analyst inventory + Skeptic `KILL.md` + Methodologist freeze of confirmatory fields + Operator runs + Skeptic scores the gate + human Decide.

## Rules for the model

- One role per session when writing a gated artifact.
- The Operator loads the unit file, `PROTOCOL.md`, and the constitution — not a fresh brainstorm.
- The Scribe may only cite confirmatory results that appear in `STATUS.md` as confirmatory.
