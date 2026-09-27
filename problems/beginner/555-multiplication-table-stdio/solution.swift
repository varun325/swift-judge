let parts = (readLine() ?? "").split(separator: " ").compactMap { Int($0) }
let n = parts[0], upTo = parts[1]
for i in stride(from: 1, through: upTo, by: 1) {
    print("\(n) x \(i) = \(n * i)")
}
