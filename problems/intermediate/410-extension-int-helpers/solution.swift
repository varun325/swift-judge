extension Int {
    var isPrime: Bool {
        guard self >= 2 else { return false }
        var d = 2
        while d * d <= self {
            if self % d == 0 { return false }
            d += 1
        }
        return true
    }

    var digits: [Int] {
        String(magnitude).compactMap(\.wholeNumberValue)
    }

    func times(_ action: () -> Void) {
        guard self > 0 else { return }
        for _ in 0..<self { action() }
    }
}

func intFacts(_ nums: [Int]) -> [String] {
    nums.map { n in
        var ticks = 0
        n.times { ticks += 1 }
        return "\(n): prime=\(n.isPrime) digits=\(n.digits) ticks=\(ticks)"
    }
}
