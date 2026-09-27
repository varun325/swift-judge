Nodes `0..<n`, directed `edges` `[from, to, weight]` (weights ≥ 0). Return the shortest distance from `source` to every node, `-1` if unreachable.

 A simple O(V²) version (pick the unvisited node with the smallest tentative distance each round) is fine here; bonus: reuse your `Heap` from the previous problem.
