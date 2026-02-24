---
name: api-db
description: Locate and interpret the API database schema and related DB documentation. Use this skill whenever a task involves tables, relations, joins, migrations, or database structure.
---

# Purpose
Provide structured access to the API database schema and define where the source of truth lives.

# Source of truth
1. Structure & relations: `references/schema.md`
2. Human-readable descriptions: `references/tables.md`
3. Implementation truth: `migrations/versions/`

If schema conflicts with migrations — migrations win, then update `references/schema.md`.

# How to work with DB tasks
- Always open `references/schema.md` first.
- Identify tables and join keys explicitly.
- If adding/changing tables: update migration + update schema.md.

# Code locations
- SQLAlchemy models / repositories: `src/app/`
- Alembic setup: `alembic.ini`, `migrations/env.py`
- Migrations: `migrations/versions/`

# Output rules
- Keep answers short.
- Name exact tables and join keys.
- Avoid assumptions not present in schema or migrations.
