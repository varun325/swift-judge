"""Append seeded random hidden tests to problem folders. Expected values are derived by the
judge from each reference solution (tests without `expected`). Idempotent: previously
generated tests (name starts with 'random ') are replaced."""
import json, os, random, string, zlib, glob

ROOT = '/Users/shrishti/Desktop/varun_notes/swift-judge/problems'
LETTERS = string.ascii_lowercase
WORDS = ['swift','code','apple','tea','eat','ate','tan','nat','bat','map','filter','reduce','closure','struct','class','enum','protocol','actor','async','await','ios','mac','a','bb','level','noon','stack','queue','heap','trie']

def R(rng, lo, hi): return rng.randint(lo, hi)
def ints(rng, n0, n1, lo, hi): return [rng.randint(lo, hi) for _ in range(rng.randint(n0, n1))]
def word(rng, n0=1, n1=8, alpha=LETTERS): return ''.join(rng.choice(alpha) for _ in range(rng.randint(n0, n1)))
def words(rng, n0, n1): return [rng.choice(WORDS) if rng.random() < .6 else word(rng) for _ in range(rng.randint(n0, n1))]
def sentence(rng, n0=0, n1=8, extra=' '): return extra.join(rng.choice(WORDS + [word(rng)]) for _ in range(rng.randint(n0, n1)))
def mixed_text(rng, n=20): return ''.join(rng.choice(LETTERS + LETTERS.upper() + '  ,.!?019é🦅') for _ in range(rng.randint(0, n)))
def dbl(rng, lo, hi, nd=2): return round(rng.uniform(lo, hi), nd)
def opt(rng, v, p=.2): return None if rng.random() < p else v

G = {}
def gen(pid, count=12):
    def deco(f): G[pid] = (f, count); return f
    return deco

# ---------------- beginner
gen('swap-values')(lambda r: {'pair': ints(r, 2, 2, -99, 99)})
gen('runtime-constant')(lambda r: {'weightKg': dbl(r, 0, 50), 'express': r.random() < .5})
gen('to-binary-string')(lambda r: {'value': R(r, -10**12, 10**12), 'radix': R(r, 2, 36)})
gen('overflow-safe-add')(lambda r: {'a': r.choice([R(r, -100, 100), R(r, 2**62, 2**63-1), R(r, -2**63, -2**62)]), 'b': r.choice([R(r, -100, 100), R(r, 2**62, 2**63-1), R(r, -2**63, -2**62)])})
gen('wrapping-hash')(lambda r: {'text': mixed_text(r, 60)})
gen('float-compare')(lambda r: (lambda a: {'a': a, 'b': r.choice([a, a + 1e-12, a * 1.001, dbl(r, -1e6, 1e6, 6)])})(dbl(r, -1e6, 1e6, 6)))
gen('digit-sum')(lambda r: {'n': R(r, -10**15, 10**15)})
gen('fahrenheit')(lambda r: {'celsius': R(r, -273, 1000)})
gen('bool-toggle-xor', 8)(lambda r: {'a': r.random() < .5, 'b': r.random() < .5, 'c': r.random() < .5})
gen('leap-year')(lambda r: {'year': r.choice([R(r, 1, 3000), R(r, 1, 30) * 100, R(r, 1, 30) * 4])})
gen('character-count')(lambda r: {'text': mixed_text(r, 15) + r.choice(['', 'é', '👨‍👩‍👧', '🇯🇵'])})
gen('reverse-words')(lambda r: {'sentence': (' ' * R(r, 0, 2)) + sentence(r, 0, 7, ' ' * R(r, 1, 3)) + (' ' * R(r, 0, 2))})
gen('palindrome')(lambda r: (lambda w: {'text': r.choice([w + w[::-1], w + 'x' + w[::-1].upper() + ',', mixed_text(r, 12)])})(word(r, 0, 6)))
gen('string-index-nth')(lambda r: (lambda t: {'text': t, 'offset': R(r, -2, len(t) + 2)})(mixed_text(r, 10)))
gen('vowel-count')(lambda r: {'text': mixed_text(r, 30)})
gen('caesar-cipher')(lambda r: {'text': mixed_text(r, 25), 'shift': R(r, -100, 100)})
gen('interpolation-receipt')(lambda r: {'item': r.choice(['Tea', 'Scone', 'Notebook', 'Pen']), 'quantity': R(r, 0, 20), 'unitCents': R(r, 0, 50000)})
gen('multiline-raw-strings', 5)(lambda r: {'user': word(r, 0, 10)})
gen('acronym')(lambda r: {'phrase': sentence(r, 0, 6, r.choice([' ', '-', ' - ', '  ']))})
gen('running-sum')(lambda r: {'nums': ints(r, 0, 25, -1000, 1000)})
gen('second-largest')(lambda r: {'nums': ints(r, 0, 12, -10, 10)})
gen('move-zeroes')(lambda r: {'nums': [x if r.random() < .6 else 0 for x in ints(r, 0, 15, -9, 9)]})
gen('rotate-array')(lambda r: {'nums': ints(r, 0, 12, -50, 50), 'k': R(r, 0, 40)})
gen('chunked')(lambda r: {'items': [word(r, 1, 3) for _ in range(R(r, 0, 14))], 'size': R(r, 1, 6)})
gen('merge-sorted')(lambda r: {'a': sorted(ints(r, 0, 10, -30, 30)), 'b': sorted(ints(r, 0, 10, -30, 30))})
gen('array-safe-subscript')(lambda r: (lambda items: {'items': items, 'indices': ints(r, 0, 8, -3, len(items) + 3)})([word(r, 1, 4) for _ in range(R(r, 0, 6))]))
def _two_sum(r):
    nums = r.sample(range(-60, 60), R(r, 2, 12))
    if r.random() < .8:
        i, j = sorted(r.sample(range(len(nums)), 2)); t = nums[i] + nums[j]
        # make the pair unique-ish: rebuild so only (i, j) sums to t
        sums = [(a, b) for a in range(len(nums)) for b in range(a + 1, len(nums)) if nums[a] + nums[b] == t]
        if len(sums) > 1: return {'nums': nums[:2], 'target': nums[0] + nums[1]}
        return {'nums': nums, 'target': t}
    return {'nums': nums, 'target': 1000}
gen('two-sum')(_two_sum)
gen('word-frequency')(lambda r: {'text': sentence(r, 0, 12, r.choice([' ', ', ', '. ', ' 42 ']))})
gen('group-anagrams')(lambda r: {'words': [r.choice(['eat','tea','ate','tan','nat','bat','tab','abc','cab','bca','z']) for _ in range(R(r, 0, 10))]})
gen('invert-dictionary')(lambda r: {'grades': {word(r, 2, 5): r.choice('ABCDF') for _ in range(R(r, 0, 8))}})
gen('first-unique-char')(lambda r: {'s': word(r, 0, 12, 'abcde')})
gen('dictionary-default-lookup', 6)(lambda r: {'codes': [r.choice([200, 201, 301, 404, 500, R(r, 100, 599)]) for _ in range(R(r, 0, 8))]})
gen('contains-duplicate')(lambda r: {'nums': ints(r, 0, 12, 0, 20)})
gen('set-algebra')(lambda r: {'a': [r.choice(WORDS[:12]) for _ in range(R(r, 0, 6))], 'b': [r.choice(WORDS[:12]) for _ in range(R(r, 0, 6))]})
gen('longest-consecutive')(lambda r: {'nums': ints(r, 0, 20, -15, 15)})
gen('hashable-point-set')(lambda r: {'coords': [[R(r, -2, 2), R(r, -2, 2)] for _ in range(R(r, 0, 12))]})
gen('min-max-tuple')(lambda r: {'nums': ints(r, 0, 10, -1000, 1000)})
gen('tuple-compare-sort')(lambda r: {'entries': [[word(r, 2, 4), str(R(r, 0, 5)), str(R(r, 0, 3))] for _ in range(R(r, 0, 8))]})
gen('stride-countdown')(lambda r: {'start': R(r, -5, 60), 'step': R(r, 1, 9)})
gen('range-clamp')(lambda r: (lambda lo: {'values': ints(r, 0, 10, -50, 50), 'low': lo, 'high': lo + R(r, 0, 40)})(R(r, -30, 10)))
gen('fix-temperature-range')(lambda r: {'temp': R(r, -20, 60)})
gen('fix-can-vote', 8)(lambda r: {'age': R(r, 0, 40)})
gen('grade-letter')(lambda r: {'score': R(r, -10, 110)})
gen('if-expression')(lambda r: {'weightKg': dbl(r, 35, 150, 1), 'heightM': dbl(r, 1.4, 2.1)})
gen('switch-multiple-patterns')(lambda r: {'text': mixed_text(r, 12)})
gen('fallthrough-description', 8)(lambda r: {'n': R(r, -5, 25)})
gen('fix-infinite-while')(lambda r: {'files': [word(r, 1, 4) + r.choice(['.jpeg', '.txt', '.png', '.jpeg', '.md']) for _ in range(R(r, 0, 7))]})
gen('labeled-break')(lambda r: {'grid': [ints(r, 0, 5, 0, 9) for _ in range(R(r, 0, 5))], 'target': R(r, 0, 9)})
gen('repeat-while-collatz')(lambda r: {'n': R(r, 1, 100000)})
gen('argument-labels')(lambda r: {'start': R(r, -20, 20), 'end': R(r, -20, 60), 'step': R(r, 1, 7)})
gen('default-parameters', 6)(lambda r: {'names': [word(r, 2, 6).title() for _ in range(R(r, 0, 5))]})
gen('variadic-average')(lambda r: {'groups': [[dbl(r, -100, 100) for _ in range(R(r, 0, 5))] for _ in range(R(r, 0, 4))]})
gen('overloading-describe', 6)(lambda r: {'ints': ints(r, 0, 3, -9, 9), 'words': [word(r, 0, 5) for _ in range(R(r, 0, 3))], 'flags': [r.random() < .5 for _ in range(R(r, 0, 3))]})
gen('nested-functions')(lambda r: {'backward': r.random() < .5, 'start': R(r, -20, 20), 'steps': R(r, 0, 8)})
gen('implicit-return-sign', 6)(lambda r: {'nums': ints(r, 0, 8, -5, 5)})
gen('enum-raw-values', 6)(lambda r: {'positions': ints(r, 0, 6, -1, 10)})
gen('enum-case-iterable', 6)(lambda r: {'maxPrice': R(r, 0, 7)})
gen('enum-associated-shapes')(lambda r: {'specs': [r.choice([f'circle {R(r,0,5)}', f'rectangle {R(r,0,9)} {dbl(r,0,5,1)}', f'triangle {R(r,1,8)} {R(r,1,8)}', 'hexagon 1', 'circle']) for _ in range(R(r, 0, 5))]})
gen('enum-mutating-toggle', 6)(lambda r: {'steps': R(r, 0, 12)})
# ---------------- intermediate
gen('parse-sum-optionals')(lambda r: {'tokens': [r.choice([str(R(r, -999, 999)), word(r, 1, 3), f'{R(r,0,9)}.5', f'+{R(r,0,9)}', f' {R(r,0,9)}']) for _ in range(R(r, 0, 10))]})
gen('if-let-chain')(lambda r: {'width': opt(r, r.choice([str(R(r, -3, 50)), 'x', ''])), 'height': opt(r, r.choice([str(R(r, -3, 50)), 'y']))})
gen('guard-let-validate', 16)(lambda r: {'username': opt(r, word(r, 1, 18)), 'age': opt(r, r.choice([str(R(r, 5, 80)), 'abc'])), 'email': opt(r, r.choice([word(r)+'@'+word(r), '@'+word(r), word(r)+'@', word(r), 'a@b@c']))})
gen('nil-coalescing-config')(lambda r: {'env': {'PORT': r.choice([str(R(r, 1, 9999)), 'x'])} if r.random() < .6 else {}, 'args': {'port': r.choice([str(R(r, 1, 9999)), 'bad'])} if r.random() < .5 else {}})
gen('optional-chaining-company')(lambda r: {'records': [[word(r, 3, 6), r.choice(['-', word(r, 2, 5)]), r.choice(['-', word(r, 3, 9)])] for _ in range(R(r, 0, 6))]})
gen('optional-map-flatmap')(lambda r: {'csv': opt(r, ','.join(r.choice([str(R(r, -99, 99)), word(r, 1, 3), '']) for _ in range(R(r, 1, 4))))})
gen('check-password-throws')(lambda r: {'password': r.choice(['12345', 'password', word(r, 0, 15, LETTERS + '0123456789')])})
gen('do-catch-patterns', 8)(lambda r: {'requests': [r.choice(['chips', 'candy', 'soda', 'caviar', 'shake', 'gum', word(r)]) for _ in range(R(r, 0, 7))]})
gen('try-optional')(lambda r: {'pairs': [[R(r, -100, 100), R(r, -3, 3)] for _ in range(R(r, 0, 8))]})
gen('defer-order')(lambda r: {'steps': [r.choice([word(r, 1, 3)] * 4 + ['fail']) for _ in range(R(r, 0, 6))]})
gen('result-type')(lambda r: {'raw': [r.choice([str(R(r, -20, 200)), word(r, 1, 3)]) for _ in range(R(r, 0, 8))]})
gen('typed-throws')(lambda r: {'balance': R(r, 0, 200), 'amounts': ints(r, 0, 8, -10, 120)})
gen('rethrows-map', 8)(lambda r: {'words': [word(r, 1, 5, LETTERS + '0') for _ in range(R(r, 0, 5))]})
gen('closure-shortening')(lambda r: {'team': [r.choice(['T', 't', 'A', 'M']) + word(r, 1, 7) for _ in range(R(r, 0, 8))]})
gen('make-counter')(lambda r: {'calls': [r.choice('ab') for _ in range(R(r, 0, 12))]})
gen('capture-list-snapshot', 6)(lambda r: {'start': R(r, -1000, 1000)})
gen('escaping-handlers', 6)(lambda r: {'events': [word(r, 2, 6) for _ in range(R(r, 0, 5))]})
gen('autoclosure-log', 4)(lambda r: {'level': R(r, -1, 5)})
gen('sort-by-keypath')(lambda r: {'rows': [[word(r, 2, 5), str(R(r, 18, 70)), r.choice(['Rome', 'Oslo', 'Lima', 'Pune', 'Kyiv'])] for _ in range(R(r, 0, 7))], 'key': r.choice(['name', 'age', 'city'])})
gen('compose-functions', 6)(lambda r: {'values': ints(r, 0, 8, -1000, 1000)})
gen('curried-add', 8)(lambda r: {'base': R(r, -100, 100), 'xs': ints(r, 0, 8, -100, 100)})
gen('reduce-into')(lambda r: {'words': [word(r, 1, 5) for _ in range(R(r, 0, 10))]})
gen('fix-vacation-setter')(lambda r: {'taken': R(r, 0, 30), 'remaining': R(r, 0, 30)})
gen('property-observers-clamp')(lambda r: {'changes': ints(r, 0, 8, -50, 200)})
gen('mutating-bank-account')(lambda r: {'ops': [f"{r.choice('dw')} {R(r, 0, 100)}" for _ in range(R(r, 0, 10))]})
gen('custom-init-keeps-memberwise', 8)(lambda r: {'names': [word(r, 1, 8).title() for _ in range(R(r, 0, 5))]})
gen('static-counter', 6)(lambda r: {'names': [word(r, 2, 5) for _ in range(R(r, 0, 6))]})
gen('dynamic-dispatch-employees', 8)(lambda r: {'roles': [r.choice(['dev', 'mgr', 'x']) for _ in range(R(r, 0, 5))], 'hours': R(r, 1, 12)})
gen('convenience-init')(lambda r: {'specs': [r.choice([f'white {R(r,0,255)}', '#' + ''.join(r.choice('0123456789ABCDEFabcdef') for _ in range(6)), '#' + word(r, 6, 6), 'white', '#12345']) for _ in range(R(r, 0, 5))]})
gen('deinit-lifecycle', 6)(lambda r: {'names': [word(r, 1, 3) for _ in range(R(r, 0, 5))]})
gen('class-let-reference', 6)(lambda r: {'renames': [word(r, 2, 6).title() for _ in range(R(r, 0, 4))]})
gen('static-vs-class-method', 5)(lambda r: {'kinds': [r.choice(['shape', 'circle']) for _ in range(R(r, 0, 5))]})
gen('required-init-factory', 6)(lambda r: {'kinds': [f"{r.choice(['goblin', 'dragon', 'enemy'])} {R(r, 1, 50)}" for _ in range(R(r, 0, 5))]})
gen('type-casting-zoo')(lambda r: {'items': [r.choice([str(R(r, -99, 99)), str(dbl(r, -9, 9)), 'true', 'false', word(r)]) for _ in range(R(r, 0, 7))]})
gen('protocol-shapes', 8)(lambda r: {'specs': [r.choice([[dbl(r, 0.1, 9)], [dbl(r, 0.1, 9), dbl(r, 0.1, 9)], [-dbl(r, 0.1, 9)]]) for _ in range(R(r, 0, 5))]})
gen('protocol-extension-default', 5)(lambda r: {'kinds': [r.choice(['en', 'pirate']) for _ in range(R(r, 0, 4))]})
gen('comparable-version')(lambda r: {'versions': [r.choice(['.'.join(str(R(r, 0, 12)) for _ in range(R(r, 1, 3))), 'x.1', '1..2', '1.2.3.4']) for _ in range(R(r, 0, 8))]})
gen('protocol-composition-delegate', 6)(lambda r: {'files': [word(r, 1, 4) for _ in range(R(r, 0, 4))], 'keepDelegate': r.random() < .5})
gen('extension-int-helpers')(lambda r: {'nums': ints(r, 0, 5, -20, 120)})
gen('extension-protocol-conformance', 6)(lambda r: {'ints': ints(r, 0, 4, -9, 99), 'words': [word(r, 0, 5) for _ in range(R(r, 0, 3))], 'flags': [r.random() < .5 for _ in range(R(r, 0, 3))]})
gen('abstract-class-emulation', 6)(lambda r: {'sizes': [ints(r, 0, 4, 0, 500), ints(r, 0, 4, 0, 20)]})
gen('nested-types-cards')(lambda r: {'draws': ints(r, 0, 6, 0, 200)})
gen('custom-string-convertible', 8)(lambda r: {'cents': ints(r, 0, 5, -100000, 100000)})
gen('for-case-optional')(lambda r: {'values': [opt(r, R(r, -20, 30), .3) for _ in range(R(r, 0, 10))]})
gen('builder-pattern-copy', 8)(lambda r: {'steps': [r.choice(['method POST', 'method PUT', 'path /' + word(r, 1, 5), f'header {word(r,1,3)} {word(r,1,3)}', 'junk']) for _ in range(R(r, 0, 6))]})
gen('tuple-swap-fibonacci')(lambda r: {'n': R(r, 0, 90), 'a': R(r, 0, 10**6), 'b': R(r, 0, 10**6)})
gen('dictionary-unique-keys')(lambda r: {'rows': [[str(R(r, 1, 4)), r.choice(['ann', 'anna', 'bo', 'cy'])] for _ in range(R(r, 0, 8))]})
gen('zip-enumerated')(lambda r: {'names': [word(r, 2, 5) for _ in range(R(r, 0, 6))], 'times': [dbl(r, 9, 15) for _ in range(R(r, 0, 6))]})
gen('protocol-default-args', 5)(lambda r: {'channels': [r.choice(['email', 'sms']) for _ in range(R(r, 0, 4))], 'message': word(r, 1, 8)})
def _ops_minstack(r):
    ops, args, size = [], [], 0
    for _ in range(R(r, 1, 20)):
        op = r.choice(['push', 'push', 'pop', 'top', 'min'])
        ops.append(op); args.append([R(r, -50, 50)] if op == 'push' else [])
    return {'ops': ops, 'args': args}
gen('design-min-stack')(_ops_minstack)
def _ops_parking(r):
    ops, args = ['init'], [[R(r, 0, 3), R(r, 0, 3), R(r, 0, 3)]]
    for _ in range(R(r, 0, 10)): ops.append('park'); args.append([R(r, 1, 3)])
    return {'ops': ops, 'args': args}
gen('design-parking-lot')(_ops_parking)
gen('queue-two-stacks')(lambda r: {'ops': [r.choice([f'enqueue {R(r,-9,99)}'] * 2 + ['dequeue', 'peek', 'count']) for _ in range(R(r, 1, 18))]})
# ---------------- advanced
gen('generic-swap-and-stack', 6)(lambda r: {'ints': ints(r, 0, 6, -9, 9), 'words': [word(r, 1, 4) for _ in range(R(r, 0, 4))]})
gen('generic-constraints-max')(lambda r: {'ints': ints(r, 0, 12, 0, 5), 'words': [r.choice('abcd') for _ in range(R(r, 0, 8))]})
gen('where-clause-extension', 8)(lambda r: {'ints': ints(r, 0, 8, -100, 100), 'doubles': [dbl(r, -10, 10) for _ in range(R(r, 0, 6))]})
gen('associated-type-container', 8)(lambda r: (lambda w: {'ints': ints(r, 0, 6, 0, 9), 'words': r.choice([w, w + w[::-1], ['x']])})([r.choice('abc') for _ in range(R(r, 0, 3))]))
gen('opaque-some-return', 6)(lambda r: {'sizes': ints(r, 0, 4, 1, 7)})
gen('type-erasure-any-shape', 6)(lambda r: {'inputs': [word(r, 0, 7) for _ in range(R(r, 0, 4))]})
gen('phantom-types-ids', 8)(lambda r: {'meters': [dbl(r, 0, 100) for _ in range(R(r, 0, 5))], 'feet': [dbl(r, 0, 300) for _ in range(R(r, 0, 5))]})
gen('conditional-conformance-pair')(lambda r: {'a': ints(r, 0, 8, 0, 3), 'b': ints(r, 0, 8, 0, 3)})
gen('dynamic-member-lookup', 8)(lambda r: (lambda keys: {'json': {k: word(r, 1, 5) for k in keys}, 'paths': [r.choice(keys + ['nope', 'a.b']) for _ in range(R(r, 0, 5))] if keys else []})(list({'.'.join(word(r, 1, 3) for _ in range(R(r, 1, 3))) for _ in range(R(r, 0, 4))})))
gen('keypath-writable', 8)(lambda r: {'updates': [r.choice([f'name={word(r)}', f'age={R(r,0,99)}', 'age=x', f'city={word(r)}', 'zip=9']) for _ in range(R(r, 0, 6))]})
def _matrix(r):
    rows, cols = R(r, 0, 4), R(r, 0, 4)
    sets = [[R(r, 0, rows - 1), R(r, 0, cols - 1), R(r, -9, 9)] for _ in range(R(r, 0, 6))] if rows and cols else []
    return {'rows': rows, 'cols': cols, 'sets': sets}
gen('custom-subscript-matrix')(_matrix)
gen('custom-operator-vector', 8)(lambda r: {'a': [R(r, -9, 9), R(r, -9, 9)], 'b': [R(r, -9, 9), R(r, -9, 9)]})
gen('pattern-match-operator', 8)(lambda r: {'words': [r.choice(['un', 're', '', 'pre']) + word(r, 0, 9) for _ in range(R(r, 0, 6))]})
gen('custom-sequence-fibonacci', 8)(lambda r: {'limit': R(r, 0, 10**9), 'take': R(r, 0, 40)})
gen('custom-collection-ring')(lambda r: {'capacity': R(r, 0, 6), 'values': ints(r, 0, 12, -20, 20)})
gen('copy-on-write', 8)(lambda r: {'values': ints(r, 0, 6, -9, 9), 'extra': R(r, -9, 9)})
def _rpn(r):
    def build(d):
        if d == 0 or r.random() < .3: return [str(R(r, -9, 9))]
        k = r.random()
        if k < .2: return build(d - 1) + ['neg']
        return build(d - 1) + build(d - 1) + [r.choice(['+', '*'])]
    toks = build(R(r, 0, 4))
    if r.random() < .2: toks = toks + [r.choice(['+', '5', 'x'])]
    return {'tokens': toks}
gen('indirect-enum-expression')(_rpn)
gen('indirect-linked-list', 8)(lambda r: {'values': ints(r, 0, 10, -50, 50)})
gen('equatable-hashable-custom')(lambda r: {'raw': [r.choice(['a.b', 'ab', 'A.B+x', 'ab+y', 'c']) + '@' + r.choice(['mail.com', 'MAIL.com', 'x.io']) for _ in range(R(r, 0, 8))]})
gen('retain-cycle-parent-child', 6)(lambda r: {'childNames': [word(r, 1, 3) for _ in range(R(r, 0, 4))]})
gen('closure-retain-cycle', 5)(lambda r: {'ticks': R(r, 0, 8)})
gen('unowned-customer-card', 6)(lambda r: (lambda n: {'customers': [word(r, 2, 4) for _ in range(n)], 'withCard': [r.random() < .6 for _ in range(n)]})(R(r, 0, 4)))
gen('noncopyable-file-handle', 6)(lambda r: {'writes': [word(r, 1, 4) for _ in range(R(r, 0, 4))], 'closeEarly': r.random() < .5})
gen('async-await-basics', 6)(lambda r: {'ids': ints(r, 0, 40, 0, 999)})
gen('actor-bank', 8)(lambda r: {'amounts': ints(r, 0, 200, -100, 100)})
gen('task-cancellation', 8)(lambda r: {'haystacks': [ints(r, 0, 30, 0, 20) for _ in range(R(r, 0, 6))], 'target': R(r, 0, 20)})
gen('async-sequence', 8)(lambda r: {'values': ints(r, 0, 15, -20, 20), 'limit': R(r, 0, 6)})
gen('main-actor-isolation', 5)(lambda r: {'names': [word(r, 1, 5) for _ in range(R(r, 0, 5))]})
gen('property-wrapper-clamped', 8)(lambda r: {'volumes': ints(r, 0, 6, -50, 200), 'names': [' ' * R(r, 0, 2) + word(r, 1, 6).title() + ' ' * R(r, 0, 2) for _ in range(R(r, 0, 3))]})
gen('result-builder-html', 8)(lambda r: {'title': word(r, 0, 8), 'items': [word(r, 1, 4) for _ in range(R(r, 0, 4))], 'showFooter': r.random() < .5})
def _users_json(r):
    users = []
    for _ in range(R(r, 0, 4)):
        u = {'user_id': R(r, 1, 999), 'first_name': word(r, 2, 6).title(), 'is_admin': r.random() < .3}
        if r.random() < .5: u['e-mail'] = word(r) + '@x.io'
        users.append(u)
    s = json.dumps(users)
    return {'json': s if r.random() < .85 else s[:-1]}
gen('codable-snake-case', 8)(_users_json)
def _products_json(r):
    ps = []
    for _ in range(R(r, 0, 3)):
        p = {'info': {'name': word(r, 2, 6).title()}, 'price': r.choice([dbl(r, 0, 99), str(dbl(r, 0, 99)), 'abc'])}
        if r.random() < .5: p['tags'] = [word(r, 1, 3) for _ in range(R(r, 0, 3))]
        if r.random() < .1: del p['info']
        ps.append(p)
    return {'json': json.dumps(ps)}
gen('codable-custom-init', 8)(_products_json)
gen('codable-round-trip', 8)(lambda r: {'events': [r.choice([f'login {word(r)}', f'purchase {word(r)} {R(r,1,9999)}', 'logout', 'junk']) for _ in range(R(r, 0, 4))]})
gen('regex-extract')(lambda r: {'text': ' '.join(r.choice([f'{R(r,1990,2030)}-{R(r,0,14):02d}-{R(r,0,33):02d}', word(r), f'{R(r,1,99)}']) for _ in range(R(r, 0, 6)))})
gen('regex-builder-log', 8)(lambda r: {'lines': [r.choice([f"[{r.choice(['INFO','WARN','ERROR','DEBUG'])}] 20{R(r,10,30)}-0{R(r,1,9)}-1{R(r,0,9)} {sentence(r,1,3)} (code {R(r,0,500)})", sentence(r, 1, 4)]) for _ in range(R(r, 0, 4))]})
gen('sha256-hash', 6)(lambda r: {'inputs': [mixed_text(r, 20) for _ in range(R(r, 0, 3))]})
gen('uuid-and-identifiable', 6)(lambda r: {'strings': [r.choice(['%08x-%04x-%04x-%04x-%012x' % (r.getrandbits(32), r.getrandbits(16), r.getrandbits(16), r.getrandbits(16), r.getrandbits(48)), word(r, 5, 36)]) for _ in range(R(r, 0, 3))]})
gen('file-manager-listing', 6)(lambda r: {'files': sorted({r.choice(['', f'd{R(r,0,2)}/']) + f'f{R(r,0,9)}.txt' for _ in range(R(r, 0, 6))})})
gen('assert-precondition', 8)(lambda r: {'ages': ints(r, 0, 8, -10, 90)})
def _ops_lru(r):
    ops, args = ['init'], [[R(r, 1, 4)]]
    for _ in range(R(r, 1, 25)):
        if r.random() < .5: ops.append('put'); args.append([R(r, 1, 6), R(r, 0, 99)])
        else: ops.append('get'); args.append([R(r, 1, 6)])
    return {'ops': ops, 'args': args}
gen('lru-cache', 16)(_ops_lru)
gen('memoization', 8)(lambda r: {'n': R(r, 0, 90)})
gen('dependency-injection', 6)(lambda r: {'hours': ints(r, 0, 6, 0, 23), 'useLive': False})
gen('valid-parentheses', 16)(lambda r: {'s': ''.join(r.choice('()[]{}') for _ in range(R(r, 0, 12)))})
gen('generic-binary-search')(lambda r: (lambda nums, ws: {'nums': nums, 'words': ws, 'target': r.choice(nums + [R(r, -5, 60)]) if nums else 1, 'word': r.choice(ws + ['zz']) if ws else 'x'})(sorted(set(ints(r, 0, 15, -5, 60))), sorted(set(word(r, 1, 3) for _ in range(R(r, 0, 6))))))
gen('merge-intervals')(lambda r: {'intervals': [(lambda s: [s, s + R(r, 0, 6)])(R(r, 0, 30)) for _ in range(R(r, 0, 8))]})
gen('top-k-frequent')(lambda r: (lambda ws: {'words': ws, 'k': R(r, 1, max(1, len(set(ws))))})([r.choice(WORDS[:8]) for _ in range(R(r, 1, 15))]))
gen('number-of-islands')(lambda r: (lambda h, w: {'grid': [''.join(r.choice('01') for _ in range(w)) for _ in range(h)]})(R(r, 0, 7), R(r, 1, 7)))
def _ops_trie(r):
    pool = ['app', 'apple', 'apply', 'ape', 'bat', 'bath', 'b', 'cat', '']
    ops = [r.choice(['insert', 'insert', 'search', 'startsWith']) for _ in range(R(r, 1, 14))]
    return {'ops': ops, 'words': [r.choice(pool) for _ in ops]}
gen('design-trie')(_ops_trie)
gen('longest-unique-substring', 16)(lambda r: {'s': word(r, 0, 20, 'abcdef')})
gen('product-except-self')(lambda r: {'nums': ints(r, 0, 10, -5, 5)})
gen('max-subarray', 16)(lambda r: {'nums': ints(r, 1, 20, -30, 30)})
gen('coin-change')(lambda r: {'coins': sorted(set(ints(r, 1, 4, 1, 30))), 'amount': R(r, 0, 300)})
gen('permutations', 6)(lambda r: {'nums': r.sample(range(-9, 10), R(r, 0, 5))})
gen('heap-kth-largest')(lambda r: (lambda nums: {'nums': nums, 'k': R(r, 1, len(nums))})(ints(r, 1, 25, -100, 100)))
def _graph(r):
    n = R(r, 1, 7)
    edges = [[R(r, 0, n - 1), R(r, 0, n - 1), R(r, 0, 20)] for _ in range(R(r, 0, 14))]
    return {'n': n, 'edges': edges, 'source': R(r, 0, n - 1)}
gen('dijkstra')(_graph)
gen('course-schedule')(lambda r: (lambda n: {'numCourses': n, 'prerequisites': [[R(r, 0, n - 1), R(r, 0, n - 1)] for _ in range(R(r, 0, n + 2))]})(R(r, 1, 7)))
def _tree(r):
    vals = [R(r, -20, 50)]
    for _ in range(R(r, 0, 12)): vals.append(opt(r, R(r, -20, 50), .3))
    # a null parent can't have children: ensure level order is valid by construction via judge's builder tolerance
    return {'levelOrder': vals if r.random() < .9 else []}
gen('binary-tree-level-order')(_tree)
gen('roman-numerals', 16)(lambda r: {'num': R(r, 1, 3999)})
gen('rotate-matrix')(lambda r: (lambda n: {'matrix': [ints(r, n, n, -9, 9) for _ in range(n)]})(R(r, 0, 5)))
gen('lcs')(lambda r: {'a': word(r, 0, 12, 'abcd'), 'b': word(r, 0, 12, 'abcd')})

# ---------------- stdio: random stdin
def _stdio(pid, f, count=6): G[pid] = (f, count)
_stdio('echo-stdin-upper', lambda r: ''.join(mixed_text(r, 15) + '\n' for _ in range(R(r, 0, 4))))
_stdio('fizzbuzz-stdio', lambda r: f'{R(r, -3, 60)}\n')
_stdio('multiplication-table-stdio', lambda r: f'{R(r, -12, 12)} {R(r, -2, 12)}\n')
_stdio('pyramid-stdio', lambda r: f'{R(r, 0, 9)}\n')
_stdio('wc-stdio', lambda r: ''.join(sentence(r, 0, 6, r.choice([' ', '  ', '\t'])) + '\n' for _ in range(R(r, 0, 5))))
_stdio('csv-column-sums-stdio', lambda r: (lambda cols: ','.join(cols) + '\n' + ''.join(','.join(r.choice([str(R(r, -9, 99)), str(dbl(r, 0, 9, 1)), '', 'x']) for _ in cols) + '\n' for _ in range(R(r, 0, 5))))([word(r, 1, 4) for _ in range(R(r, 1, 4))]))
_stdio('sort-names-stdio', lambda r: ''.join(f'{word(r,2,6).title()} {r.choice([word(r,2,7).title(), word(r,2,7)])}\n' for _ in range(R(r, 0, 6))))
_stdio('matrix-transpose-stdio', lambda r: (lambda w: ''.join(' '.join(str(R(r, -9, 99)) for _ in range(w)) + '\n' for _ in range(R(r, 0, 4))))(R(r, 1, 4)))
_stdio('gradebook-stdio', lambda r: ''.join(f"{r.choice(['ana','bo','cy','di'])} {R(r, -10, 110)}\n" if r.random() < .9 else 'junk\n' for _ in range(R(r, 0, 10))))
_stdio('stdio-bank-ledger', lambda r: ''.join(r.choice([f'deposit {R(r,-5,100)}', f'withdraw {R(r,0,150)}', 'refund 3', 'deposit x']) + '\n' for _ in range(R(r, 0, 8))))

# --------------- apply
dirs = {json.load(open(p))['id']: os.path.dirname(p) for p in glob.glob(f'{ROOT}/*/*/problem.json')}
added = 0
for pid, (f, count) in G.items():
    d = dirs.get(pid)
    assert d, f'unknown problem {pid}'
    tp = os.path.join(d, 'tests.json')
    tests = [t for t in json.load(open(tp)) if not str(t.get('name', '')).startswith('random ')]
    r = random.Random(zlib.crc32(pid.encode()))
    seen = {json.dumps(t.get('input'), sort_keys=True) for t in tests}
    k = 0; tries = 0
    while k < count and tries < count * 20:
        tries += 1
        inp = f(r)
        key = json.dumps(inp, sort_keys=True)
        if key in seen: continue
        seen.add(key)
        k += 1
        tests.append({'name': f'random {k}', 'input': inp, 'hidden': True})
    added += k
    json.dump(tests, open(tp, 'w'), indent=1, ensure_ascii=False)
print(f'augmented {len(G)} problems with {added} random tests')
