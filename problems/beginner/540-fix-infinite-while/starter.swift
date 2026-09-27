func nonJpegsReversed(_ files: [String]) -> [String] {
    var result: [String] = []
    var i = files.count - 1
    while i >= 0 {
        if files[i].hasSuffix(".jpeg") {
            continue
        }
        result.append(files[i])
        i -= 1
    }
    return result
}
