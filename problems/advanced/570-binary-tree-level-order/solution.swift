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
