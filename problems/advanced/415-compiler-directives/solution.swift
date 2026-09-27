func buildInfo() -> [String] {
    var out: [String] = []
    #if swift(>=6.0)
    out.append("swift>=6")
    #else
    out.append("swift<6")
    #endif
    #if os(macOS)
    out.append("macOS")
    #elseif os(Linux)
    out.append("Linux")
    #else
    out.append("other")
    #endif
    #if arch(arm64)
    out.append("arm64")
    #else
    out.append("x86_64")
    #endif
    #if canImport(Foundation)
    out.append("has Foundation")
    #endif
    #if DEBUG
    out.append("debug")
    #else
    out.append("release")
    #endif
    if #available(macOS 13, *) {
        out.append("macOS 13+")
    } else {
        out.append("older")
    }
    return out
}
