---
name: api-integration-domain-registrar
description: Use this skill when implementing or extending the unified integration layer for multiple domain registrars (Cloudflare, UkraineHost, Namecheap, GoDaddy) to list account domains (including expiration when available), list DNS records when supported, and enforce provider rate limits in a multi-account system via a factory-based adapter design.
---

# Domain Registrar Integrations (Domains + DNS Records)

## Goal
Implement a unified integration layer to interact with multiple domain registrars/providers:
- `cloud_flare`
- `name_cheap`
- `ukraine_host`
- `go_daddy`
- `whois` (DEFERRED: later we will treat `whois` as `whois.com` specifically)

The system is multi-account: all credentials/access tokens/keys are stored in the database and selected per account.

This skill covers **read-only** capabilities for now:
1) List all domains for a given account (and get expiration date when possible)
2) List DNS records for a given domain when the provider supports DNS management

## Non-Goals (for now)
- Purchasing, renewing, transferring domains
- Creating/updating/deleting DNS records (may be added later)
- Implementing `whois.com` integration (explicitly postponed)

## Where to Look
Provider-specific details are **not** in this skill. They live in:
- `references/registrars/cloud_flare.md`
- `references/registrars/name_cheap.md`
- `references/registrars/ukraine_host.md`
- `references/registrars/go_daddy.md`
- `references/registrars/whois.md` (placeholder; to be completed later as whois.com)

Each reference file must contain:
- Official docs links
- Auth method and required credentials fields
- Base URLs (prod/sandbox if any)
- Endpoints/commands needed for:
  - domain listing (+ expiration if available)
  - DNS record listing (if available)
- Pagination behavior
- Rate limit behavior (headers, retry strategy, quotas)
- Minimal request/response examples
- Common errors (401/403/429 etc.)

## Core Design

### Provider keys
Use stable string keys (stored in DB and used by the factory):
- `cloud_flare`, `name_cheap`, `ukraine_host`, `go_daddy`, `whois`

### Interfaces
Define small, future-proof interfaces. Providers may not implement all of them.

**1) Domains**
`DomainProvider`:
- `list_domains(account_id) -> list[DomainSummary]`

`DomainSummary` should include (nullable where not available):
- `name: str`
- `expires_at: datetime | None`
- `provider_domain_id: str | None` (if provider uses internal id)
- `raw: dict` (optional, for debugging)

**2) DNS**
`DnsProvider`:
- `list_dns_records(account_id, domain: str) -> list[DnsRecord]`

`DnsRecord`:
- `type: str`
- `name: str`
- `value: str`
- `ttl: int | None`
- `priority: int | None`
- `raw: dict` (optional)

### Stubs / Unsupported features
A provider may not support DNS listing or domain listing via API.
In that case, return a structured “not supported” result instead of crashing.

Recommended pattern:
- Raise `FeatureNotSupported(provider_key, feature_name)` and catch at service layer
  OR
- Return `Result` objects:
  - `supported: bool`
  - `data: ...`
  - `reason: str`

Pick one approach and apply consistently across providers.

### Factory
Use a factory to instantiate the correct adapter based on `provider_key` from DB:

- `RegistrarClientFactory.create(provider_key, credentials) -> RegistrarClient`
- `RegistrarClient` can expose:
  - `domains(): DomainProvider`
  - `dns(): DnsProvider`

If you prefer composition:
- `DomainProviderFactory.create(...)`
- `DnsProviderFactory.create(...)`

But keep the call-site simple and uniform.

## Credentials & Storage (DB)
All secrets live in DB per account + provider key.

Store:
- `provider_key`
- `account_id`
- `auth_type` (token, key/secret, user/pass, etc.)
- `secrets` (encrypted JSON blob)
- `meta` (JSON: base_url override, environment, client_ip, etc.)

The adapter must never read env vars directly; it must only use DB-provided credentials.

## Rate Limiting (must-have)
We need a shared approach because providers differ:
- Some have strict per-minute quotas (e.g., GoDaddy-like limits)
- Some return `Retry-After` / rate-limit headers
- Some effectively require throttling (e.g., low RPS)

### Required behavior
Every request must go through a common “rate limit gate”:
1) Check if request is allowed now
2) If not allowed, return `next_allowed_at` (or raise a dedicated error)
3) If allowed, execute request
4) Persist rate-limit signals from response headers (when present)
5) On 429:
   - respect `Retry-After` if provided
   - compute backoff and store `next_allowed_at`

### Data model (suggested)
Persist per `(account_id, provider_key)`:
- `next_allowed_at: datetime | None`
- `window_reset_at: datetime | None` (if provider gives it)
- `remaining: int | None` (if provider gives it)
- `last_response_headers: dict | None`
- `updated_at`

Storage can be DB or Redis. If Redis exists, prefer Redis for low latency, and periodically sync to DB if you need auditability.

### Common helper
Implement a shared component:
- `RateLimiterGate.acquire(account_id, provider_key, cost=1) -> Allowed | Denied(next_allowed_at)`
- `RateLimiterGate.observe_response(account_id, provider_key, response_headers, status_code)`

Adapters must call this helper for every HTTP call.

## Expiration Date Strategy
Goal: include `expires_at` when possible.

Rules:
1) Prefer registrar/provider API if it returns expiration directly.
2) If provider cannot return expiration for “account domains”, expiration may remain `None`.
3) A future enhancement may add per-domain RDAP/WHOIS lookup as a fallback (note: those do NOT list account domains; they only query a specific domain).

Do NOT silently call WHOIS/RDAP for every domain unless explicitly enabled (it’s slow and may be rate-limited externally).

## Error Handling (uniform)
Normalize provider errors into a small set of domain exceptions:
- `AuthError` (401/403)
- `RateLimited(next_allowed_at)`
- `FeatureNotSupported(feature)`
- `ProviderTransientError` (timeouts, 5xx)
- `ProviderDataError` (unexpected schema, parse issues)

Never leak secrets into logs. Log:
- provider_key, account_id, endpoint name, status code, request id (if any), safe error message.

## Implementation Steps (agent checklist)
1) Create interfaces (`DomainProvider`, `DnsProvider`) and shared DTOs.
2) Implement `RegistrarClientFactory` + adapter base class.
3) Implement `RateLimiterGate` + persistence.
4) For each provider:
   - Add `references/registrars/<provider>.md` (docs, auth, endpoints, rate limits)
   - Implement adapter:
     - `list_domains`
     - `list_dns_records` (or stub)
   - Add tests with mocked HTTP responses and recorded fixtures.
5) Add a service layer:
   - `DomainService.get_account_domains(account_id)`
   - `DnsService.get_domain_records(account_id, domain)`
6) Ensure new providers can be added without touching existing adapters (open/closed).

## Acceptance Criteria
- For a given `(account_id, provider_key)`:
  - `list_domains()` returns all domains or a clear unsupported result
  - Expiration date is populated when the provider supports it
  - `list_dns_records(domain)` returns records or clear unsupported result
- Rate limit is enforced and cached:
  - 429 triggers backoff and returns `next_allowed_at`
- All provider-specific knowledge lives in `references/registrars/*.md`

## References
See `references/registrars/*.md` (provider-specific).
