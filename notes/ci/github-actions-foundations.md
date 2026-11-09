# GitHub Actions foundations

## 9 November 2026 — scheduled 8 November learning

Workflow defines the automation; events trigger it; jobs execute on runners;
steps run commands (`run`) or actions (`uses`). Ordinary steps within a job run
sequentially. Independent workflows do not automatically fail together.

OpsDesk backend workflow installs uv/Python, syncs locked dependencies, checks
Ruff and runs non-integration tests. Frontend workflow installs Node 24 and runs
npm ci, tests, build and lint. Existing green checks alone do not prove mastery.

Prediction: exit 1 fails the demonstration step and skips the following ordinary
step; changing it to exit 0 allows that step to run.

Observed and independently checked through GitHub job metadata:
- Commit 2c59021: [failure run](https://github.com/ozdemirr1/opsdesk/actions/runs/42682092503),
  Successful command passed, Deliberate failure failed, Following step skipped.
- Commit d9eb142: [recovery run](https://github.com/ozdemirr1/opsdesk/actions/runs/42682612638),
  all three demonstration steps passed. Only exit 1 changed to exit 0.
- Backend CI and Frontend CI passed on both commits.

Lesson: a step name or printed word such as "failure" does not determine its
result; process exit status does. The failing demonstration did not cancel the
separate backend/frontend workflows. The branch and paths filters both constrain
the example workflow. It does not check out code because it only runs shell text.

The learner's repeated creation command was blocked by noclobber (file exists);
that protected the file. The subsequent editor change and Git diff show recovery.
Docker build CI and its deliberate failure exercise remain pending. Final learner
explanation is reserved for the session closure, not inferred from green checks.

## Docker build CI and controlled artifact failure

Docker CI was added at a35af07 with checkout followed by docker build on
ubuntu-latest, a 20-minute timeout and contents:read permissions. It builds on
push/pull_request without publishing an image, running a container or accessing
a database. [Initial build](https://github.com/ozdemirr1/opsdesk/actions/runs/42683580921)
passed.

At f294911, the learner changed only the source of COPY --from to
/frontend/dist-missing. [Failed run](https://github.com/ozdemirr1/opsdesk/actions/runs/42684285925)
logs show frontend build DONE, followed by runtime COPY failure at Dockerfile:28:
the source path was not found during checksum calculation; process exit 1.
The Ubuntu runner migration notice was informational, not the failure cause.

Restoring /frontend/dist at 67500f2 produced a successful
[Docker run](https://github.com/ozdemirr1/opsdesk/actions/runs/42684862264).
Backend run 42684862267 and frontend run 42684862697 also completed successfully.
Results and failing log were independently checked via GitHub CLI. The product
working tree was clean after the learner pushed the recovery. Final learner
explanation and documentation closure remain pending; no deployment is claimed.

Final review supplied: learner correctly separated frontend/build packaging scope
and deployment/runtime connectivity. Corrections: Frontend CI and Docker CI are
workflow names; their jobs are frontend-checks and docker-build. Current Docker CI
only builds; it does not run separate tests or validate runtime USER permissions.
Static/runtime test success cannot be inferred from its green status. In general
a build can access external services, but this workflow supplies no DB credentials
and makes no DB check. No independent restatement after correction is claimed.
Planned 8 November learning slice closed on 9 November.
