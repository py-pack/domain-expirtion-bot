---
name: vue-element-plus-components
description: Use when creating or refactoring visual UI components/pages in this Vue admin panel. Enforces that new UI components are based on existing Element Plus components first, with SCSS token-based theming and only thin wrappers when needed.
---

# Goal

Build and evolve visual UI with Element Plus as the default component foundation.

# Mandatory Rules

- Use existing Element Plus `El*` components as the first choice for all new visual UI.
- Do not create custom base controls (button/input/select/table/dialog/pagination/form field) if Element Plus has an equivalent.
- Compose complex UI from Element Plus primitives before introducing any custom wrapper.
- Keep wrappers thin and presentational only; business logic stays in pages/services as defined by project architecture.
- Keep theming compatible with project tokens in `src/app/styles/base/_variables.scss` and `--el-*` CSS variables.
- Use SCSS for styling adjustments; avoid inline styles except trivial one-off cases.

# Form Pattern (Mandatory)

Use the Element Plus form validation pattern for every form page/component:

- Define form `model` as a single `reactive` object (do not split each field into separate refs when avoidable).
- Use `ref<FormInstance>()` for the form instance.
- Define `rules` with `FormRules<TModel>` and bind via `:rules`.
- Add `prop` on every `el-form-item` that must be validated.
- Submit with `@submit.prevent` and call `await formRef.validate()` before mutations.
- Use horizontal form layout by default (`label-position="left"`), so labels are rendered at the left side and forms stay compact.
- Use `status-icon` and `label-width="auto"` for consistent UX.
- Use `resetFields()` for clear/reset actions where applicable.
- Keep backend field errors mapped to specific form items (`:error` or equivalent), but do not replace built-in rules with manual required checks.

# Component Selection Order

1. Select the closest Element Plus component.
2. If one component is not enough, compose multiple Element Plus components.
3. If composition is still insufficient, create a thin wrapper in `src/ui/components/common/` that delegates to Element Plus internals.
4. Create a fully custom visual component only after explicit approval.

# Definition of Done

- New or refactored visual UI is built on Element Plus components.
- No duplicate custom implementation exists for a control already covered by Element Plus.
- UI respects light/dark theme via existing `body[data-theme='light'|'dark']` token system.
