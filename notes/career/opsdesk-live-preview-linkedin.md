# OpsDesk — first live preview LinkedIn draft

Historical draft checkpoint: 19 October. The text/counts below describe that
milestone and are not automatically the latest publication copy. Before posting,
reconcile them with [current status](../../WEEKLY_STATUS.md) and the Week 15
closure (latest local frontend count: 141 on 24 October). The current mock
dashboard is now deployed; real Ticket integration and AI remain future work.
Publication is still unconfirmed; this documentation correction does not post it.


Prepared 19 October 2026. Draft only; not published or sent to LinkedIn.

## Editorial direction

Previous supplied posts covered the backend foundation and the first tenant-scoped
backend flow, then announced the move into React/TypeScript. This update completes
that story with a working browser-to-database identity flow. Lead with something
people can try and one engineering lesson, rather than another long feature/test list.
Keep English to match the supplied posts. AI remains a future roadmap item.

## Publication checkpoint

The URL is already public and the learner verified browser behavior. Before a broad
test invitation, finish the bounded abuse/cost/data review in the Week 15 plan.
Current-head Backend and Frontend CI at `2f6e00d` were rechecked on 19 October and
both passed. Runtime SHA confirmation remains separate. Small manual feedback can
begin now. Furkan chooses when to publish; publication has not been confirmed.

## Ready-to-copy post

OpsDesk has moved from localhost to its first live web preview.

Six weeks ago, on September 7, I started OpsDesk as a separate project with requirements, data models and access rules. Today, you can try its first working browser-to-database flow.

In my last update, I shared the organization-scoped backend foundation and my plan to learn React and TypeScript. That frontend now connects to FastAPI and a hosted PostgreSQL database.

You can register, sign in, check your session and sign out in the browser.

The latest recorded local checks passed:
• 506 backend non-integration tests
• 110 frontend tests

PostgreSQL integration and migration checks run separately. I also verified the deployed registration, login and session flow in the browser.

My biggest lesson: a successful build is only part of deployment. Database migrations, application permissions, health checks and the API address in the frontend build all need to work together.

For this preview, FastAPI serves both the React build and the API from one origin on Railway.

What's next?

• Turn the deliberately simple interface into a more polished, responsive dashboard: clearer navigation, consistent spacing and typography, accessible forms, and useful loading, empty and error states.
• Connect the ticket UI to real organization-scoped data, then build out ticket details, filters, comments and status workflows.
• Add Docker-based development and background processing, followed by AI-assisted ticket summaries and priority/category suggestions—with tests and evaluation alongside them.

The goal is an interface that is easier to understand and use, supported by a backend whose behavior I can explain and verify.

This is still an early identity-flow demo. The three tickets shown are clearly labelled mock data. The full ticket experience and AI features are future work.

If you try it, use a made-up address such as your-name-demo-19@example.com and a password used only for this demo. Demo accounts may be reset; please don't enter real customer or support data.

I'd appreciate feedback: was any form, message or step confusing?

Live preview: https://opsdesk-production-448f.up.railway.app/
Code: https://github.com/ozdemirr1/opsdesk

#Python #FastAPI #React #PostgreSQL #BuildInPublic

## Visual to accompany the post

Furkan chose two still images instead of video. Upload in this order:

1. [Announcement cover](../../assets/linkedin/opsdesk-live-preview/01-cover.png):
   “From localhost to live preview.” Conceptual navy/cyan infrastructure artwork.
2. [Demo walkthrough](../../assets/linkedin/opsdesk-live-preview/02-demo-walkthrough.png):
   six numbered stages from registration to sign-out, with cursor annotations.

The walkthrough is an AI-assisted composition based on the supplied real app
screenshots, not an unmodified screenshot archive. The Mac Dock and system/browser
chrome are excluded; passwords remain masked. Tickets are explicitly labelled as
mock data in the footer. No AI or real Ticket UI capability is claimed.

[Artwork details and final prompts](../../assets/linkedin/opsdesk-live-preview/README.md)
record the source mapping and tool mode. Both final PNGs are saved in the repository;
original screenshots are unchanged. Nothing has been posted to LinkedIn.

For the post body, copy the plain `Live preview:` and `Code:` URL lines above.
The Markdown link labels used in chat are not placeholders to paste into the post.

## Featured link copy

Title: OpsDesk | Live Identity Preview

Description: Try the first live OpsDesk preview: registration, login, session checks
and sign-out with React, FastAPI and PostgreSQL. Tickets currently use mock data.
An actively developed backend-focused portfolio project.

Keep the existing GitHub featured link as a separate code/evidence entry.

## Feedback record

For each report, note browser/device, action, expected result, actual result and
a sanitized screenshot if needed. Never request the tester's password or token.
Ask testers to report privately through LinkedIn if an error contains account data.
