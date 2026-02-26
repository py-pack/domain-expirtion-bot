# Cloudflare (cloud_flare)

> Scope: read-only integration for:
> 1) listing account domains (Cloudflare **Zones**)
> 2) listing DNS records for a zone
> Plus: rate limit handling signals.

## Official docs (primary)
- SDKs overview (includes Python): https://developers.cloudflare.com/fundamentals/api/reference/sdks/ 
- List Zones: https://developers.cloudflare.com/api/resources/zones/methods/list/ 
- List DNS Records: https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/list/ 
- API limits: https://developers.cloudflare.com/fundamentals/api/reference/limits/ 
- 429 guidance: https://developers.cloudflare.com/support/troubleshooting/http-status-codes/4xx-client-error/error-429/ 
- Rate limit header improvements: https://developers.cloudflare.com/changelog/2025-09-03-rate-limiting-improvement/ 

## Python library (preferred)
Use Cloudflare’s official Python SDK:
- GitHub: https://github.com/cloudflare/cloudflare-python 
- PyPI package: https://pypi.org/project/cloudflare/ 

Notes:
- Provides typed requests/responses, sync + async clients (httpx-based).
- Legacy repo `cloudflare/python-cloudflare` is archived; do not use for new work.
- There is a breaking-change beta noted recently; pin versions consciously.

Install:
```bash
pip install cloudflare
````

## Auth

Preferred: **API Token** (Bearer):

* `Authorization: Bearer <token>`

DB credentials (suggested):

* `api_token` (string)
* Optional: `account_id` (string) for filtering zones by account

## Mapping “domains” to Cloudflare entities

Cloudflare “domains” in this system are **Zones** (e.g., `example.com`).

* “List account domains” => `GET /zones`
* “List DNS records” => `GET /zones/{zone_id}/dns_records`

### Expiration date

Cloudflare Zones API generally does **not** provide domain registrar expiration.
So `expires_at = null` for Cloudflare in this scope (until a separate registrar-specific integration is added).

## Endpoints

Base: `https://api.cloudflare.com/client/v4`

### 1) List zones (account domains)

`GET /zones`  ([GitHub][1])
Supports pagination (`page`, `per_page`) and filters (e.g., `account.id`). ([GitHub][1])

### 2) List DNS records for a zone

`GET /zones/{zone_id}/dns_records`  ([GitHub][1])
Also paginated; supports filters (type/name/content). ([GitHub][1])

## Pagination

Both endpoints are paginated. ([GitHub][1])
Implementation: iterate pages until exhausted; keep parsing tolerant.

## Rate limits

Cloudflare documents limits and 429 behavior. ([GitHub][1])

Headers:

* Always: `Ratelimit`, `Ratelimit-Policy`
* On 429: `Retry-After` ([GitHub][1])

Adapter requirements:

* Every request goes through shared `RateLimiterGate`.
* On 429: respect `Retry-After`; persist `next_allowed_at`.

## Minimal DTO mapping

### DomainSummary (Zone)

* `name` = zone.name
* `provider_domain_id` = zone.id
* `expires_at` = null
* `raw` = safe subset

### DnsRecord (DNS record)

* `type`, `name`, `content/value`, `ttl`, `priority` (if present)
* `raw` = safe subset


## Python library (preferred) + example calls
Official SDK:
- https://github.com/cloudflare/cloudflare-python
- https://pypi.org/project/cloudflare/

Install:
```bash
pip install cloudflare
````

### Minimal client setup

```python
from cloudflare import Cloudflare

cf = Cloudflare(api_token=CF_API_TOKEN)  # token from DB
```

### List account domains (Zones)

```python
zones = []
page = 1

while True:
    resp = cf.zones.list(page=page, per_page=50)  # keep per_page modest
    items = list(resp)
    if not items:
        break

    for z in items:
        zones.append({
            "name": z.name,
            "provider_domain_id": z.id,
            "expires_at": None,  # Cloudflare zones don't expose registrar expiry in this scope
        })

    page += 1
```

### List DNS records for a domain (by zone_id)

```python
records = []
page = 1

while True:
    resp = cf.dns.records.list(zone_id=ZONE_ID, page=page, per_page=100)
    items = list(resp)
    if not items:
        break

    for r in items:
        records.append({
            "type": r.type,
            "name": r.name,
            "value": getattr(r, "content", None),
            "ttl": getattr(r, "ttl", None),
            "priority": getattr(r, "priority", None),
        })

    page += 1
```

### Notes

* Prefer SDK objects; keep raw HTTP only as fallback.
* Still run all SDK calls through the shared RateLimiterGate in your adapter layer
  (observe headers; handle 429 + Retry-After if present).


## GitHub link
[1]: https://github.com/cloudflare/cloudflare-python "The official Python library for the Cloudflare API"
