import SwiftUI

struct CodeView<AncillaryView: View>: View {
    let pegs: [String]
    let onTap: () -> String
    @ViewBuilder let ancillaryView: () -> AncillaryView

    init(pegs: [String], onTap: @escaping () -> String = { "none" }, @ViewBuilder ancillaryView: @escaping () -> AncillaryView) {
        self.pegs = pegs
        self.onTap = onTap
        self.ancillaryView = ancillaryView
    }

    var body: some View {
        HStack { ForEach(pegs, id: \.self) { Text($0) }; ancillaryView() }
    }
}

@MainActor func show() {
    let markers = CodeView(pegs: ["R", "G"]) { Text("2E 0I") }
    let button = CodeView(pegs: ["B"], onTap: { "guessed!" }) { Button("Guess") {} }
    let empty = CodeView(pegs: []) { EmptyView() }
    print(type(of: markers))
    print(type(of: button))
    print(type(of: empty), markers.onTap(), button.onTap())
}
show()
