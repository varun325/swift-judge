func weatherAdvice(_ forecasts: [String]) -> [String] {
    forecasts.map { forecast in
        switch forecast.lowercased() {
        case "sun": "sunscreen"
        case "rain", "drizzle": "umbrella"
        case "snow": "boots"
        case let f where f.hasPrefix("storm"): "stay in"
        default: "enjoy"
        }
    }
}
