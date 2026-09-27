import SwiftUI

final class Store: @unchecked Sendable {
    var volume = 50
}

@MainActor func run(_ writes: [Int]) -> [String] {
    let store = Store()
    let volume = Binding<Int>(
        get: { store.volume },
        set: { store.volume = min(max($0, 0), 100) }
    )
    let isMuted = Binding<Bool>(
        get: { volume.wrappedValue == 0 },
        set: { volume.wrappedValue = $0 ? 0 : 50 }
    )
    return writes.map { w in
        if w < 0 { isMuted.wrappedValue = true }
        else if w == 1000 { isMuted.wrappedValue = false }
        else { volume.wrappedValue = w }
        return "\(volume.wrappedValue) muted:\(isMuted.wrappedValue)"
    }
}

func bindingDemo(_ writes: [Int]) async -> [String] {
    await run(writes)
}
