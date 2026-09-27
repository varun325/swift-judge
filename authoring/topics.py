"""Generate content/TOPICS.md: every topic the three YouTube creators cover, how many videos each made,
and which judged problems (or quiz topics) teach it here.   python3 authoring/topics.py"""
import collections, glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'authoring', 'research'))
from taxonomy import T  # (id, area, label, regex)

videos = json.load(open(os.path.join(ROOT, 'authoring', 'research', 'all_videos.json')))
topic_of = {v['id']: v['topic'] for v in videos}
counts = collections.defaultdict(collections.Counter)
for v in videos:
    counts[v['topic']][v['channel']] += 1

problems = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(ROOT, 'problems', '*', '*', 'problem.json'))):
    m = json.load(open(f))
    for v in m.get('videos', []):
        vid = re.search(r'v=([\w-]{11})', v['url'])
        if vid and vid.group(1) in topic_of:
            problems[topic_of[vid.group(1)]].append((m['track'], m['id'], m['title'], m.get('impact')))
quiz = collections.Counter(q.get('topic', 'Other') for q in json.load(open(os.path.join(ROOT, 'content', 'quiz.json'))))

QUIZ_FOR = {'career': 'Senior engineering', 'eng-tooling': 'Xcode & tooling', 'fw-uikit': 'UIKit', 'eng-testing': 'Testing',
            'fw-cloud': 'Cloud & backend', 'eng-accessibility': 'Accessibility & localisation', 'fw-platform': 'App lifecycle'}
CH = ['Swiftful Thinking', 'Paul Hudson', 'Sean Allen']

out = ['# Topic catalogue', '',
       'Every topic covered by **Swiftful Thinking**, **Paul Hudson** (Hacking with Swift) and **Sean Allen** on YouTube '
       f'({len(videos)} videos classified), how many videos each made, and where Swift Judge teaches it. '
       'Problems link to the exact moment in those videos (Learn tab). Topics a compiler can\'t judge are covered in the Quiz.', '',
       'Regenerate with `python3 authoring/topics.py`.', '']
ORDER = ['Swift language', 'SwiftUI', 'Frameworks', 'Engineering practice', 'Career']
areas = sorted({t[1] for t in T}, key=lambda a: ORDER.index(a) if a in ORDER else len(ORDER))
for area in areas:
    out += ['', f'## {area}', '', '| Topic | Swiftful | Paul Hudson | Sean Allen | Judged problems | Quiz |', '|---|---:|---:|---:|---|---|']
    for tid, _, label, _ in (t for t in T if t[1] == area):
        c = counts.get(tid, {})
        ps = sorted(set(problems.get(tid, [])))
        core = sum(1 for p in ps if p[3] == 'core')
        shown = ', '.join(f'`{p[1]}`' for p in ps[:6]) + (f' +{len(ps) - 6} more' if len(ps) > 6 else '')
        judged = f'{len(ps)} ({core} core): {shown}' if ps else '—'
        qz = QUIZ_FOR.get(tid)
        out.append(f"| {label} | {c.get(CH[0], 0)} | {c.get(CH[1], 0)} | {c.get(CH[2], 0)} | {judged} | {f'{qz} ({quiz[qz]})' if qz else '—'} |")
open(os.path.join(ROOT, 'content', 'TOPICS.md'), 'w').write('\n'.join(out) + '\n')
print('topics', len(T), 'lines', len(out))
