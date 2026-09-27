"""Write the enrichment in e*.py into every problems/*/*/problem.json.

Each e*.py defines E[id] = (impact 'c'|'e', jsBridge markdown, [(kind, question), ...], transcript keywords, reference key).
  python3 authoring/enrichment/apply.py          # apply, then report problems still missing enrichment
"""
import glob, json, os, sys

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..'))
E = {}
for f in sorted(glob.glob(os.path.join(here, 'e*.py'))):
    scope = {}
    exec(open(f).read(), scope)
    dupes = set(scope['E']) & set(E)
    if dupes: sys.exit(f'{os.path.basename(f)} redefines {sorted(dupes)}')
    E.update(scope['E'])

KINDS = {'practice', 'js', 'java', 'contrast', 'edge'}
applied, missing, unknown = 0, [], set(E)
for path in sorted(glob.glob(os.path.join(root, 'problems', '*', '*', 'problem.json'))):
    meta = json.load(open(path))
    pid = meta['id']
    if pid not in E:
        missing.append(pid)
        continue
    unknown.discard(pid)
    impact, js, compass, keywords, ref = E[pid]
    assert impact in ('c', 'e'), pid
    assert all(k in KINDS for k, _ in compass) and len(compass) >= 3, pid
    meta['impact'] = 'core' if impact == 'c' else 'edge'
    meta['jsBridge'] = js.strip()
    meta['compass'] = [{'kind': k, 'q': q} for k, q in compass]
    json.dump(meta, open(path, 'w'), indent=2, ensure_ascii=False)
    open(path, 'a').write('\n')
    applied += 1

print(f'applied to {applied} problems; {len(missing)} still missing')
if unknown: print('entries for unknown ids:', sorted(unknown))
if missing: print('missing:', ' '.join(missing[:20]), '…' if len(missing) > 20 else '')
