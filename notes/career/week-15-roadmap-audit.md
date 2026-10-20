# Week 15 roadmap and Git audit

Recorded 19 October 2026. Repository review, not a new runtime regression or
market survey. No commits, pushes, merges or deployments were performed.

Historical checkpoint: the [20 October alignment review](../react/month-04-alignment.md)
supersedes this audit's recommendation to defer dashboard work until after Week 15.
The documentation package was subsequently committed/pushed as `3be0f38`.

## Direction and weekly scope

The path remains aligned with backend-focused junior/full-stack development:
Python/FastAPI, PostgreSQL and transaction/authorization fundamentals now connect
to a React/TypeScript browser and a bounded hosted preview. Keep the existing stack.
Docker/Redis and AI should stay in their planned phases rather than being added
to make the demo announcement broader.

Week 15's 18-hour budget includes review and documentation, with Wednesday optional.
Deployment happened early; reuse the remaining allocation for verified operation
and feedback rather than repeating provisioning. Abuse controls and restore work
are the two estimation risks. Narrow unfinished work and record it explicitly;
do not turn a three-hour exercise into a hidden multi-day infrastructure package.

The main direction risk is spending the rest of Month 04 on hosting/publication
while frontend work remains deferred. At handoff, select one existing-API-backed
Organization screen and a bounded responsive/accessibility pass. A full dashboard,
all Ticket workflows and AI are not a one-week package. Styling should improve
navigation, feedback, readability and mobile use, not just visual decoration.

## Documentation and structure

- Product code remains in the separate OpsDesk monorepo; bootcamp contains notes,
  evidence and historical learning projects. Stable module names are appropriate.
- The old long status file is archived; current status is short and links to history.
- Added the missing [Month 03 retrospective](../../monthly-reports/month-03.md)
  using existing weekly evidence, including the delayed deployment milestone.
- Updated current CI statements; retained dated historical queued checkpoints.
- Added the publication-assets directory to README navigation. The two PNGs total
  approximately 3 MB; no raw desktop screenshot archive is needed in Git.
- AGENTS.md is intentionally ignored/local. Historical Decision 003–014 database
  examples concern the Month 02 learning API. OpsDesk product tests are guarded to
  `opsdesk_product_test`, development uses `opsdesk_product_dev`, and hosted preview
  uses `opsdesk_demo`; never substitute the old learning database names in product
  commands. The product README and executable guards define those targets.

## GitHub comparison

Live `git ls-remote --heads` and GitHub CLI results:

| Repository/ref | Local and GitHub SHA | Meaning |
| --- | --- | --- |
| bootcamp main | `42cf59c821158344324ef818646940aaa2bb185d` | Committed history matches; documentation/assets remain uncommitted locally |
| OpsDesk main | `b0e6cab7d43995acbd6b499cf26a72b629ba574a` | Week 14 merged baseline |
| OpsDesk feature/week-15-railway-preview | `2f6e00d5157d820adbd54dcc20464cee917c6bf3` | Clean and pushed; three commits ahead of main |

No open PR exists in either repository at this checkpoint. No bootcamp Actions
runs were returned. OpsDesk [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39281732888)
and [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39281732882)
both succeeded at the feature head. The merged Week 14 feature branch still exists
locally/remotely; cleanup is optional and was not performed.

Working-tree equality and commit equality differ: bootcamp's committed history is
in sync, but GitHub cannot see its current local documentation and images yet.
OpsDesk feature/main inequality is expected before the weekly normal PR merge.
CI success does not prove the exact SHA running in Railway; that check remains open.

## Publication package and remaining work

Bootcamp commit candidates: README, ROADMAP, WEEKLY_STATUS, Week 14 closure,
Week 15 plan/report, archived status, Month 03 retrospective, deployment notes,
career draft/audit and the two final images with their production notes. Review
and publish this documentation package separately from product code. Use an
explicit file list, a week-based feature branch/commit and a normal PR merge.

OpsDesk has no pending local push. Week 15 PR/review/normal merge remains future
closure work; do not merge just to make main equal to the feature branch midweek.

Still open: runtime SHA, public negative/reload/recovery cases, bounded abuse
review/control evidence, credit/export/restore/rollback evidence, then weekly
review and post-merge deployment smoke. No broad production-readiness claim follows
from a successful identity demo. Current frontend and backend test totals remain
recorded evidence; they were not rerun for this documentation-only audit.
