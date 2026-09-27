func totalQuantity(_ lines: [String]) -> Int {
    lines.reduce(0) { total, line in
        guard let colon = line.firstIndex(of: ":"),
              let qty = Int(line[line.index(after: colon)...]),
              qty >= 0 else { return total }
        return total + qty
    }
}
