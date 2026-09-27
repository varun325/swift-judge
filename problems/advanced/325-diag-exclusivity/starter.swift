func balance(_ x: inout Int, _ y: inout Int) {
    let sum = x + y
    x = sum / 2
    y = sum - x
}

var a = 42, b = 30
balance(&a, &b)
print(a, b)
