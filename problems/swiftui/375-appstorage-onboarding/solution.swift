import SwiftUI

@MainActor func run(_ sessions: [[String]]) -> [String] {
    // A suite named by an absolute path is a private plist file: one per process, in the temp
    // directory, so parallel runs never clobber each other and ~/Library/Preferences stays clean.
    let suite = NSTemporaryDirectory() + "swift-judge-onboarding-\(ProcessInfo.processInfo.processIdentifier)"
    let store = UserDefaults(suiteName: suite)!
    store.removePersistentDomain(forName: suite)
    var log: [String] = []
    for actions in sessions {
        let step = AppStorage(wrappedValue: 0, "onboardingStep", store: store)
        let name = AppStorage(wrappedValue: "", "userName", store: store)
        log.append("launch step \(step.wrappedValue) name \(name.wrappedValue.isEmpty ? "-" : name.wrappedValue)")
        for action in actions {
            let p = action.split(separator: " ", maxSplits: 1).map(String.init)
            switch p[0] {
            case "next": step.wrappedValue = min(step.wrappedValue + 1, 3)
            case "skip": step.wrappedValue = 3
            case "name": name.wrappedValue = p.count > 1 ? p[1] : ""
            default: break
            }
        }
    }
    store.removePersistentDomain(forName: suite)
    try? FileManager.default.removeItem(atPath: suite + ".plist")
    return log
}

func onboardingRuns(_ sessions: [[String]]) async -> [String] {
    await run(sessions)
}
