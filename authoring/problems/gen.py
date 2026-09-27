"""Expand compact problem specs into problem folders (the folders are canonical)."""
import json, os, re, textwrap

ROOT = '/Users/shrishti/Desktop/varun_notes/swift-judge/problems'

def split_top(s, sep=','):
    out, depth, cur = [], 0, ''
    for ch in s:
        if ch in '[(<': depth += 1
        if ch in '])>': depth -= 1
        if ch == sep and depth == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    if cur.strip(): out.append(cur)
    return [x.strip() for x in out]

def parse_sig(sig):
    m = re.match(r'func\s+(\w+)\s*\((.*)\)\s*(async)?\s*(throws)?\s*(?:->\s*(.+))?$', sig.strip(), re.S)
    assert m, sig
    name, params, is_async, throws, ret = m.groups()
    ps = []
    for p in split_top(params):
        left, typ = p.split(':', 1)
        typ = typ.strip()
        words = left.split()
        label, pname = (words[0], words[1]) if len(words) == 2 else (None, words[0])
        d = {'name': pname, 'type': typ}
        if typ.startswith('inout '):
            d['type'] = typ[6:].strip(); d['inout'] = True
        if label: d['label'] = label
        ps.append(d)
    out = {'name': name, 'params': ps, 'returns': (ret or 'Void').strip()}
    if throws: out['throws'] = True
    if is_async: out['async'] = True
    return out

def placeholder(ret):
    ret = (ret or 'Void').strip()
    if ret in ('Void', '()'): return None
    if ret.endswith('?'): return 'nil'
    if ret in ('Int', 'Int64', 'UInt', 'UInt8'): return '0'
    if ret in ('Double', 'Float'): return '0'
    if ret == 'String': return '""'
    if ret == 'Bool': return 'false'
    if ret.startswith('[') and ':' in ret and not ret.startswith('[['): return '[:]'
    if ret.startswith('['): return '[]'
    return None

def starter_from_sig(sig):
    m = re.match(r'(.*?)(?:->\s*(.+))?$', sig.strip(), re.S)
    ret = m.group(2)
    ph = placeholder(ret)
    body = '    // your code here\n'
    if ph is not None: body += f'    return {ph}\n'
    elif ret and ret.strip() not in ('Void', '()'): body += '    fatalError("not implemented")\n'
    return sig.strip() + ' {\n' + body + '}\n'

def dd(s):
    return textwrap.dedent(s).strip('\n') + '\n' if s else ''

def write(spec):
    track = spec['dir'].split('/')[0]
    d = os.path.join(ROOT, spec['dir'])
    os.makedirs(d, exist_ok=True)
    old_meta = json.load(open(os.path.join(d, 'problem.json'))) if os.path.exists(os.path.join(d, 'problem.json')) else None
    for f in os.listdir(d): os.remove(os.path.join(d, f))
    mode = spec.get('mode', 'function')
    meta = {
        'id': spec['id'], 'title': spec['title'], 'track': track,
        'difficulty': spec.get('diff', 'easy'), 'topic': spec['topic'],
        'concepts': spec.get('concepts', []), 'mode': mode,
    }
    if spec.get('notes'): meta['notesRef'] = spec['notes']
    meta['docs'] = [({'title': t, 'book': b} if not b.startswith('http') else {'title': t, 'url': b}) for t, b in spec.get('docs', [])]
    if mode == 'function' and spec.get('sig'):
        meta['signature'] = parse_sig(spec['sig'])
    for k in ('compare', 'timeLimitMs', 'swiftVersion', 'starterFails', 'platforms'):
        if k in spec: meta[k] = spec[k]
    # Preserve references/hints already on disk unless the spec provides them.
    if spec.get('hints'): meta['hints'] = list(spec['hints'])
    if spec.get('videos') and not (old_meta or {}).get('videos'): meta['videos'] = [{'title': t, 'url': u, 'channel': c} for t, u, c in spec['videos']]
    if old_meta:
        old = old_meta
        for k in ('hints', 'videos', 'articles', 'impact', 'jsBridge', 'compass'):
            if k not in meta and old.get(k): meta[k] = old[k]
        # Keep extra Apple-doc URL links added by the references pass.
        extra = [x for x in old.get('docs', []) if x.get('url') and x not in meta['docs']]
        meta['docs'] += extra
    json.dump(meta, open(os.path.join(d, 'problem.json'), 'w'), indent=2, ensure_ascii=False)
    open(os.path.join(d, 'statement.md'), 'w').write(dd(spec['statement']))
    open(os.path.join(d, 'explanation.md'), 'w').write(dd(spec.get('explain', '')))
    if mode == 'predict':
        open(os.path.join(d, 'snippet.swift'), 'w').write(dd(spec['snippet']))
        tests = [{}]
    else:
        starter = spec.get('starter')
        if starter is None and mode == 'function' and spec.get('sig'): starter = starter_from_sig(spec['sig'])
        open(os.path.join(d, 'starter.swift'), 'w').write(dd(starter or ''))
        open(os.path.join(d, 'solution.swift'), 'w').write(dd(spec['solution']))
        if spec.get('harness'): open(os.path.join(d, 'harness.swift'), 'w').write(dd(spec['harness']))
        tests = []
        raw = spec['tests']
        nhidden = spec.get('hidden', max(1, len(raw) // 3) if len(raw) >= 3 else 0)
        for i, t in enumerate(raw):
            if isinstance(t, dict) and ('pattern' in t or 'severity' in t or 'name' in t and 'input' in t):
                tc = dict(t)
            elif isinstance(t, tuple):
                tc = {'input': t[0], 'expected': t[1]}
            else:
                tc = {'input': t}
            if i >= len(raw) - nhidden and mode != 'diagnostic': tc['hidden'] = True
            tests.append(tc)
    json.dump(tests, open(os.path.join(d, 'tests.json'), 'w'), indent=1, ensure_ascii=False)

def write_all(specs, track, base):
    ids = set()
    for i, s in enumerate(specs):
        assert s['id'] not in ids, s['id']; ids.add(s['id'])
        s['dir'] = f"{track}/{base + 5 * i:03d}-{s['id']}"
        write(s)
    print(f'wrote {len(specs)} problems')
