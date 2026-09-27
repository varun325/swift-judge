enum Shape {
    case circle(radius: Double)
    case rectangle(width: Double, height: Double)
    case triangle(base: Double, height: Double)

    var area: Double {
        switch self {
        case .circle(let r): .pi * r * r
        case let .rectangle(w, h): w * h
        case let .triangle(b, h): b * h / 2
        }
    }

    init?(spec: String) {
        let parts = spec.split(separator: " ")
        let nums = parts.dropFirst().compactMap { Double($0) }
        switch (parts.first, nums.count) {
        case ("circle", 1): self = .circle(radius: nums[0])
        case ("rectangle", 2): self = .rectangle(width: nums[0], height: nums[1])
        case ("triangle", 2): self = .triangle(base: nums[0], height: nums[1])
        default: return nil
        }
    }
}

func totalArea(_ specs: [String]) -> Double {
    specs.compactMap(Shape.init(spec:)).reduce(0) { $0 + $1.area }
}
