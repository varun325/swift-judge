struct Polynomial {
    let coefficients: [Int]
    func callAsFunction(_ x: Int) -> Int {
        coefficients.reduce(0) { $0 * x + $1 }
    }
}

@dynamicCallable
struct Joiner {
    let separator: String
    func dynamicallyCall(withArguments args: [String]) -> String {
        args.joined(separator: separator)
    }
}

func callablesDemo(_ values: [Int]) -> [String] {
    let p = Polynomial(coefficients: [2, 0, 1])
    let join = Joiner(separator: "-")
    return values.map { String(p($0)) } + [join("x", "y", "z")]
}
