struct Todo: Identifiable, Equatable {
    let id: Int
    var title: String
    var isDone = false
}

func applyEdits(_ ops: [String]) -> [String] {
    var todos: [Todo] = []
    for op in ops {
        let p = op.split(separator: " ", maxSplits: 2).map(String.init)
        guard p.count >= 2, let id = Int(p[1]) else { continue }
        let index = todos.firstIndex { $0.id == id }
        switch (p[0], index) {
        case ("add", nil) where p.count == 3: todos.append(Todo(id: id, title: p[2]))
        case ("toggle", let i?): todos[i].isDone.toggle()
        case ("rename", let i?) where p.count == 3: todos[i].title = p[2]
        case ("delete", let i?): todos.remove(at: i)
        default: break
        }
    }
    return todos.map { "\($0.id):\($0.title):\($0.isDone ? "done" : "todo")" }
}
