`protocol Transformer { associatedtype Input; associatedtype Output; func transform(_ x: Input) -> Output }`. Implement `Uppercaser` (String→String), `Length` (String→Int) and `Stars` (Int→String, `n` stars).

 Write a type-erased wrapper `struct AnyTransformer<In, Out>: Transformer` that stores a closure, with `init<T: Transformer>(_ base: T) where T.Input == In, T.Output == Out`, and a `func then<Next>(_ next: AnyTransformer<Out, Next>) -> AnyTransformer<In, Next>`.

 Build `AnyTransformer(Length()).then(AnyTransformer(Stars()))` and also an `[AnyTransformer<String, String>]` holding `Uppercaser` and that chain; apply each to each input, returning results in order (for each input, both transformers).
