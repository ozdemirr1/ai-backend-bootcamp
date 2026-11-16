# Week 17 plan — Docker and system fundamentals

4–9 November 2026. Planning status: not implemented. The [Month 5 agreement](../monthly-plans/month-05.md) is the authoritative source for scope and safety boundaries.

10 November closure note: the status above describes the initial plan. Technical
learning, build/runtime and CI evidence is recorded in the [Week 17 report](week-17.md).
The verification planned for 9 November took place on 10 November. PR/merge/release
status is tracked separately in the report. The initial checklist below must not
be treated as a retrospective record of results.

## Learning and implementation method

Follow concept → small example → OpsDesk implementation → controlled failure →
test → learner explanation. Do not skip GitHub Actions fundamentals because CI
already exists. The daily table sets the initial sequence; do not start dependent
work before the learning checkpoint is passed.

## Daily work

| Day | Work | Expected evidence |
| --- | --- | --- |
| 4 November | Inspect the existing image/build/CI setup; check disk space and Docker availability; record carried-over risks. | Architecture boundaries and baseline; no source-code relocation. |
| 5 November | Learn processes, PIDs, ports, DNS, HTTP/TLS and the venv/container distinction through a small example. | Diagnosis of a port conflict and a DNS failure. |
| 6 November | Start with a basic backend image: Dockerfile, layers, build context, .dockerignore and docker build/run. Then inspect locked dependencies. | Image builds without secrets or test data. |
| 7 November | Node build → Python runtime multi-stage build; layer cache, non-root execution, existing React dist copy and health smoke checks. | Existing UI/API works without new React code. |
| 8 November | Learn GitHub Actions workflow/event/runner/job/step; inspect existing YAML; add a Docker build job; deliberately break it and fix it using logs. | Ruff/pytest/Docker build results and a failed-build experiment. |
| 9 November | Container logs/SIGTERM shutdown; README setup; independent build/run repetition and weekly review. | PR/CI and Week 17 report; Week 18 configuration decision. |

## Tests and acceptance

- [ ] docker build; container health; non-root execution; safe missing-config failure; SIGTERM shutdown; verification that the image contains no secrets
- [ ] Preserve relevant regression checks, Ruff and existing frontend CI.
- [ ] Do not run destructive tests against local development or hosted data.
- [ ] The learner can explain the code's failure and data boundaries.

## Learning evidence

- [ ] The learner repeats a small implementation step and explains its rationale.
- [ ] A controlled application/CI failure is diagnosed from logs and corrected.
- [ ] Notes distinguish predictions, observed results and lessons learned.
- [ ] How do workflows, jobs and steps differ? How does a command’s exit code affect the CI result?

Planned topic notes: notes/docker/docker-foundations.md; notes/ci/github-actions-foundations.md. This plan does not claim that these notes are complete.

## Notes and closure

Keep weekly concept notes organized by topic under `notes/`; create the Week 17
report when actual work begins. Do not create separate daily reports.
`feature/week-17-docker-foundation` is the suggested feature branch name;
this plan does not create the branch. Use small, meaningful commits, review and
normal PR merges. Record test counts, durations and release results only after
execution.

## Learning questions

- Why is Docker not a venv?
- How does EXPOSE differ from publishing a port?
- Which machine does localhost refer to inside a container?

Reassess remaining work and capacity midway through the week. Starting the next
week requires verification of this week's dependencies; the schedule does not
take precedence over safe testing.
