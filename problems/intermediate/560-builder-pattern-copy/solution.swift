struct Request {
    var method = "GET"
    var path = "/"
    var headers: [String: String] = [:]

    func method(_ m: String) -> Self { var copy = self; copy.method = m; return copy }
    func path(_ p: String) -> Self { var copy = self; copy.path = p; return copy }
    func header(_ k: String, _ v: String) -> Self { var copy = self; copy.headers[k] = v; return copy }

    var summary: String {
        "\(method) \(path) " + headers.sorted { $0.key < $1.key }.map { "\($0.key)=\($0.value)" }.joined(separator: ";")
    }
}

func requestDemo(_ steps: [String]) -> [String] {
    let base = Request()
    let built = steps.reduce(base) { req, step in
        let p = step.split(separator: " ").map(String.init)
        switch (p.first, p.count) {
        case ("method", 2): return req.method(p[1])
        case ("path", 2): return req.path(p[1])
        case ("header", 3): return req.header(p[1], p[2])
        default: return req
        }
    }
    return [base.summary, built.summary]
}
