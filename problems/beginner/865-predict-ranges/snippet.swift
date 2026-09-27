let names = ["Ana", "Bo", "Cy", "Di", "Ed"]
print(names[1...3])
print(names[..<2], names[3...])
print(Array(1..<1), (1...3).count, (0..<10).contains(10))
print(Array(stride(from: 0, to: 10, by: 4)), Array(stride(from: 3, through: 0, by: -1)))
print((1...5).reversed().map { $0 * $0 })
