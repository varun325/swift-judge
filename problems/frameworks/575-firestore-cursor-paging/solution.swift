struct Post { let id: String; let createdAt: Int }

func pagesByCursor(_ posts: [[String]], pageSize: Int) -> [String] {
    var all = posts.map { Post(id: $0[0], createdAt: Int($0[1]) ?? 0) }
    func sorted() -> [Post] { all.sorted { ($1.createdAt, $0.id) < ($0.createdAt, $1.id) } }
    func isAfter(_ p: Post, _ cursor: Post) -> Bool { (cursor.createdAt, p.id) < (p.createdAt, cursor.id) ? false : (p.createdAt < cursor.createdAt || (p.createdAt == cursor.createdAt && p.id > cursor.id)) }
    guard pageSize > 0 else { return ["end"] }
    var cursor: Post?
    var pages: [String] = []
    var inserted = false
    while true {
        let page = Array(sorted().filter { p in cursor.map { isAfter(p, $0) } ?? true }.prefix(pageSize))
        if page.isEmpty { break }
        pages.append(page.map(\.id).joined(separator: ","))
        cursor = page.last
        if !inserted {
            inserted = true
            all.append(Post(id: "new", createdAt: (all.map(\.createdAt).max() ?? 0) + 1))
        }
    }
    return pages + ["end"]
}
