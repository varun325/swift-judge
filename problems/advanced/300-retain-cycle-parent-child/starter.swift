final class Log { var lines: [String] = [] }

final class Parent {
    let name: String, log: Log
    var children: [Child] = []
    init(_ name: String, log: Log) { self.name = name; self.log = log }
    deinit { log.lines.append("deinit \(name)") }
}

final class Child {
    let name: String, log: Log
    var parent: Parent?
    init(_ name: String, log: Log) { self.name = name; self.log = log }
    deinit { log.lines.append("deinit \(name)") }
}

func cycleDemo(_ childNames: [String]) -> [String] {
    let log = Log()
    do {
        let mom = Parent("mom", log: log)
        for n in childNames {
            let child = Child(n, log: log)
            child.parent = mom
            mom.children.append(child)
        }
    }
    log.lines.append("end")
    return log.lines
}
