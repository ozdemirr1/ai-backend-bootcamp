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

## 13 October Git closure and 14 October rest

- Learner supplied bootcamp f7a1d3c push to main and clean status. Tuesday is closed;
  product 2b7da04 and hosted checks are recorded above. No weekly merge occurred.
- Learner reports taking 14 October off, matching the optional rest/catch-up day.
  No work or actual working-time estimate is attributed to that date.

## 15 October opening — real registration

- Local read-only inspection confirms clean bootcamp main at f7a1d3c and clean
  OpsDesk feature/week-14-api-integration at 2b7da04. No fresh fetch/test run at opening.
- Keep the planned three-hour Thursday package and existing weekly branch. Review
  confirms POST /users accepts only email/password and returns 201 with user_id,
  email and is_active. Email canonicalization and NFC/15–128-code-point password
  policy remain server-authoritative. No additional symbol rule is invented.
- Architecture: RegisterForm owns inputs/submission state; an identity API module
  constructs the explicit payload and validates successful response shape/status;
  requestJson owns transport. Registration does not create a frontend login session.
- First learner exercise: UserProfile type/guard plus registerUser adapter and
  focused mocked-fetch tests. Guard rejects unsafe numeric identifiers rather than
  accepting rounded IDs; the wider backend bigint contract remains a known boundary.
- Subsequent work: form validation/loading/duplicate-submission handling, accurate
  mixed demo/real labels, component tests, browser success/conflict evidence against
  the development database and documentation/Git closure. No implementation or
  real registration success is claimed at opening.

## 15 October identity adapter review

- Learner implemented UserProfile, isUserProfile and registerUser; supplied 54 tests
  across seven files, successful build/lint and silent tracked whitespace check.
- Source review confirms positive safe integer IDs, required profile field types
  (including valid false), exact 201 success, explicit email/password serialization,
  AbortSignal forwarding and preserved transport failures. No blocking source issue.
- Suggested removing an unnecessary as-unknown-as cast from the extra-field test:
  structural typing already permits passing a variable with additional fields. Mock
  fixtures do not prove backend password-policy acceptance.
- Learning answer correctly rejects unvalidated success data. Refined its scope:
  a malformed response can follow a committed account; neither guard success nor
  failure independently verifies database state. Registration does not auto-login.
- Next learner exercise: wire RegisterForm, bounded server-aligned validation,
  immediate duplicate-submit gate, disabled pending controls, cancellation/unmount
  ownership, honest success/uncertain-outcome messaging and updated UI tests/labels.
  No real registration browser evidence or form completion is claimed yet.

## 15 October connected form review — fixes pending

- Learner supplied 54 passing tests and successful production build, but lint failed
  on an ASCII-range regex containing a control-character escape. Reviewed actual
  RegisterForm, replacement tests, App changes and the committed baseline.
- The pasted old source is RegisterForm.test.tsx, not the component. Replacing demo
  success expectations with mocked registration is appropriate; unchanged test count
  does not prove all previous behavior coverage was retained.
- Requested character-code ASCII validation instead of disabling lint; clear stale
  feedback when a validated request begins; reset mock implementations between tests.
- Coverage gaps identified: the combined email case omits malformed ASCII input;
  the network/invalid_response case exercises network only; unmount test checks
  abort but does not await late resolution or verify a fresh form. Restore meaningful
  Enter submission and feedback-clear assertions from the earlier tests.
- Registration response, disabled pending inputs, controller identity checks,
  NFC/code-point validation and safe uncertain-outcome handling are present. No
  real registration browser evidence or final acceptance is claimed yet.

## 15 October mentor-applied form repair

- Learner expanded form coverage to 25 tests and requested direct repair after a
  retry-feedback regression failed and the original ASCII-regex lint error remained.
- With filesystem approval, mentor changed only RegisterForm.tsx: replaced the
  control-character regex with an ASCII character-code check and added
  setFeedback(null) when a validated request begins. Preserved learner test changes.
- Mentor ran the full frontend sequence on Node 24: all 68 tests across seven files,
  production build, lint and tracked diff whitespace check passed. No test disabling
  or lint suppression was introduced. Real browser registration/conflict evidence
  and product README/Git closure still remain pending.

## 15 October real registration blocker — missing development schema

- Learner browser screenshot shows POST registration returning internal_error and
  the frontend generic HTTP error. No successful account creation is established.
- Read-only local inspection confirms PostgreSQL is listening, and a local admin
  connection to opsdesk_product_dev finds no application tables or alembic_version.
  This is a confirmed blocker, not proof that credentials have also been validated.
- Existing migrations/env.py online mode intentionally uses guarded test settings.
  Mentor did not weaken that guard or point destructive tests at development data.
- Generated and inspected offline Alembic SQL for both existing revisions up to
  31be9023cfb2. Prepared a temporary transactional script requiring the exact local
  development DB, application role, host/port and empty schema before DDL. No database
  changes have been made by these diagnostic steps. Learner application and subsequent
  real browser registration/conflict evidence remain pending.
- This exposes a missed development provisioning step: prior token-free 401 checks
  did not access the DB. Document a repeatable development migration workflow before
  closing this package; retain the separate destructive-test guard.

## 15 October development database setup completed

- At the learner's request, completed the missing development migration workflow
  before continuing browser registration. Existing roles/databases were retained;
  no bootstrap rerun, password reset, manual table creation or destructive dev test.
- Added explicit `alembic -x target=development` selection. Default online commands
  still use the guarded product test target. Development requires the exact local
  DB, application role, host and port, then checks actual connection identity before
  selecting public schema and running DDL in one transaction. Errors close the engine
  and database-operation failures keep connection details out of the public message.
- Migration-only settings can omit the password to use existing libpq authentication;
  server authentication rules were not changed. Runtime DatabaseSettings still
  requires a password. Successful local connections do not prove password checking.
- Initial real run stopped before DDL because inet_server_addr()::text included /32.
  Corrected the query to host(inet_server_addr()), reran 27 focused migration tests,
  and successfully applied 6a3066cd5538 followed by 31be9023cfb2.
- Real verification: current reports 31be9023cfb2 (head); repeated upgrade runs no
  revisions; check reports no new upgrade operations. Users, organizations,
  organization_memberships, tickets and alembic_version belong to opsdesk_product_app.
  Users count was zero. App role lacks superuser/CREATEDB/CREATEROLE/BYPASSRLS and
  CONNECT to opsdesk_product_test. No existing rows were deleted.
- Full backend regression before the final address-query correction: 455 passed,
  160 deliberately skipped database/schema tests. Focused tests and real migration
  checks passed after the correction; final Ruff/format/whitespace checks passed.
- Product README includes the development setup and repeatable upgrade/current/check
  commands. The temporary offline SQL scripts were not applied; the maintained
  Alembic path performed the setup. Real browser registration 201 and duplicate-email
  409, daily publication and hosted CI remain pending.

## 15 October Safari registration evidence

- Learner screenshots after development migration show a public profile containing
  user_id=1, the synthetic email and is_active=true, together with `Account created.
  You are not signed in.` Email is retained and both password fields are empty.
- Repeating registration shows error.code=email_already_exists and `An account with
  this email already exists.` The form is usable again and no success is claimed.
- Screenshots display response previews, not HTTP status headers. Source review
  confirms the registration adapter only accepts 201 plus a valid profile. The
  duplicate-email backend contract is 409; direct status-header evidence is not
  visible in these images. No additional account was created by the mentor.
- Local browser success/conflict behavior is now demonstrated after the schema fix.
  This does not establish login/session integration or hosted deployment. Product
  READMEs now describe real registration, remaining demos, 68 local frontend tests,
  setup requirements and the evidence limits. Product/bootcamp commit and push,
  staged whitespace review and exact-SHA hosted CI remain outstanding.

## Thursday publication and Friday opening

- Learner supplied backend logs confirming POST /users 201 and 409, both with
  unexpected_error=false. This completes the previously missing HTTP-status evidence.
- Product ea6f6f49a7981552d468fc281f640f35a4ac988d was committed/pushed; Frontend CI
  https://github.com/ozdemirr1/opsdesk/actions/runs/38753920743 and Backend CI
  https://github.com/ozdemirr1/opsdesk/actions/runs/38753920720 both passed at that SHA.
  Bootcamp publication e75cdf3 and clean working trees were verified on 15 October.
- Learner psql output confirmed the persisted synthetic User, all five public tables
  and revision 31be9023cfb2. pgAdmin was installed and connection instructions supplied;
  no completed pgAdmin query is claimed without further evidence.
- 16 October opening: clean product ea6f6f4 on the existing weekly branch. Plan
  login/current-user adapters, connected form and in-memory session with tests.
  Budget remains 3 hours, estimated 3–4 with debugging, not a measured time record.

## 16 October login/current-user adapter review

- Learner implemented AccessTokenResponse guard, loginUser and getCurrentUser in
  the existing identity module. Source review found no blocking implementation
  defect: explicit email/password payload, exact 200 checks, runtime response guards,
  bearer header, AbortSignal forwarding and preserved client errors are present.
- Mentor ran the complete frontend sequence on Node 24.21.0: 82 tests across seven
  files passed, production build/lint and tracked whitespace checks passed.
- Before form wiring, requested bounded coverage additions: getCurrentUser must
  reject a valid profile under an unexpected successful status; both adapters should
  demonstrate network and abort result propagation, beyond signal-forwarding tests.
  Token guard wrong-type fixtures can extend the existing guard test.
- isUserProfile deliberately accepts a boolean false. Session wiring must separately
  require an active current User before displaying an authenticated state. No real
  login/session or browser verification is claimed at this adapter checkpoint.

## 16 October connected login and final local review

- At the learner's request, added the six bounded adapter cases: numeric token
  rejection, current-user wrong successful status, and network/abort propagation
  for both login and current-user. The suite reached 88 passing tests.
- Learner wired LoginForm, Session and App state; the supplied check showed 93
  passing tests, build and lint. Token retrieval is followed by current-user lookup;
  only a runtime-checked active profile can establish the authenticated UI.
- Mentor completed the requested fixes: clear old feedback before a retry, suppress
  aborted-result alerts, reset identity mocks per test, and await late Promise/React
  completion before making negative assertions. Added coverage for pending controls
  and duplicate prevention across both requests, silent cancellation and recovery,
  and late profile completion after unmount/replacement.
- Final mentor-run checks on Node 24.21.0: 98 tests across seven files passed;
  TypeScript/production build, ESLint and whitespace checks passed. Breakdown:
  identity 33, client 9, errors 9, LoginForm 16, RegisterForm 25, App 4, TicketList 2.
- The token/profile pair is held in App memory, above screen selection. Nothing is
  persisted in browser storage. Registration remains separate from sign-in; mock
  Tickets remain explicitly labelled. Logout/expiry handling is not yet implemented.

## 16 October real browser evidence

- Learner backend logs confirm POST /auth/login 401, POST /users 201,
  POST /auth/login 200 and GET /users/me 200. All four entries report
  unexpected_error=false. The successful login used a newly registered synthetic
  account, not a demonstrated successful retry of the previous day's account.
- Safari shows the checked active public profile and signed-in feedback. Navigating
  Tickets → Login retains that feedback without an additional login request in the
  supplied evidence. Full reload restores the empty Login form.
- The initial failed-login response is visible; its form alert is outside the
  screenshot crop. The fixed user-facing message is covered by source/tests.
- Evidence retained here is limited to statuses, public-profile shape and observable
  behavior. No password, bearer token, Authorization header or screenshot is copied
  into this repository. Local development signing-key rotation was recommended after
  an access token appeared in a supplied screenshot; completion is not yet confirmed.
- Product READMEs, weekly status/plan and learning notes now reflect the local result.
  Friday commits/pushes and exact-SHA hosted Frontend/Backend CI are still pending.
  This is local integration evidence, not a hosted deployment or complete session
  lifecycle. Thursday's successful CI does not verify Friday's uncommitted changes.
