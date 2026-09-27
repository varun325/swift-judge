import Foundation

func parsePrices(_ inputs: [String]) -> [String] {
    let currency = Decimal.FormatStyle.Currency(code: "USD", locale: Locale(identifier: "en_US"))
    return inputs.map { input in
        let trimmed = input.trimmingCharacters(in: .whitespaces)
        let value = (try? currency.parseStrategy.parse(trimmed)) ?? Decimal(string: trimmed, locale: Locale(identifier: "en_US_POSIX"))
        guard let value else { return "invalid" }
        var cents = value * 100
        var rounded = Decimal()
        NSDecimalRound(&rounded, &cents, 0, .plain)
        return "\(NSDecimalNumber(decimal: rounded).intValue)"
    }
}
