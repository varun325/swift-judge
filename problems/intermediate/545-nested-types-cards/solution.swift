struct Card {
    enum Suit: Character, CaseIterable {
        case spades = "♠", hearts = "♥", diamonds = "♦", clubs = "♣"
    }

    enum Rank: Int, CaseIterable, Comparable {
        case two = 2, three, four, five, six, seven, eight, nine, ten, jack, queen, king, ace

        var symbol: String {
            switch self {
            case .jack: "J"
            case .queen: "Q"
            case .king: "K"
            case .ace: "A"
            default: String(rawValue)
            }
        }

        static func < (a: Rank, b: Rank) -> Bool { a.rawValue < b.rawValue }
    }

    let rank: Rank
    let suit: Suit

    var name: String { "\(rank.symbol)\(suit.rawValue)" }

    static var fullDeck: [Card] {
        Suit.allCases.flatMap { suit in Rank.allCases.map { Card(rank: $0, suit: suit) } }
    }
}

func deckSummary(_ draws: [Int]) -> [String] {
    let deck = Card.fullDeck
    let hand = draws.map { deck[$0 % deck.count] }
    let best = hand.max { $0.rank < $1.rank }
    return hand.map(\.name) + ["highest: \(best?.name ?? "none")"]
}
