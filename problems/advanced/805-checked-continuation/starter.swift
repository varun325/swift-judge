enum LegacyError: Error { case notFound }

func legacyFetch(_ key: String, completion: @escaping @Sendable (Result<String, Error>) -> Void) {
    Thread.detachNewThread {
        completion(key.hasPrefix("x") ? .failure(LegacyError.notFound) : .success(key.uppercased()))
    }
}

import Foundation

func fetchAll(_ keys: [String]) async -> [String] {
    return []
}
