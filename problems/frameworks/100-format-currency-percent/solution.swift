import Foundation

func formatted(_ values: [Double]) -> [String] {
    let us = Locale(identifier: "en_US")
    let de = Locale(identifier: "de_DE")
    return values.map { v in
        [
            v.formatted(.currency(code: "USD").locale(us)),
            v.formatted(.currency(code: "EUR").locale(de)),
            v.formatted(.percent.precision(.fractionLength(1)).locale(us)),
            v.formatted(.number.notation(.compactName).locale(us)),
        ].joined(separator: " | ")
    }
}
