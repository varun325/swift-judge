struct BankAccount {
    private(set) var funds = 0

    mutating func deposit(_ amount: Int) {
        funds += amount
    }

    mutating func withdraw(_ amount: Int) -> Bool {
        guard amount <= funds else { return false }
        funds -= amount
        return true
    }
}

func bankOps(_ ops: [String]) -> [String] {
    var account = BankAccount()
    return ops.map { op in
        let parts = op.split(separator: " ")
        let amount = Int(parts[1])!
        let ok = parts[0] == "d" ? { account.deposit(amount); return true }() : account.withdraw(amount)
        return "\(ok ? "ok" : "refused") \(account.funds)"
    }
}
