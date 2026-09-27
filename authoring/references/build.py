"""Attach references to every problem: Apple docs, Swift book / Evolution articles, and one YouTube video per
creator with a timestamp (&t=) at the moment the problem's idea is discussed, found from the transcript.

  python3 authoring/references/build.py --dry [filter]   # print picks, change nothing
  python3 authoring/references/build.py                   # write problem.json files
"""
import concurrent.futures as cf, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'authoring', 'research'))
from transcript import transcript  # noqa: E402

exec(open(os.path.join(HERE, 'registry.py')).read())  # defines BOOK, AD, SE, R
ENRICH = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'authoring', 'enrichment', 'e*.py'))):
    scope = {}; exec(open(f).read(), scope); ENRICH.update(scope['E'])
# Teaching videos only: no Shorts, vlogs, podcasts, livestreams, or Q&A clips with guest speakers.
NOT_TEACHING = re.compile(r'#short|vlog|podcast|discussion|verdict|livestream|\blive\b|q ?& ?a|interview with|reacting|\?\s+[–-]\s+[A-Z][a-z]+ [A-Z]', re.I)
VIDEOS = [v for v in json.load(open(os.path.join(ROOT, 'authoring', 'research', 'all_videos.json')))
          if not NOT_TEACHING.search(v['title']) and v['title'].count(',') < 3]  # 3+ commas: a news roundup
CHANNELS = ['Swiftful Thinking', 'Paul Hudson', 'Sean Allen']
CHAPTERS = {
    'thebasics': 'The Basics', 'basicoperators': 'Basic Operators', 'stringsandcharacters': 'Strings and Characters',
    'collectiontypes': 'Collection Types', 'controlflow': 'Control Flow', 'functions': 'Functions', 'closures': 'Closures',
    'enumerations': 'Enumerations', 'classesandstructures': 'Structures and Classes', 'properties': 'Properties',
    'methods': 'Methods', 'inheritance': 'Inheritance', 'initialization': 'Initialization', 'optionalchaining': 'Optional Chaining',
    'errorhandling': 'Error Handling', 'concurrency': 'Concurrency', 'typecasting': 'Type Casting', 'extensions': 'Extensions',
    'protocols': 'Protocols', 'generics': 'Generics', 'opaquetypes': 'Opaque and Boxed Protocol Types',
    'automaticreferencecounting': 'Automatic Reference Counting', 'memorysafety': 'Memory Safety', 'accesscontrol': 'Access Control',
    'advancedoperators': 'Advanced Operators', 'expressions': 'Expressions', 'attributes': 'Attributes',
}
STOP = set('a an the to of in on with and or for by vs from your how what why when is are be do it its this that into using use swift swiftui ios app'.split())


def words(s):
    return [w for w in re.findall(r"[a-z][a-z0-9+#@']+", s.lower()) if w not in STOP and len(w) > 2]


def score_video(title, ref, keywords, problem_title):
    """Relevance of a video title to a problem; 0 unless it matches the topic or a problem keyword."""
    t = title.lower()
    s = 0
    terms = R[ref][3]
    hit = lambda k: re.search(r'(?<![a-z])' + re.escape(k.lower()), t) is not None
    topic = bool(terms) and re.search(terms[0], t, re.I) is not None
    # Must be about the topic or the problem's core idea (its first keyword); other keywords only rank.
    if not (topic or (keywords and hit(keywords[0]))):
        return 0
    s += 2 if topic else 0
    if len(terms) > 1 and re.search(terms[1], t, re.I): s += 1
    s += sum((4 if i == 0 else 3) for i, k in enumerate(keywords) if hit(k))
    s += sum(1 for w in set(words(problem_title)) if w in t)
    return s


def pick_videos(pid, meta):
    _, _, _, keywords, ref = ENRICH[pid]
    picks = []
    for ch in CHANNELS:
        best = max(((score_video(v['title'], ref, keywords, meta['title']), -i, v) for i, v in enumerate(VIDEOS) if v['channel'] == ch),
                   default=None, key=lambda x: (x[0], x[1]))
        if best and best[0] >= 4:
            picks.append(best[2])
    if not picks:
        # Nothing specific: fall back to the best topic-level lessons (at most two creators).
        terms = R[ref][3]
        def topic_score(v):
            t = v['title']
            s = (2 if re.search(terms[0], t, re.I) else 0) + (1 if len(terms) > 1 and re.search(terms[1], t, re.I) else 0)
            return s + sum(1 for w in set(words(meta['title'])) if w in t.lower())
        pool = [(topic_score(v), -i, v) for i, v in enumerate(VIDEOS)] if terms else []
        seen = set()
        for sc, _, v in sorted(pool, key=lambda x: (x[0], x[1]), reverse=True):
            if sc < 2 or v['channel'] in seen:
                continue
            seen.add(v['channel'])
            picks.append(v)
            if len(picks) == 2:
                break
    return picks


def find_moment(video_id, keywords, problem_title):
    cues = transcript(video_id)
    if not cues:
        return None
    specific = [k.lower() for k in keywords] + [w for w in words(problem_title) if len(w) > 4]
    best = (0, None)
    for i in range(len(cues)):
        window = ' '.join(c[1] for c in cues[i:i + 5]).lower()
        s = sum(3 if k in keywords[:1] else 1 for k in specific if k in window)
        if s > best[0]:
            best = (s, i)
    if best[1] is None or best[0] < 2:
        return None
    start = max(0, int(cues[best[1]][0]) - 2)
    moment = ' '.join(c[1] for c in cues[best[1]:best[1] + 3])
    return start, re.sub(r'\s+', ' ', moment).strip()[:160]


def with_time(url, start):
    base = re.sub(r'[&?]t=\d+s?', '', url)
    return f'{base}&t={start}s' if start else base


def main():
    dry = '--dry' in sys.argv
    flt = next((a for a in sys.argv[1:] if not a.startswith('--')), '')
    files = sorted(glob.glob(os.path.join(ROOT, 'problems', '*', '*', 'problem.json')))
    metas = [(f, json.load(open(f))) for f in files]
    metas = [(f, m) for f, m in metas if flt in m['id']]
    plan = {}
    for f, m in metas:
        pid = m['id']
        if m['track'] == 'cs193p':
            vids = [{'id': re.search(r'v=([\w-]{11})', v['url']).group(1), 'title': v['title'], 'channel': v['channel']} for v in m.get('videos', [])]
        else:
            vids = [{'id': v['id'], 'title': v['title'], 'channel': v['channel']} for v in pick_videos(pid, m)]
        plan[pid] = vids
    ids = sorted({v['id'] for vs in plan.values() for v in vs})
    print(f'{len(metas)} problems, {len(ids)} unique videos; fetching transcripts…', flush=True)
    with cf.ThreadPoolExecutor(6) as ex:
        list(ex.map(transcript, ids))
    timed = total = 0
    for f, m in metas:
        pid = m['id']
        _, _, _, keywords, ref = ENRICH[pid]
        book, apple, articles, _ = R[ref]
        videos = []
        for v in plan[pid]:
            moment = find_moment(v['id'], keywords, m['title'])
            total += 1
            entry = {'title': v['title'], 'url': with_time(f"https://www.youtube.com/watch?v={v['id']}", moment[0] if moment else 0), 'channel': v['channel']}
            if moment:
                timed += 1
                entry['start'] = moment[0]
                entry['moment'] = moment[1]
            videos.append(entry)
        docs = [d for d in m.get('docs', []) if d.get('book') or d.get('url')]
        for title, path in apple:
            url = path if path.startswith('http') else AD + path
            if all(d.get('url') != url for d in docs):
                docs.append({'title': title, 'url': url})
        arts = [{'title': f'The Swift Programming Language: {CHAPTERS[c]}', 'url': f'{BOOK}{c}/', 'source': 'swift.org'} for c in book]
        arts += [{'title': t, 'url': u, 'source': s} for t, u, s in articles]
        if dry:
            print(f"\n{pid} [{ref}]")
            for v in videos: print(f"  {v['channel']:18} {v['title'][:70]}  @{v.get('start', '-')}  {v.get('moment', '')[:70]}")
            continue
        m['videos'], m['docs'], m['articles'] = videos, docs, arts
        json.dump(m, open(f, 'w'), indent=2, ensure_ascii=False)
        open(f, 'a').write('\n')
    print(f'\nvideos: {total}, with timestamps: {timed}')


main()
