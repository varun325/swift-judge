import SwiftUI

struct MaxHeightKey: PreferenceKey {
    static let defaultValue: Double = 0
    static func reduce(value: inout Double, nextValue: () -> Double) {
        value = max(value, nextValue())
    }
}

struct TitlesKey: PreferenceKey {
    static let defaultValue: [String] = []
    static func reduce(value: inout [String], nextValue: () -> [String]) {
        value.append(contentsOf: nextValue())
    }
}

func fold<K: PreferenceKey>(_ key: K.Type, _ values: [K.Value]) -> K.Value {
    var result = K.defaultValue
    for v in values { K.reduce(value: &result, nextValue: { v }) }
    return result
}

func reducePreferences(heights: [Double], titles: [String]) async -> [String] {
    ["max \(fold(MaxHeightKey.self, heights))", "titles \(fold(TitlesKey.self, titles.map { [$0] }).joined(separator: ","))"]
}
