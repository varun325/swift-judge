Build a binary tree from LeetCode-style level order (`null` = missing child) into `indirect enum Tree { case empty; case node(Tree, Int, Tree) }`. Return `[inorder traversal, [max depth], [sum of leaves]]`.

 Hint: build an array of nodes by index with a queue, or construct recursively — but enums are immutable, so assemble children **before** parents (bottom-up).
