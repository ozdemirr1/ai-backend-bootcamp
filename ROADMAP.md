# 12-Month Roadmap

## Target Role

Backend-focused developer building production AI applications, with practical
full-stack capability. Internship and junior backend/full-stack roles remain the
entry targets; this is a career direction, not a current seniority claim.

## Core Focus

Backend + Database + API + Cloud + AI Integration + Basic Frontend

## Monthly Plan

### Month 1
Engineering fundamentals, Git, terminal, Python refresh, HTTP/REST, type hints, pytest basics, Ruff, and dependency management.

### Month 2
FastAPI, PostgreSQL, SQLAlchemy, Alembic, authentication, basic CI, and first backend deployment.

### Month 3
Backend architecture, testing, logging, error handling, authorization/security,
and an early deployed OpsDesk backend preview. Expand meaningful CI coverage and
introduce Linux/network troubleshooting through deployment work. Keep persistence
synchronous; a bounded async HTTP exercise follows lifecycle understanding.

### Month 4
React, TypeScript, frontend integration, and a deployed full-stack demo.

Week 13 (6–11 October): [React foundation plan](weekly-reports/week-13-plan.md),
with a static shell, mock Ticket list, and controlled login/register forms inside
OpsDesk's `frontend/`. Budget 18 active hours within the normal 15–20 hour capacity.
Week 13 did not absorb the remaining Month 03 product backlog. Week 14 delivered
identity integration and in-memory session lifecycle. Missing Ticket reads, Tailwind
and protected-route work remain separately scoped. Deployment of the bounded
identity preview is verified at the 19 October checkpoint below; this does not
complete the full Ticket dashboard or remaining product backlog.

11 October checkpoint: Week 13 technical review passed with 23 frontend tests and
built-bundle browser evidence; product PR #41 merged as 511715d. The
[Week 14 plan](weekly-reports/week-14-plan.md) starts with frontend CI and the existing
registration/login/current-User APIs. Missing Ticket reads remain a separately scoped
dependency. Week 14 includes a hosting decision checkpoint; Week 15 targets a first
hosted identity-flow preview, subject to integration and deployment gates.

18 October checkpoint: Week 14 PR #42 merged normally at b0e6cab, with both
merge-commit CI workflows successful. Furkan selected Railway's one-time USD 5 /
up-to-30-day trial. The [Week 15 plan](weekly-reports/week-15-plan.md) allocates 18
hours to a hosted identity preview and its migration/origin/verification prerequisites.
Credit may run out before 30 days; paid continuation will be decided from actual
usage. Deployment was still unverified at that 18 October decision checkpoint.

19 October checkpoint: React and FastAPI now run on one public Railway origin,
with a separate persistent PostgreSQL service. Public HTML/assets/readiness and
learner browser registration/login/session/logout are verified at product `2f6e00d`.
Local backend regression: 506 passed, 160 deselected. Latest-head Backend and Frontend
CI both passed, rechecked on 19 October; runtime SHA confirmation, operational
checks and weekly merge remain.
The revised Week 15 plan prioritizes scoped tester feedback, abuse controls,
trial usage, backup/restore and rollback. Tickets remain mock data in the UI;
no AI feature is claimed. A LinkedIn draft documents this specific progression.

20 October correction: the original Month 04 sequence was foundations (Week 13),
API integration (Week 14), dashboard (Week 15), and UI polish (Week 16). The live
identity preview is valuable additional evidence but does not satisfy the dashboard
milestone. Week 14's real Ticket list and protected-route goals remain incomplete.
The 19 October operations-heavy schedule therefore needs correction, not a claim
that everything is on the original weekly schedule.

Resume dashboard fundamentals during Week 15: table, status badges, search/filter
and a detail view, with fixture-backed behavior clearly labelled. Scope the missing
real Ticket list/detail backend dependency and Organization context explicitly.
Week 16 combines that integration priority with bounded Tailwind/responsive/
accessibility work; comments and role-aware actions are not promised without their
backend APIs. At handoff, estimate remaining scope and record any spillover before
calling the frontend MVP complete. Operations remain timeboxed follow-up work.
See the [alignment review](notes/react/month-04-alignment.md) for feature-level gaps.
The [Month 03 retrospective](monthly-reports/month-03.md) records carried product
work and the delayed deployment milestone; the preview does not close that backlog.

### Month 5
Docker, Redis, Celery, background jobs. Prefer AWS for cloud learning after checking
cost and project fit; practical IAM, secrets, logs, and budget controls precede any
certification decision.

### Month 6
OpenAI SDK and Responses API, Structured Outputs, and bounded tool calling.
Start versioned evals with the first AI feature, including quality, authorization,
failure behavior, latency, and cost.

### Month 7
RAG fundamentals, embeddings, document upload, and early retrieval/answer evals.
Study MCP as a bounded integration topic after direct tool calling.

### Month 8
pgvector, retrieval/answer evaluation, RAG security, and DocuMind completion.
If capacity permits, evaluate one bounded agent workflow with authorization,
prompt-injection tests, execution limits, and observability. Recheck Agents API
and SDK options at adoption time; beta APIs and multi-agent orchestration are
not required project dependencies.

### Month 9
HireMatch AI project.

### Month 10
Advanced CI/CD, production deployment, monitoring, performance, and security.

### Month 11
Interview preparation, SQL, data structures, open source.

### Month 12
Final CV, LinkedIn, GitHub, project polish, mock interviews, and an intensive application sprint.

## Delivery Milestones

- Month 1: Clean Python learning projects with notes and basic checks
- Month 2: First deployed FastAPI and PostgreSQL API
- Month 3: Deployed OpsDesk backend preview
- Month 4: Deployed OpsDesk full-stack demo
- Month 5: Docker Compose development environment
- Month 6: OpsDesk AI integration, repeatable evaluation baseline, and live demo
- Month 8: DocuMind demo with retrieval evaluation
- Month 9: HireMatch AI MVP
- Month 10: Production engineering improvements
- Month 12: Final portfolio and application sprint

## Career Visibility Milestones

- Week 02: Publish the first learning journey update on LinkedIn
- Month 1: Publish the Python engineering and first-month review
- Month 2: Share the first deployed backend API
- Month 3: Start internship applications and active networking
- Month 4-6: Share product milestones and make an early open-source contribution
- Month 5: Start targeted junior backend applications in Türkiye
- Month 6: Start targeted AI/backend startup applications
- Month 8: Start suitable global internship and remote applications
- Month 12: Complete the final CV, LinkedIn, GitHub, and application sprint

## Monthly Market Reviews

- [September 2026 review](monthly-reports/2026-09-market-review.md), recorded
  17 September: retain the career direction; start evals with the first AI feature
  and make later agent work bounded, measurable, and optional.
- Existing earlier roadmap revisions remain in Git history. The
  [Month 02 report](monthly-reports/month-02.md#roadmap-variance-and-carry-over)
  records that the original Month 02 CI/deployment targets were not completed then.
  Minimal CI subsequently shipped in OpsDesk; deployment remains an evidence-based
  delivery target, not an assumed completed milestone.
- React + TypeScript remains Month 04; Docker/Redis remain Month 05. Do not move
  the learner back to pre-FastAPI fundamentals or switch persistence to async just
  to mirror a market checklist. Frameworks follow direct SDK/API understanding;
  Kubernetes and certifications remain later optional choices.
- Weekly capacity remains 15–20 hours. Security, observability, and evaluation
  accompany features rather than waiting for the final production-engineering month.
