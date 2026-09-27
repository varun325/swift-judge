enum LedgerError: Error {
    case badCommand(String)
    case badAmount(String)
    case insufficient(needed: Int)
}

func apply(_ line: String, to balance: inout Int) throws {
    let parts = line.split(separator: " ").map(String.init)
    guard parts.count == 2, ["deposit", "withdraw"].contains(parts[0]) else {
        throw LedgerError.badCommand(parts.first ?? "")
    }
    guard let amount = Int(parts[1]), amount > 0 else { throw LedgerError.badAmount(parts[1]) }
    if parts[0] == "deposit" {
        balance += amount
    } else {
        guard amount <= balance else { throw LedgerError.insufficient(needed: amount - balance) }
        balance -= amount
    }
}

var balance = 0
while let line = readLine() {
    do {
        try apply(line, to: &balance)
        print("ok \(balance)")
    } catch LedgerError.badCommand(let cmd) {
        print("error: unknown command \(cmd)")
    } catch LedgerError.badAmount(let text) {
        print("error: bad amount \(text)")
    } catch LedgerError.insufficient(let needed) {
        print("error: need \(needed) more")
    } catch {
        print("error: \(error)")
    }
}
print("final \(balance)")
