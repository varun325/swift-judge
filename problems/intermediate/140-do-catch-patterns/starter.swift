enum VendingError: Error {
    case invalidSelection
    case outOfStock
    case insufficientFunds(coinsNeeded: Int)
    case machineJammed
}

func buy(_ item: String) throws -> String {
    switch item {
    case "chips", "candy": return item
    case "soda": throw VendingError.outOfStock
    case "caviar": throw VendingError.insufficientFunds(coinsNeeded: 99)
    case "shake": throw VendingError.machineJammed
    default: throw VendingError.invalidSelection
    }
}

func vend(_ requests: [String]) -> [String] {
    // call buy(_:) for each request and handle every error
    return []
}
