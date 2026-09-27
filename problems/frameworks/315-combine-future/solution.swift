import Combine

enum ValidationError: Error { case notPositive }

func validate(_ n: Int) -> Future<Int, ValidationError> {
    Future { promise in
        promise(n > 0 ? .success(n * 2) : .failure(.notPositive))
    }
}

func futures(_ inputs: [Int]) -> [String] {
    var log: [String] = []
    var bag = Set<AnyCancellable>()
    for n in inputs {
        validate(n)
            .sink(receiveCompletion: { completion in
                switch completion {
                case .finished: log.append("finished")
                case .failure(let e): log.append("failed \(e)")
                }
            }, receiveValue: { log.append("value \($0)") })
            .store(in: &bag)
    }
    return log
}
