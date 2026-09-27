func digitSum(_ n: Int) -> Int {
    var x = n.magnitude
    var total: UInt = 0
    while x > 0 {
        total += x % 10
        x /= 10
    }
    return Int(total)
}
