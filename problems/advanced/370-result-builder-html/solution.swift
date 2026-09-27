@resultBuilder
struct HTMLBuilder {
    static func buildExpression(_ s: String) -> [String] { [s] }
    static func buildBlock(_ parts: [String]...) -> [String] { parts.flatMap { $0 } }
    static func buildOptional(_ part: [String]?) -> [String] { part ?? [] }
    static func buildEither(first: [String]) -> [String] { first }
    static func buildEither(second: [String]) -> [String] { second }
    static func buildArray(_ parts: [[String]]) -> [String] { parts.flatMap { $0 } }
}

func html(@HTMLBuilder _ content: () -> [String]) -> String {
    content().joined()
}

func renderPage(title: String, items: [String], showFooter: Bool) -> String {
    html {
        "<h1>\(title)</h1>"
        if items.isEmpty {
            "<p>empty</p>"
        } else {
            "<ul>"
            for i in items {
                "<li>\(i)</li>"
            }
            "</ul>"
        }
        if showFooter {
            "<footer/>"
        }
    }
}
