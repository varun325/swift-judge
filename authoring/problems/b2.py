import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
CT='LanguageGuide/CollectionTypes'; CF='LanguageGuide/ControlFlow'; BO='LanguageGuide/BasicOperators'; FN='LanguageGuide/Functions'
P=[]
def f(input_list, keys):  # helper: list of tuples -> dict inputs
    return [dict(zip(keys, x)) for x in input_list]
# ---------- Arrays (notes §6)
P.append(dict(id='running-sum', title='Running Sum', topic='Arrays', notes='6', concepts=['array-basics','map-filter-reduce'], docs=[('Collection Types — Arrays', CT)],
 sig='func runningSum(_ nums: [Int]) -> [Int]',
 statement="""Return an array where element `i` is the sum of `nums[0...i]`.

 ```swift
 runningSum([1, 2, 3, 4])  // [1, 3, 6, 10]
 ```""",
 solution="""
 func runningSum(_ nums: [Int]) -> [Int] {
     var result: [Int] = []
     result.reserveCapacity(nums.count)
     var total = 0
     for n in nums {
         total += n
         result.append(total)
     }
     return result
 }
 """,
 explain="""`reserveCapacity` avoids repeated reallocations when you know the final size. A functional one-liner exists — `nums.reduce(into: []) { $0.append(($0.last ?? 0) + $1) }` — but the loop is clearer and just as fast.""",
 tests=[({'nums':[1,2,3,4]},[1,3,6,10]), {'nums':[]}, {'nums':[5]}, {'nums':[3,-3,3,-3]}, {'nums':list(range(1,21))}]))
P.append(dict(id='second-largest', title='Second Largest Distinct', topic='Arrays', notes='6', concepts=['array-basics','optionals'], docs=[('Collection Types — Arrays', CT)],
 sig='func secondLargest(_ nums: [Int]) -> Int?',
 statement="""Return the second-largest **distinct** value, or `nil` if there isn't one.

 ```swift
 secondLargest([4, 1, 4, 3])  // 3
 secondLargest([7, 7])        // nil
 ```""",
 solution="""
 func secondLargest(_ nums: [Int]) -> Int? {
     var first: Int?
     var second: Int?
     for n in nums {
         if first == nil || n > first! {
             second = first
             first = n
         } else if n != first, second == nil || n > second! {
             second = n
         }
     }
     return second
 }
 """,
 explain="""A single pass with two optional slots is O(n). The short version, `Array(Set(nums)).sorted(by: >).dropFirst().first`, is O(n log n) — fine for small inputs, and very readable. Optional comparison with `==`/`!=` works directly.""",
 tests=[({'nums':[4,1,4,3]},3), ({'nums':[7,7]},None), {'nums':[]}, {'nums':[1,2]}, {'nums':[-5,-1,-3]}, {'nums':[10,9,10,8,9]}]))
P.append(dict(id='move-zeroes', title='Move Zeroes In Place', topic='Arrays', notes='6', diff='easy', concepts=['inout','array-basics'], docs=[('Collection Types — Modifying an Array', CT)],
 sig='func moveZeroes(_ nums: inout [Int])',
 statement="""Move all `0`s to the end **in place**, keeping the relative order of the other elements.

 ```swift
 var a = [0, 1, 0, 3, 12]
 moveZeroes(&a)   // a == [1, 3, 12, 0, 0]
 ```""",
 solution="""
 func moveZeroes(_ nums: inout [Int]) {
     var write = 0
     for read in nums.indices where nums[read] != 0 {
         nums.swapAt(write, read)
         write += 1
     }
 }
 """,
 explain="""Two indices: `read` scans, `write` marks where the next non-zero goes. `for … in indices where …` filters inline. `swapAt` is safe even when both indices are the same.""",
 tests=[({'nums':[0,1,0,3,12]},[1,3,12,0,0]), {'nums':[0]}, {'nums':[1,2,3]}, {'nums':[0,0,1]}, {'nums':[]}, {'nums':[4,0,5,0,0,6]}]))
P.append(dict(id='rotate-array', title='Rotate Right by k', topic='Arrays', notes='6', diff='medium', concepts=['array-basics','half-open-range'], docs=[('Collection Types — Arrays', CT)],
 sig='func rotate(_ nums: [Int], by k: Int) -> [Int]',
 statement="""Rotate the array to the right by `k` steps (`k` may exceed the count).

 ```swift
 rotate([1,2,3,4,5,6,7], by: 3)  // [5,6,7,1,2,3,4]
 ```""",
 solution="""
 func rotate(_ nums: [Int], by k: Int) -> [Int] {
     guard !nums.isEmpty else { return [] }
     let shift = k % nums.count
     return Array(nums[(nums.count - shift)...] + nums[..<(nums.count - shift)])
 }
 """,
 explain="""One-sided ranges slice from an index to the end (`nums[i...]`) or from the start (`nums[..<i]`). Slices are `ArraySlice`s — views sharing storage — and `+` concatenates them. Guard against `% 0`, which traps.""",
 tests=[({'nums':[1,2,3,4,5,6,7],'k':3},[5,6,7,1,2,3,4]), {'nums':[],'k':3}, {'nums':[1,2],'k':0}, {'nums':[1,2],'k':5}, {'nums':[-1,-100,3,99],'k':2}]))
P.append(dict(id='chunked', title='Split into Chunks', topic='Arrays', notes='6', diff='easy', concepts=['array-basics','stride'], docs=[('Control Flow — stride', CF)],
 sig='func chunked(_ items: [String], size: Int) -> [[String]]',
 statement="""Split `items` into consecutive chunks of `size` (the last may be shorter). `size` is at least 1.

 ```swift
 chunked(["a","b","c","d","e"], size: 2)  // [["a","b"],["c","d"],["e"]]
 ```""",
 solution="""
 func chunked(_ items: [String], size: Int) -> [[String]] {
     stride(from: 0, to: items.count, by: size).map {
         Array(items[$0 ..< min($0 + size, items.count)])
     }
 }
 """,
 explain="""`stride(from:to:by:)` produces the start index of each chunk and `map` turns each into a slice. `min` keeps the last range in bounds — slicing past `endIndex` traps.""",
 tests=[({'items':['a','b','c','d','e'],'size':2},[['a','b'],['c','d'],['e']]), {'items':[],'size':3}, {'items':['x'],'size':5}, {'items':['1','2','3','4','5','6'],'size':3}, {'items':['a','b','c'],'size':1}]))
P.append(dict(id='merge-sorted', title='Merge Two Sorted Arrays', topic='Arrays', notes='6', diff='easy', concepts=['array-basics','control-flow'], docs=[('Control Flow — While Loops', CF)],
 sig='func merge(_ a: [Int], _ b: [Int]) -> [Int]',
 statement="""Merge two ascending arrays into one ascending array in O(n + m) — don't just concatenate and sort.""",
 solution="""
 func merge(_ a: [Int], _ b: [Int]) -> [Int] {
     var result: [Int] = []
     result.reserveCapacity(a.count + b.count)
     var i = 0, j = 0
     while i < a.count && j < b.count {
         if a[i] <= b[j] { result.append(a[i]); i += 1 }
         else { result.append(b[j]); j += 1 }
     }
     result += a[i...]
     result += b[j...]
     return result
 }
 """,
 explain="""The classic two-pointer merge. `a[i...]` is empty when `i == a.count`, so appending the leftovers needs no extra checks. `<=` keeps the merge **stable**.""",
 tests=[({'a':[1,3,5],'b':[2,4,6]},[1,2,3,4,5,6]), {'a':[],'b':[1]}, {'a':[],'b':[]}, {'a':[1,1,1],'b':[1,1]}, {'a':[-3,10],'b':[-5,0,20,30]}]))
P.append(dict(id='array-safe-subscript', title='Safe Subscript Extension', topic='Arrays', notes='6', diff='medium', concepts=['subscripts','extensions','optionals'], docs=[('Subscripts','LanguageGuide/Subscripts'),('Extensions','LanguageGuide/Extensions')],
 sig='func pick(_ items: [String], at indices: [Int]) -> [String?]',
 statement="""Out-of-range subscripts **crash** in Swift. Add an extension so any `Collection` supports `items[safe: i]`, returning `nil` for an invalid index. Then implement `pick`, which returns `items[safe: i]` for each index.

 ```swift
 pick(["a", "b"], at: [0, 5, -1, 1])  // ["a", nil, nil, "b"]
 ```""",
 starter="""
 extension Collection {
     // add subscript(safe index: Index) -> Element?
 }

 func pick(_ items: [String], at indices: [Int]) -> [String?] {
     return []
 }
 """,
 solution="""
 extension Collection {
     subscript(safe index: Index) -> Element? {
         indices.contains(index) ? self[index] : nil
     }
 }

 func pick(_ items: [String], at indices: [Int]) -> [String?] {
     indices.map { items[safe: $0] }
 }
 """,
 explain="""A **labelled subscript** (`subscript(safe index:)`) is called as `items[safe: i]`. Writing it on `Collection` gives it to arrays, strings, slices and your own collections at once. For arrays `indices.contains` is O(1) because `indices` is a `Range`.""",
 tests=[({'items':['a','b'],'indices':[0,5,-1,1]},['a',None,None,'b']), {'items':[],'indices':[0]}, {'items':['x','y','z'],'indices':[2,2,3]}]))
# ---------- Dictionaries (notes §7)
P.append(dict(id='two-sum', title='Two Sum with a Dictionary', topic='Dictionaries', notes='7', concepts=['dictionary-basics','optional-binding'], docs=[('Collection Types — Dictionaries', CT)],
 sig='func twoSum(_ nums: [Int], target: Int) -> [Int]',
 statement="""Return the indices of the two numbers that add up to `target`, smaller index first, or `[]` if none. Solve it in **one pass** with a dictionary from value to index.

 ```swift
 twoSum([2, 7, 11, 15], target: 9)   // [0, 1]
 twoSum([3, 3], target: 6)           // [0, 1]
 twoSum([1, 2], target: 7)           // []
 ```""",
 solution="""
 func twoSum(_ nums: [Int], target: Int) -> [Int] {
     var seen: [Int: Int] = [:]
     for (i, n) in nums.enumerated() {
         if let j = seen[target - n] { return [j, i] }
         seen[n] = i
     }
     return []
 }
 """,
 explain="""`enumerated()` yields `(offset, element)` pairs. A dictionary lookup returns an **optional**, so `if let` checks and unwraps at once. Storing `seen[n] = i` *after* the lookup stops a number pairing with itself.""",
 tests=[({'nums':[2,7,11,15],'target':9},[0,1]), ({'nums':[3,3],'target':6},[0,1]), ({'nums':[1,2],'target':7},[]), {'nums':[-3,4,3,90],'target':0}, {'nums':[],'target':0}, {'nums':[5,75,25],'target':100}]))
P.append(dict(id='word-frequency', title='Word Frequency', topic='Dictionaries', notes='7', concepts=['dictionary-basics'], docs=[('Collection Types — Dictionaries', CT)],
 sig='func wordFrequency(_ text: String) -> [String: Int]',
 statement="""Count how often each word appears, case-insensitively. Words are maximal runs of letters (so punctuation and digits separate words).

 ```swift
 wordFrequency("The cat and the hat.")  // ["the": 2, "cat": 1, "and": 1, "hat": 1]
 ```""",
 solution="""
 func wordFrequency(_ text: String) -> [String: Int] {
     var counts: [String: Int] = [:]
     for word in text.lowercased().split(whereSeparator: { !$0.isLetter }) {
         counts[String(word), default: 0] += 1
     }
     return counts
 }
 """,
 explain="""`dict[key, default: 0] += 1` is *the* counting idiom — it reads the default when the key is missing and writes back in one step. Alternatively: `Dictionary(words.map { ($0, 1) }, uniquingKeysWith: +)`. Dictionaries are unordered, so the judge compares them as JSON objects.""",
 tests=[({'text':'The cat and the hat.'},{'the':2,'cat':1,'and':1,'hat':1}), {'text':''}, {'text':'Go go GO! gopher'}, {'text':"it's 2 o'clock"}]))
P.append(dict(id='group-anagrams', title='Group Anagrams', topic='Dictionaries', notes='7', diff='medium', concepts=['dictionary-basics','sort-custom'], docs=[('Collection Types — Dictionaries', CT)],
 sig='func groupAnagrams(_ words: [String]) -> [[String]]',
 compare='json-unordered-deep',
 statement="""Group words that are anagrams of each other. Order of groups and of words within a group doesn't matter (the judge ignores order).

 ```swift
 groupAnagrams(["eat","tea","tan","ate","nat","bat"])
 // [["eat","tea","ate"], ["tan","nat"], ["bat"]]
 ```""",
 solution="""
 func groupAnagrams(_ words: [String]) -> [[String]] {
     Array(Dictionary(grouping: words) { String($0.sorted()) }.values)
 }
 """,
 explain="""`Dictionary(grouping:by:)` builds `[Key: [Element]]` in one call. The sorted characters of a word are its **canonical key**. `.values` is a view; wrap in `Array` to return it.""",
 tests=[{'words':['eat','tea','tan','ate','nat','bat']}, {'words':[]}, {'words':['a']}, {'words':['abc','bca','cab','xyz','zyx','q']}, {'words':['','']}]))
P.append(dict(id='invert-dictionary', title='Invert a Dictionary', topic='Dictionaries', notes='7', diff='easy', concepts=['dictionary-basics','sort-custom'], docs=[('Collection Types — Dictionaries', CT)],
 sig='func invert(_ grades: [String: String]) -> [String: [String]]',
 statement="""`grades` maps student → letter grade. Return grade → **alphabetically sorted** list of students.

 ```swift
 invert(["ana": "A", "bo": "B", "cy": "A"])  // ["A": ["ana", "cy"], "B": ["bo"]]
 ```""",
 solution="""
 func invert(_ grades: [String: String]) -> [String: [String]] {
     var result: [String: [String]] = [:]
     for (student, grade) in grades {
         result[grade, default: []].append(student)
     }
     return result.mapValues { $0.sorted() }
 }
 """,
 explain="""Iterating a dictionary yields `(key, value)` tuples you can destructure. Because iteration order is **unspecified** (and changes between runs), the sort is what makes the output deterministic. `mapValues` keeps keys and transforms values.""",
 tests=[({'grades':{'ana':'A','bo':'B','cy':'A'}},{'A':['ana','cy'],'B':['bo']}), {'grades':{}}, {'grades':{'z':'C','y':'C','x':'C'}}]))
P.append(dict(id='first-unique-char', title='First Unique Character', topic='Dictionaries', notes='7', diff='easy', concepts=['dictionary-basics','strings-are-collections'], docs=[('Collection Types — Dictionaries', CT)],
 sig='func firstUniqueIndex(_ s: String) -> Int',
 statement="""Return the (character) index of the first character that appears exactly once, or `-1`.

 ```swift
 firstUniqueIndex("leetcode")      // 0
 firstUniqueIndex("loveleetcode")  // 2
 firstUniqueIndex("aabb")          // -1
 ```""",
 solution="""
 func firstUniqueIndex(_ s: String) -> Int {
     var counts: [Character: Int] = [:]
     for ch in s { counts[ch, default: 0] += 1 }
     for (i, ch) in s.enumerated() where counts[ch] == 1 {
         return i
     }
     return -1
 }
 """,
 explain="""Two passes: count, then find. `counts[ch] == 1` compares an `Int?` with `1` — Swift lifts `==` to optionals, so no unwrapping needed.""",
 tests=[({'s':'leetcode'},0), ({'s':'loveleetcode'},2), ({'s':'aabb'},-1), {'s':''}, {'s':'z'}, {'s':'ééa'}]))
P.append(dict(id='dictionary-default-lookup', title='Look Up with a Default', topic='Dictionaries', notes='7', diff='easy', concepts=['dictionary-basics','nil-coalescing'], docs=[('Collection Types — Accessing a Dictionary', CT)],
 sig='func describeCodes(_ codes: [Int]) -> [String]',
 statement="""Map HTTP status codes to reason phrases using this table; unknown codes become `"Unknown (<code>)"`.

 ```swift
 200: "OK", 201: "Created", 301: "Moved Permanently", 404: "Not Found", 500: "Internal Server Error"
 ```""",
 solution="""
 func describeCodes(_ codes: [Int]) -> [String] {
     let phrases = [200: "OK", 201: "Created", 301: "Moved Permanently", 404: "Not Found", 500: "Internal Server Error"]
     return codes.map { phrases[$0, default: "Unknown (\\($0))"] }
 }
 """,
 explain="""`phrases[$0, default: …]` and `phrases[$0] ?? …` are equivalent for reads. The `default:` subscript shines for **writes** like `counts[k, default: 0] += 1`.""",
 tests=[({'codes':[200,404]},['OK','Not Found']), {'codes':[]}, {'codes':[418,500,301,201]}]))
# ---------- Sets (notes §8)
P.append(dict(id='contains-duplicate', title='Contains Duplicate', topic='Sets', notes='8', diff='easy', concepts=['set-vs-array'], docs=[('Collection Types — Sets', CT)],
 sig='func containsDuplicate(_ nums: [Int]) -> Bool',
 statement="Return `true` if any value appears at least twice.",
 solution="func containsDuplicate(_ nums: [Int]) -> Bool {\n    Set(nums).count != nums.count\n}\n",
 explain="""Building a `Set` drops duplicates, so a size mismatch means there was one. For early exit on huge inputs, loop and use `insert(_:)`, whose result tuple's `inserted` flag tells you if the value was new.""",
 tests=[({'nums':[1,2,3,1]},True), ({'nums':[1,2,3,4]},False), {'nums':[]}, {'nums':[1,1,1,3,3,4,3,2,4,2]}]))
P.append(dict(id='set-algebra', title='Set Algebra on Tags', topic='Sets', notes='8', diff='easy', concepts=['set-vs-array','collection-types'], docs=[('Collection Types — Fundamental Set Operations', CT)],
 sig='func tagReport(_ a: [String], _ b: [String]) -> [[String]]',
 statement="""Given two tag lists, return four **sorted** arrays: `[common, onlyInA, onlyInB, inEitherButNotBoth]`.""",
 solution="""
 func tagReport(_ a: [String], _ b: [String]) -> [[String]] {
     let sa = Set(a), sb = Set(b)
     return [
         sa.intersection(sb).sorted(),
         sa.subtracting(sb).sorted(),
         sb.subtracting(sa).sorted(),
         sa.symmetricDifference(sb).sorted(),
     ]
 }
 """,
 explain="""`intersection`, `subtracting`, `union` and `symmetricDifference` return new sets (the `form…` variants mutate). Sets are unordered — `sorted()` returns an `Array`, giving deterministic output.""",
 tests=[({'a':['swift','ios','ml'],'b':['ml','python','swift']},[['ml','swift'],['ios'],['python'],['ios','python']]), {'a':[],'b':['x']}, {'a':['a','a','b'],'b':['b','b']}]))
P.append(dict(id='longest-consecutive', title='Longest Consecutive Run', topic='Sets', notes='8', diff='medium', concepts=['set-vs-array'], docs=[('Collection Types — Sets', CT)],
 sig='func longestConsecutive(_ nums: [Int]) -> Int',
 statement="""Return the length of the longest run of consecutive integers (in any order) in O(n).

 ```swift
 longestConsecutive([100, 4, 200, 1, 3, 2])  // 4  (1,2,3,4)
 ```""",
 solution="""
 func longestConsecutive(_ nums: [Int]) -> Int {
     let set = Set(nums)
     var best = 0
     for n in set where !set.contains(n - 1) {
         var length = 1
         while set.contains(n + length) { length += 1 }
         best = max(best, length)
     }
     return best
 }
 """,
 explain="""Only start counting at the **beginning** of a run (`n - 1` not present), so each element is visited a bounded number of times: O(n) overall thanks to O(1) set lookups.""",
 tests=[({'nums':[100,4,200,1,3,2]},4), {'nums':[]}, {'nums':[0,3,7,2,5,8,4,6,0,1]}, {'nums':[1,2,0,1]}, {'nums':[-1,-2,-3,10]}]))
P.append(dict(id='hashable-point-set', title='Unique Points (Hashable)', topic='Sets', notes='8', diff='medium', concepts=['equatable-hashable','set-vs-array'], docs=[('Collection Types — Hash Values for Set Types', CT)],
 sig='func uniquePointCount(_ coords: [[Int]]) -> Int',
 statement="""Each element of `coords` is `[x, y]`. Define `struct Point: Hashable` and return how many **distinct** points there are by putting them in a `Set<Point>`.

 (Tuples can't go in a `Set` — they can't conform to `Hashable`.)""",
 starter="""
 struct Point {
     let x: Int
     let y: Int
 }

 func uniquePointCount(_ coords: [[Int]]) -> Int {
     return 0
 }
 """,
 solution="""
 struct Point: Hashable {
     let x: Int
     let y: Int
 }

 func uniquePointCount(_ coords: [[Int]]) -> Int {
     Set(coords.map { Point(x: $0[0], y: $0[1]) }).count
 }
 """,
 explain="""Declaring `: Hashable` is enough — the compiler synthesises `==` and `hash(into:)` from the stored properties because they're all Hashable. Sets and dictionary keys require it.""",
 tests=[({'coords':[[1,2],[2,1],[1,2]]},2), {'coords':[]}, {'coords':[[0,0],[0,0],[0,0]]}, {'coords':[[1,1],[1,2],[2,1],[2,2]]}]))
# ---------- Tuples (notes §16)
P.append(dict(id='min-max-tuple', title='Min and Max in One Pass', topic='Tuples', notes='16', concepts=['tuples','optionals'], docs=[('Functions — Functions with Multiple Return Values', FN)],
 sig='func bounds(_ nums: [Int]) -> [Int]',
 statement="""First write a helper `func minMax(_ nums: [Int]) -> (min: Int, max: Int)?` that returns a **named tuple** (or `nil` for an empty array) in one pass. Then `bounds` returns `[min, max]`, or `[]`.

 (The judge needs JSON, and tuples aren't `Codable` — hence the array wrapper.)""",
 starter="""
 func minMax(_ nums: [Int]) -> (min: Int, max: Int)? {
     return nil
 }

 func bounds(_ nums: [Int]) -> [Int] {
     guard let result = minMax(nums) else { return [] }
     return [result.min, result.max]
 }
 """,
 solution="""
 func minMax(_ nums: [Int]) -> (min: Int, max: Int)? {
     guard var lo = nums.first else { return nil }
     var hi = lo
     for n in nums.dropFirst() {
         lo = Swift.min(lo, n)
         hi = Swift.max(hi, n)
     }
     return (lo, hi)
 }

 func bounds(_ nums: [Int]) -> [Int] {
     guard let result = minMax(nums) else { return [] }
     return [result.min, result.max]
 }
 """,
 explain="""Returning an **optional tuple** handles the empty case in the type. Labels (`min:`, `max:`) make the call site self-documenting. `Swift.min` disambiguates the global function from the tuple labels in scope.""",
 tests=[({'nums':[3,1,4,1,5]},[1,5]), ({'nums':[]},[]), {'nums':[7]}, {'nums':[-2,-9,0]}]))
P.append(dict(id='tuple-compare-sort', title='Sort by Several Keys with Tuples', topic='Tuples', notes='16', diff='medium', concepts=['tuple-comparison','sort-custom'], docs=[('Basic Operators — Comparison Operators', BO)],
 sig='func leaderboard(_ entries: [[String]]) -> [String]',
 statement="""Each entry is `[name, points, wins]` (numbers as strings). Return names sorted by **points descending**, then **wins descending**, then **name ascending** — compare tuples instead of writing nested `if`s.""",
 solution="""
 func leaderboard(_ entries: [[String]]) -> [String] {
     let rows = entries.map { (name: $0[0], points: Int($0[1])!, wins: Int($0[2])!) }
     return rows.sorted {
         (-$0.points, -$0.wins, $0.name) < (-$1.points, -$1.wins, $1.name)
     }.map(\\.name)
 }
 """,
 explain="""Tuples of `Comparable` elements compare **lexicographically** — first elements, then second on a tie, and so on (up to 6 elements). Negating turns descending keys into ascending ones. Key-path `map(\\.name)` works on tuple labels too.""",
 tests=[({'entries':[['ann','10','2'],['bob','12','1'],['cat','10','3'],['dan','10','3']]},['bob','cat','dan','ann']), {'entries':[]}, {'entries':[['z','0','0'],['a','0','0']]}]))
P.append(dict(id='predict-tuple-switch', title='Predict: Switching on Tuples', topic='Tuples', mode='predict', notes='16', concepts=['tuples','switch-statement'], docs=[('Control Flow — Tuples', CF)],
 statement="Predict the output. Watch the order of cases — the **first** match wins.",
 snippet="""
 let points = [(0, 0), (3, 0), (0, -2), (2, 2), (-1, 5)]
 for p in points {
     switch p {
     case (0, 0):
         print("origin")
     case (_, 0):
         print("x-axis at \\(p.0)")
     case (0, let y):
         print("y-axis at \\(y)")
     case let (x, y) where x == y:
         print("diagonal \\(x)")
     case (-2...2, _):
         print("near")
     default:
         print("far")
     }
 }
 """,
 explain="""`_` matches anything, `let` binds, `where` adds a condition, and ranges match via `~=`. Swift checks cases **top to bottom** and never falls through."""))
# ---------- Ranges & stride
P.append(dict(id='stride-countdown', title='Countdown with stride', topic='Ranges', notes='14', diff='easy', concepts=['stride','half-open-range'], docs=[('Control Flow — For-In Loops', CF)],
 sig='func countdown(from start: Int, step: Int) -> [Int]',
 statement="""Return the numbers from `start` down to `0` **inclusive** (if reachable) in steps of `step` (> 0).

 ```swift
 countdown(from: 10, step: 3)  // [10, 7, 4, 1]
 countdown(from: 6, step: 2)   // [6, 4, 2, 0]
 ```""",
 solution="func countdown(from start: Int, step: Int) -> [Int] {\n    Array(stride(from: start, through: 0, by: -step))\n}\n",
 explain="""`stride(from:through:by:)` includes the end if it lands on it; `stride(from:to:by:)` excludes it. A negative step counts down. The result is a lazy sequence — `Array(...)` materialises it.""",
 tests=[({'start':10,'step':3},[10,7,4,1]), ({'start':6,'step':2},[6,4,2,0]), {'start':0,'step':1}, {'start':-1,'step':1}, {'start':100,'step':25}]))
P.append(dict(id='range-clamp', title='Clamp to a Range', topic='Ranges', notes='14', diff='easy', concepts=['half-open-range','extensions','generic-constraints'], docs=[('Basic Operators — Range Operators', BO)],
 sig='func clampAll(_ values: [Int], low: Int, high: Int) -> [Int]',
 statement="""Add `extension Comparable { func clamped(to range: ClosedRange<Self>) -> Self }` and use it to clamp every value into `low...high`.""",
 starter="""
 extension Comparable {
     // func clamped(to range: ClosedRange<Self>) -> Self
 }

 func clampAll(_ values: [Int], low: Int, high: Int) -> [Int] {
     return values
 }
 """,
 solution="""
 extension Comparable {
     func clamped(to range: ClosedRange<Self>) -> Self {
         min(max(self, range.lowerBound), range.upperBound)
     }
 }

 func clampAll(_ values: [Int], low: Int, high: Int) -> [Int] {
     values.map { $0.clamped(to: low...high) }
 }
 """,
 explain="""Extending the **protocol** `Comparable` gives `clamped(to:)` to `Int`, `Double`, `String`, dates… `Self` is the conforming type. `ClosedRange` exposes `lowerBound`/`upperBound`.""",
 tests=[({'values':[-5,3,12],'low':0,'high':10},[0,3,10]), {'values':[],'low':0,'high':1}, {'values':[5,5],'low':5,'high':5}]))
P.append(dict(id='diag-closed-range-crash', title='Diagnostic: A Range That Can\'t Exist', topic='Ranges', mode='diagnostic', notes='14', concepts=['half-open-range','type-inference'], docs=[('Basic Operators — Range Operators', BO)],
 statement="""Some mistakes are caught at compile time, some only at runtime. Here's one the compiler *can* catch: declare a constant **of type `Range<Int>`** and try to initialise it with a *closed* range literal, `0...5`.

 You pass when the compiler reports a type mismatch mentioning `ClosedRange`.""",
 starter="let r: Range<Int> = 0..<5\nprint(r)\n",
 solution="let r: Range<Int> = 0...5\nprint(r)\n",
 explain="""`0..<5` is a `Range<Int>` and `0...5` is a `ClosedRange<Int>` — **different types**, so the compiler rejects the mismatch. (By contrast, `5...0` has the right type and only traps at *runtime*: *Range requires lowerBound <= upperBound*.)""",
 tests=[{'name':'Type mismatch reported','pattern':'ClosedRange'}]))

write_all(P, 'beginner', 300)
