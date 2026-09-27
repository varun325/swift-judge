func logged(_ message: String, function: String = #function, line: Int = #line) -> String {
    "[\(function):\(line)] \(message)"
}

struct Service {
    func start() -> String { logged("starting") }
}

print(#fileID)
print(Service().start())
print(logged("top level"))
print(#column > 0, #function)
