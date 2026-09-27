import Combine

struct BadToken: Error {}

func parseStream(_ tokens: [String], recovery: String) -> [String] {
    var log: [String] = []
    let source = tokens.publisher
    let pipeline: AnyPublisher<Int, Never>
    switch recovery {
    case "replace":
        pipeline = source.tryMap { t -> Int in guard let n = Int(t) else { throw BadToken() }; return n }
            .replaceError(with: -1).eraseToAnyPublisher()
    case "catch":
        pipeline = source.tryMap { t -> Int in guard let n = Int(t) else { throw BadToken() }; return n }
            .catch { _ in Just(0) }.eraseToAnyPublisher()
    default:
        pipeline = source.flatMap { t in
            Just(t).tryMap { t -> Int in guard let n = Int(t) else { throw BadToken() }; return n }
                .replaceError(with: -1)
        }.eraseToAnyPublisher()
    }
    let c = pipeline.sink(receiveCompletion: { _ in log.append("done") }, receiveValue: { log.append(String($0)) })
    _ = c
    return log
}
