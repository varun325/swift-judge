enum OrderStatus {
    case placed, paid, shipped, delivered, cancelled

    mutating func handle(_ event: String) -> Bool {
        switch (self, event) {
        case (.placed, "pay"): self = .paid
        case (.paid, "ship"): self = .shipped
        case (.shipped, "deliver"): self = .delivered
        case (.placed, "cancel"), (.paid, "cancel"): self = .cancelled
        default: return false
        }
        return true
    }
}

func orderTimeline(_ events: [String]) -> [String] {
    var status = OrderStatus.placed
    return events.map { event in
        status.handle(event) ? "\(event): \(status)" : "\(event): rejected"
    }
}
