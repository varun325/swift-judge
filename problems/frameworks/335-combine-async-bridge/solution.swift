import Combine

func bridge(_ values: [Int], take: Int) async -> [Int] {
    let pipeline = values.publisher
        .filter { $0 > 0 }
        .map { $0 * 10 }
    var out: [Int] = []
    guard take > 0 else { return out }
    for await v in pipeline.values {
        out.append(v)
        if out.count >= take { break }
    }
    return out
}
