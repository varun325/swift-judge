let p = (readLine() ?? "").split(separator: " ").compactMap { Int($0) }
for c in stride(from: p[0], through: p[1], by: p[2]) {
    let f = (Double(c) * 9 / 5 + 32).rounded()
    print("\(c)°C = \(Int(f))°F")
}
