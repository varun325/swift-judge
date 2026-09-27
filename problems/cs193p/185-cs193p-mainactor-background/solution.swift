import Foundation
import Observation

struct Solver {
    /// Runs on the cooperative thread pool (nonisolated), not on the main actor.
    /// `Thread.isMainThread` is unavailable directly in async code (Swift 6), so ask from a sync helper.
    static func onMainThread() -> Bool { Thread.isMainThread }

    @concurrent
    static func candidates(master: [String], choices: [String]) async -> (count: Int, onMain: Bool) {
        let onMain = onMainThread()
        guard let probePeg = choices.first, !master.isEmpty else { return (0, onMain) }
        let probe = Array(repeating: probePeg, count: master.count)
        func score(_ code: [String], _ guess: [String]) -> Int { zip(code, guess).count(where: ==) }
        let target = score(master, probe)
        var codes: [[String]] = [[]]
        for _ in master { codes = codes.flatMap { c in choices.map { c + [$0] } } }
        return (codes.count(where: { score($0, probe) == target }), onMain)
    }
}

@MainActor
@Observable
final class HintModel {
    private(set) var statuses = ["idle"]
    private(set) var solvedOnMain = true

    func findHint(master: [String], choices: [String]) async {
        statuses.append("thinking")
        let result = await Solver.candidates(master: master, choices: choices)
        solvedOnMain = result.onMain
        statuses.append("\(result.count) candidates")
    }
}

func solverDemo(master: [String], choices: [String]) async -> [String] {
    let model = await HintModel()
    await model.findHint(master: master, choices: choices)
    return await model.statuses + ["main thread during solve: \(await model.solvedOnMain)"]
}
