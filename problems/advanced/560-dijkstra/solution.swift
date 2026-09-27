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
