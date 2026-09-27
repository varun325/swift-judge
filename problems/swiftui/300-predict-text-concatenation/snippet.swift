import SwiftUI

@MainActor func show() {
    let bold = Text("Hi").bold()
    let padded = Text("Hi").padding()
    let combined = Text("Hello ").bold() + Text("world").italic()
    print(type(of: bold))
    print(type(of: padded))
    print(type(of: combined))
}
show()
