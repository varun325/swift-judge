func snapValues(_ raw: [Double], min lower: Double, max upper: Double, step: Double) -> [Double] {
    raw.map { v in
        let stepped = step > 0 ? lower + ((v - lower) / step).rounded() * step : v
        return min(max(stepped, lower), upper)
    }
}
