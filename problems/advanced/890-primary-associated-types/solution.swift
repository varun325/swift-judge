func evens(in values: some Collection<Int>) -> [Int] {
    values.filter { $0.isMultiple(of: 2) }
}

func squares(_ values: [Int]) -> some Sequence<Int> {
    values.lazy.map { $0 * $0 }
}

func primaryDemo(_ values: [Int]) -> [Int] {
    let sources: [any Sequence<Int>] = [values, values.reversed(), squares(values)]
    return evens(in: values) + Array(squares(values)) + sources.map { $0.reduce(0, +) }
}
