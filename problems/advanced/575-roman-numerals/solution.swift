func toRoman(_ num: Int) -> String {
    let table = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
                 (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    var n = num
    var result = ""
    for (value, symbol) in table {
        result += String(repeating: symbol, count: n / value)
        n %= value
    }
    return result
}
