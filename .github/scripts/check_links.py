#!/usr/bin/env python3
"""Run the same check across every markdown file in the repo.

Checks per file:
  1. relative links      -> does the target path exist on disk?
  2. cross-file anchors  -> does the heading actually exist in the target?
  3. same-file anchors   -> does the heading exist here?
  4. external links      -> HTTP status (cached, threaded)
"""
import os, re, sys, json
from concurrent.futures import ThreadPoolExecutor
import urllib.request, urllib.error

ROOT = "."
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

def gh_slug(h):
    """GitHub heading -> anchor. lowercase, strip non [alnum/space/hyphen],
    spaces->hyphens (runs are NOT collapsed)."""
    s = h.strip()
    s = re.sub(r'`([^`]*)`', r'\1', s)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)      # links -> text
    s = re.sub(r'[*_]', '', s)
    s = s.lower()
    s = re.sub(r'[^\w\s-]', '', s, flags=re.UNICODE)
    return s.replace(' ', '-')

def headings(path):
    if not os.path.isfile(path):
        return None
    out = []
    infence = False
    for line in open(path, encoding='utf-8', errors='replace'):
        if line.lstrip().startswith('```'):
            infence = not infence; continue
        if infence: continue
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m: out.append(gh_slug(m.group(2)))
    return out

def strip_code(t):
    t = re.sub(r'```.*?```', '', t, flags=re.S)
    t = re.sub(r'`[^`\n]*`', '', t)
    return t

mds = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d != '.git']
    for f in fn:
        if f.endswith('.md'):
            mds.append(os.path.join(dp, f))
mds.sort()

link_re = re.compile(r'\[[^\]]*\]\(\s*<?([^)\s>]+)>?\s*(?:"[^"]*")?\)')

ext_urls = set()
records = []   # (srcfile, raw, kind, detail)

for md in mds:
    raw_t = open(md, encoding='utf-8', errors='replace').read()
    t = strip_code(raw_t)
    d = os.path.dirname(md)
    own = headings(md)
    for m in link_re.finditer(t):
        raw = m.group(1)
        if raw.startswith('mailto:'): continue
        if raw.startswith(('http://', 'https://')):
            ext_urls.add(raw); records.append((md, raw, 'ext', raw)); continue
        if raw.startswith('#'):
            a = raw[1:]
            ok = a in (own or [])
            records.append((md, raw, 'anchor-self', 'OK' if ok else 'BROKEN'))
            continue
        path, _, anc = raw.partition('#')
        if path in ('', '.'):
            ok = anc in (own or [])
            records.append((md, raw, 'anchor-self', 'OK' if ok else 'BROKEN'))
            continue
        tgt = os.path.normpath(os.path.join(d, path))
        if os.path.isdir(tgt):
            if anc:
                hh = headings(os.path.join(tgt, 'README.md'))
                if hh is None:
                    records.append((md, raw, 'rel', 'DIR-NO-README'))
                else:
                    records.append((md, raw, 'anchor-x',
                                    'OK' if anc in hh else 'BROKEN-ANCHOR'))
            else:
                records.append((md, raw, 'rel', 'OK'))
        elif os.path.isfile(tgt):
            if anc:
                hh = headings(tgt)
                records.append((md, raw, 'anchor-x',
                                'OK' if anc in hh else 'BROKEN-ANCHOR'))
            else:
                records.append((md, raw, 'rel', 'OK'))
        else:
            records.append((md, raw, 'rel', 'MISSING-PATH'))

def fetch(u):
    import time
    for attempt in range(4):
        try:
            r = urllib.request.Request(u, headers={'User-Agent': UA})
            with urllib.request.urlopen(r, timeout=30) as resp:
                return u, resp.status
        except urllib.error.HTTPError as e:
            if e.code in (429, 403) and attempt < 3:
                time.sleep(8 * (attempt + 1)); continue
            return u, e.code
        except Exception as e:
            if attempt < 3:
                time.sleep(4); continue
            return u, f'ERR {type(e).__name__}'
    return u, 'ERR retries'

status = {}
with ThreadPoolExecutor(max_workers=4) as ex:
    for u, s in ex.map(fetch, sorted(ext_urls)):
        status[u] = s

json.dump({'records': [list(r) for r in records], 'status': {k: str(v) for k, v in status.items()}},
          open('check_results.json', 'w'), indent=1)

# ---------- report ----------
print("=" * 78)
print(f"CHECKED {len(mds)} markdown files · {len(records)} links · {len(ext_urls)} unique external")
print("=" * 78)

problems = {}
for md, raw, kind, detail in records:
    bad = False
    if kind == 'ext':
        s = str(status.get(raw, '?'))
        bad = not s.startswith('2')
        detail = s
    else:
        bad = detail != 'OK'
    if bad:
        problems.setdefault(md, []).append((kind, raw, detail))

if not problems:
    print("\n  NO BROKEN LINKS IN ANY FILE\n")
else:
    for md in sorted(problems):
        print(f"\n### {md.replace(ROOT+'/','')}")
        for kind, raw, detail in problems[md]:
            print(f"   [{detail}]  ({kind})  {raw}")

print("\n" + "=" * 78)
print("PER-FILE SUMMARY")
print("=" * 78)
for md in mds:
    n = len([r for r in records if r[0] == md])
    b = len(problems.get(md, []))
    flag = "  <-- BROKEN" if b else ""
    print(f"  {'FAIL' if b else 'ok  '}  {md.replace(ROOT+'/',''):52} {n:3} links, {b} bad{flag}")
