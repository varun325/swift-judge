struct __Input: Decodable { let ops: [String] }
func __run(_ __i: __Input) async throws -> [Int?] {
    var q = TwoStackQueue<Int>()
    return __i.ops.map { op -> Int? in
        let parts = op.split(separator: " ")
        switch parts[0] {
        case "enqueue": q.enqueue(Int(parts[1])!); return nil
        case "dequeue": return q.dequeue()
        case "peek": return q.peek
        default: return q.count
        }
    }
}
