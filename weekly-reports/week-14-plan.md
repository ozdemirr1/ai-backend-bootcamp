# Week 14 Plan — First API integration

## Dates and outcome

12–18 October 2026, Month 04. Prepared during Week 13's 11 October review.
18 planned hours across Tuesday–Sunday; Monday is an optional rest/catch-up day,
not extra mandatory capacity. Estimates are not measured time logs.

Deliver a locally verified register → login → current-User flow against OpsDesk's
existing API, with explicit loading/error states and frontend CI. Extend to the
existing Organization collection only if the required identity flow is complete.
This plan does not claim that integration or hosting has already been delivered.

## Starting gate

- Week 13 PR #41 merged as 511715d on 11 October after reviewed-head push/PR Backend
  CI passed. Product main is clean and matches locally recorded origin/main. Create
  feature/week-14-api-integration from updated main when Week 14 work begins; that
  branch does not exist yet. Bootcamp Saturday head: e970fc9;
  Sunday learning/report changes require their own commit/push evidence.
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
| Tue 13 Oct | 3 h | Verify merged baseline and create weekly branch; explained frontend CI exercise (npm ci, tests, build, lint), compatible Node selection, hosted evidence; inspect identity API/error contracts |
| Wed 14 Oct | 3 h | Small fetch example, public API configuration and local origin strategy, response/error guards and focused tests |
| Thu 15 Oct | 3 h | Connect registration; payload excludes confirmation, handle validation/conflict/network states and duplicate-submit prevention; tests |
| Fri 16 Oct | 3 h | Connect login and current User; in-memory session, loading/failure paths and tests |
| Sat 17 Oct | 3 h | Logout/expired-token/stale-request behavior, real local browser verification; optional Organization list only if core gates pass |
| Sun 18 Oct | 3 h | Full regression, browser and hosted CI evidence, documentation/Git closure, deployment checkpoint and Week 15 dependency plan |
| Total | 18 h | Includes explanations, review, tests, and documentation |

Trim optional Organization UI or cosmetic work first if capacity is tight. Record
any unfinished required flow and its revised date; do not silently claim closure.

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
