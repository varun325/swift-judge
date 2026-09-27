final class Node {
    let name: String
    init(_ name: String) { self.name = name; print("init", name) }
    deinit { print("deinit", name) }
}

var a: Node? = Node("A")
var b = a
a = nil
print("a released")
b = Node("B")
print("b reassigned")
do {
    let c = Node("C")
    _ = c
    print("leaving scope")
}
b = nil
print("end")
