func lcs(_ a: String, _ b: String) -> Int {
    let x = Array(a), y = Array(b)
    var dp = Array(repeating: Array(repeating: 0, count: y.count + 1), count: x.count + 1)
    for i in stride(from: x.count - 1, through: 0, by: -1) {
        for j in stride(from: y.count - 1, through: 0, by: -1) {
            dp[i][j] = x[i] == y[j] ? 1 + dp[i + 1][j + 1] : max(dp[i + 1][j], dp[i][j + 1])
        }
    }
    return dp[0][0]
}
