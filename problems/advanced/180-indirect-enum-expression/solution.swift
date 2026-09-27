indirect enum Expr {
    case number(Int)
    case add(Expr, Expr)
    case multiply(Expr, Expr)
    case negate(Expr)

    func evaluate() -> Int {
        switch self {
        case .number(let n): n
        case let .add(a, b): a.evaluate() + b.evaluate()
        case let .multiply(a, b): a.evaluate() * b.evaluate()
        case .negate(let e): -e.evaluate()
        }
    }
}

func evaluateRPN(_ tokens: [String]) -> Int? {
    var stack: [Expr] = []
    for token in tokens {
        switch token {
        case "+", "*":
            guard let b = stack.popLast(), let a = stack.popLast() else { return nil }
            stack.append(token == "+" ? .add(a, b) : .multiply(a, b))
        case "neg":
            guard let e = stack.popLast() else { return nil }
            stack.append(.negate(e))
        default:
            guard let n = Int(token) else { return nil }
            stack.append(.number(n))
        }
    }
    return stack.count == 1 ? stack[0].evaluate() : nil
}
