func timing(_ times: [Int], interval: Int, mode: String) -> [Int] {
    if mode == "throttle" {
        var runs: [Int] = []
        for t in times where runs.last.map({ t - $0 >= interval }) ?? true { runs.append(t) }
        return runs
    }
    return times.indices.compactMap { i in
        let quietAfter = i == times.count - 1 || times[i + 1] - times[i] >= interval
        return quietAfter ? times[i] + interval : nil
    }
}
