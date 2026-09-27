extension RandomAccessCollection where Element: Comparable {
    func binarySearch(_ target: Element) -> Index? {
        var low = startIndex
        var high = endIndex
        while low < high {
            let mid = index(low, offsetBy: distance(from: low, to: high) / 2)
            if self[mid] == target { return mid }
            if self[mid] < target { low = index(after: mid) } else { high = mid }
        }
        return nil
    }
}

func searchDemo(_ nums: [Int], _ words: [String], target: Int, word: String) -> [Int] {
    let slice = nums.count > 2 ? nums[2...] : nums[nums.endIndex...]
    return [nums.binarySearch(target) ?? -1, words.binarySearch(word) ?? -1, slice.binarySearch(target) ?? -1]
}
