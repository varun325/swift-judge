func sign(_ n: Int) -> String {
    switch n {
    case ..<0: "negative"
    case 0: "zero"
    default: "positive"
    }
}

func signs(_ nums: [Int]) -> [String] {
    nums.map(sign)
}
