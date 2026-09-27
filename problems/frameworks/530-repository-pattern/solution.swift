struct NotFound: Error {}

protocol ArticleRemote: Sendable {
    func fetch(_ id: Int) async throws -> String
}

actor MockRemote: ArticleRemote {
    private(set) var calls = 0
    func fetch(_ id: Int) async throws -> String {
        calls += 1
        if id == 0 { throw NotFound() }
        return "article \(id) v\(calls)"
    }
}

actor ArticleRepository {
    private let remote: any ArticleRemote
    private var cache: [Int: String] = [:]

    init(remote: any ArticleRemote) { self.remote = remote }

    func article(_ id: Int, forceRefresh: Bool) async -> Result<String, Error> {
        if !forceRefresh, let cached = cache[id] { return .success(cached) }
        do {
            let value = try await remote.fetch(id)
            cache[id] = value
            return .success(value)
        } catch {
            return .failure(error)
        }
    }
}

func repositoryDemo(_ requests: [String]) async -> [String] {
    let remote = MockRemote()
    let repo = ArticleRepository(remote: remote)
    var log: [String] = []
    for r in requests {
        let force = r.hasSuffix("!")
        let id = Int(r.replacingOccurrences(of: "!", with: "")) ?? 0
        switch await repo.article(id, forceRefresh: force) {
        case .success(let a): log.append(a)
        case .failure: log.append("err")
        }
    }
    log.append("remote calls \(await remote.calls)")
    return log
}

import Foundation
