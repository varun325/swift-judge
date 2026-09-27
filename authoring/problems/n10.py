import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
SW='https://developer.apple.com/documentation/swift/'
TSPL='https://docs.swift.org/swift-book/documentation/the-swift-programming-language/'
P=[]
T='Interview coding challenges'
P.append(dict(id='missing-number', title='Missing Number', topic=T, concepts=['map-filter-reduce','integer-overflow'], docs=[('Array', SW+'array')],
 sig='func missingNumber(_ nums: [Int]) -> Int',
 statement="""`nums` contains `n` distinct numbers from `0...n` — exactly one is missing. Find it in O(n) time and O(1) extra space. Try two ways: the sum formula, and XOR (which can't overflow).""",
 solution="func missingNumber(_ nums: [Int]) -> Int {\n    nums.enumerated().reduce(nums.count) { $0 ^ $1.offset ^ $1.element }\n}\n",
 explain="""XOR-ing every index and every value cancels pairs (`x ^ x == 0`), leaving the missing number — no overflow risk. The sum approach (`n(n+1)/2 − Σ`) is equally O(n) but can overflow for huge `n`.""",
 hints=("The expected sum of `0...n` is known in closed form.","`x ^ x == 0` and `x ^ 0 == x` — XOR indices and values together.","`nums.enumerated().reduce(nums.count) { $0 ^ $1.offset ^ $1.element }`."),
 tests=[({'nums':[3,0,1]},2), ({'nums':[0]},1), {'nums':[1]}, {'nums':[9,6,4,2,3,5,7,0,1]}]))
P.append(dict(id='string-compression', title='String Compression (Run-Length Encoding)', topic=T, concepts=['strings-are-collections','algorithms-chunked-by' if False else 'map-filter-reduce'], docs=[('String', SW+'string')],
 sig='func compress(_ s: String) -> String',
 statement="""Compress runs of repeated characters: `"aaabccdddd"` → `"a3b1c2d4"`. If the result isn't **shorter** than the input, return the input unchanged. Works on `Character`s (emoji count as one).""",
 solution="""
 func compress(_ s: String) -> String {
     var out = ""
     var previous: Character?
     var count = 0
     for ch in s {
         if ch == previous {
             count += 1
         } else {
             if let p = previous { out += "\\(p)\\(count)" }
             previous = ch
             count = 1
         }
     }
     if let p = previous { out += "\\(p)\\(count)" }
     return out.count < s.count ? out : s
 }
 """,
 explain="""A single pass tracking the current run is O(n). Comparing `Character`s (not bytes) keeps multi-scalar characters intact. The "only if shorter" rule is the usual interview twist.""",
 hints=("Walk the string remembering the current character and how many times it repeated.","When the character changes, append the previous run and reset.","Return the original string if compression doesn't make it shorter."),
 tests=[({'s':'aaabccdddd'},'a3b1c2d4'), ({'s':'abc'},'abc'), {'s':''}, {'s':'🍎🍎🍎🍎'}, {'s':'aabb'}]))
P.append(dict(id='max-profit-stock', title='Best Time to Buy and Sell', topic=T, concepts=['map-filter-reduce','tuples'], docs=[('Sequence.reduce(_:_:)', SW+'sequence/reduce(_:_:)')],
 sig='func maxProfit(_ prices: [Int]) -> Int',
 statement="""Buy once, sell once later. Return the maximum profit (0 if no profit is possible), in one pass.""",
 solution="""
 func maxProfit(_ prices: [Int]) -> Int {
     prices.reduce((minPrice: Int.max, best: 0)) { acc, price in
         (min(acc.minPrice, price), max(acc.best, price - min(acc.minPrice, price)))
     }.best
 }
 """,
 explain="""Track the cheapest price so far and the best profit so far — O(n), O(1). Using a labelled tuple as the `reduce` accumulator keeps both running values together.""",
 hints=("For each day, the best sale today is `price − cheapest price so far`.","Keep two running values: minimum price and best profit.","A `reduce` over a `(minPrice, best)` tuple does it in one line."),
 tests=[({'prices':[7,1,5,3,6,4]},5), ({'prices':[7,6,4,3,1]},0), {'prices':[]}, {'prices':[2,4,1,7]}]))
P.append(dict(id='majority-element', title='Majority Element (Boyer–Moore Voting)', topic=T, diff='medium', concepts=['map-filter-reduce','optionals'], docs=[('Sequence.reduce(_:_:)', SW+'sequence/reduce(_:_:)')],
 sig='func majority(_ nums: [Int]) -> Int?',
 statement="""Return the element that appears **more than n/2 times**, or `nil` if there isn't one. Use Boyer–Moore voting (O(1) space), then verify the candidate with a second pass.""",
 solution="""
 func majority(_ nums: [Int]) -> Int? {
     var candidate: Int?
     var votes = 0
     for n in nums {
         if votes == 0 { candidate = n }
         votes += n == candidate ? 1 : -1
     }
     guard let c = candidate, nums.count(where: { $0 == c }) * 2 > nums.count else { return nil }
     return c
 }
 """,
 explain="""Pairing each non-candidate with a candidate vote cancels them out; a true majority always survives. The verification pass is needed because the algorithm always produces *some* candidate, even when no majority exists.""",
 hints=("Keep a candidate and a vote count; a zero count means pick a new candidate.","Increment for matches, decrement otherwise.","Verify the survivor actually appears more than n/2 times."),
 tests=[({'nums':[2,2,1,1,1,2,2]},2), ({'nums':[1,2,3]},None), {'nums':[]}, {'nums':[5]}, {'nums':[1,1,2,2]}]))
P.append(dict(id='spiral-matrix', title='Spiral Order Traversal', topic=T, diff='medium', concepts=['array-basics','control-flow'], docs=[('Array', SW+'array')],
 sig='func spiral(_ matrix: [[Int]]) -> [Int]',
 statement="""Return the elements of an `m × n` matrix in clockwise spiral order, shrinking four boundaries (`top`, `bottom`, `left`, `right`) as you go.""",
 solution="""
 func spiral(_ matrix: [[Int]]) -> [Int] {
     guard !matrix.isEmpty, !matrix[0].isEmpty else { return [] }
     var top = 0, bottom = matrix.count - 1, left = 0, right = matrix[0].count - 1
     var out: [Int] = []
     while top <= bottom && left <= right {
         for c in stride(from: left, through: right, by: 1) { out.append(matrix[top][c]) }
         top += 1
         for r in stride(from: top, through: bottom, by: 1) { out.append(matrix[r][right]) }
         right -= 1
         if top <= bottom {
             for c in stride(from: right, through: left, by: -1) { out.append(matrix[bottom][c]) }
             bottom -= 1
         }
         if left <= right {
             for r in stride(from: bottom, through: top, by: -1) { out.append(matrix[r][left]) }
             left += 1
         }
     }
     return out
 }
 """,
 explain="""Four shrinking boundaries avoid a `visited` matrix. `stride(from:through:by:)` is empty when the range is inverted, and the two `if` checks stop single rows/columns from being read twice.""",
 hints=("Maintain four boundaries and shrink one after each side of the spiral.","Right along the top, down the right, left along the bottom, up the left.","Guard the bottom and left passes so a single remaining row or column isn't repeated."),
 tests=[({'matrix':[[1,2,3],[4,5,6],[7,8,9]]},[1,2,3,6,9,8,7,4,5]), {'matrix':[]}, {'matrix':[[1,2,3,4]]}, {'matrix':[[1],[2],[3]]}, {'matrix':[[1,2],[3,4],[5,6]]}]))
P.append(dict(id='array-intersection-counts', title='Intersection with Multiplicity', topic=T, concepts=['dictionary-basics','set-vs-array'], docs=[('Dictionary', SW+'dictionary')],
 sig='func intersect(_ a: [Int], _ b: [Int]) -> [Int]',
 statement="""Return the intersection of two arrays **including duplicates** (each element as many times as it appears in both), in the order it appears in `b`. `Set` intersection would lose the duplicates — use a count dictionary.""",
 solution="""
 func intersect(_ a: [Int], _ b: [Int]) -> [Int] {
     var counts = a.reduce(into: [Int: Int]()) { $0[$1, default: 0] += 1 }
     return b.filter { n in
         guard let c = counts[n], c > 0 else { return false }
         counts[n] = c - 1
         return true
     }
 }
 """,
 explain="""A `Set` answers "is it present?"; a count dictionary (a multiset) answers "how many are left?". Consuming counts as you go handles duplicates correctly in O(n + m).""",
 hints=("A set loses duplicates; count occurrences instead.","Build counts for `a`, then walk `b`, consuming a count each time you keep an element.","`b.filter { … }` with a mutable counts dictionary captured by the closure."),
 tests=[({'a':[1,2,2,1],'b':[2,2]},[2,2]), ({'a':[4,9,5],'b':[9,4,9,8,4]},[9,4]), {'a':[],'b':[1]}, {'a':[1,1,1],'b':[1,1]}]))
P.append(dict(id='dedupe-sorted-inplace', title='Remove Duplicates from Sorted Array (In Place)', topic=T, concepts=['inout','array-basics'], docs=[('In-Out Parameters', TSPL+'functions#In-Out-Parameters')],
 sig='func dedupeSorted(_ nums: inout [Int])',
 statement="""`nums` is sorted. Remove duplicates **in place** with a read/write two-pointer pass (no extra array), then truncate the array to the unique prefix.""",
 solution="""
 func dedupeSorted(_ nums: inout [Int]) {
     guard !nums.isEmpty else { return }
     var write = 1
     for read in 1..<nums.count where nums[read] != nums[write - 1] {
         nums[write] = nums[read]
         write += 1
     }
     nums.removeLast(nums.count - write)
 }
 """,
 explain="""Two pointers over a sorted array: the writer marks the end of the unique prefix. `removeLast(k)` trims in place. Because arrays are values, `inout` is how you get in-place mutation of the caller's array.""",
 hints=("In a sorted array, duplicates are adjacent.","Keep a write index; copy an element forward only when it differs from the last written one.","Trim the tail with `removeLast(nums.count - write)`."),
 tests=[({'nums':[1,1,2]},[1,2]), ({'nums':[0,0,1,1,1,2,2,3,3,4]},[0,1,2,3,4]), {'nums':[]}, {'nums':[7,7,7]}]))
P.append(dict(id='linked-list-reverse', title='Reverse a Linked List (Class Nodes)', topic=T, diff='medium', concepts=['class-definition','optionals','value-vs-reference'], docs=[('Classes and Structures', TSPL+'classesandstructures')],
 sig='func reverseList(_ values: [Int]) -> [Int]',
 statement="""Build a singly linked list with `final class ListNode { var value: Int; var next: ListNode? }`, reverse it **iteratively** by re-pointing `next` references (no new nodes, no arrays), then read it back into an array.""",
 solution="""
 final class ListNode {
     var value: Int
     var next: ListNode?
     init(_ value: Int, next: ListNode? = nil) { self.value = value; self.next = next }
 }

 func build(_ values: [Int]) -> ListNode? {
     values.reversed().reduce(nil as ListNode?) { ListNode($1, next: $0) }
 }

 func reverse(_ head: ListNode?) -> ListNode? {
     var previous: ListNode? = nil
     var current = head
     while let node = current {
         current = node.next
         node.next = previous
         previous = node
     }
     return previous
 }

 func reverseList(_ values: [Int]) -> [Int] {
     var out: [Int] = []
     var node = reverse(build(values))
     while let n = node { out.append(n.value); node = n.next }
     return out
 }
 """,
 explain="""Nodes are **classes** because list nodes need identity and shared references. `while let node = current` walks optionals safely; three pointers (`previous`, `current`, `next`) flip links in O(n) time, O(1) space. (Very long lists of strong `next` references can overflow the stack when ARC deallocates them recursively — real code often breaks them iteratively.)""",
 hints=("Walk the list keeping `previous` and `current`.","Save `current.next`, point `current.next` at `previous`, then advance both.","The new head is the last `previous`."),
 tests=[({'values':[1,2,3,4]},[4,3,2,1]), {'values':[]}, {'values':[9]}]))
P.append(dict(id='linked-list-cycle', title="Detect a Cycle (Floyd's Tortoise & Hare)", topic=T, diff='medium', concepts=['class-definition','equality-vs-identity','retain-cycle'], docs=[('Identity Operators', TSPL+'classesandstructures#Identity-Operators')],
 sig='func hasCycle(_ values: [Int], loopTo: Int) -> [String]',
 statement="""Build a list from `values`; if `loopTo >= 0`, point the last node's `next` back at node `loopTo` (creating a cycle). Detect the cycle with slow/fast pointers compared by **identity** (`===`), and if found also return the index where the cycle starts. Return `["cycle at <i>"]` or `["no cycle"]`. Break the cycle before returning so the nodes can be freed.""",
 solution="""
 final class Node {
     let value: Int
     var next: Node?
     init(_ value: Int) { self.value = value }
 }

 func hasCycle(_ values: [Int], loopTo: Int) -> [String] {
     let nodes = values.map(Node.init)
     for (a, b) in zip(nodes, nodes.dropFirst()) { a.next = b }
     if loopTo >= 0, loopTo < nodes.count { nodes.last?.next = nodes[loopTo] }
     defer { nodes.last?.next = nil }   // break the strong reference cycle so ARC can free the nodes

     var slow = nodes.first, fast = nodes.first
     while let f = fast?.next?.next, let s = slow?.next {
         slow = s
         fast = f
         if s === f {
             var start = nodes.first
             var meet: Node? = s
             while start !== meet { start = start?.next; meet = meet?.next }
             return ["cycle at \\(nodes.firstIndex { $0 === start } ?? -1)"]
         }
     }
     return ["no cycle"]
 }
 """,
 explain="""`===` compares object identity — two different nodes with equal values aren't the same node. A cyclic list is also a **retain cycle**: ARC can't free it until you break a link, which is why the `defer` sets `next = nil`. Floyd's second phase (restart one pointer at the head) finds the loop's entry.""",
 hints=("Move one pointer by one step and another by two; if they ever meet (by `===`), there's a cycle.","To find the start, reset one pointer to the head and advance both one step at a time.","Break the cycle before returning so ARC can deallocate the nodes."),
 tests=[({'values':[3,2,0,-4],'loopTo':1},['cycle at 1']), ({'values':[1,2],'loopTo':-1},['no cycle']), {'values':[],'loopTo':0}, {'values':[5],'loopTo':0}, {'values':[1,2,3,4,5,6],'loopTo':3}]))
P.append(dict(id='validate-bst', title='Validate a Binary Search Tree', topic=T, diff='medium', concepts=['class-definition','optionals','generics'], docs=[('Optional', SW+'optional')],
 sig='func isValidBST(_ levelOrder: [Int?]) -> Bool',
 statement="""Build a binary tree of class nodes from LeetCode-style level order (`null` = missing), then check the BST property recursively with **optional bounds**: every node must be strictly between `low` and `high` inherited from its ancestors (not just greater than its direct parent's left child!).""",
 solution="""
 final class TreeNode {
     let value: Int
     var left: TreeNode?
     var right: TreeNode?
     init(_ value: Int) { self.value = value }
 }

 func buildTree(_ values: [Int?]) -> TreeNode? {
     guard let first = values.first, let rootValue = first else { return nil }
     let root = TreeNode(rootValue)
     var queue = [root]
     var i = 1
     while !queue.isEmpty && i < values.count {
         let node = queue.removeFirst()
         if i < values.count, let v = values[i] { node.left = TreeNode(v); queue.append(node.left!) }
         i += 1
         if i < values.count, let v = values[i] { node.right = TreeNode(v); queue.append(node.right!) }
         i += 1
     }
     return root
 }

 func isValid(_ node: TreeNode?, low: Int?, high: Int?) -> Bool {
     guard let node else { return true }
     if let low, node.value <= low { return false }
     if let high, node.value >= high { return false }
     return isValid(node.left, low: low, high: node.value) && isValid(node.right, low: node.value, high: high)
 }

 func isValidBST(_ levelOrder: [Int?]) -> Bool {
     isValid(buildTree(levelOrder), low: nil, high: nil)
 }
 """,
 explain="""The classic trap: checking only `left < parent < right` misses a deep node that violates an ancestor's bound. Passing optional `low`/`high` (nil = unbounded) down the recursion fixes it — and avoids the `Int.min`/`Int.max` sentinel bug.""",
 hints=("Each node must satisfy bounds from *all* its ancestors, not just its parent.","Recurse with `(low, high)`: going left tightens `high`, going right tightens `low`.","Use optionals for \"no bound\" instead of `Int.min`/`Int.max`."),
 tests=[({'levelOrder':[2,1,3]},True), ({'levelOrder':[5,1,4,None,None,3,6]},False), ({'levelOrder':[5,4,6,None,None,3,7]},False), {'levelOrder':[]}, {'levelOrder':[2,2,2]}, {'levelOrder':[-9223372036854775808,None,9223372036854775807]}]))
P.append(dict(id='throttle-events', title='Throttle & Debounce (Event Timing)', topic=T, diff='medium', concepts=['closures','higher-order-functions'], docs=[('Combine: debounce', 'https://developer.apple.com/documentation/combine/publisher/debounce(for:scheduler:options:)'), ('Combine: throttle', 'https://developer.apple.com/documentation/combine/publisher/throttle(for:scheduler:latest:)')],
 sig='func timing(_ times: [Int], interval: Int, mode: String) -> [Int]',
 statement="""A search field fires events at the given timestamps (ms, ascending). Return the timestamps at which the handler actually **runs**:
 - `throttle` (leading edge): run on an event if at least `interval` ms have passed since the last *run*
 - `debounce` (trailing edge): run `interval` ms after an event that isn't followed by another event within `interval` — report the run time

 These are the semantics behind Combine's `throttle(latest: false)` and `debounce`.""",
 solution="""
 func timing(_ times: [Int], interval: Int, mode: String) -> [Int] {
     if mode == "throttle" {
         var runs: [Int] = []
         for t in times where runs.last.map({ t - $0 >= interval }) ?? true { runs.append(t) }
         return runs
     }
     return times.indices.compactMap { i in
         let quietAfter = i == times.count - 1 || times[i + 1] - times[i] >= interval
         return quietAfter ? times[i] + interval : nil
     }
 }
 """,
 explain="""**Throttle** limits the rate (first event wins, then a cooldown) — good for scroll handlers. **Debounce** waits for silence (last event wins) — good for search-as-you-type. In Combine you'd write `$query.debounce(for: .milliseconds(300), scheduler: RunLoop.main)`.""",
 hints=("Throttle: remember the last run time and skip events inside the cooldown.","Debounce: an event runs only if the next event is at least `interval` later (or there is none).","Debounced runs happen at `event time + interval`."),
 tests=[({'times':[0,50,120,130,400],'interval':100,'mode':'throttle'},[0,120,400]), ({'times':[0,50,120,130,400],'interval':100,'mode':'debounce'},[230,500]), {'times':[],'interval':10,'mode':'debounce'}, {'times':[5],'interval':0,'mode':'throttle'}]))
P.append(dict(id='flatten-nested', title='Flatten Arbitrarily Nested Lists', topic=T, diff='medium', concepts=['indirect-enums','codable','pattern-matching'], docs=[('Enumerations — Recursive Enumerations', TSPL+'enumerations#Recursive-Enumerations')],
 sig='func flatten(_ json: String) -> [Int]',
 statement="""Decode JSON like `[1, [2, [3, 4]], [], 5]` into `indirect enum Nested: Decodable { case value(Int), list([Nested]) }` (try `Int` first, then `[Nested]`, via a single-value container), then flatten it recursively. Invalid JSON → `[]`.""",
 solution="""
 import Foundation

 indirect enum Nested: Decodable {
     case value(Int)
     case list([Nested])

     init(from decoder: Decoder) throws {
         let c = try decoder.singleValueContainer()
         if let v = try? c.decode(Int.self) { self = .value(v) }
         else { self = .list(try c.decode([Nested].self)) }
     }

     var flattened: [Int] {
         switch self {
         case .value(let v): [v]
         case .list(let items): items.flatMap(\\.flattened)
         }
     }
 }

 func flatten(_ json: String) -> [Int] {
     (try? JSONDecoder().decode(Nested.self, from: Data(json.utf8)))?.flattened ?? []
 }
 """,
 explain="""JavaScript would just recurse over `any`; Swift makes the shape explicit with a recursive enum. A single-value container can try several types in turn, and `flatMap(\\.flattened)` does the recursion.""",
 hints=("Model \"a number or a list of these\" as an `indirect enum`.","In `init(from:)`, try decoding an `Int`, else decode `[Nested]`.","Flatten recursively with `flatMap`."),
 tests=[({'json':'[1,[2,[3,4]],[],5]'},[1,2,3,4,5]), {'json':'[]'}, {'json':'7'}, {'json':'[[[[]]]]'}, {'json':'nope'}]))
P.append(dict(id='reverse-string-ways', title='Reverse a String Three Ways', topic=T, concepts=['strings-are-collections','functions-basics'], docs=[('String', SW+'string')],
 sig='func reversals(_ s: String) -> [String]',
 statement="""Return the reversed string computed three ways, which must all agree: (1) `String(s.reversed())`, (2) a manual loop prepending characters, (3) recursion on `dropFirst()`. Then append `"agree"` or `"differ"`. Use `Character`s so `"🇮🇳ab"` reverses to `"ba🇮🇳"`, not broken flag halves.""",
 solution="""
 func recursiveReverse(_ s: Substring) -> String {
     guard let first = s.first else { return "" }
     return recursiveReverse(s.dropFirst()) + String(first)
 }

 func reversals(_ s: String) -> [String] {
     let a = String(s.reversed())
     var b = ""
     for ch in s { b = String(ch) + b }
     let c = recursiveReverse(s[...])
     return [a, b, c, a == b && b == c ? "agree" : "differ"]
 }
 """,
 explain="""Reversing by `Character` keeps grapheme clusters intact; reversing UTF-16 units (as naive JavaScript `split('').reverse()` does) breaks emoji. The recursive version works on `Substring`s so `dropFirst()` doesn't copy.""",
 hints=("`reversed()` works on `Character`s.","Prepending each character also reverses: `b = String(ch) + b`.","Recurse on `s.dropFirst()` (a `Substring`) and append the first character."),
 tests=[({'s':'🇮🇳ab'},['ba🇮🇳','ba🇮🇳','ba🇮🇳','agree']), {'s':''}, {'s':'swift'}]))
T2='Swift evolution'
P.append(dict(id='inline-array', title='InlineArray: Fixed-Size, No Heap', topic=T2, diff='medium', concepts=['memory-layout','generics','value-semantics'], docs=[('InlineArray', SW+'inlinearray'), ('SE-0453: InlineArray', 'https://github.com/swiftlang/swift-evolution/blob/main/proposals/0453-vector.md')],
 sig='func inlineDemo(_ values: [Int]) -> [Int]',
 statement="""Swift 6.2 adds `InlineArray<let count: Int, Element>` — a fixed-size array stored **inline** (no heap allocation, no copy-on-write). Copy the first four values (pad with 0) into `var board: InlineArray<4, Int>`, double each element in place, copy it to `var copy = board`, set `copy[0] = -1`, and return `[sum of board, board[0], copy[0], MemoryLayout<InlineArray<4, Int>>.size]`.""",
 solution="""
 func inlineDemo(_ values: [Int]) -> [Int] {
     var board = InlineArray<4, Int>(repeating: 0)
     for i in board.indices where i < values.count { board[i] = values[i] }
     for i in board.indices { board[i] *= 2 }
     var copy = board
     copy[0] = -1
     var sum = 0
     for i in board.indices { sum += board[i] }
     return [sum, board[0], copy[0], MemoryLayout<InlineArray<4, Int>>.size]
 }
 """,
 explain="""`InlineArray`'s size is part of its **type** (`let count` generic parameter), so it lives directly inside its container — 4 × 8 = 32 bytes, no pointer, no refcount. Copies are real copies. Use it for small fixed buffers in performance-sensitive code; `Array` remains the default.""",
 hints=("The count is part of the type: `InlineArray<4, Int>`.","Initialise with `InlineArray<4, Int>(repeating: 0)` and index like an array.","`MemoryLayout<InlineArray<4, Int>>.size` is the full inline size."),
 tests=[({'values':[1,2,3,4,5]},[20,2,-1,32]), {'values':[]}, {'values':[7]}]))
P.append(dict(id='span-safe-views', title='Span: Safe, Non-Escaping Memory Views', topic=T2, diff='hard', concepts=['ownership','memory-safety','generics'], docs=[('Span', SW+'span'), ('SE-0447: Span', 'https://github.com/swiftlang/swift-evolution/blob/main/proposals/0447-span-access-shared-contiguous-storage.md')],
 sig='func spanStats(_ values: [Int]) -> [Int]',
 statement="""Swift 6.2's `Span<Element>` is a safe view over contiguous memory: bounds-checked, **non-escapable** (can't outlive the storage), and zero-copy. Write `func sum(_ s: Span<Int>) -> Int` and `func maxRun(_ s: Span<Int>) -> Int` (longest run of equal adjacent values), and call both with `values.span`. Return `[sum, maxRun, span.count]`.""",
 solution="""
 func sum(_ s: Span<Int>) -> Int {
     var total = 0
     for i in s.indices { total += s[i] }
     return total
 }

 func maxRun(_ s: Span<Int>) -> Int {
     guard !s.isEmpty else { return 0 }
     var best = 1, current = 1
     for i in 1..<s.count {
         current = s[i] == s[i - 1] ? current + 1 : 1
         best = max(best, current)
     }
     return best
 }

 func spanStats(_ values: [Int]) -> [Int] {
     let span = values.span
     return [sum(span), maxRun(span), span.count]
 }
 """,
 explain="""`Span` replaces `UnsafeBufferPointer` for most read-only access: same speed, but the compiler proves it can't be used after the array is freed (it's `~Escapable`), and indexing is bounds-checked. APIs taking `Span` accept arrays, `InlineArray`s and other contiguous storage without copying.""",
 hints=("`values.span` gives a `Span<Int>` view without copying.","Index it like an array inside the functions; it can't be stored or returned.","Track the current and best run lengths in one pass."),
 tests=[({'values':[1,1,2,2,2,3]},[11,3,6]), {'values':[]}, {'values':[5]}]))
P.append(dict(id='raw-identifiers', title='Raw Identifiers with Backticks', topic=T2, mode='predict', concepts=['functions-basics','enums'], docs=[('SE-0451: Raw identifiers', 'https://github.com/swiftlang/swift-evolution/blob/main/proposals/0451-escaped-identifiers.md')],
 statement="""Swift 6.2 allows almost any text inside backticks as an identifier — handy for test names and enum cases that start with digits. Predict the output.""",
 snippet="""
 enum HTTPVersion: String {
     case `1.1` = "HTTP/1.1"
     case `2` = "HTTP/2"
 }

 func `formats a price with currency symbol`() -> String { "$4.99" }
 let `class` = "keywords always needed backticks"

 print(HTTPVersion.`2`.rawValue, HTTPVersion.`1.1`)
 print(`formats a price with currency symbol`())
 print(`class`)
 """,
 explain="""Backticks have long let you use keywords as names (`` `class` ``); SE-0451 extends them to spaces, digits-first names and more. The main use is readable test names — `@Test func `adds two numbers`()` — and enum cases mirroring external identifiers like versions.""",
 hints=("Backticked names are ordinary identifiers once declared.","Interpolating an enum case prints its (backticked) name without backticks.","The first line prints the raw value of `` `2` `` and the case name of `` `1.1` ``.")))
P.append(dict(id='int128', title='Int128 & Overflow Headroom', topic=T2, concepts=['integer-overflow','fundamental-types'], docs=[('Int128', SW+'int128')],
 sig='func factorials(_ ns: [Int]) -> [String]',
 statement="""`Int` overflows at 20!. Swift 6 adds `Int128`/`UInt128`. Compute n! for each n using `Int128` with **overflow detection** (`multipliedReportingOverflow`), returning the value as a string or `"overflow"`.""",
 solution="""
 func factorials(_ ns: [Int]) -> [String] {
     ns.map { n in
         guard n >= 0 else { return "undefined" }
         var result: Int128 = 1
         for k in stride(from: 2, through: n, by: 1) {
             let (value, overflow) = result.multipliedReportingOverflow(by: Int128(k))
             if overflow { return "overflow" }
             result = value
         }
         return String(result)
     }
 }
 """,
 explain="""`Int128` doubles the range (≈1.7 × 10³⁸), enough for 33! but not 35!. Overflow still **traps** by default; the `…ReportingOverflow` methods let you detect it. For truly unbounded integers you need a big-integer library — Swift has no built-in `BigInt` (unlike JavaScript's `BigInt`).""",
 hints=("Use `Int128` as the accumulator.","`multipliedReportingOverflow(by:)` returns the product and an overflow flag.","Negative inputs have no factorial."),
 tests=[({'ns':[0,5,20,21,33,34]},None), {'ns':[-1]}]))
P[-1]['tests'] = [{'ns':[0,5,20,21,33,34]}, {'ns':[-1]}]
write_all(P, 'advanced', 1000)
