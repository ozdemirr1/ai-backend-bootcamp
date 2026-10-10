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
