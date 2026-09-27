struct __Input: Decodable { let ops: [String]; let args: [[Int]] }
func __run(_ __i: __Input) async throws -> [Int?] {
    var cache: LRUCache?
    var out: [Int?] = []
    for (op, a) in zip(__i.ops, __i.args) {
        switch op {
        case "init": cache = LRUCache(capacity: a[0]); out.append(nil)
        case "put": cache!.put(a[0], a[1]); out.append(nil)
        default: out.append(cache!.get(a[0]))
        }
    }
    return out
}
