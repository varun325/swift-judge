func check(_ x: Int) -> String {
    var out = ""
    switch x {
    case let n where n < 0:
        out += "negative "
        fallthrough
    case 0:
        out += "small "
    case 1...9:
        out += "digit "
    case 10, 20, 30:
        out += "round "
        fallthrough
    default:
        out += "other"
    }
    return out
}
for x in [-5, 0, 7, 20, 99] { print(x, "->", check(x)) }
