import SwiftUI

@MainActor func show() {
    let state = State(initialValue: 3)
    print(type(of: state.wrappedValue))
    print(type(of: state.projectedValue))
    let constant = Binding.constant(true)
    print(type(of: constant), constant.wrappedValue)
    let binding = Binding<[String]>.constant(["a", "b"])
    print(type(of: binding.first), type(of: binding[0]))
}
show()
