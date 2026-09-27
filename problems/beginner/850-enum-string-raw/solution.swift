enum Size: String {
    case small = "S", medium = "M", large = "L", extraLarge = "XL"
}

func parseSizes(_ codes: [String]) -> [String] {
    codes.map { code in
        guard let size = Size(rawValue: code) else { return "invalid" }
        return "\(size)=\(size.rawValue)"
    }
}
