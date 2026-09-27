Paul's *Sharing @Observable objects through SwiftUI's environment*. One `@Observable final class Cart` is injected at the root (`.environment(cart)`); a product list "screen" adds items and a badge "screen" reads the count. Simulate both screens as structs that each hold the **same** injected reference.

 Actions: `add <item>` (list screen), `remove <item>` (list screen, first match), `badge` (badge screen logs `"badge <count>"`). Also log `"same instance <Bool>"` at the end (compare with `===`).
