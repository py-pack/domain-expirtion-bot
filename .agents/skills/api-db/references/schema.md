# API Database Schema (ERD)

> Single source of truth for structure and relations.

```mermaid
erDiagram
  users {
    bigint id PK
    varchar email
    varchar tg
  }

  units {
    bigint id PK
    varchar name
  }

  unit_responsibles {
    bigint id PK
    bigint user_id FK
    bigint unit_id FK
    varchar level
    timestamp created_at
  }

  account_domains {
    bigint id PK
    varchar name
    varchar login
    bigint unit_id FK
    jsonb accesses
    varchar status
    timestamp created_at
    timestamp last_update_at
  }

  ns_accounts {
    bigint id PK
    bigint account_id FK
    varchar ns
  }

  domains {
    bigint id PK
    varchar domain
    timestamp expiration_at
    bigint registerable_id FK
    bigint manageable_id FK
    varchar status
    timestamp ssl_expiration_at
    timestamp created_at
  }

  who_is {
    bigint id PK
    bigint domain_id FK
    varchar status
    timestamp created_at
    timestamp changed_at
    timestamp expiration_at
    timestamp updated_at
  }

  ssls {
    bigint id PK
    bigint domain_id FK
    varchar status
    timestamp created_at
    timestamp expiration_at
    timestamp updated_at
  }

  dns_records {
    bigint id PK
    bigint domain_id FK
    varchar dns_type
    varchar name
    text content
    jsonb data
    timestamp created_at
    timestamp updated_at
  }

  logs_update {
    bigint id PK
    bigint domain_id FK
    bigint account_id FK
    varchar name
    varchar status
    jsonb response
    jsonb request
    jsonb error
    timestamp created_at
  }

  users ||--o{ unit_responsibles : "has"
  units ||--o{ unit_responsibles : "has"

  units ||--o{ account_domains : "owns"
  account_domains ||--o{ ns_accounts : "has"

  account_domains ||--o{ domains : "registerable"
  account_domains ||--o{ domains : "manageable"

  domains ||--o{ who_is : "has"
  domains ||--o{ ssls : "has"
  domains ||--o{ dns_records : "has"
  domains ||--o{ logs_update : "logs"
  account_domains ||--o{ logs_update : "logs"
````

## Notes

* dns_records.dns_type: A | AAAA | CNAME | MX | TEXT
* logs_update.status: success | error
* account_domains.name: ukraine_host | name_cheap | go_daddy | whois | cloud_flare
* account_domains.status: active | inactive | warning | ban
* account_domains unique: (name, login)
* account_domains.accesses: provider-specific jsonb settings/credentials
* ns_accounts unique: (account_id, ns)
