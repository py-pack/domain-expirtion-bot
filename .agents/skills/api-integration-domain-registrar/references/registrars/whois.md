# Whois.com (whois)

> Scope: read-only integration for:
> 1) listing account domains (domain registration orders)
> 2) listing DNS records when the provider DNS service is used
> Plus: rate limit handling.
>
> Note: Whois.com control panel exposes a Reseller/LogicBoxes-style HTTP API hosted on httpapi.com.

## Official / authoritative docs (primary)
```text
https://manage.whois.com/kb/answer/753         # Access & Authentication (base URL, auth params, IP whitelist)
https://manage.whois.com/kb/node/771           # Domains: Search (list domain registration orders)
https://manage.whois.com/kb/answer/1106        # DNS: search-records (dns/manage)
````

Auth + base URL: `https://httpapi.com/` with `auth-userid` and `api-key`, and IP must be whitelisted. ([manage.whois.com][1])
Domains list: `GET /api/domains/search.json` with paging. ([manage.whois.com][2])
DNS records search: `GET /api/dns/manage/search-records.json` (requires record type). ([manage.whois.com][3])

## Python library (preferred) + example calls

Maintained-ish options (unofficial):

* PyPI: `resellerclub-python` (wrapper for HTTP API) ([PyPI][4])
* GitHub: `miracle2k/resellerclub` (CLI + usable as a Python library) ([GitHub][5])

Install (pick one; prefer PyPI wrapper first):

```bash
pip install resellerclub-python
```

### Credentials (DB)

Required per account:

* `auth_userid` (integer reseller id)
* `api_key` (string)
  Also: caller public IP must be whitelisted in the control panel settings. ([manage.whois.com][1])

### Base URL

Production API base:

```text
https://httpapi.com/
```

Test URL exists but must not be used in production:

```text
https://test.httpapi.com/
```

([manage.whois.com][1])

## Mapping “domains” and “DNS”

### Domains

“List account domains” == list **Domain Registration Orders**:

* `GET /api/domains/search.json` ([manage.whois.com][2])

Important response fields include:

* domain name: `entity.description`
* order id: `orders.orderid`
* expiry timestamp (registry): `orders.endtime` ([manage.whois.com][2])

### DNS records

There are multiple DNS-related APIs in this ecosystem; for classic DNS zone style management use:

* `GET /api/dns/manage/search-records.json` (requires `type`) ([manage.whois.com][3])

Important: this endpoint **searches** records. To fetch “all records”, you must iterate record types:
`A, AAAA, CNAME, MX, TXT, NS, SRV` and merge results. ([manage.whois.com][3])

## Example calls (library-first)

> The exact method names depend on the chosen wrapper; keep the adapter logic the same.
> If the wrapper is too thin/unreliable, fall back to raw HTTP, but then remove/avoid these examples.

### List account domains (Domain Registration Orders)

API reference: `/api/domains/search.json` with `no-of-records` (10..500) and `page-no`. ([manage.whois.com][2])

```python
# pseudo-usage: implement through the chosen wrapper; keep paging
page_no = 1
per_page = 100
domains = []

while True:
    resp = client.domains.search(no_of_records=per_page, page_no=page_no)
    items = resp.get("orders", []) or resp.get("result", [])
    if not items:
        break

    for row in items:
        domains.append({
            "name": row["entity.description"],
            "provider_domain_id": row["orders.orderid"],
            "expires_at": row.get("orders.endtime"),  # unix timestamp -> datetime
        })

    page_no += 1
```

### List DNS records for a domain

API reference: `/api/dns/manage/search-records.json` requires `domain-name`, `type`, paging. ([manage.whois.com][3])

```python
TYPES = ["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SRV"]
all_records = []

for rtype in TYPES:
    page_no = 1
    while True:
        resp = client.dns.manage.search_records(
            domain_name=DOMAIN,
            type=rtype,
            no_of_records=100,
            page_no=page_no,
        )
        items = resp.get("recs", []) or resp.get("records", []) or []
        if not items:
            break

        for r in items:
            all_records.append({
                "type": r.get("type", rtype),
                "name": r.get("host"),
                "value": r.get("value"),
                "ttl": r.get("ttl"),
                "priority": r.get("priority"),
            })

        page_no += 1
```

## Rate limits

The docs emphasize “API abuse” handling, but do not give a universal numeric quota here.
Adapter requirements:

* Always run calls via shared `RateLimiterGate`.
* On 429 / “Access Denied” bursts: set conservative backoff and persist `next_allowed_at`.
* Treat IP whitelist propagation delay (up to ~1 hour) as a non-rate-limit auth failure case. ([manage.whois.com][1])

## Minimal DTO mapping

### DomainSummary (from domains/search)

* `name` = `entity.description`
* `provider_domain_id` = `orders.orderid`
* `expires_at` = `orders.endtime` (unix -> datetime) ([manage.whois.com][2])

### DnsRecord (from dns/manage/search-records)

* record types list is defined by the API (A/MX/CNAME/TXT/NS/SRV/AAAA). ([manage.whois.com][3])


## manage.whois.com Links
[1]: https://manage.whois.com/kb/answer/753 "Access and Authentication | KnowledgeBase"
[2]: https://manage.whois.com/kb/node/771 "Search | KnowledgeBase"
[3]: https://manage.whois.com/kb/answer/1106 "Searching DNS Records | KnowledgeBase"
[4]: https://pypi.org/project/resellerclub-python/?utm_source=chatgpt.com "resellerclub-python"
[5]: https://github.com/miracle2k/resellerclub?utm_source=chatgpt.com "miracle2k/resellerclub: Resellerclub API in Python"
