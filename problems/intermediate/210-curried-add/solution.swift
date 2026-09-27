func add(_ a: Int) -> (Int) -> Int {
    { b in a + b }
}

func curryDemo(_ base: Int, _ xs: [Int]) -> [Int] {
    let addBase = add(base)
    return xs.map(addBase) + [add(1)(add(2)(3))]
}
