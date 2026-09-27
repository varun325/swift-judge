struct __Input: Decodable { let capacity: Int; let values: [Int] }
func __run(_ __i: __Input) async throws -> [[Int]] {
    var buffer = RingBuffer<Int>(capacity: __i.capacity)
    __i.values.forEach { buffer.append($0) }
    return [Array(buffer), [buffer.first ?? -1], [buffer.count], [buffer.reduce(0, +)], Array(buffer.dropFirst())]
}
