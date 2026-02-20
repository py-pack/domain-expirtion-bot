---
name: vue-storage-usage
description: Use when reading or writing client-side storage in this Vue project. Enforces dot-notation keys, key registry, typed access, env-based namespacing, and migration-safe usage
---

# Purpose

This project uses a structured storage wrapper.

Storage must be accessed via typed API only.
Keys must use dot-notation (similar to config paths).

The goal:
- Predictable key structure
- No direct browser storage usage
- Type-safe access
- Centralized namespace
- Clean, readable persistence rules

---

# Quick Start (Required Steps)

1. Add key in central registry:
- `src/shared/storage/keys.ts`

2. Add or reuse typed schema entry for that key:
- `StorageSchema` in `src/shared/storage/keys.ts`

3. If key requires session scope or legacy migration:
- configure key metadata in `src/shared/storage/storage.ts` (`keyConfigMap`)

4. Use wrapper API only from app code:
- `appStorage.getK(...)`, `appStorage.setK(...)`, `appStorage.remove(...)`
- or primitive helpers (`getString/getBoolean/getNumber`)

5. Never call browser storage directly outside wrapper:
- `localStorage`
- `sessionStorage`
- raw `JSON.parse/JSON.stringify` for persisted values

---

# Core Idea

Storage keys follow `domain.group.setting`.

Examples:
- `auth.tokens.by_domain`
- `auth.google.oauth_state`
- `ui.theme.mode`
- `ui.sidebar.collapsed`
- `filters.users.list`

Naming rules:
- lowercase only
- words with `_` when needed
- no camelCase
- no spaces

---

# Environment Contract

Storage namespace/version comes from env:
- `VITE_STORAGE_PREFIX`
- `VITE_STORAGE_VERSION`

All keys are prefixed internally by wrapper.

Do not hardcode prefix logic in app code.
Do not manually concatenate prefix with keys.

---

# Public Storage Interface

Only wrapper API may be used from feature code.

Allowed methods:
- `get(key, fallback?)`
- `set(key, value)`
- `has(key)`
- `remove(key)`
- `clear()`

Typed helpers:
- `getString(key, fallback?)`
- `getBoolean(key, fallback?)`
- `getNumber(key, fallback?)`

Strict typed access (recommended):
- `getK(key)`
- `setK(key, value)`

Application code must NOT use:
- localStorage
- sessionStorage
- JSON.parse / JSON.stringify directly

---

# Key Rules

1. Keys must be declared in the central key registry.
2. No arbitrary string keys in components.
3. Storage usage must be intentional and documented.
4. Do not store large datasets.
5. Do not store sensitive secrets.
6. Do not use storage as state management.

---

# Typical Use Cases

Allowed:

- Authentication token
- Current user snapshot
- UI preferences (theme, sidebar state)
- Table pagination settings
- Filter persistence
- Small feature flags

Not allowed:

- API responses cache
- Report datasets
- Business domain data

---

# Usage Patterns

Authentication:

- Save token on login
- Remove token on logout
- Never read token directly from storage in UI

UI preference:

- Read with fallback
- Update when changed
- Persist automatically

Filters:

- Save list filters before leaving page
- Restore on page load

---

# Practical Example

```ts
import { STORAGE_KEYS } from '@/shared/storage/keys'
import { appStorage } from '@/shared/storage/storage'

const persistedTheme = appStorage.getK(STORAGE_KEYS.ui_theme_mode)
appStorage.setK(STORAGE_KEYS.ui_theme_mode, 'dark')

const oauthState = appStorage.getString(STORAGE_KEYS.auth_google_oauth_state, '')
if (oauthState) {
  appStorage.remove(STORAGE_KEYS.auth_google_oauth_state)
}
```

---

# Error Safety

- Reading missing keys must not crash.
- Corrupted values must fallback safely.
- Components must always provide sensible defaults.

---

# Definition of Done

A storage feature is complete when:

- No direct browser storage calls exist
- Keys follow dot-notation convention
- Keys are declared in central registry
- Types are respected
- No hardcoded prefixes
- Application builds successfully

---

# Review Checklist

- `grep` shows no direct `localStorage`/`sessionStorage` usage outside `src/shared/storage/storage.ts`
- key added to `STORAGE_KEYS`
- type added to `StorageSchema`
- wrapper methods used (`getK/setK` preferred)
- migrations/legacy keys handled in wrapper metadata, not in UI code

---

# When To Use This Skill

Use this skill whenever:

- Persisting UI state
- Saving auth token
- Storing user preferences
- Adding filter persistence
- Refactoring storage logic

If implementation code touches browser storage directly, refactor to use wrapper API.
