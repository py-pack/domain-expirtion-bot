# GoDaddy (go_daddy)

> Scope: read-only integration for:
> 1) listing account domains (+ expiration when available)
> 2) listing DNS records for a domain
> Plus: rate limit handling.

## Official docs (primary)
- Get started + auth header format: https://developer.godaddy.com/getstarted 
- Domains API (interactive): https://developer.godaddy.com/doc/endpoint/domains 
- Domains API Swagger (source of truth for endpoints/fields): https://developer.godaddy.com/swagger/swagger_domains.json 
- API Terms (rate limit statement): https://www.godaddy.com/legal/agreements/godaddy-api-terms-of-use 

## Auth
GoDaddy uses API Key + Secret via `Authorization` header:
- `Authorization: sso-key <API_KEY>:<API_SECRET>` 

DB credentials (suggested shape):
- `api_key` (string)
- `api_secret` (string)
- Optional: `shopper_id` (string) — if you need `X-Shopper-Id` for reseller scenarios.

## Base URLs
- Production: https://api.godaddy.com
- OTE (testing): https://api.ote-godaddy.com 

## Mapping “domains” and “DNS”
- “List account domains” => `GET /v1/domains`
- “List DNS records” => `GET /v1/domains/{domain}/records` (all records) or more specific endpoints for type/name.

Source: Domains swagger spec.

### Expiration date
`/v1/domains` returns `expires` per domain (date-time). Use it as `expires_at`.

## Endpoints

### 1) List domains (account domains)
`GET https://api.godaddy.com/v1/domains` 

Request notes (from swagger):
- Optional header: `X-Shopper-Id` (if applicable)
- Pagination: `limit` (max 1000), `marker` for offset-style paging
- Filtering: `statuses`, `statusGroups`, `modifiedDate`, `includes` (authCode/contacts/nameServers)

Minimal curl (secrets omitted):
```bash
curl -s "https://api.godaddy.com/v1/domains" \
  -H "Authorization: sso-key <...>:<...>" \
  -H "Accept: application/json"
````

### 2) List DNS records for a domain (all)

`GET https://api.godaddy.com/v1/domains/{domain}/records`  ([developer.godaddy.com][1])

Minimal curl:

```bash
curl -s "https://api.godaddy.com/v1/domains/<domain>/records" \
  -H "Authorization: sso-key <...>:<...>" \
  -H "Accept: application/json"
```

### 3) List DNS records by type + name (granular)

`GET https://api.godaddy.com/v1/domains/{domain}/records/{type}/{name}`  ([developer.godaddy.com][1])

Notes:

* `type` enum includes: A, AAAA, CNAME, MX, NS, SOA, SRV, TXT (per swagger). ([developer.godaddy.com][1])

## Pagination

* Domains list: `limit` + `marker` (marker domain as offset). ([developer.godaddy.com][1])
* DNS endpoints: typically return arrays; swagger also mentions `offset`/`limit` for some type/name queries. ([developer.godaddy.com][1])

Implementation note:

* For `/v1/domains`: loop while response count == limit and next marker is present/derivable.

## Rate limits

GoDaddy explicitly states: each API endpoint has a limit of **60 requests per minute**. ([GoDaddy][2])
Swagger indicates `429 Too many requests received within interval` for key endpoints. ([developer.godaddy.com][1])

Adapter requirements:

* Enforce client-side throttling around 60 RPM per endpoint per credential set (conservative).
* On HTTP 429:

  * If `Retry-After` header exists, set `next_allowed_at = now + retry_after_seconds` (not guaranteed documented for GoDaddy; handle if present).
  * Otherwise use exponential backoff + jitter and persist `next_allowed_at`.

## Common errors

* 401: auth header missing/invalid (AuthError) ([developer.godaddy.com][1])
* 403: forbidden / permissions (AuthError)
* 404: domain not found (ProviderDataError)
* 429: rate limited (RateLimited) ([developer.godaddy.com][1])
* 5xx/504: transient (ProviderTransientError) ([developer.godaddy.com][1])

## Minimal DTO mapping

### DomainSummary (from GET /v1/domains)

* `name` = `domain`
* `provider_domain_id` = `domainId` (if present) ([developer.godaddy.com][1])
* `expires_at` = `expires` ([developer.godaddy.com][1])
* `raw` = safe subset

### DnsRecord (from records endpoints)

* map fields returned by GoDaddy `DNSRecord` schema (type/name/data/ttl/priority, etc.) (provider-specific; follow swagger definitions). ([developer.godaddy.com][1])


## developer.godaddy.com

[1]: https://developer.godaddy.com/swagger/swagger_domains.json "developer.godaddy.com"
[2]: https://www.godaddy.com/legal/agreements/godaddy-api-terms-of-use?utm_source=chatgpt.com "GoDaddy API Terms of Use Agreement"
