---
name: api-db
description: Locate and interpret the API database schema and related DB documentation. Use this skill whenever a task involves tables, relations, joins, migrations, or database structure.
---

# Purpose
Provide structured access to the API database schema and define where the source of truth lives.

# Source of truth
1. Structure & relations: `api/references/schema.md` (preferred) or `.agents/skills/api-db/references/schema.md` (fallback in this repo)
2. Human-readable descriptions: `api/references/tables.md` (preferred) or `.agents/skills/api-db/references/tables.md` (fallback in this repo)
3. Implementation truth: `api/migrations/versions/` (or `migrations/versions/` when already working inside `api/`)

If schema conflicts with migrations — migrations win, then update the schema file you actually used (`api/references/schema.md` preferred, otherwise the fallback under `.agents/skills/api-db/references/`).

# How to work with DB tasks
- Always open schema first (`api/references/schema.md` if present; otherwise `.agents/skills/api-db/references/schema.md`).
- Identify tables and join keys explicitly.
- If adding/changing tables: update migration + update the active schema file.
- If task touches `account_domains` / `ns_accounts`: preserve enum values, `(name, login)` uniqueness for `account_domains`, and note that `accesses` is provider-specific JSON keyed by `account_domains.name`.

# Code locations
- SQLAlchemy models / repositories: `api/src/app/` (or `src/app/` if cwd is `api/`)
- Alembic setup: `api/alembic.ini`, `api/migrations/env.py`
- Migrations: `api/migrations/versions/`

# Output rules
- Keep answers short.
- Name exact tables and join keys.
- Avoid assumptions not present in schema or migrations.
