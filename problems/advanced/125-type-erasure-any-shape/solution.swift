protocol Transformer {
    associatedtype Input
    associatedtype Output
    func transform(_ x: Input) -> Output
}

struct Uppercaser: Transformer { func transform(_ x: String) -> String { x.uppercased() } }
struct Length: Transformer { func transform(_ x: String) -> Int { x.count } }
struct Stars: Transformer { func transform(_ x: Int) -> String { String(repeating: "*", count: x) } }

struct AnyTransformer<In, Out>: Transformer {
    private let _transform: (In) -> Out

    init<T: Transformer>(_ base: T) where T.Input == In, T.Output == Out {
        _transform = base.transform
    }

    private init(closure: @escaping (In) -> Out) { _transform = closure }

    func transform(_ x: In) -> Out { _transform(x) }

    func then<Next>(_ next: AnyTransformer<Out, Next>) -> AnyTransformer<In, Next> {
        AnyTransformer<In, Next>(closure: { next.transform(self.transform($0)) })
    }
}

func pipelineDemo(_ inputs: [String]) -> [String] {
    let stars = AnyTransformer(Length()).then(AnyTransformer(Stars()))
    let all: [AnyTransformer<String, String>] = [AnyTransformer(Uppercaser()), stars]
    return inputs.flatMap { input in all.map { $0.transform(input) } }
}
