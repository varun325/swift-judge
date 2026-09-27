import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
GE='LanguageGuide/Generics'; CT='LanguageGuide/CollectionTypes'; EN='LanguageGuide/Enumerations'; CF='LanguageGuide/ControlFlow'; FN='LanguageGuide/Functions'; SC='LanguageGuide/StringsAndCharacters'
P=[]
T='Algorithms'
P.append(dict(id='valid-parentheses', title='Valid Parentheses', topic=T, diff='easy', concepts=['switch-statement','array-basics','dictionary-basics'], docs=[('Collection Types', CT)],
 sig='func isValid(_ s: String) -> Bool',
 statement="""Return whether every bracket in `s` (`()[]{}` only) is closed in the correct order. Use an array as a stack and a `[Character: Character]` of closing → opening.""",
 solution="""
 func isValid(_ s: String) -> Bool {
     let pairs: [Character: Character] = [")": "(", "]": "[", "}": "{"]
     var stack: [Character] = []
     for ch in s {
         if let open = pairs[ch] {
             guard stack.popLast() == open else { return false }
         } else {
             stack.append(ch)
         }
     }
     return stack.isEmpty
 }
 """,
 explain="""`popLast()` returns `nil` on an empty stack, and comparing `Character?` with `Character` via `==` handles that case without unwrapping.""",
 tests=[({'s':'()[]{}'},True), ({'s':'(]'},False), {'s':''}, {'s':'([{}])'}, {'s':'(('}, {'s':'))'}, {'s':'{[()()]}'}, {'s':'([)]'}]))
P.append(dict(id='generic-binary-search', title='Generic Binary Search', topic=T, diff='medium', concepts=['generics','generic-constraints','extensions'], docs=[('Generics — Extensions with a Generic Where Clause', GE)],
 sig='func searchDemo(_ nums: [Int], _ words: [String], target: Int, word: String) -> [Int]',
 statement="""Add `func binarySearch(_ target: Element) -> Index?` to every `RandomAccessCollection where Element: Comparable` (assume sorted input). Return `[index of target in nums or -1, index of word in words or -1, index of target in nums[2...] or -1]` — the slice case proves you used the collection's own **indices**, not `0..<count`.""",
 solution="""
 extension RandomAccessCollection where Element: Comparable {
     func binarySearch(_ target: Element) -> Index? {
         var low = startIndex
         var high = endIndex
         while low < high {
             let mid = index(low, offsetBy: distance(from: low, to: high) / 2)
             if self[mid] == target { return mid }
             if self[mid] < target { low = index(after: mid) } else { high = mid }
         }
         return nil
     }
 }

 func searchDemo(_ nums: [Int], _ words: [String], target: Int, word: String) -> [Int] {
     let slice = nums.count > 2 ? nums[2...] : nums[nums.endIndex...]
     return [nums.binarySearch(target) ?? -1, words.binarySearch(word) ?? -1, slice.binarySearch(target) ?? -1]
 }
 """,
 explain="""`RandomAccessCollection` guarantees O(1) `index(_:offsetBy:)`, keeping the search O(log n). An `ArraySlice` keeps the **original** indices (`nums[2...]` starts at 2), which is why generic code must use `startIndex`/`endIndex`.""",
 tests=[({'nums':[1,3,5,7,9],'words':['a','c','e'],'target':7,'word':'c'},[3,1,3]), {'nums':[],'words':[],'target':1,'word':'x'}, {'nums':[1,2],'words':['z'],'target':1,'word':'z'}, {'nums':[2,4,6,8,10,12],'words':['ant','bee','cat','dog'],'target':4,'word':'dog'}]))
P.append(dict(id='merge-intervals', title='Merge Intervals', topic=T, diff='medium', concepts=['sort-custom','tuples'], docs=[('Collection Types', CT)],
 sig='func merge(_ intervals: [[Int]]) -> [[Int]]',
 statement="""Merge all overlapping `[start, end]` intervals (touching ones like `[1,4]` and `[4,5]` merge too) and return them sorted by start.""",
 solution="""
 func merge(_ intervals: [[Int]]) -> [[Int]] {
     var result: [[Int]] = []
     for iv in intervals.sorted(by: { $0[0] < $1[0] }) {
         if let last = result.last, iv[0] <= last[1] {
             result[result.count - 1][1] = max(last[1], iv[1])
         } else {
             result.append(iv)
         }
     }
     return result
 }
 """,
 explain="""Sorting by start means each interval can only overlap the **last** merged one. `if let last = result.last, condition` combines unwrapping and a test. Nested-array mutation `result[i][1] = …` works in place because arrays are value types with in-place mutation through subscripts.""",
 tests=[({'intervals':[[1,3],[2,6],[8,10],[15,18]]},[[1,6],[8,10],[15,18]]), {'intervals':[[1,4],[4,5]]}, {'intervals':[]}, {'intervals':[[5,6],[1,10]]}, {'intervals':[[1,2],[3,4],[2,3]]}]))
P.append(dict(id='top-k-frequent', title='Top K Frequent Words', topic=T, diff='medium', concepts=['dictionary-basics','sort-custom','tuple-comparison'], docs=[('Collection Types', CT)],
 sig='func topKFrequent(_ words: [String], _ k: Int) -> [String]',
 statement="""Return the `k` most frequent words, sorted by frequency (high → low), ties alphabetical (LeetCode #692).""",
 solution="""
 func topKFrequent(_ words: [String], _ k: Int) -> [String] {
     let counts = words.reduce(into: [String: Int]()) { $0[$1, default: 0] += 1 }
     return counts
         .sorted { ($1.value, $0.key) < ($0.value, $1.key) }
         .prefix(k)
         .map(\\.key)
 }
 """,
 explain="""Sorting dictionary entries gives `[(key, value)]`. Swapping which side each element appears on in the tuple comparison makes count **descending** and key **ascending** in one expression. `prefix(k)` is safe even if `k > count`.""",
 tests=[({'words':['i','love','leetcode','i','love','coding'],'k':2},['i','love']), {'words':['the','day','is','sunny','the','the','the','sunny','is','is'],'k':4}, {'words':[],'k':3}, {'words':['b','a','c'],'k':2}]))
P.append(dict(id='number-of-islands', title='Number of Islands (BFS)', topic=T, diff='medium', concepts=['inout','array-basics','tuples'], docs=[('Collection Types', CT)],
 sig='func numIslands(_ grid: [String]) -> Int',
 statement="""Each string is a row of `"1"` (land) and `"0"` (water). Count 4-directionally connected islands. Convert the rows to `[[Character]]`, and write a BFS helper that takes the grid `inout` and sinks visited land.""",
 solution="""
 func sink(_ grid: inout [[Character]], _ r: Int, _ c: Int) {
     var queue = [(r, c)]
     grid[r][c] = "0"
     while !queue.isEmpty {
         let (y, x) = queue.removeLast()
         for (dy, dx) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
             let ny = y + dy, nx = x + dx
             guard grid.indices.contains(ny), grid[ny].indices.contains(nx), grid[ny][nx] == "1" else { continue }
             grid[ny][nx] = "0"
             queue.append((ny, nx))
         }
     }
 }

 func numIslands(_ grid: [String]) -> Int {
     var g = grid.map(Array.init)
     var count = 0
     for r in g.indices {
         for c in g[r].indices where g[r][c] == "1" {
             count += 1
             sink(&g, r, c)
         }
     }
     return count
 }
 """,
 explain="""`grid.map(Array.init)` turns each `String` into `[Character]` for O(1) indexing. Tuples make great lightweight coordinates, and destructuring `let (y, x) = …` unpacks them. `indices.contains` is the bounds check. (Using `removeLast()` makes it DFS order — either works for counting.)""",
 tests=[({'grid':['11110','11010','11000','00000']},1), ({'grid':['11000','11000','00100','00011']},3), {'grid':[]}, {'grid':['0']}, {'grid':['101','010','101']}]))
P.append(dict(id='design-trie', title='Design: Trie (Prefix Tree)', topic=T, diff='medium', concepts=['class-definition','dictionary-basics'], docs=[('Structures and Classes','LanguageGuide/ClassesAndStructures')],
 statement="""Implement `final class Trie` with `insert(_ word: String)`, `search(_ word: String) -> Bool` and `startsWith(_ prefix: String) -> Bool` (LeetCode #208). Nodes are a class with `children: [Character: Node]` and `isEnd`.

 The judge sends `{"ops": [...], "words": [...]}` — one word per op — and prints the Bool results (`null` for insert).""",
 starter="""
 final class Trie {
     func insert(_ word: String) {}
     func search(_ word: String) -> Bool { false }
     func startsWith(_ prefix: String) -> Bool { false }
 }
 """,
 solution="""
 final class Trie {
     private final class Node {
         var children: [Character: Node] = [:]
         var isEnd = false
     }

     private let root = Node()

     func insert(_ word: String) {
         var node = root
         for ch in word {
             if let next = node.children[ch] {
                 node = next
             } else {
                 let next = Node()
                 node.children[ch] = next
                 node = next
             }
         }
         node.isEnd = true
     }

     private func find(_ prefix: String) -> Node? {
         var node = root
         for ch in prefix {
             guard let next = node.children[ch] else { return nil }
             node = next
         }
         return node
     }

     func search(_ word: String) -> Bool { find(word)?.isEnd ?? false }
     func startsWith(_ prefix: String) -> Bool { find(prefix) != nil }
 }
 """,
 harness="""
 struct __Input: Decodable { let ops: [String]; let words: [String] }
 func __run(_ __i: __Input) async throws -> [Bool?] {
     let trie = Trie()
     return zip(__i.ops, __i.words).map { op, word -> Bool? in
         switch op {
         case "insert": trie.insert(word); return nil
         case "search": return trie.search(word)
         default: return trie.startsWith(word)
         }
     }
 }
 """,
 explain="""A class suits tree nodes: children are shared references that we mutate in place. `var node = root` walks the tree by reassigning a **reference**. Optional chaining plus `??` (`find(word)?.isEnd ?? false`) collapses the not-found case.""",
 tests=[({'ops':['insert','search','search','startsWith','insert','search'],'words':['apple','apple','app','app','app','app']},[None,True,False,True,None,True]),
        {'ops':['search','startsWith'],'words':['a','']},
        {'ops':['insert','insert','startsWith','search','search'],'words':['café','cab','ca','cafe','café']}]))
P.append(dict(id='longest-unique-substring', title='Longest Substring Without Repeats', topic=T, diff='medium', concepts=['dictionary-basics','strings-are-collections'], docs=[('Strings and Characters', SC)],
 sig='func lengthOfLongestSubstring(_ s: String) -> Int',
 statement="""Return the length of the longest substring without repeating **characters** (grapheme clusters — emoji count as one). Sliding window + dictionary of last positions.""",
 solution="""
 func lengthOfLongestSubstring(_ s: String) -> Int {
     var lastSeen: [Character: Int] = [:]
     var start = 0
     var best = 0
     for (i, ch) in s.enumerated() {
         if let prev = lastSeen[ch], prev >= start { start = prev + 1 }
         lastSeen[ch] = i
         best = max(best, i - start + 1)
     }
     return best
 }
 """,
 explain="""`enumerated()` gives integer offsets while iterating `Character`s — no `String.Index` arithmetic needed. Each character is visited once: O(n).""",
 tests=[({'s':'abcabcbb'},3), ({'s':'bbbbb'},1), ({'s':'pwwkew'},3), {'s':''}, {'s':'🍎🍌🍎'}, {'s':'dvdf'}, {'s':'abba'}]))
P.append(dict(id='product-except-self', title='Product of Array Except Self', topic=T, diff='medium', concepts=['array-basics','map-filter-reduce'], docs=[('Collection Types', CT)],
 sig='func productExceptSelf(_ nums: [Int]) -> [Int]',
 statement="""Return `answer[i]` = product of all elements except `nums[i]`, in O(n) **without division** (LeetCode #238).""",
 solution="""
 func productExceptSelf(_ nums: [Int]) -> [Int] {
     var answer = Array(repeating: 1, count: nums.count)
     var prefix = 1
     for i in nums.indices {
         answer[i] = prefix
         prefix *= nums[i]
     }
     var suffix = 1
     for i in nums.indices.reversed() {
         answer[i] *= suffix
         suffix *= nums[i]
     }
     return answer
 }
 """,
 explain="""Two passes: prefix products left→right, then multiply in suffix products right→left. `indices.reversed()` iterates backwards without index arithmetic.""",
 tests=[({'nums':[1,2,3,4]},[24,12,8,6]), {'nums':[-1,1,0,-3,3]}, {'nums':[5]}, {'nums':[]}, {'nums':[0,0]}]))
P.append(dict(id='max-subarray', title='Maximum Subarray (Kadane)', topic=T, diff='easy', concepts=['map-filter-reduce','tuples'], docs=[('Closures','LanguageGuide/Closures')],
 sig='func maxSubArray(_ nums: [Int]) -> Int',
 statement="""Return the largest sum of a non-empty contiguous subarray. Try writing it as a single `reduce` over a `(current, best)` tuple.""",
 solution="""
 func maxSubArray(_ nums: [Int]) -> Int {
     guard let first = nums.first else { return 0 }
     return nums.dropFirst().reduce((current: first, best: first)) { acc, x in
         let current = max(x, acc.current + x)
         return (current, max(acc.best, current))
     }.best
 }
 """,
 explain="""Kadane's algorithm keeps the best sum **ending here** and the best overall. A labelled tuple is a neat `reduce` accumulator for multiple running values.""",
 tests=[({'nums':[-2,1,-3,4,-1,2,1,-5,4]},6), {'nums':[1]}, {'nums':[-3,-1,-2]}, {'nums':[5,4,-1,7,8]}]))
P.append(dict(id='coin-change', title='Coin Change (Dynamic Programming)', topic=T, diff='medium', concepts=['array-basics','optionals'], docs=[('Collection Types', CT)],
 sig='func coinChange(_ coins: [Int], _ amount: Int) -> Int',
 statement="""Return the fewest coins that make `amount`, or `-1` if impossible (LeetCode #322). Use a bottom-up DP array of `Int?` where `nil` means unreachable.""",
 solution="""
 func coinChange(_ coins: [Int], _ amount: Int) -> Int {
     var best: [Int?] = Array(repeating: nil, count: amount + 1)
     best[0] = 0
     guard amount > 0 else { return 0 }
     for value in 1...amount {
         best[value] = coins.compactMap { coin in
             coin <= value ? best[value - coin].map { $0 + 1 } : nil
         }.min()
     }
     return best[amount] ?? -1
 }
 """,
 explain="""Modelling "unreachable" as `nil` instead of a magic `Int.max` avoids overflow bugs. `Optional.map` adds 1 only when reachable, `compactMap` drops the rest, and `min()` on an empty array is `nil` — exactly right.""",
 tests=[({'coins':[1,2,5],'amount':11},3), ({'coins':[2],'amount':3},-1), {'coins':[1],'amount':0}, {'coins':[186,419,83,408],'amount':6249}, {'coins':[3,7],'amount':5}]))
P.append(dict(id='permutations', title='Permutations (Backtracking)', topic=T, diff='medium', concepts=['inout','functions-basics'], docs=[('Functions — In-Out Parameters', FN)],
 sig='func permute(_ nums: [Int]) -> [[Int]]',
 compare='json-unordered',
 statement="""Return all permutations of distinct integers (any order). Write a nested recursive helper that builds the current path with `inout` state and backtracks.""",
 solution="""
 func permute(_ nums: [Int]) -> [[Int]] {
     var result: [[Int]] = []
     var path: [Int] = []
     var used = Array(repeating: false, count: nums.count)

     func backtrack() {
         if path.count == nums.count {
             result.append(path)
             return
         }
         for i in nums.indices where !used[i] {
             used[i] = true
             path.append(nums[i])
             backtrack()
             path.removeLast()
             used[i] = false
         }
     }

     backtrack()
     return result
 }
 """,
 explain="""A nested function can capture and mutate the enclosing function's `var`s — no need to pass everything around. Every choice is undone after recursing (`removeLast`, `used[i] = false`): that's backtracking.""",
 tests=[{'nums':[1,2,3]}, {'nums':[0,1]}, {'nums':[1]}, {'nums':[]}]))
P.append(dict(id='heap-kth-largest', title='Generic Heap: Kth Largest', topic=T, diff='hard', concepts=['generics','generic-constraints','closures'], docs=[('Generics', GE)],
 sig='func kthLargest(_ nums: [Int], _ k: Int) -> Int',
 statement="""Swift's standard library has no heap. Write `struct Heap<Element>` with a stored `areSorted: (Element, Element) -> Bool` comparator, `insert`, `popTop() -> Element?`, `peek` and `count` (sift up / sift down).

 Use a **min-heap of size k** to find the k-th largest element (1 ≤ k ≤ count).""",
 solution="""
 struct Heap<Element> {
     private var items: [Element] = []
     private let areSorted: (Element, Element) -> Bool

     init(by areSorted: @escaping (Element, Element) -> Bool) { self.areSorted = areSorted }

     var count: Int { items.count }
     var peek: Element? { items.first }

     mutating func insert(_ x: Element) {
         items.append(x)
         var child = items.count - 1
         while child > 0 {
             let parent = (child - 1) / 2
             guard areSorted(items[child], items[parent]) else { break }
             items.swapAt(child, parent)
             child = parent
         }
     }

     mutating func popTop() -> Element? {
         guard !items.isEmpty else { return nil }
         items.swapAt(0, items.count - 1)
         let top = items.removeLast()
         var parent = 0
         while true {
             let l = 2 * parent + 1, r = l + 1
             var candidate = parent
             if l < items.count, areSorted(items[l], items[candidate]) { candidate = l }
             if r < items.count, areSorted(items[r], items[candidate]) { candidate = r }
             if candidate == parent { break }
             items.swapAt(parent, candidate)
             parent = candidate
         }
         return top
     }
 }

 func kthLargest(_ nums: [Int], _ k: Int) -> Int {
     var heap = Heap<Int>(by: <)
     for n in nums {
         heap.insert(n)
         if heap.count > k { _ = heap.popTop() }
     }
     return heap.peek!
 }
 """,
 explain="""Storing the comparator as a closure lets one generic type be a min-heap (`<`) or max-heap (`>`) — operators are functions, so `Heap(by: <)` just works. Keeping only k elements makes it O(n log k).""",
 tests=[({'nums':[3,2,1,5,6,4],'k':2},5), ({'nums':[3,2,3,1,2,4,5,5,6],'k':4},4), {'nums':[1],'k':1}, {'nums':[-1,-1,-2],'k':3}, {'nums':list(range(100,0,-3)),'k':7}]))
P.append(dict(id='dijkstra', title="Dijkstra's Shortest Paths", topic=T, diff='hard', concepts=['dictionary-basics','tuples','optionals'], docs=[('Collection Types', CT)],
 sig='func shortestPaths(_ n: Int, _ edges: [[Int]], _ source: Int) -> [Int]',
 statement="""Nodes `0..<n`, directed `edges` `[from, to, weight]` (weights ≥ 0). Return the shortest distance from `source` to every node, `-1` if unreachable.

 A simple O(V²) version (pick the unvisited node with the smallest tentative distance each round) is fine here; bonus: reuse your `Heap` from the previous problem.""",
 solution="""
 func shortestPaths(_ n: Int, _ edges: [[Int]], _ source: Int) -> [Int] {
     var adjacency = Array(repeating: [(to: Int, w: Int)](), count: n)
     for e in edges { adjacency[e[0]].append((e[1], e[2])) }
     var dist: [Int?] = Array(repeating: nil, count: n)
     var done = Array(repeating: false, count: n)
     dist[source] = 0
     for _ in 0..<n {
         guard let u = (0..<n).filter({ !done[$0] && dist[$0] != nil }).min(by: { dist[$0]! < dist[$1]! }) else { break }
         done[u] = true
         for (v, w) in adjacency[u] {
             let candidate = dist[u]! + w
             if dist[v].map({ candidate < $0 }) ?? true { dist[v] = candidate }
         }
     }
     return dist.map { $0 ?? -1 }
 }
 """,
 explain="""Named tuples (`(to: Int, w: Int)`) make adjacency lists readable without a struct. `Int?` distances model "infinity" without sentinel overflow. `dist[v].map { candidate < $0 } ?? true` reads: *if there's a distance, is the candidate shorter; if not, take it.*""",
 tests=[({'n':4,'edges':[[0,1,4],[0,2,1],[2,1,2],[1,3,1]],'source':0},[0,3,1,4]), {'n':3,'edges':[],'source':1}, {'n':1,'edges':[],'source':0}, {'n':5,'edges':[[0,1,10],[0,4,3],[4,1,4],[1,2,2],[4,2,8],[2,3,7],[4,3,2],[3,2,9]],'source':0}]))
P.append(dict(id='course-schedule', title='Topological Sort: Course Order', topic=T, diff='medium', concepts=['dictionary-basics','array-basics'], docs=[('Collection Types', CT)],
 sig='func courseOrder(_ numCourses: Int, _ prerequisites: [[Int]]) -> [Int]',
 statement="""`[a, b]` means course `b` must come before `a`. Return a valid order using **Kahn's algorithm**, always taking the **smallest** available course next (so the answer is unique), or `[]` if there's a cycle.""",
 solution="""
 func courseOrder(_ numCourses: Int, _ prerequisites: [[Int]]) -> [Int] {
     var indegree = Array(repeating: 0, count: numCourses)
     var next = Array(repeating: [Int](), count: numCourses)
     for p in prerequisites {
         next[p[1]].append(p[0])
         indegree[p[0]] += 1
     }
     var available = Set((0..<numCourses).filter { indegree[$0] == 0 })
     var order: [Int] = []
     while let course = available.min() {
         available.remove(course)
         order.append(course)
         for n in next[course] {
             indegree[n] -= 1
             if indegree[n] == 0 { available.insert(n) }
         }
     }
     return order.count == numCourses ? order : []
 }
 """,
 explain="""Kahn's algorithm repeatedly removes nodes with no remaining prerequisites. `while let course = available.min()` loops until the set is empty. If some courses never become available, there's a cycle.""",
 tests=[({'numCourses':4,'prerequisites':[[1,0],[2,0],[3,1],[3,2]]},[0,1,2,3]), ({'numCourses':2,'prerequisites':[[1,0],[0,1]]},[]), {'numCourses':1,'prerequisites':[]}, {'numCourses':3,'prerequisites':[[0,2]]}]))
P.append(dict(id='binary-tree-level-order', title='Binary Tree from Level Order', topic=T, diff='hard', concepts=['indirect-enums','optionals','pattern-matching'], docs=[('Enumerations — Recursive Enumerations', EN)],
 sig='func treeStats(_ levelOrder: [Int?]) -> [[Int]]',
 statement="""Build a binary tree from LeetCode-style level order (`null` = missing child) into `indirect enum Tree { case empty; case node(Tree, Int, Tree) }`. Return `[inorder traversal, [max depth], [sum of leaves]]`.

 Hint: build an array of nodes by index with a queue, or construct recursively — but enums are immutable, so assemble children **before** parents (bottom-up).""",
 solution="""
 indirect enum Tree {
     case empty
     case node(Tree, Int, Tree)

     var inorder: [Int] {
         guard case let .node(l, v, r) = self else { return [] }
         return l.inorder + [v] + r.inorder
     }

     var depth: Int {
         guard case let .node(l, _, r) = self else { return 0 }
         return 1 + max(l.depth, r.depth)
     }

     var leafSum: Int {
         switch self {
         case .empty: 0
         case .node(.empty, let v, .empty): v
         case let .node(l, _, r): l.leafSum + r.leafSum
         }
     }
 }

 func build(_ values: [Int?]) -> Tree {
     guard let rootValue = values.first ?? nil else { return .empty }
     // Assign each present node its children's positions in level order.
     var children: [Int: (left: Int?, right: Int?)] = [:]
     var queue = [0]
     var next = 1
     while !queue.isEmpty {
         let i = queue.removeFirst()
         var pair: (left: Int?, right: Int?) = (nil, nil)
         if next < values.count { if values[next] != nil { pair.left = next; queue.append(next) }; next += 1 }
         if next < values.count { if values[next] != nil { pair.right = next; queue.append(next) }; next += 1 }
         children[i] = pair
     }
     func make(_ i: Int?) -> Tree {
         guard let i, let v = values[i] else { return .empty }
         return .node(make(children[i]?.left), v, make(children[i]?.right))
     }
     _ = rootValue
     return make(0)
 }

 func treeStats(_ levelOrder: [Int?]) -> [[Int]] {
     let tree = build(levelOrder)
     return [tree.inorder, [tree.depth], [tree.leafSum]]
 }
 """,
 explain="""Nested patterns like `.node(.empty, let v, .empty)` match leaves directly. Since `indirect` enums are immutable values, you first compute the child positions (the level-order queue), then build recursively from the leaves up. `values.first ?? nil` flattens a `Int??`.""",
 tests=[({'levelOrder':[3,9,20,None,None,15,7]},[[9,3,15,20,7],[3],[31]]), {'levelOrder':[]}, {'levelOrder':[1]}, {'levelOrder':[1,None,2,3]}, {'levelOrder':[1,2,3,4,5,6,7]}]))
P.append(dict(id='roman-numerals', title='Integer to Roman', topic=T, diff='easy', concepts=['tuples','for-in'], docs=[('Control Flow', CF)],
 sig='func toRoman(_ num: Int) -> String',
 statement="""Convert `1...3999` to Roman numerals using an ordered array of `(value, symbol)` tuples including the subtractive pairs (`900 "CM"`, `4 "IV"`…).""",
 solution="""
 func toRoman(_ num: Int) -> String {
     let table = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
                  (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
     var n = num
     var result = ""
     for (value, symbol) in table {
         result += String(repeating: symbol, count: n / value)
         n %= value
     }
     return result
 }
 """,
 explain="""An **array** of tuples keeps the order (a dictionary wouldn't). Destructuring in the `for` pattern names both parts.""",
 tests=[({'num':3},'III'), ({'num':58},'LVIII'), ({'num':1994},'MCMXCIV'), {'num':3999}, {'num':4}, {'num':944}]))
P.append(dict(id='rotate-matrix', title='Rotate an Image In Place', topic=T, diff='medium', concepts=['inout','array-basics'], docs=[('Functions — In-Out Parameters', FN)],
 sig='func rotate(_ matrix: inout [[Int]])',
 statement="""Rotate an `n × n` matrix 90° clockwise **in place**: transpose, then reverse each row.""",
 solution="""
 func rotate(_ matrix: inout [[Int]]) {
     let n = matrix.count
     for i in 0..<n {
         for j in (i + 1)..<max(i + 1, n) {
             (matrix[i][j], matrix[j][i]) = (matrix[j][i], matrix[i][j])
         }
     }
     for i in 0..<n { matrix[i].reverse() }
 }
 """,
 explain="""Tuple assignment swaps without a temporary (the law of exclusivity prevents `swap(&m[i][j], &m[j][i])` on the same array — try it!). `reverse()` mutates in place, `reversed()` returns a view.""",
 tests=[({'matrix':[[1,2,3],[4,5,6],[7,8,9]]},[[7,4,1],[8,5,2],[9,6,3]]), {'matrix':[[1]]}, {'matrix':[]}, {'matrix':[[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]}]))
P.append(dict(id='lcs', title='Longest Common Subsequence', topic=T, diff='medium', concepts=['array-basics','strings-are-collections'], docs=[('Strings and Characters', SC)],
 sig='func lcs(_ a: String, _ b: String) -> Int',
 statement="""Return the length of the longest common subsequence of two strings (by `Character`). Classic 2-D DP — convert strings to `[Character]` first.""",
 solution="""
 func lcs(_ a: String, _ b: String) -> Int {
     let x = Array(a), y = Array(b)
     var dp = Array(repeating: Array(repeating: 0, count: y.count + 1), count: x.count + 1)
     for i in stride(from: x.count - 1, through: 0, by: -1) {
         for j in stride(from: y.count - 1, through: 0, by: -1) {
             dp[i][j] = x[i] == y[j] ? 1 + dp[i + 1][j + 1] : max(dp[i + 1][j], dp[i][j + 1])
         }
     }
     return dp[0][0]
 }
 """,
 explain="""`Array(string)` gives O(1) character access for DP tables. `Array(repeating: Array(repeating: 0, count: m), count: n)` builds a grid — each row is an independent copy (value semantics), unlike some languages' shared-row gotcha.""",
 tests=[({'a':'abcde','b':'ace'},3), {'a':'abc','b':'def'}, {'a':'','b':'x'}, {'a':'AGGTAB','b':'GXTXAYB'}, {'a':'🍎a🍌','b':'a🍌🍎'}]))
# ---------- stdio set
P.append(dict(id='wc-stdio', title='Word Count Clone (stdin)', topic='Standard I/O', mode='stdio', diff='easy', concepts=['strings-are-collections','for-in'], docs=[('Strings and Characters', SC)],
 statement="""Implement a tiny `wc`: read **all** of standard input and print `lines words characters` separated by spaces, where lines = number of `readLine()` results, words = whitespace-separated tokens, characters = total `Character`s **excluding** newlines.""",
 starter="var lines = 0, words = 0, chars = 0\n\nprint(lines, words, chars)\n",
 solution="""
 var lines = 0, words = 0, chars = 0
 while let line = readLine() {
     lines += 1
     words += line.split(whereSeparator: \\.isWhitespace).count
     chars += line.count
 }
 print(lines, words, chars)
 """,
 explain="""`print(a, b, c)` separates items with a space by default. `\\.isWhitespace` is a key path used as a predicate function.""",
 tests=['hello world\nswift is fun\n','', 'one\n\n  spaced   out  \n', '🦅 flies\n'], hidden=1))
P.append(dict(id='csv-column-sums-stdio', title='CSV Column Sums (stdin)', topic='Standard I/O', mode='stdio', diff='medium', concepts=['compactmap-flatmap','dictionary-basics','string-interpolation'], docs=[('Strings and Characters', SC)],
 statement="""The first input line is a CSV header; the rest are rows. For each column, print `"<header>: <sum>"` summing values that parse as `Double` (skip blanks/non-numeric). Print sums with no decimals if whole (`12`), else as Swift prints a `Double` (`3.5`). Columns keep header order.""",
 starter="let header = readLine()?.split(separator: \",\", omittingEmptySubsequences: false).map(String.init) ?? []\n",
 solution="""
 let header = readLine()?.split(separator: ",", omittingEmptySubsequences: false).map(String.init) ?? []
 var sums = Array(repeating: 0.0, count: header.count)
 while let line = readLine() {
     let cells = line.split(separator: ",", omittingEmptySubsequences: false)
     for (i, cell) in cells.enumerated() where i < sums.count {
         if let v = Double(cell.trimmingCharacters(in: .whitespaces)) { sums[i] += v }
     }
 }
 for (name, sum) in zip(header, sums) {
     let text = sum == sum.rounded() ? String(Int(sum)) : String(sum)
     print("\\(name): \\(text)")
 }
 """,
 explain="""`zip` pairs headers with sums and stops at the shorter one. `omittingEmptySubsequences: false` keeps empty cells so columns stay aligned. (`trimmingCharacters` is from Foundation — in `main.swift`, add `import Foundation`.)""",
 tests=['a,b,c\n1,2,3\n4,x,6.5\n', 'price\n', 'x,y\n1,\n,2\n 3 , 4\n'], hidden=1))
P[-1]['solution'] = "import Foundation\n" + P[-1]['solution'].lstrip('\n')
P[-1]['starter'] = "import Foundation\n\n" + P[-1]['starter']
P.append(dict(id='sort-names-stdio', title='Sort Names (stdin)', topic='Standard I/O', mode='stdio', diff='easy', concepts=['sort-custom','tuple-comparison'], docs=[('Collection Types', CT)],
 statement="""Each input line is `"First Last"`. Print the names sorted by **last name**, then first name, case-insensitively, one per line as `"LAST, First"` (last name uppercased). Skip blank lines.""",
 starter="var people: [(first: String, last: String)] = []\n",
 solution="""
 var people: [(first: String, last: String)] = []
 while let line = readLine() {
     let parts = line.split(separator: " ")
     guard parts.count == 2 else { continue }
     people.append((String(parts[0]), String(parts[1])))
 }
 for p in people.sorted(by: { ($0.last.lowercased(), $0.first.lowercased()) < ($1.last.lowercased(), $1.first.lowercased()) }) {
     print("\\(p.last.uppercased()), \\(p.first)")
 }
 """,
 explain="""An array of labelled tuples is a lightweight record type for scripts. Lowercasing both keys gives a case-insensitive order; tuple `<` handles the tie-break.""",
 tests=['Ada Lovelace\nAlan Turing\ngrace hopper\nAlan Kay\n', '', '\nSolo Name\n\n'], hidden=1))
P.append(dict(id='matrix-transpose-stdio', title='Transpose a Matrix (stdin)', topic='Standard I/O', mode='stdio', diff='easy', concepts=['compactmap-flatmap','array-basics'], docs=[('Collection Types', CT)],
 statement="""Read rows of space-separated integers (all rows the same length) until end of input, and print the transpose in the same format.""",
 starter="var rows: [[Int]] = []\n",
 solution="""
 var rows: [[Int]] = []
 while let line = readLine() {
     let row = line.split(separator: " ").compactMap { Int($0) }
     if !row.isEmpty { rows.append(row) }
 }
 if let width = rows.first?.count {
     for c in 0..<width {
         print(rows.map { String($0[c]) }.joined(separator: " "))
     }
 }
 """,
 explain="""`rows.first?.count` is `nil` for empty input, so `if let` handles "nothing to print". Building each output line with `map` + `joined` avoids trailing spaces.""",
 tests=['1 2 3\n4 5 6\n', '', '7\n', '1 2\n3 4\n5 6\n'], hidden=1))
P.append(dict(id='gradebook-stdio', title='Grade Book Report (stdin)', topic='Standard I/O', mode='stdio', diff='medium', concepts=['dictionary-basics','sort-custom','optional-binding'], docs=[('Collection Types — Dictionaries', CT)],
 statement="""Lines are `"name score"` (a name may appear many times; ignore malformed lines or scores outside 0…100). Print one line per student, sorted by name: `"<name> avg=<average rounded to nearest int> best=<max> n=<count>"`, then a final line `"class avg=<rounded average of all valid scores>"` (or `"class avg=n/a"`).""",
 starter="var scores: [String: [Int]] = [:]\n",
 solution="""
 var scores: [String: [Int]] = [:]
 while let line = readLine() {
     let parts = line.split(separator: " ")
     guard parts.count == 2, let score = Int(parts[1]), (0...100).contains(score) else { continue }
     scores[String(parts[0]), default: []].append(score)
 }
 func roundedAverage(_ xs: [Int]) -> Int { Int((Double(xs.reduce(0, +)) / Double(xs.count)).rounded()) }
 for (name, list) in scores.sorted(by: { $0.key < $1.key }) {
     print("\\(name) avg=\\(roundedAverage(list)) best=\\(list.max()!) n=\\(list.count)")
 }
 let all = scores.values.flatMap { $0 }
 print("class avg=\\(all.isEmpty ? "n/a" : String(roundedAverage(all)))")
 """,
 explain="""Grouping with `dict[key, default: []].append(x)`, then **sorting the dictionary** gives deterministic output. `flatMap` concatenates every student's list. `.rounded()` uses schoolbook rounding (halves away from zero).""",
 tests=['ana 90\nbo 70\nana 81\nbo 101\nbad line\n', '', 'zed 50\nzed 51\n'], hidden=1))

write_all(P, 'advanced', 500)
