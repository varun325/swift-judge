import Foundation

func localTimes(_ timestamps: [String], zones: [String]) -> [String] {
    timestamps.map { ts in
        guard let date = try? Date(ts, strategy: .iso8601) else { return "invalid" }
        return zones.compactMap { TimeZone(identifier: $0) }.map { zone in
            let f = DateFormatter()
            f.locale = Locale(identifier: "en_US_POSIX")
            f.timeZone = zone
            f.dateFormat = "HH:mm zzz"
            return f.string(from: date)
        }.joined(separator: " / ")
    }
}
