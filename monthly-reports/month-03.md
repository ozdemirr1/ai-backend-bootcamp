# Month 03 retrospective — OpsDesk backend foundation

Consolidated on 19 October 2026 from the existing weekly reports. This is a
retrospective, not a newly executed test run or a claim that the entire product
backlog was completed. Month 03 learning covers Weeks 09–12, beginning 7 September;
the final Week 12 package closed on 5 October. Month 04 began on 6 October.

## Delivered evidence

| Week | Outcome | Source |
| --- | --- | --- |
| 09 | Separate OpsDesk repository, requirements, domain/access rules and reviewed API backlog | [Week 09 report](../weekly-reports/week-09.md) |
| 10 | FastAPI foundation, guarded synchronous PostgreSQL, identity schema, errors and request diagnostics | [Week 10 report](../weekly-reports/week-10.md) |
| 11 | Registration, login/JWT, persisted current User and remaining API contracts | [Week 11 report](../weekly-reports/week-11.md) |
| 12 | Tenant-consistent Ticket schema, Organization creation/reads and authenticated Ticket creation | [Week 12 report](../weekly-reports/week-12.md) |

Final Week 12 Ticket-creation verification recorded 439 non-integration tests,
157 ordinary PostgreSQL integration tests and 3 guarded schema/migration tests
in separate suites. Alembic ended at `31be9023cfb2`; product main ended at
`ec418f9`. These historical numbers are not today's regression totals.

## Engineering lessons

- Database constraints establish structural invariants; current membership,
  role, activity and workflow authority still require application checks.
- Services own business transactions; repositories do not commit independently.
- Real PostgreSQL tests demonstrate constraints, locks, persistence and rollback
  that fake repositories cannot establish.
- A validated JWT identifies a User; it does not replace current tenant authorization.
- Written concurrency rules are not implementation evidence. Record design,
  executable behavior, local tests and hosted checks separately.

## Variance and carry-over

Illness and underestimated schema/test work affected the calendar. Week 10 carried
into the following week; Week 11 closed 28 September and Week 12 closed 5 October.
Actual active hours were not measured. Do not describe calendar days as coding hours.

The early deployed-backend milestone was not achieved during Month 03. It was
delivered during the Week 15 Railway work on 18–19 October and is recorded there,
not retroactively counted as Month 03 completion.

Ticket reads, assignment/status workflows, comments and remaining membership
mutations are still product backlog. Guarded database CI, Docker, Redis and AI
also remain later work. A complete support platform was not the delivered result.

## Handoff and current position

Week 13 introduced React/TypeScript and mock Ticket forms; Week 14 integrated the
identity API. Week 15 now has a public identity preview. This progression supports
the backend-focused career goal while adding practical frontend skills.

After the bounded Week 15 release checks, resume Month 04 integration and UI
fundamentals. The 20 October alignment correction restores dashboard exercises now,
with Organization context and missing Ticket reads tracked as integration dependencies.
Preserve Month 05 Docker/background-work and Month 06
AI sequencing. See [current status](../WEEKLY_STATUS.md) and the
[roadmap](../ROADMAP.md) for current evidence and next priorities.
