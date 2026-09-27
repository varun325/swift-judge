enum PipelineError: Error { case notANumber, negative }

func parse(_ s: String) -> Result<Int, PipelineError> {
    Int(s).map(Result.success) ?? .failure(.notANumber)
}

func validate(_ n: Int) -> Result<Int, PipelineError> {
    n < 0 ? .failure(.negative) : .success(n)
}

func pipeline(_ inputs: [String]) -> [String] {
    inputs.map { input in
        switch parse(input).flatMap(validate).map({ $0 * $0 }) {
        case .success(let value): "ok \(value)"
        case .failure(let error): "error \(error)"
        }
    }
}
