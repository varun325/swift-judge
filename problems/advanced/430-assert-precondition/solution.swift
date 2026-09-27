func validatedAge(_ age: Int) -> Int {
    precondition(age >= 0, "age must be non-negative")
    return age
}

func checkedAges(_ ages: [Int]) -> [String] {
    let valid = ages.filter { $0 >= 0 }
    var out = valid.map { "ok \(validatedAge($0))" }
    out.append("rejected \(ages.count - valid.count)")
    assert(out.count == valid.count + 1, "one line per valid age plus the summary")
    return out
}
