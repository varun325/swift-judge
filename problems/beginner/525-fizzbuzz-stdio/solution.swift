let n = Int(readLine() ?? "") ?? 0
if n >= 1 {
    for i in 1...n {
        switch (i % 3, i % 5) {
        case (0, 0): print("FizzBuzz")
        case (0, _): print("Fizz")
        case (_, 0): print("Buzz")
        default: print(i)
        }
    }
}
