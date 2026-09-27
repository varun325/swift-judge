func totalQuantity(_ lines: [String]) -> Int {
    var total = 0
    for line in lines {
        let colon = line.firstIndex(of: ":")!
        total += Int(line[line.index(after: colon)...])!
    }
    return total
}
