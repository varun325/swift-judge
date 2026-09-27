func plan(route: [String], using describe: (String, Int) -> String) -> [String] {
    route.enumerated().map { describe($0.element, $0.offset + 1) }
}

func travel(_ legs: [String]) -> [String] {
    let verbose = plan(route: legs) { stop, number in
        "Leg \(number): to \(stop)"
    }
    let short = plan(route: legs) { "\($1)-\($0)" }
    return verbose + short
}
