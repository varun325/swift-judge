func chunked(_ items: [String], size: Int) -> [[String]] {
    stride(from: 0, to: items.count, by: size).map {
        Array(items[$0 ..< min($0 + size, items.count)])
    }
}
