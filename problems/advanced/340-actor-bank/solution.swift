actor Account {
    private var balance = 0
    func deposit(_ amount: Int) { balance += amount }
    var current: Int { balance }
}

func concurrentDeposits(_ amounts: [Int]) async -> Int {
    let account = Account()
    await withTaskGroup(of: Void.self) { group in
        for amount in amounts {
            group.addTask { await account.deposit(amount) }
        }
    }
    return await account.current
}
