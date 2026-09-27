enum AgeError: Error { case notANumber, negative, unrealistic }

func parseAge(_ s: String) -> Result<Int, AgeError> {
    guard let n = Int(s) else { return .failure(.notANumber) }
    if n < 0 { return .failure(.negative) }
    if n > 150 { return .failure(.unrealistic) }
    return .success(n)
}

func parseAges(_ raw: [String]) -> [String] {
    let results = raw.map(parseAge)
    var lines = results.map { result in
        switch result {
        case .success(let age): "ok \(age)"
        case .failure(let error): "fail \(error)"
        }
    }
    lines.append("total \(results.compactMap { try? $0.get() }.reduce(0, +))")
    return lines
}
