enum SwipeDecision: String { case like, nope, superlike, `return` }

func decide(x: Double, predictedX: Double, y: Double) -> SwipeDecision {
    if y < -150 && abs(x) < 60 { return .superlike }
    if x > 120 || predictedX > 300 { return .like }
    if x < -120 || predictedX < -300 { return .nope }
    return .return
}

func swipeDecisions(_ drags: [[Double]]) -> [String] {
    drags.map { d in
        let rotation = min(max(d[0] / 20, -15), 15)
        return "\(decide(x: d[0], predictedX: d[1], y: d[2]).rawValue) \((rotation * 10).rounded() / 10)°"
    }
}
