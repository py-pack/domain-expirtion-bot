---
name: vue-storage-usage
description: Use when reading/writing browser storage in frontend code. Enforces AGENTS.md storage boundaries, especially auth-token and server-state restrictions.
---

# Purpose

This skill defines safe storage boundaries for `front/`.

The goal:
- prevent security drift
- prevent storage from becoming state/cache layer
- keep persistence limited to small UI concerns

---

# Non-Negotiable Rules (From AGENTS.md)

1. Never store auth tokens in `localStorage` by default.
2. Access token belongs in memory.
3. Refresh token is HttpOnly cookie (preferred).
4. Pinia is not a server-data cache.
5. Server data (lists/entities/reports/analytics) belongs in Vue Query cache.

If existing legacy code stores tokens, do not expand that pattern in new changes.

---

# Allowed Storage Scope

Allowed (small, non-sensitive UI state only):
- theme preference (if project chooses persistence)
- minor UI preferences (for example collapsed sidebar)
- non-sensitive ephemeral UX flags

Not allowed:
- access/refresh tokens
- API response payloads
- large datasets/reports
- business entities as pseudo-cache

---

# Integration Rules

- Theme state must live in Pinia as `theme: 'light' | 'dark'` (`front/src/shared/ui/theme.store.ts`).
- UI components must not manage storage business rules directly.
- If a storage wrapper exists in the project, use the wrapper instead of raw browser APIs.
- Keep storage writes minimal and explicit.

---

# Implementation Checklist

When adding storage usage:
1. Confirm it is UI preference data, not auth/server/business data.
2. Keep values small, serializable, and non-sensitive.
3. Keep reads resilient (fallback defaults).
4. Keep writes centralized (store/service/helper), not scattered across UI components.
5. Verify no token storage was introduced.

---

# Review Checklist

- No new auth-token storage calls in frontend code.
- No server-data persistence added to storage.
- Storage usage is limited to non-sensitive UI preferences.
- UI behavior remains correct with missing/corrupted stored values.

---

# When To Use This Skill

Use this skill whenever:
- adding or refactoring browser-storage usage
- persisting UI preferences
- auditing auth/storage boundaries
- migrating legacy localStorage patterns to AGENTS-compliant policy
