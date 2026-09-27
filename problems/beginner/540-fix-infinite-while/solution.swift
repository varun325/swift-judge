func nonJpegsReversed(_ files: [String]) -> [String] {
    var result: [String] = []
    for file in files.reversed() where !file.hasSuffix(".jpeg") {
        result.append(file)
    }
    return result
}
