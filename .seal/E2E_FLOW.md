# End-to-end flow

Assembled from existing practices. Not a new framework.

Software SDD: lock the spec, then implement, then check the spec.  
This loop: lock the **preregistration**, then analyze, then check the preregistration.

Instantiate by copying `templates/` into a study directory. Fill study-specific gates and units there. This file stays generic.

---

## What we compose

| Stage | Working files | Source (do not reinvent) |
|---|---|---|
| Explore | `research/` notes | OpenSpec explore; BMAD forge-idea |
| Rules | `.seal/constitution.md` | Spec Kit constitution; COS confirmatory vs exploratory |
| What / why | `QUESTION.md`, `CLAIMS.md` | Spec Kit specify; BMAD spec |
| Cheap stop | `KILL.md` | Go/no-go; BMAD forge-idea |
| How | `PROTOCOL.md` | Spec Kit plan; SAP |
| Tighten | Clarify + read-only Analyze | Spec Kit clarify / analyze |
| **Lock** | Git SHA in `STATUS.md`; **OSF secondary-data prereg** | [OSF](https://osf.io/gvcs); [prereg](https://pypi.org/project/prereg/) CLI |
| Packets | `units/*.md` | BMAD stories (context only — no Scrum) |
| Execute | Run one unit; do not edit sealed fields | Spec Kit implement |
| Check | Converge vs protocol | Spec Kit converge |
| Side quests | `EXPLORE.md` | OpenSpec archive; COS exploratory ledger |
| Human gates | Reviewer marks kill and Decide | Spec Kit: agents do not self-approve |
| Optional later | Eureka / Science Superpowers hooks | After a first Decide, if IDE enforcement is needed |

The public lock is **OSF**, not a local nickname.

---

## The loop

```
 EXPLORE          SPECIFY              PLAN               LOCK
 (OpenSpec /      (question +          (protocol +        (git hash +
  BMAD forge)      claims + kill)       clarify/analyze)    OSF prereg)
      │                  │                    │                  │
      └──────────────────┴────────────────────┴──────────────────┘
                                      │
                                      ▼
                         UNITS → RUN → CONVERGE → DECIDE
                         (BMAD packets)  (Spec Kit)   (human)
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
                  stop          reduced scope         full paper
                               (new lock)          (tests stay frozen)
```

Chat shorthand:  
**Explore → Question → Kill → Protocol → Clarify → Analyze → Seal (OSF) → Unit → Run → Converge → Decide → Archive.**

---

## Stages

### 0. Explore

Pressure-test candidate questions. Record rejects and deferrals in `EXPLORE.md`.

**Exit:** one question.

### 1. Specify

| File | Job |
|---|---|
| `QUESTION.md` | One sentence |
| `CLAIMS.md` | What we may / may not say |
| `KILL.md` | Pass/fail gates and Decide table |

Human agrees, or changes **now**. After Seal, amendments only.

**Exit:** claims and kill criteria accepted.

### 2. Plan

| File | Job |
|---|---|
| `PROTOCOL.md` | CONFIRMATORY fields: data roles, endpoints, models, cutoff rule |
| `PHASES.md` | Study checklist |
| `units/` | Operator packets |

**Clarify** gaps. **Analyze** (read-only): artifacts must not contradict. Note in `STATUS.md`.

**Exit:** Analyze recorded.

### 3. Lock

1. Human: protocol is good.
2. Git commit of `QUESTION.md`, `CLAIMS.md`, `KILL.md`, `PROTOCOL.md`.
3. Record SHA in `STATUS.md`. Optional: `prereg freeze`.
4. **OSF** Secondary Data Preregistration, mapping those files. Disclose prior knowledge of the datasets; disclose that confirmatory outcome plots have **not** been used to choose the model.
5. Agent may read CONFIRMATORY sections; may not edit them to fit results.

**Exit:** `STATUS.md` has sealed + SHA (+ OSF URL when submitted).  
Until then: no confirmatory outcome-vs-predictor analysis.

### 4. Execute

Operator loads constitution + protocol + **one** unit.

**Exit:** kill gates scored by the human (Skeptic may draft).

### 5. Converge

Compare outputs to the sealed protocol. Gaps → new units (append-only). Do not rewrite confirmatory fields. Archive leftovers in `EXPLORE.md`.

### 6. Decide (human)

Typical branches (rename in the study `KILL.md`):

| Kill result | Next |
|---|---|
| Gates pass | Full paper; confirmatory analyses stay frozen |
| Map/resource passes, outcome test fails | Reduced paper; outcome chapter reported negative |
| Confound explains the signal | Stop or reframe without the strong claim |
| All gates fail | Stop |

### 7. After Decide

Only the chosen branch. Scribe ≤ `CLAIMS.md`. OSF: upload outputs; label deviations exploratory. Optional: copy this `.seal/` folder into the next study.

---

## Roles

| Who | When |
|---|---|
| Analyst | Inventory, literature |
| Skeptic | Kill criteria, gate scoring draft |
| Methodologist | Protocol, stats, data wall |
| Operator | One unit at a time |
| Human | Seal, gate pass/fail, Decide, OSF |
| Scribe | After Decide |

---

## Where the study-specific list lives

Unit IDs, datasets, and gate names belong in the study dir (`PHASES.md`, `KILL.md`, `units/`), not in this file.
