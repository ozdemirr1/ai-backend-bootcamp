# Month 05 conversation handoff

Prepared 3 November 2026. Start: 4 November. Target closure: 30 November.
This document transfers context; it is not evidence that planned work was performed.

## Read first

- Local `AGENTS.md` in the bootcamp checkout (gitignored; not available in a fresh clone).
- [Month 05 plan](month-05.md): approved scope, architecture, safety and acceptance.
- [Week 17 plan](../weekly-reports/week-17-plan.md): first daily task.
- [ROADMAP](../ROADMAP.md), [WEEKLY_STATUS](../WEEKLY_STATUS.md), [DECISIONS](../DECISIONS.md).
- [Month 04 review](../monthly-reports/month-04.md): dated evidence and remaining risks.
- In the separate OpsDesk checkout: applicable AGENTS.md, README.md,
  docs/project-status.md, docs/api-contract.md and existing CI workflows.

## Product baseline

OpsDesk has live authentication, protected organization workspaces, real Ticket
creation/search/list/detail, persisted comments, role-aware priority controls,
responsive styling and creation modal. PR #49 delivered the feature code; #50
aligned recovery/release evidence. Check current Git/CI/deployment state before
assuming these are still the latest commits. Historical tests are recorded in
the Month 04 review; do not report them as fresh runs.

Product issues #19/#24 were closed with evidence. #25 PostgreSQL CI is targeted
in Week 18. Assignment, lifecycle and membership/ownership backlog remains;
this month does not require completing all product issues. Hosted backup coverage,
provider audit, dependency findings and abuse controls have follow-ups; review
the latest records rather than claiming the whole product is complete.

## Approved Month 05 scope

- Week 17, 4–9 November: basic Docker image, then multi-stage Node build/Python
  runtime, non-root and Linux/process/port/log basics; GitHub Actions foundations.
- Week 18, 10–16 November: Compose, DNS/volumes/config/readiness, migrations and
  guarded PostgreSQL integration CI.
- Week 19, 17–23 November: organization-scoped Ticket status stats, Redis cache,
  TTL/invalidation, login/register rate limiting; Redis CI and failure tests.
- Week 20, 24–30 November: simple Celery worker first, then retry/timeouts,
  durable idempotency, commit/publish gap and bounded outbox; real worker CI.

Preserve existing src/opsdesk and frontend structure. Existing React is built and
served by FastAPI; no new frontend features. No RQ, RAG, MCP, agents, Kubernetes,
AI implementation or cloud migration. Compose must start the system after the
one-time documented local configuration. Existing CI stays; Docker/DB/Redis/worker
checks are added as implemented. Estimates total 84–108 hours; extend dates if
learning or acceptance fails rather than compressing or inventing completion.

## Working agreement

Explain reasoning/architecture before substantial code. Use concept → small
example → bounded OpsDesk change → deliberate failure diagnosis → tests → learner
explanation. Teach GitHub Actions fully despite existing CI/test counts. Small
examples are useful; do not turn them into unrelated new projects or build the
whole month without learner checkpoints. Do not invent personal reflections.

Use existing weekly reports and topic notes; no unsolicited daily work reports.
Weekly feature branches and meaningful product wording, no assistant branding.
Normal PR merges preserve history. Verify checks before merging. Keep one primary
conversation per month. New chat begins by reading files, not recreating the plan.

Keep secrets, complete DB URLs and machine paths out of committed config/logs.
Destructive product tests target only guarded opsdesk_product_test; never dev or
hosted databases. Preserve synchronous SQLAlchemy, Alembic and explicit transaction
ownership. Authorization precedes cache; worker idempotency is not HTTP idempotency.
Real email/AI is excluded; notification simulation must be labelled accurately.

## First session — 4 November

Inspect both repositories' git status, applicable instructions, existing build/CI
configuration and local Docker availability. Preserve unrelated edits. Explain
the architecture and today's bounded steps. Begin Week 17's baseline task and
small Docker concept exercise; do not jump straight to Redis or Celery.

The local AGENTS.md was aligned with this plan but is ignored by Git. If it is
missing, this tracked handoff and the monthly plan retain the essential agreement.
