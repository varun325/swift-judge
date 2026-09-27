final class ListNode {
    var value: Int
    var next: ListNode?
    init(_ value: Int, next: ListNode? = nil) { self.value = value; self.next = next }
}

func build(_ values: [Int]) -> ListNode? {
    values.reversed().reduce(nil as ListNode?) { ListNode($1, next: $0) }
}

func reverse(_ head: ListNode?) -> ListNode? {
    var previous: ListNode? = nil
    var current = head
    while let node = current {
        current = node.next
        node.next = previous
        previous = node
    }
    return previous
}

func reverseList(_ values: [Int]) -> [Int] {
    var out: [Int] = []
    var node = reverse(build(values))
    while let n = node { out.append(n.value); node = n.next }
    return out
}
