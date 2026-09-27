import Foundation

func conflicts(_ meetings: [[Int]]) -> [String] {
    let day = Date(timeIntervalSince1970: 0)
    let intervals = meetings.map { DateInterval(start: day.addingTimeInterval(Double($0[0] * 60)), duration: Double($0[1] * 60)) }
    var out: [String] = []
    for i in intervals.indices {
        for j in intervals.indices where j > i {
            if let overlap = intervals[i].intersection(with: intervals[j]), overlap.duration > 0 {
                out.append("\(i)-\(j) \(Int(overlap.duration / 60))")
            }
        }
    }
    return out
}
