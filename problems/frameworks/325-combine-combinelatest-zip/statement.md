Two `PassthroughSubject`s: `a` (Int) and `b` (String). Events are `a <n>` or `b <s>`. Depending on `mode`, subscribe with:
 - `combineLatest` → `"<a>-<b>"` whenever either changes (after both have emitted)
 - `zip` → pairs `"<a>-<b>"` in order, one from each
 - `merge` → map both to strings and merge: `"a<n>"` / `"b<s>"`
