import SwiftUI

func badge(_ on: Bool) -> some View {
    if on { return Text("on") } else { return Image(systemName: "xmark") }
}
