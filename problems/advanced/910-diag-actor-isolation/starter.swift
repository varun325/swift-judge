actor Counter { var value = 0 }

func read(_ c: Counter) async -> Int {
    await c.value
}
