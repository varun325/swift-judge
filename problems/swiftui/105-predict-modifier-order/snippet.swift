import SwiftUI

@MainActor func show() {
    let one = Text("Hi").padding().background(Color.red)
    let two = Text("Hi").background(Color.red).padding()
    print(type(of: one))
    print(type(of: two))
    print(type(of: one) == type(of: two))
}
show()
