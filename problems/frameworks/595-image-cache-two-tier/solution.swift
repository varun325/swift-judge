import Foundation

final class Box { let value: String; init(_ v: String) { value = v } }

actor ImageStore {
    private let memory = NSCache<NSString, Box>()
    private let folder: URL
    private(set) var downloads = 0

    init() {
        folder = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try? FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
    }

    func image(_ key: String) async -> (String, String) {
        if let hit = memory.object(forKey: key as NSString) { return (hit.value, "memory") }
        let file = folder.appendingPathComponent(key)
        if let data = try? Data(contentsOf: file) {
            let value = String(decoding: data, as: UTF8.self)
            memory.setObject(Box(value), forKey: key as NSString)
            return (value, "disk")
        }
        downloads += 1
        let value = "img:\(key)"
        try? Data(value.utf8).write(to: file, options: .atomic)
        memory.setObject(Box(value), forKey: key as NSString)
        return (value, "network")
    }

    func purgeMemory() { memory.removeAllObjects() }
    func purgeDisk() {
        try? FileManager.default.removeItem(at: folder)
        try? FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
    }
    func cleanup() { try? FileManager.default.removeItem(at: folder) }
}

func twoTierCache(_ requests: [String]) async -> [String] {
    let store = ImageStore()
    var log: [String] = []
    for r in requests {
        let p = r.split(separator: " ").map(String.init)
        switch p[0] {
        case "get" where p.count == 2: log.append(await store.image(p[1]).1)
        case "purge-memory": await store.purgeMemory()
        case "purge-disk": await store.purgeDisk()
        default: break
        }
    }
    log.append("downloads \(await store.downloads)")
    await store.cleanup()
    return log
}
