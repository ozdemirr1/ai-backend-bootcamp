# Week 13 Report — In Progress

## Dates and scope

6–11 October 2026. Month 04: React + TypeScript foundations.
See the [18-hour plan](week-13-plan.md) for daily packages and acceptance criteria.

## 6 October opening checkpoint

- Reviewed Week 12 closure and bootcamp handoff commit `5119d8d`.
- Confirmed local OpsDesk `main` is clean at `ec418f9` and equal to the locally
  recorded `origin/main`. This inspection did not fetch remote state.
- Confirmed `frontend/` is absent; Node `v25.2.1` and npm `11.6.2` are available.
- Recorded the Week 13 schedule and first learner exercise. Updated roadmap,
  weekly status, README navigation, and local mentoring context.
- No frontend commands, learner implementation, frontend checks, or product commits
  have run yet. The planned product branch has not been created.
- Bootcamp planning edits are uncommitted at this checkpoint.

## 6 October setup checkpoint

- Learner created `feature/week-13-react-foundation` and scaffolded `frontend/`
  with Vite's `react-ts` template, selecting ESLint and automatic installation/start.
- Supplied terminal evidence reports 160 packages added, zero audit findings at
  installation time, and Vite `8.3.3` serving on local port 5173.
- Read-only inspection confirms the branch and untracked `frontend/` directory.
  The generated App still contains the template UI and counter.
- Package scripts are `dev: vite`, `build: tsc -b && vite build`, `lint: eslint .`,
  and `preview: vite preview`. No behavior-test script is configured yet.
- The development server started; browser display, build, and lint remain unverified.
  Installation/start does not establish those checks. No product commit yet.

## Remaining work and time

Tuesday's learning, implementation, verification, and local product commit are
complete. The full week remains budgeted at 18 hours, with 14.5 planned hours for
Wednesday–Sunday. These are planning estimates, not measured durations. Active-time
reporting is optional and is not a closure requirement. Bootcamp planning, notes, and
Tuesday evidence are grouped in the daily documentation commit.

As of 9 October, Tuesday–Thursday are committed and pushed in both repositories.
Friday's controlled Login demo, 12-test verification, browser review, learning answer,
documentation, and both repositories' commit/push closure are complete.
Saturday–Sunday retains 5.5 planned hours for the Register demo, its tests, review,
and weekly closure. These allocations are estimates, not measured time spent.

## 6 October static-shell review

- Learner implemented typed `AppHeaderProps`, a presentational header, App composition,
  semantic header/main regions, minimal CSS, and the OpsDesk document title.
- Review found no blocking functional issue in this static exercise. Normalized three
  trailing spaces in App and the missing final newline in AppHeader; no logic changed.
- `npm run lint` passed. `npm run build` passed TypeScript checking and Vite bundling.
- Browser inspection showed the heading, subtitle, and mock-data explanation with
  readable layout and no starter counter. Captured warning/error logs were empty.
- Updated product-root and frontend READMEs with current scope, setup, scripts,
  source layout, and test/CI boundaries. Lockfile versions: React/React DOM 19.3.0,
  TypeScript 6.0.3, Vite 8.3.3. Package manifest ranges are not resolved versions.
- Recorded the learner's correct props/reuse explanation with a precision correction:
  the component has an explicit props dependency rather than no external dependency.
- Added [foundation review notes](../notes/react/react-typescript-foundations.md).
- Learner delegated README and documentation maintenance to the mentor; implementation
  and concept exercises remain learner-owned. No behavior-test runner is installed.
- Product changes remain uncommitted on `feature/week-13-react-foundation`.

## 6 October type-error experiment

- Learner screenshots prove `productName={123}` produced TS2322 during
  `npm run build`, identifying the required string type in AppHeaderProps.
- The restored string removes the editor diagnostic. Local source inspection confirms
  `productName="OpsDesk"` and removal of the temporary experiment.
- The final post-experiment build output is not yet supplied; earlier shell build/lint
  and browser checks remain recorded separately at this checkpoint.
- Git inspection still shows modified product README and untracked frontend files on
  `feature/week-13-react-foundation`; no commit has been made by the mentor.

## 6 October daily closure

- Learner supplied a successful post-experiment `npm run build`: TypeScript passed
  and Vite 8.3.3 generated the production bundle. Earlier lint and browser checks
  passed; no new behavior-test claim is made for this static exercise.
- Staged whitespace check passed. The staged inventory includes the npm lockfile
  and source/configuration files, not node_modules or dist.
- Learner created product commit `781e74b` — `week-13: add React TypeScript frontend
  shell` — on `feature/week-13-react-foundation` (21 files changed).
- Independent local Git inspection confirms that commit, branch, and clean working
  tree. Push, PR, hosted CI, and merge are not established by this local evidence.
- Tuesday's technical package is complete; no technical carry-over. Bootcamp evidence
  is included in the daily documentation commit with message
  `week-13: record React shell and Tuesday closure`.
- Next session: Wednesday 7 October, approximately 3 planned active hours for state,
  events, conditional rendering, local screen selection, and the first meaningful
  frontend behavior test. Explain with a small analogy before the learner implements.
- This closes Tuesday's package, not Week 13 as a whole.

## Time tracking and documentation ownership clarification

The learner clarified that previous daily durations were planning estimates and
active-time reports were not part of the workflow. Historical Week 09–12 reports
explicitly state that actual hours were not measured. Removed the newly introduced
Week 13 mandatory time-report requirement; optional feedback can improve estimates,
but missing duration data is not unfinished work. The mentor owns documentation and
its daily/milestone Git checkpoint. Tuesday's documentation commit was initially
omitted from the closure and is being completed with this evidence package.

## 6 October publication evidence

- Learner terminal output confirms bootcamp `main` pushed from `5119d8d` to `ef0e94f`.
- OpsDesk `feature/week-13-react-foundation` was pushed and upstream tracking set;
  its current product commit is `781e74b`. This is branch publication, not a PR/merge.

## 7 October opening checkpoint

- Local inspection confirms clean bootcamp at `ef0e94f` and clean OpsDesk on
  `feature/week-13-react-foundation` at `781e74b`. OpsDesk HEAD equals its locally
  recorded upstream; no fresh fetch was performed.
- Reviewed the shell, header, package scripts, and Vite/TypeScript configuration.
  No test script is configured yet.
- Prepared the approximately 3-hour state/events/screen-selection/test package.
  Wednesday implementation and verification are pending learner work.
- Documentation remains mentor-owned. Daily closure includes review, documents,
  commit, push, and verification; active-time reporting is optional.

## 7 October screen-selection review

- Learner implemented one `Screen` union state with initial Tickets, three button
  handlers, conditional screen sections, aria-pressed selection, and focus styles.
- Learner correctly explained why independent boolean flags could represent multiple
  active screens, whereas one union state represents a single selected screen.
- Browser review verified Tickets → Login → Register → Tickets, replacement of old
  content, corresponding pressed states, and Tab/Enter activation of Register with
  a visible focus ring. Captured warning/error logs were empty.
- ESLint passed. Git whitespace check found trailing spaces in App.tsx; learner
  cleanup is pending. Current diff has only App.tsx and App.css changes.
- Existing visual design is sufficient for this foundation. Suggested only wrapping
  the button row on narrow widths and narrowing CSS transitions to intended properties.
  No broader dashboard or styling framework is needed.
- Next: learner installs the test dependencies and implements the grouped config,
  cleanup setup, and App behavior tests. Tests and final build are not yet verified.

## 7 October test review and technical completion

- Learner supplied Vitest 4.1.11 output: one test file and three passing tests.
  The same terminal package passed TypeScript/Vite build and ESLint. Its final
  warnings came from `git diff --check`, not ESLint.
- Reviewed all tests: initial Tickets with absent Login/Register headings; Login
  selection and return to Tickets; Register selection with other headings absent
  and the other buttons unpressed. Queries use accessible roles/names, interactions
  are awaited, and afterEach cleanup isolates each rendered tree.
- Configuration correctly reuses the React Vite plugin, sets jsdom, imports DOM
  matchers through the Vitest entry point, and exposes run-once/watch scripts.
- Learner added navigation wrapping and targeted color transitions. Mentor removed
  only App.tsx trailing whitespace; Git whitespace check then passed. No behavior
  changed after the supplied passing test/build/lint package, so those checks were
  not repeated for documentation/whitespace-only edits.
- Updated product and frontend READMEs with actual screen-selection/test scope,
  scripts, source layout, and browser/jsdom/CI boundaries. Forms and Ticket rows are
  still future work; no backend/API or authentication changes were made.
- Wednesday's implementation, learning review, behavior tests, and browser evidence
  are complete. Product and bootcamp commit/push evidence remains pending; do not
  claim a clean published state until those operations finish.
- Suggested product commit: `week-13: add screen selection and behavior tests`.
  Suggested evidence commit: `week-13: record screen selection and test evidence`.
- Next learning package: 8 October typed mock Tickets, list rendering, stable keys,
  and populated/empty list tests (approximately 3 planned hours).

## 7 October publication evidence

- Learner terminal output confirms OpsDesk `5f7f5c3` committed and pushed on
  `feature/week-13-react-foundation`, and bootcamp `b32dadf` committed and pushed
  on main. Both final working-tree status outputs were empty.
- Wednesday's Git closing step is complete. PR/merge is not claimed.

## 8 October opening checkpoint

- Local inspection confirms clean bootcamp at `b32dadf` and clean OpsDesk at
  `5f7f5c3`, still on `feature/week-13-react-foundation`. Product HEAD equals the
  locally recorded upstream; no new remote fetch was performed.
- Prepared a 3-hour typed mock Ticket-list package with populated/empty tests and
  App navigation regression. Current three tests are previous evidence, not rerun
  results for Thursday.
- Checked backend Ticket vocabulary: open/in_progress/resolved/closed and
  low/medium/high/urgent. The frontend display type is deliberately smaller than
  the backend Ticket representation; this week still has no real API integration.
- Implementation and Thursday checks remain learner work. No time report is required.

## 8 October mock Ticket review and verification

- Learner implemented typed status/priority/summary declarations, three synthetic
  records, and a props-driven TicketList. It uses fixed ticketId keys, displays each
  row's title/ID/status/priority, and renders an explicit empty-state message.
- App now supplies mock data to the list in the Tickets screen. Existing navigation
  tests also verify list presence, removal on Login/Register, and restoration.
- Two isolated TicketList tests use independent fixtures and within() to verify
  each row's own fields; the empty test confirms no list or items are rendered.
- Learner's test/build/lint package passed with five tests in two files. Git reported
  trailing spaces in App; review also found them in the new untracked list test.
- Mentor removed trailing spaces, added flex-wrap to Ticket metadata for narrow
  screens, and added role="list" because list-style:none can suppress native list
  accessibility semantics in Safari. No list/business logic was replaced.
- After those fixes, mentor reran all five frontend tests, TypeScript/Vite build,
  ESLint, and Git whitespace checks successfully.
- Browser verification displayed all three mock records, exposed the named list,
  removed it on Login, and restored it on Tickets. A 375px viewport confirmed
  readable wrapped metadata. Captured warning/error logs were empty.
- The development server was initially stopped; mentor started a loopback-only
  temporary server for inspection and stopped it afterwards. Browser startup had a
  prolonged tool delay; it is not learner active time.
- Product and frontend READMEs now describe actual mock-list scope and five tests.
  Forms, API requests, token handling, and backend mutations remain outside this slice.
- Remaining: stable-key learning answer and product/bootcamp commit and push evidence.
  Suggested messages: `week-13: add typed mock ticket list and tests` and
  `week-13: record mock ticket list evidence`. No Thursday publication claimed yet.

## 8 October closure and learning correction

- Learner terminal evidence confirms product commit `dcae2ba` pushed on the feature
  branch and bootcamp commit `e355fa0` pushed on main, with empty final status output.
- Learner correctly identified index-key state misassociation after inserting a row.
  Clarified that index keys do not necessarily rebuild the whole list and stable keys
  do not prevent renders or guarantee a performance gain; preserving item identity
  and associated state is the central purpose. Thursday is complete.

## 9 October opening checkpoint

- Local inspection confirms clean bootcamp at `e355fa0` and clean OpsDesk at
  `dcae2ba` on the existing feature branch. Product HEAD equals its locally recorded
  upstream; no fresh fetch or test rerun at opening.
- Reviewed backend LoginRequest and normalization: email/password fields, strict
  email normalization, and NFC password validation with a 15–128-code-point bound.
- Friday's local form has an explicitly smaller UX-validation scope (required fields
  and a basic email-shape check). It must not claim backend validation parity or
  actual credential verification. Real integration remains Week 14 planning work.
- Saved the 3-hour controlled-login-form package; implementation and checks pending.

## 9 October Login form first review

- Learner implemented controlled email/password fields, form-owned feedback,
  preventDefault/noValidate submission, ordered local checks, alert/status messages,
  stale-feedback clearing, and password clearing after demo success. App wiring and
  form styles are present; no network/storage/authentication logic was introduced.
- Supplied terminal evidence reports 11 passing tests (6 LoginForm, 3 App, 2 TicketList),
  successful TypeScript/Vite build and ESLint. Tracked-file whitespace check is clean.
- Code review found the final LoginForm test's name claims error/success clearing,
  but its body only verifies error clearing when email changes. Request one additional
  test for clearing a success status when password is edited, and rename the existing
  test to describe its actual coverage. Product behavior appears correct; regression
  evidence is incomplete for the accepted success-feedback requirement.
- The two new untracked LoginForm files still contain trailing whitespace, which
  plain git diff --check does not inspect. Include their cleanup in the same learner
  edit package; no need for new formatter dependencies.
- Remaining: focused test correction, browser/keyboard verification, final docs,
  controlled-input learning answer, and both repositories' commit/push closure.

## 9 October Login form final review

- Learner renamed the error-clearing test and added an independent test proving that
  editing password after demo success removes the status and leaves no alert.
- Supplied terminal output at 14:31 reports 12 passing tests across three files:
  seven LoginForm, three App, and two TicketList. TypeScript/Vite build and ESLint
  passed; tracked-file git diff --check produced no warnings. These checks were
  learner-run; the mentor did not rerun the suite for documentation-only changes.
- Browser verification confirmed empty-submit feedback, corrected synthetic input
  submitted with Enter, the explicit demo status, retained email, cleared password,
  and status removal after password editing. Tab moved focus from email to password
  with a visible focus indicator. Captured warning/error logs were empty.
- Reviewed source and tests: form state stays local, validation is bounded UX only,
  and there is no request, storage, token, or authentication behavior.
- Learner correctly explained that value makes React state authoritative. Refined
  the explanation: React restores the input to the supplied value when synchronous
  onChange state updates are missing; lack of a render alone is not the cause.
  Rendering for another reason would still supply the same unchanged value.
- Mentor updated both product READMEs and learning records and removed three
  trailing-whitespace lines from the new LoginForm file without changing behavior.
  Plain git diff --check does not inspect untracked files; inspect them separately
  and use git diff --cached --check after staging.
- Friday implementation/review is complete. Both repositories' commits, pushes,
  and clean-status outputs remain pending. No Friday commit ID, hosted CI, PR, or
  merge is claimed. Next learning package: 10 October controlled Register demo.

## 9 October Git closure

- Learner supplied successful commit/push output for OpsDesk `7dab029` on
  `feature/week-13-react-foundation` and bootcamp `1febb25` on main.
- Both staged whitespace checks and final short-status outputs were clean.
  Friday is complete; no PR/merge or frontend hosted CI result is claimed.

## 10 October opening checkpoint

- Read-only local inspection confirms clean product at `7dab029` on the same weekly
  feature branch and clean bootcamp at `1febb25` before planning changes. No fresh
  remote fetch or test run was performed at opening.
- Reviewed RegisterUserRequest: only email/password are accepted; extra fields are
  forbidden. Backend normalizes email and NFC password with a 15–128-code-point
  bound. Today's demo retains Friday's smaller local UX-validation scope.
- Saturday adds RegisterForm with a UI-only confirmPassword field to practice
  comparing two controlled values. Confirmation is not an API field, and no request
  or account/session is created. App retains screen state; form owns field state.
- Saved the approximately 3-hour exercise, tests, browser acceptance, and learning
  question in the weekly plan. Implementation and verification remain learner work.

## 10 October Register first review

- Learner implemented local controlled email/password/confirmation state, ordered
  validation, field-edit feedback clearing, explicit demo status, and both-password
  clearing. App renders RegisterForm; existing form styles are reused.
- Learner terminal evidence at 17:46 reports 21 passing tests (9 RegisterForm,
  7 LoginForm, 3 App, 2 TicketList), successful build and lint. Mentor inspection
  confirms clean tracked diff whitespace and no trailing whitespace in TSX files,
  including the new untracked files. No test suite was rerun during this review.
- Browser verified mismatched-password alert, correction and Enter submission,
  explicit demo status, both-password clearing, and fresh fields/no feedback after
  switching to Tickets and back. Keyboard focus is visible; warning/error logs empty.
- Two existing feedback tests only edit confirmation despite names implying all
  fields. Request accurate names plus email-after-error and password-after-success
  coverage. App's reset test must establish feedback before leaving and assert it is
  absent on return. Group these changes with App's Register indentation cleanup and
  removal of obsolete edit-history JSX comments. No form logic bug found.
- Learner correctly distinguishes UI confirmation from account creation. Clarify
  that backend schemas need not mirror storage models; this API explicitly accepts
  only email/password and forbids extra fields. OpsDesk currently uses NFC password
  normalization and 15–128 code points, without special-symbol/breach-list checks.
  Account creation occurs at successful database commit; a 201 response acknowledges
  it, but response delivery can fail after commit. A timeout does not prove rollback.
- Remaining: focused learner test/format corrections, final verification, product
  README updates, and both repositories' commit/push closure.

## 10 October Register final review

- Learner corrected both confirmation-test names and added email-after-error and
  password-after-success clearing tests. Each establishes feedback before editing.
- App's Register test now creates a mismatch alert before leaving, then verifies
  empty fields and absent alert/status after returning. Register indentation and
  obsolete edit-history JSX comments are corrected. No form behavior change needed.
- Supplied terminal evidence at 17:57 reports 23 passing tests in four files:
  11 RegisterForm, 7 LoginForm, 3 App, 2 TicketList. TypeScript/Vite build and ESLint
  passed; git diff --check was silent. Source review confirms the requested changes.
  Earlier same-day browser evidence remains applicable: no form logic/styles changed.
- Mentor updated product-root/frontend READMEs for both implemented demos, test
  coverage, source layout, browser checks, and the explicit mock-only API boundary.
  Learning notes include the API-schema and commit-versus-response clarifications.
- Saturday implementation, learning review, tests, browser review, and documentation
  are complete. Commit/push and final clean-status evidence for both repositories
  remain pending. No Saturday commit, hosted frontend CI, PR, or merge is claimed.
- Next scheduled package is Sunday's weekly review and Week 14 dependency planning.
