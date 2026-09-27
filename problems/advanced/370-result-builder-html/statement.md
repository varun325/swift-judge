Write `@resultBuilder struct HTMLBuilder` with `buildBlock`, `buildOptional`, `buildEither(first:)/(second:)`, `buildArray` and `buildExpression(_ s: String)` — building a `[String]` of fragments.

 Then `func html(@HTMLBuilder _ content: () -> [String]) -> String` joins fragments. Render:
 ```swift
 html {
     "<h1>\(title)</h1>"
     if items.isEmpty { "<p>empty</p>" } else { "<ul>"; for i in items { "<li>\(i)</li>" }; "</ul>" }
     if showFooter { "<footer/>" }
 }
 ```
 (Write the `else` branch across lines — semicolons are shown only for brevity.)
