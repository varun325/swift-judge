import json, glob, sys
def apply(H):
    dirs = {json.load(open(p))['id']: p for p in glob.glob('/Users/shrishti/Desktop/varun_notes/swift-judge/problems/*/*/problem.json')}
    for pid, hints in H.items():
        assert pid in dirs, pid
        assert len(hints) == 3, pid
        p = dirs[pid]; m = json.load(open(p)); m['hints'] = list(hints)
        json.dump(m, open(p, 'w'), indent=2, ensure_ascii=False)
    print(f'applied hints to {len(H)} problems')
