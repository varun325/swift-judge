import SwiftUI

@MainActor func types(flag: Bool) {
    let a = VStack { Text("A"); Text("B") }
    let b = VStack { Text("A"); if flag { Text("B") } }
    let c = VStack { if flag { Text("A") } else { Image(systemName: "star") } }
    print(type(of: a))
    print(type(of: b))
    print(type(of: c))
}
types(flag: true)
