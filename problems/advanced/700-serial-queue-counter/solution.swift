import Dispatch

final class SafeCounter: @unchecked Sendable {
    private var value = 0
    private let queue = DispatchQueue(label: "counter")   // serial by default

    func increment() { queue.sync { value += 1 } }
    var current: Int { queue.sync { value } }
}

func hammer(threads: Int, incrementsEach: Int) -> Int {
    let counter = SafeCounter()
    DispatchQueue.concurrentPerform(iterations: threads) { _ in
        for _ in 0..<incrementsEach { counter.increment() }
    }
    return counter.current
}
