func invert(_ grades: [String: String]) -> [String: [String]] {
    var result: [String: [String]] = [:]
    for (student, grade) in grades {
        result[grade, default: []].append(student)
    }
    return result.mapValues { $0.sorted() }
}
