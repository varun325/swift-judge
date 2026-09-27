import Observation

@Observable
final class CartModel {
    var items: [String] = []
    var coupon = ""
    @ObservationIgnored var analyticsCount = 0
}

final class Counter: @unchecked Sendable {
    var fires = 0
    var armed = false
}

/// Like SwiftUI: track what `body` reads; after a change fires, re-render and track again.
func observe(_ model: CartModel, _ counter: Counter) {
    guard !counter.armed else { return }
    counter.armed = true
    withObservationTracking {
        _ = model.items.count
    } onChange: {
        counter.fires += 1
        counter.armed = false
    }
}

func trackingDemo(_ changes: [String]) async -> [String] {
    let model = CartModel()
    let counter = Counter()
    for change in changes {
        observe(model, counter)
        let p = change.split(separator: " ", maxSplits: 1).map(String.init)
        switch p[0] {
        case "add": model.items.append(p.count > 1 ? p[1] : "")
        case "coupon": model.coupon = p.count > 1 ? p[1] : ""
        default: model.analyticsCount += 1
        }
    }
    return ["notified \(counter.fires)", "items \(model.items.count)"]
}
