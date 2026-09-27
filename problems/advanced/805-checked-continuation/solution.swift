enum LegacyError: Error { case notFound }

func legacyFetch(_ key: String, completion: @escaping @Sendable (Result<String, Error>) -> Void) {
    Thread.detachNewThread {
        completion(key.hasPrefix("x") ? .failure(LegacyError.notFound) : .success(key.uppercased()))
    }
}

import Foundation

func fetch(_ key: String) async throws -> String {
    try await withCheckedThrowingContinuation { continuation in
        legacyFetch(key) { result in
            continuation.resume(with: result)
        }
    }
}

func fetchAll(_ keys: [String]) async -> [String] {
    var out: [String] = []
    for key in keys {
        out.append((try? await fetch(key)) ?? "missing \(key)")
    }
    return out
}
