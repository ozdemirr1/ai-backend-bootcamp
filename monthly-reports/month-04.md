# Month 04 review — React and full-stack integration

Weeks 13–16, starting 6 October 2026. Planned Week 16 window: 26 October–1 November;
final hosted acceptance and recovery review continued on **2 November**.
This report closes the implementation/evidence review, not every operational gate
or the entire OpsDesk backlog. Actual active hours were not measured; the
42-hour plan plus 8-hour contingency was an estimate, not time worked.

## Original targets and delivered results

| Target | Delivered evidence | Boundary |
| --- | --- | --- |
| React/TypeScript components, props, state, events, lists and forms | [Week 13](../weekly-reports/week-13.md): login/register and mock list | Foundation exercises; later product flow uses real data |
| API layer, session, validation and loading/errors | [Week 14](../weekly-reports/week-14.md); completed Organization context and protected routes in [Week 16](../weekly-reports/week-16.md) | Tokens in memory; reload requires login; logout is not token revocation |
| Ticket table/search/filter/badges/detail, comments and role-aware action | [Week 15](../weekly-reports/week-15.md) mock dashboard; Week 16 real reads, persisted comments and priority action | Assignment/status transitions and membership administration remain backlog |
| Tailwind, responsive sidebar, empty states, notification, modal, accessibility | Week 16 shared styles/forms, creation dialog, success notice, actionable states; keyboard and 1280/700/320 CSS-pixel checks | Bounded accessibility review, not a full certification |
| Backend/frontend integration, screenshots, repository/release evidence | [OpsDesk PR #49](https://github.com/ozdemirr1/opsdesk/pull/49), runtime `8a633d0`, live screenshot and persistence checks | Early synthetic-data preview; broader operational gates remain |

Real Ticket reads and protected routes slipped beyond Week 14 because the backend
read endpoints and Organization context were missing. Deployment incident recovery
also consumed time. Week 16 added these dependencies instead of presenting mock
records as completed integration. Publishing the identity preview early was useful,
but did not replace the dashboard, comments or UI outcomes.

## Final verification evidence

- Release CI on 1 November: **740 backend non-integration** and **356 frontend**
  tests; frontend build/lint and backend Ruff passed.
- Fresh 2 November: **281 PostgreSQL data tests**, **5 schema tests**, no Alembic
  metadata drift. Only guarded `opsdesk_product_test` was used destructively.
- Hosted runtime `8a633d0` / deployment `3215ab49-07c6-4b91-9372-59c14d63f47e`:
  create/select workspace, create Ticket, change priority, post Comment, logout,
  login and verify persistence. A missing comments-table runtime grant was found
  and narrowly repaired. Test and hosted schema: `84c2f9a17d60`.
- Real local two-Organization/customer/staff acceptance, 98 focused database and
  88 focused frontend tests verify scope isolation, rejected writes and cleanup.
  Those focused counts overlap the larger suites; never add them to a grand total.
- Isolated custom-format dump/restore preserved 2 Users, 2 Organizations,
  3 Memberships, 3 Tickets, 1 Comment and sequence state. Prior app `b7800e4`
  could still read its Ticket on the expanded schema without changing data.
  No live restore or hosted backup automation was performed.

Detailed commands, dates and limitations are in the
[Week 16 report](../weekly-reports/week-16.md) and
[product recovery record](https://github.com/ozdemirr1/opsdesk/blob/main/docs/release-recovery.md).

## Learner review — answers supplied on 2 November

1. **Membership versus role.** Furkan explained membership as the User/Organization
   relationship, protected by `UNIQUE(user_id, organization_id)`, and role as the
   allowed actions for owner/admin/agent/customer. His analogy was entry into a
   building versus keys to its rooms. Review: the distinction is correct; a row's
   existence alone is insufficient. Current membership, User and Organization
   activity and object-level access rules must also pass.
2. **Late responses after logout.** Furkan explained that logout resets session
   and state; an earlier asynchronous response can otherwise repopulate private
   data or conflict with cleared state. It must no longer reach the UI. Review:
   correct. Abort is best effort, so session/Organization/request identity checks
   are also needed when the network response arrives anyway.
3. **Personal difficulty and independent repeat target.** Not supplied. Leave this
   learner reflection open rather than inventing an answer or an independent
   exercise result.

Suggested short independent review before the next implementation: explain why
hiding a priority button cannot authorize a PUT, show which service owns the
transaction, and contrast app rollback with dropping the Comment migration.
These are review prompts, not claims that the learner has completed them.

## Explicit carry-over and risk assessment

| Follow-up | Why it remains | Next action |
| --- | --- | --- |
| Registration/login abuse limits and provider incident audit | Neither a healthy endpoint nor a successful demo proves safe broad exposure | Review before inviting a larger audience; keep synthetic manual testing |
| Hosted backup/export, retention and isolated restore from that export | Local synthetic restore verifies the mechanism, not hosted backup coverage or role grants | Establish and rehearse a restricted hosted-export process before further schema work |
| Development dependency findings | 2 November npm audit: 14 moderate + 2 high; production-only audit: zero | Separate compatible toolchain update with full tests/build/lint; no forced downgrade/update in this closure |
| Current hosting spend | Last supplied 1 November screenshot: $4.08 credit / 16 days; not today's balance | Recheck Usage before further deployments; no implicit paid upgrade |
| PostgreSQL CI (Q03), assignment/status and membership administration | Outside the bounded frontend completion subset | Keep as product backlog, do not close these issues from this report |
| Personal reflection | Third learner answer missing | Add the learner's own difficulty/repeat goal when supplied |

The UI/integration outcomes have evidence. The original combined Month 04
operational checklist is **not entirely green**; the unresolved gates remain
visible in the plan. This report does not waive them or claim production readiness.
Optional open-source contribution was not a required delivery and is not claimed.

## Month 05 handoff

Continue toward the same backend-focused role: Docker and Docker Compose first,
then Redis and one bounded background job (Celery or RQ after comparing the actual
need). Keep AI integration in Month 06 and RAG in Months 07–08. No provider switch
or new frontend framework is required.

Start a new project-scoped Month 05 conversation with this report, the Week 16
report and OpsDesk project status. First reconcile the operational carry-over,
then learn image/container/volume/network fundamentals using OpsDesk. Define a
reproducible local app + PostgreSQL Compose setup, guarded test targets and volume
backup semantics before adding Redis or a worker. Containerizing an unsafe setup
does not close its permissions, backup or abuse-control gaps.

No Month 05 implementation, measured hours or independent learner exercise is
claimed by this handoff. Preserve the weekly report/normal-merge workflow.
