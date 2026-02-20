# AGENTS.md

This file defines **how AI agents (OpenAI Codex, assistants, codegen tools)** must work with this repository.
The agent is expected to read and follow these rules **before making any changes**.

---

## 1. Project Overview

This repository is a **monorepo with two applications**:
- `front/` - Vue 3 SPA admin panel
- `api/` - Python FastAPI backend service

The frontend (`front/`) is focused on managing:
- push notification campaigns
- user segmentation
- flow-based automation (node-based flow builder)
- analytics and reports (charts, funnels, time series)

### Core principles
- Frontend (`front/`) is a SPA (static build)
- Clean layered architecture
- No business logic inside UI components
- Strong typing (TypeScript)
- Predictable data flow
- Backend (`api/`) has separate implementation rules in `api/AGENTS.md`

### Monorepo scope (must read first)
- Frontend architecture/style/testing rules in this file apply to `front/` unless explicitly stated otherwise.
- Backend changes MUST follow `api/AGENTS.md`.

---

## 2. Frontend Tech Stack (Authoritative for `front/`)

The agent **must not replace or introduce alternatives** unless explicitly instructed.

### Core
- Vue 3
- Vite
- TypeScript (strict)
- Vue Router
- Pinia (UI + auth state only)

### Data & API
- Axios (single shared instance)
- @tanstack/vue-query (server-state, caching, retries)
- REST API (`api/` backend in this repository)

### Forms & Validation
- vee-validate
- zod (runtime schemas)

### Flow Builder
- @vue-flow/core

### Charts & Reports
- Apache ECharts
- vue-echarts

### Styling
- SCSS
- No TailwindCSS
- No inline styles except trivial cases

### Testing & Quality
- Vitest (unit & component)
- Vue Test Utils
- Playwright (E2E)
- ESLint
- Prettier
- Stylelint (SCSS)
- Husky + lint-staged
- commitlint (Conventional Commits)

---

## 3. Architecture Rules (Very Important)

### Layered architecture (strict)

```

UI (pages/components)
↓
State (Pinia – UI & auth only)
↓
Services (business orchestration)
↓
Repositories (API calls, DTO mapping)
↓
HTTP client (axios instance)
↓
Models (TypeScript types + zod schemas)

```

### Hard rules
- ❌ UI components MUST NOT call axios directly
- ❌ UI components MUST NOT contain business logic
- ❌ Repositories MUST NOT mutate UI state
- ❌ Pinia MUST NOT contain server data (lists, entities, reports)
- ✅ Server data lives in TanStack Query cache
- ✅ All API calls go through the shared HTTP client

If the agent violates this, the change is considered **invalid**.

---

## 4. Project Structure

Canonical frontend structure inside `front/src/` (do not improvise):

```
front/src/
├─ app/
│  ├─ main.ts
│  ├─ app.vue
│  ├─ router/
│  │  ├─ index.ts
│  │  └─ guards.ts
│  ├─ i18n/
│  │  ├─ index.ts
│  │  └─ locales/
│  │     ├─ en.json
│  │     ├─ uk.json
│  │     └─ pt-PT.json
│  └─ styles/
│     ├─ _variables.scss
│     ├─ _mixins.scss
│     └─ main.scss
│
├─ shared/
│  ├─ http/
│  │  ├─ client.ts          # axios instance + interceptors
│  │  ├─ auth-refresh.ts    # refresh token lock/queue
│  │  ├─ errors.ts          # ApiError mapping
│  │  └─ types.ts           # API DTOs
│  ├─ auth/
│  │  ├─ token-store.ts
│  │  └─ auth-events.ts
│  └─ utils/
│     ├─ retry.ts
│     ├─ time.ts
│     └─ id.ts
│
├─ domain/
│  ├─ users/
│  │  ├─ model.ts
│  │  ├─ repository.ts
│  │  ├─ service.ts
│  │  └─ queries.ts
│  ├─ segments/
│  │  ├─ model.ts
│  │  ├─ repository.ts
│  │  ├─ service.ts
│  │  └─ queries.ts
│  ├─ pushes/
│  │  ├─ model.ts
│  │  ├─ repository.ts
│  │  ├─ service.ts
│  │  └─ queries.ts
│  ├─ flows/
│  │  ├─ model.ts
│  │  ├─ validator.ts
│  │  ├─ repository.ts
│  │  └─ service.ts
│  └─ reports/
│     ├─ model.ts
│     ├─ repository.ts
│     ├─ service.ts
│     └─ queries.ts
│
├─ ui/
│  ├─ layout/
│  │  ├─ AppShell.vue
│  │  ├─ Sidebar.vue
│  │  └─ Topbar.vue
│  ├─ components/
│  │  ├─ common/
│  │  │  ├─ UiTable.vue
│  │  │  ├─ UiFormField.vue
│  │  │  ├─ UiEmptyState.vue
│  │  │  └─ icons/
│  │  │     └─ *.vue
│  │  ├─ flow/
│  │  │  ├─ FlowCanvas.vue
│  │  │  └─ nodes/
│  │  │     ├─ TriggerNode.vue
│  │  │     ├─ ConditionNode.vue
│  │  │     └─ ActionNode.vue
│  │  └─ charts/
│  │     ├─ TimeSeriesChart.vue
│  │     ├─ FunnelChart.vue
│  │     └─ BarBreakdownChart.vue
│  └─ pages/
│     ├─ LoginPage.vue
│     ├─ UsersPage.vue
│     ├─ SegmentsPage.vue
│     ├─ FlowsPage.vue
│     └─ ReportsPage.vue

```

### Domain folder rules
Each domain module MUST follow this template:

```
domain/x/
├─ model.ts        # Domain types + zod schemas
├─ repository.ts   # API interface + implementation
├─ service.ts      # Business logic / orchestration
└─ queries.ts      # TanStack Query hooks (server-state)
```

---

## 5. HTTP & Authentication Rules

### Axios
- Use **one shared axios instance**
- Interceptors handle:
  - Bearer token injection
  - Token refresh
  - Retry (idempotent requests only)
  - Error normalization

### Tokens
- Access token: memory
- Refresh token: HttpOnly cookie (preferred)
- NEVER store tokens in localStorage by default

### Errors
All HTTP errors must be converted to a unified `ApiError` type.
UI must display **mapped, human-readable messages only**.

---

## 6. Server State & Caching

### TanStack Query
- Used for:
  - Lists
  - Entity details
  - Reports
  - Analytics
- Handles:
  - Caching
  - Deduplication
  - Retry
  - Refetching
  - Invalidation

### Pinia is NOT a data cache
Pinia stores only:
- auth state
- UI preferences
- feature flags

---

## 7. Flow Builder Rules

### Flow constraints
- Exactly ONE trigger per flow
- Conditions must have explicit branches (yes/no)
- End nodes have no outgoing edges
- No cycles unless explicitly allowed
- All edges must reference existing nodes

### Flow changes
- Drafts are mutable
- Published flows are immutable
- Publishing increments version
- Restoring creates a new draft

Both frontend and backend validation are required.

---

## 8. Charts & Reports

### Rules
- Charts receive prepared DTOs only
- Charts NEVER fetch data themselves
- Aggregation happens on the backend
- Chart components are pure and stateless

Allowed chart types:
- Time series
- Funnel
- Bar breakdown
- Heatmaps (if data exists)

---

## 9. Code Style & Conventions

### TypeScript
- `strict: true`
- No `any`
- Prefer explicit return types in services

### Vue
- Composition API
- `<script setup>`
- Components in PascalCase
- Files in kebab-case

### Naming
- Services: `XService`
- Repositories: `XRepository`
- Query keys: `['domain', params]`

---

## 10. Testing Expectations

Minimum expectations:
- HTTP client: unit tested
- Auth refresh logic: unit tested
- Flow validation: unit tested
- Services: unit tested
- Pages: smoke tests
- Critical paths: E2E tests

Agent must **not remove or weaken tests**.

---

## 11. Git & Commit Rules

### Commit format (mandatory)

```

type(scope): short description

```

Allowed types:
- feat
- fix
- refactor
- test
- chore
- docs

Examples:
- `feat(flows): add condition node editor`
- `fix(auth): prevent refresh token race condition`

---

## 12. Guardrails (Do NOT do this)

The agent MUST NOT:
- Change project architecture
- Introduce new state management libraries
- Replace axios or vue-query
- Add TailwindCSS
- Bypass validation rules
- Store tokens in localStorage
- Modify CI or build configs without request
- Delete files it does not fully understand

---

## 13. When in Doubt

If something is unclear:
- STOP
- Ask for clarification
- Do NOT guess

Silent architectural changes are considered **critical errors**.

---

## 14. Backend Snapshot (`api/`) (informational)

Backend-specific architecture and coding rules are defined in `api/AGENTS.md` and are mandatory for backend changes.

Current backend layout:

```
api/
├─ pyproject.toml          # FastAPI service config (uv, dependencies)
├─ migrations/             # Alembic migrations
├─ src/app/
│  ├─ main.py              # FastAPI app + router registration
│  ├─ core/                # settings + database session setup
│  ├─ domains/
│  │  ├─ auth/             # models/repository/service/router/schemas
│  │  └─ tools/            # domain tools router (expiration endpoint)
│  ├─ infra/               # HTTP dependencies/middleware, JWT, logging
│  └─ cli/                 # CLI commands (includes add_user)
```

Current backend notes:
- Stack: FastAPI, SQLAlchemy, Alembic, pydantic-settings, JWT (python-jose/PyJWT), bcrypt.
- Main API routes: `/api/domain/expiration` and `/api/v1/auth/*` (login, Google login, refresh, logout).
- Auth model: access/refresh JWT + persisted refresh tokens (`refresh_tokens` table).
- Infrastructure includes PostgreSQL (via SQLAlchemy) and Redis in docker environment.

---

## 15. Bootstrap & Local Ops Notes (from `docs/CREATE_NEW.md`)

### Root repository layout

```
.
├─ api/                  # backend service
├─ front/                # frontend SPA
├─ docker/               # docker-related files
├─ .env                  # shared env for local docker setup
└─ docker-compose.yml    # base compose config
```

### Docker-first bootstrap context
- Backend and frontend were initially scaffolded from docker containers (`docker compose run ...` flow).
- Frontend bootstrap command reference: `docker compose run --rm front bash` -> `npm create vue@latest`.
- `docs/CREATE_NEW.md` contains a Poetry-based backend bootstrap (historical project creation notes).
- For this repository's current backend workflows, use `uv` commands from `api/AGENTS.md` as authoritative.

### Migrations context
- Alembic is the migration tool for backend schema changes.
- Standard lifecycle remains: create revision -> upgrade -> (if needed) downgrade.
- In this repository, prefer running Alembic through `uv` from `api/` (see `api/AGENTS.md` for exact commands).

### Optional IDE setup context
- `docs/CREATE_NEW.md` also documents a Docker-based Python interpreter setup path for PyCharm.
- Treat that section as local developer environment guidance, not as an architecture rule.

---

## 16. UI Styling Baseline (Project Decision)

- Design direction: **Flat / Semi-flat with subtle depth** (Material-like hierarchy, no neumorphism).
- Styling stack: **SCSS only**. Tailwind is not allowed.
- Base spacing scale:
  - small: `4px`
  - base: `8px`
  - large: `16px` and `24px`
- Base typography:
  - `16px` body text
  - `line-height: 1.5`
  - clean heading weights (avoid over-bolded UI)
- Shadow policy:
  - use only light elevation (cards/popovers)
  - canonical card shadow: `0px 1px 4px rgba(0,0,0,0.08)`

### Theme tokens
- Light theme is default.
- Theme is controlled via `body[data-theme='light']` and `body[data-theme='dark']`.
- Keep color tokens in SCSS variables and expose runtime CSS custom properties.
- Color variables location:
  - source of truth (SCSS): `front/src/app/styles/base/_variables.scss`
  - runtime theme vars (CSS custom props): `front/src/app/styles/base/_variables.scss`
- SCSS variable names:
  - `$color-bg`
  - `$color-text`
  - `$color-primary`
  - `$color-accent`
  - `$color-success`
  - `$color-warning`
  - `$color-danger`
  - `$card-shadow`
- CSS custom property names used by UI:
  - `--color-bg`
  - `--color-surface`
  - `--color-surface-soft`
  - `--color-text`
  - `--color-text-muted`
  - `--color-border`
  - `--color-primary`
  - `--color-primary-soft`
  - `--color-accent`
  - `--color-success`
  - `--color-warning`
  - `--color-danger`
  - `--card-shadow`
  - `--space-1` .. `--space-5`
  - `--radius-sm`, `--radius-md`

### SCSS structure (must keep)
- `front/src/app/styles/base/`
  - `_index.scss`
  - `_variables.scss`
  - `_mixins.scss`
  - `_reset.scss`
  - `_typography.scss`
- `front/src/app/styles/components/`
  - `_index.scss`
  - `_buttons.scss`
  - `_forms.scss`
- `front/src/app/styles/pages/`
  - `_index.scss`
  - `_layout.scss`

### Theme state
- Theme state must live in Pinia as `theme: 'light' | 'dark'`.
- Use a dedicated UI store (`front/src/shared/ui/theme.store.ts`) for theme initialization/toggle.

### Icons
- Selected icon library: **lucide-vue-next**.
- Use it for navigation, action buttons, and status-level UI icons.
- Reusable custom SVG icons (brand logos, provider icons, etc.) must be stored in:
  - `front/src/ui/components/common/icons/`
- Do not duplicate inline SVG markup across pages; extract to shared icon component first.

### Auth UI env variables
- Env flags location example: `.env.example`
- Variable names:
  - `VITE_AUTH_PASSWORD_ENABLED`
  - `VITE_AUTH_GOOGLE_ENABLED`
