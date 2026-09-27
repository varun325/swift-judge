import json, re, sys

def initial_data(html):
    m = re.search(r'var ytInitialData = (\{.*?\});</script>', html, re.S) or re.search(r'ytInitialData"\]\s*=\s*(\{.*?\});', html, re.S)
    return json.loads(m.group(1))

def text(v):
    if isinstance(v, str): return v
    if isinstance(v, dict):
        if 'content' in v: return v['content']
        if 'simpleText' in v: return v['simpleText']
        if 'runs' in v: return ''.join(r.get('text', '') for r in v['runs'])
    return ''

def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values(): yield from walk(v)
    elif isinstance(o, list):
        for v in o: yield from walk(v)

def playlists(html):
    out = {}
    for d in walk(initial_data(html)):
        if 'lockupViewModel' in d:
            lv = d['lockupViewModel']
            if lv.get('contentType') == 'LOCKUP_CONTENT_TYPE_PLAYLIST':
                title = text(lv.get('metadata', {}).get('lockupMetadataViewModel', {}).get('title', {}))
                count = ''
                for x in walk(lv.get('contentImage', {})):
                    if 'text' in x and isinstance(x['text'], str) and 'video' in x['text'].lower(): count = x['text']
                out[lv['contentId']] = (title, count)
        if 'gridPlaylistRenderer' in d:
            g = d['gridPlaylistRenderer']; out[g['playlistId']] = (text(g.get('title')), text(g.get('videoCountText')))
    return out

def videos(html):
    out = []
    for d in walk(initial_data(html)):
        r = d.get('playlistVideoRenderer') or d.get('videoRenderer') or d.get('gridVideoRenderer')
        if r and 'videoId' in r:
            out.append((r['videoId'], text(r.get('title'))))
        if 'lockupViewModel' in d and d['lockupViewModel'].get('contentType') == 'LOCKUP_CONTENT_TYPE_VIDEO':
            lv = d['lockupViewModel']
            out.append((lv['contentId'], text(lv.get('metadata', {}).get('lockupMetadataViewModel', {}).get('title', {}))))
    seen = set(); res = []
    for v in out:
        if v[0] not in seen: seen.add(v[0]); res.append(v)
    return res

if __name__ == '__main__':
    mode, path = sys.argv[1], sys.argv[2]
    html = open(path, encoding='utf-8', errors='ignore').read()
    if mode == 'playlists':
        for pid, (t, c) in playlists(html).items(): print(f'{pid}\t{c}\t{t}')
    else:
        for vid, t in videos(html): print(f'{vid}\t{t}')
