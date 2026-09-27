import Foundation

func cartBadges(_ counts: [Int]) -> [String] {
    counts.map { n in
        let phrase = AttributedString(localized: "^[\(n) item](inflect: true) in cart")
        return String(phrase.characters)
    }
}
