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
    requests.map { request in
        do {
            return "got \(try buy(request))"
        } catch VendingError.invalidSelection, VendingError.outOfStock {
            return "unavailable"
        } catch VendingError.insufficientFunds(let needed) {
            return "insert \(needed) more"
        } catch {
            return "error"
        }
    }
}
