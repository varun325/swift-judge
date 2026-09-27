import json, glob
extra = {
 'predict-struct-vs-class': ['immutability'], 'builder-pattern-copy': ['immutability'],
 'overflow-safe-add': ['swift-advantages'], 'string-index-nth': ['swift-advantages'],
 'predict-optional-printing': ['nil-vs-null'], 'for-case-optional': ['nil-vs-null'],
 'curried-add': ['functions-vs-methods'], 'static-vs-class-method': ['functions-vs-methods', 'open-vs-public'],
 'nested-functions': ['functions-vs-closures'], 'make-counter': ['functions-vs-closures'],
 'closure-retain-cycle': ['self-usage', 'memory-leaks'], 'predict-self-vs-Self': ['self-usage'],
 'protocol-shapes': ['protocol-vs-class'], 'abstract-class-emulation': ['protocol-vs-class', 'multiple-inheritance'],
 'extension-protocol-conformance': ['extension-vs-protocol-extension', 'multiple-inheritance'], 'protocol-extension-default': ['extension-vs-protocol-extension'],
 'deinit-lifecycle': ['arc-vs-gc'], 'predict-deinit-order': ['arc-vs-gc'],
 'retain-cycle-parent-child': ['memory-leaks'], 'diag-private-access': ['open-vs-public'],
 'actor-bank': ['dispatch-sync-async'],
}
for p in glob.glob('/Users/shrishti/Desktop/varun_notes/swift-judge/problems/*/*/problem.json'):
    m = json.load(open(p))
    add = [c for c in extra.get(m['id'], []) if c not in m['concepts']]
    if add:
        m['concepts'] += add
        json.dump(m, open(p, 'w'), indent=2, ensure_ascii=False)
print('tagged')
