func recursiveReverse(_ s: Substring) -> String {
    guard let first = s.first else { return "" }
    return recursiveReverse(s.dropFirst()) + String(first)
}

func reversals(_ s: String) -> [String] {
    let a = String(s.reversed())
    var b = ""
    for ch in s { b = String(ch) + b }
    let c = recursiveReverse(s[...])
    return [a, b, c, a == b && b == c ? "agree" : "differ"]
}
