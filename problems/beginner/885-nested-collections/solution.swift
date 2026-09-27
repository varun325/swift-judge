func roster(_ enrolments: [[String]]) -> [String] {
    var classes: [String: Set<String>] = [:]
    for e in enrolments { classes[e[0], default: []].insert(e[1]) }
    let sorted = classes.map { (name: $0.key, students: $0.value.sorted()) }.sorted { $0.name < $1.name }
    var lines = sorted.map { "\($0.name): \($0.students.joined(separator: ", "))" }
    let largest = sorted.min { ($1.students.count, $0.name) < ($0.students.count, $1.name) }
    lines.append("largest: \(largest?.name ?? "none")")
    return lines
}
