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
