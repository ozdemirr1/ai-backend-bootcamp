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
