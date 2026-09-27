actor Counter { var value = 0; func bump() { value += 1 } }

func work() async {
    let counter = Counter()
    Task { await counter.bump() }
    await counter.bump()
}
