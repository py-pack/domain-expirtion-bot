# Namecheap (name_cheap)

> Scope: read-only integration for:
> 1) listing account domains (+ expiration when available)
> 2) listing DNS records for a domain
> Plus: rate limit handling.

## Official API docs (reference)
- Intro / enable API + whitelist IP: https://www.namecheap.com/support/api/intro/
- Global params (ApiUser/ApiKey/UserName/ClientIp): https://www.namecheap.com/support/api/global-parameters/
- Domains: getList: https://www.namecheap.com/support/api/methods/domains/get-list/
- DNS: getHosts: https://www.namecheap.com/support/api/methods/domains-dns/get-hosts/
- API FAQ (limits): https://www.namecheap.com/support/knowledgebase/article.aspx/9739/63/api-faq/

## Python library (preferred) + example calls
Use a maintained Python SDK:
- PyPI: https://pypi.org/project/namecheap-python/
- GitHub: https://github.com/adriangalilea/namecheap-python

Install:
```bash
pip install namecheap-python
````

### Credentials (DB)

Namecheap requires:

* `api_user`
* `api_key`
* `user_name`
* `client_ip` (must be whitelisted IPv4) ([Namecheap][2])

### Minimal client setup (concept)

> Use DB-stored credentials; do not read env vars in adapters.

```python id="8uvyq3"
# pseudocode-ish: keep this aligned with the SDK's actual client constructor
from namecheap import Namecheap  # library provides an API client

client = Namecheap(
    api_user=API_USER,
    api_key=API_KEY,
    user_name=USER_NAME,
    client_ip=CLIENT_IP,
    sandbox=False,  # or True for sandbox
)
```

### List account domains (+ expires_at)

Namecheap API source of truth: `namecheap.domains.getList` includes expiration (`Expires`). ([Namecheap][3])

```python id="m2l8u1"
# conceptual: method names depend on SDK version
domains = client.domains.get_list()  # wraps namecheap.domains.getList
out = [
    {
        "name": d.name,
        "provider_domain_id": getattr(d, "id", None),
        "expires_at": getattr(d, "expires", None),  # parse to datetime
    }
    for d in domains
]
```

### List DNS records for a domain

Namecheap API source of truth: `namecheap.domains.dns.getHosts` (needs SLD/TLD). ([Namecheap][4])

```python id="qxg1b6"
# split "example.com" -> SLD="example", TLD="com"
records = client.domains.dns.get_hosts(sld=SLD, tld=TLD)

out = [
    {
        "type": r.type,
        "name": r.name,
        "value": r.value,
        "ttl": getattr(r, "ttl", None),
        "priority": getattr(r, "priority", None),
    }
    for r in records
]
```

## Base URLs (FYI)

* Production: [https://api.namecheap.com/xml.response](https://api.namecheap.com/xml.response) ([Namecheap][3])
* Sandbox: [https://api.sandbox.namecheap.com/xml.response](https://api.sandbox.namecheap.com/xml.response) (see intro) ([Namecheap][2])

## Pagination

`getList` supports paging (provider-specific parameters in docs). ([Namecheap][3])
Adapter should iterate pages until exhausted.

## Rate limits

Namecheap mentions limits in API FAQ (values can change; treat as policy input). ([Namecheap][2])

Adapter requirements:

* Every SDK call passes through shared `RateLimiterGate`.
* On “too many requests” (or 429-like errors), persist `next_allowed_at` and return/raise `RateLimited(next_allowed_at)`.

## Notes / pitfalls

* If `client_ip` is not whitelisted, calls fail even with correct key. ([Namecheap][2])
* `getHosts` may not work if DNS is not managed by Namecheap for that domain (treat as unsupported per-domain, not a global provider failure).

## Minimal DTO mapping

### DomainSummary

* `name` = domain name
* `provider_domain_id` = id if available
* `expires_at` = Expires (when present) ([Namecheap][3])

### DnsRecord

* Map host record fields (type/name/value/ttl/priority). ([Namecheap][4])

## Namecheap Links

[1]: https://pypi.org/project/namecheap-python/?utm_source=chatgpt.com "Namecheap Python SDK"
[2]: https://www.namecheap.com/support/knowledgebase/subcategory/63/namecheap-api/?utm_source=chatgpt.com "Namecheap API - Namecheap.com Knowledgebase"
[3]: https://www.namecheap.com/support/api/methods/domains/get-list/?utm_source=chatgpt.com "API Documentation - namecheap.domains.getList"
[4]: https://www.namecheap.com/support/api/methods/domains-dns/get-hosts/?utm_source=chatgpt.com "API Documentation - namecheap.domains.dns.getHosts"
