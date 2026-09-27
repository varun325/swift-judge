final class Color {
    let red: Int, green: Int, blue: Int

    init(red: Int, green: Int, blue: Int) {
        self.red = red
        self.green = green
        self.blue = blue
    }

    convenience init(white: Int) {
        self.init(red: white, green: white, blue: white)
    }

    convenience init?(hex: String) {
        guard hex.count == 7, hex.first == "#", let value = Int(hex.dropFirst(), radix: 16) else { return nil }
        self.init(red: (value >> 16) & 0xFF, green: (value >> 8) & 0xFF, blue: value & 0xFF)
    }
}

func makeColors(_ specs: [String]) -> [String] {
    specs.map { spec in
        let color: Color? = if spec.hasPrefix("white "), let w = Int(spec.dropFirst(6)) {
            Color(white: w)
        } else {
            Color(hex: spec)
        }
        guard let c = color else { return "invalid" }
        return "rgb(\(c.red),\(c.green),\(c.blue))"
    }
}
