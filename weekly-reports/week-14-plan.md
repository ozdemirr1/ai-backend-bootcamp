# Week 14 Plan — First API integration

## Dates and outcome

12–18 October 2026, Month 04. Prepared during Week 13's 11 October review.
18 planned hours. On 12 October the learner chose to start on Monday: move the
3-hour frontend CI package from Tuesday to Monday. On 13 October the learner chose
to continue: move Wednesday's runtime/request-boundary package to Tuesday and keep
Wednesday as optional rest/catch-up. Other packages and the 18-hour total stay
unchanged. Estimates are not measured time logs.

Deliver a locally verified register → login → current-User flow against OpsDesk's
existing API, with explicit loading/error states and frontend CI. Extend to the
existing Organization collection only if the required identity flow is complete.
This plan does not claim that integration or hosting has already been delivered.

## Starting gate

- User decision on 11 October: use normal PR merges (`gh pr merge --merge`) from
  Week 14 onward to preserve meaningful daily commits and their original history.
  Keep weekly branches, reviewed-head checks, and post-merge branch cleanup. Discuss
  any future strategy change first. Retain Week 13's squash merge as a completed
  learning example; do not rewrite that history.
- Week 13 PR #41 merged as 511715d on 11 October after reviewed-head push/PR Backend
  CI passed. Product main is clean and matches locally recorded origin/main. Create
  feature/week-14-api-integration from updated main when Week 14 work begins; that
  branch does not exist yet at Monday opening. Bootcamp Sunday closure was committed
  and pushed as 1bdca71; two subsequent merge-strategy note edits remain uncommitted
  and will join the Monday documentation package.
- The learner implemented 23 passing frontend tests, typed mock Tickets, and both
  controlled demo forms. Preserve those behaviors unless intentionally replacing
  the demo behavior with the reviewed real flow and updating tests together.
- Explain architecture and show a small analogous request example before asking
  the learner to implement product requests. Setup and feature exercises stay
  learner-owned; mentor maintains documentation and reviews.

## Ready endpoints and dependencies

| Flow | Existing endpoint | Boundary |
| --- | --- | --- |
| Registration | POST /users | email/password only; 201 public profile; 409 duplicate email |
| Login | POST /auth/login | 200 access_token/token_type; generic 401 for invalid credentials |
| Current User | GET /users/me | Requires bearer token and active persisted User |
| Optional Organizations | GET /organizations | Existing membership-scoped paginated collection; empty is valid |
| Real Ticket list | Not implemented | Keep mock Tickets clearly labelled; separately scope backend read work |

Organization creation exists but is not automatically added to this package. Do not
make Ticket reads, all remaining role/workflow features, or a redesign prerequisites
for the first connected identity screen.

## Integration decisions to implement after review

- Use a small fetch-based request module. Decode responses as untrusted runtime data
  and validate required shapes at the boundary; a TypeScript cast is not validation.
  A small explicit guard is sufficient to start. No new schema or form library is
  required solely to satisfy this exercise.
- Match the existing API error envelope and field names by inspecting source/contracts
  before coding. Check HTTP status; network failure and HTTP error are different cases.
  Map known errors to safe messages rather than rendering arbitrary response bodies.
- Use explicit public API configuration. Explain Vite browser-exposed configuration;
  no backend credentials or JWT signing secret enter frontend code or committed files.
  Choose one documented local origin strategy: a development proxy or narrowly scoped
  backend CORS. A dev proxy does not configure production networking; verify preview
  and hosted origin behavior separately. Do not disable browser security.
- Begin with a bounded in-memory access-token/session design, no browser persistence
  or refresh-token feature. Reload requires login; logout and an expired/invalid token
  clear session state. Never print/store tokens in logs or documents. Prevent late
  requests from restoring stale session state after logout; teach cancellation or
  request ownership when implementing that path.
- Keep session state above screens that need it, while each form owns its input state.
  UI guards are navigation aids; existing backend identity/object/role checks remain
  authoritative. Do not introduce a router or global state library just for this flow.
- Review backend email canonicalization and NFC/15–128-code-point password rules
  before real form submission. Confirmation stays UI-only. The server revalidates all
  inputs; never treat client validation as credential verification or authorization.
- Real success must follow a checked successful response. Registration does not
  automatically log in. A request timeout may occur after a successful server commit;
  avoid automatic registration retries or asserting that no account was created.

## Daily allocation

| Day | Budget | Package |
| --- | --- | --- |
| Mon 12 Oct | 3 h | Verify merged baseline and create weekly branch; explained frontend CI exercise (npm ci, tests, build, lint), compatible Node selection, hosted evidence; inspect identity API/error contracts |
| Tue 13 Oct | 3 h | Align local Node with CI; small fetch example, public API configuration and local origin strategy, response/error guards and focused tests |
| Wed 14 Oct | Optional | Rest/catch-up; no additional required hours |
| Thu 15 Oct | 3 h | Connect registration; payload excludes confirmation, handle validation/conflict/network states and duplicate-submit prevention; tests |
| Fri 16 Oct | 3 h | Connect login and current User; in-memory session, loading/failure paths and tests |
| Sat 17 Oct | 3 h | Logout/expired-token/stale-request behavior, real local browser verification; optional Organization list only if core gates pass |
| Sun 18 Oct | 3 h | Full regression, browser and hosted CI evidence, documentation/Git closure, deployment checkpoint and Week 15 dependency plan |
| Total | 18 h | Includes explanations, review, tests, and documentation |

Trim optional Organization UI or cosmetic work first if capacity is tight. Record
any unfinished required flow and its revised date; do not silently claim closure.

## Monday implementation package — Frontend CI

Opening evidence: product main clean at 511715d; bootcamp at 1bdca71 with only the
two acknowledged merge-strategy note edits. Existing workflow runs Backend CI only.
Local Node is 25.2.1/npm 11.6.2; inspected lockfile engines for Vite, Vitest, ESLint,
plugin-react, TypeScript, and jsdom permit Node 24. Official release guidance lists
24 as LTS and 25 as EOL. Adopt Node 24 for hosted checks and plan local runtime
alignment before integration; do not claim local Node 25 runs prove Node 24 behavior.

- Learner updates main with a fast-forward pull, creates the planned weekly branch,
  and writes .github/workflows/frontend-ci.yml. Keep Backend CI unchanged.
- Workflow name Frontend CI; events push and pull_request, initially without path or
  branch filters. permissions contents: read. One frontend-checks job on ubuntu-latest
  with timeout-minutes: 10; defaults.run.working-directory: frontend.
- Checkout using actions/checkout@v7, persist-credentials: false. Setup Node using
  actions/setup-node@v7 with node-version: '24', cache: npm, and cache-dependency-path:
  frontend/package-lock.json. Action inputs remain repository-relative: defaults.run
  changes only run steps. Official action docs were checked on 12 October.
- Separate named run steps: npm ci, npm test, npm run build, npm run lint. Failures
  must fail the job; no continue-on-error, background/watch/dev/preview server,
  secret, database, deployment, artifact upload, or dependency upgrade is required.
- Explain with a small analogous subdirectory job first. npm cache holds package
  data, not a ready node_modules tree; npm ci remains necessary even on a cache hit.
- Learner runs npm ci/test/build/lint and whitespace checks locally, then mentor
  reviews workflow, updates product READMEs, and prepares commit/push. Confirm the
  actual Frontend CI run at the pushed SHA. Configured YAML or local tests alone do
  not establish hosted success. Read runner Node/npm output if environments differ.
- Keep the feature branch open for the week's remaining work. Daily meaningful
  commits and push; eventual weekly PR merges with --merge, not --squash.
- Learning question: Why is npm ci still needed when the setup-node npm cache hits?

Sources: [setup-node](https://github.com/actions/setup-node),
[run defaults](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/set-default-values-for-jobs),
[Node release status](https://nodejs.org/en/about/previous-releases).

### Monday outcome

Product da695c0 is committed/pushed. Frontend and Backend CI both passed at the exact
head; frontend logs show Node 24.21.0/npm 11.19.0 and 23 passing tests, build and lint.
Workflow review, README updates, local checks, and cache learning review are complete.
Bootcamp documentation publication remains the daily closure step. Keep the weekly
branch open; align local Node with CI before the next integration package.

## Tuesday opening — 13 October

Monday is closed: product da695c0 has successful Frontend/Backend CI and bootcamp
publication is 1979854. Local inspection confirms both trees clean at opening.
Continue feature/week-14-api-integration; no new branch or dependency upgrade.

First checkpoint: local Node 25.2.1 is installed via Homebrew's unversioned node
formula. No Node 24 executable exists at the inspected Homebrew opt path. Learner
installs the separate node@24 formula, then puts its bin directory first in PATH
for the working terminal. Verify node/npm paths and versions before npm ci/test/
build/lint. This shell selection is temporary; revisit persistent/project selection
after proving the runtime works, without unlinking other Node installations.

Checkpoint completed 13 October: mentor resolved the OpenSSL link blocker, installed
Node 24.21.0/npm 11.19.0, and verified persistent shell selection after backing up
the shell configuration. Clean dependency installation, 23 tests, build, lint and
whitespace checks passed under Node 24. No frontend package/lockfile change required.

After that checkpoint, teach a small analogous fetch example and issue the grouped
API boundary/configuration exercise. Reviewed current backend errors: JSON envelope
error.code/message/details; fetch HTTP errors and network failures must be handled
separately. Do not implement form wiring or token persistence in this first package.

Sources checked 13 October: [Homebrew node@24](https://formulae.brew.sh/formula/node@24)
and [Fetch behavior](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch).

## Verification and acceptance

- Request tests cover valid shapes, malformed response data, known HTTP failures,
  network rejection, and omitted confirmation. Use independent response fixtures.
- Component tests cover waiting, disabled duplicate submission, recovery from error,
  verified success, secret-field clearing, and accurate demo-versus-real messaging.
- Session tests cover current User, logout, 401 expiration, and stale responses;
  403 must not be misrepresented as successful access. Add tests for implemented
  behavior, not every hypothetical feature.
- Run test/build/lint and whitespace checks locally; confirm frontend CI at the actual
  reviewed commit. Backend CI remains separate. Backend configuration changes require
  relevant backend tests; database tests must retain the product test-target guard.
- Verify a real local browser flow against an explicitly selected non-production
  backend with synthetic credentials; no destructive integration tests on development
  data. Hosted API access and CORS need actual browser evidence, not only jsdom mocks.
- Keep mock Tickets explicit until real read APIs exist. No real Ticket-read success
  or deployment may be inferred from a successful identity flow.

## Deployment checkpoint

The Month 04 hosted full-stack demo remains an outstanding delivery goal. By Sunday
18 October, record a cost-reviewed hosting choice, database/migration/secrets plan,
browser/API origin plan, bounded public demo scope, and a concrete Week 15 deployment
task. Assess provider options at that time using current pricing/documentation.
Target a first hosted identity-flow preview during Week 15 (19–25 October), subject
to the integration and hosting gates; this is a planning target, not a promised launch.
Do not defer every hosting task to Month 10 or make the first preview depend on the
entire Ticket backlog. Month 10 remains later production-engineering improvements.

### Tuesday outcome — 13 October

Runtime alignment, error guards/messages, public API base configuration, local Vite
proxy and requestJson are implemented and reviewed. The learner corrected redundant
assignment, cancellation during body reading and test cleanup scope. Local evidence:
41 tests in six files, successful build/lint, and a real Safari request through the
proxy receiving the expected unauthenticated HTTP 401 confirmed by backend logs.
The generic helper returns unknown success data; endpoint-specific success validation
and form payload construction (including omitted confirmation) remain later work.
No authenticated session, DB connectivity or deployment is established by this probe.
Documentation prepared; product commit/push, hosted CI and bootcamp publication are
pending. Wednesday remains optional rest/catch-up; Thursday's core is real registration.

Tuesday publication update: product `2b7da04` is pushed with a clean tree. Both
[Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/38414908289) and
[Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/38414908140) passed
at that SHA; hosted frontend logs confirm 41 tests, build/lint and an npm cache hit.
Only bootcamp documentation publication remains for Tuesday's daily closure.

## Thursday opening — 15 October

Tuesday closed with bootcamp f7a1d3c; learner took Wednesday off as planned. Start
from clean product 2b7da04 on the existing weekly branch. Keep the three-hour budget.
First implement/test the identity API adapter: unknown -> checked UserProfile,
explicit email/password request, exact 201 success, safe failure propagation and
no confirmation field leakage. Then wire RegisterForm with loading/error/success,
server-aligned bounded validation, duplicate-submit prevention and cancellation on
unmount. Update labels so real registration is distinguishable from remaining demos.
Finish with component tests, real development registration/conflict evidence and
README/report/publication checks. Registration must not imply automatic login.

### Thursday setup correction

The live registration check exposed an empty development schema despite existing
roles/databases. Added and tested an explicit guarded development Alembic target;
applied both existing revisions through 31be9023cfb2 and verified a repeat upgrade,
model/schema alignment and app-role isolation. The test migration target remains
the default and destructive tests remain restricted to the product test database.
Resume the learner's browser check: first registration must show 201 and the checked
profile/success message; repeating the same email must show 409 and its safe message.
Do not mark real registration complete based only on schema setup or mocked tests.

Learner follow-up: Safari response previews now show a created public profile and
success message with cleared passwords, then email_already_exists with correct form
feedback. Local behavior is demonstrated; HTTP status headers are not visible in
those screenshots. READMEs and evidence updated. Proceed with daily Git publication
and exact-SHA frontend/backend CI before closing this package.

## Friday opening — 16 October

Thursday is closed: backend request logs confirmed POST /users 201 then 409, both
with unexpected_error=false. Product ea6f6f4 and bootcamp e75cdf3 were pushed; both
CI workflows passed at the exact product SHA. Product remains clean at Friday opening
on feature/week-14-api-integration. The learner also read the persisted synthetic
User and migration revision through psql; pgAdmin connection walkthrough followed.

Friday retains a 3-hour active-work budget, with a practical 3–4-hour estimate if
debugging is needed; breaks and CI waiting are separate and this is not measured time.
Implement login/current-user adapters first, then connect the form and hold the
reviewed session above screens. Accept login only after 200 plus a checked bearer
reply; use the token for GET /users/me and establish authenticated UI only after a
checked active profile. Do not persist or log tokens. Loading, failure, unmount and
stale-result handling are part of the feature, with meaningful tests. Saturday
retains logout, expired-session and expanded stale-request/browser checks.

Start with a small analogous runtime response guard, then learner edits the existing
identity adapter and tests. Preserve registration coverage. No new branch, dependency,
database reprovisioning or UI redesign is needed. Review the adapter before form wiring.

### Friday outcome — local verification complete

- Adapter coverage additions passed, followed by connected LoginForm and App session
  wiring. Mentor completed the explicitly requested cancellation/retry/test fixes.
- Final local check: 98 tests across seven files, production build, lint and whitespace
  checks passed on Node 24. The session is accepted only after a checked active profile.
- Learner browser/backend evidence: wrong login 401; a new synthetic registration 201;
  correct login 200 and current-user 200, all unexpected_error=false. Tickets → Login
  preserved the signed-in state; full reload restored the empty form.
- Product READMEs and bootcamp evidence are updated. Publish the daily changes on the
  existing weekly branch, then verify both hosted workflows at the new commit SHA.
- Logout, expired-session handling and remaining lifecycle checks are still Saturday
  work. No optional Organization reads or real Ticket reads are claimed complete.
  Keep normal merge for the weekly PR; local browser verification is not deployment.
