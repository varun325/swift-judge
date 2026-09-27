@MainActor
final class ViewModel {
    var items: [String] = []

    nonisolated static func transform(_ s: String) async -> String { s.uppercased() }

    func load(_ names: [String]) async {
        for name in names {
            let value = await Self.transform(name)
            items.append(value)
        }
    }
}

func uiDemo(_ names: [String]) async -> [String] {
    let vm = await ViewModel()
    await vm.load(names)
    let items = await vm.items
    return items + ["count \(items.count)"]
}
