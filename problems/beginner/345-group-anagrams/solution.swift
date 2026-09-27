func groupAnagrams(_ words: [String]) -> [[String]] {
    Array(Dictionary(grouping: words) { String($0.sorted()) }.values)
}
