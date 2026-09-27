struct __Input: Decodable { let values: [Int]; let extra: Int }
func __run(_ __i: __Input) async throws -> [[Int]] {
    let counter = CopyCounter()
    var a = COWArray(counter: counter)
    __i.values.forEach { a.append($0) }
    var b = a
    b.append(__i.extra)
    b.append(__i.extra + 1)
    return [a.items, b.items, [counter.copies]]
}
