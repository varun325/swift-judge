import Combine

final class SearchViewModel: ObservableObject {
    @Published var query = ""
    @Published private(set) var results: [String] = []
    private let all = ["apple", "apricot", "banana", "blueberry", "cherry"]

    init() {
        $query
            .map { $0.trimmingCharacters(in: .whitespaces).lowercased() }
            .removeDuplicates()
            .dropFirst()
            .map { [all] q in q.isEmpty ? all : all.filter { $0.hasPrefix(q) } }
            .assign(to: &$results)
    }
}

import Foundation

func searchPipeline(_ typed: [String]) -> [String] {
    let vm = SearchViewModel()
    return typed.map { text in
        vm.query = text
        return vm.results.joined(separator: ",")
    }
}
