# Week 14 Plan — First API integration

## Dates and outcome

12–18 October 2026, Month 04. Prepared during Week 13's 11 October review.
18 planned hours. On 12 October the learner chose to start on Monday: move the
3-hour frontend CI package from Tuesday to Monday, keeping Tuesday as the optional
rest/catch-up day. Other packages and total capacity stay unchanged. Estimates are
not measured time logs.

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
| Tue 13 Oct | Optional | Rest/catch-up; no additional required hours |
| Wed 14 Oct | 3 h | Small fetch example, public API configuration and local origin strategy, response/error guards and focused tests |
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
