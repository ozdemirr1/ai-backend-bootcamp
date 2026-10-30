# AI Backend / Full-Stack Bootcamp

My 12-month learning journey toward junior backend/full-stack work, with a
backend focus and a longer-term goal of building production AI applications.
This repository contains plans, learning notes, exercises and evidence;
the real product code lives in [OpsDesk](https://github.com/ozdemirr1/opsdesk).
Production AI is the direction of the roadmap, not a claim of current readiness.

## Current checkpoint — 30 October 2026

**Week 16, Month 04: completing real integration and the frontend MVP.**
The [OpsDesk live preview](https://opsdesk-production-448f.up.railway.app/) now
requires login for Workspaces and reads real Organization/Ticket data. Registration,
login, workspace creation/selection, Ticket list/detail, search/filter, reload and
logout passed hosted smoke on 29 October, closing the interrupted 28 October work.
A new workspace starts empty; Ticket creation UI is still pending.

Product PR #47 merged as `2013248`, bootcamp PR #11 as `e94c0a9`. Product CI passed
and Railway deployed successfully from `main`, including Comment storage migration
`84c2f9a17d60`. Comment service/GET/POST API and authorization/concurrency tests were then
implemented locally on 29 October. On 30 October, CommentForm/list and the priority backend subset were completed
locally. Publication, priority UI and the full visual pass remain open: **the original Month 04 MVP is not complete**.

30 October results: 740 backend non-integration, 281 PostgreSQL data and 278
frontend tests across 14 files; build/lint/Ruff passed. The 5 schema tests retain
their 28 October results. Comment API commits were pushed to the feature branch;
the UI/priority continuation is uncommitted and not deployed.
The revised Week 16 plan targets all original Month 04 outcomes on 26 October–1
November: 42 focused hours plus up to 8 contingency hours and explicit gates.

- [Current status and evidence limits](WEEKLY_STATUS.md)
- [Week 15 plan](weekly-reports/week-15-plan.md) and [report](weekly-reports/week-15.md)
- [Month 04 alignment and carry-over](notes/react/month-04-alignment.md)
- [Week 16 plan: 26 October–1 November](weekly-reports/week-16-plan.md) and [in-progress report](weekly-reports/week-16.md)
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
| Month 04 · Weeks 13–16 | React/TypeScript, live identity/workspace integration, real Ticket reads and Comment storage | [13](weekly-reports/week-13.md), [14](weekly-reports/week-14.md), [15](weekly-reports/week-15.md), [16 plan](weekly-reports/week-16-plan.md) | In progress; [dependency and schedule correction](notes/react/month-04-alignment.md#25-october-checkpoint-and-carry-over) |

Week 01 records its focus and outcomes in one report; Weeks 02–15 have separate
plan/report files in `weekly-reports/`. Week 16 now has its plan and an in-progress
report: Monday baseline, contract, backend read implementation, database tests
and Railway usage review are recorded. The new backend is published through
[OpsDesk PR #46](https://github.com/ozdemirr1/opsdesk/pull/46); the live dashboard
now uses the protected real-data flow deployed through PR #47. Future work is not presented as completed evidence. The Month 04 retrospective is due at its
1 November handoff, not fabricated in advance. Test counts demonstrate specific
checks; learner explanations and independent exercises remain separate evidence.

## Projects and technology sequence

| Project | Current state | Planned direction |
| --- | --- | --- |
| [OpsDesk](https://github.com/ozdemirr1/opsdesk) | Active product since Week 09; live identity/workspace flow and real Ticket reads | Support-ticket workflow, comments and UI integration; AI summaries/priority/category suggestions in Month 06 |
| DocuMind | Planned; no completed product claimed | Document upload, embeddings, pgvector retrieval and grounded answers in Months 07–08 |
| HireMatch AI | Planned; no completed product claimed | CV/job matching with validated structured output in Month 09 |

Current stack: Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, React,
TypeScript and GitHub Actions. Tailwind is planned for the complete Month 04 UI package in Week 16;
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
