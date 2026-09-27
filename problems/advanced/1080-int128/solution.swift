func factorials(_ ns: [Int]) -> [String] {
    ns.map { n in
        guard n >= 0 else { return "undefined" }
        var result: Int128 = 1
        for k in stride(from: 2, through: n, by: 1) {
            let (value, overflow) = result.multipliedReportingOverflow(by: Int128(k))
            if overflow { return "overflow" }
            result = value
        }
        return String(result)
    }
}
