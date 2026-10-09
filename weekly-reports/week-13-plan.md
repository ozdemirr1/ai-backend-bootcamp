# Week 13 Plan

## Dates, objective, and boundaries

6–11 October 2026. Month 04 starts in this month's primary project conversation.
Budget: 18 active hours, within the normal 15–20 hour weekly capacity. Breaks,
downloads, and external CI waits are additional. Durations are planning estimates,
not measured time logs. The learner is not required to report active time; optional
feedback about a package taking longer or shorter can refine future estimates.
Close packages by learning outcomes, implementation, checks, documentation, and Git
evidence, not by a time-report requirement.

Learn React + TypeScript through three small OpsDesk outputs: login screen,
register screen, and a Ticket list backed only by synthetic mock data. Build in
the product monorepo's `frontend/`, on `feature/week-13-react-foundation`.
Use Vite's current `react-ts` template and ordinary CSS.

Week 12 closed on 5 October with no technical carry-over. Ticket list/detail APIs,
workflow, assignment, membership mutations, comments, database CI, and deployment
remain explicit Month 03/product backlog. Review only necessary backend dependencies
during Week 14 integration planning. No real API calls, token storage, protected
routes, Tailwind, broad dashboard, Docker, Redis, or AI integration this week.

## Daily packages

| Date | Active budget | Learning, implementation, and evidence |
| --- | ---: | --- |
| Tue 6 Oct | 3.5 h | Components, JSX, typed props; learner-run Vite setup; static shell/header; browser, build, lint; notes and Git review |
| Wed 7 Oct | 3 h | State, events, conditional rendering; simple local screen selection; introduce a minimal Vitest/React Testing Library setup and test a visible interaction |
| Thu 8 Oct | 3 h | Typed mock Tickets, array map, stable keys, list and empty state; tests for populated and empty lists |
| Fri 9 Oct | 3 h | Controlled login form, labels, email/password inputs, submit event, local validation and explicit demo feedback; interaction tests |
| Sat 10 Oct | 3 h | Controlled register form using reviewed API field vocabulary; accessible local feedback and behavior tests; no authentication claim |
| Sun 11 Oct | 2.5 h | Relevant frontend regression, build/lint, browser/keyboard review, README, interview review, weekly report, Git closure and Week 14 dependencies |
| Total | 18 h | All budgets include explanation, implementation, review, and notes |

Allow at most 2 additional hours of buffer within the 20-hour ceiling. If needed,
reduce styling and optional refactoring first. Never quietly drop form/list behavior
tests or expand into backend work. Record unfinished acceptance criteria and revised
dates explicitly. Do not count reading time as implementation evidence.

## Tuesday package — 3–4 active hours

1. Planning and baseline review: 20 minutes.
2. Components, JSX, props, TypeScript shapes, and a small non-OpsDesk analogy:
   40 minutes. Explain unfamiliar destructuring and imports before using them.
3. Learner-run Vite setup and generated-file tour: 35 minutes.
4. Learner implementation of the static shell/header: 65 minutes.
5. Browser check, lint/build, README, learning notes, Git diff: 35 minutes.
6. Understanding check and daily checkpoint: 15 minutes.

The nominal total is 210 minutes. Track remaining work by these packages; revise
estimates from remaining scope, observed blockers, and optional learner feedback.

Tuesday closure: completed on 6 October in local product commit `781e74b`, with
successful build/lint, browser smoke verification, the deliberate prop-type error
experiment, documentation, and a clean product working tree. No Tuesday technical
carry-over; Wednesday's package remains next.

### First real exercise and file-level package

- `frontend/src/components/AppHeader.tsx`: define a props type with required
  `productName: string` and `subtitle: string`; render a semantic header containing
  one h1 and a paragraph from those props. No state or side effects.
- `frontend/src/App.tsx`: compose AppHeader with OpsDesk text and a main region
  explaining that this week's screens use mock data. Remove the demo counter and
  unused starter imports together, then verify the whole file once.
- `frontend/src/App.css` and `frontend/src/index.css`: replace conflicting demo
  styles with minimal readable spacing and typography. No design-system work.
- `frontend/index.html`: set the page title to OpsDesk and the document language
  to the language actually used for visible UI text.
- `frontend/README.md`: explain setup, scripts, directory purpose, and mock-only
  scope. Keep commands portable and record resolved versions from package files.
- `notes/react/react-typescript-foundations.md` in the bootcamp repository: mentor
  records explanations and reviewed learner answers. On 6 October the learner
  delegated README/documentation maintenance to the mentor; implementation and
  concept exercises remain learner-owned.

Acceptance: the header uses parent-provided strings, the shell is visible without
the backend, there is no starter counter, and there are no browser-console errors.
Temporarily pass a number to the string prop, observe a TypeScript diagnostic,
then restore it. This exercise does not prove runtime input validation.

### Verification boundary

- Inspect the generated package scripts before relying on their names. Expected
  checks are `npm run build` (TypeScript check plus production bundle in the usual
  template) and `npm run lint`. A dev server alone does not prove type correctness.
- Tuesday's presentation-only shell uses browser inspection plus build/lint;
  no snapshot test is required for static text. Lint/build are not behavior tests.
- From Wednesday, introduce behavior tests with the first stateful interaction.
  Test the visible result rather than component internals. For forms cover editing,
  invalid submit, valid demo submit, and accessible feedback; for Tickets cover
  populated and empty states. Add filters only if time remains, with their tests.
- Never log, render, persist, or commit plaintext passwords or access tokens.
  Demo password input exists only in transient form state and is cleared on successful
  demo submission. Feedback must state that no account/session was created.
- No PostgreSQL or backend test run is needed for frontend-only changes. If shared
  configuration changes, assess the affected checks before declaring completion.

## Wednesday package — 7 October, approximately 3 hours

1. State, event handlers, conditional rendering, and literal union types through a
   small reading-panel analogy: 35 minutes.
2. Learner implementation and focused review of local screen selection: 45 minutes.
3. Explain and configure Vitest, React Testing Library, user-event, and a DOM test
   environment; learner writes meaningful interaction tests: 60 minutes.
4. Test/build/lint, browser and keyboard smoke check, learning review, documentation,
   commit, push, and verification: 40 minutes.

These are planning estimates, not time-report requirements. Continue on
`feature/week-13-react-foundation` from `781e74b`.

### Implementation package

- `frontend/src/App.tsx`: use one `activeScreen` state with a literal union of
  `tickets`, `login`, and `register`, initially `tickets`. Keep the existing header
  and mock-data explanation. Render three explicitly typed buttons in a labelled
  navigation region; each click selects its corresponding state. Use `aria-pressed`
  to expose the current selection. Render exactly one heading/placeholder paragraph
  for the selected screen inside main. Do not implement the forms or Ticket rows yet.
- `frontend/src/App.css`: use a dedicated class for the selector, modest spacing,
  visible selected state, and a clear keyboard focus indicator. Leave global styles
  and AppHeader unchanged unless review identifies a concrete need.
- Keep event handlers as functions passed to onClick; do not invoke setters during
  render. Call useState at the component's top level. No effects or duplicated boolean
  flags are needed. Selection is local UI state; it resets on a full reload and does
  not change the URL or grant authentication/authorization.

### Test package and acceptance

After reviewing the implementation, explain the test tools before the learner runs
installation commands. Group package scripts, test configuration/setup, and the App
test file as one coherent package. Test default Tickets rendering, switching to Login
and Register, disappearance of the previous heading, returning to Tickets, and the
selected-button state. Query elements by role/name; simulate awaited user interactions.
Do not test React's internal state or add snapshot tests for this behavior.

Acceptance: only one screen is rendered, all three choices work via normal buttons,
the current selection is exposed and visible, keyboard focus is visible, and the
header remains intact. Final checks are behavior tests, TypeScript/build, ESLint,
browser/keyboard smoke check, and reviewed Git changes. The mentor maintains README,
learning notes, and evidence; record today's Git closure for both repositories in the
same closing package.

## Thursday package — 8 October, approximately 3 hours

1. Typed arrays, map, stable keys, and a small book-list analogy: 30 minutes.
2. Learner implements typed mock data, a props-driven TicketList, App wiring, and
   minimal list styling: 60 minutes.
3. Learner writes populated/empty component tests and extends the existing App
   navigation test to prove the list is wired and removed/restored: 45 minutes.
4. Review, test/build/lint/browser checks, documentation, commit/push for both
   repositories, and verification: 45 minutes.

Continue on `feature/week-13-react-foundation` from `5f7f5c3`. No dependencies or
backend changes are needed. No fetch, effects, duplicated list state, filtering,
pagination, CRUD, or routing in this bounded package.

### Grouped file package

- `frontend/src/types/ticket.ts`: export TicketStatus (`open`, `in_progress`,
  `resolved`, `closed`), TicketPriority (`low`, `medium`, `high`, `urgent`), and
  TicketSummary with ticketId: number, title: string, status, and priority. This is
  a small frontend display model, not a claim about an implemented list API contract.
- `frontend/src/data/mockTickets.ts`: export a typed TicketSummary array with three
  synthetic records and fixed unique ticketId values. Import types with import type.
- `frontend/src/components/TicketList.tsx`: accept tickets: TicketSummary[] via props,
  show `No tickets yet.` for an empty array, otherwise render one labelled native
  unordered list with one li per Ticket using ticketId as key. Each row shows its
  title as h3 and visible ID/status/priority text. Keep the Tickets h2 in App.
  Do not import mock data here, mutate props, or copy props into state.
- `frontend/src/App.tsx`: import mockTickets and TicketList; replace the Tickets
  placeholder paragraph with the list, preserving screen state, heading, and forms'
  placeholders. One-way data flow is mockTickets → App → TicketList.
- `frontend/src/App.css`: scoped list/row spacing and readable borders/typography;
  preserve navigation/focus styles. Avoid styling expansion.
- `frontend/src/components/TicketList.test.tsx`: use independent typed fixtures,
  not the application's mock array. Verify populated item count and title/ID/status/
  priority association within each row; verify empty message with no list items.
  Explain within() before asking the learner to scope repeated status/priority text.
- `frontend/src/App.test.tsx`: extend existing initial/navigation checks to prove
  the named list is initially present, absent on Login, and present after returning
  to Tickets; preserve all previous screen-selection checks.

Stable keys identify siblings across insertion/removal/reordering. Do not generate
keys during render or use array positions. Keys are React metadata, not a DOM
attribute to assert. Verify this choice in code review and learning explanation.

Final commands from frontend: npm test, npm run build, npm run lint, git diff --check.
Browser checks include all three mock rows, switching away/back, and no console/key
warnings. Mentor maintains READMEs and notes after reviewing implemented behavior.

## Friday package — 9 October, approximately 3 hours

1. Controlled inputs, change events, form submit, preventDefault, and a small
   non-authentication analogy: 30 minutes.
2. Learner implements an isolated LoginForm and integrates it into App: 60 minutes.
3. Learner writes input/validation/feedback tests and extends App wiring evidence:
   45 minutes.
4. Review, browser/keyboard checks, test/build/lint, docs, and both repositories'
   commit/push verification: 45 minutes.

Continue the existing feature branch from `dcae2ba`; no new dependency. The form
owns email/password strings initialized to empty and transient feedback. App keeps
screen-selection state and the existing Login h2. No fetching, fake tokens, storage,
protected route, form library, effects, timers, or backend changes.

### Grouped file package and demo contract

- `frontend/src/components/LoginForm.tsx`: labelled Email and Password controls,
  type=email/password, name=email/password, autoComplete=username/current-password,
  value/onChange, and an enabled `Continue demo` submit button. Use explicit label
  associations and visible required markers. Use form onSubmit with preventDefault
  and noValidate so the component consistently renders its own validation feedback.
- Initialize feedback to null; a small union of error/success messages is sufficient.
  Changing either input clears stale feedback. Validate on submit in this order:
  trimmed email empty → `Email is required.`; basic email-shape mismatch →
  `Enter a valid email address.`; password exactly empty → `Password is required.`.
  Use `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` only as an explicitly bounded demo heuristic.
  Do not trim the password. Do not claim parity with backend email validation,
  ASCII/NFC rules, or the backend's 15–128-code-point password limits.
- Failure renders a role=alert message and keeps input available for correction.
  Valid demo input renders role=status with `Demo only: no sign-in request was sent.`
  and clears password state. Keep email for convenience. Never echo/log/store a
  password, submit credentials over the network, or claim an authenticated session.
  Use synthetic test values, never real credentials.
- `frontend/src/App.tsx`: replace only the Login placeholder paragraph with LoginForm;
  keep the existing h2, navigation, Ticket list, and Register placeholder.
- `frontend/src/App.css`: scoped auth-form styles for readable width, vertical labels,
  controls, feedback and visible keyboard focus. Avoid altering navigation buttons.
- `frontend/src/components/LoginForm.test.tsx`: isolated tests cover editable fields,
  missing email, missing password with a valid email, malformed email, valid demo
  submit with password clearing and retained email, and stale feedback removal when
  editing. Use getByLabelText for fields and awaited user-event interactions. Click
  the submit button; do not invoke handler functions directly. Check invalid input
  has no success status and success has no error alert. Do not enforce an arbitrary
  test count if a focused table-driven case is clearer.
- `frontend/src/App.test.tsx`: extend the Login navigation test to find the labelled
  controls after switching in and confirm they are absent after returning to Tickets.
  Retain the existing list and navigation assertions.

Keep all changes and checks for each file in one package. Final checks: npm test,
npm run build, npm run lint, git diff --check; browser submit via button and Enter,
labels/focus, invalid/corrected submission, password clearing, no console errors.
Mentor updates README and learning notes after implementation review. Completion
requires both repos' Git closure and a short explanation of value/onChange and why
client-side validation does not establish authentication or authorization.

### Friday review checkpoint

Implementation and learning review are complete on 9 October. Learner evidence:
12 frontend tests passed (7 LoginForm, 3 App, 2 TicketList), build and lint passed.
Browser checks verified button/Enter submission, feedback transitions, password
clearing, and visible keyboard focus. Both READMEs and bootcamp records are updated.
Both repositories' commit/push/clean-status evidence is the remaining closure step.
Continue with the Saturday Register demo after that checkpoint; no new library or
real authentication integration is needed for Week 13.

## Notes, commits, and closure

Append daily concept notes, one mistake/fix, verification outcomes, remaining work,
and Git status. Record optional duration feedback only when provided. Suggested product commits after verification:
`week-13: add React TypeScript frontend shell`, `week-13: render mock ticket list`,
and `week-13: add controlled authentication demo forms`. Group behavior tests with
their feature. Commit mentor-maintained bootcamp evidence at daily or milestone
closure after reviewing the diff; do not leave it pending solely for a time report.
Tuesday evidence commit message: `week-13: record React shell and Tuesday closure`.
Do not commit node_modules, dist, secrets, or machine-specific paths. Keep the npm
lockfile under version control. Review exact changed files before staging.

Sunday closure requires evidence for all three screens, meaningful behavior tests,
build/lint and browser checks, README and notes, weekly report, and recorded
commit/PR/CI status where applicable. Do not claim merge or remote synchronization
without evidence.

## Interview review and next week

1. What makes a function a React component, and what does JSX describe?
2. How do parent-provided props differ from component state?
3. Why does a TypeScript prop type not validate an HTTP response at runtime?
4. Why do lists need stable keys rather than array indexes?
5. What makes an input controlled, and why prevent the default form submission?
6. What do lint, type checking, behavior tests, and a browser check each prove?
7. Why do local form validation and hidden UI controls not enforce authorization?

Before Week 14, inspect existing auth and Organization contracts and decide whether
Ticket reads are required for the first connected screen. Scope backend dependencies
explicitly and retain backend object-level authorization and validation. Plan token
lifecycle, error/loading states, and API configuration before connecting the UI.

## Official reading

Reviewed on 6 October 2026:

- [React Quick Start](https://react.dev/learn)
- [React with TypeScript](https://react.dev/learn/typescript)
- [Thinking in React](https://react.dev/learn/thinking-in-react)
- [Vite guide](https://vite.dev/guide/)

Read the portions needed for the current exercise, then apply them. Do not turn this
week into an unbounded documentation or tutorial sprint.
