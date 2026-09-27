import sys; sys.path.insert(0, '/private/tmp/claude-501/-Users-shrishti-Desktop-varun-notes/4fdb1b4a-c26d-41e1-9aeb-bcccc0343f8b/scratchpad/author')
from gen import write_all
TB='LanguageGuide/TheBasics'
B=[]
B.append(dict(id='typealias-grid', title='typealias for Readable Types', topic='Type inference', notes='10', concepts=['typealias','tuples'], docs=[('The Basics — Type Aliases', TB)],
 sig='func neighbours(_ grid: [[Int]], row: Int, col: Int) -> [Int]',
 statement="""Declare `typealias Grid = [[Int]]` and `typealias Cell = (row: Int, col: Int)`, then write `func cells(around c: Cell, in grid: Grid) -> [Cell]` returning the in-bounds 8-neighbours in reading order (row by row, left to right).

 `neighbours` returns the **values** at those cells.""",
 solution="""
 typealias Grid = [[Int]]
 typealias Cell = (row: Int, col: Int)

 func cells(around c: Cell, in grid: Grid) -> [Cell] {
     var result: [Cell] = []
     for dr in -1...1 {
         for dc in -1...1 where !(dr == 0 && dc == 0) {
             let r = c.row + dr, col = c.col + dc
             if grid.indices.contains(r), grid[r].indices.contains(col) { result.append((r, col)) }
         }
     }
     return result
 }

 func neighbours(_ grid: [[Int]], row: Int, col: Int) -> [Int] {
     cells(around: (row, col), in: grid).map { grid[$0.row][$0.col] }
 }
 """,
 explain="""A `typealias` is just another name — `Grid` **is** `[[Int]]`, so `neighbours` can pass its `[[Int]]` straight in. Aliases shine for tuple types and closure types (`typealias Handler = (Result<Data, Error>) -> Void`). For a genuinely distinct type, use a struct.""",
 tests=[({'grid':[[1,2,3],[4,5,6],[7,8,9]],'row':1,'col':1},[1,2,3,4,6,7,8,9]), {'grid':[[1,2,3],[4,5,6],[7,8,9]],'row':0,'col':0}, {'grid':[[5]],'row':0,'col':0}, {'grid':[[1,2],[3]],'row':1,'col':0}]))
B.append(dict(id='predict-nested-comments', title='Predict: Comments That Nest', topic='Constants & variables', mode='predict', notes='10', concepts=['comments'], docs=[('The Basics — Comments', TB)],
 statement="""Unlike C, Swift's block comments **nest**. Predict the output — which `print`s survive?""",
 snippet="""
 print("one")
 /* print("two")
    /* print("three") */
    print("four")
 */
 print("five") // print("six")
 /// Documentation comments are ignored at runtime too.
 print("seven" /* inline */, "eight")
 """,
 explain="""The outer `/* … */` contains an inner complete comment, so the first `*/` only closes the inner one — "four" stays commented out. In C, "four" would print (and the final `*/` would be a syntax error). Nesting lets you comment out code that already contains block comments."""))
write_all(B, 'beginner', 700)
I=[]
I.append(dict(id='fix-force-unwrap', title='Fix the Crash: Force Unwrapping', topic='Optionals', notes='25', concepts=['forced-unwrapping','optional-binding','nil-vs-null'], docs=[('The Basics — Forced Unwrapping', TB)],
 sig='func totalQuantity(_ lines: [String]) -> Int',
 statement="""Order lines look like `"apples:3"`. The starter force-unwraps everything and **crashes** on malformed lines (run it and read the runtime error). Rewrite it so malformed lines (missing `:`, non-integer or negative quantity) are **skipped**, with no `!` anywhere.""",
 starter="""
 func totalQuantity(_ lines: [String]) -> Int {
     var total = 0
     for line in lines {
         let colon = line.firstIndex(of: ":")!
         total += Int(line[line.index(after: colon)...])!
     }
     return total
 }
 """,
 solution="""
 func totalQuantity(_ lines: [String]) -> Int {
     lines.reduce(0) { total, line in
         guard let colon = line.firstIndex(of: ":"),
               let qty = Int(line[line.index(after: colon)...]),
               qty >= 0 else { return total }
         return total + qty
     }
 }
 """,
 explain="""`!` means "I promise this isn't nil — crash otherwise" (*Fatal error: Unexpectedly found nil while unwrapping an Optional value*). With data you don't control, bind with `guard let`/`if let` and handle the failure. Reserve `!` for genuine programmer errors.""",
 tests=[({'lines':['apples:3','pears:4']},7), ({'lines':['apples:3','broken','kiwis:x','figs:-2','nuts:5']},8), {'lines':[]}, {'lines':[':1','a::2','b:+3']}]))
write_all(I, 'intermediate', 700)
A_=[]
A_.append(dict(id='serial-queue-counter', title='GCD: A Serial Queue Guards State', topic='Concurrency', diff='medium', concepts=['dispatch-sync-async','actors','sendable'], docs=[('Dispatch','https://developer.apple.com/documentation/dispatch'),('Concurrency', 'LanguageGuide/Concurrency')],
 sig='func hammer(threads: Int, incrementsEach: Int) -> Int',
 statement="""Before actors, shared state was protected with a **serial** `DispatchQueue`. Write `final class SafeCounter: @unchecked Sendable` with a private `value` and a private serial queue; `increment()` uses `queue.sync { value += 1 }` and `var current: Int` reads with `queue.sync { value }`.

 `hammer` runs `DispatchQueue.concurrentPerform(iterations: threads)`, each iteration calling `increment()` `incrementsEach` times, and returns `current`. (Without the queue, increments would be lost — a data race.)""",
 solution="""
 import Dispatch

 final class SafeCounter: @unchecked Sendable {
     private var value = 0
     private let queue = DispatchQueue(label: "counter")   // serial by default

     func increment() { queue.sync { value += 1 } }
     var current: Int { queue.sync { value } }
 }

 func hammer(threads: Int, incrementsEach: Int) -> Int {
     let counter = SafeCounter()
     DispatchQueue.concurrentPerform(iterations: threads) { _ in
         for _ in 0..<incrementsEach { counter.increment() }
     }
     return counter.current
 }
 """,
 explain="""A serial queue runs one block at a time, so `sync` blocks make access mutually exclusive. `sync` waits for the block to finish (never call it on the queue you're already on — deadlock); `async` returns immediately. `@unchecked Sendable` tells Swift 6 "I've synchronised this myself" — you take responsibility. Actors do this for you, checked by the compiler.""",
 tests=[({'threads':4,'incrementsEach':1000},4000), {'threads':1,'incrementsEach':0}, {'threads':8,'incrementsEach':250}, {'threads':16,'incrementsEach':100}]))
write_all(A_, 'advanced', 700)
