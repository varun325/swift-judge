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
