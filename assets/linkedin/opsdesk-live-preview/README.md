# OpsDesk live-preview LinkedIn artwork

Prepared 19 October 2026. Built-in image_gen tool, via imagegen skill; no CLI/API fallback.

## Deliverables

1. [Cover](01-cover.png) — conceptual announcement artwork, not an application screenshot.
2. [Demo walkthrough](02-demo-walkthrough.png) — AI-assisted composition based on Furkan's real screenshots; six numbered identity-flow stages. Screen regions were recomposed by the image tool, so this is an illustrated walkthrough rather than an unmodified screenshot archive.

Both images use a 4:5 portrait layout. Upload the cover first, walkthrough second. The app's Mac Dock, menu bar and browser chrome are excluded. Passwords remain masked. The footer states that Tickets use mock data. Original screenshots are unchanged.

## Source mapping for walkthrough

- 01 Create an account: 19.27.20 screenshot.
- 02 Registration confirmed: 19.27.26 screenshot.
- 03 Sign in: 19.28.04 screenshot.
- 04 Signed in and 05 Check your session: two details from the 19.28.17 screenshot.
- 06 Sign out: 19.28.27 screenshot.

The 19.25.49 Ticket-list and redundant 19.28.10 signed-in screenshot were omitted to keep the identity-flow illustration readable.

## Final cover prompt

Use case: ads-marketing.
Create one polished LinkedIn announcement cover for OpsDesk, portrait 4:5, ideally 2048 x 2560. This is image 1 of a coordinated two-image post. Visual identity: deep midnight navy, cyan and turquoise accents, white typography, elegant restrained 3D infrastructure illustration, premium editorial graphic design. Headline dominates top half with generous margins and excellent mobile readability.
Exact text:
small upper eyebrow "OPSDESK / DEVELOPMENT UPDATE"
large headline "From localhost"
large cyan headline "to live preview."
supporting line "React + TypeScript · FastAPI · PostgreSQL"
Lower illustration: a beautifully rendered glass browser-window symbol connected by thin cyan light paths to an API module and PostgreSQL-style database cylinder on a minimal architectural platform. Browser contains only abstract interface lines and a small checkmark, NOT a fictional finished dashboard. Show the concept of browser to API to database, purposeful composition, subtle dark technical grid, soft studio light, no chaotic neon or excessive decoration.
Under illustration three small editorial labels "Register" "Sign in" "Check session"
Lower caption "A working identity flow, now in the browser."
Small clear footer note "Early demo · Ticket list uses mock data"
Author footer "Furkan Özdemir"
Use clean precise sans serif typography with expressive hierarchy, no logos that imply endorsement, no desktop furniture, no Mac menu bar or Dock, no screenshots needed, no extra claims about AI or a finished ticket product. All specified text legible and exact. Produce a single finished cover, not mockups of a social post or multiple alternatives.

## Final walkthrough prompt

Use case: compositing. Create ONE finished high resolution LinkedIn infographic image, portrait 4:5, ideally 2048x2560. Companion to a midnight navy/cyan OpsDesk announcement. Combine the FIVE supplied real application screenshots into an elegant SIX-step, 2-column, 3-row sequence (input4 used for two different focused crops). Each input is a screenshot/compositing source. Preserve actual application contents and blue/white UI, do not invent a better dashboard. Crop away ALL Mac Dock, menu bar, desktop, Safari chrome and excessive white space from each screenshot; only meaningful app regions should appear. Faithful screenshot crops are paramount. Each screenshot region should be enlarged enough to read. Use focused close-up crops rather than tiny full desktops. Navy page with turquoise numbered step circles, white panel frames, thin restrained arrows between steps, generous margins. Large modern typography and balanced consistent spacing.
Top eyebrow "OPSDESK / LIVE PREVIEW"
Large title "Try the identity flow."
Subtitle "Register. Sign in. Check your session. Sign out."
Six panels, reading left to right and top to bottom:
01 "Create an account" — input1 registration form crop: email, masked password, confirm password, blue Create account button. Add a crisp black mouse pointer with white border and small cyan click ring near Create account button edge; don't cover label. Email "Opsdesk-demo@example.com". Password stays masked.
02 "Registration confirmed" — input2 focused crop of registration form bottom: cleared password and confirm password fields, blue Create account button, green success notice "Account created. You are not signed in." Preserve exact notice, prominent. No automatic sign-in.
03 "Sign in" — input3 focused login form crop with email, masked password and blue Sign in button. Mouse pointer and cyan click ring near button edge.
04 "Signed in" — input4 focused screenshot crop of heading Login and text "Signed in as opsdesk-demo@example.com". Below the crop add editorial caption "The API returns the current user." Don't insert this caption into actual UI.
05 "Check your session" — input4 different focused crop of navigation including "Check session" and "Sign out" buttons and relevant signed-in content if space. Mouse pointer on Check session button edge. A second small editorial pointer annotation identifies "Sign out" as the next action without obscuring.
06 "Sign out" — input5 focused crop of now-empty login form, email and password fields blank, blue Sign in button. Editorial caption below screenshot "Back to the login form." No invented toast.
Connect steps with subtle arrows outside screenshots. Both left-right reading order and step numbers obvious.
Footer note "Early demo · Ticket list uses mock data · Use test details only"
Footer author "Furkan Özdemir"
Constraints: Exactly SIX numbered steps. Input4 split into two crops for04 and05. Keep actual UI and original English wording. No fictional tickets, AI features, organizations or success banners. No Mac dock, system menu, browser tabs, LinkedIn chrome. Synthetic example email okay to show. No credential disclosure. Images are evidence; do not redesign or recolor the app UI. Make the surrounding editorial layout excellent.
