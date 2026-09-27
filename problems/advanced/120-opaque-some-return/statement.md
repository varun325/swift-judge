`protocol Drawable { func draw() -> String }`. Write:
 - `func makeTriangle(_ n: Int) -> some Drawable` (lines of `*` growing from 1 to `n`, joined by `"/"`)
 - `func flipped(_ d: some Drawable) -> some Drawable` (reverses the `"/"`-separated lines)

 For each size return `flipped(makeTriangle(size)).draw()`. Then answer in `explanation`: why can't `makeTriangle` return a `Triangle` for small `n` and a `Square` otherwise?
