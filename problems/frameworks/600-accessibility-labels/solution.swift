func a11yLabels(_ rows: [[String]]) -> [String] {
    rows.map { r in
        let cents = Int(r[1]) ?? 0
        let d = cents / 100, c = cents % 100
        var price = "\(d) \(d == 1 ? "dollar" : "dollars")"
        if c > 0 { price += " \(c) \(c == 1 ? "cent" : "cents")" }
        let rating = ((Double(r[2]) ?? 0) * 10).rounded() / 10
        return "\(r[0]), \(price), rated \(rating) out of 5 stars\(r[3] == "y" ? ", bestseller" : "")"
    }
}
