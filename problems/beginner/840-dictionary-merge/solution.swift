func mergeInventories(_ a: [String: Int], _ b: [String: Int]) -> [String: Int] {
    a.merging(b, uniquingKeysWith: +).filter { $0.value > 0 }
}
