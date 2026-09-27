func diffRows(old: [[String]], new: [[String]]) -> [String] {
    let diff = new.map { $0[0] }.difference(from: old.map { $0[0] }).inferringMoves()
    var inserts: [String] = [], removes: [String] = [], moves: Set<String> = []
    for change in diff {
        switch change {
        case let .insert(_, id, associatedWith):
            if associatedWith != nil { moves.insert(id) } else { inserts.append(id) }
        case let .remove(_, id, associatedWith):
            if associatedWith != nil { moves.insert(id) } else { removes.append(id) }
        }
    }
    let oldTitles = Dictionary(old.map { ($0[0], $0[1]) }, uniquingKeysWith: { a, _ in a })
    let updates = new.filter { row in oldTitles[row[0]].map { $0 != row[1] } ?? false }.map { $0[0] }
    return inserts.sorted().map { "insert \($0)" }
        + removes.sorted().map { "remove \($0)" }
        + moves.sorted().map { "move \($0)" }
        + updates.sorted().map { "update \($0)" }
}
