import SwiftUI

struct CounterView: View {
    var count = 0
    var body: some View {
        Button("Count: \(count)") { count += 1 }
    }
}
