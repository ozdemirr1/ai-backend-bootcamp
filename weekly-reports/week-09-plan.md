# Week 09 Plan

## Date

7 September - 13 September 2026

## Estimated Active Time

15-20 hours across the week.

This estimate includes architecture discussion, design review, documentation,
repository setup, and issue planning. It does not assume that coding starts
before the domain boundaries are understood.

## Main Focus

- Begin the real OpsDesk product in a separate public repository
- Define product requirements and explicit non-goals
- Establish shared domain vocabulary and invariants
- Model organization-scoped membership and roles
- Design Ticket, Comment, and Attachment relationships
- Produce a relational ERD
- Produce an authorization matrix
- Define the initial API surface
- Convert the design into prioritized GitHub issues
- Begin a bounded internship and networking routine

## Main Goal

Finish Week 09 with an implementation-ready OpsDesk design. A developer should
be able to read the requirements, ERD, access matrix, endpoint inventory, and
issue backlog and understand what Week 10 must build without inventing core
business rules during implementation.

## Product Boundary

OpsDesk is a multi-organization support-ticket system. Month 03 focuses on a
serious backend foundation, not AI features or a frontend.

### In Scope

- User identity
- Organizations
- Organization membership
- Organization-scoped roles
- Tickets and their lifecycle
- Comments
- Attachment metadata
- Access-control rules
- API contracts and failure behavior
- Test and delivery strategy

### Out of Scope for Week 09

- Full CRUD implementation
- React frontend
- Docker and Docker Compose
- Redis and background jobs
- AI summarization, categorization, or priority suggestion
- File-object storage implementation
- Refresh tokens, MFA, billing, and enterprise SSO
- Premature microservices or asynchronous database migration

## Domain Decisions to Resolve

### User and Organization Membership

A User is a global identity. A role should not be a permanent global property
of that identity because one User may be an administrator in one Organization
and a customer in another.

```text
User 1 ---- * OrganizationMembership * ---- 1 Organization
                         |
                         v
                owner/admin/agent/customer
```

The role therefore belongs to `OrganizationMembership`. Database uniqueness
should prevent the same User from holding duplicate memberships in one
Organization.

### Ticket Participants

The terms must be separated before choosing columns:

- Organization: the tenant boundary that owns the Ticket
- Requester: the member who asks for support
- Assignee: the agent currently responsible for handling the Ticket
- Creator: the identity that submitted the record, when auditing requires it

The word “owner” must not ambiguously mean both organization ownership and
Ticket responsibility. Week 09 will choose precise names and document their
invariants.

### Roles

- `owner`: controls the Organization and its membership
- `admin`: manages organization operations without owning the tenant
- `agent`: works assigned or visible support Tickets
- `customer`: creates and follows permitted Tickets

These labels are only a starting vocabulary. The access-control matrix is the
authority for what each role can actually do.

### Ticket Workflow

- Status: `open`, `in_progress`, `resolved`, `closed`
- Priority: `low`, `medium`, `high`, `urgent`

The design must specify who can perform each transition and which transitions
are invalid. Enum values alone do not define a workflow.

## Required Entities

- `User`
- `Organization`
- `OrganizationMembership`
- `Ticket`
- `Comment`
- `Attachment`

For each entity, document:

- purpose and lifecycle
- stable identity
- required and optional fields
- uniqueness rules
- relationships and deletion behavior
- trusted writer for sensitive fields
- invariants that belong in domain logic
- constraints that belong in PostgreSQL

## Required Outputs

- [x] Separate public `opsdesk` repository
- [x] Product problem statement and target users
- [x] Functional requirements (initial scope)
- [x] Non-functional requirements (initial security requirement)
- [x] Explicit non-goals
- [x] Domain glossary
- [ ] Entity and relationship decisions (domain rules reviewed; relational details pending)
- [ ] Mermaid ERD
- [ ] Organization role/permission matrix
- [ ] Ticket status-transition matrix
- [ ] Initial API endpoint inventory
- [ ] Error and pagination contract sketches
- [ ] Prioritized GitHub issue list with acceptance criteria
- [ ] Week 10 implementation sequence
- [ ] Week 09 report and interview review

Monday evidence: [OpsDesk](https://github.com/ozdemirr1/opsdesk), initial commit
`eb0e20e`. README and `docs/requirements.md` contain the reviewed initial scope
and three acceptance scenarios. Assignment, visibility, and status-transition
policies remain open. The checked scope outputs do not satisfy the full
implementation gate or complete the Week 09 architecture interview review.

Tuesday evidence: Furkan drafted all six entities and reviewed the ownership,
membership, Ticket participation, assignment-handover, Comment, and Attachment
policies. OpsDesk's `docs/domain-model.md` consolidates these decisions in commit
`0dab9c4`, which has been pushed on `feature/week-09-domain-design`. The previous
remote branch name was removed. The README and requirements reference
the model. The seven-question daily review is complete;
ERD, physical relationships, full access/transition matrices, and the end-of-week
architecture review remain pending. No executable code or application tests exist.

## Daily Plan

### Monday - Handoff, Scope, and Repository Foundation (2-3 hours)

- Read the Month 02 to Month 03 handoff in the new Codex conversation.
- Confirm this learning repository is clean and synchronized.
- Review the OpsDesk problem, actors, goals, constraints, and non-goals.
- Create the separate public `opsdesk` repository only after its purpose and
  initial structure are agreed.
- Add a focused product README and design-document locations.
- Do not copy the Month 02 learning API wholesale into the new product.

### Tuesday - Domain Language and Invariants (2.5-3 hours)

- Define User, Organization, Membership, Ticket, Comment, and Attachment.
- Separate global identity from organization membership.
- Separate requester, assignee, creator, and organization-owner terminology.
- Define lifecycle and invariant candidates before database columns.
- Record decisions that would otherwise be rediscovered during Week 10.

### Wednesday - Relational Design and ERD (3-4 hours)

- Translate the domain into tables, keys, foreign keys, and uniqueness rules.
- Decide required versus nullable relationships from lifecycle evidence.
- Specify deletion behavior deliberately.
- Model attachment metadata without implementing object storage.
- Produce and review the Mermaid ERD.

### Thursday - Authorization and Workflow Matrices (3-4 hours)

- Define organization-scoped permissions for owner, admin, agent, and customer.
- Define Ticket visibility, mutation, assignment, commenting, and closing rules.
- Define valid status transitions and the actor allowed to perform each one.
- Test the design using concrete cross-organization and cross-role scenarios.
- Identify likely BOLA and privilege-escalation threats.

### Friday - API Contract Inventory (2.5-3.5 hours)

- Convert use cases into resource-oriented endpoints.
- Define authentication and organization-context expectations.
- Sketch request/response boundaries without implementing every schema.
- Assign expected success and failure status codes.
- Record pagination and standard-error needs for Week 11.

### Saturday - Issues, Sequencing, and Minimal Automation (2-3 hours)

- Turn approved design slices into small GitHub issues.
- Add acceptance criteria, dependencies, and labels.
- Order Week 10 work by vertical slices rather than by database files alone.
- If a minimal executable Python package and meaningful tests now exist, add
  basic CI for locked installation, Ruff, and pytest. Otherwise schedule it as
  the first suitable Week 10 issue.
- Do not add a Docker build before a real Dockerfile exists.

### Sunday - Review, Report, and Career Routine (1.5-2 hours)

- Review ERD, matrices, endpoints, issues, and unresolved questions together.
- Complete the Week 09 architecture interview review.
- Write the Week 09 report and prepare Week 10.
- Begin a bounded networking routine: update the project narrative, identify a
  small set of relevant people or organizations, and record one concrete
  outreach or internship-preparation action without displacing engineering
  work.

## Initial Endpoint Areas

The final list is a Week 09 output, but design should cover:

- authentication and current identity
- organizations and membership
- Tickets and status changes
- assignment
- comments
- attachment metadata
- privileged membership and organization administration

Endpoints will be named only after resource ownership and authorization rules
are clear.

## Test Strategy to Design

- Domain invariant tests
- Request/response validation tests
- Service and repository contract tests
- PostgreSQL integration tests
- Authentication tests
- Organization-isolation and role-permission tests
- Ticket workflow tests
- Error-contract tests
- Pagination tests

Week 12 requires at least 25 tests, but the goal is meaningful risk coverage,
not merely reaching a number. The Month 02 experience already demonstrates
that fast tests and guarded database tests serve different purposes.

## GitHub Issue Quality Rule

Each implementation issue should state:

- user or system outcome
- scope and explicit exclusions
- acceptance criteria
- relevant authorization rule
- expected tests
- dependencies on earlier issues

Avoid one issue named “build backend.” The backlog should be small enough that
each completed issue produces reviewable evidence.

## Definition of Done

Week 09 is complete when:

- OpsDesk has a dedicated repository and clear product statement.
- Functional and non-functional requirements are explicit.
- Entity names and relationships are unambiguous.
- Organization roles live on membership rather than the global User.
- Ticket participant names and lifecycle rules are documented.
- The ERD can support the planned Month 03 workflows.
- The permission and transition matrices answer concrete scenarios.
- The endpoint inventory matches the domain and access rules.
- GitHub issues contain acceptance criteria, test expectations, and sequence.
- CI has either been added to meaningful executable code or assigned to the
  earliest appropriate implementation issue.
- The original Month 02 deployment carry-over has an explicit Month 03 path.
- The design can be explained in the Week 09 interview review.

## Guardrails

- Do not copy the learning application into OpsDesk without re-evaluating its
  domain assumptions.
- Do not put organization roles directly on the global User.
- Do not use one ambiguous `owner_id` for every business relationship.
- Do not confuse authentication with organization authorization.
- Do not start CRUD before requirements and access rules are reviewable.
- Do not add framework abstractions without a current use case.
- Do not start Docker, Redis, React, or AI work early.
- Do not commit credentials, local paths, `.env`, or complete tokens.
- Keep the first persistence path synchronous unless a demonstrated need
  changes the decision.
