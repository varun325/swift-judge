func squaredFirstNumber(_ csv: String?) -> Int? {
    csv
        .flatMap { $0.split(separator: ",", omittingEmptySubsequences: false).first }
        .flatMap { Int($0) }
        .map { $0 * $0 }
}
