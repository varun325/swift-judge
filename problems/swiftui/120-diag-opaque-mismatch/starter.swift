import SwiftUI

@ViewBuilder func badge(_ on: Bool) -> some View {
    if on { Text("on") } else { Image(systemName: "xmark") }
}
