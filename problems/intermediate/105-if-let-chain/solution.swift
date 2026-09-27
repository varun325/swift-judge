func rectangleArea(width: String?, height: String?) -> String {
    if let width, let w = Int(width), let height, let h = Int(height), w > 0, h > 0 {
        return "area \(w * h)"
    }
    return "invalid"
}
