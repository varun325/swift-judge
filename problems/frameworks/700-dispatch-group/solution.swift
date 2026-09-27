import Dispatch

final class Results: @unchecked Sendable {
    private var values: [Int] = []
    private let lock = DispatchQueue(label: "results.lock")
    func add(_ v: Int) { lock.sync { values.append(v) } }
    var all: [Int] { lock.sync { values } }
}

func gcdBatch(_ items: [Int]) -> [String] {
    let worker = DispatchQueue(label: "worker", attributes: .concurrent)
    let group = DispatchGroup()
    let results = Results()
    for item in items {
        group.enter()
        worker.async {
            results.add(item * item)
            group.leave()
        }
    }
    group.wait()
    return results.all.sorted().map(String.init) + ["items \(items.count)"]
}
