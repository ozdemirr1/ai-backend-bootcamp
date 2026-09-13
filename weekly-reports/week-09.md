# Week 09 Report

## Date

7-13 September 2026 — Month 03

## Result

Established OpsDesk as a separate public product repository and reviewed its
requirements, domain, relational model, authorization rules, lifecycle, and
22-endpoint API baseline. Published 26 bounded GitHub issues with priorities,
acceptance criteria, test expectations, and dependency links.

This is design and planning evidence. No OpsDesk runtime, applied migrations,
application tests, CI, or deployed backend exists yet. The Month 02 learning API
remains a separate historical project; its test results are not OpsDesk results.

The broad domain and backlog review is complete. Precise validation, identity,
remaining API contracts, and concurrency decisions are explicit prerequisites
in design issues #1-#4, rather than silently treated as settled.

## Outputs

- [OpsDesk repository](https://github.com/ozdemirr1/opsdesk)
- Requirements and explicit Month 03 exclusions
- Six-entity domain and relational design, including conceptual Attachment metadata
- Mermaid ERD with organization-scoped participant relationships
- Role/resource access matrix and Ticket state-transition rules
- API baseline covering 22 endpoints, errors, pagination, and response examples
- [Published issue index](https://github.com/ozdemirr1/opsdesk/blob/feature/week-09-domain-design/docs/issue-plan.md)
- [GitHub backlog](https://github.com/ozdemirr1/opsdesk/issues): 26 issues, eight labels
- Completed daily learning reviews and Sunday architecture review
- [Week 10 implementation handoff](week-10-plan.md)

## Main Design Decisions

- User identity is global; roles belong to OrganizationMembership.
- One membership exists per User-Organization pair across active/inactive states.
- Composite foreign keys enforce tenant-consistent Ticket participants and children.
  Active-state checks, permissions, and workflow rules remain separate concerns.
- An active Organization requires exactly one active owner belonging to an active
  User. The partial unique index enforces only the at-most-one membership rule.
- Ticket requester and creator are server-derived and fixed; assignee may change
  through authorized workflows. New Tickets are open and unassigned.
- Customers see their requested Tickets; staff see their Organization's Tickets.
  Visibility alone grants neither mutation permission nor unrestricted assignment.
- Closed is terminal. Authorized reopening of resolved Tickets preserves an eligible
  assignee and clears an ineligible one in the same coordinated transaction.
- Comments are append-only for all roles. Closed Tickets remain readable under
  visibility rules but accept no new comments. Internal notes are deferred.
- Attachment metadata remains a design topic; its API and physical storage are deferred.
- Integration tests will use real commits and separate cleanup transactions against
  the exact guarded test target, with explicit allowlists and sequential scopes.

## Learning Review and Precision Corrections

Furkan correctly explained contextual roles, tenant constraints versus permission,
owner-index limitations, real-commit rollback boundaries, current identity checks,
planning versus completion, and independent-session persistence verification.

- Atomic ownership transfer means both changes commit or neither commits; SQL
  statements need not execute simultaneously. Constraint timing and a cooperating
  concurrency protocol must be designed. Locks do not replace authorization checks.
- Cleanup first validates the exact `opsdesk_test` database and allowed server.
  Only allowlisted tables are cleared, in foreign-key-safe order, while preserving
  migration history. Sessions are closed and unfinished transactions rolled back.
  Cleanup failures remain visible and block subsequent scopes; hard termination
  cannot guarantee teardown, so validated startup cleanup handles leftovers.
- A closed issue is not sufficient evidence. A design task needs reviewed decisions
  and examples in the product contract; implementation needs relevant checks and
  committed behavior. Administrative closure or cancellation proves neither.
- Ticket creation #18 depends on #1, #3, #4, #8, #13, and #10. Finalizing title and
  description rules alone does not provide schema, identity, errors, or coordination.
- Independent-session checks verify relevant durable state, not just an ORM object.
  Compare status, assignment, timestamps, and created child records as applicable;
  intended rejection logs may still be written.
- GitHub tracks current work status and discussion. Product documents describe the
  current accepted contract; closed design issues retain decision history. Local
  issue files preserve their initial published scope.

## Verification Evidence

- Local Markdown links/anchors, tables, fences, JSON examples, and whitespace checked.
- Dependency graph checked for cycles; all 22 endpoints mapped to implementation work.
- GitHub read-back verified all 26 issue titles, planning IDs, labels, and dependency URLs.
- Publication helper checked offline for existing-issue reuse, repeat execution, and
  dependency URL mapping. This is tooling verification, not an OpsDesk application test.
- Dependency URLs in issue descriptions are ordinary links; native GitHub blocking
  relationships have not been configured by this publication workflow.

## Git Evidence

OpsDesk feature branch: `feature/week-09-domain-design`.

| Day | OpsDesk commit | Outcome |
| --- | --- | --- |
| Monday | `eb0e20e` | Scope and repository foundation |
| Tuesday | `0dab9c4` | Domain design and review |
| Wednesday | `e021f17` | Relational design and ERD |
| Thursday | `196c1b2` | Access control and lifecycle |
| Friday | `35ba9b5` | API contracts and release boundaries |
| Saturday | `8d546bd` | Initial issue drafts and dependencies |
| Sunday | `3ad42fe` | Consolidated 26-issue backlog |
| Sunday | `08717e6` | Published issue links and completed review records |

Furkan supplied successful commit/push evidence for these milestones. The final
OpsDesk publication commit `08717e6` is pushed; the supplied terminal output confirms
a clean working tree synchronized with the remote feature branch. Bootcamp closing
documents still await his staged review, commit, and push. Final PR/merge evidence
is not yet recorded here.

## Variance and Carry-Over

- Initial Week 09 ambition was a fully implementation-ready design. Core rules and
  backlog are reviewed, but #1-#4 retain precise decisions that block dependent work.
- Saturday's unfinished backlog work moved to Sunday. Actual hours were not tracked;
  estimates are not evidence of time spent.
- Month 02 CI/deployment carry-over has concrete paths: #9 fast CI after meaningful
  tests, #25 guarded PostgreSQL CI, and #26 the Month 03 backend preview.
- No internship application, outreach, or completed networking action was evidenced
  this week. Carry one bounded action into Week 10 and record the actual result.
- Docker, frontend, Redis/jobs, and AI remain in their scheduled later phases.

## Closure Status

Technical review, published backlog, report, and Week 10 handoff are prepared.
OpsDesk publication commit/push is verified; bootcamp closing Git evidence is pending.
No implementation issue is marked complete merely
because its description has been published.
