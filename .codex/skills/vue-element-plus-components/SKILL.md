---
name: vue-element-plus-components
description: Legacy skill name. Use when creating/refactoring visual UI in `front/`; enforces AGENTS.md styling/component rules and prevents accidental UI-library drift.
---

# Goal

Build and evolve visual UI according to `AGENTS.md` baseline:
- SCSS-only styling
- shared project components first
- no unapproved new UI framework

---

# Mandatory Rules

- Do not introduce Element Plus or any other new component framework unless explicitly requested.
- Reuse project shared UI components first (for example under `front/src/ui/components/common/`).
- Keep UI components presentational; business logic stays outside UI layer.
- Use SCSS only; no TailwindCSS.
- Avoid inline styles except trivial one-off cases.
- Keep light/dark compatibility through `body[data-theme='light'|'dark']`.
- Use theme tokens from `front/src/app/styles/base/_variables.scss` and runtime CSS custom properties.
- Use `lucide-vue-next` for standard UI icons.

---

# Composition Rules

1. Reuse existing shared component if it fits.
2. Compose existing primitives before adding new component files.
3. If a new reusable component is needed, place it in canonical shared location and keep API minimal.
4. Add custom SVG icons only in `front/src/ui/components/common/icons/`.

---

# Definition of Done

- New/refactored UI follows SCSS token system and theme policy from `AGENTS.md`.
- No new unapproved UI framework dependency is introduced.
- No business logic leaks into visual components.
