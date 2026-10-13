# Week 14 Report — In Progress

## Scope and dates

12–18 October 2026, Month 04. Follow the [Week 14 plan](week-14-plan.md).
Core outcome: frontend CI and real registration/login/current-User integration.
Optional Organization reads follow the core gates; Ticket reads and public hosting
remain explicitly tracked dependencies/deliverables, not assumed completed work.

## 12 October opening

- Learner chose to start Monday. Move Tuesday's 3-hour CI package forward, retain
  Tuesday as optional rest/catch-up, and keep the weekly estimate at 18 hours.
- Local inspection confirms clean OpsDesk main at 511715d, the merged Week 13
  foundation. Bootcamp head is 1bdca71; two acknowledged uncommitted changes record
  the squash lesson and preference for normal merges. Preserve and include them in
  today's documentation package. No fresh remote fetch or test rerun at opening.
- Existing Backend CI has no frontend steps. Reviewed the frontend lockfile engines
  and official setup-node/run-default/Node release docs; Node 24 LTS is the selected
  hosted runtime. Local Node 25.2.1 differs and is EOL; local alignment is planned
  before integration, and actual hosted Node 24 evidence is required for this package.
- Learner exercise: separate Frontend CI workflow with checkout, Node setup, npm
  package caching, lockfile installation, tests, build, and lint in frontend/.
  No new product feature or dependency required. Branch creation, workflow writing,
  local checks, README updates, hosted evidence, and daily Git closure remain pending.
- Weekly merge strategy is normal merge (--merge), preserving daily commits.

## 12 October workflow review and local checks

- Learner updated main and created feature/week-14-api-integration, then implemented
  .github/workflows/frontend-ci.yml. Review confirms push/pull_request triggers,
  contents: read, a single Ubuntu frontend-checks job with a ten-minute timeout,
  frontend run defaults, checkout without persisted credentials, Node 24 and npm
  package caching using the correct repository-relative lockfile path.
- Separate install/test/build/lint steps are correct; Backend CI and package files
  are unchanged. No blocking issue found in the workflow source review.
- Learner's 11:50 terminal evidence: npm ci installed 245 packages and reported no
  audit findings in that run; 23 frontend tests passed, build and lint succeeded,
  and tracked diff whitespace check was silent. These are local Node 25 results;
  hosted Node 24 success has not yet been established.
- Mentor updated product/frontend READMEs with the workflow, runtime, caching,
  command-directory behavior, and explicit hosted-evidence boundary. No source
  behavior changed, so the passing test suite was not rerun for documentation edits.
- Remaining: product commit/push, Frontend CI inspection at its exact SHA, learner's
  cache-versus-install explanation, and final bootcamp documentation commit/push.
  Do not open/merge the weekly PR just to close the first daily package.

## 12 October hosted verification and learning review

- Learner committed/pushed `da695c09bdbeafbc4edb9b9c1041a1b206e654f2`,
  week-14: add frontend CI checks. Local read-only inspection confirms that head
  and a clean product working tree on feature/week-14-api-integration.
- GitHub read-only lookup confirms both runs completed successfully at that SHA:
  [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/38226432895) and
  [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/38226432836).
- Frontend log inspection confirms Node 24.21.0/npm 11.19.0, lockfile installation,
  23 tests across four files, successful TypeScript/Vite build, and ESLint. The first
  run missed the npm cache and saved it at completion; no cache-hit run is claimed.
- Learner correctly distinguishes cached package data from an installed node_modules
  tree. Refined the claim that cache eliminates network traffic: entries can be
  missing, so downloads may still be needed. npm ci remains the installation step.
- Monday's technical/learning package is complete. Remaining daily step is bootcamp
  documentation commit/push with clean-status evidence, including the carried-over
  merge-strategy notes. No weekly PR or merge is required today; --merge remains the
  agreed weekly strategy. Next planned implementation package is Wednesday's request
  boundary/configuration exercise; Tuesday remains optional rest/catch-up.
- Local runtime alignment from Node 25 to Node 24 remains an explicit prerequisite
  before API integration; hosted success does not itself change the learner's machine.

## 12 October Git closure

- Learner supplied bootcamp commit/push 1979854 and clean short status. Product
  da695c0 and both successful hosted runs are recorded above. Monday is closed.

## 13 October opening and runtime checkpoint

- Learner chose to continue Tuesday. Move Wednesday's 3-hour package forward and
  reserve Wednesday as optional rest/catch-up; keep the weekly estimate unchanged.
- Local inspection confirms clean bootcamp at 1979854 and clean product at da695c0
  on feature/week-14-api-integration. No fetch or test run at this opening.
- Node resolves through Homebrew to Cellar/node/25.2.1; the inspected node@24 opt
  executable is absent. Prepared learner install/temporary PATH selection commands
  using Homebrew's official node@24 formula. Runtime installation/verification and
  Node 24 local checks remain pending; no machine setting was changed by the mentor.
- Inspected existing backend error envelope and Vite test setup for the upcoming
  request boundary exercise. Teach fetch with an analogous example after the runtime
  checkpoint, before learner implementation. Forms remain demos at this stage.

## 13 October runtime recovery and verification

- Repeated learner installation attempts failed while Homebrew tried to install/link
  OpenSSL 4 and reported an OpenSSL 3 lock. OpenSSL 4 was already installed but not
  linked; repeating installation alone did not resolve it.
- At the learner's request to resolve the blocker directly, mentor completed
  `brew link openssl@4` with system approval. Homebrew switched the OpenSSL command
  links from version 3 to version 4; the version 3 installation was not removed.
  Subsequent Node 24 installation completed with its required dependency upgrades.
- Mentor verified Node 24.21.0/npm 11.19.0, ran npm ci and confirmed 23 tests across
  four files, production build, lint and git diff --check all passed. npm emitted
  an install-script approval warning for fsevents; no extra script approval was
  granted and the checks still passed.
- After backing up the existing shell configuration, mentor added Node 24 PATH
  selection and verified it in a fresh login/interactive shell. Existing open
  learner terminals still need a reload or a new terminal window.
- Runtime checkpoint is complete; API boundary exercise and today's Git closure
  remain pending. No API integration or new product feature is claimed here.

## 13 October learner checkpoint and first API exercise

- Learner reloaded the shell configuration and supplied Node v24.21.0 evidence.
- First bounded exercise issued: API error envelope guard and safe message mapping,
  with unknown input, explicit runtime validation and focused unit tests. A small
  analogous type-guard example precedes implementation; learner owns source/tests.
- Next steps remain public API configuration/local proxy, fetch HTTP/network error
  separation and response guards. No exercise completion or real API call is claimed.

## 13 October API error boundary review

- Learner implemented api/errors.ts and nine behavior tests. Mentor source review
  confirms unknown-input validation, null/array rejection, required string fields,
  details array/string-valued record checks and fixed safe messages for known codes.
  Unknown/malformed payloads fall back without displaying arbitrary server messages.
- No blocking issue found for decoded JSON inputs. Minor comment precision: the
  isRecord helper excludes null/arrays but does not guarantee a plain-object prototype.
- Learner supplied 32 passing tests across five files, successful build and lint,
  and silent git diff --check. These are learner-run checks, not a new mentor run.
  The new API files are untracked, so ordinary git diff --check does not cover them;
  repeat the staged whitespace check before commit.
- Runtime typeof-object learning answer remains pending. Next exercise: public API
  base configuration and Vite local proxy; real fetch/form wiring is not yet present.

## 13 October configuration review and learning answer

- Learner's object-check explanation is correct: typeof includes null and arrays
  and does not validate required nested properties. The helper comment now accurately
  describes a non-null, non-array object check rather than a plain-prototype check.
- Reviewed Vite proxy: /api forwards to the local backend on port 8000 and removes
  the prefix. Public configuration uses VITE_API_BASE_URL with /api fallback.
  .env.example contains the public prefix; git check-ignore confirms .env.local
  is ignored. No private environment contents were read for this review.
- Learner supplied 32 passing tests, build/lint success and silent whitespace check.
  These do not establish a successful real browser request through the proxy.
- Next bounded exercise issued: requestJson returning a discriminated result union,
  unknown success data, HTTP status preservation, safe error messages, JSON decoding
  failures and fetch/network failures; focused fetch-mocked tests. No form wiring yet.

## 13 October request client review — corrections pending

- Learner supplied 39 passing tests and a successful build. Lint failed at the
  initial errorData=null assignment, which is overwritten in both try/catch paths.
  Requested removal of the redundant initializer rather than disabling the rule.
- Source review found an uncovered cancellation path: response.json() can reject
  with AbortError after fetch resolves. Both body-read catch blocks currently
  misclassify it. Requested shared abort detection and two focused regression cases
  (successful and unsuccessful HTTP responses whose body reading is aborted).
- Learning refinement: a fetch network error does not prove the request never
  reached/changed the server; CORS or response loss can hide a completed request.
  Avoid automatic registration retries. A login 401 means invalid credentials;
  a current-session protected-request 401 requires session handling by its owner,
  not unconditional navigation from the generic HTTP client.
- Request client approval, corrected lint/test evidence and actual local proxy
  verification remain pending. No real identity integration is claimed.

## 13 October request client correction review

- Learner supplied 41 passing tests across six files plus successful build/lint and
  a silent whitespace check. Source confirms redundant initializer removal and
  AbortError classification in fetch and both body-reading paths.
- Follow-up review found the two new abort tests outside the describe block that
  owns afterEach(vi.unstubAllGlobals). Requested moving those tests into the block
  so their global fetch mocks are also cleaned up. Passing counts alone do not
  establish test isolation. Final rerun and real local proxy check remain pending.

## 13 October request client local acceptance

- Source review confirms both new body-abort tests now belong to the describe block
  containing global mock cleanup. Learner reran all 41 tests and lint successfully;
  whitespace check was silent. Earlier production build passed before this test-only
  placement change. Request helper is accepted for the bounded JSON exercise.
- Issued real local verification through the Vite browser origin: import the client
  module in development and call requestJson('/users/me') without credentials. Expect
  HTTP 401/unauthenticated from the backend and the safe client result. This verifies
  proxy and error transport only, not a successful authenticated identity flow.
  Actual browser result and documentation/Git closure remain pending.

## 13 October real local proxy evidence and publication checkpoint

- Learner initially hit a missing JWT secret at backend startup. Explained that the
  reloader starting is not application readiness and shell exports are terminal-
  scoped. Learner supplied development settings for the product database, entered
  the existing database password privately and generated a local JWT secret without
  printing it. Screenshot confirms Application startup complete.
- Vite screenshot confirms localhost:5173. Safari console rejected the top-level
  await snippet before any request; the equivalent dynamic-import promise chain
  ran successfully. No source change was needed for that console syntax issue.
- Learner screenshot shows /api/users/me returned 401 and requestJson produced:
  ok=false, kind=http, status=401, and the fixed authentication message. Backend
  request_finished evidence confirms GET /users/me, status_code=401,
  response_started=true and unexpected_error=false. This is real browser/proxy/API
  evidence for an unauthenticated read, not a mocked request.
- The console's fulfilled Promise with undefined is the return from the logging
  chain; the separately logged ApiResult carries the HTTP outcome. Red HTTP 401 is
  expected here. No accounts, tokens, or database writes were created by the probe.
- No successful DB connection, authenticated current User, registration, login,
  production networking or deployment is claimed. Forms and Tickets remain demos;
  endpoint-specific success guards and identity form wiring are later packages.
- Mentor updated both product READMEs and bootcamp notes/status/plan/report. Local
  exercise is accepted: 41 tests, build/lint, learning review and browser probe.
  Remaining daily closure: learner product commit/push, exact-SHA Frontend/Backend CI
  verification, then bootcamp documentation commit/push. No weekly merge today.

## 13 October product publication and hosted verification

- Learner committed/pushed `2b7da04c49f25aa060a5c80fbe591de6550ca973`,
  week-14: add API request boundary and local proxy. Staged whitespace check was
  silent. Mentor read-only inspection confirms that local HEAD and a clean product
  working tree on feature/week-14-api-integration.
- GitHub reports both workflows completed successfully at that exact SHA:
  [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/38414908289) and
  [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/38414908140).
- Frontend logs confirm Node 24.21.0/npm 11.19.0, npm package cache restored,
  dependency installation succeeded, 41 tests across six files passed, and build
  and lint succeeded. Unlike Monday's cache miss, this run supplies actual cache-hit
  evidence; npm ci still ran afterward.
- Tuesday's technical, learning and product-publication checkpoints are complete.
  Remaining daily closure is bootcamp documentation commit/push and clean status.
  Keep the weekly feature branch open; normal merge is still the Sunday strategy.
  Wednesday is optional rest/catch-up; the next core feature is real registration.
