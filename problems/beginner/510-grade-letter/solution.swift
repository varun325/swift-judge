func letterGrade(_ score: Int) -> String {
    switch score {
    case 90...100: "A"
    case 80..<90: "B"
    case 70..<80: "C"
    case 60..<70: "D"
    case 0..<60: "F"
    default: "invalid"
    }
}
