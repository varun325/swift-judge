import Combine
import Observation

final class ProfileVM: ObservableObject {
    @Published var name = ""
    @Published var followers = 0
}

@Observable
final class ProfileModel {
    var name = ""
    var followers = 0
}

final class Tally: @unchecked Sendable {
    var fires = 0
    var armed = false
}

func track(_ model: ProfileModel, _ tally: Tally) {
    guard !tally.armed else { return }
    tally.armed = true
    withObservationTracking { _ = model.name } onChange: {
        tally.fires += 1
        tally.armed = false
    }
}

func invalidations(_ changes: [String]) -> [Int] {
    let legacy = ProfileVM()
    var legacyCount = 0
    let cancellable = legacy.objectWillChange.sink { legacyCount += 1 }
    let modern = ProfileModel()
    let tally = Tally()
    for change in changes {
        track(modern, tally)
        let p = change.split(separator: " ", maxSplits: 1).map(String.init)
        let value = p.count > 1 ? p[1] : ""
        if p[0] == "name" {
            legacy.name = value
            modern.name = value
        } else {
            legacy.followers = Int(value) ?? 0
            modern.followers = Int(value) ?? 0
        }
    }
    _ = cancellable
    return [legacyCount, tally.fires]
}
