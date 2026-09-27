var handlers: [() -> Void] = []
for i in 1...3 {
    handlers.append { print("loop", i) }
}
var counter = 0
for _ in 1...3 {
    handlers.append { print("shared", counter) }
    counter += 1
}
let snapshot = { [counter] in print("snapshot", counter) }
counter = 100
handlers.forEach { $0() }
snapshot()
