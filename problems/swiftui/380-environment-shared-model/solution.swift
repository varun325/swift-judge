import Observation

@Observable
final class Cart {
    var items: [String] = []
}

struct ProductListScreen {
    let cart: Cart
    func add(_ item: String) { cart.items.append(item) }
    func remove(_ item: String) {
        if let i = cart.items.firstIndex(of: item) { cart.items.remove(at: i) }
    }
}

struct BadgeScreen {
    let cart: Cart
    var label: String { "badge \(cart.items.count)" }
}

func cartScreens(_ actions: [String]) -> [String] {
    let cart = Cart()
    let list = ProductListScreen(cart: cart)
    let badge = BadgeScreen(cart: cart)
    var log: [String] = []
    for action in actions {
        let p = action.split(separator: " ", maxSplits: 1).map(String.init)
        switch p[0] {
        case "add": list.add(p.count > 1 ? p[1] : "")
        case "remove": list.remove(p.count > 1 ? p[1] : "")
        default: log.append(badge.label)
        }
    }
    log.append("same instance \(list.cart === badge.cart)")
    return log
}
