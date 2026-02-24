# API Database Tables (Descriptions)

> Informational only. Schema.md is structural truth.

## Core

### users
System users.

### units
Organizational units/teams.

### unit_responsibles
Many-to-many link between users and units with access level.

### account_domains
Provider account used to manage/register domains.

## Domain Layer

### domains
Main domain record with status and expiration dates.

### ns_accounts
Nameserver configuration per provider account.

## Operational

### dns_records
DNS entries per domain.

### ssls
SSL tracking per domain.

### who_is
WHOIS state tracking per domain.

### logs_update
Operation logs (request/response/error snapshots).

