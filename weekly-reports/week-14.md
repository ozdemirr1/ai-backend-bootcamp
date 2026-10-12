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
