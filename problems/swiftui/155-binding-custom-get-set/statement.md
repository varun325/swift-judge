Swiftful's *Create custom Bindings*. Given storage in a class (`final class Store { var volume = 50 }`), create `Binding<Int>(get:set:)` whose setter **clamps** to 0…100, and a derived `Binding<Bool>` "isMuted" that reads `volume == 0` and, when set to `true`, stores 0 (setting `false` restores 50).

 Apply each write to the volume binding (negative numbers mean "set isMuted = true", `1000` means "set isMuted = false"). Return `"<volume> muted:<Bool>"` after each write.
