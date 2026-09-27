func describe(_ n: Int) -> String {
    var description = "The number \(n) is"
    switch n {
    case 2, 3, 5, 7, 11, 13, 17, 19:
        description += " a prime number, and also"
        fallthrough
    default:
        description += " an integer."
    }
    return description
}
