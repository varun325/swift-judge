enum ServiceError: Error { case offline }

protocol DataService: Sendable {
    func fetchTitles() async throws -> [String]
}

struct MockService: DataService {
    let behaviour: String
    func fetchTitles() async throws -> [String] {
        switch behaviour {
        case "fail": throw ServiceError.offline
        case "empty": return []
        default: return ["One", "Two", "Three"]
        }
    }
}

@MainActor
final class TitlesViewModel {
    enum State {
        case idle, loading, loaded([String]), failed(String)
        var label: String {
            switch self {
            case .idle: "idle"
            case .loading: "loading"
            case .loaded(let t): "loaded(\(t.count))"
            case .failed(let e): "failed(\(e))"
            }
        }
    }

    private(set) var history: [String] = []
    private(set) var state: State = .idle { didSet { history.append(state.label) } }
    private let service: any DataService

    init(service: any DataService) {
        self.service = service
        history = [state.label]
    }

    func load() async {
        state = .loading
        do {
            state = .loaded(try await service.fetchTitles())
        } catch {
            state = .failed("\(error)")
        }
    }
}

func loadScreen(_ behaviours: [String]) async -> [String] {
    var out: [String] = []
    for b in behaviours {
        let vm = await TitlesViewModel(service: MockService(behaviour: b))
        await vm.load()
        out.append(await vm.history.joined(separator: " → "))
    }
    return out
}
