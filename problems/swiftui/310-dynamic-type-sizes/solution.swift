import SwiftUI

func layoutFor(_ sizes: [String]) async -> [String] {
    let byName = Dictionary(uniqueKeysWithValues: DynamicTypeSize.allCases.map { ("\($0)", $0) })
    var out = sizes.map { name -> String in
        guard let size = byName[name] else { return "\(name): unknown" }
        return "\(name): \(size >= .accessibility1 ? "VStack" : "HStack")"
    }
    out.append("accessibility sizes: \(DynamicTypeSize.allCases.filter(\.isAccessibilitySize).count)")
    return out
}
