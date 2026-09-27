import Observation

enum Screen: Hashable, CustomStringConvertible {
    case login, home, product(Int), cart, checkout, receipt
    var description: String {
        switch self {
        case .login: "login"
        case .home: "home"
        case .product(let id): "product\(id)"
        case .cart: "cart"
        case .checkout: "checkout"
        case .receipt: "receipt"
        }
    }
}

@Observable
final class AppRouter {
    var stack: [Screen] = [.login]
    var sheet: Screen?

    func handle(_ event: String) {
        let p = event.split(separator: " ").map(String.init)
        switch p[0] {
        case "loggedIn": stack = [.home]
        case "tapProduct": if let id = Int(p.count > 1 ? p[1] : "") { stack.append(.product(id)) }
        case "openCart": sheet = .cart
        case "checkout":
            guard sheet == .cart else { return }
            sheet = nil
            stack.append(.checkout)
        case "paid": stack = [.home, .receipt]
        case "back": if stack.count > 1 { stack.removeLast() }
        case "logout": stack = [.login]; sheet = nil
        default: break
        }
    }

    var summary: String { stack.map(\.description).joined(separator: ">") + (sheet.map { " [\($0)]" } ?? "") }
}

func appFlow(_ events: [String]) -> [String] {
    let router = AppRouter()
    return events.map { router.handle($0); return router.summary }
}
