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
  Bootcamp closing commit/push completed as `5275f70`; Wednesday opening confirms
  clean main. Issue closure/PR merge remain separate user actions. No actual duration
  was recorded for the combined session.

## Wednesday — Guarded Database Testing (2.5-3 hours)

Allow an additional 20-30 minutes for the foundation PR handoff agreed with Furkan
at Tuesday closure: create the PR, review its checks, merge, and verify closure of
#1/#2/#5/#9 before branching for #6. Total Wednesday estimate: 3-3.5 hours including
daily review and Git closure; record any incomplete acceptance criteria explicitly.

Foundation handoff completed on 16 September: PR #28 merged as `64b14eb`, issues
#1/#2/#5/#9 closed, local main clean and synchronized, and merge-commit CI passed.
Branch cleanup and #6 implementation follow this verified baseline.

- Implement [#6](https://github.com/ozdemirr1/opsdesk/issues/6): synchronous engine and
  session factories, separate application/test settings, exact database/host guards.
- Verify real commits with independent sessions and allowlisted cleanup using a
  probe table, including exception cleanup and resource release.
- Stop here if the safety and isolation checks fail; schema work depends on them.

## Wednesday Progress Evidence — 16 September

- Furkan removed the merged foundation branch and began feature/week-10-postgresql-tests.
- Provisioned new opsdesk_product_dev/test databases with separate restricted owner
  roles; the old Month 02 databases remain untouched. README preserves fresh setup
  SQL, environment configuration, and hidden password-entry instructions.
- Implemented sync database settings/engine/session helpers, exact target guards,
  probe cleanup before/after scopes, and explicit transaction ownership.
- Local checks: Ruff passes, 20 files formatted, 37 non-database tests pass, and
  six opt-in PostgreSQL tests pass. Real commits, independent-session visibility,
  rollback, exception cleanup, and connection return are covered.
- Subprocess checks cover cleanup failure and stopping later tests. Synthetic
  secrets remain absent under the documented native-traceback/no-locals policy;
  this does not guarantee every possible debug or logging format is safe.
- Evidence and limitations are documented; grouped learning review is complete.
  Furkan committed/pushed OpsDesk as a91e2fd with a clean synchronized branch.
  The #6 target amendment is published and PR #29 has passing checks for a91e2fd.
  PR #29 merged as 3f85571 and #6 closed; main is clean and synchronized. Branch
  cleanup and bootcamp closing commit/push remain. The existing hosted workflow
  only runs seven foundation tests; expanding fast-test selection
  is a bounded follow-up, while database CI remains #25.
- No business schema or migrations were introduced. Do not compress #7 review to
  compensate for the time spent on infrastructure; actual duration is unmeasured.

## Thursday — Identity and Organization Schema (2.5-3 hours)

- Opening adjustment, 17 September: record the requested
  [September market review](../monthly-reports/2026-09-market-review.md) before
  schema work. The direction and #7 scope remain unchanged; account for this
  review within weekly capacity rather than compress migration/test verification.
- Implement [#7](https://github.com/ozdemirr1/opsdesk/issues/7) after #2 and #6 evidence.
- Initialize Alembic; add Users, Organizations, Memberships, reviewed constraints,
  canonical-email uniqueness, and the partial owner index.
- Verify upgrade/downgrade/re-upgrade separately from ordinary data tests and restore
  the expected schema. No unguarded destructive database commands.

## Thursday Carry-over Completed — Friday 18 September

- Initial identity migration, constraints, guarded Alembic configuration, identity
  cleanup, and isolated migration-cycle tests are implemented on the feature branch.
- Local evidence: 51 non-database tests, 60 PostgreSQL data tests, and 2 separate
  schema tests pass; Ruff passes for 34 Python files. Ordinary runs skip 62 database
  tests. Existing hosted CI covers only the seven foundation tests.
- Thursday exceeded its estimate. Friday completed #7 through PR #30, merged as
  d5147fe; #7 is closed, main is clean/synchronized, and the feature branch was
  removed locally/remotely. Bootcamp evidence commit/push remains pending. Do not
  compress Friday's remaining work to hide the carry-over.
- Continue with bounded #3/#10 work only after the handoff. Unfinished Friday scope
  remains explicit; no new authentication work is implied by the schema milestone.

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
  ownership, Alembic, and guarded `opsdesk_product_test` verification. The renamed
  target refers to the new product database; old Month 02 databases stay unchanged.
- Ticket schema #8 and creation #18 follow their actual dependencies; they are not
  required to fit this week. Remaining features, database CI #25, and preview #26
  stay in the Month 03 backlog.
- Docker/Compose, Redis/jobs, React, AI, and Attachment APIs remain out of scope.
- Update estimates as evidence arrives; reduce scope before skipping review or tests.


## Friday Closing Checkpoint — 18 September

#7 is merged/closed. The bootcamp schema/market-review handoff was pushed as
16b4f09. Friday's new #3/#10 work stops at an accepted shared-error contract and
passing ApiError implementation slice (23 focused tests). Product branch:
feature/week-10-api-errors. Interim product/bootcamp commits are pending evidence.

Saturday first resumes validation/transport/framework mappings, unexpected-error
handling, request IDs, safe diagnostics, and #10 verification/closure. These replace
any assumption that Saturday starts registration. Keep #3's unrelated contracts
and #4 coordination decisions open; do not compress or skip tests to reclaim time.
