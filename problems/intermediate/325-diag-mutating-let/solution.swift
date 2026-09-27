struct Counter {
    var count = 0
    mutating func increment() { count += 1 }
}

let c = Counter()
c.increment()
print(c.count)
