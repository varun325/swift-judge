import Foundation

func runs(_ kilometres: [Double]) -> [String] {
    let us = Locale(identifier: "en_US")
    let style = Measurement<UnitLength>.FormatStyle(width: .abbreviated, locale: us, usage: .asProvided, numberFormatStyle: .number.precision(.fractionLength(2)))
    return kilometres.map { km in
        let distance = Measurement(value: km, unit: UnitLength.kilometers)
        let miles = distance.converted(to: .miles)
        let pace = Duration.seconds(km * 330)
        return "\(distance.formatted(style)) = \(miles.formatted(style)) in \(pace.formatted(.time(pattern: .hourMinuteSecond)))"
    }
}
