func holdProgress(_ holds: [Double], required: Double) -> [String] {
    holds.map { held in
        let progress = required > 0 ? min(max(held / required, 0), 1) : 1
        let state = progress >= 1 ? "confirmed" : progress < 0.3 ? "cancelled" : "partial"
        return "\(Int((progress * 100).rounded(.down)))% \(state)"
    }
}
