# Week 10 Plan

## Date and Capacity

14-20 September 2026 — Month 03

Target: 15-20 active hours including review, documentation, and Git work. Daily
estimates below total approximately 16-20 hours. This is a capacity plan, not a
promise to finish every P0 issue or all 22 endpoints.

## Schedule Adjustment — Tuesday, 15 September

Furkan could not access the system on Monday, 14 September; no work is recorded
for that day. At his request, Monday and Tuesday work is combined into one session
on 15 September. Aim to complete the scheduled scope with approximately 5-6 active
hours plus breaks; this remains an estimate, not completed-work evidence.

| Work block | Target time |
| --- | --- |
| Repository checks and Furkan's feature-branch setup | 15 minutes |
| #1 Ticket creation validation decisions and examples | 45 minutes |
| #2 Identity/authentication contract decisions and examples | 75 minutes |
| #5 Executable foundation, settings, tests, and README | 120 minutes |
| #9 Fast CI after meaningful tests pass locally | 45 minutes |
| Grouped learning review, documentation, and Git closure | 30 minutes |

Preserve review and test gates during the combined session. Feature-specific design
issues do not block independent foundation work; #9 requires #5's meaningful tests.
If a blocker remains, record it rather than declaring the combined scope complete.

## Outcome

Move from reviewed design into a small executable OpsDesk foundation: reproducible
installation, meaningful lifecycle/configuration tests, guarded PostgreSQL testing,
and the initial identity/Organization schema. Begin the authentication slice only
when its prerequisites and remaining capacity permit.

Continue in the Month 03 conversation. Furkan writes the learning implementation
and performs Git/GitHub mutations; mentoring starts with rationale and a small example.
OpsDesk PR #27 is merged as `c3a45ed`; local main was verified synchronized.
Use a `feature/week-10-...` branch from the verified current main after final cleanup.

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

## Tuesday Completion Evidence — 15 September

- Reviewed #1 Ticket validation (`fc81057`) and #2 identity/authentication contracts
  (`8959911`); these are design outcomes, not implemented business endpoints.
- Furkan implemented #5's package, app factory, settings, and seven tests (`a5461a4`),
  then explicit tool configuration and #9's minimal CI (`0bc43d5`). All commits were
  pushed to feature/week-10-backend-foundation; the product working tree is clean.
- Locked installation, Ruff lint/format, and seven tests passed locally. Hosted
  [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/35004969487) passed
  for `0bc43d5`. Intentional lint/format/test failures returned exit code 1 in local
  temporary copies; no hosted failure experiment or production readiness is claimed.
- The existing dependency deprecation warning remains visible. Grouped learning
  review is complete, with precision notes on factory isolation, validation timing,
  lockfile guarantees, and evidence boundaries recorded in WEEKLY_STATUS.md.
  Bootcamp closing commit/push is pending; issue closure/PR merge remain separate
  user actions. No actual duration was recorded for the combined session.

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
