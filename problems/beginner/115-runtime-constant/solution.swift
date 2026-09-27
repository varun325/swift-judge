func shippingCost(weightKg: Double, express: Bool) -> Double {
    let rate: Double
    if express {
        rate = 5.0
    } else {
        rate = 2.5
    }
    return max(10.0, rate * weightKg)
}
