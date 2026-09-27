func resolvePort(env: [String: String], args: [String: String]) -> Int {
    args["port"].flatMap { Int($0) } ?? env["PORT"].flatMap { Int($0) } ?? 8080
}
