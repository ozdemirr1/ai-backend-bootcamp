# Week 11 Plan

## Dates, scope and completion target

21–27 September 2026 — Month 03. Monday/Tuesday were used for Week 10 carry-over.
Revised at Furkan's request on 23 September: consolidate remaining Week 10 work here
and target completion by Sunday 27 September, with no planned Week 12 spillover.
This supersedes the earlier 15–18-hour identity-only plan and registration-only
fallback. It changes the work plan, not the backend-first roadmap or test standards.

## Fixed completion scope

1. Publish Week 10 report, completed career research and bootcamp evidence.
2. Resolve all six remaining D03 groups: membership/Comment inputs, collections and
   filters/count consistency, nested responses, repeated requests/error precedence,
   timestamp policy and Attachment migration timing. Review examples and publish a
   design PR closing #3 only when every acceptance criterion is met.
3. Implement, test and merge registration #11, login #12 and current User #13.
4. Verify the complete identity flow, update documentation, close Week 11 evidence
   and prepare Week 12 without intentionally carrying these tasks forward.

Career research and the unsent draft are already prepared; do not repeat them or
send an application automatically. #4 design is already merged; do not reopen it.

## Late Wednesday adjustment — 23 September, 23:19

At Furkan's request, Wednesday ends with Week 10 Git publication only. No D03
review, registration schemas or hashing implementation is claimed for Wednesday.
Redistribute that technical scope across 24–27 September without removing any
of the fixed completion scope above or planning a Week 12 transfer.

Remaining technical-work estimate: 24–31 active hours over four days, including
explanations, tests, review, documentation and Git work. Tonight's closing commands
are separate (approximately 10–20 minutes). This is a planning estimate, not measured
throughput or a guarantee. Breaks and external CI waits are additional.

## Daily packages

| Date | Active-hour estimate | Work and completion evidence |
| --- | --- | --- |
| Wed 23, closing only | 10–20 min | Review/stage Week 10 evidence and revised plan, commit/push, verify clean synchronized bootcamp; stop for the night |
| Thu 24 | 7–9 h | Resolve D03 field limits and response structures; explain registration architecture, schemas and Argon2id; complete registration persistence/endpoint and grouped validation/hash tests |
| Fri 25 | 6–8 h | Finish registration rollback and controlled duplicate-email race, review/CI/merge #11; decide D03 collection/filter/count policy; implement and verify login/JWT issuance #12 |
| Sat 26 | 6–8 h | Resolve D03 repeats/error precedence, timestamps and Attachment timing; cross-check/publish #3 design PR; implement bearer verification and /users/me #13 with full D02 rejection/current-state tests |
| Sun 27 | 5–6 h | Finish outstanding verification/review and #3/#12/#13 merges; register→login→me integration, relevant regression, corrections, learning review, Week 11 report and Git closure |

Sunday retains correction time but has less free buffer after redistribution.
Thursday/Friday overruns must be surfaced at block boundaries, not first discovered
on Sunday. No extra feature is added if a block finishes early.

Track four packages above, and update completed/remaining work after each 60–90
minute block. Group same-file tests and explain each behavior before implementation.
Use Sunday buffer first when earlier work overruns; do not add another feature just
because one block finishes early. Report any blocker threatening Sunday completion
as soon as discovered, with remaining work and options. A missed target is reported
honestly, never concealed by skipped tests, silent scope reduction or false closure.

## Architecture and verification gates

- Explain HTTP schema → application service → persistence responsibilities before
  code; use a small analogous example, then Furkan implements the product exercise.
- Reuse accepted identity contract and shared safe transport/error behavior.
  Never write password or JWT cryptography manually; secrets stay in environment.
- Hash before holding database write locks. Commit before 201; only the known email
  constraint becomes email_already_exists. Unknown failures do not become 409/401.
- Registration creates a User only. Verify original password against stored hash,
  secret-free projections, extra-field rejection, insertion/commit rollback and
  concurrent duplicate attempts with independent sessions joined before cleanup.
- Login tests use controlled time/settings, actual library signature verification,
  generic credential failure and no token issuance after failure. No exact timing
  equality guarantee is claimed.
- /users/me re-reads persisted User state; validate all D02 claim types and required
  claims. A valid token is not Organization authorization. No business writes.
- Use the guarded opsdesk_product_test target; no destructive old Month 02 database
  access. No schema-cycle reruns unless schema/migration changes justify them.
- Group tests by file/behavior and explain what each tests. Complete relevant focused
  checks, then one regression pass per merge candidate; repeat only for new evidence.
- Branches: feature/week-11-registration, feature/week-11-login and
  feature/week-11-current-user, created only as needed from the proper reviewed base.
  Furkan performs commits/push/merge; every closure needs the matching head and CI.

## Notes and learning review

Record accepted architecture, failure mappings and actual test results in the
product README and weekly evidence. Explain: authentication versus authorization;
why hashing precedes a short write transaction; why a pre-query cannot guarantee
email uniqueness; why JWT signature/claims are checked before trusting sub; why
current User activity must be read even with a valid token; why DB failure is not 401.

## Month 03 backlog outside this combined scope

D03 design decisions are now included above rather than deferred. Their dependent
Organization/Ticket endpoints are separate implementation issues, not automatically
part of Week 10 carry-over. Ticket schema #8, Organization services, executable #4
business locking, database CI #25 and preview deployment remain in the Month 03
backlog. This five-day plan does not claim to deliver the entire monthly milestone.
Reconcile those remaining monthly deliverables at the Week 12 planning gate; do not
call them complete or promise an unchanged Month 03 delivery date without sizing.

## Thursday progress — 24 September 2026

- Completed the registration architecture and implementation slice: strict email and
  password schemas, shared normalization, pwdlib Argon2id hashing, domain/repository
  boundaries, explicit commit/rollback ownership, SQLAlchemy persistence, dependency
  wiring and `POST /users`.
- Verified safe projection, rejected client-controlled fields, known-constraint-only
  duplicate mapping, rollback paths, fresh-Session persistence, absence of membership
  side effects and the application-owned engine lifecycle.
- Local final checks passed: Ruff lint; 57 formatted Python files; 147
  non-integration tests with 68 database/schema tests deselected; and all 66 ordinary
  PostgreSQL integration tests. The two schema-cycle tests were intentionally not
  rerun because no schema or migration changed.
- Completed two D03 groups: Comment/membership input fields and Organization/
  ownership-transfer response structures. Collections/filter/count consistency,
  repeated-operation/error precedence, timestamps and Attachment migration timing
  remain open.
- Published clean synchronized product commits `c2eef64` (registration) and
  `3ad8771` (contract refinements) on `feature/week-11-registration`. No PR, hosted
  CI, merge or issue closure is claimed yet.

Registration still requires the controlled independent-Session duplicate race before
#11 review. The remaining fixed Week 11 scope is estimated at 17–23 active hours over
Friday–Sunday: finish and merge #11, resolve four D03 groups and #3, implement/merge
#12 and #13, run the complete identity-flow review, and close weekly evidence. This
replaces the pre-Thursday remaining estimate; it does not reduce acceptance criteria.
