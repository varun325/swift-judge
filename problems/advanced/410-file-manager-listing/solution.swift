import Foundation

func listing(_ files: [String]) throws -> [String] {
    let fm = FileManager.default
    let root = fm.temporaryDirectory.appendingPathComponent(UUID().uuidString, isDirectory: true)
    try fm.createDirectory(at: root, withIntermediateDirectories: true)
    defer { try? fm.removeItem(at: root) }

    for path in files {
        let url = root.appendingPathComponent(path)
        try fm.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
        try Data(path.utf8).write(to: url)
    }

    var found: [String] = []
    let base = root.resolvingSymlinksInPath().path + "/"
    if let e = fm.enumerator(at: root, includingPropertiesForKeys: [.isRegularFileKey]) {
        for case let url as URL in e {
            let isFile = (try? url.resourceValues(forKeys: [.isRegularFileKey]))?.isRegularFile ?? false
            if isFile { found.append(url.resolvingSymlinksInPath().path.replacingOccurrences(of: base, with: "")) }
        }
    }
    return found.sorted()
}
