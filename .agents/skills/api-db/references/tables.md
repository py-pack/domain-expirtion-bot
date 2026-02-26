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

Fields/constraints:
- `name` enum: `ukraine_host | name_cheap | go_daddy | whois | cloud_flare`
- unique pair: (`name`, `login`)
- `status` enum: `active | inactive | warning | ban`
- `accesses` (`jsonb`): provider-specific API credentials/settings payload (shape depends on provider)
- `unit_id` -> `units.id` (owner unit, nullable in current implementation)
- `last_update_at`: last account settings/status update timestamp

## Domain Layer

### domains
Main domain record with status and expiration dates.

### ns_accounts
Nameserver configuration per provider account.

Fields/constraints:
- `account_id` -> `account_domains.id`
- `ns`: nameserver value (hostname/string)
- unique pair: (`account_id`, `ns`)

## Operational

### dns_records
DNS entries per domain.

### ssls
SSL tracking per domain.

### who_is
WHOIS state tracking per domain.

### logs_update
Operation logs (request/response/error snapshots).
