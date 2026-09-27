func indexUsers(_ rows: [[String]]) -> [String: String] {
    Dictionary(rows.map { ($0[0], $0[1]) }, uniquingKeysWith: { old, new in
        old.split(separator: "|").contains(Substring(new)) ? old : old + "|" + new
    })
}
