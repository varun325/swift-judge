enum BankError: Error {
    case invalidAmount
    case insufficientFunds(short: Int)
}

func withdraw(_ amount: Int, from balance: inout Int) throws(BankError) {
    guard amount > 0 else { throw .invalidAmount }
    guard amount <= balance else { throw .insufficientFunds(short: amount - balance) }
    balance -= amount
}

func withdrawals(balance: Int, amounts: [Int]) -> [String] {
    var current = balance
    return amounts.map { amount in
        do throws(BankError) {
            try withdraw(amount, from: &current)
            return "ok -> \(current)"
        } catch {
            switch error {
            case .invalidAmount: return "invalid"
            case .insufficientFunds(let short): return "short by \(short)"
            }
        }
    }
}
