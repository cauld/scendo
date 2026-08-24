# Workflows

**Canonical sequence:** [`E2E_FLOW.md`](E2E_FLOW.md). This file is the command cheat-sheet.

| Borrow | From | Here |
|---|---|---|
| Constitution → specify → plan → tasks → implement → converge | Spec Kit | Renamed for research |
| Explore before committing; archive extras | OpenSpec | Explore + `EXPLORE.md` |
| Personas; each phase writes the next phase’s context | BMAD | Without Agile |
| Kill criteria; confirmatory lock; named confound | Preregistration / COS | First-class |

## Commands

Say these in chat. The agent follows this kernel and writes under the **study dir**.

| You say | Does | Artifact |
|---|---|---|
| **Explore** | Pressure-test candidate questions | notes in `research/` |
| **Question** | Lock one claim and non-claims | `QUESTION.md`, `CLAIMS.md` |
| **Kill** | Cheap pass/fail before the full build | `KILL.md` |
| **Protocol** | How the kill (or paper) will be run | `PROTOCOL.md` (draft) |
| **Clarify** | Up to five gaps in the protocol | amendments in `PROTOCOL.md` |
| **Analyze** | Read-only consistency across artifacts | note in `STATUS.md` |
| **Seal** | Human: freeze protocol (git SHA + OSF) | `STATUS.md` sealed |
| **Unit** | One context packet the Operator can run | `units/<id>.md` |
| **Run** | Execute current unit(s) only | code + outputs |
| **Converge** | Compare outputs to protocol; append gaps | `STATUS.md` |
| **Decide** | Human: stop / shrink / full paper | `STATUS.md` decision |
| **Archive** | Side quests and dead ends | `EXPLORE.md` |

## Phase diagram

```
Explore
    → Question + Claims
    → Kill spec
    → Protocol (draft) → Clarify → Analyze
    → Seal (git + OSF)
    → Units
    → Run
    → Converge
    → Decide
        ├─ stop
        ├─ reduced scope (new protocol + new lock)
        └─ full paper (confirmatory analyses stay frozen)
```

## Out of scope for this kernel

- Epics, sprints, story points, Scrum Master
- Shipping the full product before Decide
- Treating browser screenshots as confirmatory results
