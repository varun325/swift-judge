infix operator >>> : AdditionPrecedence

func >>> <A, B, C>(f: @escaping (A) -> B, g: @escaping (B) -> C) -> (A) -> C {
    { g(f($0)) }
}

func double(_ x: Int) -> Int { x * 2 }
func increment(_ x: Int) -> Int { x + 1 }
func describe(_ x: Int) -> String { "#\(x)" }

func pipeline(_ values: [Int]) -> [String] {
    let transform = double >>> increment >>> describe
    return values.map(transform)
}
