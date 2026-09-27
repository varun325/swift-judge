enum Coffee: String, CaseIterable {
    case espresso, latte, cappuccino, mocha

    var price: Int {
        switch self {
        case .espresso: 2
        case .latte, .cappuccino: 4
        case .mocha: 5
        }
    }
}

func menu(maxPrice: Int) -> [String] {
    Coffee.allCases.filter { $0.price <= maxPrice }.map(\.rawValue)
}
