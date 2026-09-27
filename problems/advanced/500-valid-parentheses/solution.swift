func isValid(_ s: String) -> Bool {
    let pairs: [Character: Character] = [")": "(", "]": "[", "}": "{"]
    var stack: [Character] = []
    for ch in s {
        if let open = pairs[ch] {
            guard stack.popLast() == open else { return false }
        } else {
            stack.append(ch)
        }
    }
    return stack.isEmpty
}
