---
name: ui-pages-structure
description: Use when adding or moving frontend pages. Enforces AGENTS.md canonical page location, naming, and router update rules for `front/`.
---

# Purpose

Use this skill whenever you add, move, or refactor route pages in the frontend.

Goals:
- keep pages discoverable in one canonical location
- keep router imports stable
- avoid silent structure drift from `AGENTS.md`

---

# Mandatory Page Location Rules

Pages must follow `AGENTS.md` canonical location:

```text
front/src/ui/pages/
```

Default page structure (from `AGENTS.md`):

```text
front/src/ui/pages/
  LoginPage.vue
  UsersPage.vue
  SegmentsPage.vue
  FlowsPage.vue
  ReportsPage.vue
```

Rules:
- Do not silently introduce a new nested page-folder convention.
- For new pages, prefer the same canonical flat layout unless user explicitly requests a new structure.
- If folder organization is required and not specified, stop and ask before changing page layout policy.

Page naming rule:
- follow the canonical `*Page.vue` convention already documented in `AGENTS.md`

---

# Routing Rules

- Update router imports whenever a page is added or moved.
- Canonical router location is `front/src/app/router/index.ts` per `AGENTS.md`.
- If the codebase still uses a legacy router path (for example `front/src/router/index.ts`), update the active router and do not create duplicate router modules.
- Keep route paths stable and descriptive.

When moving pages, update all related imports and route records.

---

# Page Composition Rules

- Page files contain page-level orchestration and layout only.
- UI components must not contain business logic.
- Page components must not call axios directly.
- Server-state flows through repositories/services/query hooks as defined in `AGENTS.md`.

---

# Refactor Checklist

When adding or moving pages:
1. Place file in `front/src/ui/pages/` (canonical layout).
2. Use the canonical `*Page.vue` naming style.
3. Update router imports and route records.
4. Verify no direct axios usage was introduced in page code.
5. Run frontend build/tests relevant to the change.
