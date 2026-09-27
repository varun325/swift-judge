func podium(_ names: [String], _ times: [Double]) -> [String] {
    zip(names, times)
        .sorted { $0.1 < $1.1 }
        .prefix(3)
        .enumerated()
        .map { "\($0.offset + 1). \($0.element.0) (\($0.element.1)s)" }
}
