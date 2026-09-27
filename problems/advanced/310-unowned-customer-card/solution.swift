final class Log { var lines: [String] = [] }

final class Customer {
    let name: String
    var card: CreditCard?
    let log: Log
    init(name: String, log: Log) { self.name = name; self.log = log }
    deinit { log.lines.append("deinit \(name)") }
}

final class CreditCard {
    let number: Int
    unowned let customer: Customer
    let log: Log
    init(number: Int, customer: Customer, log: Log) { self.number = number; self.customer = customer; self.log = log }
    deinit { log.lines.append("deinit \(number)") }
}

func cardDemo(_ customers: [String], withCard: [Bool]) -> [String] {
    let log = Log()
    var nextNumber = 1000
    for (name, hasCard) in zip(customers, withCard) {
        let customer = Customer(name: name, log: log)
        if hasCard {
            customer.card = CreditCard(number: nextNumber, customer: customer, log: log)
            nextNumber += 1
            if let card = customer.card { log.lines.append("\(card.number) belongs to \(card.customer.name)") }
        }
    }
    return log.lines
}
