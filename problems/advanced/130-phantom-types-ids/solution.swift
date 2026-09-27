protocol LengthUnit { static var metersPerUnit: Double { get } }
enum Meters: LengthUnit { static let metersPerUnit = 1.0 }
enum Feet: LengthUnit { static let metersPerUnit = 0.3048 }

struct Length<Unit: LengthUnit> {
    let value: Double

    static func + (a: Length, b: Length) -> Length { Length(value: a.value + b.value) }

    func converted<To: LengthUnit>(to: To.Type) -> Length<To> {
        Length<To>(value: value * Unit.metersPerUnit / To.metersPerUnit)
    }
}

func distances(_ meters: [Double], _ feet: [Double]) -> [Double] {
    let m = meters.map { Length<Meters>(value: $0) }.reduce(Length(value: 0), +)
    let f = feet.map { Length<Feet>(value: $0) }.reduce(Length(value: 0), +)
    return [m.value, f.value, (m + f.converted(to: Meters.self)).value]
}
