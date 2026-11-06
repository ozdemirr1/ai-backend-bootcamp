# Week 17 — Docker and systems foundations

Teaching preference updated on 4 November: explain and continue through bounded
exercises without a question/checkpoint after each one. Collect learner review
questions at the end of the day. Execution evidence is still required; prepared
commands are not completed work.

4–9 November 2026. In progress; follow the [weekly plan](week-17-plan.md)
and [Month 05 scope](../monthly-plans/month-05.md).

## 4 November — repository and environment baseline

- Read the local bootcamp instructions, tracked handoff, monthly/weekly plans,
  status, roadmap and decisions. Bootcamp AGENTS.md is ignored and untracked.
  No AGENTS.md was found in the product checkout or its ancestor directories;
  the supplied product guardrails and tracked handoff remain applicable.
- Fetched both origins. Bootcamp main matched `8e2408a` (planning PR #14);
  product main matched `f8f42be` (PR #50). Both had zero ahead/behind commits.
  Product working tree was clean; existing untracked LinkedIn milestone assets
  in bootcamp were preserved. Bootcamp notes now use
  `feature/week-17-docker-foundation`; product remains on main without edits.
- Inspected product README, project status, API contract baseline, build manifests,
  Railpack configuration and both CI workflows. No tracked Dockerfile,
  .dockerignore or Compose configuration exists yet.
- Backend: Python 3.14.7, `pyproject.toml` + `uv.lock`, existing `src/opsdesk`.
  Frontend: Node 24, npm lockfile, TypeScript/Vite build. `railpack.json` extends
  the provider build with frontend installation/build and enables FastAPI serving
  `frontend/dist`; the configured frontend API base is the same origin.
- Backend CI: push/PR → Ubuntu → checkout → uv/Python → locked dependencies →
  Ruff lint/format → non-integration pytest. Frontend CI: push/PR → Ubuntu →
  Node 24 → npm ci → tests → build → lint. Both have read-only contents permission
  and a ten-minute job timeout. PostgreSQL and Docker build checks are absent.
- GitHub currently reports successful [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/41490591574)
  and [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/41490591535)
  for `f8f42be`. These are existing runs inspected today, not newly executed tests
  or evidence of independent CI understanding. Hosted runtime was not rechecked.
- Docker CLI 28.5.1 and Compose v2.40.2-desktop.1 were installed. The initial
  daemon connection failed. Starting Docker Desktop made the socket available;
  subsequent sandbox socket denial was resolved by approved access. Engine now
  reports 28.5.1, Linux, aarch64. This distinguishes engine availability from
  tool sandbox permissions; no socket permission change was made.
- Host free disk: approximately 5 GiB. Docker reports five images, one stopped
  container, six local volumes and about 172 MB build cache. Existing resources
  were not started, removed or pruned. Check capacity before larger builds.

## Carry-over reviewed, still open

The Month 04 records retain hosted-export/restore evidence, abuse controls,
provider incident audit/current usage, dependency maintenance and personal learner
reflection as follow-ups. The 2 November npm findings are historical, not a fresh
audit. Q03 PostgreSQL CI is a Week 18 target. Assignment, lifecycle and membership
backlog are not added to this month's implementation scope.

The README's final “Next” paragraph still describes already-delivered Month 04
work; the development guide also contains dated mock-Ticket language. Use current
delivered-boundary evidence; align these passages during the scoped product docs
update without rewriting historical checkpoints.

## First learning checkpoint

Prepared [a small Python-container exercise](../notes/docker/docker-foundations.md).
Purpose: distinguish image, container, main process and venv before writing the
OpsDesk Dockerfile. Learner prediction and conceptual explanation were accepted:
Linux VM kernel, main-process lifetime, successful exit and Uvicorn connection.
Furkan then ran the exercise and supplied terminal evidence: image pull succeeded,
Python printed Linux and PID 1; `docker ps` omitted the completed container while
`docker ps -a` showed Exited (0). Logs retained the output and inspect confirmed
`exited exit=0`. This is learner-supplied evidence, not a separate mentor rerun.
No custom image build or backend/frontend/database test ran.

Furkan supplied the controlled failure output (RuntimeError traceback, exit 1),
identified Python as the source, then independently supplied and ran the corrected
command using the same image (`recovered`, exit 0). He removed only the failure
and fixed containers afterward. Review corrected one overstatement: exit 1 alone
does not prove an exception; the traceback does. Docker CLI startup exit statuses
must also be distinguished from stored container state. This completes the first
small run/log/failure/recovery exercise on learner-supplied evidence.

HTTP follow-up: learner terminal output and Docker Desktop screenshot show
`week17-http` running with host 8087 mapped to container 8000. Curl returned 200
and server logs recorded GET/200. Learner explained process lifetime and port
mapping; review distinguished detachment from lifetime and peer-IP observation
from proof of gateway configuration. HTTP container is still running at the
supplied checkpoint. Wrong-port diagnosis subsequently passed on learner output:
8088 failed with curl exit 7, container stayed Up, log tails were unchanged, and
8087 returned 200 again. Learner distinguished connection failure from HTTP error
and process crash. No listener inventory was performed; absence of a listener is
an explanation rather than independently proven host state.

HTTP/client status distinction: learner correctly predicted plain curl exit 0
despite HTTP 404. Supplied execution returned 404 for `/week17-missing.txt`, exit
0 and a matching GET/404 server log. The learner subsequently verified `--fail`:
404 produced exit 22; `/` returned HTML and exit 0. Stopping `week17-http` yielded
Exited (137). Follow-up inspection showed OOM false, empty runtime error and the
default stop signal. Learner's measured comparison: SIGTERM with a three-second
timeout took 3.235 seconds and exited 137; SIGINT took 0.250 seconds, exited 0
and logged `Keyboard interrupt received, exiting.` This strongly supports stop
timeout escalation in the first case; no event trace was collected. The small
shutdown comparison is complete; product SIGTERM acceptance remains separate.
The exercise container is stopped and retained.
Port collision, DNS and broader weekly gates are not completed
by these exercises.

Learner shutdown explanation accepted: Furkan explained commit succeeding before
process termination prevents the HTTP response from reaching the client. Review
emphasized uncertain write outcomes and duplicate risk from automatic POST retry.
The 4 November baseline and first small Docker learning checkpoint are complete;
this does not complete Week 17 or implement the product image.

Subsequent learner evidence: host-port collision produced Docker exit 125 and
a Created container with empty logs, while the original server kept responding.
The failed container was removed; the second server was created on host 8088,
but immediate curl returned 52 (empty reply). Its successful HTTP response is
still unverified; startup timing is only a hypothesis. Invalid-name resolution
failed with socket.gaierror/exit 1; localhost resolved to IPv4/IPv6 loopback.
Both HTTP containers were then stopped with SIGINT. These are learner-supplied
results; no product implementation or external DNS-health proof is claimed.

Follow-up: learner restarted the second server, observed startup, ended log
following and obtained verbose HTTP 200, curl exit 0 and a matching GET/200 log
on port 8088. Then stopped it with SIGINT. Current access is verified; the initial
empty reply's exact cause remains unproven. The next tiny Dockerfile illustration
is prepared, not built, before the separate basic OpsDesk image.

Subsequently Furkan built `week17-python-demo:v1` from a small temporary context
with app.py, FROM/WORKDIR/COPY/CMD and an allowlist .dockerignore. Default-command
execution printed the expected message and `/app`, with exit 0. This is a custom
learning image only; the product Dockerfile remains unimplemented.

Source snapshot/cache exercise passed on learner transcript: v1 retained its
original output after the host file changed; v2 built and printed the new text.
WORKDIR was cached on the changed build, and both WORKDIR/COPY were cached on
an unchanged repeat. No product Dockerfile or product build is claimed.

Context exclusion experiment passed on learner evidence: COPY failed with
not-found/build exit 1 despite the file existing on the host. Restoring ignore
rules allowed cached COPY, successful build and v2 runtime output with exit 0.

Command-default check passed: image inspect showed /app and the Python CMD;
a one-run override printed source, and the following normal run used the original
CMD. The 4 November planned baseline and initial learning work are complete;
some later-day foundations were brought forward. Day-end learner review and
documentation/commit closure remain, not another product implementation block.
Estimated remaining closure effort: 10–15 minutes, not measured work time.

Next session: reconcile remaining weekly fundamentals and begin the bounded basic
product image when its prerequisites are covered, before multi-stage work.
No new daily report, commit, push,
PR, deployment or product implementation is claimed.

## 6 November — review and closure of the 4 November session

Furkan supplied the end-of-day review on 6 November and explicitly requested
closing the 4 November program without another experiment. Preserve the exercise
dates above; this review does not claim 5 November work or completion of the
scheduled 6 November product implementation.

- Image/source: correctly explained the build-time snapshot, rebuilding and
  starting a container from the new image. Also described a development bind
  mount. Clarification: changed files become visible through the mount, but the
  running application may need reload/restart; no bind-mount exercise was run.
- Diagnosis: correctly separated TCP connection failure from HTTP 404 and
  explained default curl versus `--fail`. Access-log expectations are correct
  for the exercised server; in general, logging configuration and proxies must
  be considered. A 404 need not originate in the intended backend process.
- Reflection: identified container exit code versus curl exit code, and detach
  versus main-process lifetime, as the most important distinctions. No claim
  is made that he selected or completed a further independent repeat exercise.

The 4 November baseline and bounded learning session are closed. Remaining
Week 17 work includes product dependency/config boundaries, basic product image,
then multi-stage/non-root/runtime acceptance and full GitHub Actions teaching.
Broader Linux/networking/HTTP-TLS coverage must be reconciled with the plan;
the small exercises do not automatically close every weekly learning gate.

Closure is limited to the weekly report, Docker topic note and current status
on `feature/week-17-docker-foundation`. Whitespace checks passed. No product
test rerun was needed for these documentation changes. Product working tree
was checked clean on main; unrelated untracked LinkedIn assets were preserved.
No new daily report, push, PR, merge or deployment is part of this closure.

## 6 November — continuation of the 5 November systems plan

The prior closure was pushed as `c908860` to the weekly feature branch after the
learner requested publication. This continuation preserves that same branch.

Environment comparison: learner screenshot showed macOS/Darwin, Python 3.14.7,
venv true and FastAPI discoverable in the product venv. The container command
initially stalled. An approved read-only Docker version probe also timed out
after ten seconds; this was not evidence of a Python application failure.
Subsequent learner output showed both Docker client (Darwin/ARM64) and server
(Linux/ARM64), then a successful `container ready` run. Exact recovery action
and root cause were not supplied, so neither is asserted.

The repeated base-image comparison returned Linux, Python 3.14.10, venv false
and FastAPI unavailable. This confirms separate dependency environments and
version drift between the mutable image tag and product interpreter. No product
dependency was installed or changed. Do not copy the Mac venv into the Linux
image; construct the target environment from dependency definitions and lockfile.
The venv/container comparison is complete.

TLS learner evidence: example.com resolved, TCP connected on 443, TLS 1.3 was
negotiated, hostname matched the certificate, verification succeeded, and HTTP/2
returned 200 with curl exit 0. Local plain HTTP on 8087 returned HTML. Sending
HTTPS to the same plain-HTTP server connected TCP but failed the TLS handshake
with curl 35; the server logged binary request syntax and HTTP 400. This is a
protocol mismatch, not proof that a TLS-capable server needs a version downgrade
or disabled certificate validation. No -k was used. Learner stopped the server
with SIGINT afterward. These results are not a fresh OpsDesk hosted smoke test.

Product mapping reviewed from existing development docs: FastAPI serves the
React build and API on one origin; readiness checks SELECT 1, not all schema
privileges. Railway's official edge documentation describes TLS termination at
its edge before forwarding to the deployment. No provider configuration or
database TLS setting was changed.

Final review supplied on 6 November:
- Correct central explanation: host FastAPI installation is not automatically
  available in the container. Corrections: container isolation is not absolute
  or equivalent to a separate guest VM; Linux containers share their host kernel
  (the Docker Desktop VM's kernel here). A base Python image is not guaranteed
  to contain only the standard library; the observed fact is FastAPI absence.
  Copying or mounting files also does not automatically make packages importable
  or compatible with the container's OS/interpreter.
- Learner understood why certificate verification should not be casually
  disabled, but incorrectly stated -k would establish the connection in this
  protocol-mismatch case. Corrected explicitly: -k skips certificate verification;
  it does not add TLS to a plain-HTTP server or fix protocol negotiation.
  No revised independent learner answer or -k experiment is claimed.

The 5 November planned systems session was completed on 6 November with the
review corrections above; this is not an assertion that both original answers
were fully correct. No additional exercise is required for this session closure.
Next: bounded basic OpsDesk image and locked dependency/config boundaries, before
multi-stage work. GitHub Actions foundations remain required. Documentation-only
closure uses the same weekly branch and preserves unrelated LinkedIn assets;
no product test rerun, PR, merge or deployment is included.
