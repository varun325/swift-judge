import SwiftUI

final class Counter { nonisolated(unsafe) static var calls = 0 }

struct ContentView: View {
    var body: some View {
        Counter.calls += 1
        return VStack {
            Image(systemName: "globe")
            Text("Hello, world!")
        }
        .padding()
    }
}

@MainActor func show() {
    let view = ContentView()
    print(type(of: view.body))
    _ = view.body
    print(Counter.calls)
}
show()
