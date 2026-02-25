---
name: ui-pages-structure
description: Use when adding or moving frontend pages. Enforces AGENTS.md canonical page location, naming, and router update rules for `front/`.
---

# When to Use

Use this skill when you add/refactor route pages in `front/`, especially for CRUD/admin entity pages.

## Where Pages Live

Route pages live in:

```text
front/src/ui/pages/
```

Current project convention for entity pages:

```text
front/src/ui/pages/
  users/
    UsersListPage.vue
    UserCreatePage.vue
    UserEditPage.vue
```

Rules:
- Keep route pages under `front/src/ui/pages/`.
- For grouped entity CRUD pages, use a dedicated folder per entity (`users/`, `domains/`, etc.).
- Use `CamelCase` file names with `Page.vue` suffix for route pages.
- Do not create alternative page roots (for example `front/src/pages`).

## Page Template (Preferred)

Use `front/src/ui/layout/UiEntityPageLayout.vue` for management pages.

It provides:
- page title
- description as tooltip (via `UiTooltip` + `Teleport`)
- right-side actions slot
- breadcrumbs under the title
- optional meta row

### Basic usage

```vue
<UiEntityPageLayout
  title="Users"
  description="System users management"
  :breadcrumbs="[{ label: 'Users' }]"
>
  <template #actions>
    <UiButton @click="...">Create user</UiButton>
  </template>

  <!-- page content -->
</UiEntityPageLayout>
```

### Slots

- `#actions` - buttons/controls rendered on the right side of the header
- `#meta` - extra contextual text under breadcrumbs (e.g. email + ID on edit page)
- default slot - page content (tables, forms, states)

## Breadcrumbs Pattern

Use `UiBreadcrumbs` indirectly via `UiEntityPageLayout` `breadcrumbs` prop.

Patterns:
- list page: `[{ label: 'Users' }]`
- create page: `[{ label: 'Users', to: { name: 'users' } }, { label: 'Create' }]`
- edit page: `[{ label: 'Users', to: { name: 'users' } }, { label: 'Edit' }]`

Breadcrumb links should navigate back to the entity index page (`name: 'users'`, etc.).

## Router Updates (Required)

Update the active router in:

```text
front/src/app/router/index.ts
```

When splitting one page into CRUD pages:
- add imports for each page file
- keep route names explicit (`users`, `users-create`, `users-edit`)
- keep paths predictable (`/users`, `/users/create`, `/users/:id/edit`)

## Page Responsibilities

Page files should contain:
- route-level orchestration
- query/mutation hooks (`domain/*/queries.ts`)
- navigation (`router.push`)
- layout composition (`UiEntityPageLayout`)

Do not put in page files:
- direct axios calls
- reusable UI primitives (extract to `ui/components/common` or domain-specific components)

Layout-level reusable page shells belong in `front/src/ui/layout/` (for example `UiEntityPageLayout.vue`).

## Quick Checklist

1. Place/rename page files under `front/src/ui/pages/<entity>/` in `CamelCase`.
2. Use `UiEntityPageLayout` for title + tooltip + breadcrumbs + actions.
3. Add breadcrumbs that link back to the entity index page.
4. Update `front/src/app/router/index.ts` imports and routes.
5. Run `npm run type-check` in `front/`.
