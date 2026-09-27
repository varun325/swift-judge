protocol Report {
    var title: String { get }
    func rows() -> [String]
}

extension Report {
    func render() -> [String] {
        let body = rows()
        return ["== \(title) =="] + body + ["(\(body.count) rows)"]
    }
}

struct SalesReport: Report {
    let amounts: [Int]
    var title: String { "Sales" }
    func rows() -> [String] { amounts.map { "$\($0)" } }
}

struct TeamReport: Report {
    let headcounts: [Int]
    var title: String { "Team" }
    func rows() -> [String] { headcounts.enumerated().map { "team \($0.offset + 1): \($0.element)" } }
}

func report(_ sizes: [[Int]]) -> [String] {
    SalesReport(amounts: sizes[0]).render() + TeamReport(headcounts: sizes[1]).render()
}
