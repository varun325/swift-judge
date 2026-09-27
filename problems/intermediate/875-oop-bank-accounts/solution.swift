class Account {
    let id: String
    private(set) var balance = 0
    init(id: String) { self.id = id }
    func deposit(_ amount: Int) { balance += amount }
    func withdraw(_ amount: Int) -> Bool {
        guard amount <= balance else { return false }
        balance -= amount
        return true
    }
}

final class SavingsAccount: Account {
    override func withdraw(_ amount: Int) -> Bool {
        guard balance - amount >= 100 else { return false }
        return super.withdraw(amount)
    }
}

func bank(_ ops: [String]) -> [String] {
    var accounts: [String: Account] = [:]
    return ops.map { op in
        let p = op.split(separator: " ").map(String.init)
        if p[0] == "open" {
            accounts[p[1]] = p[2] == "savings" ? SavingsAccount(id: p[1]) : Account(id: p[1])
            return "ok"
        }
        guard let account = accounts[p[1]] else { return "no account" }
        switch p[0] {
        case "dep": account.deposit(Int(p[2])!); return "ok"
        case "wd": return account.withdraw(Int(p[2])!) ? "ok" : "refused"
        default: return "\(account.id): \(account.balance)"
        }
    }
}
