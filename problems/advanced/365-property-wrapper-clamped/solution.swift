@propertyWrapper
struct Clamped<Value: Comparable> {
    private var value: Value
    private let range: ClosedRange<Value>
    private(set) var projectedValue = 0

    init(wrappedValue: Value, _ range: ClosedRange<Value>) {
        self.range = range
        self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }

    var wrappedValue: Value {
        get { value }
        set {
            let clamped = min(max(newValue, range.lowerBound), range.upperBound)
            if clamped != newValue { projectedValue += 1 }
            value = clamped
        }
    }
}

@propertyWrapper
struct Trimmed {
    private var value = ""
    init(wrappedValue: String) { self.wrappedValue = wrappedValue }
    var wrappedValue: String {
        get { value }
        set { value = newValue.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() }
    }
}

import Foundation

struct Settings {
    @Clamped(0...100) var volume = 50
    @Trimmed var username = ""
}

func wrapperDemo(_ volumes: [Int], _ names: [String]) -> [String] {
    var s = Settings()
    var log: [String] = []
    for v in volumes { s.volume = v; log.append("v=\(s.volume)") }
    for n in names { s.username = n; log.append("u=\(s.username)") }
    log.append("clamps=\(s.$volume)")
    return log
}
