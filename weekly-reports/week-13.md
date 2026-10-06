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

The rest of the week: state/events, mock Ticket rendering, controlled login/register
forms, behavior tests, documentation, interview review, and Git closure.

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
