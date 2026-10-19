# forge-uptime

Outside uptime probe for Forge Chat 1.0 (release item 7: "stays up 7 days") and Forge App 1.0.
Public, read-only checks every 15 minutes from GitHub Actions. There are no secrets, keys, private hosts or addresses in this repo.

| check | URL | pass |
|---|---|---|
| chat_access | https://forge.elienterprise.app/app/chat.html | 302 to the Cloudflare Access login |
| app_access | https://forge.elienterprise.app/app/v1/index.html | 302 to the Cloudflare Access login |
| root_access | https://forge.elienterprise.app/ | 302 to the Cloudflare Access login |
| site_up | https://elienterprise.app/ | 200 |

Results: one JSON line per run on the [`status` branch](../../blob/status/forge-public-probe.jsonl), plus each run's job summary. The Access login URL is not stored, because it carries a one-time token.
Pass rule (from the release card): every check passes on every run for 7 days in a row. A missing run counts as a gap.
Run locally: `python3 tools/forge_public_probe.py`.
