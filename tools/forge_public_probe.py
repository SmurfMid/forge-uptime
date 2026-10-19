#!/usr/bin/env python3
"""FORGE_PUBLIC_PROBE_V1 (grok, 2026-10-19). Outside uptime check for Forge Chat 1.0 (item 7) and Forge App 1.0.
Public URLs only, unauthenticated GETs, no keys or secrets, no writes except stdout and an optional JSONL line.
 Q1 chat_access   GET https://forge.elienterprise.app/app/chat.html   -> 302 to https://elienterprise.cloudflareaccess.com/...
 Q2 app_access    GET https://forge.elienterprise.app/app/v1/index.html -> 302 to the same Access host (route behind Access)
 Q3 root_access   GET https://forge.elienterprise.app/                -> 302 to the same Access host
 Q4 site_up       GET https://elienterprise.app/                      -> 200
Exit 0 when all pass, 1 otherwise. Usage: forge_public_probe.py [--jsonl FILE]"""
import json, sys, time, urllib.request, urllib.error, datetime as dt
ACCESS = 'https://elienterprise.cloudflareaccess.com/'
CHECKS = [('chat_access', 'https://forge.elienterprise.app/app/chat.html'), ('app_access', 'https://forge.elienterprise.app/app/v1/index.html'),
          ('root_access', 'https://forge.elienterprise.app/')]
SITE = ('site_up', 'https://elienterprise.app/')
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
op = urllib.request.build_opener(NoRedirect)
def get(u):
    try: r = op.open(urllib.request.Request(u, headers={'User-Agent': 'forge-public-probe'}), timeout=15); return r.status, r.headers.get('Location', '')
    except urllib.error.HTTPError as e: return e.code, e.headers.get('Location', '')
    except Exception as e: return 0, repr(e)[:120]
row = {'v': 'FORGE_PUBLIC_PROBE_V1', 'ts': dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(), 'checks': {}}
for name, u in CHECKS:
    c, loc = get(u); ok = c == 302 and loc.startswith(ACCESS)
    row['checks'][name] = {'pass': ok, 'code': c, 'to_access': loc.startswith(ACCESS)}   # the Access URL itself is not stored (it carries a one-time meta token)
c, _ = get(SITE[1]); row['checks'][SITE[0]] = {'pass': c == 200, 'code': c}
row['pass'] = all(v['pass'] for v in row['checks'].values())
print(json.dumps(row))
if '--jsonl' in sys.argv:
    with open(sys.argv[sys.argv.index('--jsonl') + 1], 'a') as f: f.write(json.dumps(row) + '\n')
sys.exit(0 if row['pass'] else 1)
