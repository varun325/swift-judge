Like Swiftful's *Rebuild Bumble in SwiftUI*: when a drag ends you get `translation` and `predictedEndTranslation`. Decide per drag `[translationX, predictedEndX, translationY]`:
 - `"like"` if translationX > 120 **or** predictedEndX > 300
 - `"nope"` if translationX < −120 or predictedEndX < −300
 - `"superlike"` if translationY < −150 and |translationX| < 60
 - otherwise `"return"` (spring back)

 Also report the card's rotation for the translation: `rotation = translationX / 20` degrees, clamped to ±15, as `"<decision> <rotation rounded to 1dp>°"`.
