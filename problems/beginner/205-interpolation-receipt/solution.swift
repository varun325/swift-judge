func dollars(_ cents: Int) -> String {
    let remainder = cents % 100
    return "$\(cents / 100).\(remainder < 10 ? "0" : "")\(remainder)"
}

func receiptLine(item: String, quantity: Int, unitCents: Int) -> String {
    "\(quantity) x \(item) @ \(dollars(unitCents)) = \(dollars(quantity * unitCents))"
}
