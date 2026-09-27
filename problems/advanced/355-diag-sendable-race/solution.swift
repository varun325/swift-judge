class Counter { var value = 0 }

func work() async {
    let counter = Counter()
    Task { counter.value += 1 }
    counter.value += 1
}
