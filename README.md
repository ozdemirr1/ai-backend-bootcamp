# AI Backend / Full-Stack Bootcamp

My 12-month learning journey toward junior backend/full-stack work, with a
backend focus and a longer-term goal of building production AI applications.
This repository contains plans, learning notes, exercises and evidence;
the real product code lives in [OpsDesk](https://github.com/ozdemirr1/opsdesk).
Production AI is the direction of the roadmap, not a claim of current readiness.

## Current focus — Month 05 planning, 3 November 2026

The [approved Month 05 plan](monthly-plans/month-05.md) defines Docker/Compose,
Redis cache/rate limiting, Celery retry/idempotency and expanded CI with basic
Linux/logging. Weekly plans: [17](weekly-reports/week-17-plan.md),
[18](weekly-reports/week-18-plan.md), [19](weekly-reports/week-19-plan.md),
[20](weekly-reports/week-20-plan.md). Planning is complete; implementation has not
started. GitHub Actions fundamentals, incremental examples and
independent failure diagnosis are included; existing test counts do not replace learning. Existing frontend behavior stays; no new React/AI/Kubernetes scope.

Month 05 starts on **4 November 2026**; planned closure is 30 November.
Continue in a new month-scoped conversation using the
[Month 05 handoff](monthly-plans/month-05-handoff.md).

## Month 04 checkpoint — 2 November 2026

**Month 04 UI/integration delivered; technical review and Month 05 handoff recorded.**
The [OpsDesk preview](https://opsdesk-production-448f.up.railway.app/) uses protected
workspaces, real Ticket creation/search/detail, persisted comments and role-aware
priority changes. Tailwind/responsive layout, modal, success feedback and keyboard/
empty/loading/error handling shipped through
[OpsDesk PR #49](https://github.com/ozdemirr1/opsdesk/pull/49) at `8a633d0`.

Hosted persistence and local customer/staff isolation were verified on 2 November.
Fresh local checks: 281 PostgreSQL data tests and 5 schema tests, no drift, plus
isolated backup/restore and previous-version Ticket-read compatibility. Release CI
on 1 November passed 740 backend non-integration and 356 frontend tests, build/lint
and Ruff. These are separate test groups and dates.

The scoped frontend outcomes are delivered; **the combined Month 04 operational
gates are not all closed**. Hosted backup coverage, abuse controls, provider audit,
current usage review and development-tool dependency findings remain explicit.
The learner supplied two review answers; the personal reflection is still open.

- [Month 04 review and Month 05 handoff](monthly-reports/month-04.md)
- [Current status](WEEKLY_STATUS.md)
- [Week 16 plan](weekly-reports/week-16-plan.md) and [report](weekly-reports/week-16.md)
- [Month 04 alignment history](notes/react/month-04-alignment.md)
- [12-month roadmap](ROADMAP.md) and [decision log](DECISIONS.md)

## Learning journey and evidence

Weekly reports and the separate plans introduced after Week 01 continue through
Months 03 and 04. The main change is
where implementation lives: Month 01/02 exercises are here; product development
moved to OpsDesk in Week 09. Later reports contain dated daily checkpoints;
their opening summaries distinguish final outcomes from earlier pending work.

| Phase | Learning and implementation | Weekly evidence | Review / actual outcome |
| --- | --- | --- | --- |
| Month 01 · Weeks 01–04 | Git/terminal, Python, HTTP/REST, CLI exercises and basic tests | [01](weekly-reports/week-01.md), [02](weekly-reports/week-02.md), [03](weekly-reports/week-03.md), [04](weekly-reports/week-04.md) | [Month 01 review](weekly-reports/week-04.md#month-1-review) is inside Week 04 |
| Month 02 · Weeks 05–08 | FastAPI, PostgreSQL, SQLAlchemy/Alembic, authentication and authorization in the learning API | [05](weekly-reports/week-05.md), [06](weekly-reports/week-06.md), [07](weekly-reports/week-07.md), [08](weekly-reports/week-08.md) | [Month 02 review](monthly-reports/month-02.md); original CI/deployment targets carried forward |
| Month 03 · Weeks 09–12 | Separate OpsDesk product: design, architecture, CI/errors, schema, identity, Organization reads and Ticket creation | [09](weekly-reports/week-09.md), [10](weekly-reports/week-10.md), [11](weekly-reports/week-11.md), [12](weekly-reports/week-12.md) | [Month 03 retrospective](monthly-reports/month-03.md); workflow/comments and full backend release remained open |
| Month 04 · Weeks 13–16 | React/TypeScript/Tailwind, protected real-data workspaces, Ticket creation/reads, comments and priority | [13](weekly-reports/week-13.md), [14](weekly-reports/week-14.md), [15](weekly-reports/week-15.md), [16 plan](weekly-reports/week-16-plan.md) | [Month 04 review](monthly-reports/month-04.md); UI/integration delivered, operational carry-over explicit |

Week 01 records focus and outcomes in one report; subsequent weeks have separate
plan/report files. Week 16 closes its implementation evidence on 2 November while
keeping operational gates and learner reflection explicit. Test counts verify
specific checks; they do not substitute for independent learner explanations.

## Projects and technology sequence

| Project | Current state | Planned direction |
| --- | --- | --- |
| [OpsDesk](https://github.com/ozdemirr1/opsdesk) | Active since Week 09; live workspace, Ticket creation/reads, comments and priority | Remaining workflow/membership operations; Docker/Redis in Month 05, AI in Month 06 |
| DocuMind | Planned; no completed product claimed | Document upload, embeddings, pgvector retrieval and grounded answers in Months 07–08 |
| HireMatch AI | Planned; no completed product claimed | CV/job matching with validated structured output in Month 09 |

Current stack: Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, React,
TypeScript, Tailwind and GitHub Actions;
Docker/Redis/background jobs remain Month 05, OpenAI integration/evals Month 06,
and RAG/pgvector Months 07–08. Prefer depth over unrelated technology switching.

## Repository guide

- [Weekly plans and reports](weekly-reports/) — learning goals, tasks, code/test
  evidence, review questions and next-week preparation.
- [Monthly reviews](monthly-reports/) — outcomes, deviations and handoffs; Month 01
  is preserved in Week 04 as linked above.
- [Topic notes](notes/) — concepts and scoped examples. Historical learning API
  designs are not the current OpsDesk product contract.
- [Historical learning projects](projects/) — including the completed
  [Month 02 Ticket API](projects/month-02-ticket-api/README.md) and bounded
  [Week 06 SQL lab](projects/week-06-postgresql-sql/README.md).
- [Railway deployment notes](notes/deployment/opsdesk-railway-preview.md) — dated
  setup/recovery evidence and open operational checks.
- [Publication draft](notes/career/opsdesk-live-preview-linkedin.md) and
  [visual assets](assets/linkedin/opsdesk-live-preview/README.md) — drafts/assets
  do not establish publication or current product scope.
- [September market review](monthly-reports/2026-09-market-review.md) — sourced
  career review and adopted priorities.

The learning API uses `opsdesk_dev` / `opsdesk_test`. The separate product uses
`opsdesk_product_dev` / `opsdesk_product_test`; the hosted demo is `opsdesk_demo`.
Never substitute the old learning database for the product's guarded test target.

## Development Setup

Install `uv` by following the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

The repository pins its development Python version in `.python-version` and stores the exact dependency resolution in `uv.lock`.

Create or synchronize the project environment:

```bash
uv sync
```

Project commands can be run through `uv run` without manually activating the virtual environment.

Runtime dependencies are declared in `[project.dependencies]`. Test and code-quality tools are declared in `[dependency-groups].dev`.

## Quality Checks

Verify that the lockfile and environment are synchronized:

```bash
uv sync --check
uv lock --check
```

Run all tests:

```bash
uv run pytest -q
```

Run lint and formatting checks:

```bash
uv run ruff check .
uv run ruff format --check .
```

Check the installed dependency set:

```bash
uv pip check
```
