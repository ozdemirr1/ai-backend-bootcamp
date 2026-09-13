# Week 10 Plan

## Date and Capacity

14-20 September 2026 — Month 03

Target: 15-20 active hours including review, documentation, and Git work. Daily
estimates below total approximately 16-20 hours. This is a capacity plan, not a
promise to finish every P0 issue or all 22 endpoints.

## Outcome

Move from reviewed design into a small executable OpsDesk foundation: reproducible
installation, meaningful lifecycle/configuration tests, guarded PostgreSQL testing,
and the initial identity/Organization schema. Begin the authentication slice only
when its prerequisites and remaining capacity permit.

Continue in the Month 03 conversation. Furkan writes the learning implementation
and performs Git/GitHub mutations; mentoring starts with rationale and a small example.
Use a `feature/week-10-...` branch after resolving the Week 09 branch/PR handoff.

## Monday — Contracts and Foundation Start (2.5-3 hours)

- Confirm final Week 09 commits and branch/PR state before choosing the checkout.
- Work on [#1 Ticket validation](https://github.com/ozdemirr1/opsdesk/issues/1) and
  [#2 identity contracts](https://github.com/ozdemirr1/opsdesk/issues/2): choose exact
  bounds, normalization, password handling, duplicate behavior, and token policy.
- Record reviewed decisions and boundary examples in product documents. Carry any
  unfinished decision forward explicitly; issue closure alone is not evidence.
- Begin [#5 foundation](https://github.com/ozdemirr1/opsdesk/issues/5) as capacity allows.
  Use the established Python/uv workflow after compatibility checks, without copying
  Month 02 source or adding unrelated dependency-management alternatives.

## Tuesday — Executable Foundation and Fast CI (2.5-3 hours)

- Continue #5: application creation, settings, lifespan, README commands, and isolated
  startup/configuration/docs tests. No database or authentication dependency yet.
- Add [#9 fast CI](https://github.com/ozdemirr1/opsdesk/issues/9) only once meaningful
  executable tests exist. Verify locked installation, Ruff, and pytest.

## Wednesday — Guarded Database Testing (2.5-3 hours)

- Implement [#6](https://github.com/ozdemirr1/opsdesk/issues/6): synchronous engine and
  session factories, separate application/test settings, exact database/host guards.
- Verify real commits with independent sessions and allowlisted cleanup using a
  probe table, including exception cleanup and resource release.
- Stop here if the safety and isolation checks fail; schema work depends on them.

## Thursday — Identity and Organization Schema (2.5-3 hours)

- Implement [#7](https://github.com/ozdemirr1/opsdesk/issues/7) after #2 and #6 evidence.
- Initialize Alembic; add Users, Organizations, Memberships, reviewed constraints,
  canonical-email uniqueness, and the partial owner index.
- Verify upgrade/downgrade/re-upgrade separately from ordinary data tests and restore
  the expected schema. No unguarded destructive database commands.

## Friday — Shared Contracts and Errors (2.5-3 hours)

- Resolve required portions of [#3](https://github.com/ozdemirr1/opsdesk/issues/3)
  before [#10 shared errors/logging](https://github.com/ozdemirr1/opsdesk/issues/10).
- Implement only reviewed error and logging behavior; verify sensitive input is
  excluded and infrastructure failures are not mislabeled as ordinary user errors.
- Continue [#4 concurrency design](https://github.com/ozdemirr1/opsdesk/issues/4)
  before any dependent coordinated mutation work. Do not invent a locking protocol
  inside a feature implementation without review.

## Saturday — Consolidation or First Authentication Slice (2-3 hours)

- Finish incomplete foundation/schema/error work first.
- If #2, #7, and #10 are complete, begin
  [#11 registration](https://github.com/ozdemirr1/opsdesk/issues/11), including hash
  verification, safe output, known-constraint mapping, and duplicate-email races.
- [#12 login](https://github.com/ozdemirr1/opsdesk/issues/12) and
  [#13 current-user resolution](https://github.com/ozdemirr1/opsdesk/issues/13) are
  stretch work. Controlled fixtures allow their tests without requiring registration
  to be implemented first. Shared identity/hash contracts must remain consistent.

## Sunday — Review and Handoff (1.5-2 hours)

- Run the checks appropriate to completed work and record actual results.
- Review architecture questions, update product documents, and close issues only
  with their acceptance evidence. Record partial progress and carry-over honestly.
- Write the weekly report and perform Furkan's staged review/commit/push workflow.
- Spend 20-30 minutes on the carried-over career action: identify two relevant
  backend internship targets and prepare one tailored English outreach draft.
  Furkan chooses whether to send it; no outreach is sent automatically.

## Boundaries and Completion Evidence

- Design tasks require reviewed decisions/examples; implementation tasks require
  relevant passing tests and committed code. A green unrelated test is insufficient.
- Retain synchronous SQLAlchemy, request-scoped sessions, explicit transaction
  ownership, Alembic, and guarded `opsdesk_test` verification.
- Ticket schema #8 and creation #18 follow their actual dependencies; they are not
  required to fit this week. Remaining features, database CI #25, and preview #26
  stay in the Month 03 backlog.
- Docker/Compose, Redis/jobs, React, AI, and Attachment APIs remain out of scope.
- Update estimates as evidence arrives; reduce scope before skipping review or tests.
