enum AuthState: CustomStringConvertible {
    case signedOut
    case signingIn(method: String)
    case signedIn(userID: String, isAnonymous: Bool)
    case failed(String)

    var description: String {
        switch self {
        case .signedOut: "signedOut"
        case .signingIn(let m): "signingIn(\(m))"
        case let .signedIn(uid, anon): "signedIn(\(uid)\(anon ? ", anonymous" : ""))"
        case .failed(let r): "failed(\(r))"
        }
    }

    func handling(_ event: String) -> AuthState? {
        let p = event.split(separator: " ").map(String.init)
        let arg = p.count > 1 ? p[1] : ""
        switch (self, p.first ?? "") {
        case (.signedOut, "start"), (.failed, "start"): return .signingIn(method: arg)
        case (.signingIn(let method), "success"): return .signedIn(userID: arg, isAnonymous: method == "anonymous")
        case (.signingIn, "failure"): return .failed(arg)
        case (.signedIn(let uid, true), "link"): return .signedIn(userID: uid, isAnonymous: false)
        case (.signedIn, "signOut"), (.signedIn, "delete"), (.failed, "signOut"): return .signedOut
        default: return nil
        }
    }
}

func authFlow(_ events: [String]) -> [String] {
    var state = AuthState.signedOut
    return events.map { event in
        guard let next = state.handling(event) else { return "ignored" }
        state = next
        return state.description
    }
}
