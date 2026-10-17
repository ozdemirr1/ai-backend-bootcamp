# React and TypeScript Foundations

## 6 October 2026 — Static OpsDesk shell

Mentor-maintained review notes; these do not claim that the learner independently
authored every explanation below.

- A component is a function describing part of the UI. `App` composes the screen;
  `AppHeader` presents a product name and subtitle.
- JSX describes the rendered structure. Braces embed expressions, and capitalized
  component names distinguish components from built-in HTML elements.
- Props are inputs supplied by the parent. `AppHeaderProps` requires two strings:
  `productName` and `subtitle`. Destructuring extracts those fields from the object.
- `export default` exposes a module's default export; `import` makes that export
  available in another module. A props type need not be exported unless another
  module needs it, but exporting it here is harmless.
- The current rendering path is `index.html` → `main.tsx` → `App` → `AppHeader`.
- `index.css` supplies global defaults; `App.css` supplies current layout styles.
  These ordinary CSS files are global, not automatically scoped to components.

## Reviewed learner answer

The learner explained that passing the OpsDesk name through App makes AppHeader
reusable with different text without changing the component's implementation.
This reasoning is correct. Refine “no external dependency” to “an explicit props
contract”: AppHeader still depends on its supplied props and React, but no longer
hardcodes a particular product name.

## Verification boundaries

- `npm run build` runs `tsc -b && vite build`: type checking followed by bundling.
- TypeScript checks source-level type compatibility, not untrusted runtime data.
  It does not replace backend validation, authentication, or authorization.
- `npm run lint` checks the configured ESLint rules, not all formatting preferences.
- Browser inspection verifies the displayed shell and captured console output;
  it does not establish responsive coverage or future interactive behavior.
- Behavior tests begin with state/events. The current static shell has no test script.
- A plain `git diff --check` does not inspect untracked source files. The first review
  explicitly checked new files and found trailing whitespace that ESLint accepted.
- `package.json` declares allowed version ranges; `package-lock.json` records exact
  dependency resolution. Use `npm ci` to install that recorded dependency tree.

Completed learner experiment on 6 October: supplied screenshots show
`productName={123}` failing `npm run build` with TS2322 because a number is not
assignable to the declared string prop. Since the script uses `tsc -b && vite build`,
the failed type check prevents the Vite build step from running. This is a compile-time
contract check, not runtime validation.

The learner restored `productName="OpsDesk"`; the editor reports no problems and
local source inspection confirms the restoration. Subsequent learner terminal evidence
confirms a successful post-experiment build. The final shell is recorded in product
commit `781e74b`; earlier lint and browser smoke checks also passed.

## 7 October — State and screen selection

- Props supply inputs; state remembers the component's current selection between
  renders. Calling the setter requests a render with the updated value.
- A local variable assignment does not notify React to render. Call useState at the
  top level, and pass event handlers to onClick rather than calling setters in render.
- Learner used `Screen = 'tickets' | 'login' | 'register'`. Their explanation was
  correct: three independent booleans can encode contradictory active screens; one
  union state selects one value. Matching conditional rendering must still implement
  that selection correctly.
- Current screen selection changes only local UI state. It is neither routing nor
  authentication; refreshing initializes the selection again.
- Review verified click transitions, one visible screen heading at a time, updated
  aria-pressed, and keyboard activation/focus. Behavior tests are the next exercise.

## 7 October — First behavior tests completed

- Vitest runs the tests; React Testing Library renders components and finds DOM
  elements by accessible role/name. user-event applies awaited interactions.
- jsdom supplies a DOM environment inside Node, not a full visual browser.
  jest-dom adds assertions such as toBeInTheDocument and toHaveAttribute.
- getByRole throws when the expected element is absent; queryByRole returns null
  when absent, which makes it appropriate for disappearance assertions.
- Role-specific queries distinguish a Tickets button from a Tickets heading.
- afterEach cleanup removes the rendered tree so tests do not inherit prior DOM.
- Three learner-written tests verify initial selection, Login and return to Tickets,
  and Register with other screen content absent and other buttons unpressed.
  They assert observable behavior without reaching into activeScreen state.
- Test/build/lint passed in the learner's terminal. Git diff checks whitespace
  separately; its trailing-space warnings were fixed without changing behavior.

## 8 October — Typed mock lists

- TicketSummary[] describes an array of display records; status and priority unions
  match the current product vocabulary. This display type is not runtime API validation.
- Data flows mockTickets → App → TicketList. The list receives props rather than
  importing a global mock array or copying unchanged props into local state.
- map creates JSX items; a callback block with braces needs an explicit return.
- Each rendered li uses ticketId as key. Stable IDs track record identity even when
  positions change; an index tracks a position. React keys are not DOM attributes.
  Learner correctly explained state misassociation with shifted index keys. Clarified
  that index keys do not necessarily rebuild the whole list, and stable keys neither
  prevent renders nor guarantee performance gains; preserving identity is the goal.
- Empty data is a normal UI state: show the message with no list/listitems.
- Independent test fixtures plus within(row) prove that fields belong to the correct
  row, not just that those strings occur somewhere in the document.
- Five tests passed: two list tests plus three App navigation tests. Browser smoke
  checks additionally verified the list and 375px metadata wrapping.
- list-style:none can remove Safari's list semantics; role="list" preserves them.
  See [MDN list accessibility](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/list-style#accessibility).
  DOM tests do not establish real-browser layout or accessibility behavior.

## 9 October — Controlled Login demo

- value supplies the input's displayed value; onChange reads currentTarget.value
  and synchronously calls the matching state setter. Initialize controlled text
  fields with empty strings. Without the state update, React restores the supplied
  value after editing, so the field behaves as read-only. This is not simply a lack
  of re-rendering: another render still supplies the unchanged state value.
- Form onSubmit handles button and Enter submission. preventDefault stops native
  navigation; noValidate bypasses native constraint-validation blocking so this
  exercise can show its own consistent messages. Neither validates credentials.
- Validate required email, a bounded email-shape heuristic, then non-empty password.
  Trim only the email for checks; do not trim the password. This demo deliberately
  does not reproduce the backend's full normalization and validation contract.
- A Feedback union represents an error, success, or no message. Use role=alert for
  errors and role=status for demo completion. Editing clears stale feedback; demo
  completion clears the password and retains email. Switching screens unmounts the
  form and discards its local state.
- Client validation helps correct input; only the backend can verify credentials
  and enforce access rules. This demo sends no request and establishes no session.
- Test names must match assertions. The first review found a test named for both
  error and success clearing but checking only an email edit after an error. Renamed
  that case and added password-edit-after-success coverage. Final evidence: seven
  form tests plus the existing five tests, with build/lint and browser checks passing.
- git diff --check omits untracked files. Check new source separately, then run
  git diff --cached --check after git add so the commit candidate is covered.

## 10 October — Register and cross-field validation

- Keep confirmation in local state because the form needs its current value for
  rendering and comparison. Compute password equality from current fields rather
  than storing another synchronized boolean. Check required values before equality:
  two empty strings also match.
- confirmPassword is a UX correction aid. OpsDesk's RegisterUserRequest accepts
  only email/password and forbids extras; confirmation is not a request field.
  Absence from a database model alone does not decide an API schema: other APIs may
  deliberately accept transient fields. Client form validation is bypassable.
- Matching passwords neither verifies the backend's full rules nor creates an
  account. OpsDesk's current password rules are NFC normalization and 15–128 code
  points, not special-symbol requirements or breached-password lookups.
- Successful database commit creates the persisted account. A 201 response reports
  that outcome; if delivery fails after commit, the account can exist even though
  the client saw a network error. Do not infer rollback from a timeout.
- Register fields use anchored label queries to distinguish Password from Confirm
  password. Tests should prove each claimed field-edit behavior; two tests editing
  only confirmation cannot establish email/password feedback clearing.
- A reset test should first create the state it claims to reset: type into fields
  and establish feedback before switching screens, then assert empty fields and no
  alert/status after return. Learner completed these additions and corrected the
  confirmation-test names. Final evidence: 11 Register tests and 23 frontend tests
  overall, with successful build/lint and applicable same-day browser verification.

## 11 October — Final assessment and integration boundary

- Learner correctly explained type erasure: a TypeScript TicketSummary annotation
  cannot inspect an HTTP response at runtime. Treat decoded data as untrusted and
  validate required fields before use. Small explicit type guards or a schema tool
  can serve this purpose; Zod is an option, not a new mandatory dependency.
- A null value may cause an exception or incorrect UI depending on how it is used;
  null itself does not always throw. Tests should exercise the intended failure path.
- Learner correctly located authorization on the backend. Hidden buttons are UX;
  direct HTTP calls still need current identity and resource/organization/role checks.
- Test/build/lint results prove their checked scope. jsdom does not render visual
  layout; mocked responses do not prove the real API/CORS deployment works. However,
  HTTP errors, expiration, network rejection, and malformed payloads can and should
  have deliberate tests. Real browser/integration checks complement those tests.
- The learner reviewed the built bundle using npm run preview and reported all
  requested flows and layout/focus checks passed. Preview is local serving of dist,
  not public deployment. Sunday terminal evidence again shows 23 tests/build/lint
  passing; GitHub's Backend CI is separately verified and does not run frontend tests.

## 11 October — Merge strategy lesson

- Week 13 used squash merge for PR #41: five daily product commits became one new
  main commit, 511715d, dated 11 October. Code was preserved, while the original
  daily commit identities were not incorporated into main's ancestry. This explains
  the different history graph and daily contribution attribution compared with the
  normal merges used in earlier weeks. Deleting the feature branch was not the cause.
- The learner accepted retaining this squash merge as a useful comparison between
  strategies. It was not a planned experiment before merging; its effects were
  discussed afterward. No history rewrite is requested.
- Agreed practice from Week 14: normal merge (`--merge`) for the weekly PR so meaningful
  daily commits remain in main's history. Discuss any future strategy change first.

## 12 October — Frontend CI and npm cache

- GitHub Actions now checks the same frontend install/test/build/lint sequence on
  pushes and pull requests. defaults.run.working-directory applies to shell steps;
  setup-node's cache-dependency-path remains relative to the repository root.
- npm's package cache is not a ready node_modules tree. npm ci installs the locked
  dependency tree, replacing an existing node_modules directory when present.
  Cached data can reduce downloads, but a cache hit does not guarantee zero network
  activity or every required package being available. Do not skip installation.
- Learner explained that distinction correctly, with the network-traffic caveat
  clarified in review. Actual first hosted run had no npm cache hit and saved a cache
  afterward; subsequent reuse is possible but was not tested by this first run.
- At product da695c0, hosted Node 24.21.0/npm 11.19.0 passed 23 tests, build, and lint.
  This proves the configured hosted checks at that commit, not real API integration,
  browser layout, deployment, or local runtime alignment. Backend CI passed separately.

## 13 October — API boundary, configuration and runtime evidence

- Local Node 24.21.0/npm 11.19.0 now matches the inspected CI runtime. PATH selects
  an installed executable; adding a nonexistent directory does not install Node.
  Homebrew's partially linked OpenSSL dependency had to be repaired before install.
- typeof object includes null and arrays and proves no nested field shape. Guards
  narrow unknown by checking object/null/array boundaries, required string fields
  and details entries. Excluding null/arrays alone does not prove a plain prototype.
- Error codes map to fixed client messages; arbitrary server messages are not shown.
  Successful parsed JSON remains unknown until an endpoint-specific guard checks it.
- VITE_ configuration is public browser data, never a place for backend secrets.
  The local /api proxy removes that prefix before forwarding to the backend.
  This configuration does not automatically provision production routing or CORS.
- fetch resolving does not mean an HTTP operation succeeded. Inspect response.ok
  and preserve status. JSON decoding is another asynchronous step and can fail.
  AbortError can occur during fetch or body reading; both paths need deliberate tests.
- Network failure does not prove the server never processed a request. CORS may hide
  a response and connections can fail after commit. Do not blindly retry registration.
- Login 401 and expired-session 401 need context-specific UI/session handling.
  The generic request helper classifies results; it does not navigate or clear sessions.
- A describe-scoped afterEach only cleans tests within that scope. Keep fetch-mocking
  tests inside the cleanup scope. Green tests alone do not establish isolation.
- Safari console verification used a dynamic import with .then callbacks after the
  top-level await form failed to parse. Console logging returns undefined; a fulfilled
  logging Promise is separate from the logged ApiResult's ok=false HTTP outcome.
- Local evidence: 41 tests, build/lint, and browser /api/users/me -> backend /users/me
  returning 401 with safe message. This proves proxy/error transport, not completed
  identity integration, database connectivity, or a hosted deployment.
- Hosted follow-up at product 2b7da04: Frontend CI restored the npm package cache
  and still ran the dependency installation step before 41 passing tests, build
  and lint. Backend CI also passed. This supplies concrete cache-hit evidence in
  addition to Monday's first-run miss.

## 15 October — Real registration and persistence readiness

- TypeScript types do not validate network responses. The registration adapter
  checks unknown data and only accepts HTTP 201 plus the public profile shape.
  Confirmation stays in form state; the request explicitly includes email/password.
- A malformed or lost response can follow a committed account. Show an uncertain
  outcome instead of claiming no account exists or blindly repeating creation.
- Controlled registration normalizes passwords to NFC, checks code-point length,
  compares confirmation and leaves final validation/uniqueness to the backend.
- State disables pending controls; an immediate request ref prevents duplicate
  submissions before the next render. Unmount aborts and stale-result ownership
  checks prevent old responses updating a fresh form. Abort is not server rollback.
- Provisioning roles/databases, migrating tables and running an API are separate
  steps. Startup and a token-free 401 do not prove persistence readiness. The local
  development target now has an explicit guarded Alembic path; destructive tests
  remain isolated in the product test database.
- Learner Safari evidence after migration: public profile and success feedback,
  retained email and cleared passwords; repeat submission returns duplicate-email
  feedback. Registration creates an account but does not create a frontend session.
- Local frontend evidence: 68 tests across seven files, build and lint passed.
  Browser screenshots show response bodies; direct HTTP status headers are separate
  evidence. Login remains a demo until its own integration is implemented.

## 16 October — Login, current User and in-memory session

- Login success requires the endpoint's exact HTTP 200 and a checked bearer-response
  shape. A token string guard does not verify its signature or prove authorization.
  GET /users/me verifies the current identity through the backend; frontend session
  establishment also requires an active profile. A boolean false is valid profile
  data but does not satisfy the rule for entering the signed-in UI.
- Form state owns email/password/feedback; App state owns the checked session above
  the screens. Unmounting LoginForm discards form state while navigation preserves
  App's session. Full reload creates fresh App state and requires another sign-in.
- One AbortController and an immediate request ref cover login plus profile lookup.
  Disable controls throughout both requests and verify result ownership after each
  await. An old response must not authenticate a newly mounted form. Abort cannot
  guarantee that the server undid a request it already processed.
- Clear stale feedback when a retry begins, including when inputs are unchanged.
  Expected cancellation should not produce a misleading error alert. Resetting mocks
  clears queued implementations as well as call history; clearing calls alone does
  not provide that isolation. Await controlled Promise completion inside act before
  asserting that a late response did not call the session callback.
- Final local evidence: 98 tests, build/lint and whitespace checks passed. Browser
  evidence covers 401 login, 201 registration, 200 login and 200 current-user, plus
  navigation survival and reload reset. Logout and expiry handling remain separate.
- Removing a token from browser memory does not revoke a still-valid server JWT.
  Keep full tokens out of screenshots/logs/reports. Rotating a local development
  signing secret invalidates tokens signed with the previous secret, without deleting
  database users; this is not a replacement for the application's logout design.

## 17 October — Session checks, logout and stale responses

- Local logout clears App's session and cancels its pending check; it does not revoke
  the JWT at the server. A page without new protected requests cannot automatically
  discover that its token has become invalid. Check session explicitly asks /users/me.
- A 401 or inactive checked profile clears the session. Network failures, 500 and
  invalid response data do not establish invalid credentials, so preserve the session
  and offer safe retry feedback. A successful login clears the previous warning.
- Keep session refs synchronized in event/result handlers rather than writing refs
  during render. State drives the UI; the request ref and AbortSignal establish which
  asynchronous response still owns permission to update it. A replacement login must
  invalidate earlier work even if that work eventually completes.
- Type deferred test Promises with CurrentUserResult rather than any. Test both the
  abort signal and completed late responses: cancellation and stale-result suppression
  are related but distinct protections. Await React updates before negative assertions.
- Verified locally: 110 tests plus build/lint/whitespace checks. Real browser evidence
  shows check 200, invalid signature 401 after local key rotation, and recovery via
  login/profile 200. It does not prove elapsed-time expiry or hosted deployment.
