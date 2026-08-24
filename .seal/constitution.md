# Constitution

Principles every later artifact is judged against. Update rarely. If a unit of work violates this file, stop and record the exception in the study `STATUS.md` — do not silently patch the protocol after seeing results.

Study files live in a single directory (`scendo/` here; `studies/<slug>/` when extracted). Below, **study dir** means that folder.

## 1. Claims are smaller than stories

Write what the study will claim and what it will not. Do not claim clinical practice change, unmeasured mechanisms, or a “breakthrough” from a computational screen. A map plus a pre-specified test is a valid claim.

## 2. Explore freely, confirm once

Anything that informs the confirmatory analysis is **exploration**. The confirmatory test uses a frozen protocol. Results that appear only after peeking at the outcome data are exploratory, even if they look clean.

## 3. The lock is mechanical

After `PROTOCOL.md` is sealed:

- The agent may **read** it.
- The agent may **not** edit confirmatory fields (endpoints, datasets, models, gene/feature lists, pass/fail rules) to fit a nicer p-value.
- Changes require a human-authored protocol amendment with a reason, dated in `STATUS.md`, and an OSF amendment if already registered.

## 4. Discovery data ≠ confirmatory data

States, signatures, and cutoffs are defined without confirmatory outcome labels. Scoring those frozen objects on held-out (or never-trained-on) samples is the test. Retraining on the test set is a failed run, not a finding.

## 5. Kill cheaply

A short kill phase exists to stop the project. A negative kill is a success. Do not build the full paper product (atlas browser, large models, manuscript claims) before the kill decision.

## 6. Name the confound you are most afraid of

Every confirmatory claim names its leading alternative explanation and the adjustment that would kill the claim. Write that in `KILL.md`, not as an afterthought in the discussion.

## 7. Agents do not self-approve gates

Checklists and kill criteria are reviewer-owned. An agent may draft an evaluation; a human marks pass/fail.

## 8. Context is files, not chat

The next phase reads artifacts in the study dir. If it is not in those files, it did not happen.

## 9. Scale to the work

A kill test is a short loop: question → kill protocol → run → decide. A full paper adds units and converge. Do not import epics, sprints, or story points.

## 10. Extract after one completed Decide

Keep this kernel beside the first study until that study reaches Decide. Then copy `.seal/` (and filled templates, cleaned of results) into the next project.
