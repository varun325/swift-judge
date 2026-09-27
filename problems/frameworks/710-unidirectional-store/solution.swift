struct AppState: Equatable {
    var count = 0
    var fact: String?
    var isLoading = false
}

enum Action {
    case increment, decrement, factButtonTapped
    case factResponse(String)
}

typealias Effect = @Sendable () async -> Action

func reduce(_ state: inout AppState, _ action: Action) -> Effect? {
    switch action {
    case .increment: state.count += 1; state.fact = nil; return nil
    case .decrement: state.count -= 1; state.fact = nil; return nil
    case .factButtonTapped:
        state.isLoading = true
        let n = state.count
        return { .factResponse("fact about \(n)") }
    case .factResponse(let fact):
        state.isLoading = false
        state.fact = fact
        return nil
    }
}

@MainActor
final class Store {
    private(set) var state = AppState()
    private(set) var history: [String] = []

    func send(_ action: Action) async {
        let effect = reduce(&state, action)
        history.append("\(state.count) \(state.isLoading ? "loading" : "-") \(state.fact ?? "-")")
        if let effect { await send(await effect()) }
    }
}

func storeRun(_ actions: [String]) async -> [String] {
    let store = await Store()
    for a in actions {
        switch a {
        case "+": await store.send(.increment)
        case "-": await store.send(.decrement)
        case "fact": await store.send(.factButtonTapped)
        default: break
        }
    }
    return await store.history
}
