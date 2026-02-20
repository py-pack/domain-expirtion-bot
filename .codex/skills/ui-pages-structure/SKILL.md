---
name: ui-pages-structure
description: Enforces scalable page folder structure and shared page navigation template for this Vue admin project.
---

# Purpose

Use this skill whenever you add, move, or refactor route pages under `src/ui/pages`.

Goals:
- keep pages grouped by feature
- keep route files easy to find
- reuse one consistent top navigation header

---

# Mandatory Page Location Rules

Store pages by feature folder, not as flat files.

Canonical structure:

```text
src/ui/pages/
  auth/
    login-page.vue
    google-auth-callback-page.vue
  dashboard/
    dashboard-page.vue
  profile/
    profile-page.vue
  segments/
    segments-page.vue
  users/
    users-page.vue
    users-create-page.vue
    users-edit-page.vue
```

For new domains, create a dedicated folder:

```text
src/ui/pages/<domain>/
  <domain>-page.vue          # index/list page
  <domain>-create-page.vue   # optional create page
  <domain>-edit-page.vue     # optional edit page
```

File naming rule:
- use kebab-case filenames
- suffix with `-page.vue`

---

# Routing Rules

- Router imports must point to feature folders, e.g.:
  - `@/ui/pages/users/users-page.vue`
- Keep route paths stable and descriptive:
  - list: `/users`
  - create: `/users/create`
  - edit: `/users/:id/edit`

When moving pages, update all related imports in `src/app/router/index.ts`.

---

# Mandatory Top Navigation Template

Every non-trivial page must use the shared page header component:

- `src/ui/components/common/UiPageNav.vue`

Required behavior:
- breadcrumbs are always provided
- page title is provided
- right-side action buttons use `#actions` slot

Example:

```vue
<UiPageNav
  title="Users"
  description="Manage platform users."
  :breadcrumbs="[{ label: 'Users' }]"
>
  <template #actions>
    <RouterLink to="/users/create" class="btn btn--primary">Create user</RouterLink>
  </template>
</UiPageNav>
```

For nested pages:

```ts
const breadcrumbs = [
  { label: 'Users', to: '/users' },
  { label: 'Create user' },
]
```

---

# Page Composition Rules

- page file contains only page-level orchestration and layout
- domain logic remains in `src/domain/*`
- server data must come from vue-query hooks
- avoid duplicating header layouts; reuse `UiPageNav`

---

# Refactor Checklist

When adding or moving pages:
1. Place file in `src/ui/pages/<feature>/`.
2. Use kebab-case `*-page.vue` name.
3. Update router imports and route records.
4. Add `UiPageNav` with breadcrumbs.
5. Put action buttons in `UiPageNav` `#actions` slot.
6. Run `npm run build`.

