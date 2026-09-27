import SwiftUI

@MainActor func show() {
    let erased = AnyView(Text("x"))
    let looped = ForEach(0..<3, id: \.self) { Text("\($0)") }
    let grouped = Group { Text("a"); Text("b"); Text("c") }
    print(type(of: erased))
    print(type(of: looped))
    print(type(of: grouped))
}
show()
