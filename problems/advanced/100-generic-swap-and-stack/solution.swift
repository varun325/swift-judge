struct Stack<Element> {
    private var items: [Element] = []
    var isEmpty: Bool { items.isEmpty }
    var peek: Element? { items.last }
    mutating func push(_ item: Element) { items.append(item) }
    mutating func pop() -> Element? { items.popLast() }
}

func stackDemo(_ ints: [Int], _ words: [String]) -> [String] {
    var a = Stack<Int>()
    var b = Stack<String>()
    ints.forEach { a.push($0) }
    words.forEach { b.push($0) }
    var out: [String] = []
    while let x = a.pop() { out.append(String(x)) }
    while let w = b.pop() { out.append(w) }
    return out
}
