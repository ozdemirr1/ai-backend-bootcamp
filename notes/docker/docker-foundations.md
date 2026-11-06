# Docker foundations

## 4 November 2026 — first exercise

OpsDesk needs a repeatable runtime across development and CI. Its Python venv
isolates Python dependencies; it does not package the Linux userland or isolate
process/network views. An image supplies filesystem layers and startup metadata.
A container is an instance of an image, with runtime configuration and a writable
layer; it can be running or stopped. The main process determines its running
lifetime. On this Mac, Docker Desktop runs Linux containers through a Linux VM.

The first experiment uses Python only. No application files, secrets, database
connections, host directory mounts or published ports are needed. It is a
preparation exercise, not the OpsDesk image or a new learning project.

Before running, predict:

1. Will `platform.system()` report Darwin or Linux? Why?
2. After the Python command finishes, will this container still be running?
3. Does stopping a container remove its image?

```sh
docker run --name week17-python-first python:3.14-slim \
  python -c 'import os, platform; print("system:", platform.system()); print("pid:", os.getpid())'
```

`docker run` creates and starts a container. `--name` gives it a recognizable
name. `python:3.14-slim` identifies the image; Docker will attempt to pull it if
absent locally. The remaining arguments specify the process to execute.
This tag is mutable; it is not
an immutable product-build dependency decision. Pull/network failures must be
distinguished from the Python process failing.

Once it runs, inspect the result:

```sh
docker ps --filter name=week17-python-first
docker ps -a --filter name=week17-python-first
docker logs week17-python-first
docker inspect --format '{{.State.Status}} exit={{.State.ExitCode}}' week17-python-first
```

We deliberately omit `--rm` so the stopped container and its logs remain available
for inspection. Repeating `docker run` with the same name will conflict with that
existing container; use `docker start -a week17-python-first` to rerun it.

After interpreting the successful run, the next controlled failure uses a separate
container running `python -c 'raise RuntimeError("week17 deliberate failure")'`.
Inspect its logs and exit code, identify the application-level cause and compare
with the corrected command. Results are recorded below.

Prediction supplied on 4 November: Furkan expects Linux because Docker Desktop
runs the container on its Linux VM kernel, and Exited (0) after the short Python
main process finishes. The stopped container remains inspectable.

Observation from Furkan's terminal output on 4 November: the image was pulled
successfully, Python printed `system: Linux` and `pid: 1`. The container was absent
from `docker ps`, present in `docker ps -a` as Exited (0), and retained both log
lines. Inspect returned `exited exit=0`. These are learner-supplied execution
results, not a separate mentor rerun. No custom image build was performed.

Learner explanation: Furkan connected the container lifetime to its main process
and explained that Uvicorn keeps serving requests until it exits or fails.
Review: correct; Uvicorn is PID 1 when launched directly, rather than through a
wrapper or init process. A running container alone does not prove API/database
readiness. Prediction and successful execution agree.

Failure and recovery, learner-supplied terminal evidence on 4 November:
`week17-python-failure` logged the deliberate RuntimeError traceback and inspect
returned `exited exit=1`. Furkan correctly located the failure in Python using
the traceback. His replacement command used the same image with
`python -c 'print("recovered")'` in `week17-python-fixed`; output was `recovered`
and inspect returned `exited exit=0`. He then removed only the failure and fixed
containers with `docker rm`. No image removal or broad cleanup was shown.

Review correction: exit 1 alone cannot identify a Python exception; explicit
`sys.exit(1)` also produces it. The traceback establishes the cause here.
Docker documents 125 (Docker-side failure), 126 (command cannot be invoked) and
127 (command not found) as `docker run` CLI exit statuses. Do not conflate that
CLI status with the stored `.State.ExitCode` read by inspect, particularly if
container startup fails. Failure diagnosis and recovery are complete for this
small exercise; this is not an OpsDesk build or product test result.

## HTTP process and published port — 4 November

Furkan ran a detached `week17-http` container from the same Python image with
`-p 127.0.0.1:8087:8000` and
`python -u -m http.server 8000 --bind 0.0.0.0 --directory /tmp`.
Supplied terminal evidence: Up state, the expected port mapping, HTTP 200 with
an empty directory listing, and a matching GET/200 server log. The supplied Docker
Desktop screenshot also shows the HTTP container running and the first Python
container stopped. No host directory was mounted. The HTTP container remains
running at this checkpoint; no stop is claimed.

Learner correctly explained host port 8087 versus container port 8000 and the
long-lived server process. Clarification: `-d` detaches the terminal; it does not
keep a completed process alive. A request-serving loop need not be an asyncio
event loop. The log's peer address alone does not prove the full network route
or gateway configuration. Docker Desktop forwards host connections through its
backend into the Linux VM; see [Desktop networking](https://docs.docker.com/desktop/features/networking/).

Wrong-port exercise completed on learner-supplied output: port 8088 returned curl
exit 7 (connection failed), container remained Up, and before/after log tails
were unchanged. Correct port 8087 then returned HTTP 200. Furkan correctly
distinguished failed connection establishment from an HTTP error or process crash.
Review: the evidence proves connection failure, not an exhaustive inventory of
host listeners or firewall rules. The requested port was wrong; this does not
establish a defect in Docker's configured forwarding. Existing favicon 404 logs
are earlier HTTP responses, not records of the failed 8088 connection.

HTTP status versus client exit code: Furkan predicted that plain curl would exit
0 for a completed HTTP 404 response. His supplied run against
`/week17-missing.txt` returned 404, immediate `echo $?` returned 0, and server logs
recorded the matching GET/404. Prediction and observation agree. HTTP error status
alone does not fail default curl; transfer or local I/O errors can still fail it.
Furkan then confirmed `--fail` returns exit 22 for the missing path and exit 0
with HTML for `/`. His `docker stop week17-http` stopped the container, but the
subsequent listing showed Exited (137). This is not a graceful-shutdown result.
Initial exit 137 alone did not identify the cause. Follow-up learner inspection
showed `oom=false`, empty runtime error and no configured stop signal (default
SIGTERM). A bounded repeat using `docker stop --timeout 3` took 3.235 seconds and
returned exit 137 with OOM false. After restarting the same container,
`docker stop --signal SIGINT --timeout 3` took 0.250 seconds, returned exit 0,
and logged `Keyboard interrupt received, exiting.`

The timing and repeat strongly support SIGTERM timeout followed by forced kill;
no Docker event trace was collected. SIGINT was handled successfully by this
Python HTTP server. The container is now stopped and retained for inspection.
This closes the small shutdown comparison, not OpsDesk's future SIGTERM or
in-flight-request cleanup acceptance. Do not change the product's stop signal
based on a standard-library learning server. All measurements are supplied by
the learner, not independently rerun.

Learner transaction explanation: Furkan described a successful database commit
followed by process termination before the HTTP response reaches the client.
Review: correct. Loss of a response leaves the client uncertain; it does not
prove rollback or commit. Retrying a non-idempotent Ticket POST can create a
duplicate. This connects shutdown behavior to the existing explicit recovery
flow; no HTTP idempotency implementation or guarantee is added.

## Port conflict and name resolution — learner evidence, 4 November

Reusing host 127.0.0.1:8087 produced `port is already allocated` and Docker CLI
exit 125. The attempted container remained Created with no application logs;
the original server still returned HTML. Furkan removed the failed container
and created a second server on host 8088, still using container port 8000.
The immediate curl returned 52 (empty reply), so successful HTTP access through
8088 is not yet verified. A startup/readiness race is a hypothesis, not a proven
cause; the command sequence did not wait for application readiness.

The invalid-name experiment raised socket.gaierror and exited 1. Localhost
resolution returned 127.0.0.1 and ::1; this verifies local name resolution, not
external DNS service health or a listening application. Both HTTP containers
were subsequently stopped by the learner using SIGINT. Next: inspect the second
server state/logs, restart it and check HTTP access after observing startup.

Follow-up learner evidence: the second server's prior stop had exit 0, OOM false
and empty runtime error. After restart and observing its startup log, verbose
curl connected to 8088, received HTTP 200 and exited 0. A timestamped GET/200
matched that request. SIGINT stop then completed. Current access is verified;
the original empty reply remains consistent with a startup race but its cause
was not conclusively established. Ending `docker logs --follow` with Ctrl+C
did not stop the server, as the subsequent HTTP response demonstrates.

First custom learning image built by Furkan: a temporary minimal build context
with `app.py`, a four-instruction Dockerfile (FROM/WORKDIR/COPY/CMD), and an
allowlist `.dockerignore`. Supplied build output confirms creation of
`week17-python-demo:v1`; running its default command printed the learning message
and `working_directory=/app`, then exited 0. The illustration remains outside
the product checkout; it is not the OpsDesk image.

Learner's pasted follow-up transcript confirms the snapshot/cache experiment:
editing app.py did not change v1 output. Building v2 reused WORKDIR but executed
COPY for the changed file; v2 printed the updated message. An unchanged v2 build
then reported both WORKDIR and COPY as CACHED. Runtime manifest/config digests
were unchanged on that repeat, while attestation and top-level manifest-list
digests changed; cache reuse is not a guarantee of identical exported metadata.
Context failure/recovery confirmed by learner output: app.py remained on disk,
but a final exclusion rule made COPY fail with checksum/not-found and build
exit 1. Restoring the ignore rules restored the context; COPY reused cache and
the context-check image printed v2 and /app with exit 0. This demonstrates a
build-input error, not a Python runtime failure or corrupt cache. Next prepared
explanation: RUN versus CMD and overriding the default command for one container.

Learner then verified image configuration `/app` and `["python","-u","app.py"]`.
A one-run command override printed the embedded source file; a subsequent normal
run printed the v2 application output again. The default CMD remained unchanged.
RUN versus CMD was explained, but no separate RUN instruction exercise is claimed.

## Final review received 6 November — 4 November session

Furkan correctly explained immutable image contents versus changed host source,
rebuilding for a new runtime, and bind mounts as a development alternative.
Mounts make file changes visible; they do not automatically reload code already
loaded by the process. A reload mechanism or process restart may still be needed.
No bind-mount execution is claimed.

He correctly separated connection failure from HTTP 404 and default curl exit
status from `--fail` behavior. The expected HTTP logs were observed in this
exercise; access logging can be disabled or handled by a proxy in a real system.
Absence of an access-log entry alone is not universal proof of an unreachable
application, and a proxy can generate a 404 before a request reaches the backend.

His stated key takeaways were that container and curl exit codes belong to
different processes, and that `-d` detaches rather than keeps a process alive.
Review accepted with these clarifications. At his request, no additional repeat
exercise is added; the 4 November learning session is closed.

References: [Docker container concepts](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/),
[docker run and process exit status](https://docs.docker.com/engine/containers/run/).
