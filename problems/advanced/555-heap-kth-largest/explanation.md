Storing the comparator as a closure lets one generic type be a min-heap (`<`) or max-heap (`>`) — operators are functions, so `Heap(by: <)` just works. Keeping only k elements makes it O(n log k).
