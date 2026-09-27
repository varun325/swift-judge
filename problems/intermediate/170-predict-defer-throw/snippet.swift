struct Boom: Error {}

func work(_ fail: Bool) throws -> Int {
    print("start \(fail)")
    defer { print("cleanup A") }
    defer { print("cleanup B") }
    if fail { throw Boom() }
    print("finish")
    return 1
}

do {
    _ = try work(false)
    _ = try work(true)
    print("unreachable")
} catch {
    print("caught \(error)")
}
print(try? work(true) as Any)
