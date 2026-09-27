Implement `final class LRUCache` with `init(capacity: Int)`, `func get(_ key: Int) -> Int` (`-1` if missing) and `func put(_ key: Int, _ value: Int)`, both **O(1)**, evicting the least-recently-used key when over capacity.

 Use a dictionary of key → node plus a doubly linked list of `final class Node`s (with `weak`/`unowned` or plain optional links — think about retain cycles). The judge drives it like LeetCode #146.
