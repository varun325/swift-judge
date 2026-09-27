func describeCodes(_ codes: [Int]) -> [String] {
    let phrases = [200: "OK", 201: "Created", 301: "Moved Permanently", 404: "Not Found", 500: "Internal Server Error"]
    return codes.map { phrases[$0, default: "Unknown (\($0))"] }
}
