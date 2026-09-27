enum Lifetime { case transient, singleton }

final class Container {
    private var factories: [ObjectIdentifier: (lifetime: Lifetime, make: () -> Any)] = [:]
    private var singletons: [ObjectIdentifier: Any] = [:]

    func register<T>(_ type: T.Type, lifetime: Lifetime, factory: @escaping () -> T) {
        factories[ObjectIdentifier(type)] = (lifetime, { factory() })
    }

    func resolve<T>(_ type: T.Type) -> T? {
        let key = ObjectIdentifier(type)
        guard let entry = factories[key] else { return nil }
        if entry.lifetime == .singleton {
            if let existing = singletons[key] as? T { return existing }
            let made = entry.make()
            singletons[key] = made
            return made as? T
        }
        return entry.make() as? T
    }
}

protocol AnalyticsService: AnyObject { var name: String { get } }
protocol APIClient: AnyObject { var name: String { get } }
protocol Unregistered {}

final class LiveAnalytics: AnalyticsService { let name = "live analytics" }
final class MockAnalytics: AnalyticsService { let name = "mock analytics" }
final class LiveAPI: APIClient { let name = "live api" }
final class MockAPI: APIClient { let name = "mock api" }

func containerDemo(useMocks: Bool) -> [String] {
    let c = Container()
    c.register(AnalyticsService.self, lifetime: .singleton) { useMocks ? MockAnalytics() as any AnalyticsService : LiveAnalytics() }
    c.register(APIClient.self, lifetime: .transient) { useMocks ? MockAPI() as any APIClient : LiveAPI() }
    let a1 = c.resolve(AnalyticsService.self)!, a2 = c.resolve(AnalyticsService.self)!
    let p1 = c.resolve(APIClient.self)!, p2 = c.resolve(APIClient.self)!
    return [a1.name, "analytics same:\(a1 === a2)", p1.name, "api same:\(p1 === p2)", c.resolve(Unregistered.self) == nil ? "missing" : "found"]
}
