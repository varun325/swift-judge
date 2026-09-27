struct Counter {
    var count = 0
    mutating func increment() { count += 1 }
}

var c = Counter()
c.increment()
print(c.count)
