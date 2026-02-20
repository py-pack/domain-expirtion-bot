---
name: vue-admin-backend-layer
description: Use when implementing or modifying any interaction with the Laravel REST backend in this Vue 3 admin project. Explains architecture, environment variables, authorization, error handling, and repository/query patterns.
---

# Purpose

This skill defines how the frontend must interact with the Laravel REST backend.

Goal:
- One consistent HTTP layer
- No direct HTTP calls from UI
- Centralized authorization
- Predictable error handling
- Type-safe API contracts

This is an MVP phase using Laravel standard Bearer token.
JWT/JWS may be introduced later but MUST NOT be implemented unless explicitly requested.

---

# Mandatory Libraries

For backend-layer work in this project, use:
- `@tanstack/vue-query` for server-state queries/mutations, cache, invalidation, retries
- `zod` for runtime validation/parsing of backend payloads and request DTOs

Do not replace these with alternatives unless explicitly requested.

---

# Backend Configuration (Environment Variables)

Backend domain MUST be defined via environment variables.

Required variable:

- `VITE_API_BASE_URL`

Example `.env`:

VITE_API_BASE_URL=https://api.example.com

Rules:
- Never hardcode backend URLs inside repositories or components.
- Always access env via `import.meta.env.VITE_API_BASE_URL`
- If `VITE_API_BASE_URL` is missing → STOP and request it from the developer.
- Do not use `process.env` (this is a Vite project).

Reference:
https://vitejs.dev/guide/env-and-mode.html

---

# Architecture (Mandatory Layering)

Strict layering must be respected:

UI (pages/components)
↓
Vue Query hooks
↓
Domain services (optional orchestration)
↓
Repositories
↓
HTTP client (axios instance)
↓
Laravel API

Rules:
- UI MUST NOT import axios or fetch.
- Repositories are thin: only HTTP calls and DTO mapping.
- Services contain business orchestration logic.
- All server-state must use TanStack Vue Query.
- Runtime validation of backend contracts must use Zod schemas.

Reference:
https://tanstack.com/query/latest/docs/framework/vue/overview

---

# HTTP Client Rules

A single axios instance must exist:

Location:
`src/shared/http/client.ts`

Configuration requirements:
- baseURL = `import.meta.env.VITE_API_BASE_URL`
- timeout (e.g. 20000 ms)
- header `Accept: application/json`

Reference:
https://axios-http.com/docs/instance

## Request Interceptor (Authorization)

If token exists in auth store:
Add header:

Authorization: Bearer <token>

Token source:
`src/shared/auth/auth.store.ts`

Never manually attach Authorization header inside repositories.

---

# Authentication (MVP Phase)

Current backend auth:
- Laravel standard Bearer token
- Token received after login
- Stored in auth store (localStorage allowed in MVP)

On 401 response:
- Clear token
- Redirect to `/login`
- No refresh-token logic yet

JWT/JWS support is planned for future phases only.

Laravel reference:
https://laravel.com/docs/authentication

---

# Error Handling Contract

All backend errors must be normalized into ApiError.

Location:
`src/shared/http/api-error.ts`

Standard shape:

- status?: number
- message: string
- code?: string
- fieldErrors?: Record<string, string[]>
- raw?: unknown

Mapping rules:
- 422 → extract Laravel validation errors into fieldErrors
- 403/404 → preserve backend message
- Network errors → generic message
- Never throw raw axios errors above repository layer

UI rules:
- Forms display fieldErrors
- Non-validation errors show notification/toast

Laravel validation reference:
https://laravel.com/docs/validation

---

# Repository Pattern

For each backend entity (Users, Segments, Campaigns, etc.):

Create:

src/domain/<domain>/
dto.ts
<domain>.repository.ts
<domain>.queries.ts
<domain>.service.ts (optional)

Repository responsibilities:
- Call HTTP client
- Map request/response
- Return typed DTOs
- Throw ApiError (already normalized by interceptor)

Do not:
- Store state
- Implement UI logic
- Access router

---

# Index/List Pages (Mandatory Contract Rules)

Applies to pages like `/apps`, `/streams`, `/clients`, `/segments`, `/campaigns`, `/funnels`.

## Query params for list endpoints

When parsing list filters (`parseXxxQuery` / `parseXxxListFilters`):
- Always trim string filters via Zod.
- Do not pass empty strings to axios params.
- Build a normalized query object and include only meaningful values.
- Keep valid numeric filters (`page`, `per_page`, limits) even when optional.

Required behavior:
- ✅ `''` / `'   '` string filters are omitted from request params.
- ✅ Request should be `/api/entity` instead of `/api/entity?name=&updated_since=`.

## List response envelopes

Canonical list contract:
- `{ success: boolean, message?: string, data: Item[], pagination?: Pagination }`

Where `Pagination` is a top-level object (same level as `success` and `data`), e.g.:
- `{ total, count, limit, currentPage, totalPages }`

Rules:
- Do not expect `data.<entity_plural>` wrappers for index/list endpoints.
- Parse `data` directly as an array of items.
- If pagination is present, read totals/pages from top-level `pagination`.
- Keep compatibility fallback for legacy endpoints only when needed:
- `{ data: Item[] }`
- raw `Item[]`

## Pagination policy for index tables (mandatory)

Pagination contract is uniform for all paginated index endpoints:
- `pagination.total`
- `pagination.count`
- `pagination.limit`
- `pagination.currentPage`
- `pagination.totalPages`

If OpenAPI/docs for a list endpoint includes `pagination`, you MUST plan and implement full pagination flow immediately (backend layer + table UI):
- Add `page` and `per_page` to list query schema (`parseXxxQuery` / `parseXxxListFilters`).
- Keep empty string filters removed, but keep numeric pagination params.
- Parse list response into a typed list result shape:
- `items`, `total`, `currentPage`, `perPage`, `lastPage`.
- Return this list result from repository/service/query hook (not plain array).
- In index page table, render pagination control (`el-pagination`) and bind it to query filters.
- Update current page on pagination events and refetch via query key params.

This is not optional:
- If docs show `pagination` for index endpoint, table-level pagination must be present in UI.

## Detail response envelopes

Detail parsers should support:
- `{ data: Item }`
- `{ success: boolean, message?: string, data: Item }`
- raw `Item` (legacy fallback)

## Nullability hygiene

For API fields that backend may return as `null` (`created_at`, `updated_at`, nullable FK/user fields):
- model schema must use `.nullable().optional()` instead of `string().optional()`.

---

# Vue Query Conventions

All server-state reads must use Vue Query.

Query key examples:

["segments", "list", params]
["segments", "detail", id]

Mutation rules:
- Invalidate related queries on success
- Do not manually refetch from UI
- Optimistic updates only when explicitly required

Reference:
https://tanstack.com/query/latest/docs/framework/vue/guides/queries

---

# Zod Conventions

Use Zod in domain `model`/`dto` layers to:
- validate API responses before mapping to domain types
- validate mutation/input payloads before repository calls
- provide predictable validation errors for UI mapping

Do not pass raw unknown backend payloads into UI/state without Zod parsing.

Reference:
https://zod.dev/

---

# OpenAPI / Swagger Integration

If available:

references/api-docs.json

`references/api-docs.json` is the primary source of truth for backend routes.

Rules:
- Before implementing/changing any backend call, check `paths` in `references/api-docs.json`.
- Use it to verify exact endpoint path, HTTP method, request body, query params, and response schema.
- Generate DTO types from schema definitions.
- If an expected endpoint is missing in `paths`:
  - STOP
  - Ask for clarification or updated spec
  - Do not guess route names
- If backend behavior differs from spec:
  - follow real backend behavior
  - note discrepancy in implementation summary

Quick lookup workflow:
1. Find path in `paths` section.
2. Confirm method block (`get/post/put/delete`).
3. Check `parameters` + `requestBody`.
4. Check `responses` schema.
5. Implement repository call only after this check.

OpenAPI reference:
https://swagger.io/specification/

---

# Definition of Done (Backend Layer)

A backend feature is correctly implemented when:

- No axios usage exists in UI folders
- All HTTP goes through repository
- Authorization header is automatically attached
- 401 properly logs out user
- 422 errors map into form fieldErrors
- Query keys are stable and invalidated correctly
- Zod schemas validate request/response contracts where needed
- TypeScript build passes
- No hardcoded backend URLs

---

# When This Skill Must Be Used

Use this skill whenever:
- Adding a new backend endpoint
- Refactoring API calls
- Modifying auth behavior
- Adding domain repositories
- Integrating new backend features

If implementation violates this document, refactor before continuing.
