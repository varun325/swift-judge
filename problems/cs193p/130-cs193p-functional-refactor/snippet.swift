var bonus = 1
let pegs = ["R", "G", "B"]
let labels = pegs.map { peg in "\(peg)\(bonus)" }
bonus = 10
let makers = pegs.map { peg in { "\(peg)\(bonus)" } }
bonus = 100
print(labels)
print(makers.map { $0() })
let indexed = pegs.enumerated().map { i, peg in i.isMultiple(of: 2) ? peg.lowercased() : peg }
print(indexed)
