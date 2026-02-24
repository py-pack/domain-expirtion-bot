---
name: vue-admin-backend-layer
description: Use when implementing or changing frontend interaction with the repository FastAPI backend (`api/`). Enforces AGENTS.md layering, auth, and API contract checks.
---

# Purpose

This skill defines how frontend code in `front/` must interact with backend API in `api/`.

Goals:
- one shared HTTP client
- no direct HTTP calls from UI
- predictable typed contracts
- consistent error normalization
- no auth-token persistence policy violations

---

# Mandatory Stack For Backend Layer

Use only the stack defined in `AGENTS.md`:
- `axios` via one shared instance
- `@tanstack/vue-query` for server-state
- `zod` for runtime schemas/contracts

Do not replace these libraries unless explicitly requested.

---

# Monorepo Contract

- Frontend lives in `front/`.
- Backend lives in `api/`.
- Backend-specific implementation rules are in `api/AGENTS.md`.

Frontend must treat backend as REST API and must not assume Laravel-specific behavior.

---

# Backend Configuration (Environment Variables)

API base URL must come from frontend env wrapper:
- `front/src/env.ts`
- `VITE__API_BASE_URL`

Rules:
- Never hardcode backend URLs in components/repositories.
- Do not use `process.env` in Vite frontend.
- If `VITE__API_BASE_URL` is missing, stop and request env setup.

CORS note:
- Backend allowlist is configured with `APP__API__ORIGINS` in backend env.
- If frontend origin is not in `APP__API__ORIGINS`, browser requests may fail due to CORS.

---

# Architecture (Mandatory Layering)

Keep layering aligned with `AGENTS.md`:

UI (pages/components)
-> State (Pinia: UI + auth only)
-> Services (business orchestration)
-> Repositories (API + DTO mapping)
-> HTTP client (axios instance)
-> Models (TypeScript types + zod schemas)

Hard rules:
- UI components must not import axios/fetch directly.
- UI components must not implement business logic.
- Repositories must not mutate UI state.
- Pinia is not server-data cache.
- Lists/entities/reports must live in Vue Query cache.

---

# HTTP Client Rules

A single shared axios instance is required.

Baseline requirements:
- baseURL from `env.api.baseUrl`
- centralized request/response interceptors
- bearer token injection handled centrally
- refresh handling and retry orchestration only in HTTP layer
- normalized API errors only (no raw axios errors above repository layer)

---

# Auth Rules (Frontend Side)

Follow `AGENTS.md` security policy:
- Access token: memory
- Refresh token: HttpOnly cookie (preferred)
- Never store auth tokens in `localStorage` by default

If existing legacy code still persists tokens, do not expand that pattern in new code; prefer migration toward the policy above.

---

# Error Handling Contract

All HTTP errors must be mapped to a unified `ApiError` type before they reach UI.

UI rules:
- Show mapped human-readable messages only.
- Do not surface raw backend/axios payloads directly.

---

# Domain Module Pattern

For frontend domain modules, follow canonical `AGENTS.md` template:

```text
front/src/domain/<domain>/
  model.ts
  repository.ts
  service.ts
  queries.ts
```

Rules:
- `repository.ts`: API calls + DTO mapping only
- `service.ts`: business orchestration
- `queries.ts`: Vue Query hooks, keys, invalidation policy

---

# Vue Query Conventions

- Query keys must be stable and domain-scoped: `['domain', params]`.
- Lists/details/reports/analytics must be served via Vue Query.
- Invalidate related queries on successful mutations.
- Avoid manual refetch orchestration from UI when invalidation can be used.

---

# OpenAPI / Contract Source

`references/api-docs.json` is optional and may be absent.

Primary contract source for this repo is FastAPI live schema:
- `${VITE__API_BASE_URL}/openapi.json`
- `${VITE__API_BASE_URL}/docs` (interactive docs)

Rules:
- Before implementing/changing an endpoint, verify method/path/request/response in live OpenAPI.
- If live schema is unavailable, inspect backend routers in `api/src/app/domains/**/router.py`.
- Do not invent route names or payload shape.
- If API behavior differs from docs, follow real backend behavior and note mismatch in summary.

---

# Definition of Done (Backend Layer)

A backend integration task is complete when:
- no axios usage exists in UI folders
- API calls are routed through repository layer
- query keys are stable and invalidation is correct
- zod validates critical request/response contracts
- auth handling follows memory + HttpOnly-cookie policy
- no hardcoded backend URL was introduced
- frontend build/typecheck passes

---

# When This Skill Must Be Used

Use this skill whenever:
- adding or changing backend endpoints in frontend
- refactoring repositories/services/query hooks
- changing auth request/refresh behavior
- aligning frontend contracts with FastAPI backend
