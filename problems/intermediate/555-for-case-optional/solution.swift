func sumPresent(_ values: [Int?]) -> [Int] {
    var total = 0
    for case let x? in values { total += x }
    var nils = 0
    for v in values { if case .none = v { nils += 1 } }
    var big = 0
    for case let x? in values where x > 10 { big += x }
    return [total, nils, big]
}
